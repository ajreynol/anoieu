#!/usr/bin/env python3
"""Resolve this repository's links into other ecosystem trees, against checkouts.

**A link into another repository is the one link nothing resolves, from either
end.** `checker.py` resolves every committed path and every anchor in the tree it
is given and stops at `http`, deliberately: an unpinned cross-repository check
inside a member's build would turn that build red for a rename in a tree nobody
near them touched. That is why it sits on
[the contract page](README.md#what-a-new-contract-would-carry) as a contract 2
candidate rather than as a check.

**This is the half that is ours to do anyway.** It needs local checkouts, so it is
a command somebody runs and **never a CI gate** — the shared policy asks that a
check fail for a reason in the tree, not for what somebody else pushed this
morning, and this one fails for exactly that. It reports and exits 0 unless asked
otherwise.

**What it is worth, measured rather than argued.** Its first run, 2026-09-21,
found four dead links out of forty-four: a board heading kanon no longer keeps,
and three paths in epikrisis that moved when that repository put its children's
documents under `docs/`. Every one had been invisible to two green builds.

**Two rules about what it will not resolve**, both of which would make it lie:

- **A link naming a ref other than `main` is a link to a version**, not to a
  path, and resolving it against whatever is checked out would report a file as
  missing because history moved on. Those are counted and skipped.
- **A repository with no checkout here is reported as unknown**, never as passing.
  Absence is not a pass; the run says how many it could not ask about.

    python3 -m policy_check.outbound              # report, exit 0
    python3 -m policy_check.outbound --strict     # exit 1 if any link is dead
    python3 -m policy_check.outbound --trees DIR  # where the checkouts are
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

#: Where a sibling checkout of another ecosystem repository is expected to be.
#: The default is this repository's own parent directory, which is how the trees
#: are laid out on the machines this is run on; `--trees` overrides it.
DEFAULT_TREES = os.path.dirname(ROOT)

#: A Markdown link into a GitHub repository, with the owner, the ref, the path
#: and any fragment. Both owners the ecosystem uses are accepted; a third would
#: be a link out of the ecosystem and is not this command's business.
LINK = re.compile(
    r"\]\(https://github\.com/(?:ajreynol|cvc5)/([A-Za-z0-9_.-]+)"
    r"/blob/([^/)]+)/([^)#\s]+)(#[^)\s]*)?\)")


def links_out(rel: str, prose) -> list[tuple[str, str, str, str]]:
    """Every `(repo, ref, path, fragment)` a document links to, prose only.

    Fenced code is not prose and a path inside it is not a link -- the same
    argument `check_links` makes, and for the same reason: a quoted URL in an
    example is a string somebody is being shown how to type.
    """
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        text = prose(fh.read())
    return [(m.group(1), m.group(2), m.group(3), m.group(4) or "")
            for m in LINK.finditer(text)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="resolve links into other ecosystem trees against checkouts")
    ap.add_argument("--trees", default=DEFAULT_TREES,
                    help="directory holding sibling checkouts")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when a link does not resolve")
    args = ap.parse_args(argv)

    from policy_check import checker

    files = subprocess.run(["git", "-C", ROOT, "ls-files", "*.md"],
                           capture_output=True, text=True).stdout.split()
    dead: list[str] = []
    unknown: dict[str, int] = {}
    pinned = resolved = 0
    for rel in sorted(files):
        for repo, ref, path, frag in links_out(rel, checker.prose):
            if ref != "main":
                pinned += 1
                continue
            tree = os.path.join(args.trees, repo)
            if not os.path.isdir(os.path.join(tree, ".git")):
                unknown[repo] = unknown.get(repo, 0) + 1
                continue
            resolved += 1
            full = os.path.join(tree, path)
            if not os.path.exists(full):
                dead.append(f"{rel}: {repo}/{path} — no such path")
                continue
            if frag:
                with open(full, encoding="utf-8") as fh:
                    anchors = checker.anchors_in(checker.prose(fh.read()))
                if frag[1:] not in anchors:
                    dead.append(f"{rel}: {repo}/{path}{frag} — "
                                "the path resolves and the section does not")

    for line in dead:
        print(f"dead {line}")
    print("-- links into another ecosystem tree, resolved against checkouts")
    print(f"   {resolved} resolved, {len(dead)} dead")
    print(f"   {pinned} skipped: a link naming a ref is a link to a version")
    if unknown:
        total = sum(unknown.values())
        print(f"   {total} not asked about: no checkout of "
              + ", ".join(f"{r} ({n})" for r, n in sorted(unknown.items())))
        print("   absence is not a pass — those links are unknown, not resolving")
    if not args.strict:
        print("   this is never a CI gate: it fails for a rename in a tree "
              "nobody here touched")
    return 1 if (dead and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
