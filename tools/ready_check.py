#!/usr/bin/env python3
"""Can `init_eo new` be run on this name today?

**Temporary, on purpose, and built so that it cannot quietly become
permanent.** It exists so that opening this repository on the web answers *what
is the next thing to do* without anybody reading a board. It is wired to two CI
jobs whose names are the whole point: `Ready - init_eo kanon` and
`Ready - init_eo tekton`.

**A missing stub is a failure, not a pass.** When a spawned repository proves
itself and the stub is deleted under the handoff protocol, this goes red and the
only repair is to delete the job and this file. That is the design: a check that
outlives its purpose is worse than no check, because a green tick nobody can
explain is read as an endorsement of something.

Green here means three things and no more:

  * the name is in the register, so `init_eo new` will not stop on it;
  * a stub holds its place, and still says it is a stub;
  * every other job in this workflow passed, which the handoff protocol makes
    non-negotiable before anything is handed to anybody.

**It does not mean the tool should be built**, that anybody has agreed to build
it, or that it will be any good. It means the paperwork is not in the way.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUB_SENTENCE = "this is a stub"


def check(name: str) -> list[str]:
    """What is not ready, as a list of sentences. Empty means ready."""
    bad = []

    register = os.path.join(ROOT, "tools", "ynoia", "names.md")
    try:
        with open(register, encoding="utf-8") as f:
            names = f.read()
    except OSError:
        return [f"the name register is missing at {register}"]

    if f"**{name}**" not in names:
        bad.append(f"`{name}` is not in tools/ynoia/names.md -- `init_eo new` is "
                   "told to stop when the register has no entry, so it would "
                   "stop on this one")

    stub = os.path.join(ROOT, "tools", name, "README.md")
    if not os.path.isfile(stub):
        # Not "nothing to do". Either the stub was never made, or it was
        # deleted because the work has a repository now -- and in the second
        # case this job has done its job and should be removed with it.
        bad.append(f"there is no stub at tools/{name}/. If it was deleted "
                   "because the tool now exists, delete this job too: it is "
                   "temporary and this is how it says so")
        return bad

    with open(stub, encoding="utf-8") as f:
        text = f.read().lower()
    if STUB_SENTENCE not in text:
        bad.append(f"tools/{name}/README.md no longer says it is a stub, so "
                   "either it has become something else or the sentence was "
                   "edited away")
    return bad


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: ready_check.py <name>", file=sys.stderr)
        return 2
    name = argv[0]
    problems = check(name)
    if problems:
        print(f"NOT READY: init_eo new, for {name}")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"READY: run `init_eo new` in a fresh repository named {name}.")
    print(f"  the register entry is in tools/ynoia/names.md")
    print(f"  the stub holding its place is tools/{name}/")
    print("  every other job in this workflow passed, which the handoff "
          "protocol requires before anything is handed over")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
