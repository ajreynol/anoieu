"""What counts as a finding, what makes two findings the same one, and how a
case is cut down to the part that matters.

The oracle is three sentences long.

- **A disagreement.** Two checkers were given the same file and one accepted it
  while the other refused. One of them is wrong, and which one is a question for
  a person -- but the two directions are not equally serious, and the oracle
  says which is which rather than leaving it to whoever reads the row.
  **Accepting what the reference refuses** is the serious one: a checker taking
  something outside the reference's definition of the language, which for a
  verified checker means its theorem is about a term its parser invented.
  Refusing what the reference accepts costs its users a proof and guarantees
  nothing false. Error and warning respectively, `FUZ0001` and `FUZ0005`.
- **A crash.** A checker went down with nothing to say: a signal and an empty
  stream, an assertion, an uncaught exception. Ethos reports every ordinary
  error by aborting, so "died on a signal" is not on its own a finding --
  `checkers.classify` says what is.
- **An unexplained failure.** A checker printed something and then failed
  anyway, outside the diagnostic convention it uses everywhere else. A defect
  in what the checker says rather than in what it does, which is why it is a
  kind of its own rather than a crash.
- **A timeout.** A checker never answered. Suspect rather than certain: the
  generator can write a genuinely expensive file, and the finding says so.

Nothing here knows what the file means, and none of these three needs it to.

Two things make this usable rather than merely correct. **Buckets**: a
thousand cases hitting one defect must collapse to one directory, or the corpus
is a log rather than a set of bugs. **Shrinking**: what is saved is the two
commands that provoke it, not the forty that were generated around them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Callable

from .checkers import ABNORMAL, Outcome
from .codes import KIND_TO_CODE
from .gen import Case


@dataclass
class Finding:
    kind: str  # disagreement | crash | timeout
    bucket: str
    summary: str
    case: Case
    outcomes: list[Outcome] = field(default_factory=list)

    @property
    def code(self) -> str:
        return KIND_TO_CODE[self.kind]

    def as_json(self) -> dict:
        return {
            "kind": self.kind,
            "code": self.code,
            "bucket": self.bucket,
            "summary": self.summary,
            "mode": self.case.mode,
            "seed": self.case.seed,
            "source": self.case.source,
            "commands": len(self.case.commands),
            "outcomes": [
                {
                    "checker": o.checker,
                    "status": o.status,
                    "coarse": o.coarse,
                    "detail": o.detail,
                    "exit": o.code,
                    "seconds": round(o.seconds, 3),
                }
                for o in self.outcomes
            ],
        }


def judge(case: Case, outcomes: list[Outcome], reference: str = "") -> Finding | None:
    """The oracle. `None` means the run was ordinary.

    `reference` names the checker that decides which direction a disagreement
    runs in -- ethos, by default, because it is what defines operationally
    which files are Eunoia. A disagreement in which the reference took part and
    *refused* is the serious one. When the reference did not run, the
    disagreement is reported as the serious one anyway: assuming the mild
    reading of something nobody attributed is the wrong way to be wrong.
    """
    ran = [o for o in outcomes if o.coarse != "skipped"]
    if not ran:
        return None

    dead = [o for o in ran if o.coarse == ABNORMAL]
    if dead:
        first = dead[0]
        kind = first.status if first.status in ("timeout", "unexplained") else "crash"
        summary = f"{first.checker} {first.status}: {first.detail}"
        return Finding(kind, _bucket(kind, first.checker, first.detail), summary, case, ran)

    verdicts = {o.coarse for o in ran}
    if len(verdicts) > 1:
        accepting = sorted(o.checker for o in ran if o.coarse == "accept")
        refusing = [o for o in ran if o.coarse == "reject"]
        why = refusing[0].detail if refusing else ""
        summary = (
            f"{', '.join(accepting)} accepted what "
            f"{', '.join(o.checker for o in refusing)} refused: {why}"
        )
        ref = next((o for o in ran if o.checker.split(" ")[0] == reference), None)
        kind = "underaccept" if ref is not None and ref.coarse == "accept" else "overaccept"
        who = "+".join(f"{o.checker}={o.coarse}" for o in sorted(ran, key=lambda o: o.checker))
        # The bucket keeps saying `disagreement` in both directions. The
        # direction is already in `who`, and the prefix is part of a reproducer's
        # path, which is part of its fingerprint -- so renaming it would restate
        # every finding already in the ledger to say something the row next to it
        # already says.
        return Finding(kind, _bucket("disagreement", who, why), summary, case, ran)
    return None


_UNSAFE = re.compile(r"[^a-z0-9]+")


def _bucket(kind: str, who: str, detail: str) -> str:
    """A directory name that is the same for two instances of one defect.

    The readable half is for whoever opens the corpus; the six hex digits are
    what actually makes it unique, because `_portable` has already thrown away
    everything that varies between two instances of the same bug.
    """
    stem = _UNSAFE.sub("-", f"{kind}-{who}-{detail}".lower()).strip("-")[:56]
    digest = hashlib.sha1(f"{kind}|{who}|{detail}".encode()).hexdigest()[:6]
    return f"{stem}-{digest}" if stem else f"{kind}-{digest}"


# -- shrinking ----------------------------------------------------------------

Probe = Callable[[Case], Finding | None]


def shrink(case: Case, probe: Probe, bucket: str, budget: int = 120) -> tuple[Case, int]:
    """Delta-debug the command list, keeping the finding the same finding.

    "The same" is the bucket, not the message: dropping a command moves every
    line number after it, so a shrink that insisted on an identical diagnostic
    would refuse to shrink anything.

    The commands-not-characters granularity is why this is short. It also
    bounds what it can do -- it will not simplify a term inside a command --
    which is a trade the corpus makes for a shrinker anyone can read.

    **A seed run as it stands is never shrunk.** The bucket is coarse on
    purpose, and it says nothing about *where* a checker refused -- so an edit
    the verdict does not depend on holds the bucket and is kept. That is a good
    trade for a case this fuzzer wrote and a bad one for a file somebody else
    committed, where the finding is "this file, as it is, disagrees" and any
    edit restates it as a claim about a file nobody has. It cost us a real one:
    a reproducer promoted from `test-indexed-op.cpc` with the `_` cut out of
    line 4 by this function, while the reference had refused at line 3
    throughout, and a note that named the cut as the cause. See
    `docs/reports/reports.md`.
    """
    if case.source.startswith("seed:"):
        return case, 0
    best = case
    spent = 0

    def holds(commands: list[str]) -> bool:
        nonlocal spent, best
        if not commands or spent >= budget:
            return False
        spent += 1
        got = probe(case.replace(commands))
        if got is not None and got.bucket == bucket:
            best = got.case
            return True
        return False

    commands = list(case.commands)
    n = 2
    while len(commands) >= 2 and spent < budget:
        size = max(1, len(commands) // n)
        chunks = [commands[i : i + size] for i in range(0, len(commands), size)]
        for i in range(len(chunks)):
            rest = [c for j, chunk in enumerate(chunks) if j != i for c in chunk]
            if holds(rest):
                commands, n = rest, max(2, n - 1)
                break
        else:
            if n >= len(commands):
                break
            n = min(2 * n, len(commands))

    # one last pass, one command at a time: cheap, and it usually takes a few
    # more off what the chunked passes left behind
    i = 0
    while i < len(commands) and spent < budget:
        rest = commands[:i] + commands[i + 1 :]
        if holds(rest):
            commands = rest
        else:
            i += 1

    # and then inside each surviving command, because "one command" is still
    # a whole `declare-rule` and the defect is usually one subterm of it
    for i in range(len(commands)):
        if spent >= budget:
            break
        commands[i] = _shrink_terms(
            commands[i], lambda c, i=i: holds(commands[:i] + [c] + commands[i + 1 :])
        )
    return best.replace(commands), spent


def _spans(text: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """The parenthesised spans of a command, and its atoms, as (start, end).

    The lexical rules are the ones `gen.split_commands` uses -- `;` to the end
    of the line, `"..."`, `|...|` -- because a shrinker that cut inside a string
    literal would be editing a token rather than a term.

    A parenthesis with no partner is reported as an atom, so the shrinker can
    delete it. The mutator inserts them, and a reproducer that still carries
    one is a reproducer whose reader has to work out whether it matters.
    """
    groups: list[tuple[int, int]] = []
    atoms: list[tuple[int, int]] = []
    stack: list[int] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == ";":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == '"':
            j = i + 1
            while j < n:
                if text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if text[j] == '"':
                    break
                j += 1
            atoms.append((i, min(j + 1, n)))
            i = j + 1
            continue
        if c == "|":
            j = text.find("|", i + 1)
            j = n if j < 0 else j
            atoms.append((i, min(j + 1, n)))
            i = j + 1
            continue
        if c == "(":
            stack.append(i)
        elif c == ")":
            if stack:
                groups.append((stack.pop(), i + 1))
            else:
                atoms.append((i, i + 1))
        elif not c.isspace():
            j = i
            while j < n and not text[j].isspace() and text[j] not in '()";|':
                j += 1
            atoms.append((i, j))
            i = j
            continue
        i += 1
    atoms += [(i, i + 1) for i in stack]  # openers that never closed
    return sorted(groups), sorted(atoms)


def _cut(text: str, start: int, end: int) -> str:
    """Delete a span, and the space it left behind with it.

    Only whitespace *between* lexed pieces is swallowed, which is why this
    takes the span rather than a pattern: nothing here can reach inside a
    string literal.
    """
    while start > 0 and text[start - 1] in " \t":
        if end >= len(text) or text[end] in " \t\n)":
            start -= 1
        else:
            break
    return text[:start] + text[end:]


def _shrink_terms(command: str, holds: Callable[[str], bool]) -> str:
    """Cut pieces out of one command while it still provokes the finding.

    Three moves, tried outside in: drop a parenthesised span, replace one with
    the first thing inside it, and drop a single atom. Between them they take
    `(declare-const f (-> (Seq T) Bool))` down to `(declare-const f (->))`,
    which is the difference between a reproducer somebody reads and one
    somebody has to reduce by hand first.

    The outermost span is left alone: deleting it is deleting the command,
    which the pass above has already tried.
    """
    for _ in range(8):  # each round strictly shortens; a few settle it
        groups, atoms = _spans(command)
        moves: list[str] = []
        for start, end in groups[1:]:
            inner = command[start + 1 : end - 1].strip()
            moves.append(_cut(command, start, end))
            if inner:
                moves.append(command[:start] + inner.split()[0] + command[end:])
        for start, end in atoms:
            moves.append(_cut(command, start, end))
        for candidate in moves:
            candidate = candidate.strip()
            if candidate and candidate != command and holds(candidate):
                command = candidate
                break
        else:
            return command
    return command


# -- the corpus ---------------------------------------------------------------


class Corpus:
    """Where findings are kept: one directory per bucket, first instance only.

    Deliberately append-only in the same sense `docs/reports/open-findings.md` is: a
    bucket that already has a case keeps the one it has, so re-running the
    fuzzer over a wider seed range never overwrites the small reproducer
    somebody already shrank and read.
    """

    def __init__(self, root: str) -> None:
        self.root = root
        self.new: list[Finding] = []
        # What is already on disk counts as seen. Append-only has to survive
        # the process ending, or a second run into the same directory writes a
        # second case beside the first one -- a `.cpc` next to an `.eo`, from a
        # different mode -- and the reproducer somebody read is no longer the
        # one the record describes.
        self.counts: dict[str, int] = {
            name: 1
            for name in (os.listdir(root) if os.path.isdir(root) else [])
            if os.path.isfile(os.path.join(root, name, "finding.json"))
        }

    def seen(self, bucket: str) -> bool:
        return bucket in self.counts

    def add(self, finding: Finding) -> bool:
        """Record it. True when this bucket is new, and a case was written."""
        first = finding.bucket not in self.counts
        self.counts[finding.bucket] = self.counts.get(finding.bucket, 0) + 1
        if not first:
            return False
        self.new.append(finding)
        where = os.path.join(self.root, finding.bucket)
        os.makedirs(where, exist_ok=True)
        with open(os.path.join(where, "case" + finding.case.suffix), "w") as f:
            f.write(finding.case.text())
        with open(os.path.join(where, "finding.json"), "w") as f:
            json.dump(finding.as_json(), f, indent=1)
        with open(os.path.join(self.root, "findings.jsonl"), "a") as f:
            f.write(json.dumps(finding.as_json(), sort_keys=True) + "\n")
        return True
