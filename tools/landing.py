#!/usr/bin/env python3
"""The landing audit: did the changes we closed on actually land?

A row closes here when a maintainer accepted it and the change is a commit on a
named branch -- not when that branch is merged. `docs/reports/reporting-workflow.md` says
why: holding a finding open until somebody else's review queue drains is not
information about the finding. What it buys in agility it borrows against the
one failure this repository has already had, and had for three months --

    three cvc5 rows sat closed as *fixed upstream* on a fix that never landed,
    and nothing noticed, because a closed id is one nothing re-derives.

So the debt is written down. A row closed before its change has landed ends its
verdict with a marker naming where the change is:

    awaiting landing: <project> <branch> <commit>

and this reads them back. It is a **separate pass with its own question** -- did
what we closed actually land -- asked on its own schedule rather than while
somebody is processing a reply. That separation is deliberate: the two get
confused exactly when there is a hurry on, which is when the wrong one is
skipped.

    python3 tools/landing.py             # what is outstanding, from the ledger
    python3 tools/landing.py --check     # ... and ask each checkout about it
    python3 tools/landing.py --repo ethos=/src/ethos --check

Checkouts come from `scripts/repos.local` -- the same mapping `process_anoieu`
uses, and equally optional -- or from `--repo`. A project with no checkout is
reported as unknown rather than skipped: an audit that quietly drops what it
could not reach is the thing it exists to prevent.

Nothing here writes. When a change lands, a person edits the verdict, replacing
the marker with what landed it, and the row leaves this report by saying so.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(ROOT, "docs", "reports", "closed-findings.md")
REPOS = os.path.join(ROOT, "scripts", "repos.local")

#: The marker a row closed on a promise carries, in its verdict cell.
MARKER = re.compile(
    r"awaiting landing:\s+(?P<project>\S+)\s+(?P<branch>\S+)\s+(?P<commit>[0-9a-f]{7,40})\b"
)
_ROW = re.compile(r"^\|\s*`([0-9a-f]{16})`\s*\|")


class Outstanding:
    """One closed row whose change has not been seen to land."""

    def __init__(self, fid: str, project: str, branch: str, commit: str) -> None:
        self.id, self.project, self.branch, self.commit = fid, project, branch, commit
        self.state = "unknown"  # landed | not yet | unknown
        self.detail = ""


def read_ledger(path: str = LEDGER) -> list[Outstanding]:
    """Every `awaiting landing:` marker in the verdicts, in file order."""
    out: list[Outstanding] = []
    with open(path) as f:
        for line in f:
            m = _ROW.match(line)
            if not m:
                continue
            found = MARKER.search(line)
            if found:
                out.append(Outstanding(m.group(1), *found.group("project", "branch", "commit")))
    return out


def malformed(path: str = LEDGER) -> list[str]:
    """Rows that say `awaiting landing` and do not parse.

    Checked rather than assumed, because a marker that has been reworded into
    something unreadable removes a row from this audit without removing the
    debt -- silently, and in the direction that looks fine.
    """
    bad = []
    with open(path) as f:
        for line in f:
            m = _ROW.match(line)
            if m and "awaiting landing" in line and not MARKER.search(line):
                bad.append(m.group(1))
    return bad


def checkouts(extra: list[str]) -> dict[str, str]:
    """Where each project is on this machine: `--repo` wins over repos.local."""
    found: dict[str, str] = {}
    if os.path.exists(REPOS):
        with open(REPOS) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(None, 1)
                if len(parts) == 2:
                    found.setdefault(parts[0], os.path.expanduser(parts[1].strip()))
    for pair in extra:
        name, _, path = pair.partition("=")
        if path:
            found[name] = os.path.expanduser(path)
    return found


def _git(repo: str, *args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", "-C", repo, *args], capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)[:80]
    return p.returncode, (p.stdout or p.stderr).strip()


def base_of(repo: str) -> str:
    """The branch a change is supposed to land on."""
    code, out = _git(repo, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if code == 0 and out:
        return out
    for cand in ("origin/main", "origin/master", "main", "master"):
        if _git(repo, "rev-parse", "--verify", "--quiet", cand)[0] == 0:
            return cand
    return ""


def ask(item: Outstanding, repo: str) -> None:
    """Whether that commit has reached the project's default branch."""
    if _git(repo, "rev-parse", "--is-inside-work-tree")[0] != 0:
        item.detail = f"{repo} is not a git repository"
        return
    if _git(repo, "cat-file", "-e", item.commit + "^{commit}")[0] != 0:
        item.detail = f"{item.commit} is not in this checkout -- fetch, or it was rewritten"
        return
    base = base_of(repo)
    if not base:
        item.detail = "no default branch to compare against"
        return
    if _git(repo, "merge-base", "--is-ancestor", item.commit, base)[0] == 0:
        item.state, item.detail = "landed", f"in {base}"
        return
    item.state = "not yet"
    code, out = _git(repo, "rev-list", "--count", f"{base}..{item.commit}")
    ahead = out if code == 0 else "?"
    item.detail = f"{ahead} commit(s) {base} does not have"


def main() -> int:
    ap = argparse.ArgumentParser(description="what we closed before it landed")
    ap.add_argument("--check", action="store_true",
                    help="ask each checkout whether the commit has landed")
    ap.add_argument("--repo", action="append", default=[], metavar="NAME=PATH",
                    help="where a project is checked out; repeatable")
    args = ap.parse_args()

    bad = malformed()
    items = read_ledger()

    print(f"-- {len(items)} row(s) closed before the change landed")
    if not items:
        print("   nothing is owed")

    repos = checkouts(args.repo) if args.check else {}
    for item in items:
        if args.check:
            repo = repos.get(item.project, "")
            if repo and os.path.isdir(repo):
                ask(item, repo)
            else:
                item.detail = f"no checkout for {item.project}" if not repo else f"{repo} is not there"
        mark = {"landed": "LANDED  ", "not yet": "not yet ", "unknown": "unknown "}[item.state]
        where = f"{item.project} {item.branch}@{item.commit}"
        print(f"   {mark} {item.id}  {where}" + (f"  -- {item.detail}" if item.detail else ""))

    if args.check:
        landed = [i for i in items if i.state == "landed"]
        unknown = [i for i in items if i.state == "unknown"]
        if landed:
            print(f"-- {len(landed)} have landed; edit the verdict to say so and they leave this list")
        if unknown:
            print(f"-- {len(unknown)} could not be answered -- that is an unaudited row, not a clean one")

    if bad:
        print(f"-- {len(bad)} verdict(s) say `awaiting landing` and do not parse: {', '.join(bad)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
