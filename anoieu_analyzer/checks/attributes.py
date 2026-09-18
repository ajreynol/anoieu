"""Checks on declaration attributes.

The manual states a contract for every attribute that makes an operator
variadic, and ethos enforces none of them: it accepts the declaration and lets
the consequence appear at a use site, in another file, as a type error about a
term the reader did not write.
"""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from ..model import NARY_ATTRS, NIL_ATTRS
from ..resolve import resolve_decl
from ..shape import arrow_parts, infer_simple_type, strip_requires, type_head
from . import Context, check

_RIGHT = {":right-assoc", ":right-assoc-nil", ":right-assoc-non-singleton-nil"}
_LEFT = {":left-assoc", ":left-assoc-nil", ":left-assoc-non-singleton-nil"}


def _where(span) -> str:
    """A span as a note reads it: the file's own name, not its path."""
    import os

    return f"{os.path.basename(span.path)}:{span.line}:{span.col}"


@check(
    "EO0040",
    "an associative operator's type does not have the shape the attribute requires",
    page="""
A constant marked `:right-assoc` (or a `-nil` variant) must have a type of the
form `(-> T1 T2 T2)`, and one marked `:left-assoc` a type of the form
`(-> T1 T2 T1)`: the fold has to be able to put its own result back into the
argument it came from. Ethos does not check this. A declaration that breaks it
type checks, and the first application of it fails somewhere else.
""",
)
def assoc_type_shape(ctx: Context) -> Iterator[Diagnostic]:
    for d in ctx.signature.decls:
        a = None
        for at in d.attrs:
            if at.key in NARY_ATTRS and at.key in (_RIGHT | _LEFT):
                a = at
                break
        if a is None:
            continue
        parts = arrow_parts(d.type)
        if parts is None:
            yield Diagnostic(
                code="EO0040",
                severity=Severity.ERROR,
                message=f"`{d.name}` is marked `{a.key}` but is not a function",
                span=(d.type.span if d.type is not None else d.span),
                label="this is not a `->` type",
                help="an associative operator has type (-> T1 T2 T2) or (-> T1 T2 T1)",
            )
            continue
        if len(parts) != 3:
            yield Diagnostic(
                code="EO0040",
                severity=Severity.ERROR,
                message=(
                    f"`{d.name}` is marked `{a.key}` but takes "
                    f"{len(parts) - 1} argument(s), not 2"
                ),
                span=(d.type.span if d.type is not None else d.span),
                help="an associative operator is binary: (-> T1 T2 T2) or (-> T1 T2 T1)",
            )
            continue
        t1, t2, ret = parts
        want, other = (t2, "second argument") if a.key in _RIGHT else (t1, "first argument")
        want_s, ret_s = strip_requires(want), strip_requires(ret)
        wh, rh = type_head(want_s), type_head(ret_s)
        params = {p.name for p in d.params}
        # a type parameter unifies with anything, and a dependent return type
        # -- (BitVec (eo::add n m)) against (BitVec m) -- agrees where it counts,
        # which is the constructor. Only a difference there is a finding.
        if wh is None or rh is None or wh in params or rh in params or wh == rh:
            continue
        if True:
            yield Diagnostic(
                code="EO0040",
                severity=Severity.ERROR,
                message=(
                    f"`{d.name}` is marked `{a.key}`, so its {other} and its "
                    f"return type must agree"
                ),
                span=(d.type.span if d.type is not None else d.span),
                label=f"{want_s} vs {ret_s}",
                notes=[
                    "a right-associative operator has type (-> T1 T2 T2); "
                    "a left-associative one (-> T1 T2 T1)"
                ],
            )


@check(
    "EO0041",
    "a nil terminator does not have the operator's tail type",
    page="""
`:right-assoc-nil t` inserts `t` at the tail of every application of the
operator, so `t` must have the operator's second argument type (for
`:left-assoc-nil`, its first). Ethos checks nothing at the declaration:

    (declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)   ; accepted

and `(define P () (or a b))` is then accepted too, because a `define` body with
no `:type` is never type checked. The error surfaces the first time anything
asks for the type of a term built with the operator.

This check reports only when both types can be read off the declarations: a
literal whose category has a `declare-consts`, a declared constant, or an
application of one.
""",
)
def nil_type(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for d in sig.decls:
        attr = next((a for a in d.attrs if a.key in NIL_ATTRS), None)
        if attr is None or attr.value is None:
            continue
        parts = arrow_parts(d.type)
        if parts is None or len(parts) != 3:
            continue  # EO0040 has already said so
        expect = parts[1] if attr.key in _RIGHT else parts[0]
        got = infer_simple_type(attr.value, sig)
        if got is None:
            continue
        eh, gh = type_head(expect), type_head(got)
        if eh is None or gh is None or eh == gh:
            continue
        # a parameter of the declaration is a type variable, not a constructor
        param_names = {p.name for p in d.params}
        if eh in param_names or gh in param_names:
            continue
        yield Diagnostic(
            code="EO0041",
            severity=Severity.ERROR,
            message=f"the nil terminator of `{d.name}` has the wrong type",
            span=attr.value.span,
            label=f"this has type {got}",
            notes=[f"`{d.name}` is marked `{attr.key}`, so its nil must have type {expect}"],
            help="ethos accepts the declaration; the mismatch appears at the first "
            "application of the operator whose type is asked for",
        )


_COMBINER_ATTRS = {
    ":chainable": "combining operator",
    ":pairwise": "combining operator",
    ":arg-list": "list constructor",
    ":binder": "variable-list constructor",
}


@check(
    "EO0042",
    "the operator an attribute names is not variadic, or does not exist",
    page="""
`:chainable c`, `:pairwise c`, `:arg-list c` and `:binder c` each hand `c` a
number of arguments that depends on the application, so `c` has to accept any
number of them -- it must itself be marked `:right-assoc`, `:left-assoc`, one of
the `-nil` variants, or `:chainable`.

With a binary `c`, ethos accepts the declaration and the consequence appears at
a use site: a chain of three arguments works, one of four fails with
`Non-function ... as head of APPLY`, and a chain of one fails with
`Incorrect arity`.
""",
)
def combiner_variadic(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for d in sig.decls:
        for a in d.attrs:
            role = _COMBINER_ATTRS.get(a.key)
            if role is None or a.value is None or not a.value.is_atom:
                continue
            cname = a.value.text or ""
            target = resolve_decl(cname, sig)
            if target is None:
                yield Diagnostic(
                    code="EO0042",
                    severity=Severity.ERROR,
                    message=f"`{cname}` is not declared",
                    span=a.value.span,
                    label=f"named as the {role} of `{d.name}`",
                )
                continue
            if not any(at.key in NARY_ATTRS for at in target.attrs):
                yield Diagnostic(
                    code="EO0042",
                    severity=Severity.WARNING,
                    message=f"the {role} `{cname}` is not variadic",
                    span=a.value.span,
                    label="takes a fixed number of arguments",
                    notes=[
                        f"`{cname}` is declared at {_where(target.span)} with no "
                        ":right-assoc / :left-assoc / -nil / :chainable attribute",
                        f"applications of `{d.name}` that need more than two "
                        f"{'conjuncts' if a.key in (':chainable', ':pairwise') else 'elements'} "
                        "will not build",
                    ],
                )


@check(
    "EO0046",
    "an opaque argument stands after an ordinary one",
    page="""
The manual: "Opaque arguments should always be expected before other arguments.
Otherwise all applications of the given function will be ill-typed." That is a
property of the declaration, so it can be said at the declaration rather than at
every application of it.
""",
)
def opaque_first(ctx: Context) -> Iterator[Diagnostic]:
    for d in ctx.signature.decls:
        seen_ordinary = None
        for p in d.params:
            if p.has(":implicit"):
                continue
            if p.has(":opaque"):
                if seen_ordinary is not None:
                    yield Diagnostic(
                        code="EO0046",
                        severity=Severity.ERROR,
                        message=f"opaque argument `{p.name}` stands after ordinary argument "
                        f"`{seen_ordinary}`",
                        span=p.span,
                        notes=["every application of this symbol will be ill-typed"],
                        help="write the opaque arguments first",
                    )
                    break
            else:
                seen_ordinary = p.name
