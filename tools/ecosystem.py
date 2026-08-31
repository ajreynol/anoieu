#!/usr/bin/env python3
"""Print the state of the Eunoia ecosystem: who is in it, and how they look.

No assistant and no prompting -- this is a local command that reads trees and
reports. It is the thing to run when the question is *where does everything
stand*; `scripts/global_audit` is the thing to run when the question needs
somebody to read across the answer and form a view.

    python3 tools/ecosystem.py            # the table
    python3 tools/ecosystem.py --verbose  # and why each policy verdict came out

Health here means **what can be established from a checkout in about a second**:
does it declare membership, does the policy check pass, is there a channel to
reach them, how long since anything moved. It deliberately does not build,
test, or read anybody's source. A row that says `ok` is a claim about form, and
a quiet row is not evidence that a tool is well -- the same caution the analyzer
carries about its own silence applies here.

Membership is a decision rather than a measurement, so the `status` column comes
from `tools/ecosystem.json` and is never inferred. Where the measurement and the
recorded status disagree, the row says so; changing the file is a person's job.
"""

from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY = os.path.join(ROOT, "tools", "ecosystem.json")
REPOS_FILE = os.environ.get("ANOIEU_REPOS_FILE",
                            os.path.join(ROOT, "scripts", "repos.local"))


def git(*args, cwd=None):
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def locate(repo: str) -> str:
    """A repo id, the way every script here resolves one: the mapping file, then
    a scan of $ANOIEU_REPOS. Never a bare path -- these ids come from a file."""
    if os.path.isfile(REPOS_FILE):
        for line in open(REPOS_FILE, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2 and parts[0] == repo:
                path = os.path.expanduser(parts[1].strip())
                if os.path.isdir(path):
                    return path
    for r in os.environ.get("ANOIEU_REPOS", os.path.expanduser("~")).split(":"):
        cand = os.path.join(r, repo)
        if os.path.isdir(cand):
            return cand
    return ""


def age(path: str) -> str:
    when = git("log", "-1", "--format=%cI", cwd=path)
    if not when:
        return "?"
    then = datetime.datetime.fromisoformat(when)
    days = (datetime.datetime.now(then.tzinfo) - then).days
    return "today" if days == 0 else f"{days}d"


def check(path: str) -> tuple[str, list[str]]:
    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "policy_check.py"),
         "--root", path], capture_output=True, text=True)
    # count the failing *checks*, not their detail lines: one check that reports
    # three things is one thing wrong, and saying "3 fail" overstates it.
    failed = [l[5:] for l in out.stdout.splitlines() if l.startswith("FAIL ")]
    detail = [l.strip() for l in out.stdout.splitlines() if l.startswith("     ")]
    return ("ok" if out.returncode == 0 else f"{len(failed)} failing"), detail


def main() -> int:
    verbose = "--verbose" in sys.argv
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    rows, notes = [], []

    for name, e in inv.items():
        if name == "_comment":
            continue
        status = e.get("status", "?")
        if status in ("child", "served"):
            rows.append((name, status, "-", "-", "-", e.get("parent", "")))
            continue
        path = locate(e.get("repo", name))
        if not path:
            rows.append((name, status, "no checkout", "-", "-", ""))
            continue
        verdict, fails = check(path)
        topics = ""
        disc = os.path.join(path, "docs", "discussion.md")
        if os.path.isfile(disc):
            text = open(disc, encoding="utf-8").read()
            for_us = text.count("**To:** anoieu")
            topics = f"{for_us} for us" if for_us else "yes"
        else:
            topics = "none"
        rows.append((name, status, verdict, topics, age(path), path))
        if verdict == "ok" and status == "candidate":
            notes.append(f"{name} passes and is recorded as a candidate: "
                         "if it declares membership, the status is out of date")
        if verdict != "ok" and status == "member":
            notes.append(f"{name} is recorded as a member and does not pass: "
                         "this is the state the check exists to catch")
        if verbose and fails:
            notes.append(f"{name}: " + "; ".join(fails[:6]))

    w = max(len(r[0]) for r in rows) + 2
    print(f"{'tool':<{w}}{'status':<11}{'policy':<12}{'channel':<10}{'moved':<8}where")
    for name, status, verdict, topics, moved, where in rows:
        short = where.replace(os.path.expanduser("~"), "~") if where else ""
        print(f"{name:<{w}}{status:<11}{verdict:<12}{topics:<10}{moved:<8}{short}")

    if notes:
        print()
        for n in notes:
            print(f"note: {n}")
    print()
    print("Form only. A passing row says those checks passed on that tree, and "
          "nothing about\nwhether the tool is any good -- see docs/reports/"
          "reporting-policy.md on silence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
