"""Checks on the shape of a proof rule.

A rule is a pattern for an application, and some of what it says can be read
without knowing anything about types: a requirement that compares two different
values can never hold, and a premise list has to be gathered by an operator that
takes any number of arguments.
"""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from ..model import NARY_ATTRS
from ..resolve import resolve_decl
from ..syntax.parser import Node
from . import Context, check


def _value_text(node: Node) -> str | None:
    """The text of a term that is a value written out, or None."""
    if not node.is_atom:
        return None
    if node.text in ("true", "false"):
        return node.text
    return node.text if node.literal_category else None


@check(
    "EO0067",
    "a requirement that can never hold",
    page="""
`:requires ((a b))` is satisfied when the two sides evaluate to the same term.
Where both sides are values written out and they are different values, no
substitution can make them equal, so the rule can never be applied -- and
nothing says so until someone tries.

The same holds for an `eo::requires` written into a conclusion by hand, which
is what the attribute is sugar for.
""",
)
def impossible_requirement(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        pairs = list(rule.requires)
        for node in [rule.conclusion]:
            if node is None:
                continue
            for nd in node.walk():
                if nd.is_list and nd.head == "eo::requires" and len(nd.children) == 4:
                    pairs.append((nd.children[1], nd.children[2]))
        for a, b in pairs:
            ta, tb = _value_text(a), _value_text(b)
            if ta is None or tb is None or ta == tb:
                continue
            yield Diagnostic(
                code="EO0067",
                severity=Severity.ERROR,
                message=f"rule `{rule.name}` requires {ta} to be {tb}",
                span=a.span,
                label="these are different values",
                notes=["no application of this rule can satisfy it"],
            )


@check(
    "EO0069",
    "a premise list gathered by an operator that is not variadic",
    page="""
`:premise-list F op` collects the formulas its premises prove and builds one
term from them with `op`, so `op` has to accept any number of arguments: the
manual asks for one marked `:right-assoc`, `:left-assoc`, a `-nil` variant, or
`:chainable`. With a binary operator, a rule applied to three premises builds an
application that does not type check, and one applied to none has nothing to
build.
""",
)
def premise_list_operator(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for rule in sig.rules:
        if rule.premise_list is None:
            continue
        _pattern, op = rule.premise_list
        if not op.is_atom:
            continue
        decl = resolve_decl(op.text, sig)
        if decl is None:
            yield Diagnostic(
                code="EO0069",
                severity=Severity.ERROR,
                message=f"`{op.text}` is not declared",
                span=op.span,
                label=f"named as the premise-list operator of `{rule.name}`",
            )
            continue
        if any(a.key in NARY_ATTRS for a in decl.attrs):
            continue
        yield Diagnostic(
            code="EO0069",
            severity=Severity.WARNING,
            message=f"the premise-list operator `{op.text}` is not variadic",
            span=op.span,
            label="takes a fixed number of arguments",
            notes=[
                f"`{rule.name}` gathers any number of premises with it, so it needs "
                ":right-assoc, :left-assoc, a -nil variant or :chainable"
            ],
        )
