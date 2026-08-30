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

from . import __version__
from .baseline import Baseline
from .checks import REGISTRY, Context, load_checks, run_all
from .config import discover
from .desugar import Scope, curry, desugar
from .diagnostics import (
    Diagnostic,
    Severity,
    SourceMap,
    render_github,
    render_json,
    render_sarif,
    render_text,
)
from .loader import _params_from, load
from .semantics import load_set
from .model import NIL_ATTRS
from .resolve import resolve_decl
from .suppress import apply as suppress_apply
from .suppress import collect as suppress_collect
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


def _expand(paths: list[str]) -> list[str]:
    """A directory names every signature under it, which is how a repository
    points at a tree of them rather than listing forty files."""
    out: list[str] = []
    for path in paths:
        if os.path.isdir(path):
            for root, _dirs, names in os.walk(path):
                out += [os.path.join(root, n) for n in sorted(names) if n.endswith(".eo")]
        else:
            out.append(path)
    return out


def _profiles(args, cfg) -> list[tuple[str, list[str]]]:
    """What to analyse, as ordered profiles.

    A profile is a list of signatures loaded *in order into one symbol table*,
    which is how a consumer loads them: cvc5 checks an expert proof by including
    `Cpc.eo` and then `expert/CpcExpert.eo`. Analysing the two apart makes a rule
    of the second unable to see a program of the first, and asks "does anything
    reach this" in a world that nobody runs.
    """
    if args.file:
        return [("", _expand([os.path.abspath(f) for f in args.file]))]
    out: list[tuple[str, list[str]]] = []
    for p in cfg.profiles:
        name = str(p.get("name", "")) or "profile"
        includes = [os.path.abspath(cfg.resolve(i)) for i in p.get("includes", [])]
        if includes and (not args.profile or name in args.profile):
            out.append((name, _expand(includes)))
    if out:
        return out
    if cfg.entry_points:
        return [("", _expand([os.path.abspath(cfg.resolve(e)) for e in cfg.entry_points]))]
    return []


# Codes whose subject is *reachability*, which has an answer only relative to a
# profile: a program unreached in one profile may be named by a rule of another.
# A run over several profiles reports one only where it holds in all of them.
PROFILE_SCOPED = {"EO0060", "EO0057"}


def _common_root(paths: list[str], cfg) -> str:
    if cfg.found:
        return cfg.root
    dirs = [os.path.dirname(p) for p in paths]
    return os.path.commonpath(dirs) if len(dirs) > 1 else (dirs[0] if dirs else os.getcwd())


# How the embedding spells a name it declares. A configuration set writes the
# bare name; the embedding declares it under one of these.
_EMBED_PREFIXES = (
    "$emb_sm.", "$emb_tsm.", "$emb_vsm.", "$emb_msm.", "$emb_ssm.",
    "$sm_", "$tsm_", "$vsm_", "$msm_", "$ssm_", "$smt_", "$smtx_", "$native_",
)


def _embedding_vocabulary(path: str) -> set[str]:
    """The bare names the deep embedding declares, however it spells them."""
    result = load(path)
    out: set[str] = set()
    for name in result.signature.all_named():
        out.add(name)
        for prefix in _EMBED_PREFIXES:
            if name.startswith(prefix):
                out.add(name[len(prefix):])
    return out


def _show(path: str, root: str) -> str:
    """A path as a log should carry it: relative where that is shorter to read,
    and as it stands where relative would climb out of the tree."""
    try:
        rel = os.path.relpath(path, root)
    except ValueError:
        return path
    return path if rel.startswith("..") else rel


def cmd_check(args: argparse.Namespace) -> int:
    load_checks()
    cfg = discover(args.file[0] if args.file else os.getcwd(), args.config)
    profiles = _profiles(args, cfg)
    if not profiles:
        print(
            "error: name a signature to check, or list `profiles` or `entry_points` "
            "in anoieu.json",
            file=sys.stderr,
        )
        return 2
    missing = [e for _n, es in profiles for e in es if not os.path.isfile(e)]
    if missing:
        for m in missing:
            print(f"error: no such file: {m}", file=sys.stderr)
        return 2
    entries = [e for _n, es in profiles for e in es]

    enabled = None
    if args.only:
        enabled = {c.upper() for c in args.only}
    elif cfg.enable:
        enabled = set(cfg.enable)
    if enabled is not None:
        unknown = sorted(enabled - set(REGISTRY))
        if unknown:
            print(
                f"error: no check called {', '.join(unknown)}; "
                f"`anoieu list-checks` prints every code",
                file=sys.stderr,
            )
            return 2
    semantics = smt_semantics = None
    for opt, what in ((args.semantics, "--semantics"), (args.smt_semantics, "--smt-semantics")):
        if opt and not os.path.isfile(opt):
            print(f"error: no such file: {opt}", file=sys.stderr)
            return 2
    if args.semantics:
        semantics = load_set(args.semantics)
    if args.smt_semantics:
        smt_semantics = load_set(args.smt_semantics)
    embedding_names: set[str] = set()
    if args.embedding:
        if not os.path.isfile(args.embedding):
            print(f"error: no such file: {args.embedding}", file=sys.stderr)
            return 2
        embedding_names = _embedding_vocabulary(args.embedding)

    root = _common_root(entries, cfg)
    pedantic = args.pedantic or cfg.pedantic
    diags: list[Diagnostic] = []
    sources = SourceMap()
    files: dict = {}
    read = 0
    counts = {"decls": 0, "programs": 0, "rules": 0}

    per_profile: dict[str, list[Diagnostic]] = {}
    profile_files: dict[str, set[str]] = {}
    for pname, includes in profiles:
        result = load(includes, profile=pname)
        ctx = Context(
            signature=result.signature,
            files=result.files,
            sources=result.sources,
            root=root,
            pedantic=pedantic,
            include_edges=result.include_edges,
            profile=pname,
            semantics=semantics,
            smt_semantics=smt_semantics,
            embedding_names=embedding_names,
        )
        for path, parsed in result.files.items():
            if path not in files:
                files[path] = parsed
                sources.add(path, parsed.text)
                read += 1
        found = list(result.diagnostics) + run_all(ctx, enabled)
        for d in found:
            if not d.profile:
                d.profile = pname
        per_profile[pname] = found
        profile_files[pname] = set(result.files)
        diags += found
        for sem in (semantics, smt_semantics):
            if sem is not None and sem.path not in files:
                sources.add(sem.path, sem.text)
                read += 1
                diags += sem.diagnostics
        counts["decls"] += len(result.signature.decls)
        counts["programs"] += len(result.signature.programs)
        counts["rules"] += len(result.signature.rules)

    # A reachability claim holds only where it holds in every profile the answer
    # could differ in -- that is, every profile that loaded the file the subject
    # stands in. A profile that never read the file is not evidence either way,
    # which is what keeps a finding about an expert-only program from being
    # dropped because the safe profile never saw it.
    if len(per_profile) > 1:
        keys = {
            name: {(d.code, d.span.path, d.message) for d in found if d.code in PROFILE_SCOPED}
            for name, found in per_profile.items()
        }
        kept: list[Diagnostic] = []
        for d in diags:
            if d.code not in PROFILE_SCOPED:
                kept.append(d)
                continue
            key = (d.code, d.span.path, d.message)
            relevant = [n for n, files in profile_files.items() if d.span.path in files]
            if all(key in keys[n] for n in relevant):
                d.profile = ", ".join(relevant)
                kept.append(d)
        diags = kept
    if enabled is not None:
        diags = [d for d in diags if d.code in enabled]
    if cfg.disable and not args.only:
        diags = [d for d in diags if d.code not in set(cfg.disable)]
    for d in diags:
        override = cfg.severity.get(d.code)
        if override in {s.value for s in Severity}:
            d.severity = Severity(override)
    diags = _sorted(diags)

    silenced: list = []
    if not args.no_suppress:
        diags, silenced = suppress_apply(diags, suppress_collect(files))

    baseline_path = args.baseline or (cfg.resolve(cfg.baseline) if cfg.baseline else None)
    held, stale = 0, []
    if args.update_baseline:
        if baseline_path is None:
            print(
                "error: --update-baseline needs --baseline PATH, or `baseline` in "
                "anoieu.json",
                file=sys.stderr,
            )
            return 2
        written = Baseline(baseline_path).write(diags, sources, root)
        print(f"-- wrote {_show(baseline_path, root)}: {written} finding(s) baselined")
        return 0
    if baseline_path is not None:
        diags, held, stale = Baseline.load(baseline_path).filter(diags, sources, root)

    if args.format == "json":
        print(render_json(diags, root))
    elif args.format == "github":
        print(render_github(diags, root))
    elif args.format == "sarif":
        print(render_sarif(diags, root))
    else:
        color = sys.stdout.isatty() and not args.no_color
        if diags:
            print(render_text(diags, sources, root, color=color), end="")
        print(
            f"-- checked {read} file(s) under "
            f"{len(profiles)} profile(s): "
            f"{counts['decls']} declarations, {counts['programs']} programs, "
            f"{counts['rules']} rules"
        )
        tally = {s: sum(1 for d in diags if d.severity is s) for s in Severity}
        parts = [
            f"{tally[s]} {s.value}{'s' if tally[s] != 1 else ''}" for s in Severity if tally[s]
        ]
        print("-- " + (", ".join(parts) if parts else "nothing to report"))
        if silenced:
            print(f"--   {len(silenced)} silenced by comments in the signature")
        if held:
            print(f"--   {held} held by {_show(baseline_path, root)}")
        if stale:
            print(
                f"--   {len(stale)} baseline entr{'y' if len(stale) == 1 else 'ies'} "
                f"no longer reported; run --update-baseline to prune"
            )

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
    ap.add_argument("--version", action="version", version=f"anoieu {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="check a signature")
    c.add_argument("file", nargs="*", help="entry points; defaults to anoieu.json")
    c.add_argument("--semantics", help="the calculus semantics (.eos) [accepted, not read yet]")
    c.add_argument(
        "--smt-semantics", help="the SMT-LIB semantics (.eos) [accepted, not read yet]"
    )
    c.add_argument("--format", choices=["text", "json", "github", "sarif"], default="text")
    c.add_argument("--config", help="an anoieu.json to use instead of the discovered one")
    c.add_argument("--profile", action="append",
                   help="analyse only this profile of anoieu.json; repeatable")
    c.add_argument("--embedding", help="the .eo file declaring the deep embedding, "
                   "e.g. plugins/model_smt/model_smt.eo")
    c.add_argument("--baseline", help="a baseline file: findings it holds are not reported")
    c.add_argument("--update-baseline", action="store_true", help="rewrite the baseline")
    c.add_argument("--no-suppress", action="store_true",
                   help="ignore `; anoieu: allow` comments")
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
