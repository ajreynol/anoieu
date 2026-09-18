#!/usr/bin/env python3
"""Refresh bug_db/bugs.json from static analysis and promoted fuzzer findings.

    python3 scripts/update_bug_db.py --dry-run  # inspect inputs; write nothing
    python3 scripts/update_bug_db.py --preview  # analyse; preview Koine's append
    python3 scripts/update_bug_db.py            # analyse and record both sources

Uses the existing producers and Koine writer. It neither starts a fuzzing
campaign nor updates verdicts. See bug_db/README.md for setup and the artifact.
"""

from __future__ import annotations

import argparse
import os
import sys

import gen_open_findings as findings
import koine
import targets


def missing_inputs(spec: list[dict], roots: dict) -> list[str]:
    """Refuse a partial refresh when a configured target cannot be read."""
    missing = []
    for target in spec:
        needed = [(target["project"], path) for path in target["paths"]]
        needed.extend((target.get("triple") or {}).values())
        for project, path in needed:
            root = roots.get(project, "")
            if not root or not os.path.exists(os.path.join(root, path)):
                missing.append(f"{target['id']}: {project}/{path}")
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true",
                      help="check setup and list inputs without analysis or writes")
    mode.add_argument("--preview", action="store_true",
                      help="run analysis and preview the append without changing the database")
    args = parser.parse_args(argv)

    spec = targets.load()
    roots, source = targets.roots()
    if args.dry_run:
        print("\n".join(targets.describe(spec)))
    missing = missing_inputs(spec, roots)
    if missing:
        print("-- missing inputs; configure scripts/repos.local or prepare deps/ "
              "before refreshing the database:", file=sys.stderr)
        for path in missing:
            print(f"   {path}", file=sys.stderr)
        return 2

    # Validate promoted evidence before asking either producer to update the DB.
    try:
        fuzz = findings.fuzz_bugs(findings.load_fuzz())
        tool = koine.find(clone=not args.dry_run)
        print(f"-- koine {koine.version(tool) or '(unknown)'} at {tool}")
        print(f"-- {len(fuzz)} promoted fuzzer finding(s); recorded evidence, not replayed")
        print(f"-- database: {findings.DB}")
        if args.dry_run:
            return 0
        print(f"-- analysing {len(spec)} target(s), paths from {source}", flush=True)
        found = findings.collect(roots, targets=targets.as_tuples(spec), fuzz=False)
        print(f"-- {len(found)} static finding(s); recording both sources through koine",
              flush=True)
        code = findings.record(found, roots, preview=args.preview)
        if code:
            return code
        if not args.preview:
            findings.render_static(findings.DB, findings.STATIC_PAGE)
        return 0
    except (OSError, ValueError) as exc:
        print(f"-- cannot refresh bug database: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
