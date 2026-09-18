"""Guards against reporting too much.

A check that reports two hundred findings has almost certainly broken rather
than found two hundred defects. It has happened here: a change to how a
directory is read once merged 191 unrelated test signatures into one symbol
table, and three checks reported 253 findings that were all artefacts of the
merge. Nothing failed; the run simply printed them.

So a run bounds what it will report, per check and in total, and treats hitting
a bound as *a defect in the analyzer* rather than as a result about the
signature: it says so as an error, holds the flood back, and keeps a few
examples. The alternative -- printing everything and trusting a reader to notice
the shape of it -- is how a tool teaches people to ignore it.

Nothing is ever dropped silently. A bound that bites says which check, how many
it held, and how to see them anyway.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass

from .diagnostics import Diagnostic, Severity, Span

# Deliberately low. The most any single check reports on the corpora we know is
# fourteen; a check in the fifties is telling you about itself.
DEFAULT_PER_CHECK = 25
DEFAULT_TOTAL = 200

# How many of a held-back check's findings to keep, so that the report still
# shows what it was reporting.
KEEP = 3


@dataclass
class Limits:
    per_check: int = DEFAULT_PER_CHECK
    total: int = DEFAULT_TOTAL
    enabled: bool = True


def apply(diags: list[Diagnostic], limits: Limits) -> list[Diagnostic]:
    """What a run reports, with a flood held back and said out loud."""
    if not limits.enabled or not diags:
        return diags

    out: list[Diagnostic] = []
    counts = collections.Counter(d.code for d in diags)
    kept_per_code: collections.Counter = collections.Counter()
    floods = {c: n for c, n in counts.items() if n > limits.per_check}

    for d in diags:
        if d.code not in floods:
            out.append(d)
            continue
        if kept_per_code[d.code] < KEEP:
            kept_per_code[d.code] += 1
            out.append(d)

    for code, n in sorted(floods.items()):
        first = next(d for d in diags if d.code == code)
        out.append(
            Diagnostic(
                code="ANO0001",
                severity=Severity.ERROR,
                message=f"{code} reported {n} findings, over the limit of "
                f"{limits.per_check}",
                span=Span(first.span.path, first.span.line, first.span.col),
                label="held back",
                notes=[
                    f"{KEEP} are shown above and {n - KEEP} are not",
                    "a check reporting this much is usually misfiring rather than "
                    "finding: the signature is the same size it was yesterday",
                    f"to see them anyway: --only {code} --no-limits",
                ],
                help="if the findings are real, raise `limits.per_check` in "
                "anoieu.json and say why",
            )
        )

    if len(out) > limits.total:
        dropped = len(out) - limits.total
        out = out[: limits.total]
        first = out[0] if out else None
        out.append(
            Diagnostic(
                code="ANO0002",
                severity=Severity.ERROR,
                message=f"this run reported more than {limits.total} findings; "
                f"{dropped} are not shown",
                span=Span(first.span.path if first else "<run>", 1, 1),
                label="held back",
                notes=[
                    "a run this loud is a run nobody reads, and is more often the "
                    "analyzer's fault than the signature's",
                    "to see them anyway: --no-limits",
                ],
            )
        )
    return out
