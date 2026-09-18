"""The standard targets, and where each project is on this machine.

Two files, and the split between them is the point:

* `anoieu_analyzer/reporting/config/targets.json` is **committed**. Which files are worth
  analysing -- `Cpc.eo`, ethos's test signatures -- is a claim about the
  ecosystem, and one anybody can check.
* `anoieu_analyzer/reporting/config/repos.local` is **gitignored**. A path under somebody's home
  directory is not a claim anybody else can check, and a report about *the
  version on my laptop* is a report about nothing -- which is why `deps/` exists
  and is what a run falls back to.

Both producers read this: `scripts/anoieu_analyzer` to run the checks, and
`prompts/anoieu_analyzer_agent` to tell an agent which files to read. A second
producer pointed at different files is not a second producer, it is a different
question.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

from . import ROOT, CONFIG_DIR
CONFIG = os.path.join(CONFIG_DIR, "targets.json")
LOCAL = os.path.join(CONFIG_DIR, "repos.local")


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
    from .gen_corpus_table import DEFAULT_ROOTS  # noqa: PLC0415

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
            return {**DEFAULT_ROOTS, **found}, "anoieu_analyzer/reporting/config/repos.local"
    return dict(DEFAULT_ROOTS), "deps/"


def commit_of(path: str) -> str:
    """What that checkout is at. Empty when it is not a repository."""
    if not path or not os.path.isdir(path):
        return ""
    out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def describe(spec: list[dict]) -> list[str]:
    """Every signature a run would read, resolved on this machine.

    Concrete on purpose: a target names `tests`, and what is actually analysed is
    the `.eo` files under it, minus the ones nobody here is the author of. A run
    that reads nothing and a run that finds nothing print the same *0 bug(s)*, so
    this is what tells the two apart before either happens.
    """
    from .gen_corpus_table import not_audited, signatures  # noqa: PLC0415

    where, said = roots()
    out = [f"paths from {said}"]
    total = 0
    for t in spec:
        root = where.get(t["project"], "")
        commit = commit_of(root)
        out.append(f"{t['id']}  ({t['project']} at {commit or 'NOT A REPOSITORY'})")
        if not root or not os.path.isdir(root):
            out.append(f"  {root or '?'}   NO CHECKOUT -- this target is skipped")
            continue
        skip = not_audited(t["project"], root)
        for p in t["paths"]:
            full = os.path.join(root, p)
            if not os.path.exists(full):
                out.append(f"  {full}   MISSING")
                continue
            files = sorted({f for group in signatures([full], skip) for f in group})
            kind = "directory" if os.path.isdir(full) else "file"
            out.append(f"  {full}   {kind}, {len(files)} signature(s)")
            total += len(files)
        for excluded in sorted(skip):
            if any(excluded.startswith(os.path.abspath(os.path.join(root, p)))
                   for p in t["paths"]):
                out.append(f"  {excluded}   NOT AUDITED -- somebody else is its author")
        # The triple's companions are read to check the signature against, not
        # analysed themselves, and they live in other projects. A target that
        # silently lost one would still run, and report less.
        for role, (project, rel) in sorted((t.get("triple") or {}).items()):
            full = os.path.join(where.get(project, "?"), rel)
            out.append(f"  {full}   {role}, from {project}"
                       + ("" if os.path.exists(full) else "   MISSING"))
    out.append(f"{total} signature(s) in {len(spec)} target(s)")
    return out


if __name__ == "__main__":
    print("\n".join(describe(select(load(), sys.argv[1:]))))
