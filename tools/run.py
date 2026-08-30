#!/usr/bin/env python3
"""The run: refresh what we analyse, measure it, and append anything new.

One command, four steps, in this order:

1. **Bump.** The tools we find bugs in move, and a report of yesterday's commit
   is a report about nothing. Each watched checkout is fetched and, with
   `--bump`, fast-forwarded onto its upstream. Nothing is ever forced: a
   checkout with uncommitted work, without an upstream, or whose upstream is not
   a fast-forward is left alone and said so, because these are trees somebody
   else is working in.
2. **Versions.** What the run reads is pinned in `docs/versions.md` by branch,
   commit and date. A finding is only ever true of a version, and the report's
   rows carry none of their own, so this is what they are relative to.
3. **Counts.** `docs/corpus.md`, rewritten whole.
4. **Findings.** `docs/open-findings.md`, appended to and never trimmed — a row
   leaves it only through the review step described in `docs/ci.md`.

    python3 tools/run.py                  # fetch, report what is behind, measure
    python3 tools/run.py --bump           # ... and fast-forward what safely can be
    python3 tools/run.py --check          # verify without writing; what CI runs
    python3 tools/run.py --roots corpus   # the CI layout

Every step prints one `--` line and its detail beneath, so the log of a run
reads as what changed.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VERSIONS = os.path.join(ROOT, "docs", "versions.md")

sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from anoieu import __version__  # noqa: E402
from gen_corpus_table import DEFAULT_ROOTS  # noqa: E402

# Repositories a run reads, beside the analyzer itself. A missing one is
# recorded as missing rather than skipped silently.
WATCHED = [
    # cvc5's `proofs/eo` and nothing else: whether the *solver* can justify what
    # it decides -- its build system, its proof-production code, the emitter --
    # is dokimasia's job, not ours. See docs/design.md, "A neighbouring tool".
    ("cvc5", "`proofs/eo`: the CPC signature and the expert extension"),
    (
        "ethos",
        "three of the tools at once: the checker, `ethos-eoc`, and `user_manual.md`, "
        "which is where Eunoia is defined",
    ),
    ("logos", "the Lean development, and the CPC semantics it owns"),
    ("eudaimonia", "the template, and the example calculi we read"),
]


def git(root: str, *args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", root, *args], capture_output=True, text=True, timeout=30
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def fetch(root: str) -> str:
    """Bring the checkout's knowledge of its upstream up to date, changing
    nothing in the tree."""
    if not os.path.isdir(root):
        return "not present"
    if not git(root, "rev-parse", "--abbrev-ref", "@{u}"):
        return "no upstream to compare against"
    out = subprocess.run(
        ["git", "-C", root, "fetch", "--quiet"], capture_output=True, text=True
    )
    if out.returncode:
        return "could not fetch (offline?)"
    behind = git(root, "rev-list", "--count", "HEAD..@{u}") or "0"
    ahead = git(root, "rev-list", "--count", "@{u}..HEAD") or "0"
    if behind == "0" and ahead == "0":
        return "current"
    parts = []
    if behind != "0":
        parts.append(f"{behind} behind")
    if ahead != "0":
        parts.append(f"{ahead} ahead")
    return " and ".join(parts)


def bump(root: str) -> str:
    """Fast-forward a checkout onto its upstream, or say why it was left alone.

    Deliberately timid: these are working trees, and a report is not worth
    disturbing one. Nothing is stashed, nothing is merged, nothing is forced.
    """
    status = fetch(root)
    if status in ("not present", "no upstream to compare against", "could not fetch (offline?)"):
        return status
    if git(root, "status", "--porcelain"):
        return "left alone: uncommitted changes"
    behind = git(root, "rev-list", "--count", "HEAD..@{u}") or "0"
    if behind == "0":
        return status
    out = subprocess.run(
        ["git", "-C", root, "merge", "--ff-only", "@{u}"], capture_output=True, text=True
    )
    if out.returncode:
        return f"left alone: {behind} behind, and not a fast-forward"
    return f"fast-forwarded {behind} commit(s)"


def describe(root: str) -> dict | None:
    if not os.path.isdir(root):
        return None
    sha = git(root, "rev-parse", "--short=12", "HEAD")
    if not sha:
        return None
    return {
        "branch": git(root, "rev-parse", "--abbrev-ref", "HEAD") or "—",
        "commit": sha,
        "date": git(root, "log", "-1", "--format=%cs"),
        "dirty": bool(git(root, "status", "--porcelain")),
    }


def render_versions(roots: dict) -> str:
    rows = []
    me = describe(ROOT)
    rows.append(
        ("anoieu", "this analyzer", me or {"branch": "—", "commit": "—", "date": "—"})
    )
    for name, what in WATCHED:
        rows.append((name, what, describe(roots.get(name, "")) or {}))

    out = [
        "# What the report was measured against",
        "",
        "Written by `tools/run.py`. A finding is only ever true of a version: the",
        "rows in [`open-findings.md`](open-findings.md) carry none of their own, and",
        "this is what they are relative to. A row that outlives the commit it was",
        "found in is a row worth re-checking.",
        "",
        "| tool | what it holds | branch | commit | dated |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name, what, v in rows:
        if not v:
            out.append(f"| **{name}** | {what} | — | *not present* | — |")
            continue
        dirty = " *(uncommitted changes)*" if v.get("dirty") else ""
        out.append(
            f"| **{name}** | {what} | `{v['branch']}` | `{v['commit']}`{dirty} | "
            f"{v.get('date', '—')} |"
        )
    out += [
        "",
        f"The analyzer reports its own version as `{__version__}`; the commit above is",
        "what actually ran.",
        "",
        "A repository shown with uncommitted changes measured a working tree rather",
        "than a commit, so its findings are not reproducible from the commit alone.",
    ]
    return "\n".join(out) + "\n"


def step(msg: str) -> None:
    print(f"-- {msg}")


def item(msg: str) -> None:
    print(f"--   {msg}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", help="a directory holding cvc5/, ethos/ and logos/")
    ap.add_argument(
        "--check", action="store_true", help="verify without writing; what CI runs"
    )
    ap.add_argument(
        "--bump",
        action="store_true",
        help="fast-forward each watched checkout onto its upstream where that is safe",
    )
    args = ap.parse_args()

    roots = dict(DEFAULT_ROOTS)
    if args.roots:
        roots = {name: os.path.join(args.roots, name) for name in DEFAULT_ROOTS}

    passthrough = ["--roots", args.roots] if args.roots else []
    failures = 0

    if not args.check:
        step("Bumping the tools we read" if args.bump else "Checking what has moved")
        for name, _what in WATCHED:
            root = roots.get(name, "")
            item(f"{name:11} {bump(root) if args.bump else fetch(root)}")

    step("Recording what this run reads")
    text = render_versions(roots)
    for name, _what in WATCHED:
        v = describe(roots.get(name, ""))
        item(f"{name:8} {'not present' if not v else v['branch'] + ' @ ' + v['commit']}")
    if args.check:
        current = open(VERSIONS).read() if os.path.isfile(VERSIONS) else ""
        if current != text:
            item("docs/versions.md is stale; run tools/run.py")
    elif not os.path.isfile(VERSIONS) or open(VERSIONS).read() != text:
        with open(VERSIONS, "w") as f:
            f.write(text)
        item("docs/versions.md updated")

    for title, script in (
        ("Counting what the checks report", "gen_corpus_table.py"),
        ("Appending anything new to the report", "gen_open_findings.py"),
    ):
        step(title)
        cmd = [sys.executable, os.path.join(HERE, script)] + passthrough
        if args.check:
            cmd.append("--check")
        result = subprocess.run(cmd, capture_output=True, text=True)
        for line in (result.stdout + result.stderr).splitlines():
            item(line.lstrip("- ").strip())
        failures += 1 if result.returncode else 0

    if failures:
        print(
            "error: the report is not current; run `python3 tools/run.py` and commit",
            file=sys.stderr,
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
