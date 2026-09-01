#!/usr/bin/env python3
"""Print the state of the Eunoia ecosystem: who is in it, and how they look.

No assistant and no prompting -- this is a local command that reads trees and
reports. It is the thing to run when the question is *where does everything
stand*; `scripts/prompts/global_audit` is the thing to run when the question needs
somebody to read across the answer and form a view.

    python3 tools/ecosystem.py            # the table
    python3 tools/ecosystem.py --verbose  # and why each policy verdict came out
    python3 tools/ecosystem.py --check    # is the inventory itself still true?
    python3 tools/ecosystem.py --check --online   # ... and ask each remote

Health here means **what can be established from a checkout in about a second**:
does it declare membership, does the policy check pass, is there a channel to
reach them, how long since anything moved. It deliberately does not build,
test, or read anybody's source. A row that says `ok` is a claim about form, and
a quiet row is not evidence that a tool is well -- the same caution the analyzer
carries about its own silence applies here.

Membership is a decision rather than a measurement, so the `status` column comes
from `tools/ecosystem.json` and is never inferred. Where the measurement and the
recorded status disagree, the row says so; changing the file is a person's job.

`--check` is the same principle with an exit code, and it is what CI runs. Two
questions, and the second is why it exists:

**Is the inventory well formed?** Offline, and always: every entry has the fields
its status requires, every parent named by a child exists, no two ids are one
typo apart, and every repository the board addresses has a row here.

**Is it still true?** With `--online`, each entry that is somebody's own
repository has its README fetched from the remote and read for the membership
declaration, by `policy_check.declaration_in` — the same function that decides it
on a checkout. A tool recorded as a candidate that now declares membership is a
stale inventory, and so is a member that has stopped declaring. That is the
failure this was written for: three tools joined and the file did not move for
long enough that nobody could say from the file alone which of them had.

**What it cannot see** is whether a declaration is backed: that needs their whole
tree and their own CI is where it is decided. A remote that cannot be reached is
reported and not counted against anybody -- a network error is evidence about the
network.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY = os.path.join(ROOT, "tools", "ecosystem.json")
REPOS_FILE = os.environ.get("ANOIEU_REPOS_FILE",
                            os.path.join(ROOT, "scripts", "repos.local"))


#: What each status requires of an entry, beyond `what`.
#:
#: `associate` requires `vetted` and `why`, and nothing else requires either. A
#: footing that rests on our judgement rather than on their declaration carries
#: the date a person last made that judgement and what they made it about, or it
#: becomes a claim that only ever accumulates. `why` is what we vetted them
#: *as* -- why they are load-bearing for us -- and is not a second `what`.
REQUIRED = {
    "member": ("repo", "url"),
    "associate": ("repo", "url", "vetted", "why"),
    "candidate": ("repo", "url"),
    "foundation": ("repo", "url"),
    "child": ("parent",),
}

#: The statuses whose entry asserts something about a README somebody else
#: keeps, and which `--online` therefore reads. `foundation` is deliberately not
#: here: its entry is a fact about *our* arrangement, asserts nothing about their
#: tree, and asking them for anything is what that footing exists to refuse.
OWN_REPO = ("member", "associate", "candidate")



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


def near(a: str, b: str) -> bool:
    """Whether two ids are one edit apart, by the same rule `welcome_eo` uses."""
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "near.py"), a, b],
                         capture_output=True, text=True)
    return out.stdout.strip() == "1"


def board_entities() -> set[str]:
    """Every repository the board addresses, from its `Entities` lines."""
    path = os.path.join(ROOT, "docs", "board.md")
    if not os.path.isfile(path):
        return set()
    out = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\*\*Entities:\*\* (.+)", line.strip())
        if m:
            out |= {e.strip(" `") for e in m.group(1).split(",")}
    return out


def well_formed(inv: dict) -> list[str]:
    """The inventory read as a document about itself. No network, no checkouts."""
    bad = []
    for name, e in inv.items():
        status = e.get("status", "")
        if status not in REQUIRED:
            bad.append(f"{name}: status {status or '(none)'} is not one this file defines")
            continue
        for field in REQUIRED[status] + ("what",):
            if not e.get(field):
                bad.append(f"{name}: a {status} entry needs `{field}`")
        if status == "child":
            parent = e.get("parent", "")
            if parent not in inv:
                bad.append(f"{name}: its parent `{parent}` is not in this file")
            elif inv[parent].get("status") == "child":
                bad.append(f"{name}: its parent `{parent}` is itself a child project")
        url = e.get("url", "")
        if url and not url.startswith("https://"):
            bad.append(f"{name}: `{url}` is not an https url")
    names = sorted(inv)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if near(a, b):
                bad.append(f"`{a}` and `{b}` are one character apart, which is a "
                           "typo before it is two tools")
    for entity in sorted(board_entities() - set(inv)):
        bad.append(f"docs/board.md addresses `{entity}`, which has no row here")
    return bad


def readme_of(url: str, timeout: int = 20) -> tuple[str, str]:
    """A repository's README, from its remote. Returns (text, why-not).

    Read over https rather than by cloning, because this runs on every push and
    the question is one file. Only GitHub urls can be turned into a raw one from
    here; anything else is reported as unreadable rather than guessed at.
    """
    m = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if not m:
        return "", f"{url} is not a github url this can read a file from"
    raw = f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/HEAD/README.md"
    try:
        with urllib.request.urlopen(raw, timeout=timeout) as r:  # noqa: S310
            return r.read().decode("utf-8", "replace"), ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "", ""          # no README is an answer, not a failure to ask
        return "", f"{raw}: HTTP {e.code}"
    except (urllib.error.URLError, OSError, ValueError) as e:
        return "", f"{raw}: {str(e)[:60]}"


def still_true(inv: dict) -> tuple[list[str], list[str]]:
    """Ask each remote whether the status recorded here is still the right one.

    Returns (failures, unreachable). Unreachable is neither: it is a fact about
    the network, and counting it as a stale inventory would make this job red for
    something nobody here can fix.
    """
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import policy_check  # noqa: PLC0415

    bad, unseen = [], []
    for name, e in inv.items():
        status = e.get("status")
        if status not in OWN_REPO:
            continue
        text, why = readme_of(e.get("url", ""))
        if why:
            unseen.append(f"{name}: {why}")
            continue
        missing = policy_check.declaration_in(text)
        declares = not missing
        if status == "candidate" and declares:
            bad.append(f"{name} declares membership on its default branch and is "
                       "recorded here as a candidate: it has joined, and this file "
                       "has not been told")
        if status == "member" and not declares:
            bad.append(f"{name} is recorded here as a member and its README does "
                       f"not declare it: {missing[0]}")
        if status == "associate":
            # The affiliating note is asked about first, and a tree that carries
            # one is settled: its refusal clause is what stops `declaration_in`
            # reading it as a declaration, so the two can never both be true.
            # Only a tree with no affiliating note can have joined outright.
            gone = policy_check.affiliation_in(text)
            if not gone:
                pass
            elif declares:
                bad.append(f"{name} declares full membership and is recorded here "
                           "as an associate: it has joined, and this file has not "
                           "been told")
            else:
                bad.append(f"{name} is recorded here as an associate and its "
                           f"README does not carry the affiliating note: {gone[0]}")
    return bad, unseen


def audit(online: bool) -> int:
    """`--check`: the inventory as a document, and optionally as a claim.

    Named apart from `check` above, which asks the policy checker about one
    checkout. The two were briefly the same name, and the table stopped working
    for as long as that was true.
    """
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    inv = {k: v for k, v in inv.items() if not k.startswith("_")}

    bad = well_formed(inv)
    for b in bad:
        print(f"FAIL {b}")
    print(f"-- the inventory is well formed: {len(bad)} failure(s), "
          f"{len(inv)} entries")

    if not online:
        print("-- whether it is still true was not asked: --online does that")
        return 1 if bad else 0

    stale, unseen = still_true(inv)
    for b in stale:
        print(f"FAIL {b}")
    for u in unseen:
        print(f"     unreachable, so unasked: {u}")
    asked = sum(1 for e in inv.values() if e.get("status") in OWN_REPO) - len(unseen)
    print(f"-- who has joined is current: {len(stale)} failure(s), {asked} asked")
    print("   One section of one README is what this reads: a declaration for a "
          "member,\n   an affiliating note for an associate. Whether their tree "
          "backs a declaration is\n   decided by their own CI, running the same "
          "checker, and is not visible from here.")
    print("   Whether an associate is still worth vetting is nobody's to decide "
          "from here\n   either: the `vetted` date says when a person last did, "
          "and it does not expire\n   on its own.")
    return 1 if bad or stale else 0


def main() -> int:
    if "--check" in sys.argv:
        return audit("--online" in sys.argv)
    verbose = "--verbose" in sys.argv
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    rows, notes = [], []

    for name, e in inv.items():
        if name == "_comment":
            continue
        status = e.get("status", "?")
        if status in ("child", "foundation"):
            rows.append((name, status, "-", "-", "-", e.get("parent", "")))
            continue
        path = locate(e.get("repo", name))
        if not path:
            rows.append((name, status, "no checkout", "-", "-", ""))
            continue
        # An associate is held to none of this, so nothing here runs the checker
        # over its tree. A failure count in that row would be this table
        # grading somebody who never agreed to be graded, which is the whole of
        # what the footing refuses.
        verdict, fails = ("not held", []) if status == "associate" else check(path)
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
