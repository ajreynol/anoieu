"""Checks on the terms a signature writes, wherever they stand.

Everything here is about a term rather than a declaration: a builtin applied to
the wrong number of arguments, a literal whose category the signature never gave
a type, an evaluation the manual says cannot happen. Ethos reaches none of these
until something asks for the value or the type of the term that holds them, and
inside a program body or a rule nothing does.
"""

from __future__ import annotations

from typing import Iterator

from ..builtins import ARITHMETIC, BITWISE, EO_ARITY, SAME_CATEGORY
from ..diagnostics import Diagnostic, Severity
from ..model import Param
from ..syntax.parser import Node
from . import Context, check


def _tested(term: Node) -> set[int]:
    """Every subterm under an `(eo::is_ok X)`.

    `eo::is_ok` asks whether a term evaluates, so a term beneath one is being
    tested rather than relied on -- which is what a test suite writes, and what
    a signature writes when it branches on whether a computation succeeded.
    """
    out: set[int] = set()
    for nd in term.walk():
        if nd.is_list and nd.head == "eo::is_ok":
            for child in nd.children[1:]:
                out.update(id(x) for x in child.walk())
    return out


def _terms(ctx: Context) -> Iterator[tuple[Node, str, dict[str, Param]]]:
    """Every term a signature writes, with where it was written and the
    parameters in scope around it."""
    sig = ctx.signature
    for prog in sig.programs:
        params = {p.name: p for p in prog.params}
        for lhs, rhs in prog.cases:
            yield lhs, f"program `{prog.name}`", params
            yield rhs, f"program `{prog.name}`", params
        for arg in prog.sig_args:
            yield arg, f"the signature of `{prog.name}`", params
        if prog.sig_ret is not None:
            yield prog.sig_ret, f"the signature of `{prog.name}`", params
    for rule in sig.rules:
        params = {p.name: p for p in rule.params}
        for node in [rule.conclusion, rule.assumption, *rule.premises, *rule.args]:
            if node is not None:
                yield node, f"rule `{rule.name}`", params
        for a, b in rule.requires:
            yield a, f"rule `{rule.name}`", params
            yield b, f"rule `{rule.name}`", params
    for d in sig.defines:
        if d.body is not None:
            yield d.body, f"definition `{d.name}`", {p.name: p for p in d.params}
    for decl in sig.decls:
        if decl.type is not None:
            yield decl.type, f"the type of `{decl.name}`", {p.name: p for p in decl.params}
        for a in decl.attrs:
            if a.value is not None:
                yield a.value, f"`{a.key}` on `{decl.name}`", {p.name: p for p in decl.params}


@check(
    "EO0072",
    "a builtin operator is applied to the wrong number of arguments",
    page="""
Every `eo::` operator has the arity the user manual gives it, and an application
of another arity is a term that never evaluates -- ethos leaves it as it stands
rather than refusing it, so a rule written around one simply fails to fire, and
a program returns an application of itself.

The list operators are the easy ones to get wrong, because each takes the
operator it is about as its first argument: `eo::list_concat` takes three
arguments, not two, and `eo::nil` takes the operator and, where the nil depends
on it, a type.
""",
)
def builtin_arity(ctx: Context) -> Iterator[Diagnostic]:
    for term, where, _params in _terms(ctx):
        tested = _tested(term)
        for nd in term.walk():
            if not nd.is_list or nd.head is None or id(nd) in tested:
                continue
            bounds = EO_ARITY.get(nd.head)
            if bounds is None:
                continue
            lo, hi = bounds
            n = len(nd.children) - 1
            if n >= lo and (hi is None or n <= hi):
                continue
            want = f"{lo}" if hi == lo else (f"{lo} or more" if hi is None else f"{lo} to {hi}")
            yield Diagnostic(
                code="EO0072",
                severity=Severity.ERROR,
                message=f"`{nd.head}` takes {want} argument(s), and is applied to {n} here",
                span=nd.span,
                label="this never evaluates",
                notes=[f"in {where}"],
            )


@check(
    "EO0071",
    "a literal whose category the signature never gave a type",
    page="""
`declare-consts` is what associates a syntactic category with a type: without
`(declare-consts <numeral> Int)` a numeral in a term has no type, and the term
holding it is ill-typed the moment anything asks. Signature files do no
normalisation, so a hexadecimal literal needs `<hexadecimal>` even where
`<binary>` is declared -- the normalisation of one into the other applies to
proof and reference files only.

`<boolean>` is exempt: `true` and `false` are builtin, and so is a literal that
stands only under a computational operator: ethos distinguishes a numeral value
independently of its type, so `(eo::add 1 1)` evaluates in a signature that
declares no numerals at all. What is reported is a literal standing where its
type is asked for.
""",
)
def literal_without_type(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    seen: set[tuple[str, str]] = set()
    for term, where, _params in _terms(ctx):
        for nd in _typed_positions(term):
            if not nd.is_atom:
                continue
            cat = nd.literal_category
            if cat is None or cat == "<boolean>" or cat in sig.literal_type:
                continue
            key = (cat, where)
            if key in seen:
                continue
            seen.add(key)
            yield Diagnostic(
                code="EO0071",
                severity=Severity.ERROR,
                message=f"`{nd.text}` is a {cat} literal, and this signature has no "
                f"`declare-consts {cat}`",
                span=nd.span,
                label="no type for this literal",
                notes=[f"in {where}"],
                help=f"declare the category, e.g. (declare-consts {cat} Int)",
            )


# Where a term's type is asked for. A computational operator does not ask: ethos
# "internally distinguishes whether a term is a numeral value, independently of
# its type", so `(eo::add 1 1)` needs no `declare-consts` at all. The operators
# that hand a term back do ask, at the places they hand it back from.
_PASS_THROUGH: dict[str, set[int]] = {
    "eo::ite": {2, 3},
    "eo::requires": {3},
    "eo::define": {1, 2},
}


def _typed_positions(node: Node, typed: bool = True) -> Iterator[Node]:
    """Every subterm standing where something will ask for its type."""
    if typed:
        yield node
    if not node.is_list or not node.children:
        return
    head = node.head or ""
    if head.startswith("eo::"):
        keep = _PASS_THROUGH.get(head, set())
        for i, child in enumerate(node.children[1:], start=1):
            yield from _typed_positions(child, typed and i in keep)
        return
    for child in node.children[1:] if head else node.children:
        yield from _typed_positions(child, typed)


@check(
    "EO0073",
    "an evaluation the language says cannot happen",
    page="""
The computational operators evaluate on values of one category -- "no mixed
arithmetic", as the manual puts it -- and on arguments in range. Where both
arguments are literals, whether the application evaluates is decided at the
point it is written:

    (eo::add 2 1/3)     stays as it is: a numeral and a rational
    (eo::zdiv 7 0)      stays as it is: division by zero
    (eo::pow 2 -1)      stays as it is: the exponent is negative

A term that does not evaluate is not an error to ethos; it is simply a term, and
the rule or program built around it does not do what it was written to do.
""",
)
def impossible_evaluation(ctx: Context) -> Iterator[Diagnostic]:
    for term, where, _params in _terms(ctx):
        tested = _tested(term)
        for nd in term.walk():
            if not nd.is_list or nd.head is None or not nd.head.startswith("eo::"):
                continue
            if id(nd) in tested:
                continue
            args = nd.children[1:]
            cats = [a.literal_category for a in args]
            if any(c is None for c in cats):
                continue

            if nd.head in SAME_CATEGORY and len(set(cats)) > 1:
                mixed = " and ".join(sorted(set(c for c in cats if c)))
                yield Diagnostic(
                    code="EO0073",
                    severity=Severity.ERROR,
                    message=f"`{nd.head}` is applied to {mixed}, and evaluates only on "
                    f"values of one category",
                    span=nd.span,
                    label="this never evaluates",
                    notes=[f"in {where}", "the manual: there is no mixed arithmetic"],
                )
                continue

            if (
                nd.head in {"eo::zdiv", "eo::zmod", "eo::qdiv"}
                and len(args) == 2
                and cats[1] in ARITHMETIC
                and _is_zero(args[1])
            ):
                yield Diagnostic(
                    code="EO0073",
                    severity=Severity.ERROR,
                    message=f"`{nd.head}` is applied to a zero divisor, and never evaluates",
                    span=nd.span,
                    label="this never evaluates",
                    notes=[f"in {where}"],
                )
                continue

            if (
                nd.head == "eo::pow"
                and len(args) == 2
                and cats[1] == "<numeral>"
                and (args[1].text or "").startswith("-")
            ):
                yield Diagnostic(
                    code="EO0073",
                    severity=Severity.ERROR,
                    message="`eo::pow` is applied to a negative exponent, and never evaluates",
                    span=nd.span,
                    label="this never evaluates",
                    notes=[f"in {where}"],
                )


def _is_zero(node: Node) -> bool:
    text = (node.text or "").strip()
    if text in {"0", "-0", "0.0", "-0.0"}:
        return True
    if "/" in text:
        num = text.split("/")[0]
        return num in {"0", "-0"}
    return False


# Every list operator takes the operator its list is of as its first argument.
_LIST_OPS = {
    "eo::nil": 1,
    "eo::cons": 1,
    "eo::list_len": 1,
    "eo::list_concat": 1,
    "eo::list_nth": 1,
    "eo::list_find": 1,
    "eo::list_rev": 1,
    "eo::list_erase": 1,
    "eo::list_erase_all": 1,
    "eo::list_setof": 1,
    "eo::list_minclude": 1,
    "eo::list_meq": 1,
    "eo::list_diff": 1,
    "eo::list_inter": 1,
    "eo::list_singleton_elim": 1,
    "eo::list_singleton_intro": 1,
    "eo::list_repeat": 1,
}


@check(
    "EO0074",
    "a list operator applied to something that is not an n-ary operator",
    page="""
Every list operator is *about* an operator, which it takes as its first
argument: `(eo::list_concat or x y)` concatenates two `or`-lists. The manual is
explicit that these evaluate only where that argument is an associative operator
with a nil terminator, so applying one to a symbol that was never marked
variadic gives a term that stays as it is -- and a program returning it looks,
to whatever called it, like a program that failed.
""",
)
def list_operator_subject(ctx: Context) -> Iterator[Diagnostic]:
    from ..model import NARY_ATTRS
    from ..resolve import resolve_decl

    sig = ctx.signature
    for term, where, params in _terms(ctx):
        tested = _tested(term)
        for nd in term.walk():
            if not nd.is_list or nd.head not in _LIST_OPS or id(nd) in tested:
                continue
            subject = nd.at(_LIST_OPS[nd.head])
            if subject is None or not subject.is_atom or subject.text in params:
                continue
            decl = resolve_decl(subject.text, sig)
            if decl is None or any(a.key in NARY_ATTRS for a in decl.attrs):
                continue
            yield Diagnostic(
                code="EO0074",
                severity=Severity.ERROR,
                message=f"`{nd.head}` is applied to `{subject.text}`, which is not an "
                f"n-ary operator",
                span=subject.span,
                label="no nil terminator, no list",
                notes=[
                    f"in {where}",
                    f"`{subject.text}` is declared at "
                    f"{decl.span.path.rsplit('/', 1)[-1]}:{decl.span.line} with no "
                    ":right-assoc / :left-assoc / -nil / :chainable attribute",
                    "the application never evaluates",
                ],
            )


@check(
    "EO0076",
    "a `:list` annotation that does nothing",
    page="""
`:list` says how a parameter behaves as a child of an n-ary application. A
parameter that never stands in one is annotated for nothing -- which is either a
leftover, or a misunderstanding of what the annotation does, and the second is
worth knowing about because the same misunderstanding is what leaves it *off*
where it was needed.
""",
    default_on=False,
)
def inert_list_annotation(ctx: Context) -> Iterator[Diagnostic]:
    from ..model import NIL_ATTRS
    from ..resolve import resolve_decl

    sig = ctx.signature
    # where `:list` changes what is built: an operator with a nil terminator, and
    # an `:arg-list` symbol, whose desugaring asks whether its lone argument is a
    # list before wrapping it
    matters = NIL_ATTRS | {":arg-list"}

    def under_nary(node: Node, name: str) -> bool:
        for nd in node.walk():
            if not nd.is_list or not nd.children:
                continue
            decl = resolve_decl(nd.head, sig)
            if decl is None or not any(a.key in matters for a in decl.attrs):
                continue
            if any(c.is_atom and c.text == name for c in nd.children[1:]):
                return True
        return False

    def scan(name: str, span, nodes: list[Node], where: str) -> Iterator[Diagnostic]:
        if any(under_nary(n, name) for n in nodes if n is not None):
            return
        yield Diagnostic(
            code="EO0076",
            severity=Severity.HINT,
            message=f"`{name}` is marked `:list` and never stands under an n-ary "
            f"operator",
            span=span,
            notes=[f"in {where}", "the annotation has no effect where it is used"],
        )

    for prog in sig.programs:
        nodes = [n for case in prog.cases for n in case]
        for p in prog.params:
            if p.has(":list"):
                yield from scan(p.name, p.span, nodes, f"program `{prog.name}`")
    for rule in sig.rules:
        nodes = [rule.conclusion, rule.assumption, *rule.premises, *rule.args]
        nodes += [n for pair in rule.requires for n in pair]
        for p in rule.params:
            if p.has(":list"):
                yield from scan(p.name, p.span, nodes, f"rule `{rule.name}`")
