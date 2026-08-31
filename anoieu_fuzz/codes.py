"""The codes the fuzzer reports under, and the page behind each.

A finding from the fuzzer goes into the same ledger as a finding from the
checks -- [`docs/reports/open-findings.md`](../docs/reports/open-findings.md), an id, an owner,
a verdict -- so it needs the same two things a check has: a code, and a page
saying what the code means. The prefix is the marker. `EO`, `DOC` and `TRI` are
things *anoieu read*; **`FUZ` is something the fuzzer provoked**, and the two
are worth telling apart on sight, because they are confirmed differently: a
check's finding is re-derived by running the check again, and a fuzzer's is
re-derived by running a binary against a committed reproducer.

The pages are written here rather than in the analyzer's registry on purpose.
The fuzzer depends on anoieu's front end; anoieu does not depend on the fuzzer,
and a page that made it do so would be paying for tidiness with a cycle.
"""

from __future__ import annotations

from dataclasses import dataclass

from anoieu.diagnostics import Severity


@dataclass(frozen=True)
class Code:
    code: str
    title: str
    severity: Severity
    page: str


CODES: dict[str, Code] = {}


def _code(code: str, title: str, severity: Severity, page: str) -> None:
    CODES[code] = Code(code, title, severity, page.strip())


_code(
    "FUZ0001",
    "a checker accepted what the reference refused",
    Severity.ERROR,
    """
A checker took a file that the reference implementation will not. This is the
serious direction, and it is the reason the fuzzer distinguishes the two.

Ethos is the reference: it is what defines, operationally, which files are
Eunoia and which proofs are derivations. A second checker that accepts a file
ethos rejects is accepting something outside that definition, and if the second
checker is a verified one, its theorem is now about a term its parser invented
rather than about the proof somebody wrote. That is the shape of an unsoundness
even when the particular case is harmless -- the guarantee has been quietly
restated.

It is not proof of one. Ethos refuses files for reasons that are about ethos: a
`declare-fun` outside a reference file is a fact about its file roles rather
than about the proof. So the finding is a question, and the answer is one of:

- the second checker is wrong, and the fix is in its parser or its checker;
- the reference is stricter than the language requires, and `ethos` is the
  finding;
- the two are answering different questions, and the comparison was unfair --
  check `--require-proof-of-false` is in play before anything else.

Which checker is the reference is configuration -- the `"reference"` key of a
`--config` file, `ethos` by default. When the reference did not run, a
disagreement is reported under this code rather than `FUZ0005`, because
assuming the less serious reading of an unattributed disagreement is the wrong
way to be wrong.
""",
)

_code(
    "FUZ0002",
    "a checker died with nothing to say",
    Severity.ERROR,
    """
The checker went down without a diagnostic: a signal and an empty stream, an
assertion, `terminate called after throwing ...`. Whatever the input was, this
is a defect in the checker -- a proof checker is a program that answers, and
the answers are `correct`, `incomplete`, `incorrect` or an explained refusal.

Note what this is *not*. Ethos reports every ordinary error by aborting, so a
`SIGABRT` on its own is not this finding; what makes it one is the absence of
any explanation. `anoieu_fuzz/checkers.py:classify` is where that line is drawn,
and it is drawn on what the checker said rather than on how it exited.

The reproducer is committed beside this finding. Confirm it against a build of
the commit `tools/deps.lock` records before filing it: a crash in somebody's
working tree is not news.
""",
)

_code(
    "FUZ0003",
    "a checker failed outside its own diagnostic convention",
    Severity.WARNING,
    """
The checker printed something and then failed anyway, but not in the form it
uses for everything else. Ethos's convention is
`Error: <file>:<line>.<col>: <what>`, and it has paths that skip it entirely --
declaring a literal category twice, `assume-push` at the top level of a
signature, an `include` of a file that is not there. Each of those aborts with
an internal message carrying no `Error:`, no file and no line.

This is a defect in what the checker *says* rather than in what it does, which
is why it is a warning and a code of its own. It matters anyway: an editor, a
CI annotation and this repository's own oracle all read that output by its
shape, and a message outside the shape is a failure they report as something
else, or miss.

The fix is on the checker's side and is usually one line -- route the message
through the same reporting path as the rest.
""",
)

_code(
    "FUZ0004",
    "a checker did not answer",
    Severity.WARNING,
    """
The checker was still running when the timeout expired. Suspect rather than
certain, and reported as a warning for that reason: the generator can write a
file that is genuinely expensive, and "slower than N seconds" is not by itself
a defect.

What makes it one is disproportion. Raise `--timeout` and re-run: a case that
finishes in twice the budget is a slow case, and a case that is still running
in a hundred times the budget is a checker that does not terminate on it. The
second is worth filing and the first is not.
""",
)

_code(
    "FUZ0005",
    "a checker refused what the reference accepted",
    Severity.WARNING,
    """
The other direction, and the less serious one: a checker will not take a file
the reference checks happily.

Nothing unsound follows from it. A checker that refuses too much rejects
work it should have done, which costs its users a proof they cannot check;
a checker that accepts too much (`FUZ0001`) may be guaranteeing something it
has not established. The two are not symmetric and the severity says so --
error there, warning here.

It is still a defect, and often a documentation defect rather than a code one.
A checker with a deliberately narrower input format -- assumptions before
steps, say, because its correctness theorem is stated over an assumption list
-- is not wrong to have one, but the restriction is then part of its interface
and should be written down where somebody producing proofs for it will read it.
A parity claim that is not qualified is what turns a restriction into a
finding.
""",
)

#: What each kind of finding is reported as. The two directions of a
#: disagreement are different findings with different severities; everything
#: else is about one checker on its own.
KIND_TO_CODE = {
    "overaccept": "FUZ0001",
    "underaccept": "FUZ0005",
    "crash": "FUZ0002",
    "unexplained": "FUZ0003",
    "timeout": "FUZ0004",
}


def code_for(kind: str) -> Code:
    return CODES[KIND_TO_CODE[kind]]
