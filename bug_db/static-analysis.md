# Open static analysis findings

Generated from [bugs.json](bugs.json) by `anoieu_analyzer.reporting.database`.
Do not edit this view by hand. [Update instructions](README.md).

Only static findings without a `closed_verdict` appear here. Closed findings,
including declined and intentional (won't fix) findings, remain in
[bugs.json](bugs.json) with their verdicts, evidence and ingestion dates.
[bugs.md](bugs.md) includes open findings from both the analyzer and fuzzer.
Open means nobody has ruled; ingestion dates do not imply a fresh reproduction.
See [Closure](README.md#closure) for the verdicts and the separate audit
of fixes awaiting landing.

## Open static findings (1)

| bug | owner | code | where | description | status | first seen | last seen |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EO0083-Rewrites.eo-94 | cvc5 | EO0083 | proofs/eo/cpc/rules/Rewrites.eo:94 | rule \`arith-eq-elim-int\` matches exactly what \`arith-eq-elim-real\` matches | open | 2026-09-16 | 2026-09-16 |
