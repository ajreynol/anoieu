#!/usr/bin/env python3
"""Refuse a bump to a commit anoieu's own CI did not pass.

A member takes on whatever we have changed by moving a pin -- `ANOIEU_REV` in
their `anoieu / policy` workflow -- to a commit of this repository. **That bump
is valid only if this repository's CI is green at exactly that commit**, and this
is the program that decides it. Published so that four members do not each write
it; nothing obliges anybody to use this one, and the requirement is the refusal
rather than the program.

*Internally we plan in stretches called epochs and this is what makes one
deployable -- `docs/epoch-policy.md`. That vocabulary is ours and a member does
not need it: the rule below is about a bump, and it holds whether or not anybody
upstream plans in anything.*

Three properties, and the first is the one everything else follows from.

**It asks about a commit, never about the tip.** Green-at-a-commit is a fact that
never changes once the run has finished; green-at-HEAD is a fact that changes
without anybody committing. Asking about the tip would make the answer depend on
what we pushed this morning, which is the failure the whole pinning discipline
exists to prevent.

**It fails closed.** Not green, not finished, or not reachable -- all refuse.
That is the opposite of how `tools/ecosystem.py --check --online` treats an
unreachable remote, and the difference is that adopting an epoch is *optional and
deferrable*: refusing costs a member nothing but a later attempt, where a
fail-closed check inside a build would turn somebody's tree red for a network
they do not own.

**It must never run in CI.** Not ours, not theirs. It reads a remote over the
network, so a build that called it could go red without anybody committing --
and a build that can change colour on its own cannot be evidence that a commit
was good. It is a command a person or a bump script runs at the moment of
adoption, and nothing else.

    python3 tools/bump_check.py --rev 59e8e07     # may this epoch be adopted?
    python3 tools/bump_check.py --root PATH       # read the pin from a member's workflow
    python3 tools/bump_check.py --rev X --dry-run # print what it would ask, ask nothing

Exit codes, which are the interface a bump script consumes:

    0   green at that commit -- adoption may proceed
    1   not green -- refuse
    2   could not be verified -- refuse, and say why
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = "ajreynol/anoieu"
API = "https://api.github.com/repos/{repo}/commits/{rev}/check-runs"

#: Conclusions that do not stand in the way of adoption. `neutral` and `skipped`
#: are how a job that correctly decided it had nothing to do reports itself, and
#: refusing on those would make adding a conditional job a breaking change for
#: every member.
PASSING = {"success", "neutral", "skipped"}


def verdict(runs: list[dict]) -> tuple[int, str]:
    """The decision, as (exit code, reason). Pure, so it is tested offline.

    A commit with no check runs at all is `2` and never `0`: *no runs* and *all
    runs passed* are indistinguishable from an empty list, and guessing in the
    permissive direction here would let an epoch through on a commit CI never
    looked at.
    """
    if not runs:
        return 2, "no check runs recorded at that commit, so nothing says it passed"
    pending = [r for r in runs if r.get("status") != "completed"]
    if pending:
        names = ", ".join(sorted(r.get("name", "?") for r in pending)[:4])
        return 2, f"still running, so the answer is not final yet: {names}"
    failed = [r for r in runs if r.get("conclusion") not in PASSING]
    if failed:
        names = ", ".join(sorted(f"{r.get('name', '?')} ({r.get('conclusion')})"
                                 for r in failed)[:4])
        return 1, f"not green: {names}"
    return 0, f"green, across {len(runs)} check run(s)"


def pinned_rev(root: str) -> tuple[str, str]:
    """The `ANOIEU_REV` a member's workflow pins, as (rev, why-not).

    Read as text rather than as YAML, deliberately: this runs in somebody else's
    checkout with whatever Python they have, and the policy's own promise is that
    nothing needs installing.
    """
    d = os.path.join(root, ".github", "workflows")
    if not os.path.isdir(d):
        return "", f"{root} has no .github/workflows to read a pin from"
    for name in sorted(os.listdir(d)):
        if not name.endswith((".yml", ".yaml")):
            continue
        text = open(os.path.join(d, name), encoding="utf-8", errors="replace").read()
        m = re.search(r"^\s*ANOIEU_REV\s*:\s*[\"']?([0-9a-fA-F]{7,40})[\"']?\s*$",
                      text, re.M)
        if m:
            return m.group(1), ""
    return "", ("no ANOIEU_REV found in .github/workflows -- this member tracks the "
                "tip, which the policy allows and this check cannot speak about")


def epoch_marker(root: str) -> str:
    """The `EUNOIA_EPOCH` a repository records, or "" if it records none.

    The marker says which epoch of this ecosystem's *advice* a tree was built
    against; `pinned_rev` above says which commit of the *checker* it is held to.
    Two different facts, allowed to disagree, read from the same file because
    that is where somebody already looks.

    **Absent is the ordinary case and never a failure.** The convention is
    encouraged and not required, so a tool reading this reports what it finds and
    grades nobody.
    """
    d = os.path.join(root, ".github", "workflows")
    if not os.path.isdir(d):
        return ""
    for name in sorted(os.listdir(d)):
        if not name.endswith((".yml", ".yaml")):
            continue
        text = open(os.path.join(d, name), encoding="utf-8", errors="replace").read()
        m = re.search(r"^\s*EUNOIA_EPOCH\s*:\s*[\"']?(E\d+)[\"']?\s*$", text, re.M)
        if m:
            return m.group(1)
    return ""


def current_epoch(root: str = "") -> str:
    """The newest epoch in `docs/epochs.md`, or "" if there is none.

    The log is newest-first, so the first `## E<n>` heading is the current one.
    Read from the prose rather than from a second file on purpose: a machine-
    readable copy would be one more thing to keep in step with the log, and the
    log is already the ground truth for what an epoch is.
    """
    path = os.path.join(root or os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "docs", "epochs.md")
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(r"^##\s+(E\d+)\b", fh.read(), re.M)
    except OSError:
        return ""
    return m.group(1) if m else ""


def ask(rev: str, timeout: int = 20) -> tuple[list[dict], str]:
    url = API.format(repo=REPO, rev=rev)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "anoieu-epoch-check",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
            return json.load(r).get("check_runs", []), ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return [], f"{REPO} has no commit {rev}, or it is not public"
        if e.code in (403, 429):
            return [], (f"the API refused ({e.code}) -- unauthenticated requests are "
                        "rate limited, so try again later rather than adopting")
        return [], f"HTTP {e.code} from {url}"
    except (urllib.error.URLError, OSError, ValueError) as e:
        return [], f"{url}: {str(e)[:80]}"


def main() -> int:
    argv = sys.argv[1:]

    def opt(name: str) -> str:
        return argv[argv.index(name) + 1] if name in argv else ""

    rev, root = opt("--rev"), opt("--root")
    if root and not rev:
        rev, why = pinned_rev(root)
        if why:
            print(f"-- cannot check: {why}")
            return 2
        print(f"-- {root} pins {REPO} at {rev}")
    if not rev:
        print(__doc__.strip().split("\n\n")[-2])
        return 2

    if "--dry-run" in argv:
        print(API.format(repo=REPO, rev=rev))
        return 0

    runs, why = ask(rev)
    if why:
        print(f"-- REFUSE: {why}")
        print("   Unverified is refused rather than allowed: adopting an epoch is "
              "optional and\n   deferring costs nothing, so the cautious answer is "
              "the cheap one.")
        return 2

    code, reason = verdict(runs)
    print(f"-- {'ADOPT' if code == 0 else 'REFUSE'}: {REPO} at {rev} is {reason}")
    if code == 0:
        print("   This says those checks passed at that commit, and nothing about "
              "whether the\n   epoch is any good -- see docs/reports/"
              "reporting-policy.md on silence.")
    return code


if __name__ == "__main__":
    sys.exit(main())
