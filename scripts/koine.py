"""Where koine is on this machine, and which commit of it we are using.

[koine](https://github.com/ajreynol/koine) is one script, `koine_append_db`: it
takes a run's dump of bugs and adds the new ones to a database of every bug the
tool has ever found. It never edits or removes what is already there. There is
no package and no install step -- a customer pins a commit and clones it -- so
this is the whole of the integration on our side.

Three places are tried, in order, and the first that has the modules wins:

1. `$KOINE`, if it is set. What CI uses, and what a bisect uses.
2. `../koine` beside this repository, which is where it sits on a machine that
   works on both.
3. `deps/koine`, a clone this script makes at the commit in `koine.lock`.

`koine.lock` is the pin and it is a choice rather than a fact: moving it changes
what our record is checked by. The ecosystem's rule is that a pin only moves to
a commit where the other project's CI is green.
"""

from __future__ import annotations

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOCK = os.path.join(HERE, "koine.lock")
URL = "https://github.com/ajreynol/koine.git"
CLONE = os.path.join(ROOT, "deps", "koine")

#: What we use. A directory without this is not koine, whatever it is called --
#: worth checking, because `../koine` is a guess about a layout.
MODULES = ("koine_append_db",)


def pinned() -> str:
    """The commit `koine.lock` names."""
    for line in open(LOCK).read().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            return line
    raise SystemExit(f"{LOCK}: names no commit")


def _is_koine(path: str) -> bool:
    return bool(path) and all(
        os.path.isfile(os.path.join(path, m)) for m in MODULES
    )


def _clone() -> str:
    commit = pinned()
    if not os.path.isdir(os.path.join(CLONE, ".git")):
        os.makedirs(os.path.dirname(CLONE), exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", URL, CLONE], check=True)
    subprocess.run(["git", "-C", CLONE, "fetch", "--quiet", "origin", commit],
                   check=False)
    subprocess.run(["git", "-C", CLONE, "checkout", "--quiet", commit], check=True)
    return CLONE


def find(clone: bool = True) -> str:
    """The directory to put on `sys.path`."""
    for candidate in (os.environ.get("KOINE", ""),
                      os.path.join(os.path.dirname(ROOT), "koine"),
                      CLONE):
        if _is_koine(candidate):
            return candidate
    if not clone:
        raise SystemExit(
            "koine is not on this machine. Set $KOINE, put a checkout at "
            f"{os.path.join(os.path.dirname(ROOT), 'koine')}, or let "
            "scripts/koine.py clone it into deps/koine"
        )
    return _clone()


def append_db(clone: bool = True) -> str:
    """The path to `koine_append_db`, cloning koine if it is not here."""
    return os.path.join(find(clone), "koine_append_db")


def version(path: str) -> str:
    """The commit that checkout is at, for a run record. Empty if it is not git."""
    out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""
