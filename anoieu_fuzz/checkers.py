"""Running a checker, and reducing what it says to something comparable.

A checker in the Eunoia ecosystem has a very small interface: hand it one file,
read one word. `ethos` prints `correct` and exits 0, or writes a line beginning
`Error:` and aborts. `logos` prints `correct`, `incorrect` or `incomplete` and
exits 0, 1 or 2. That is the whole contract, and it is why a *third* checker is
three lines of configuration rather than a plugin.

Everything here is about turning "what the process did" into a verdict two
checkers can be compared on. The reduction is deliberately coarse:

    accept    the file was checked and the checker was happy with it
    reject    the checker refused, and said why, in the form it says everything
    abnormal  it died some other way, or never answered

Two checkers that disagree at that granularity have a real disagreement. Two
that reject with different messages have not: they are two programs writing two
sentences, which is not a defect in either. `status` keeps the finer word for
whoever reads the finding.

### Why ethos is run with `--require-proof-of-false`

Ethos, by default, does not care *what* a proof proves: it prints `correct` for
any file whose steps all check. Logos's `correct` means the assumptions are
unsatisfiable -- a refutation, or nothing. Compared as they stand, the two
disagree on almost every file, and the fuzzer reports nothing but that one
fact. `--require-proof-of-false` is what makes the two words mean the same
thing, so it is part of the default configuration rather than an option.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field

#: What a run uses when nothing was configured. `{file}` is the case and
#: `{signature}` the fixed signature a proof is written against; an argument
#: naming `{signature}` is dropped when no signature was given, because a case
#: generated without one carries its own declarations.
DEFAULT_CONFIG: dict = {
    "checkers": {
        "ethos": {
            "env": "ETHOS",
            "modes": {
                "proof": [
                    "ethos",
                    "--include={signature}",
                    "--require-proof-of-false",
                    "{file}",
                ],
                "signature": ["ethos", "{file}"],
            },
        },
        "logos": {
            "env": "LOGOS",
            "modes": {"proof": ["logos", "{file}"]},
        },
    },
    "signature": "",
    # Which checker decides the direction of a disagreement. Ethos is it
    # because it is the implementation that defines, operationally, which files
    # are Eunoia -- not because it is more likely to be right.
    "reference": "ethos",
}

ACCEPT = "accept"
REJECT = "reject"
ABNORMAL = "abnormal"

#: The words a checker may print as its verdict, and what each counts as.
VERDICTS = {
    "correct": ACCEPT,
    "incomplete": ACCEPT,
    "incorrect": REJECT,
    "invalid": REJECT,
}

_EXPLAINED = re.compile(r"^\s*(Error|error)\b")
_ABNORMAL_MARKS = re.compile(
    r"^\s*(Assertion|terminate called|Segmentation|libc\+\+abi|panic|"
    r"thread '\w+' panicked|uncaught exception)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Outcome:
    """What one checker did with one file."""

    checker: str
    status: str  # correct | incomplete | incorrect | rejected | crash | timeout | missing
    coarse: str  # accept | reject | abnormal | skipped
    detail: str = ""
    code: int = 0
    seconds: float = 0.0

    def line(self) -> str:
        head = f"{self.checker}: {self.status}"
        if self.code:
            head += f" (exit {self.code})"
        return head + (f" -- {self.detail}" if self.detail else "")


@dataclass
class Checker:
    """One binary, and how to ask it about a file."""

    name: str
    modes: dict[str, list[str]] = field(default_factory=dict)
    env: str = ""

    def argv(self, mode: str, path: str, signature: str) -> list[str] | None:
        template = self.modes.get(mode)
        if template is None:
            return None
        binary = os.environ.get(self.env, "") if self.env else ""
        out = []
        for i, arg in enumerate(template):
            if "{signature}" in arg and not signature:
                continue  # nothing to include: the case stands on its own
            arg = arg.replace("{file}", path).replace("{signature}", signature)
            out.append(binary if (i == 0 and binary) else arg)
        return out

    def resolve(self, mode: str = "proof") -> str:
        """The path this checker would run, or "" if nothing is there."""
        argv = self.argv(mode, "x", "y")
        if argv is None:
            argv = next(iter(self.modes.values()), [""])
            binary = os.environ.get(self.env, "") if self.env else ""
            argv = [binary or argv[0]]
        return shutil.which(argv[0]) or ""

    def run(self, mode: str, path: str, signature: str, timeout: float) -> Outcome:
        argv = self.argv(mode, path, signature)
        if argv is None:
            return Outcome(self.name, "skipped", "skipped")
        started = time.monotonic()
        try:
            p = subprocess.run(
                argv, capture_output=True, text=True, timeout=timeout, errors="replace"
            )
        except subprocess.TimeoutExpired:
            return Outcome(
                self.name, "timeout", ABNORMAL, f">{timeout:g}s", 0, timeout
            )
        except OSError as e:
            return Outcome(self.name, "missing", "skipped", str(e)[:80])
        return classify(self.name, p.returncode, p.stdout, p.stderr, time.monotonic() - started)


def classify(name: str, code: int, out: str, err: str, seconds: float) -> Outcome:
    """What the process did, as a verdict.

    The order matters. A checker's own verdict word, printed on stdout, is the
    most reliable thing it says, so it is read first: `logos` prints `incorrect`
    on stdout *and* an explanation beginning `Error:` on stderr, and the word is
    the one to believe.

    Then the explained failures. Ethos reports every error by aborting -- a
    `Fatal failure within ...` line, an `Error: ...` line, and `SIGABRT` -- so
    "died on a signal" cannot on its own mean "crashed". What separates a
    refusal from the rest is whether the checker explained itself the way it
    explains everything else, which for both checkers here is a line beginning
    `Error`.

    That leaves two ways to fail:

    - `crash`, which is a checker going down with nothing to say, or with
      something only a runtime says -- an assertion, `terminate called`, a
      signal and an empty stream;
    - `unexplained`, which is a checker that *did* print something and then
      failed anyway, outside its own diagnostic convention. The one such path
      this found first is real but small: declaring a literal category twice
      aborts ethos with an internal message carrying no file, no line and no
      `Error:`, so every tool that reads ethos's output misses it.

    Both are findings. They are separated because they are triaged differently:
    one is a bug in the checker, the other in what the checker says.
    """
    lines = [l for l in (out + "\n" + err).splitlines() if l.strip()]
    word = next((l.strip() for l in reversed(out.splitlines()) if l.strip()), "")
    if word in VERDICTS:
        return Outcome(name, word, VERDICTS[word], _detail(lines), code, seconds)
    if any(_ABNORMAL_MARKS.match(l) for l in lines):
        return Outcome(name, "crash", ABNORMAL, _detail(lines), code, seconds)
    if any(_EXPLAINED.match(l) for l in lines):
        return Outcome(name, "rejected", REJECT, _detail(lines), code, seconds)
    if code == 0:
        return Outcome(name, "quiet", ACCEPT, _detail(lines), code, seconds)
    if lines:
        return Outcome(name, "unexplained", ABNORMAL, _detail(lines), code, seconds)
    return Outcome(name, "crash", ABNORMAL, _detail(lines), code, seconds)


def _detail(lines: list[str]) -> str:
    """The one line worth keeping: what the checker said was wrong."""
    for line in lines:
        if _EXPLAINED.match(line) or _ABNORMAL_MARKS.match(line):
            return _portable(line)
    return _portable(lines[0]) if lines else ""


def _portable(line: str) -> str:
    """Drop what is about this machine, or this case, rather than about the bug.

    Two runs of the same defect must reduce to the same string or the corpus
    fills with one directory per case. Paths, line numbers and the generated
    names the anoieu fuzzer invents are all per-case; the sentence around them is not.
    """
    line = line.strip()
    line = re.sub(r"(/[^\s:,]+)+", "<path>", line)
    line = re.sub(r"\b\d+\.\d+\b", "N.N", line)
    line = re.sub(r"\b\d+\b", "N", line)
    line = re.sub(r"`[^`]*`", "`_`", line)
    # A checker that quotes the offending *term* back at you says something
    # different about every instance of one defect, and a bucket per instance is
    # the thing bucketing exists to prevent: logos's "assumption after the first
    # proof step: (assume @p1 @t6)" was landing in a new directory each time.
    # A parenthesised group with a space in it is a term; one without is a token
    # class, and `(EOF)` and `(SYMBOL)` are exactly the distinction that must
    # survive.
    for _ in range(8):  # innermost first, then outward: (not (= x N)) -> (...)
        collapsed = re.sub(r"\([^()]*\s[^()]*\)", "\x00", line)
        if collapsed == line:
            break
        line = collapsed
    line = line.replace("\x00", "(...)")
    return line[:160]


# -- configuration ------------------------------------------------------------


def load_config(path: str = "") -> dict:
    """The defaults, or what a file says instead.

    A file that names `checkers` *replaces* the set rather than adding to it.
    Merging reads well until the day a run quietly also asks the two default
    binaries about every case and reports a disagreement between one of them
    and a checker somebody was testing on its own. `anoieu-fuzz checkers` prints
    the default entries, so re-stating one is a copy rather than an archaeology
    exercise.
    """
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if not path:
        return cfg
    with open(path) as f:
        given = json.load(f)
    cfg.update(given)
    return cfg


def from_config(cfg: dict, only: list[str] | None = None) -> list[Checker]:
    out = []
    for name, entry in cfg.get("checkers", {}).items():
        if only and name not in only:
            continue
        modes = entry.get("modes") or {}
        if isinstance(modes, list):  # one command, every mode
            modes = {"proof": modes, "signature": modes}
        out.append(Checker(name=name, modes=dict(modes), env=entry.get("env", "")))
    return out
