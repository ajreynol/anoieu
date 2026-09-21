# Open bugs

Generated from [bugs.json](bugs.json) by `anoieu_analyzer.reporting.database`.
Do not edit this view by hand. [Update instructions](README.md).

Only open findings appear here. Entries carrying a `closed_verdict`,
including declined and intentional (won't fix) findings, are omitted.
The complete history and closure reasoning remain in [bugs.json](bugs.json).
See [Closure](README.md#closure) for the verdicts and the separate audit
of fixes awaiting landing. Open means nobody has ruled, not that a check
was re-run. Dates record ingestion, not fresh reproduction. Static evidence
links use the originally recorded source commit; fuzzer links open the
committed reproducers.

| Producer | Open findings |
| --- | ---: |
| [Static analyzer](#static-analyzer) | 1 |
| [Fuzzer](#fuzzer) | 0 |

## Static analyzer

| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7ca5c014646b8984 | [EO0083](../anoieu_analyzer/checks.md#eo0083) | cvc5 | rule \`arith-eq-elim-int\` matches exactly what \`arith-eq-elim-real\` matches | open | [proofs/eo/cpc/rules/Rewrites.eo:94](https://github.com/cvc5/cvc5/blob/aee8742/proofs/eo/cpc/rules/Rewrites.eo#L94) | 2026-09-16 | 2026-09-19 |

## Fuzzer

No open findings.
