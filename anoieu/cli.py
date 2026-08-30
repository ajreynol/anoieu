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
from .desugar import Scope, curry, desugar
from .diagnostics import Diagnostic, Severity, render_github, render_json, render_text
from .loader import _params_from, load
from .model import NIL_ATTRS
from .resolve import resolve_decl
from .syntax.parser import parse


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


def _scope(sig, params_src: str | None):
    params = []
    if params_src:
        forms = parse("<params>", params_src).forms
        if forms:
            params = _params_from(forms[0], [])
    return Scope(sig, {p.name: p for p in params}), params


def cmd_desugar(args: argparse.Namespace) -> int:
    """What the parser builds from a term written in this signature's scope."""
    result = load(args.file)
    scope, _params = _scope(result.signature, args.params)
    parsed = parse("<term>", args.term)
    if not parsed.forms:
        print("error: could not read the term", file=sys.stderr)
        return 2
    term = parsed.forms[0]
    out = desugar(term, scope)
    print(f"-- in the scope of {os.path.basename(args.file)}")
    if args.params:
        print(f"   parameters {args.params}")
    print(f"   written    {term}")
    print(f"   desugared  {out}")
    if args.curried:
        print(f"   curried    {curry(out)}")
    if str(out) == str(term):
        print("   (no sugar in this term)")
    return 0


def cmd_symbol(args: argparse.Namespace) -> int:
    """One symbol, and everything a run knows about it."""
    result = load(args.file)
    sig = result.signature
    name = args.name
    decls = sig.by_name.get(name, [])
    prog = sig.programs_by_name.get(name)
    define = sig.defines_by_name.get(name)
    if not decls and prog is None and define is None:
        print(f"error: {os.path.basename(args.file)} declares no `{name}`", file=sys.stderr)
        return 2

    root = os.path.dirname(os.path.abspath(args.file))
    print(f"-- {name}")
    for d in decls:
        where = os.path.relpath(d.span.path, root)
        print(f"   declared   {where}:{d.span.line}  ({d.kind})")
        if d.type is not None:
            print(f"   type       {d.type}")
        for p in d.params:
            marks = " ".join(a.key for a in p.attrs)
            print(f"   parameter  {p.name} {p.type}{'  ' + marks if marks else ''}")
        for a in d.attrs:
            print(f"   attribute  {a.key}{' ' + str(a.value) if a.value is not None else ''}")
    if prog is not None:
        print(f"   program    :signature ({' '.join(str(s) for s in prog.sig_args)}) "
              f"{prog.sig_ret}, {len(prog.cases)} case(s)")
    if define is not None:
        print(f"   defined as {define.body}")

    decl = decls[-1] if decls else None
    if decl is not None and decl.constructor_attr is not None:
        scope, _ = _scope(sig, args.params)
        binder = decl.constructor_attr.key == ":binder"
        print("   applied")
        forms = (
            [f"({name} ((x T)) t1)", f"({name} ((x T) (y T)) t1)"]
            if binder
            else [f"({name} {' '.join(f't{j}' for j in range(1, k + 1))})" for k in (1, 2, 3)]
        )
        for written in forms:
            form = parse("<t>", written).forms[0]
            print(f"     {written:28} ->  {desugar(form, scope)}")
        nil = decl.nil
        if nil is not None:
            from .desugar import is_ground

            ground = is_ground(nil, decl)
            print(f"   nil        {nil}  ({'ground' if ground else 'depends on the type'})")
            if not ground:
                print("   obligation this operator needs an `:is-list-nil` case in the "
                      "calculus semantics (see docs/design.md, M4)")

    users = []
    for p in sig.programs:
        for lhs, rhs in p.cases:
            if any(s.text == name for node in (lhs, rhs) for s in node.symbols()):
                users.append(f"program {p.name}")
                break
    for r in sig.rules:
        nodes = [r.conclusion, r.assumption, *r.premises, *r.args]
        if any(s.text == name for n in nodes if n is not None for s in n.symbols()):
            users.append(f"rule {r.name}")
    if users:
        shown = ", ".join(users[:6])
        more = f", and {len(users) - 6} more" if len(users) > 6 else ""
        print(f"   named by   {len(users)}: {shown}{more}")
    else:
        print("   named by   nothing in this signature")
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

    d = sub.add_parser("desugar", help="what the parser builds from a term")
    d.add_argument("file")
    d.add_argument("--term", required=True, help="the term to desugar, in quotes")
    d.add_argument("--params", help="a parameter list the term is read under, e.g. "
                   "'((x Bool) (xs Bool :list))'")
    d.add_argument("--curried", action="store_true", help="also print the core form")
    d.set_defaults(fn=cmd_desugar)

    y = sub.add_parser("symbol", help="one symbol: declaration, sugar, and who names it")
    y.add_argument("name")
    y.add_argument("file")
    y.add_argument("--params", help="a parameter list to read applications under")
    y.set_defaults(fn=cmd_symbol)

    s = sub.add_parser("stats", help="what a signature holds")
    s.add_argument("file")
    s.set_defaults(fn=cmd_stats)

    l = sub.add_parser("list-checks", help="every check and what it says")
    l.set_defaults(fn=cmd_list)

    args = ap.parse_args(argv)
    return args.fn(args)
