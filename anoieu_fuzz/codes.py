"""The codes the fuzzer reports under, and the page behind each.

A finding from the fuzzer goes into the same ledger as a finding from the
checks -- [`docs/open-findings.md`](../docs/open-findings.md), an id, an owner,
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
    "two checkers answer the same file differently",
    Severity.ERROR,
    """
One checker accepted this file and another refused it. Both were given the same
bytes, so exactly one of them is wrong, and which one this finding does not say
-- deciding that needs the semantics the fuzzer deliberately does without.

Read it in the direction that matters for the checker you own:

- **the reference accepts and yours refuses** is a completeness gap: a proof
  somebody could legitimately produce, that your checker will not take;
- **yours accepts and the reference refuses** is the one to look at first. It
  may be a soundness bug, and it may equally be the reference being stricter
  than the language requires -- ethos refuses `declare-fun` outside a reference
  file, for instance, which is a fact about ethos's file roles rather than about
  the proof.

Before filing either, check the comparison is fair. Ethos is run with
`--require-proof-of-false` so that its `correct` means what logos's does; a
checker configured without the equivalent will disagree about almost every file
and none of it will be a defect. `docs/fuzzing.md` has the arrangement.
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

#: What each kind of finding is reported as.
KIND_TO_CODE = {
    "disagreement": "FUZ0001",
    "crash": "FUZ0002",
    "unexplained": "FUZ0003",
    "timeout": "FUZ0004",
}


def code_for(kind: str) -> Code:
    return CODES[KIND_TO_CODE[kind]]
