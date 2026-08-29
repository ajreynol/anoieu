"""Checks on the documentation convention of a signature.

CPC documents each rule and program in a comment block above it. The blocks are
read by people and by nothing else, so nothing keeps them true: a premise added
to a rule does not add a line to its docstring, and a rule renamed does not
rename the `; rule:` line above it.
"""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from . import Context, check


@check(
    "DOC0010",
    "a docstring names something other than what it documents",
    page="""
The `; rule: X` or `; program: X` line above a declaration names what it
documents. When the two disagree, one of them was renamed and the other was not,
and the docstring is now attached to the wrong thing.
""",
)
def doc_name(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        doc = rule.doc
        if doc is None or doc.name is None:
            continue
        if doc.kind == "rule" and doc.name != rule.name:
            yield Diagnostic(
                code="DOC0010",
                severity=Severity.WARNING,
                message=f"this docstring says `{doc.name}`, but documents rule `{rule.name}`",
                span=doc.span,
            )
    for prog in ctx.signature.programs:
        doc = prog.doc
        if doc is None or doc.name is None:
            continue
        if doc.kind == "program" and doc.name != prog.name:
            yield Diagnostic(
                code="DOC0010",
                severity=Severity.WARNING,
                message=f"this docstring says `{doc.name}`, but documents program `{prog.name}`",
                span=doc.span,
            )


@check(
    "DOC0011",
    "a docstring documents a different number of premises or arguments",
    page="""
`; premises:` and `; args:` list one `- name: description` item per premise and
per argument. A count that disagrees with the declaration means a premise or an
argument was added or removed on one side only.

A rule written with `:premise-list` takes any number of premises, so its
docstring is not counted.
""",
)
def doc_counts(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        doc = rule.doc
        if doc is None:
            continue
        if rule.premise_list is None and "premises" in doc.fields:
            n = len(doc.fields["premises"])
            if n and n != len(rule.premises):
                yield Diagnostic(
                    code="DOC0011",
                    severity=Severity.WARNING,
                    message=f"rule `{rule.name}` takes {len(rule.premises)} premise(s), "
                    f"and its docstring lists {n}",
                    span=doc.span,
                )
        if "args" in doc.fields:
            n = len(doc.fields["args"])
            if n and n != len(rule.args):
                yield Diagnostic(
                    code="DOC0011",
                    severity=Severity.WARNING,
                    message=f"rule `{rule.name}` takes {len(rule.args)} argument(s), "
                    f"and its docstring lists {n}",
                    span=doc.span,
                )
    for prog in ctx.signature.programs:
        doc = prog.doc
        if doc is None or "args" not in doc.fields or not prog.sig_args:
            continue
        n = len(doc.fields["args"])
        if n and n != len(prog.sig_args):
            yield Diagnostic(
                code="DOC0011",
                severity=Severity.WARNING,
                message=f"program `{prog.name}` takes {len(prog.sig_args)} argument(s), "
                f"and its docstring lists {n}",
                span=doc.span,
            )


@check(
    "DOC0012",
    "a docstring documents a field the declaration does not have",
    page="""
A docstring that documents an assumption, premises or a requirement the rule
does not have describes a rule that was changed underneath it.
""",
)
def doc_fields(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        doc = rule.doc
        if doc is None:
            continue
        pairs = [
            ("assumption", rule.assumption is not None),
            ("premises", bool(rule.premises)),
            ("args", bool(rule.args)),
            ("requires", bool(rule.requires)),
        ]
        for field, present in pairs:
            documented = field in doc.fields and (doc.fields[field] or doc.prose.get(field))
            if documented and not present:
                yield Diagnostic(
                    code="DOC0012",
                    severity=Severity.WARNING,
                    message=f"rule `{rule.name}` has no {field}, and its docstring "
                    f"documents one",
                    span=doc.span,
                )


@check(
    "DOC0001",
    "a rule or program with no docstring",
    page="""
Off by default. A signature that documents most of its rules is saying that the
undocumented ones are an oversight.
""",
    default_on=False,
)
def missing_doc(ctx: Context) -> Iterator[Diagnostic]:
    for rule in ctx.signature.rules:
        if rule.doc is None or rule.doc.kind != "rule":
            yield Diagnostic(
                code="DOC0001",
                severity=Severity.HINT,
                message=f"rule `{rule.name}` has no docstring",
                span=rule.span,
            )
