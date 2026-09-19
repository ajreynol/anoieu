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
`awaiting_landing` with the commit that landed it -- and where a pull request was
squashed or rebased, `--check` names the commit that carries the change so that
the person is not left to find it.
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


def _git(root: str, *args: str) -> str:
    try:
        r = subprocess.run(["git", "-C", root, *args],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout if r.returncode == 0 else ""


def _patch_id(root: str, commit: str) -> str:
    """What `commit` changes, independent of which commit carries it.

    `git patch-id --stable` over the commit's own diff. Two commits with the
    same patch id are the same change, which is what survives a rebase or a
    squash.
    """
    diff = _git(root, "show", "--no-color", commit)
    if not diff:
        return ""
    try:
        r = subprocess.run(["git", "-C", root, "patch-id", "--stable"],
                           input=diff, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout.split()[0] if r.stdout.split() else ""


def _landed(root: str, commit: str) -> tuple[str, str]:
    """Has the change reached the default branch, and under which commit?

    Returns one of `LANDED`, `not yet` or `unknown`, and the commit that carries
    it where that is not the one we recorded.

    **Asking only whether the commit is an ancestor of the default branch is the
    wrong question**, and it answered *no* forever for every project that
    squash-merges. ethos accepted seven findings on a branch, merged them as one
    squashed pull request, and this audit went on reporting the debt as
    outstanding — under-reporting in the safe direction, which is worse than it
    sounds: an audit that cannot ever clear an item is one people stop reading.

    So the exact question is asked first, and where it says no, the change is
    looked for by **patch id** among the commits the default branch has that the
    recorded commit's branch point does not. A rebase or a squash of a single
    commit preserves the patch id; a squash of several does not, and that case
    is still reported as `not yet` rather than guessed at.
    """
    if not root or not os.path.isdir(os.path.join(root, ".git")):
        return "unknown", ""
    branch = _git(root, "symbolic-ref", "--short",
                  "refs/remotes/origin/HEAD").strip() or "origin/main"
    if not _git(root, "rev-parse", "--verify", "--quiet", commit + "^{commit}"):
        return "unknown", ""
    try:
        r = subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor",
                            commit, branch], capture_output=True, timeout=30)
        if r.returncode == 0:
            return "LANDED", ""
    except (OSError, subprocess.SubprocessError):
        return "unknown", ""

    want = _patch_id(root, commit)
    if not want:
        return "not yet", ""
    base = _git(root, "merge-base", commit, branch).strip()
    if not base:
        return "not yet", ""
    for line in _git(root, "log", "--format=%H", f"{base}..{branch}").split():
        if _patch_id(root, line) == want:
            return "LANDED", line
    return "not yet", ""


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
        state, carried = "unknown", ""
        if args.check:
            state, carried = _landed(repos.get(m["project"], ""), m["commit"])
        note = f"  -- landed as {carried[:12]}" if carried else ""
        print(f"   {state:8s} {b['id']}  {where}{note}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
