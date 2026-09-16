"""The standard targets, and where each project is on this machine.

Two files, and the split between them is the point:

* [`targets.json`](targets.json) is **committed**. Which files are worth
  analysing -- `Cpc.eo`, ethos's test signatures -- is a claim about the
  ecosystem, and one anybody can check.
* [`repos.local`](repos.local) is **gitignored**. A path under somebody's home
  directory is not a claim anybody else can check, and a report about *the
  version on my laptop* is a report about nothing -- which is why `deps/` exists
  and is what a run falls back to.

Both producers read this: `scripts/run_static_analysis` to run the checks, and
`prompts/prompt_static_analysis` to tell an agent which files to read. A second
producer pointed at different files is not a second producer, it is a different
question.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONFIG = os.path.join(HERE, "targets.json")
LOCAL = os.path.join(HERE, "repos.local")

sys.path.insert(0, HERE)


def load(path: str = CONFIG) -> list[dict]:
    """Every standard target, in the order the file lists them."""
    return json.load(open(path))["targets"]


def select(spec: list[dict], want: list[str]) -> list[dict]:
    """The named targets, or all of them. Raises on a name that is not one."""
    if not want:
        return spec
    unknown = set(want) - {t["id"] for t in spec}
    if unknown:
        raise KeyError(", ".join(sorted(unknown)))
    return [t for t in spec if t["id"] in want]


def as_tuples(spec: list[dict]) -> list[tuple]:
    """A target in the shape `gen_open_findings.collect` takes.

    That shape is the old workflow's `TARGETS` literal, and `tests/run.py`
    fails if the two descriptions disagree -- the new path reads the JSON and
    the old one reads the literal, and two descriptions of one thing that
    nothing compares is the drift this ecosystem keeps finding.
    """
    out = []
    for t in spec:
        triple = None
        if t.get("triple"):
            triple = {k: tuple(v) for k, v in t["triple"].items()}
        out.append((t["label"], t["project"], list(t["paths"]), triple))
    return out


def roots() -> tuple[dict, str]:
    """Where each project is, and what said so."""
    from gen_corpus_table import DEFAULT_ROOTS  # noqa: PLC0415

    if os.path.isfile(LOCAL):
        local = {}
        for line in open(LOCAL).read().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            name, _, where = line.partition(" ")
            if where.strip():
                local[name] = os.path.expanduser(where.strip())
        found = {n: p for n, p in local.items() if os.path.isdir(p)}
        if found:
            return {**DEFAULT_ROOTS, **found}, "scripts/repos.local"
    return dict(DEFAULT_ROOTS), "deps/"


def commit_of(path: str) -> str:
    """What that checkout is at. Empty when it is not a repository."""
    if not path or not os.path.isdir(path):
        return ""
    out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def describe(spec: list[dict]) -> list[str]:
    """One line per path a run would read, for a person or for a prompt."""
    where, _ = roots()
    out = []
    for t in spec:
        root = where.get(t["project"], "")
        commit = commit_of(root)
        for p in t["paths"]:
            out.append(f"  {t['id']:22} {t['project']:12} {os.path.join(root, p)}"
                       + (f"   (at {commit})" if commit else "   (MISSING)"))
    return out


if __name__ == "__main__":
    print("\n".join(describe(select(load(), sys.argv[1:]))))
