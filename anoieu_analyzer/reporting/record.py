#!/usr/bin/env python3
"""Collect every finding this project reports, and record it through koine.

Maintaining this? Start at `docs/maintenance.md`.

**There is one record, and it is `bug_db/bugs.json`.** This module finds what
there is to record and hands it to koine, which is that file's only writer. It
writes no ledger of its own: the verdict against a finding, and the prose behind
it, live on the database entry -- see *Closure* in `bug_db/README.md`.

Two sources, one dump. The **checks** are re-derived on every run, over the
corpora in `deps/`. The **fuzzer** cannot be -- re-deriving one of its findings
means running somebody else's binary, which this job does not have -- so its
findings come from `tests/fuzz/`, the reproducers a person promoted, and are
told apart by their `FUZ` code.

A koine failure fails the run. `--check` uses koine's dry run and writes
nothing. A normal run also refreshes `bug_db/bugs.md` and
`bug_db/static-analysis.md` with the findings still open in the database.

**Recording is additive and closure is not its business.** koine adds what is
new and never removes what is there, so a finding that has stopped being
reported keeps its entry and its dates. Deciding that something is *fixed* takes
a commit and a re-reading, which is `prompts/close_bug_db`, not a diff between
two dumps.

    python3 -m anoieu_analyzer.reporting.record             # record anything new
    python3 -m anoieu_analyzer.reporting.record --check     # koine dry run; write nothing
    python3 -m anoieu_analyzer.reporting.record --roots elsewhere
"""

from __future__ import annotations

import argparse
import json
import os
import sys


from anoieu_analyzer.checks import Context, load_checks, run_all  # noqa: E402
from anoieu_analyzer.cli import _embedding_vocabulary  # noqa: E402
from anoieu_analyzer.fingerprint import fingerprint  # noqa: E402
from anoieu_analyzer.loader import load  # noqa: E402
from anoieu_analyzer.semantics import load_set  # noqa: E402

from .gen_corpus_table import DEFAULT_ROOTS, TARGETS, not_audited, signatures  # noqa: E402
from . import koine  # noqa: E402
from .targets import commit_of  # noqa: E402
from .database import render as render_database

from anoieu_fuzz.report import rows as fuzz_rows  # noqa: E402
from anoieu_fuzz.report import bugs as fuzz_bugs, load as load_fuzz  # noqa: E402

from . import ROOT
DB = os.path.join(ROOT, "bug_db", "bugs.json")
DUMP = os.path.join(ROOT, "scratch", "new-report-bugs.json")
STATIC_PAGE = os.path.join(ROOT, "bug_db", "static-analysis.md")



def owner_of(path: str, roots: dict) -> str:
    for name, root in roots.items():
        if os.path.abspath(path).startswith(os.path.abspath(root) + os.sep):
            return name
    return "—"


def collect(roots: dict, targets: list | None = None, fuzz: bool = True) -> dict[str, dict]:
    """Every finding, keyed by the fingerprint a closing step refers to.

    `targets` defaults to every standard target, which is what a report is. It
    is a parameter because `scripts/anoieu_analyzer` runs them one at a time,
    so that each row can record which target saw it and at what commit -- a row's
    absence says nothing until the record says whether anything read its file.
    `fuzz` is off there for the same reason: the fuzzer is a separate producer
    and a static analysis run should not claim its findings as something it read.
    """
    load_checks()
    out: dict[str, dict] = {}
    for _label, repo, rels, triple in (TARGETS if targets is None else targets):
        paths = [os.path.join(roots[repo], r) for r in rels]
        needed = list(paths) + (
            [os.path.join(roots[r], rel) for r, rel in triple.values()] if triple else []
        )
        if not all(os.path.exists(p) for p in needed):
            continue
        sem = smt = None
        embed: set[str] = set()
        if triple:
            r, rel = triple["semantics"]
            sem = load_set(os.path.join(roots[r], rel))
            r, rel = triple["smt"]
            smt = load_set(os.path.join(roots[r], rel))
            r, rel = triple["embedding"]
            embed = _embedding_vocabulary(os.path.join(roots[r], rel))
        skip = not_audited(repo, roots[repo])
        for group in signatures(paths, skip):
            result = load(group)
            ctx = Context(
                signature=result.signature,
                files=result.files,
                sources=result.sources,
                root=roots[repo],
                include_edges=result.include_edges,
                semantics=sem,
                smt_semantics=smt,
                embedding_names=embed,
            )
            for d in list(result.diagnostics) + run_all(ctx):
                if d.code.startswith("ANO"):
                    continue
                if os.path.abspath(d.span.path) in skip:
                    continue  # see NOT_AUDITED in anoieu_analyzer/reporting/gen_corpus_table.py
                owner = owner_of(d.span.path, roots)
                key = fingerprint(d, result.sources, roots.get(owner, roots[repo]))
                if key in out:
                    continue
                where = os.path.relpath(d.span.path, roots.get(owner, roots[repo]))
                out[key] = {
                    "owner": owner,
                    "code": d.code,
                    "where": f"{where}:{d.span.line}",
                    "what": d.message.replace("|", "\\|"),
                }
    # and the findings that came from the other half. They are keyed by the
    # same fingerprint and shaped the same way, so from here down nothing
    # distinguishes them but their code -- which is the point.
    if fuzz:
        for key, row in fuzz_rows().items():
            out.setdefault(key, row)
    return out




def static_bug(fid: str, row: dict, commit: str) -> dict:
    """A static row in the input shape koine consumes, shared by both runners."""
    path, _, line = row["where"].rpartition(":")
    return {
        "id": fid,
        "bug": f"{row['code']}-{os.path.basename(path)}-{line}",
        "tool": "anoieu",
        "description": row["what"],
        "owner": row["owner"],
        "code": row["code"],
        "where": row["where"],
        "found_at": commit,
    }


def record(found: dict, roots: dict, preview: bool = False) -> int:
    """Hand both producers' findings to koine, which is the database's only writer."""
    bugs = [static_bug(fid, row, commit_of(roots.get(row["owner"], "")))
            for fid, row in found.items() if not row["code"].startswith("FUZ")]
    bugs.extend(fuzz_bugs(load_fuzz()))
    os.makedirs(os.path.dirname(DUMP), exist_ok=True)
    with open(DUMP, "w", encoding="utf-8") as fh:
        json.dump(bugs, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    code = koine.main([DUMP, DB] + (["--dry-run"] if preview else []))
    if code == 0 and not preview:
        render_database(DB, STATIC_PAGE)
    return code


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", help="a directory of clones; defaults to deps/")
    ap.add_argument("--check", action="store_true",
                    help="koine dry run; write nothing")
    args = ap.parse_args()

    roots = dict(DEFAULT_ROOTS)
    if args.roots:
        roots = {name: os.path.join(args.roots, name) for name in DEFAULT_ROOTS}

    found = collect(roots)
    code = record(found, roots, preview=args.check)
    if code:
        return code

    if args.check:
        print(f"-- {len(found)} finding(s) collected; koine accepted the dry run")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
