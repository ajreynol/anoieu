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

## Open static findings (13)

| bug | owner | code | where | description | status | first seen | last seen |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EO0083-Rewrites.eo-94 | cvc5 | EO0083 | proofs/eo/cpc/rules/Rewrites.eo:94 | rule \`arith-eq-elim-int\` matches exactly what \`arith-eq-elim-real\` matches | open | 2026-09-16 | 2026-09-16 |
| EO0084-Builtin-rules.eo-61 | ethos | EO0084 | tests/Builtin-rules.eo:61 | rule \`identity\` concludes one of its own premises | open | 2026-09-16 | 2026-09-16 |
| EO0084-binder-ex.eo-10 | ethos | EO0084 | tests/binder-ex.eo:10 | rule \`id\` concludes one of its own premises | open | 2026-09-16 | 2026-09-16 |
| EO0084-binder-subterm-share.eo-8 | ethos | EO0084 | tests/binder-subterm-share.eo:8 | rule \`id\` concludes one of its own premises | open | 2026-09-16 | 2026-09-16 |
| EO0054-conclusion-spec.eo-8 | ethos | EO0054 | tests/conclusion-spec.eo:8 | this pattern matches an \`or\` of exactly 2 element(s) | open | 2026-09-16 | 2026-09-16 |
| EO0071-eo-definitions.eo-190 | ethos | EO0071 | tests/eo-definitions.eo:190 | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0071-eo-definitions.eo-229 | ethos | EO0071 | tests/eo-definitions.eo:229 | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0071-eo-definitions.eo-252 | ethos | EO0071 | tests/eo-definitions.eo:252 | \`-1\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0071-eo-definitions.eo-263 | ethos | EO0071 | tests/eo-definitions.eo:263 | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0071-right-assoc-variants.eo-62 | ethos | EO0071 | tests/right-assoc-variants.eo:62 | \`""\` is a &lt;string&gt; literal, and this signature has no \`declare-consts &lt;string&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0071-right-assoc-variants.eo-48 | ethos | EO0071 | tests/right-assoc-variants.eo:48 | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | 2026-09-16 | 2026-09-16 |
| EO0054-Nary.eo-157 | ethos | EO0054 | tests/Nary.eo:157 | this pattern matches an \`cons\` of exactly 2 element(s) | open | 2026-08-31 | 2026-08-31 |
| EO0054-Nary.eo-90 | ethos | EO0054 | tests/Nary.eo:90 | this pattern matches an \`cons\` of exactly 2 element(s) | open | 2026-08-31 | 2026-08-31 |
