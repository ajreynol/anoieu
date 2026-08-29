"""Structural checks: names, declarations, and the include graph."""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from ..syntax.parser import Node
from . import Context, check

# The prefixes ethos-eoc writes names under. A signature that declares one of
# them collides with what the compiler generates.
COMPILER_PREFIXES = (
    "$eoc_",
    "$emb_",
    "$sm_",
    "$tsm_",
    "$vsm_",
    "$msm_",
    "$ssm_",
    "$smtx_",
    "$native_",
    "$parse_",
    "$eoo_",
)

# `$eo_` is the desugar layer's, and a signature written against ethos alone may
# reasonably use it -- `tests/eo-definitions.eo` defines the whole of `eo::` that
# way -- so it is reported only when asked for.
SOFT_PREFIXES = ("$eo_",)


def _where(span) -> str:
    """A span as a note reads it: the file's own name, not its path."""
    import os

    return f"{os.path.basename(span.path)}:{span.line}:{span.col}"


@check(
    "EO0030",
    "a declared name collides with the compiler's namespace",
    page="""
`ethos-eoc` generates names under fixed prefixes: `$eo_` for the Eunoia deep
embedding, `$sm_`/`$tsm_`/`$vsm_` for the SMT term, type and value families,
`$smtx_` for the programs written over them, `$native_` for the native layer,
`$eoc_` for what a configuration block compiles to. A signature that declares
one of those is fine under ethos and collides under the compiler, where the
generated file holds two declarations of one name.
""",
)
def compiler_namespace(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    named: list[tuple[str, object]] = []
    named += [(d.name, d.span) for d in sig.decls]
    named += [(p.name, p.span) for p in sig.programs]
    named += [(d.name, d.span) for d in sig.defines]
    seen: set[str] = set()
    for name, span in named:
        if name in seen:
            continue
        seen.add(name)
        prefixes = COMPILER_PREFIXES + (SOFT_PREFIXES if ctx.pedantic else ())
        for prefix in prefixes:
            if name.startswith(prefix):
                yield Diagnostic(
                    code="EO0030",
                    severity=Severity.WARNING,
                    message=f"`{name}` is written in the namespace ethos-eoc generates",
                    span=span,
                    label=f"`{prefix}` is the compiler's",
                    help="name a signature-internal helper `$` plus something of your own",
                )
                break


@check(
    "EO0031",
    "an overload no application can tell apart",
    page="""
Overloading is resolved by the type of the application: ethos takes the most
recently declared symbol of that name whose application type checks. Two
declarations of one name with the *same* type are therefore indistinguishable --
the earlier one can never be selected -- and ethos says nothing, by design, so
that a signature may order declarations by precedence.
""",
)
def indistinguishable_overload(ctx: Context) -> Iterator[Diagnostic]:
    for name, decls in ctx.signature.by_name.items():
        if len(decls) < 2:
            continue
        by_type: dict[str, list] = {}
        for d in decls:
            if d.type is None:
                continue
            by_type.setdefault(str(d.type), []).append(d)
        for tstr, group in by_type.items():
            if len(group) < 2:
                continue
            first, later = group[0], group[-1]
            yield Diagnostic(
                code="EO0031",
                severity=Severity.WARNING,
                message=f"`{name}` is declared twice with the type {tstr}",
                span=first.span,
                label="this declaration can never be selected",
                notes=[f"the later declaration stands at {_where(later.span)}"],
            )


@check(
    "EO0011",
    "the include graph has a cycle",
    page="""
Ethos includes a file once, so a cycle terminates rather than looping -- but it
means the order symbols are declared in depends on which file a run started
from, and a signature that only works from one entry point is a signature with a
latent error.
""",
)
def include_cycle(ctx: Context) -> Iterator[Diagnostic]:
    import os

    edges: dict[str, list[str]] = {}
    for src, dst in getattr(ctx, "include_edges", []):
        edges.setdefault(os.path.realpath(src), []).append(os.path.realpath(dst))
    colour: dict[str, int] = {}
    cycles: list[list[str]] = []

    def visit(node: str, path: list[str]) -> None:
        colour[node] = 1
        for nxt in edges.get(node, []):
            if colour.get(nxt) == 1:
                cycles.append(path[path.index(nxt) :] + [nxt] if nxt in path else [nxt, node, nxt])
            elif colour.get(nxt, 0) == 0:
                visit(nxt, path + [nxt])
        colour[node] = 2

    for node in list(edges):
        if colour.get(node, 0) == 0:
            visit(node, [node])
    for cyc in cycles:
        path = ctx.signature.files[0] if ctx.signature.files else ""
        yield Diagnostic(
            code="EO0011",
            severity=Severity.WARNING,
            message="include cycle: " + " -> ".join(os.path.basename(p) for p in cyc),
            span=__import__("anoieu.diagnostics", fromlist=["Span"]).Span(path, 1, 1),
        )


@check(
    "EO0056",
    "a parameter nothing uses",
    page="""
The parameter list of a rule or a program is a pool of names its patterns and
bodies draw on. One that no case mentions is dead, and is usually the trace of a
case that was edited away or a name that was misspelled where it was used.
""",
    default_on=False,
)
def unused_parameter(ctx: Context) -> Iterator[Diagnostic]:
    def used_names(nodes: list[Node]) -> set[str]:
        out: set[str] = set()
        for nd in nodes:
            if nd is None:
                continue
            for sym in nd.symbols():
                out.add(sym.text or "")
        return out

    for prog in ctx.signature.programs:
        nodes: list[Node] = []
        for lhs, rhs in prog.cases:
            nodes += [lhs, rhs]
        nodes += prog.sig_args + ([prog.sig_ret] if prog.sig_ret else [])
        # a parameter used only in the *type* of another parameter is used
        nodes += [p.type for p in prog.params if p.type is not None]
        used = used_names(nodes)
        for p in prog.params:
            if p.name not in used:
                yield Diagnostic(
                    code="EO0056",
                    severity=Severity.HINT,
                    message=f"`{p.name}` is declared by `{prog.name}` and never used",
                    span=p.span,
                )
    for rule in ctx.signature.rules:
        nodes = list(rule.premises) + list(rule.args)
        nodes += [rule.conclusion, rule.assumption]
        for a, b in rule.requires:
            nodes += [a, b]
        if rule.premise_list is not None:
            nodes += list(rule.premise_list)
        nodes += [p.type for p in rule.params if p.type is not None]
        used = used_names([n for n in nodes if n is not None])
        for p in rule.params:
            if p.name not in used:
                yield Diagnostic(
                    code="EO0056",
                    severity=Severity.HINT,
                    message=f"`{p.name}` is declared by rule `{rule.name}` and never used",
                    span=p.span,
                )
