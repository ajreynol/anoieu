"""The vocabulary a fixed signature offers the generator.

The fuzzer does not know what CPC means and does not try to. What it does need
is a list of names it may write down, and a rough idea of where each one fits:
`or` takes Bools, `str.++` takes sequences, `refl` is a rule with one argument
and no premises. All of that is in the declarations themselves, and anoieu
already reads those -- so this module is a projection of
`anoieu.model.Signature` onto the handful of facts a generator uses, and
nothing else. It is the only place anoieu-fuzz touches the analyzer, and it
touches the front end rather than the checks.

Types are used the way a parser uses them: as *shapes*, to pick an argument
that is at least plausible. Anything a shape does not settle -- a type
parameter, a dependent return type, an `eo::` computation -- becomes the
wildcard sort `?`, which matches everything. That is the whole type discipline
here, and it is meant to be shallow. A generator that produced only well-typed
terms would only ever ask a checker the questions it was built to answer.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

WILDCARD = "?"

# Ethos knows these without being told. `Type` is the sort of sorts, `Bool` the
# sort every proof is about; everything else a signature declares for itself.
BUILTIN_SORTS = ("Bool",)

# One value per literal category, enough to write the category down. The
# categories themselves are declared by `declare-consts`, so which of these are
# in play is a fact about the signature rather than about Eunoia.
LITERAL_VALUES = {
    "<numeral>": ("0", "1", "7", "1000000000000000000000"),
    "<rational>": ("1/2", "0/1", "-3/4"),
    "<decimal>": ("0.0", "1.5", "-2.25"),
    "<binary>": ("#b0", "#b101", "#b11111111"),
    "<hexadecimal>": ("#x0", "#x1f", "#xdeadbeef"),
    "<string>": ('""', '"a"', '"a\\u{7}b"'),
}


@dataclass(frozen=True)
class Op:
    """A declared symbol, as something to apply.

    `args` is one sort per argument, `ret` the sort of the application. `kind`
    is how the parser wants it written: `plain` is `(f a b)`, `nary` takes any
    number of arguments, `binder` wants a variable list first.
    """

    name: str
    args: tuple[str, ...]
    ret: str
    kind: str = "plain"  # plain | nary | binder

    @property
    def arity(self) -> int:
        return len(self.args)


@dataclass(frozen=True)
class Rule:
    """A proof rule, as something to write a `step` for."""

    name: str
    premises: int
    args: int
    premise_list: bool = False
    sorry: bool = False


@dataclass
class Vocabulary:
    """Everything the generator may write down, and where it fits."""

    name: str = "builtin"
    sorts: list[str] = field(default_factory=list)  # ground sorts
    sort_ctors: list[Op] = field(default_factory=list)  # sorts that take sorts
    ops: list[Op] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    literals: dict[str, str] = field(default_factory=dict)  # category -> sort

    # -- indexes, built once

    by_ret: dict[str, list[Op]] = field(default_factory=dict)
    nullary: dict[str, list[Op]] = field(default_factory=dict)

    def index(self) -> "Vocabulary":
        self.by_ret = {}
        self.nullary = {}
        for op in self.ops:
            self.by_ret.setdefault(op.ret, []).append(op)
            if op.arity == 0:
                self.nullary.setdefault(op.ret, []).append(op)
        return self

    def ops_returning(self, sort: str) -> list[Op]:
        """Every operator whose application could have this sort.

        The wildcard matches in both directions: an operator whose return type
        is a parameter could return anything, and a request for `?` will take
        anything.
        """
        if sort == WILDCARD:
            return self.ops
        return self.by_ret.get(sort, []) + self.by_ret.get(WILDCARD, [])

    def all_names(self) -> list[str]:
        return (
            [op.name for op in self.ops]
            + [op.name for op in self.sort_ctors]
            + list(self.sorts)
            + [r.name for r in self.rules]
        )


# -- reading one out of a signature ------------------------------------------

_NARY = {
    ":left-assoc",
    ":right-assoc",
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
    ":chainable",
    ":pairwise",
    ":arg-list",
}

_TOKEN = re.compile(r"[^\s()]+")


def _sort_key(node, params: set[str]) -> str:
    """A type as a sort name, or the wildcard where a parameter stands in it.

    A type mentioning a parameter is a *family* of types, and which member a
    given application has is exactly the question a type checker answers and
    this does not. So it answers `?`, and the generator treats it as "anything".
    """
    if node is None:
        return WILDCARD
    text = str(node)
    if not text or text.startswith("eo::"):
        return WILDCARD
    for tok in _TOKEN.findall(text):
        if tok in params or tok.startswith("eo::"):
            return WILDCARD
    return text


def from_signature(sig, name: str = "") -> Vocabulary:
    """Project a loaded signature onto what a generator can use."""
    from anoieu.shape import arrow_parts, strip_requires  # noqa: PLC0415

    voc = Vocabulary(name=name or os.path.basename(getattr(sig, "root", "") or "?"))
    voc.sorts = list(BUILTIN_SORTS)

    for decl in getattr(sig, "decls", []):
        if decl.kind not in ("const", "parameterized-const"):
            continue
        params = {p.name for p in decl.params}
        typ = strip_requires(decl.type)
        parts = arrow_parts(typ)
        if parts is None:
            args, ret = (), _sort_key(typ, params)
        else:
            args = tuple(_sort_key(p, params) for p in parts[:-1])
            ret = _sort_key(parts[-1], params)
        keys = {a.key for a in decl.attrs}
        kind = "plain"
        if ":binder" in keys or ":let-binder" in keys:
            kind = "binder"
        elif keys & _NARY:
            kind = "nary"
        if ret == "Type":
            op = Op(decl.name, args, ret, kind)
            if args:
                voc.sort_ctors.append(op)
            elif decl.name not in voc.sorts:
                voc.sorts.append(decl.name)
            continue
        voc.ops.append(Op(decl.name, args, ret, kind))

    for rule in getattr(sig, "rules", []):
        voc.rules.append(
            Rule(
                name=rule.name,
                premises=len(rule.premises),
                args=len(rule.args),
                premise_list=rule.premise_list is not None,
                sorry=any(a.key == ":sorry" for a in rule.attrs),
            )
        )

    for lit in getattr(sig, "literals", []):
        if lit.category in LITERAL_VALUES:
            voc.literals[lit.category] = _sort_key(lit.type, set())

    return voc.index()


def load(path: str | list[str], name: str = "") -> tuple[Vocabulary, str]:
    """Read a signature and return its vocabulary, plus a note about how it went.

    A signature that will not load is not a reason to stop: the fallback
    vocabulary below is enough to fuzz a parser, and a checker that cannot read
    its own signature is somebody's finding rather than ours.
    """
    try:
        from anoieu.loader import load as load_signature  # noqa: PLC0415

        res = load_signature(path)
    except Exception as e:  # the analyzer is a dependency, not an authority
        return fallback(), f"could not read {path}: {type(e).__name__}: {e}"
    voc = from_signature(res.signature, name)
    note = (
        f"{voc.name}: {len(voc.ops)} operators, {len(voc.rules)} rules, "
        f"{len(voc.sorts)} sorts"
    )
    bad = [d for d in res.diagnostics if getattr(d.severity, "name", "") == "ERROR"]
    if bad:
        note += f" ({len(bad)} error(s) reading it, which we ignore)"
    return voc, note


def fallback() -> Vocabulary:
    """A vocabulary for when there is no signature: enough Eunoia to be Eunoia.

    Everything here is either builtin to ethos or declared by the prelude the
    generator emits with it, so a case built from this vocabulary stands on its
    own -- which is what the signature-writing mode and the test suite need.
    """
    voc = Vocabulary(name="builtin")
    voc.sorts = ["Bool", "Int"]
    voc.ops = [
        Op("true", (), "Bool"),
        Op("false", (), "Bool"),
        Op("not", ("Bool",), "Bool"),
        Op("and", ("Bool", "Bool"), "Bool", "nary"),
        Op("or", ("Bool", "Bool"), "Bool", "nary"),
        Op("=>", ("Bool", "Bool"), "Bool", "nary"),
        Op("=", (WILDCARD, WILDCARD), "Bool"),
        Op("ite", ("Bool", WILDCARD, WILDCARD), WILDCARD),
    ]
    voc.rules = []
    voc.literals = {"<numeral>": "Int"}
    return voc.index()


#: The `declare-const` commands the fallback vocabulary assumes are in scope.
FALLBACK_PRELUDE = (
    "(declare-const Int Type)",
    "(declare-consts <numeral> Int)",
    "(declare-const not (-> Bool Bool))",
    "(declare-const and (-> Bool Bool Bool) :right-assoc-nil true)",
    "(declare-const or (-> Bool Bool Bool) :right-assoc-nil false)",
    "(declare-const => (-> Bool Bool Bool) :right-assoc)",
    "(declare-parameterized-const = ((A Type :implicit)) (-> A A Bool))",
    "(declare-parameterized-const ite ((A Type :implicit)) (-> Bool A A A))",
)
