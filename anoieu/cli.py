"""The command line.

    anoieu check <file.eo> [--semantics X.eos] [--smt-semantics smt.eos]
    anoieu explain <CODE>
    anoieu stats <file.eo>
    anoieu list-checks
"""

from __future__ import annotations

import argparse
import os
import sys

from .checks import REGISTRY, Context, load_checks, run_all
from .diagnostics import Diagnostic, Severity, render_github, render_json, render_text
from .loader import load


def _sorted(diags: list[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple] = set()
    out = []
    for d in sorted(diags, key=lambda d: (d.span.path, d.span.line, d.span.col, d.code)):
        k = (d.span.path, d.span.line, d.span.col, d.code, d.message)
        if k in seen:
            continue
        seen.add(k)
        out.append(d)
    return out


def cmd_check(args: argparse.Namespace) -> int:
    load_checks()
    result = load(args.file)
    ctx = Context(
        signature=result.signature,
        files=result.files,
        sources=result.sources,
        root=os.path.dirname(os.path.abspath(args.file)),
        pedantic=args.pedantic,
        include_edges=result.include_edges,
    )
    enabled = None
    if args.only:
        enabled = {c.upper() for c in args.only}
        unknown = sorted(enabled - set(REGISTRY))
        if unknown:
            print(
                f"error: no check called {', '.join(unknown)}; "
                f"`anoieu list-checks` prints every code",
                file=sys.stderr,
            )
            return 2
    for opt, what in (
        (args.semantics, "--semantics"),
        (args.smt_semantics, "--smt-semantics"),
    ):
        if opt:
            print(
                f"warning: {what} is accepted but not read yet; the checks over a "
                f"triple are not written (see docs/design.md, M4)",
                file=sys.stderr,
            )
    diags = list(result.diagnostics)
    if enabled is not None:
        diags = [d for d in diags if d.code in enabled]
    diags += run_all(ctx, enabled)
    diags = _sorted(diags)

    if args.format == "json":
        print(render_json(diags, ctx.root))
    elif args.format == "github":
        print(render_github(diags, ctx.root))
    else:
        color = sys.stdout.isatty() and not args.no_color
        if diags:
            print(render_text(diags, result.sources, ctx.root, color=color), end="")
        counts = {s: sum(1 for d in diags if d.severity is s) for s in Severity}
        parts = [
            f"{counts[s]} {s.value}{'s' if counts[s] != 1 else ''}"
            for s in Severity
            if counts[s]
        ]
        sig = result.signature
        print(
            f"-- checked {len(sig.files)} file(s): {len(sig.decls)} declarations, "
            f"{len(sig.programs)} programs, {len(sig.rules)} rules"
        )
        print("-- " + (", ".join(parts) if parts else "nothing to report"))

    worst = min((d.severity.rank for d in diags), default=9)
    if worst == 0:
        return 1
    if worst == 1 and args.deny_warnings:
        return 1
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    load_checks()
    chk = REGISTRY.get(args.code.upper())
    if chk is None:
        print(f"error: no check called {args.code}", file=sys.stderr)
        return 1
    print(f"{chk.code}: {chk.title}\n")
    print(chk.page or "(no manual page yet)")
    if not chk.default_on:
        print("\nThis check is off by default; run with --pedantic or --only.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    load_checks()
    for code in sorted(REGISTRY):
        chk = REGISTRY[code]
        flag = "" if chk.default_on else "  (off by default)"
        print(f"{code}  {chk.title}{flag}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    result = load(args.file)
    sig = result.signature
    nary = [d for d in sig.decls if d.is_nary]
    print(f"-- {os.path.basename(args.file)}")
    print(f"   files          {len(sig.files)}")
    print(f"   declarations   {len(sig.decls)}  ({len(nary)} n-ary)")
    print(f"   definitions    {len(sig.defines)}")
    print(f"   programs       {len(sig.programs)}")
    print(f"   proof rules    {len(sig.rules)}")
    print(f"   literal kinds  {len(sig.literals)}")
    documented = sum(1 for r in sig.rules if r.doc is not None)
    print(f"   documented     {documented}/{len(sig.rules)} rules")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="anoieu", description="a static analyzer for Eunoia")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="check a signature")
    c.add_argument("file")
    c.add_argument("--semantics", help="the calculus semantics (.eos) [accepted, not read yet]")
    c.add_argument(
        "--smt-semantics", help="the SMT-LIB semantics (.eos) [accepted, not read yet]"
    )
    c.add_argument("--format", choices=["text", "json", "github"], default="text")
    c.add_argument("--only", action="append", help="run only this check code")
    c.add_argument("--pedantic", action="store_true", help="also run the checks that are off by default")
    c.add_argument("--deny-warnings", action="store_true")
    c.add_argument("--no-color", action="store_true")
    c.set_defaults(fn=cmd_check)

    e = sub.add_parser("explain", help="the manual page of a check")
    e.add_argument("code")
    e.set_defaults(fn=cmd_explain)

    s = sub.add_parser("stats", help="what a signature holds")
    s.add_argument("file")
    s.set_defaults(fn=cmd_stats)

    l = sub.add_parser("list-checks", help="every check and what it says")
    l.set_defaults(fn=cmd_list)

    args = ap.parse_args(argv)
    return args.fn(args)
