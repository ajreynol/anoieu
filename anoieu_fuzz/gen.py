"""Writing files nobody would write.

Two generators, because there are two questions to ask a checker.

**Proofs** (`proof`) are written against a signature the checkers already
agree on -- CPC, say -- so the file itself declares only its own constants and
then assumes and steps. Two checkers reading the same such file should reach
the same verdict, and that is the whole oracle.

**Signatures** (`signature`) are written from nothing: `declare-const`,
`declare-rule`, `program`, attributes attached to symbols that cannot carry
them. There is no second checker for these, so what they are looking for is a
checker falling over rather than a checker disagreeing.

Both produce a `Case`: a list of top-level commands, in order. Keeping a case
as a *list* rather than as text is what makes shrinking a five-line function
(`triage.ddmin`) instead of a parser.

Neither generator knows what any of it means. Types are followed where
`vocab` recorded one, ignored with probability `wild`, and the result is
handed over without being read back. A generator that only wrote sensible
files would only ever ask a checker what it already answers.
"""

from __future__ import annotations

import os
import random
import re
from dataclasses import dataclass, field

from .vocab import LITERAL_VALUES, WILDCARD, Op, Rule, Vocabulary, fallback

# Every attribute ethos parses, and a few it does not. The point of the last
# few is that ethos accepts an unknown attribute with a warning and ignores it,
# so a generator that only wrote known ones would never exercise that path.
ATTRS = [
    ":left-assoc",
    ":right-assoc",
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
    ":chainable",
    ":pairwise",
    ":binder",
    ":let-binder",
    ":arg-list",
    ":opaque",
    ":restrict",
    ":is_eq",
    ":syntax",
    ":unknown-attribute",
]

# Attributes that want a term after them. The generator supplies one about as
# often as it does not, because "the attribute with no value" is its own path
# through the parser.
ATTRS_WITH_VALUE = {
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
    ":chainable",
    ":binder",
    ":let-binder",
    ":restrict",
}

LIT_CATEGORIES = tuple(LITERAL_VALUES)


@dataclass
class Case:
    """One file, as the commands it is made of."""

    commands: list[str]
    mode: str = "proof"
    suffix: str = ".cpc"
    seed: str = ""
    source: str = "generated"
    notes: list[str] = field(default_factory=list)

    def text(self) -> str:
        header = [f"; anoieu-fuzz {self.mode} case, seed {self.seed} ({self.source})"]
        return "\n".join(header + list(self.commands)) + "\n"

    def replace(self, commands: list[str]) -> "Case":
        """The same case, with a different command list. Provenance survives."""
        return Case(
            commands=list(commands),
            mode=self.mode,
            suffix=self.suffix,
            seed=self.seed,
            source=self.source,
            notes=list(self.notes),
        )


# -- splitting a file back into commands --------------------------------------


def split_commands(text: str) -> list[str]:
    """Every top-level form of a file, as text, comments and all.

    A hand-written seed is not one command per line, and a shrinker that works
    on lines would cut a term in half. This is the paren matcher that makes
    "delete a command" mean what it says: it knows that `;` runs to the end of
    the line, that `"..."` and `|...|` may hold anything, and that `\\` escapes
    inside a string.
    """
    out: list[str] = []
    depth = 0
    start = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == ";":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == '"':
            i += 1
            while i < n:
                if text[i] == "\\" and i + 1 < n:
                    i += 2
                    continue
                if text[i] == '"':
                    break
                i += 1
            i += 1
            continue
        if c == "|":
            i += 1
            while i < n and text[i] != "|":
                i += 1
            i += 1
            continue
        if c == "(":
            if depth == 0:
                start = i
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                out.append(text[start : i + 1])
            elif depth < 0:
                depth = 0  # an unbalanced seed is still worth mutating
        i += 1
    if depth > 0:
        out.append(text[start:])  # a truncated last form: keep it as it stands
    return out


_INCLUDE = re.compile(r'\((include|reference)\s+"([^"]*)"')


def absolutize(commands: list[str], base: str) -> list[str]:
    """Make a seed's `include` and `reference` paths absolute.

    A case is written to a temporary file and handed to a checker from there,
    so a seed that says `(include "../theories/Builtin.eo")` would be asking
    about a file that is not where it was. Every checker then fails to open it,
    which is a finding about this harness rather than about anything else --
    and it was the first thing the harness reported, before this existed.
    """

    def fix(m: "re.Match[str]") -> str:
        path = m.group(2)
        if not path or os.path.isabs(path):
            return m.group(0)
        return f'({m.group(1)} "{os.path.normpath(os.path.join(base, path))}"'

    return [_INCLUDE.sub(fix, c) for c in commands]


# -- the generator ------------------------------------------------------------


class Generator:
    """Everything random, driven by one seeded `random.Random`.

    One generator serves one case, so its symbol table -- what this file has
    declared so far -- is instance state and a case is reproducible from its
    seed alone.
    """

    def __init__(
        self,
        rng: random.Random,
        voc: Vocabulary | None = None,
        wild: float = 0.1,
        depth: int = 3,
    ) -> None:
        self.rng = rng
        self.voc = voc or fallback()
        self.wild = wild
        self.max_depth = depth
        self.consts: dict[str, list[str]] = {}
        self.sorts: list[str] = list(self.voc.sorts)
        self.proofs: list[str] = []
        self.n = 0

    # -- small helpers

    def fresh(self, stem: str) -> str:
        self.n += 1
        return f"{stem}{self.n}"

    def pick(self, xs):
        return self.rng.choice(xs) if xs else None

    def chance(self, p: float) -> bool:
        return self.rng.random() < p

    def sort(self) -> str:
        """Some sort: a declared one, or an application of a sort constructor."""
        if self.voc.sort_ctors and self.chance(0.15):
            ctor = self.rng.choice(self.voc.sort_ctors)
            args = " ".join(
                self.sort() if a == "Type" else self.term(a, 1) for a in ctor.args
            )
            return f"({ctor.name} {args})"
        return self.rng.choice(self.sorts) if self.sorts else "Bool"

    # -- terms

    def literal(self, sort: str) -> str | None:
        cats = [c for c, s in self.voc.literals.items() if sort in (s, WILDCARD)]
        if sort == WILDCARD:
            cats = list(self.voc.literals)
        if not cats:
            return None
        return self.rng.choice(LITERAL_VALUES[self.rng.choice(cats)])

    def leaf(self, sort: str) -> str:
        """An atom of this sort, or something that could pass for one."""
        pool: list[str] = list(self.consts.get(sort, ()))
        pool += [op.name for op in self.voc.nullary.get(sort, ())]
        if sort == WILDCARD or self.chance(self.wild):
            for names in self.consts.values():
                pool += names
            pool += [op.name for op in self.voc.ops if op.arity == 0]
        lit = self.literal(sort)
        if lit is not None and (not pool or self.chance(0.3)):
            return lit
        if pool:
            return self.rng.choice(pool)
        if sort == "Bool":
            return self.rng.choice(("true", "false"))
        # Nothing in scope has this sort. Naming something undeclared is a
        # perfectly good question to ask a checker, so ask it.
        return self.fresh("u")

    def term(self, sort: str = WILDCARD, depth: int | None = None) -> str:
        if depth is None:
            depth = self.max_depth
        if self.chance(self.wild):
            sort = WILDCARD
        if depth <= 0 or self.chance(0.35):
            return self.leaf(sort)
        ops = self.voc.ops_returning(sort)
        if not ops:
            return self.leaf(sort)
        return self.apply(self.rng.choice(ops), depth)

    def apply(self, op: Op, depth: int) -> str:
        if op.kind == "binder" and op.args:
            var = self.fresh("v")
            body = self.term(op.args[-1], depth - 1)
            return f"({op.name} (({var} {self.sort()})) {body})"
        if op.kind == "nary":
            k = self.rng.choice((0, 1, 2, 2, 3, 4))
            arg = op.args[0] if op.args else WILDCARD
            args = [self.term(arg, depth - 1) for _ in range(k)]
        else:
            args = [self.term(a, depth - 1) for a in op.args]
            if self.chance(self.wild):  # the wrong number of arguments
                if args and self.chance(0.5):
                    args.pop()
                else:
                    args.append(self.term(WILDCARD, depth - 1))
        if not args:
            return op.name if self.chance(0.5) else f"({op.name})"
        return f"({op.name} {' '.join(args)})"

    # -- proof cases

    def proof_case(self, prelude: bool = False) -> list[str]:
        cmds: list[str] = []
        if prelude:
            from .vocab import FALLBACK_PRELUDE  # noqa: PLC0415

            cmds += list(FALLBACK_PRELUDE)
        for _ in range(self.rng.randint(0, 1)):
            name = self.fresh("S")
            cmds.append(f"(declare-sort {name} 0)")
            self.sorts.append(name)
        for _ in range(self.rng.randint(1, 5)):
            sort = self.sort()
            name = self.fresh("c")
            cmds.append(f"(declare-const {name} {sort})")
            self.consts.setdefault(sort, []).append(name)
        if self.chance(0.2):
            name = self.fresh("d")
            cmds.append(f"(define {name} () {self.term()})")
            self.consts.setdefault(WILDCARD, []).append(name)
        depth = 0
        for _ in range(self.rng.randint(1, 8)):
            if not self.proofs or self.chance(0.3):
                push = self.chance(0.2)
                pid = self.fresh("@p")
                cmds.append(
                    f"({'assume-push' if push else 'assume'} {pid} {self.term('Bool')})"
                )
                self.proofs.append(pid)
                depth += 1 if push else 0
            else:
                pop = depth > 0 and self.chance(0.3)
                cmds.append(self.step("step-pop" if pop else "step"))
                depth -= 1 if pop else 0
        return cmds

    def step(self, kind: str = "step") -> str:
        pid = self.fresh("@p")
        rule = self.pick(self.voc.rules)
        parts = [kind, pid]
        if rule is None or self.chance(0.6):
            parts.append(self.term("Bool"))
        parts.append(":rule")
        parts.append(rule.name if rule else self.fresh("r"))
        want_p = rule.premises if rule else self.rng.randint(0, 2)
        if rule and rule.premise_list:
            want_p = self.rng.randint(1, 3)
        if self.chance(self.wild):
            want_p = max(0, want_p + self.rng.choice((-1, 1)))
        if want_p and self.proofs:
            prem = [self.rng.choice(self.proofs) for _ in range(want_p)]
            parts.append(f":premises ({' '.join(prem)})")
        want_a = rule.args if rule else self.rng.randint(0, 2)
        if self.chance(self.wild):
            want_a = max(0, want_a + self.rng.choice((-1, 1)))
        if want_a:
            args = [self.term() for _ in range(want_a)]
            parts.append(f":args ({' '.join(args)})")
        self.proofs.append(pid)
        return "(" + " ".join(parts) + ")"

    # -- signature cases

    def signature_case(self, include: str = "") -> list[str]:
        # A signature that declares nothing declares nothing to go wrong with:
        # every term in it names a symbol that is not there, and ethos stops at
        # the first one. So a case opens with a prelude and the generated part
        # is written against symbols that exist.
        #
        # Which prelude is the whole difference between two experiments. The
        # default is the handful of declarations `vocab.fallback()` describes,
        # and what it reaches is the front end. `include` instead opens the case
        # with a real signature -- CPC, 190 declarations and 241 programs -- so
        # what follows is nonsense written in a language the checker knows well,
        # and the type checker has something to do.
        from .vocab import FALLBACK_PRELUDE  # noqa: PLC0415

        cmds: list[str] = [f'(include "{include}")'] if include else list(FALLBACK_PRELUDE)
        for _ in range(self.rng.randint(1, 2)):
            name = self.fresh("S")
            cmds.append(f"(declare-const {name} Type)")
            self.sorts.append(name)
        # A category the vocabulary already has is a category ethos aborts on,
        # by a path that is already a promoted finding -- and against a real
        # signature that is most of them, so generating one would spend a fifth
        # of every run re-finding it. Take a category nobody has claimed.
        free = [c for c in LIT_CATEGORIES if c not in self.voc.literals]
        if free and self.chance(0.4):
            cat = self.rng.choice(free)
            sort = self.sort()
            cmds.append(f"(declare-consts {cat} {sort})")
            self.voc.literals[cat] = sort
        for _ in range(self.rng.randint(2, 9)):
            cmds.append(self.signature_command())
        return cmds

    def signature_command(self) -> str:
        what = self.rng.choices(
            (
                "const",
                "param-const",
                "define",
                "rule",
                "program",
                "datatype",
                "sort",
                "misc",
            ),
            weights=(4, 3, 2, 3, 3, 1, 1, 1),
        )[0]
        return getattr(self, "_cmd_" + what.replace("-", "_"))()

    def _fun_type(self, arity: int) -> tuple[str, list[str]]:
        args = [self.sort() for _ in range(arity)]
        ret = self.sort()
        if not args:
            return ret, []
        return f"(-> {' '.join(args)} {ret})", args

    def _attrs(self) -> str:
        out = []
        for _ in range(self.rng.randint(0, 2)):
            key = self.rng.choice(ATTRS)
            if key in ATTRS_WITH_VALUE and self.chance(0.7):
                out.append(f"{key} {self.term()}")
            else:
                out.append(key)
        return (" " + " ".join(out)) if out else ""

    def _cmd_const(self) -> str:
        name = self.fresh("f")
        arity = self.rng.choice((0, 0, 1, 2, 2, 3))
        typ, args = self._fun_type(arity)
        op = Op(name, tuple(args), self.sorts[-1] if self.sorts else "Bool")
        self.voc.ops.append(op)
        self.voc.index()
        if not args:
            self.consts.setdefault(op.ret, []).append(name)
        return f"(declare-const {name} {typ}{self._attrs()})"

    def _cmd_param_const(self) -> str:
        name = self.fresh("g")
        params = [(self.fresh("T"), "Type") for _ in range(self.rng.randint(1, 2))]
        decl = " ".join(
            f"({p} {t}{' :implicit' if self.chance(0.6) else ''})" for p, t in params
        )
        arity = self.rng.choice((0, 1, 2))
        body = [self.rng.choice([p for p, _ in params] + self.sorts) for _ in range(arity)]
        ret = self.rng.choice([p for p, _ in params] + self.sorts)
        typ = f"(-> {' '.join(body)} {ret})" if body else ret
        self.voc.ops.append(Op(name, tuple(WILDCARD for _ in body), WILDCARD))
        self.voc.index()
        return f"(declare-parameterized-const {name} ({decl}) {typ}{self._attrs()})"

    def _cmd_define(self) -> str:
        name = self.fresh("h")
        params = [(self.fresh("x"), self.sort()) for _ in range(self.rng.randint(0, 2))]
        for p, s in params:
            self.consts.setdefault(s, []).append(p)
        decl = " ".join(f"({p} {s})" for p, s in params)
        body = self.term()
        for p, s in params:
            self.consts[s].remove(p)
        self.voc.ops.append(Op(name, tuple(s for _, s in params), WILDCARD))
        self.voc.index()
        typ = f" :type {self.sort()}" if self.chance(0.3) else ""
        return f"(define {name} ({decl}) {body}{typ})"

    def _cmd_rule(self) -> str:
        name = self.fresh("R")
        params = [(self.fresh("x"), self.sort()) for _ in range(self.rng.randint(0, 3))]
        for p, s in params:
            self.consts.setdefault(s, []).append(p)
        decl = " ".join(f"({p} {s})" for p, s in params)
        parts = [f"(declare-rule {name} ({decl})"]
        if self.chance(0.2):
            parts.append(f"  :assumption {self.term('Bool')}")
        if self.chance(0.5):
            n = self.rng.randint(1, 2)
            parts.append(f"  :premises ({' '.join(self.term('Bool') for _ in range(n))})")
        elif self.chance(0.2):
            parts.append(f"  :premise-list {self.term('Bool')} {self.term()}")
        if self.chance(0.5):
            n = self.rng.randint(1, 2)
            parts.append(f"  :args ({' '.join(self.term() for _ in range(n))})")
        if self.chance(0.25):
            parts.append(f"  :requires (({self.term()} {self.term()}))")
        concl = ":conclusion-explicit" if self.chance(0.15) else ":conclusion"
        parts.append(f"  {concl} {self.term('Bool')}")
        if self.chance(0.05):
            parts.append("  :sorry")
        for p, s in params:
            self.consts[s].remove(p)
        self.voc.rules.append(Rule(name, premises=0, args=0))
        return "\n".join(parts) + ")"

    def _cmd_program(self) -> str:
        name = self.fresh("$p")
        params = [(self.fresh("x"), self.sort()) for _ in range(self.rng.randint(1, 2))]
        for p, s in params:
            self.consts.setdefault(s, []).append(p)
        decl = " ".join(f"({p} {s})" for p, s in params)
        args = [s for _, s in params]
        ret = self.sort()
        cases = []
        for _ in range(self.rng.randint(1, 3)):
            lhs = f"({name} {' '.join(self.term(a, 2) for a in args)})"
            cases.append(f"(({lhs} {self.term(ret, 2)}))"[1:-1])
        for p, s in params:
            self.consts[s].remove(p)
        self.voc.ops.append(Op(name, tuple(args), ret))
        self.voc.index()
        body = " ".join(cases)
        return (
            f"(program {name} ({decl}) :signature ({' '.join(args)}) {ret}\n"
            f"  ({body})\n)"
        )

    def _cmd_datatype(self) -> str:
        name = self.fresh("D")
        self.sorts.append(name)
        ctors = []
        for _ in range(self.rng.randint(1, 2)):
            cname = self.fresh("k")
            sels = " ".join(
                f"({self.fresh('sel')} {self.sort()})" for _ in range(self.rng.randint(0, 2))
            )
            ctors.append(f"({cname}{' ' + sels if sels else ''})")
        return f"(declare-datatype {name} ({' '.join(ctors)}))"

    def _cmd_sort(self) -> str:
        name = self.fresh("S")
        arity = self.rng.choice((0, 0, 1, 2))
        if arity == 0:
            self.sorts.append(name)
        return f"(declare-sort {name} {arity})"

    def _cmd_misc(self) -> str:
        return self.rng.choice(
            (
                '(echo "anoieu_fuzz")',
                "(set-option :normalize-num true)",
                "(set-option :no-parse-let false)",
                "(echo)",
            )
        )


# -- the two entry points -----------------------------------------------------


def generate(
    seed: str,
    mode: str = "proof",
    voc: Vocabulary | None = None,
    wild: float = 0.1,
    depth: int = 3,
    include: str = "",
) -> Case:
    rng = random.Random(seed)
    standalone = voc is None or voc.name == "builtin"
    if mode == "signature":
        # a copy: a signature case writes into its vocabulary as it declares
        gen = Generator(rng, (voc or fallback()).copy(), wild=wild, depth=depth)
        return Case(gen.signature_case(include), mode, ".eo", seed, "generated")
    gen = Generator(rng, voc, wild=wild, depth=depth)
    return Case(gen.proof_case(prelude=standalone), mode, ".cpc", seed, "generated")


# -- mutation -----------------------------------------------------------------

_ATOM = re.compile(r"[^\s()]+")


def mutate(seed: str, base: Case, pool: list[str], rounds: int = 3) -> Case:
    """Damage a case that already exists.

    Generation from a grammar reaches the parser; mutation of something that
    already checks reaches everything past it. Both are cheap, so anoieu-fuzz
    does both and lets the corpus say which pays.

    `pool` is every command from every seed file, so a mutation can splice a
    command from one proof into another -- the cheapest way to write a file
    that is locally sensible and globally not.
    """
    rng = random.Random(seed)
    cmds = list(base.commands)
    notes = []
    for _ in range(rng.randint(1, rounds)):
        if not cmds:
            break
        what = rng.choice(
            ("drop", "dup", "swap", "splice", "rename", "truncate", "paren", "atom")
        )
        i = rng.randrange(len(cmds))
        if what == "drop":
            cmds.pop(i)
        elif what == "dup":
            cmds.insert(i, cmds[i])
        elif what == "swap" and len(cmds) > 1:
            j = rng.randrange(len(cmds))
            cmds[i], cmds[j] = cmds[j], cmds[i]
        elif what == "splice" and pool:
            cmds.insert(i, rng.choice(pool))
        elif what == "rename":
            names = _ATOM.findall(cmds[i])
            if names:
                old = rng.choice(names)
                everywhere = _ATOM.findall(" ".join(cmds))
                new = rng.choice(everywhere) if everywhere else "x"
                cmds[i] = cmds[i].replace(old, new, 1)
        elif what == "truncate":
            cmds[i] = cmds[i][: max(1, rng.randrange(len(cmds[i])))]
        elif what == "paren":
            c = cmds[i]
            k = rng.randrange(len(c))
            cmds[i] = c[:k] + rng.choice("()") + c[k:]
        elif what == "atom":
            names = _ATOM.findall(cmds[i])
            if names:
                old = rng.choice(names)
                new = rng.choice(("0", "-1", '"s"', "#b1", "true", "eo::nil", "|a b|"))
                cmds[i] = cmds[i].replace(old, new, 1)
        notes.append(what)
    return Case(cmds, base.mode, base.suffix, seed, f"mutated:{base.source}", notes)


# -- metamorphic transforms ---------------------------------------------------


def reformat(seed: str, base: Case) -> Case:
    """The same file, written differently: comments and whitespace, nothing else.

    This is the one thing a fuzzer can ask a *single* checker that is still a
    differential question. Ethos's answer to a file must not depend on how the
    file is laid out, so two runs that differ are a defect without any second
    checker having an opinion.

    What it does is deliberately timid, because an aggressive rewrite is a
    rewrite whose meaning has to be argued: whitespace is inserted only
    immediately after an opening parenthesis, and only in commands that carry
    no comment and no string, so nothing can land inside a token, a `"..."`, a
    `|...|` or a `;` line.
    """
    rng = random.Random("reformat:" + seed)
    out: list[str] = []
    for cmd in base.commands:
        if rng.random() < 0.4:
            out.append(";" + " " * rng.randint(0, 3) + "anoieu_fuzz")
        safe = ";" not in cmd and '"' not in cmd and "|" not in cmd
        if safe and rng.random() < 0.7:
            cmd = re.sub(
                r"\(", lambda m: "(" + rng.choice(("", " ", "\n  ", "\t")), cmd
            )
        out.append(cmd)
    if rng.random() < 0.5:
        out.append("; anoieu-fuzz")
    return Case(out, base.mode, base.suffix, base.seed, base.source + "+reformatted",
                list(base.notes))
