"""Where koine is on this machine, and which commit of it we are using.

[koine](https://github.com/ajreynol/koine) keeps bug databases: its
`bug_db/koine_append_db` takes a run's dump of bugs and adds the new ones to a
database of every bug the tool has ever found. It never edits or removes what is
already there. There is no package and no install step -- a customer pins a
commit and clones it -- so this is the whole of the integration on our side.

Three places are tried, in order, and the first that has the modules wins:

1. `$KOINE`, if it is set. What CI uses, and what a bisect uses.
2. `../koine` beside this repository, which is where it sits on a machine that
   works on both.
3. `deps/koine`, a clone this script makes at the commit in `koine.lock`.

`koine.lock` is the pin and it is a choice rather than a fact: moving it changes
what our record is checked by. The ecosystem's rule is that a pin only moves to
a commit where the other project's CI is green.

**The script moved on 2026-09-17**, from the root of a checkout to `bug_db/`,
when koine gave each of its two purposes a directory of its own. The script
itself did not change. A checkout from before the move is still koine and its
script still works, but it is not the commit `koine.lock` names -- so `find`
says so rather than passing over it for a clone without a word. Being passed
over in silence is how a machine that develops both repositories stops testing
the checkout it is editing.
"""

from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOCK = os.path.join(HERE, "koine.lock")
URL = "https://github.com/ajreynol/koine.git"
CLONE = os.path.join(ROOT, "deps", "koine")

#: What we use, as paths inside a checkout. A directory without this is not
#: koine, whatever it is called -- worth checking, because `../koine` is a guess
#: about a layout.
MODULES = (os.path.join("bug_db", "koine_append_db"),)

#: Where that same script lived before the move. Read only to tell *koine, but
#: older than our pin* apart from *not koine*: the root name still exists after
#: the move, as a tombstone that exits rather than appending, so a checkout is
#: from before the move only when it has one of these and none of MODULES.
BEFORE_MOVE = ("koine_append_db", os.path.join("scripts", "koine_append_db"))


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


def _is_before_move(path: str) -> bool:
    return bool(path) and not _is_koine(path) and any(
        os.path.isfile(os.path.join(path, m)) for m in BEFORE_MOVE
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
    """The checkout of koine to use."""
    candidates = (os.environ.get("KOINE", ""),
                  os.path.join(os.path.dirname(ROOT), "koine"),
                  CLONE)
    for candidate in candidates:
        if _is_koine(candidate):
            return candidate
    for candidate in candidates:
        if _is_before_move(candidate):
            print(f"-- {candidate} is koine from before koine_append_db moved "
                  f"to {MODULES[0]} on 2026-09-17, so it is being passed over. "
                  "Pull that checkout, or point $KOINE at one at the commit in "
                  "scripts/koine.lock.", file=sys.stderr)
    if not clone:
        raise SystemExit(
            "koine is not on this machine. Set $KOINE, put a checkout at "
            f"{os.path.join(os.path.dirname(ROOT), 'koine')}, or let "
            "scripts/koine.py clone it into deps/koine"
        )
    return _clone()


def script_in(root: str) -> str:
    """The path to `koine_append_db` in that checkout."""
    return os.path.join(root, MODULES[0])


def append_db(clone: bool = True) -> str:
    """The path to `koine_append_db`, cloning koine if it is not here."""
    return script_in(find(clone))


def version(path: str) -> str:
    """The commit that checkout is at, for a run record. Empty if it is not git."""
    out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""
