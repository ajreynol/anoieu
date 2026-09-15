#!/usr/bin/env python3
"""Can `init_eo new` be run on this name today?

**Temporary, on purpose, and built so that it cannot quietly become
permanent.** It exists so that opening this repository on the web answers *what
is the next thing to do* without anybody reading a board. It is wired to the
`Ready - init_eo kanon` CI job.

**A missing stub is a failure, not a pass.** When a spawned repository proves
itself and the stub is deleted under the handoff protocol, this goes red and the
only repair is to delete the job and this file. That is the design: a check that
outlives its purpose is worse than no check, because a green tick nobody can
explain is read as an endorsement of something.

**And it stops claiming the name is free once the repository exists.** The
check used to read the stub and nothing else, so it went on saying *run
`init_eo new` in a fresh repository* about a repository that had already been
created. The stub is still correct to be there -- `PROTO-20` keeps it until CI
is green on both sides -- but *what to do next* had changed and this said
otherwise. **A green tick that names the wrong next step is the failure this
file was written to avoid**, committed by the file itself.

Green here means three things and no more:

  * the name is in the ecosystem's name register, so `init_eo new` will not
    stop on it;
  * a stub holds its place, and still says it is a stub;
  * every other job in this workflow passed, which the handoff protocol makes
    non-negotiable before anything is handed to anybody.

**It does not mean the tool should be built**, that anybody has agreed to build
it, or that it will be any good. It means the paperwork is not in the way.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STUB_SENTENCE = "this is a stub"


def existing(name: str) -> str:
    """The footing the inventory records for this name, if it is a repository.

    Empty string when the inventory has never heard of it, or records it as a
    child -- neither of which is a repository somebody could have created.
    """
    path = os.path.join(HERE, "ecosystem", "ecosystem.json")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as f:
        inv = json.load(f)
    entry = inv.get(name)
    if not isinstance(entry, dict) or not entry.get("url"):
        return ""
    status = entry.get("status", "")
    return "" if status == "child" else status


def check(name: str) -> tuple[list[str], str]:
    """What is not ready, and where the register was found.

    Empty list means ready.
    """
    bad = []

    # Found rather than hardcoded. The register lives in a child project, and a
    # child project is an island: naming its directory from here would make it
    # one no longer, for a path this file does not actually need to know.
    found = glob.glob(os.path.join(ROOT, "tools", "*", "names.md"))
    if not found:
        return (["there is no name register under tools/*/names.md"], "")
    register = found[0]
    rel = os.path.relpath(register, ROOT)
    with open(register, encoding="utf-8") as f:
        names = f.read()

    if f"**{name}**" not in names:
        bad.append(f"`{name}` is not in {rel} -- `init_eo new` is told to stop "
                   "when the register has no entry, so it would stop on this one")

    stub = os.path.join(ROOT, "tools", name, "README.md")
    if not os.path.isfile(stub):
        # Not "nothing to do". Either the stub was never made, or it was
        # deleted because the work has a repository now -- and in the second
        # case this job has done its job and should be removed with it.
        bad.append(f"there is no stub at tools/{name}/. If it was deleted "
                   "because the tool now exists, delete this job too: it is "
                   "temporary and this is how it says so")
        return bad, rel

    with open(stub, encoding="utf-8") as f:
        text = f.read().lower()
    if STUB_SENTENCE not in text:
        bad.append(f"tools/{name}/README.md no longer says it is a stub, so "
                   "either it has become something else or the sentence was "
                   "edited away")
    return bad, rel


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: ready_check.py <name>", file=sys.stderr)
        return 2
    name = argv[0]
    problems, register = check(name)
    if problems:
        print(f"NOT READY: init_eo new, for {name}")
        for p in problems:
            print(f"  - {p}")
        return 1
    footing = existing(name)
    if footing:
        # The name has a repository. Creating one is no longer the next step,
        # and the stub is not stale: PROTO-20 holds it until both sides are
        # green, which is the thing still outstanding.
        print(f"HELD: `{name}` already exists as a repository, recorded as "
              f"{footing}.")
        print(f"  the stub at tools/{name}/ stays until `PROTO-20` is "
              "satisfied -- CI green on both sides, non-negotiable")
        print(f"  the register entry is in {register}")
        print("  `init_eo new` is not the next step here and this job no "
              "longer says it is")
        return 0
    print(f"READY: run `init_eo new` in a fresh repository named {name}.")
    print(f"  the register entry is in {register}")
    print(f"  the stub holding its place is tools/{name}/")
    print("  every other job in this workflow passed, which the handoff "
          "protocol requires before anything is handed over")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
