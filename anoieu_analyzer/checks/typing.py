"""Checks that need the type of a term, where its head settles it.

Ethos computes a type when something asks for one: a `define` with `:type`, a
term a proof step builds, a rule application. Nothing asks about the conclusion
of a rule that no proof has used yet, or about the right-hand side of a program
case no proof has reached, so a signature can carry a rule that cannot be
applied and a case that cannot be evaluated, indefinitely.

These checks ask. They ask shallowly -- see `anoieu_analyzer/typing.py` -- and say
nothing wherever the answer is not readable off the declarations.
"""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from ..model import Param
from ..resolve import canonical_type_head, is_type_constructor, resolve_decl, resolve_name
from ..shape import strip_requires, type_head
from ..syntax.parser import Node
from ..typing import full_arity, infer, is_variadic, type_is, type_params_of
from . import Context, check
from .terms import _typed_positions


def _params(ps: list[Param]) -> dict[str, Param]:
    return {p.name: p for p in ps}


@check(
    "EO0062",
    "a rule concludes a term that is not a Bool",
    page="""
A proof step wraps what its rule proves in `(eo::pf F)`, which requires `F` to be
a `Bool`. Ethos never checks the conclusion when the rule is *declared*: the
program a rule desugars to is given return type `Bool` outright, and the
conclusion term is not compared with it. So

    (declare-rule bad ((x Int)) :args (x) :conclusion (+ x 1))

is accepted, and the first step that applies it fails with

    Expression of unexpected type: (_ (+ a) 1)  Type: Int  Expected: Bool

The rule can never be applied successfully, and nothing says so until someone
writes the proof that finds out.
""",
)
def rule_conclusion_bool(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for rule in sig.rules:
        if rule.conclusion is None:
            continue
        params = _params(rule.params)
        tvars = type_params_of(params)
        t = infer(rule.conclusion, params, sig)
        got = canonical_type_head(t, sig)
        if got is None or got == "Bool" or not is_type_constructor(got, sig):
            continue
        yield Diagnostic(
            code="EO0062",
            severity=Severity.ERROR,
            message=f"rule `{rule.name}` concludes a term of type "
            f"{strip_requires(t)}, not Bool",
            span=rule.conclusion.span,
            label=f"this has type {strip_requires(t)}",
            notes=[
                "a step wraps what a rule proves in (eo::pf F), which requires F to be "
                "a Bool, so no application of this rule can succeed"
            ],
        )


@check(
    "EO0063",
    "a rule takes a premise that is not a Bool",
    page="""
A premise pattern is matched against what a premise proof proves, which is
always a `Bool`. A pattern of another type matches nothing, so the rule cannot
be applied.
""",
)
def premise_bool(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for rule in sig.rules:
        params = _params(rule.params)
        tvars = type_params_of(params)
        for pat in rule.premises:
            t = infer(pat, params, sig)
            got = canonical_type_head(t, sig)
            if got is None or got == "Bool" or not is_type_constructor(got, sig):
                continue
            yield Diagnostic(
                code="EO0063",
                severity=Severity.ERROR,
                message=f"rule `{rule.name}` takes a premise of type "
                f"{strip_requires(t)}, not Bool",
                span=pat.span,
                label=f"this has type {strip_requires(t)}",
                notes=["a premise proof proves a Bool, so this pattern matches nothing"],
            )


@check(
    "EO0064",
    "a program case returns a type the program does not declare",
    page="""
"Terms in program bodies are not statically type checked" -- the user manual
says so, and `typeCheckProgramPair` checks only that the right-hand side binds
nothing new and that no pattern holds an evaluatable subterm. So a case that
returns the wrong type is accepted, and it fails only when a proof reaches that
case:

    (program $mk ((x Int) (F Bool)) :signature (Bool) Bool
      ( (($mk (not F)) F)
        (($mk F)       (+ 1 1)) ))    ; Int where Bool was declared

A proof that takes the first case checks `correct`. One that takes the second
fails, in a step that names neither the program nor the case.

Compared by type constructor, so a dependent return type -- `(BitVec n)` against
`(BitVec (eo::add n m))` -- agrees.
""",
)
def case_return_type(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for prog in sig.programs:
        if prog.sig_ret is None or not prog.cases:
            continue
        params = _params(prog.params)
        tvars = type_params_of(params)
        want = canonical_type_head(prog.sig_ret, sig)
        if want is None or not is_type_constructor(want, sig):
            continue
        for lhs, rhs in prog.cases:
            t = infer(rhs, params, sig)
            got = canonical_type_head(t, sig)
            if got is None or got == want or not is_type_constructor(got, sig):
                continue
            yield Diagnostic(
                code="EO0064",
                severity=Severity.ERROR,
                message=f"this case of `{prog.name}` returns {strip_requires(t)}, "
                f"and the program declares {strip_requires(prog.sig_ret)}",
                span=rhs.span,
                label=f"this has type {strip_requires(t)}",
                notes=[
                    "program bodies are not type checked, so this is reported only when "
                    "a proof reaches this case"
                ],
            )


@check(
    "EO0065",
    "a symbol is applied to more arguments than it takes",
    page="""
An application of a symbol to more arguments than its type has is ill-typed, and
inside a program body or a rule nothing asks, so it sits there:

    (program $p ((F Bool)) :signature (Bool) Bool
      ( (($p F) (not F F)) ))          ; `not` is unary -- accepted, "correct"

Variadic symbols are exempt, since that is what their attribute is for, and a
symbol applied to *fewer* arguments than it takes is an ordinary partial
application.
""",
)
def over_application(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature

    def scan(node: Node, params: dict[str, Param], where: str) -> Iterator[Diagnostic]:
        for nd in node.walk():
            if not nd.is_list or not nd.children:
                continue
            head = nd.head
            if head is None or head in params or head.startswith("eo::") or head == "_":
                continue
            if head in sig.programs_by_name or head in sig.defines_by_name:
                continue
            decl = resolve_decl(head, sig)
            if decl is None or is_variadic(decl) or decl.kind in ("datatype", "sort"):
                continue
            if len(sig.by_name.get(head, [])) > 1:
                continue  # overloaded: another declaration may take this many
            fa = full_arity(decl)
            if fa is None:
                continue
            args, _ret = fa
            nargs = len(nd.children) - 1
            if not args or nargs <= len(args):
                continue
            yield Diagnostic(
                code="EO0065",
                severity=Severity.ERROR,
                message=f"`{head}` takes {len(args)} argument(s), and is applied to "
                f"{nargs} here",
                span=nd.span,
                label="too many arguments",
                notes=[f"in {where}"],
            )

    for prog in sig.programs:
        params = _params(prog.params)
        for lhs, rhs in prog.cases:
            yield from scan(rhs, params, f"program `{prog.name}`")
            yield from scan(lhs, params, f"program `{prog.name}`")
    for rule in sig.rules:
        params = _params(rule.params)
        for node in [rule.conclusion, rule.assumption, *rule.premises, *rule.args]:
            if node is not None:
                yield from scan(node, params, f"rule `{rule.name}`")
    for d in sig.defines:
        if d.body is not None:
            yield from scan(d.body, _params(d.params), f"definition `{d.name}`")


@check(
    "EO0066",
    "a program is applied to the wrong number of arguments",
    page="""
A program declares its arity with `:signature`, and an application of another
arity never evaluates. Ethos notices at parse time and prints

    Wrong number of arguments when applying program $q, 3 arguments expected, got 2

without a file or a line, and the run still ends in `correct` with exit 0. This
says the same thing, where it happened.
""",
)
def program_call_arity(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature

    def scan(node: Node, where: str, params: dict[str, Param]) -> Iterator[Diagnostic]:
        for nd in node.walk():
            if not nd.is_list or not nd.children:
                continue
            head = nd.head
            if head is None or head in params:
                continue
            prog = sig.programs_by_name.get(head)
            if prog is None or not prog.sig_args:
                continue
            nargs = len(nd.children) - 1
            if nargs == len(prog.sig_args):
                continue
            yield Diagnostic(
                code="EO0066",
                severity=Severity.ERROR,
                message=f"`{head}` takes {len(prog.sig_args)} argument(s), and is "
                f"applied to {nargs} here",
                span=nd.span,
                label="wrong arity",
                notes=[f"in {where}", "an application of another arity never evaluates"],
            )

    for prog in sig.programs:
        params = _params(prog.params)
        for lhs, rhs in prog.cases:
            yield from scan(rhs, f"program `{prog.name}`", params)
    for rule in sig.rules:
        params = _params(rule.params)
        for node in [rule.conclusion, rule.assumption, *rule.premises, *rule.args]:
            if node is not None:
                yield from scan(node, f"rule `{rule.name}`", params)
        for a, b in rule.requires:
            yield from scan(a, f"rule `{rule.name}`", params)
            yield from scan(b, f"rule `{rule.name}`", params)
    for d in sig.defines:
        if d.body is not None:
            yield from scan(d.body, f"definition `{d.name}`", _params(d.params))


@check(
    "EO0068",
    "an argument has a different type constructor from the one an operator requires",
    page="""
A well-shaped application can still supply an argument of the wrong sort:
`(not x)` requires a Bool even when it is hidden in a program whose `x` is Int.
Checking only the application's return type misses this, since `not` still
declares a Bool result. Program bodies and rule conclusions can retain such
applications until a proof asks for their type.

This check compares known type constructors in program results, rule conclusions
and definition bodies. It checks ordinary fixed-arity declarations, including
aliases, and reports only when both constructors are known and different.
It does not compare dependent indices or infer a polymorphic argument's expected
type. Overloads, variadic operators, parameter-bound heads, patterns, computational
tests, binder bodies and local `eo::define` scopes are left to the checker. An unknown type is
not a mismatch.
""",
)
def argument_type(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature

    def scan(term: Node, params: dict[str, Param], where: str) -> Iterator[Diagnostic]:
        # Local computational bindings need their own environment; do not read
        # a same-named outer parameter or global declaration through one.
        scoped: set[int] = set()
        for node in term.walk():
            decl = resolve_decl(node.head, sig)
            if (node.head == "eo::define" or
                    (decl is not None and any(a.key in {":binder", ":let-binder"}
                                              for a in decl.attrs))):
                scoped.update(id(child) for child in node.walk())
        caller_types = type_params_of(params)
        for node in _typed_positions(term):
            head = node.head
            if (id(node) in scoped or not node.is_list or not head or head in params
                    or head.startswith("eo::") or head == "_"):
                continue
            name = resolve_name(head, sig)
            if len(sig.by_name.get(name, [])) > 1:
                continue
            decl = resolve_decl(head, sig)
            if decl is None or is_variadic(decl):
                continue
            arity = full_arity(decl)
            if arity is None or len(arity[0]) != len(node.children) - 1:
                continue
            callee_types = type_params_of(_params(decl.params))
            for index, (formal, actual) in enumerate(zip(arity[0], node.children[1:]), 1):
                want = canonical_type_head(formal, sig)
                got_type = infer(actual, params, sig)
                got = canonical_type_head(got_type, sig)
                if (want in callee_types or got in caller_types or want == got
                        or not is_type_constructor(want, sig)
                        or not is_type_constructor(got, sig)):
                    continue
                yield Diagnostic(
                    code="EO0068", severity=Severity.ERROR,
                    message=f"argument {index} of `{head}` has type {strip_requires(got_type)}, "
                            f"but the operator requires {strip_requires(formal)}",
                    span=actual.span, label=f"expected {want}, got {got}",
                    notes=[f"in {where}", "distinct type constructors; no dependent indices compared"],
                )

    for prog in sig.programs:
        for _lhs, rhs in prog.cases:
            yield from scan(rhs, _params(prog.params), f"program `{prog.name}`")
    for rule in sig.rules:
        if rule.conclusion is not None:
            yield from scan(rule.conclusion, _params(rule.params), f"rule `{rule.name}`")
    for define in sig.defines:
        if define.body is not None:
            yield from scan(define.body, _params(define.params), f"definition `{define.name}`")
