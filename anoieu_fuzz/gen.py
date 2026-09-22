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

from anoieu_analyzer.syntax.parser import Node, parse

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


def unwrap(commands: list[str]) -> list[str]:
    """`( <command>* )` -> `<command>*`, which is how cvc5 emits a proof.

    `cvc5 --dump-proofs --proof-format=cpc` prints `unsat` and then the whole
    proof inside one outer pair of parentheses. Read literally that is a single
    top-level form, so a mutator working at command granularity has exactly one
    command to work with and a shrinker has nothing to remove.

    Only the wrapper is removed, and only when what is inside it is a list of
    forms -- the same rule logos's `unwrapProof` applies. The wrapped file is
    still worth asking about as it stands, which is why this is applied to the
    copy a run mutates and not to the copy it checks first.
    """
    if len(commands) != 1:
        return commands
    outer = commands[0].strip()
    if not (outer.startswith("(") and outer.endswith(")")):
        return commands
    body = outer[1:-1].strip()
    if not body.startswith("("):
        return commands
    inner = split_commands(body)
    return inner if len(inner) > 1 else commands


# -- the surface the two checkers may differ on -------------------------------


@dataclass(frozen=True)
class Feature:
    """One thing a proof may do, with the declarations that let it do it.

    `decls` are commands and `terms` are Bool terms written against them.
    Everything a feature needs beyond CPC it declares itself, which is what
    lets a case be assembled out of several of them without any of them
    knowing about the others.

    **The names are fixed rather than generated**, and each feature's are its
    own, so no two features collide and no two cases of one feature differ.
    That is not tidiness: a checker quotes the offending symbol back in its
    diagnostic, `checkers._portable` reduces a diagnostic to the string a
    bucket is named from, and a bare `D1` against a bare `D2` is a word
    boundary short of being normalized away. Generated indices would put one
    defect in a new directory every time it was found, which is the thing
    bucketing exists to prevent. The cost is that a case draws each feature at
    most once; the mutator's splicing is what still writes a file with two.

    `weight` is how often it is drawn. The ones that cost a case -- a feature
    that aborts a checker before it has read anything else -- are drawn rarely,
    because a case spent re-finding a bucket the corpus already has is a case
    not spent anywhere else.
    """

    name: str
    decls: tuple[str, ...] = ()
    terms: tuple[str, ...] = ("true",)
    weight: int = 2


#: Every construct a proof file may contain, as of a reading of ethos's
#: `CmdParser` and logos's `parseCommand` on 2026-09-22 and a measurement of
#: both binaries against each entry here.
#:
#: The two checkers' command tables are not the same table. Ethos takes
#: `declare-parameterized-const`, `declare-consts`, `declare-rule`, `program`,
#: `declare-datatype`, `set-option`, `echo`, `reset` and `exit` in a proof file
#: and logos takes none of them; logos takes `declare-fun`, which ethos admits
#: only in a reference file. Neither takes `define-fun`, `define-const` or
#: `define-sort` there. Which of these divergences are defects is not for this
#: table to say: it writes them down, the oracle reports what the two checkers
#: did, and a person rules.
#:
#: The entries that *agree* are not filler. A case both checkers accept is the
#: only case a mutation can push across the boundary, and the boundary is where
#: a disagreement lives -- so the agreeing shapes are what makes the disagreeing
#: ones reachable by anything other than luck.
FEATURES: tuple[Feature, ...] = (
    # -- how a symbol comes into scope
    Feature("declare-const", ("(declare-const cbool Bool)",), ("cbool",), 4),
    Feature("declare-fun", ("(declare-fun ffun (Int Int) Int)",),
            ("(= (ffun 1 1) (ffun 1 1))",)),
    Feature("declare-sort", ("(declare-sort Ssrt 0)", "(declare-const ssrt Ssrt)"),
            ("(= ssrt ssrt)",), 3),
    Feature("declare-sort-nullary-plus",
            ("(declare-sort Sone 1)", "(declare-const sone (Sone Int))"),
            ("(= sone sone)",)),
    Feature("declare-consts", ("(declare-sort Slit 0)", "(declare-consts <numeral> Slit)"),
            ("(= 1 1)",), 1),
    Feature("declare-parameterized-const",
            ("(declare-parameterized-const gpar ((T Type :implicit)) (-> T T))",),
            ("(= (gpar 1) (gpar 1))",)),
    Feature("const-attribute",
            ("(declare-const aassoc (-> Bool Bool Bool) :right-assoc-nil true)",),
            ("(aassoc true true)",)),
    Feature("overload", ("(declare-const oover Int)", "(declare-const oover Bool)"),
            ("oover", "(= oover oover)")),
    Feature("quoted-symbol", ("(declare-const |q sym| Bool)",), ("|q sym|",)),

    # -- datatypes, which is where the two most nearly agree and do not
    Feature("datatype-ground",
            ("(declare-datatypes ((Dgrd 0)) (((cgrd (sgrd Int)) (egrd))))",),
            ("(= egrd egrd)", "(= (sgrd (cgrd 1)) 1)", "((_ is cgrd) egrd)"), 3),
    Feature("datatype-parametric",
            ("(declare-datatypes ((Dpar 1)) ((par (T) ((cpar (spar T)) (epar)))))",
             "(declare-const dpar (Dpar Int))"),
            ("(= dpar dpar)", "((_ is cpar) dpar)"), 3),
    Feature("datatype-parametric-binary",
            ("(declare-datatypes ((Dprb 2)) ((par (A B) ((cprb (fprb A) (gprb B))))))",),
            ("(= 1 1)",)),
    Feature("datatype-mutual",
            ("(declare-datatypes ((Amut 0) (Bmut 0))"
             " (((camut (sbmut Bmut))) ((cbmut (samut Amut)) (ebmut))))",),
            ("(= ebmut ebmut)", "(= (samut (cbmut (camut ebmut))) (camut ebmut))")),
    Feature("datatype-singular",
            ("(declare-datatype Dsng ((csng (ssng Int)) (esng)))",),
            ("(= esng esng)",)),
    Feature("datatype-updater",
            ("(declare-datatypes ((Dupd 0)) (((cupd (supd Int)) (eupd))))",),
            ("(= ((_ update supd) (cupd 1) 2) (cupd 2))",)),

    # -- definitions and programs
    Feature("define-nullary", ("(define dnil () (= 1 1))",), ("dnil",), 3),
    Feature("define-params", ("(define dprm ((x Bool)) (= x x))",), ("(dprm true)",), 3),
    Feature("declare-rule",
            ("(declare-rule rrule ((x Bool)) :args (x) :conclusion (= x x))",),
            ("(= 1 1)",)),
    Feature("program",
            ("(declare-sort Sprg 0)", "(declare-const sprg Sprg)",
             "(program $pprg ((x Sprg)) :signature (Sprg) Sprg ((($pprg x) x)))"),
            ("(= ($pprg sprg) sprg)",)),
    Feature("smt2-define-fun", ("(define-fun dfun ((x Int)) Int x)",), ("(= 1 1)",), 1),
    Feature("smt2-define-const", ("(define-const dcon Int 1)",), ("(= dcon 1)",), 1),
    Feature("smt2-define-sort", ("(define-sort Dsrt () Int)",), ("(= 1 1)",), 1),

    # -- how a term is written
    Feature("partial-application", ("(declare-const fpap (-> Int Int Int))",),
            ("(= (fpap 1) (fpap 1))", "(= (fpap 1 1) (fpap 1 1))"), 3),
    Feature("higher-order-argument",
            ("(declare-const fhoa (-> Int Int Int))",
             "(declare-const Phoa (-> (-> Int Int) Bool))"),
            ("(Phoa (fhoa 1))",), 3),
    Feature("apply-marker", ("(declare-const fmrk (-> Int Int Int))",),
            ("(= (_ (_ fmrk 1) 1) (fmrk 1 1))",), 3),
    Feature("function-equality",
            ("(declare-const feqa (-> Int Int Int))",
             "(declare-const feqb (-> Int Int Int))"),
            ("(= feqa feqb)", "(= feqa feqa)")),
    Feature("indexed-operator", ("(declare-const vidx (BitVec 4))",),
            ("(= ((_ extract 1 0) vidx) #b00)", "(= (_ (_ extract 1 0) vidx) #b00)")),
    Feature("type-ascription", ("(declare-sort Sasc 0)", "(declare-const sasc Sasc)"),
            ("(= (as sasc Sasc) sasc)",), 1),
    Feature("binder", (), ("(forall ((xbnd Int)) (= xbnd xbnd))",
                           "(exists ((xbnd Int)) (= xbnd xbnd))")),
    Feature("lambda", ("(declare-const Plam (-> (-> Int Int) Bool))",),
            ("(Plam (lambda ((xlam Int)) xlam))",)),
    Feature("eo-builtin", (), ("(= (eo::add 1 1) 2)", "(= (eo::define ((xeo 1)) xeo) 1)",
                               "(= (eo::list_len and (and true true)) 2)")),

    # -- the theory sorts a case may name
    Feature("sequence-sort", ("(declare-const sqseq (Seq Int))",), ("(= sqseq sqseq)",)),
    Feature("array-sort", ("(declare-const ararr (Array Int Int))",),
            ("(= (select ararr 1) (select ararr 1))",)),
    Feature("set-sort", ("(declare-const stset (Set Int))",), ("(= stset stset)",)),
    Feature("literal", (), ('(= (str.len "\\u{61}b") 2)', "(= 1.5 1.5)", "(= #x1f #x1f)",
                            "(= 100000000000000000000000 100000000000000000000000)",
                            "(= (- 1) (- 1))"), 3),

    # -- commands that are not about a symbol at all
    Feature("set-option", ("(set-option :normalize-num true)",), ("(= 1 1)",), 1),
    Feature("echo", ('(echo "anoieu-fuzz")',), ("(= 1 1)",), 1),
    Feature("exit", (), ("(= 1 1)",), 1),
    Feature("reset", ("(reset)",), ("(= 1 1)",), 1),
)

#: Emitted after the refutation rather than before it.
TRAILING = {"exit"}


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

    # -- feature cases

    def feature_case(self) -> list[str]:
        """A proof both checkers should check, built around one thing they may not.

        The proof generator above writes files that die at their first command.
        Against ethos and logos on CPC it is refused by both about ninety-nine
        times in a hundred, and two checkers that both refuse a file agree about
        it: a run of it reports crashes and nothing else. A differential oracle
        only says something at the *boundary* -- a file one checker takes and the
        other does not -- and nothing arrives at the boundary by accident.

        So this writes the boundary on purpose. The frame is a refutation both
        checkers check without complaint,

            (assume @a F) (assume @b (not F))
            (step @c false :rule contra :premises (@a @b))

        and `F`, together with the declarations under it, is drawn from
        `FEATURES`. What the two checkers then say about the file is what they
        say about the features in it, because the frame around them is one they
        have both already agreed about.

        It is still a fuzzer rather than a fixture, and `wild` is how much:
        how often the formula is replaced by a generated term instead, whether
        the declarations are left in the order they were written, whether the
        closing step states its conclusion, and whether something harmless is
        in the way. What a case of this shape is really for is the mutator --
        a case both checkers accepted is the only case a single edit can push
        *across* the boundary, and `Session.learn` keeps it for exactly that.
        """
        picked = self._pick_features(self.rng.choice((1, 1, 2, 2, 3)))
        head: list[str] = []
        tail: list[str] = []
        terms: list[str] = []
        for feat in picked:
            (tail if feat.name in TRAILING else head).extend(feat.decls)
            terms.append(self.rng.choice(feat.terms))

        if self.chance(self.wild) or not terms:
            formula = self.term("Bool")
        elif len(terms) == 1:
            formula = terms[0]
        else:
            formula = "(and " + " ".join(terms) + ")"

        if self.chance(self.wild):
            # Declaration order is a question in its own right -- a datatype
            # used before the block that declares it, a definition read before
            # the symbol it names -- and it is one neither checker has to
            # answer the same way.
            self.rng.shuffle(head)

        a, b, c = self.fresh("@a"), self.fresh("@b"), self.fresh("@c")
        body = [f"(assume {a} {formula})", f"(assume {b} (not {formula}))"]
        if self.chance(0.15):
            # A step that checks and is never used. It is here because a file
            # whose every command matters is a file that exercises no path for
            # ignoring one.
            body.append(f"(step {self.fresh('@r')} :rule refl :args ({terms[0]}))")
        body.append(f"(step {c}{self._conclusion()} :rule contra :premises ({a} {b}))")
        return head + body + tail

    def _conclusion(self) -> str:
        """What the closing step says it proves -- which it need not say at all.

        `contra` derives `false` from a formula and its negation, so `false` is
        the conclusion this frame is built to have, and leaving it out is the
        other way the same proof is written. `wild` is how often the case states
        a *third* thing: a conclusion the rule does not derive, or one naming a
        symbol nothing declared. A checker that reads the annotation has to
        refuse such a file; one that ignores it cannot tell the difference. The
        frame is otherwise too well-behaved to ask.
        """
        if self.chance(self.wild):
            return " " + self.rng.choice(
                ("true", "(= 1 2)", "nosuchsymbol", "(not false)")
            )
        return "" if self.chance(0.3) else " false"

    def _pick_features(self, k: int) -> list[Feature]:
        """`k` distinct features, by weight.

        Distinct because a feature's symbols are its own and fixed, so drawing
        one twice would write the same declaration twice -- which is a question
        worth asking a checker, but the mutator's splicing asks it already and
        this would spend a case on it every time.
        """
        pool = [f for f in FEATURES for _ in range(f.weight)]
        picked: list[Feature] = []
        while pool and len(picked) < k:
            feat = self.rng.choice(pool)
            picked.append(feat)
            pool = [f for f in pool if f.name != feat.name]
        return picked

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

    def _fun_type(self, arity: int) -> tuple[str, list[str], str]:
        args = [self.sort() for _ in range(arity)]
        ret = self.sort()
        if not args:
            return ret, [], ret
        return f"(-> {' '.join(args)} {ret})", args, ret

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
        typ, args, ret = self._fun_type(arity)
        op = Op(name, tuple(args), ret)
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
    features: float = 0.5,
) -> Case:
    rng = random.Random(seed)
    standalone = voc is None or voc.name == "builtin"
    if mode == "signature":
        # a copy: a signature case writes into its vocabulary as it declares
        gen = Generator(rng, (voc or fallback()).copy(), wild=wild, depth=depth)
        return Case(gen.signature_case(include), mode, ".eo", seed, "generated")
    gen = Generator(rng, voc, wild=wild, depth=depth)
    # `FEATURES` is written against CPC -- `BitVec`, `Seq`, `str.len`, `extract`
    # -- so a run with no signature loaded, which is what the test suite and
    # `--signature ""` are, gets the generator that carries its own prelude.
    if not standalone and rng.random() < features:
        return Case(gen.feature_case(), mode, ".cpc", seed, "feature")
    return Case(gen.proof_case(prelude=standalone), mode, ".cpc", seed, "generated")


def feature_commands() -> list[str]:
    """Every declaration `FEATURES` can write, once.

    The mutator splices a command from one case into another, and what it has
    to splice is whatever the seed corpus happened to contain. These are worth
    adding to that pool on their own: a real cvc5 proof with a parametric
    datatype block dropped into the middle of it is a file nobody would write
    and both checkers have an opinion about.
    """
    out: list[str] = []
    for feat in FEATURES:
        out.extend(feat.decls)
    return out


# -- mutation -----------------------------------------------------------------

_ATOM = re.compile(r"[^\s()]+")


def _term_roots(form: Node) -> list[Node]:
    """Value positions, leaving command names, bindings and file paths intact."""
    roots: list[Node] = []
    if form.head in {"assume", "assume-push", "step", "step-pop"}:
        conclusion = form.at(2)
        if conclusion is not None and not conclusion.is_keyword:
            roots.append(conclusion)
        for i, child in enumerate(form.children[:-1]):
            if child.text == ":args":
                roots.extend(form.children[i + 1].children)
    elif form.head == "define" and form.at(3) is not None:
        roots.append(form.children[3])
    elif form.head == "declare-rule":
        for i, child in enumerate(form.children[:-1]):
            if child.text in {":conclusion", ":conclusion-explicit"}:
                roots.append(form.children[i + 1])
    elif form.head == "program":
        name = form.at(1)
        for group in form.children:
            for pair in group.children:
                if (len(pair.children) == 2 and name is not None
                        and pair.children[0].head == name.text):
                    roots.append(pair.children[1])
    return roots


def mutate_term(rng: random.Random, commands: list[str]) -> list[str]:
    """Edit one parsed value without damaging the surrounding command syntax.

    No parser recovery is used as evidence of a valid mutation. Strings and
    quoted symbols are indivisible tokens; replacements use whole node spans.
    Types and proof validity can change, which is what the checkers are asked.
    """
    choices: list[tuple[int, Node, list[Node]]] = []

    def values(node: Node):
        if not node.is_keyword:
            yield node
        for child in node.children[1:]:
            yield from values(child)

    for i, command in enumerate(commands):
        parsed = parse("<mutation>", command)
        if parsed.diagnostics or len(parsed.forms) != 1:
            continue
        roots = _term_roots(parsed.forms[0])
        nodes = [node for root in roots for node in values(root)]
        choices.extend((i, node, nodes) for node in nodes)
    if not choices:
        return list(commands)
    i, node, nodes = rng.choice(choices)
    if node.literal_category in LITERAL_VALUES:
        replacements = [v for v in LITERAL_VALUES[node.literal_category] if v != str(node)]
    elif node.is_list and len(node.children) > 1:
        args = [str(n) for n in node.children[1:]]
        j = rng.randrange(len(args))
        replacements = [args[j]]
        replacements.append(f"({node.children[0]} {' '.join(args[:j] + args[j + 1:])})")
        replacements.append(f"({node.children[0]} {' '.join(args[:j] + [args[j]] + args[j:])})")
        if len(args) > 1:
            args[j], args[(j + 1) % len(args)] = args[(j + 1) % len(args)], args[j]
            replacements.append(f"({node.children[0]} {' '.join(args)})")
    else:
        replacements = [str(n) for n in nodes if n.is_atom and str(n) != str(node)]
        replacements.extend(["true", "false"])
    replacements = [text for text in replacements if text != str(node)]
    if not replacements:
        return list(commands)
    lines = commands[i].splitlines(keepends=True)
    start = sum(map(len, lines[:node.line - 1])) + node.col - 1
    end = sum(map(len, lines[:node.end_line - 1])) + node.end_col - 1
    out = list(commands)
    out[i] = commands[i][:start] + rng.choice(replacements) + commands[i][end:]
    return out


def mutate(seed: str, base: Case, pool: list[str], rounds: int = 3,
           mode: str = "mixed") -> Case:
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
        what = "term" if mode == "terms" else rng.choice(
            ("drop", "dup", "swap", "splice", "rename", "truncate", "paren", "atom",
             "term", "term", "term", "term"))
        i = rng.randrange(len(cmds))
        if what == "term":
            cmds = mutate_term(rng, cmds)
        elif what == "drop":
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
