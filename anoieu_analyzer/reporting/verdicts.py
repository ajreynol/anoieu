#!/usr/bin/env python3
"""The verdict audit: is every closure readable, and did what we closed land?

A finding closes on a `closed_verdict` written to its `bug_db/bugs.json` entry
by `prompts/close_bug_db`, against a named commit and a re-reading of the source.
**A verdict is one of seven words**, and the list is the whole of it --
`bug_db/README.md` defines it under *Closure*, this module is the copy that runs,
and `tests/run.py` compares the two.

The vocabulary is closed for one reason. `accepted and fixed` closes a finding
*before* its change reaches the project's default branch, which is the one
mistake this repository has already made and had for three months --

    three cvc5 rows sat closed as *fixed upstream* on a fix that never landed,
    and nothing noticed, because a closed entry is one nothing re-derives.

So the debt is written down, as an `awaiting_landing` object naming where the
change is, and this reads them back. Requiring an *outcome* rather than a phrase
is what makes that checkable: a marker in prose can be reworded out of existence
and a required word cannot. Rewording a verdict now takes it out of the
vocabulary rather than out of the audit.

    python3 -m anoieu_analyzer.reporting.verdicts          # what is outstanding
    python3 -m anoieu_analyzer.reporting.verdicts --check  # ... and ask each checkout

Checkouts come from `anoieu_analyzer/reporting/config/repos.local`, or `--repo`.
A project with no checkout is reported as unknown rather than skipped: an audit
that quietly drops what it could not reach is the thing it exists to prevent.

Nothing here writes. When a change lands, a person replaces the entry's
`awaiting_landing` with the commit that landed it.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

from . import ROOT, CONFIG_DIR

DB = os.path.join(ROOT, "bug_db", "bugs.json")
REPOS = os.path.join(CONFIG_DIR, "repos.local")

#: **What a verdict may be, and which of them owes a landing.** The copy that
#: runs; the definition is *Closure* in `bug_db/README.md`, and `tests/run.py`
#: compares the two.
PROMISE, LANDED, SETTLED = "promise", "landed", "settled"
OUTCOMES = {
    "accepted and fixed": PROMISE,
    "fixed and landed": LANDED,
    "declined": SETTLED,
    "intentional": SETTLED,
    "not audited": SETTLED,
    "withdrawn": SETTLED,
    "re-coded": SETTLED,
}

REQUIRED = ("project", "branch", "commit")


def entries(path: str = DB) -> list[dict]:
    """Every database entry carrying a verdict."""
    with open(path, encoding="utf-8") as fh:
        return [b for b in json.load(fh)["bugs"] if "closed_verdict" in b]


def unreadable(path: str = DB) -> list[str]:
    """Closures whose verdict is not in the vocabulary.

    Not a style lapse: an outcome nothing can read is how a debt leaves this
    audit without leaving the database.
    """
    return [b["id"] for b in entries(path) if b["closed_verdict"] not in OUTCOMES]


def malformed(path: str = DB) -> list[str]:
    """Closures whose `awaiting_landing` does not name a place to look."""
    out = []
    for b in entries(path):
        m = b.get("awaiting_landing")
        if m is None:
            continue
        if not isinstance(m, dict) or not all(str(m.get(k, "")).strip() for k in REQUIRED):
            out.append(b["id"])
    return out


def undeclared(path: str = DB) -> list[str]:
    """Closed on a promise, and does not say where the change is."""
    return [b["id"] for b in entries(path)
            if OUTCOMES.get(b["closed_verdict"]) == PROMISE
            and not b.get("awaiting_landing")]


def overdeclared(path: str = DB) -> list[str]:
    """Carries a landing to watch and is not closed on a promise.

    A settled or landed entry still naming a branch is a contradiction somebody
    has to resolve, and it inflates the outstanding count.
    """
    return [b["id"] for b in entries(path)
            if b.get("awaiting_landing")
            and OUTCOMES.get(b["closed_verdict"]) in (LANDED, SETTLED)]


def outstanding(path: str = DB) -> list[dict]:
    """Every closure still owing a landing, with where to look for it."""
    return [b for b in entries(path) if b.get("awaiting_landing")]


def _checkouts(overrides: list[str] | None) -> dict[str, str]:
    repos: dict[str, str] = {}
    if os.path.isfile(REPOS):
        for line in open(REPOS):
            line = line.split("#")[0].strip()
            if line and len(line.split()) == 2:
                name, path = line.split()
                repos[name] = path
    for item in overrides or []:
        name, _, path = item.partition("=")
        repos[name] = path
    return repos


def _landed(root: str, commit: str) -> bool | None:
    """Has `commit` reached the checkout's default branch? None if unaskable."""
    if not os.path.isdir(os.path.join(root, ".git")):
        return None
    try:
        head = subprocess.run(
            ["git", "-C", root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
            capture_output=True, text=True, timeout=30)
        branch = head.stdout.strip() or "origin/main"
        r = subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor",
                            commit, branch], capture_output=True, timeout=30)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="ask each checkout whether the commit has landed")
    ap.add_argument("--repo", action="append", metavar="name=/path",
                    help="a checkout to ask; repeatable")
    ap.add_argument("--db", default=DB)
    args = ap.parse_args(argv)

    failures = 0
    for fid in unreadable(args.db):
        print(f"FAIL {fid}: verdict is not in the vocabulary", file=sys.stderr)
        failures += 1
    for fid in malformed(args.db):
        print(f"FAIL {fid}: awaiting_landing names no place to look", file=sys.stderr)
        failures += 1
    for fid in undeclared(args.db):
        print(f"FAIL {fid}: `accepted and fixed` and does not say where the change is",
              file=sys.stderr)
        failures += 1
    for fid in overdeclared(args.db):
        print(f"FAIL {fid}: carries a landing and is not closed on a promise",
              file=sys.stderr)
        failures += 1

    owed = outstanding(args.db)
    print(f"-- {len(owed)} closure(s) recorded before the change landed")
    repos = _checkouts(args.repo) if args.check else {}
    for b in owed:
        m = b["awaiting_landing"]
        where = f"{m['project']} {m['branch']}@{m['commit']}"
        state = "unknown"
        if args.check:
            root = repos.get(m["project"])
            got = _landed(root, m["commit"]) if root else None
            state = {True: "LANDED", False: "not yet", None: "unknown"}[got]
        print(f"   {state:8s} {b['id']}  {where}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
