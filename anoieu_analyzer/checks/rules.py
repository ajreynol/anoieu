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


@check(
    "EO0077",
    "the rules a calculus admits without justification",
    page="""
`:sorry` marks a rule that has no formal justification, and it is a legitimate
thing to write: CPC's `trust` rule carries every inference cvc5 has not
formalised, and says so in its own docstring. What it changes is what a run
means -- ethos answers `incomplete` rather than `correct` for any proof that
uses one, and the compiler has nothing to verify about it.

So this is an inventory rather than a defect report, and a hint rather than a
warning: it puts the admitted rules of a calculus in one place, because "which
rules is this proof's verdict resting on" is a question worth being able to ask
without grep.
""",
)
def sorry_rule(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        attr = next((a for a in rule.attrs if a.key == ":sorry"), None)
        if attr is None:
            continue
        yield Diagnostic(
            code="EO0077",
            severity=Severity.HINT,
            message=f"rule `{rule.name}` is admitted: it is marked `:sorry`",
            span=attr.span,
            label="no formal justification",
            notes=[
                "a proof using it makes ethos answer `incomplete` rather than `correct`"
            ],
        )


@check(
    "EO0078",
    "a rule reaches `eo::hash`, which no generated checker can model",
    page="""
`eo::hash` returns "a numeral unique to" a value and nothing further: the
language deliberately leaves it underconstrained. That is enough for a signature
to reason through and not enough for a model to follow, so the Lean backend
refuses to print the program that would call it, and a calculus that reasons
through hash is one no generated Lean checker can be built for.

Ethos itself is unaffected -- it computes a hash and carries on -- which is why
this is worth saying at the signature: the consequence lands in another tool, on
another day.
""",
)
def hash_reachable(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature

    # which programs each program and rule reaches, one step
    calls: dict[str, set[str]] = {}
    for prog in sig.programs:
        named: set[str] = set()
        for _lhs, rhs in prog.cases:
            named |= {s.text or "" for s in rhs.symbols()}
        calls[prog.name] = named & set(sig.programs_by_name)

    def reaches(start: set[str]) -> set[str]:
        seen, stack = set(), list(start)
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack += list(calls.get(name, ()))
        return seen

    uses_hash = {
        prog.name
        for prog in sig.programs
        for _lhs, rhs in prog.cases
        if any(nd.is_list and nd.head == "eo::hash" for nd in rhs.walk())
    }
    if not uses_hash:
        return

    for rule in sig.rules:
        nodes = [rule.conclusion, rule.assumption, *rule.premises, *rule.args]
        nodes += [n for pair in rule.requires for n in pair]
        direct = {
            s.text or "" for n in nodes if n is not None for s in n.symbols()
        } & set(sig.programs_by_name)
        through = reaches(direct) & uses_hash
        if not through:
            continue
        via = ", ".join(sorted(through)[:3])
        yield Diagnostic(
            code="EO0078",
            severity=Severity.WARNING,
            message=f"rule `{rule.name}` reaches `eo::hash`",
            span=rule.span,
            label="cannot be compiled to a Lean checker",
            notes=[
                f"through {via}",
                "the language leaves what hash returns underconstrained, so the Lean "
                "backend refuses to print the program that calls it",
            ],
        )


def _shape(node: Node, params: set[str], seen: dict[str, str]) -> str:
    """A term with its parameters renamed by first appearance.

    Two rules that differ only in what they call their parameters are the same
    rule, so comparing them means comparing something that does not carry the
    names.
    """
    if node.is_atom:
        text = node.text or ""
        if text in params:
            return seen.setdefault(text, f"#{len(seen)}")
        return text
    return "(" + " ".join(_shape(c, params, seen) for c in node.children) + ")"


@check(
    "EO0083",
    "two rules that are the same rule",
    page="""
A calculus of several hundred rules can gain one twice: the same premises, the
same arguments and the same conclusion, differing only in the names its
parameter list gives them. Both are then declared, both are compiled, both get a
verification condition and a Lean lemma, and a proof may cite either.

Compared after renaming each rule's parameters by first appearance, so that a
rule is not reported as a duplicate of itself under other names -- and only where
*everything* agrees: premises, arguments, requirements, assumption, premise-list
operator and whether the conclusion is explicit. The requirements matter most:
CPC has nineteen rules whose premises and conclusion are `(= a b)` and which
differ only in what they require of it.
""",
)
def duplicate_rules(ctx: Context) -> Iterator[Diagnostic]:
    by_shape: dict[str, str] = {}
    for rule in ctx.signature.rules:
        if rule.conclusion is None:
            continue
        params = {p.name for p in rule.params}
        seen: dict[str, str] = {}
        # everything that makes a rule the rule it is: what it takes, what it
        # demands of what it took, and what it gives back. Leaving the
        # requirements out of this made every rule of the shape
        # `:args ((= a b)) :requires (...) :conclusion (= a b)` look like every
        # other one -- which on CPC is nineteen rules that differ only there.
        nodes = list(rule.premises) + list(rule.args) + [rule.conclusion]
        nodes += [n for pair in rule.requires for n in pair]
        if rule.assumption is not None:
            nodes.append(rule.assumption)
        if rule.premise_list is not None:
            nodes.append(rule.premise_list[1])
        parts = [_shape(n, params, seen) for n in nodes]
        key = "|".join(parts) + (
            f"|{len(rule.premises)}|{len(rule.args)}|{len(rule.requires)}"
            f"|{rule.assumption is not None}|{rule.premise_list is not None}"
            f"|{rule.conclusion_explicit}"
        )
        first = by_shape.setdefault(key, rule)
        if first is rule:
            continue
        types = [str(p.type) for p in rule.params]
        first_types = [str(p.type) for p in first.params]
        notes = [
            f"`{first.name}` is declared at {first.span.path.rsplit('/', 1)[-1]}:"
            f"{first.span.line}",
            "both are compiled, both get a verification condition, and a proof may "
            "cite either",
        ]
        if types != first_types:
            notes.insert(
                1,
                f"their parameters are declared at different types -- {first_types} "
                f"against {types} -- but matching does not check a parameter's type, "
                "so the same applications match both",
            )
        yield Diagnostic(
            code="EO0083",
            severity=Severity.WARNING,
            message=f"rule `{rule.name}` matches exactly what `{first.name}` matches",
            span=rule.span,
            label="same premises, arguments, requirements and conclusion",
            notes=notes,
        )


@check(
    "EO0084",
    "a rule whose conclusion is one of its premises",
    page="""
A rule that concludes exactly what it was given proves nothing: applying it
leaves the proof where it was. Sometimes that is deliberate -- a rule that exists
to re-label a step, or a placeholder -- and sometimes it is a conclusion that was
edited into the wrong shape.
""",
)
def identity_rule(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        if rule.conclusion is None or rule.premise_list is not None:
            continue
        for premise in rule.premises:
            if str(premise) != str(rule.conclusion):
                continue
            yield Diagnostic(
                code="EO0084",
                severity=Severity.WARNING,
                message=f"rule `{rule.name}` concludes one of its own premises",
                span=rule.conclusion.span,
                label="this is premise text, unchanged",
                notes=["an application of it leaves the proof where it was"],
            )
            break


@check(
    "EO0085",
    "a requirement that always holds",
    page="""
`:requires ((a b))` is satisfied when the two sides evaluate to the same term. A
pair whose two sides are written identically is satisfied by every substitution,
so it constrains nothing -- the opposite of `EO0067`, and usually a requirement
that was half-edited.
""",
)
def trivial_requirement(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        for a, b in rule.requires:
            if str(a) != str(b):
                continue
            yield Diagnostic(
                code="EO0085",
                severity=Severity.WARNING,
                message=f"rule `{rule.name}` requires {a} to equal itself",
                span=a.span,
                label="satisfied by everything",
                notes=["the requirement constrains no application of the rule"],
            )
