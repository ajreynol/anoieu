"""The sources a report is generated from, cloned and kept current by us.

A report about "the version on my laptop" is a report about nothing, so nothing
here reads a checkout somebody else owns. Each project named in `deps.json` is
cloned into `deps/` beside this repository and updated from its remote before a
run measures anything.

The clones are **shallow and sparse**: one commit, no blobs beyond what is
needed, and only the paths a project's entry names. The analysis reads text —
signatures, semantics, the manual — and builds nothing, so there is no reason to
fetch a history or a source tree we never open. (The one thing that *does* need
a build is the differential oracle in `tests/run.py --oracle`, which runs the
real ethos binary. That is a separate job and not part of a report.)

`deps/` is not checked in. It is a cache: delete it and the next run rebuilds
it.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, "deps.json")
DEPS = os.path.join(ROOT, "deps")
LOCK = os.path.join(HERE, "deps.lock")


@dataclass
class Dep:
    name: str
    url: str
    ref: str
    paths: list[str]
    reads: str
    path: str = ""
    sha: str = ""
    full: str = ""
    date: str = ""
    status: str = ""


def manifest(path: str = MANIFEST) -> list[Dep]:
    with open(path) as f:
        data = json.load(f)
    return [
        Dep(
            name=name,
            url=entry["url"],
            ref=entry["ref"],
            paths=list(entry.get("paths", [])),
            reads=entry.get("reads", ""),
        )
        for name, entry in data.items()
        if not name.startswith("_")
    ]


def _git(*args: str, cwd: str | None = None) -> tuple[int, str]:
    out = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=900
    )
    return out.returncode, (out.stdout + out.stderr).strip()


def sync(dep: Dep, deps_dir: str = DEPS, offline: bool = False, pin: str = "") -> Dep:
    """Bring one project's clone to a commit: the tip of its ref, or `pin`.

    The clone is ours, so this is allowed to be blunt about it — a hard reset
    onto what was fetched is the whole update.

    `pin` is what makes a report reproducible. Given a commit, this fetches
    exactly that commit rather than whatever the branch has since become, so a
    run over a recorded version measures the same bytes it measured before.
    """
    dep.path = os.path.join(deps_dir, dep.name)
    exists = os.path.isdir(os.path.join(dep.path, ".git"))

    if pin and not offline:
        if not exists:
            os.makedirs(deps_dir, exist_ok=True)
            code, msg = _git("clone", "--no-checkout", "--filter=blob:none",
                             "--sparse", "--depth", "1", "--branch", dep.ref,
                             dep.url, dep.path)
            if code:
                dep.status = f"could not clone: {msg.splitlines()[-1][:70]}"
                return dep
        _git("sparse-checkout", "set", *dep.paths, cwd=dep.path)
        code, msg = _git("fetch", "--depth", "1", "origin", pin, cwd=dep.path)
        if code:
            # A commit can fall out of reach — force-pushed away, or a server
            # that will not serve one by name. Say so rather than silently
            # measuring something else.
            dep.status = f"pinned {pin[:12]} unreachable"
        else:
            _git("checkout", "--force", "FETCH_HEAD", cwd=dep.path)
            dep.status = f"pinned to {pin[:12]}"
    elif offline:
        dep.status = "clone reused (offline)" if exists else "missing, and offline"
    elif not exists:
        os.makedirs(deps_dir, exist_ok=True)
        code, msg = _git(
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            "--branch",
            dep.ref,
            dep.url,
            dep.path,
        )
        if code:
            dep.status = f"could not clone: {msg.splitlines()[-1][:80]}"
            return dep
        code, msg = _git("sparse-checkout", "set", *dep.paths, cwd=dep.path)
        dep.status = "cloned" if not code else f"cloned, but sparse-checkout failed: {msg[:60]}"
    else:
        code, _ = _git("sparse-checkout", "set", *dep.paths, cwd=dep.path)
        code, msg = _git("fetch", "--depth", "1", "origin", dep.ref, cwd=dep.path)
        if code:
            dep.status = "clone reused (could not fetch)"
        else:
            before = _git("rev-parse", "HEAD", cwd=dep.path)[1]
            _git("reset", "--hard", "FETCH_HEAD", cwd=dep.path)
            after = _git("rev-parse", "HEAD", cwd=dep.path)[1]
            dep.status = "current" if before == after else "updated"

    if os.path.isdir(dep.path):
        dep.full = _git("rev-parse", "HEAD", cwd=dep.path)[1]
        dep.sha = dep.full[:12]
        dep.date = _git("log", "-1", "--format=%cs", cwd=dep.path)[1]
    return dep


def sync_all(
    deps_dir: str = DEPS, offline: bool = False, pins: dict | None = None
) -> list[Dep]:
    pins = pins or {}
    return [sync(d, deps_dir, offline, pins.get(d.name, "")) for d in manifest()]


def read_lock(path: str = LOCK) -> dict[str, str]:
    """The exact commits a report was measured against, by project.

    `docs/reports/corpus.md` shows these to a reader in twelve characters, which is
    plenty to recognise a commit and not enough to fetch one. This file is the
    same fact written for a machine, and is what `--pinned` restores.
    """
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        return {k: v["commit"] for k, v in json.load(f).items() if not k.startswith("_")}


def render_lock(deps: list[Dep]) -> str:
    body = {
        "_comment": "Written by tools/run.py. The commits docs/reports/corpus.md reports "
        "on, in full, so `tools/run.py --pinned` can fetch exactly them. Edited by "
        "a run, not by hand.",
    }
    for d in deps:
        if d.full:
            body[d.name] = {"ref": d.ref, "commit": d.full, "date": d.date}
    return json.dumps(body, indent=2) + "\n"


def roots(deps_dir: str = DEPS) -> dict[str, str]:
    """Where each project's files are, for whatever reads them."""
    return {d.name: os.path.join(deps_dir, d.name) for d in manifest()}
