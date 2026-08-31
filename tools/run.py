#!/usr/bin/env python3
"""The run: refresh the sources, measure them, and append anything new.

Maintaining this? Start at `docs/coherence.md`.

Three steps, in order:

1. **Sync.** Every project a report is about is cloned into `deps/` and updated
   from its remote — shallow, sparse, and managed by us. Nothing reads a
   checkout somebody else owns, so a report is a property of named commits
   rather than of the machine it was generated on. `tools/deps.json` says which
   projects, which refs, and which paths of each; changing a ref there changes
   what the report is a report of.
2. **Measure.** `docs/reports/corpus.md`, rewritten whole: the commits that were read,
   and what the checks report on them. A count and the version it was taken from
   belong in one file.
3. **Findings.** `docs/reports/open-findings.md`, appended to and never trimmed — a row
   leaves it only through the review step described in
   `docs/reports/reporting-workflow.md`.

    python3 tools/run.py                 # move to each tip, then measure
    python3 tools/run.py --pinned --check # re-measure the recorded commits
    python3 tools/run.py --offline       # measure whatever deps/ already holds

Two of those are different questions. Without `--pinned` a run asks *what is
true of the projects now*, which is what produces a new report and what a
scheduled refresh does. With `--pinned` it asks *do the recorded versions still
report what this file says they report*, which depends on nothing but this
repository — so a red build means a check changed, never that somebody upstream
pushed. That is the one CI runs on a push.

Nothing is built. The analysis reads signatures, semantics and configuration as
text, so a clone needs no toolchain and no history; the one thing that does need
a built ethos is the differential oracle, which is a separate job.

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
CORPUS = os.path.join(ROOT, "docs", "reports", "corpus.md")

sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import deps as deps_mod  # noqa: E402
import gen_corpus_table as corpus_mod  # noqa: E402

from anoieu import __version__  # noqa: E402


def git(root: str, *args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", root, *args], capture_output=True, text=True, timeout=30
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def render_corpus(synced: list, rows: list) -> str:
    """`docs/reports/corpus.md`: the versions a run read, and what the checks said about
    them. One file, because a count is only meaningful next to the commit it was
    taken from."""
    out = [
        "# The corpus: what was measured, and what the checks report",
        "",
        "Written by `tools/run.py`. Nothing here is typed by hand, and anything",
        "that is will be lost on the next run.",
        "",
        "## The versions",
        "",
        "Every project below is a clone this repository manages under `deps/`,",
        "restored to the commit named before the run that produced this file — not",
        "a checkout on anyone's machine. A finding is only ever true of a version,",
        "and the rows in [`open-findings.md`](open-findings.md) carry none of their",
        "own, so these are what they are relative to.",
        "",
        "| project | ref | commit | dated | what is read |",
        "| --- | --- | --- | --- | --- |",
    ]
    for d in synced:
        commit = f"`{d.sha}`" if d.sha else "*not cloned*"
        out.append(f"| **{d.name}** | `{d.ref}` | {commit} | {d.date or '—'} | {d.reads} |")
    out += [
        "",
        f"Produced by anoieu `{__version__}`. Which commit of anoieu produced it is",
        "the commit this file is committed in, and is deliberately not written here:",
        "recording it would make the file stale the moment it was committed.",
        "",
        "The clones are shallow and sparse: only the paths `tools/deps.json` names",
        "are checked out, and nothing is built, because the analysis reads text.",
        "",
        corpus_mod.render(rows),
    ]
    return "\n".join(out)


def step(msg: str) -> None:
    print(f"-- {msg}")


def item(msg: str) -> None:
    print(f"--   {msg}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", help="a directory of clones; defaults to deps/")
    ap.add_argument(
        "--check", action="store_true", help="verify without writing; what CI runs"
    )
    ap.add_argument(
        "--offline",
        action="store_true",
        help="measure whatever deps/ already holds, without fetching",
    )
    ap.add_argument(
        "--pinned",
        action="store_true",
        help="re-measure the commits docs/reports/corpus.md records, not each tip",
    )
    args = ap.parse_args()

    deps_dir = args.roots or deps_mod.DEPS
    passthrough = ["--roots", deps_dir] if args.roots else []
    failures = 0

    pinned = deps_mod.read_lock() if args.pinned else {}
    step(
        "Using deps/ as it stands"
        if args.offline
        else "Restoring the recorded commits under deps/"
        if pinned
        else "Syncing the sources under deps/"
    )
    synced = []
    for dep in deps_mod.manifest():
        d = deps_mod.sync(dep, deps_dir, args.offline, pinned.get(dep.name, ""))
        synced.append(d)
        item(f"{d.name:11} {d.ref:16} {d.status:24} {d.sha}")
    if any(not d.sha for d in synced):
        item("a project is missing; what it holds is reported as not measured")
    astray = [d.name for d in synced if pinned.get(d.name) and d.full != pinned[d.name]]
    if astray:
        item(f"could not restore: {', '.join(astray)} — the comparison below is not pinned")
        # Under --check this is the failure, and it has to be reported as that
        # one. Everything after this point compares against something other than
        # the recorded commits, so a difference it finds is about the restore
        # rather than about a check -- and the advice for a stale report, run the
        # generator and commit, would here write a *worse* lock than the one it
        # could not restore.
        failures += 1 if args.check else 0

    step("Measuring what the checks report")
    roots = corpus_mod.roots_for(deps_dir) if args.roots else corpus_mod.DEFAULT_ROOTS
    rows = corpus_mod.measure_all(roots)
    measured = sum(1 for *_x, ok in rows if ok)
    item(f"{measured} of {len(rows)} corpora measured")
    written = [
        (CORPUS, "docs/reports/corpus.md", render_corpus(synced, rows)),
        (deps_mod.LOCK, "tools/deps.lock", deps_mod.render_lock(synced)),
    ]
    for path, label, text in written:
        current = open(path).read() if os.path.isfile(path) else ""
        if args.check:
            stale = current != text
            item(f"{label} is stale" if stale else f"{label} is current")
            # Under --pinned the commits are restored exactly, so a difference
            # here is a check of ours reporting something new -- worth failing
            # on. Unpinned it means upstream moved, which is news rather than a
            # fault, and that run is not the one CI does.
            failures += 1 if stale else 0
        elif current != text:
            with open(path, "w") as f:
                f.write(text)
            item(f"{label} updated")
        else:
            item(f"{label} unchanged")

    for title, script in (
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

    if astray and args.check:
        print(
            f"error: could not restore {', '.join(astray)} at the commit "
            "tools/deps.lock records, so nothing below was measured against what "
            "the report claims. Fix the pin or the ref in tools/deps.json; "
            "running the generator here would only record the shortfall.",
            file=sys.stderr,
        )
    elif failures:
        print(
            "error: the report is not current; run `python3 tools/run.py` and commit",
            file=sys.stderr,
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
