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
| [Static analyzer](#static-analyzer) | 13 |
| [Fuzzer](#fuzzer) | 1 |

## Static analyzer

| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7ca5c014646b8984 | [EO0083](../anoieu_analyzer/checks.md#eo0083) | cvc5 | rule \`arith-eq-elim-int\` matches exactly what \`arith-eq-elim-real\` matches | open | [proofs/eo/cpc/rules/Rewrites.eo:94](https://github.com/cvc5/cvc5/blob/aee8742/proofs/eo/cpc/rules/Rewrites.eo#L94) | 2026-09-16 | 2026-09-16 |
| 52b5ae926f12d4c9 | [EO0084](../anoieu_analyzer/checks.md#eo0084) | ethos | rule \`identity\` concludes one of its own premises | open | [tests/Builtin-rules.eo:61](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/Builtin-rules.eo#L61) | 2026-09-16 | 2026-09-16 |
| 7f3eb81581c1f0a1 | [EO0084](../anoieu_analyzer/checks.md#eo0084) | ethos | rule \`id\` concludes one of its own premises | open | [tests/binder-ex.eo:10](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/binder-ex.eo#L10) | 2026-09-16 | 2026-09-16 |
| 74c6f064da7c2464 | [EO0084](../anoieu_analyzer/checks.md#eo0084) | ethos | rule \`id\` concludes one of its own premises | open | [tests/binder-subterm-share.eo:8](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/binder-subterm-share.eo#L8) | 2026-09-16 | 2026-09-16 |
| 516184abdc82d1df | [EO0054](../anoieu_analyzer/checks.md#eo0054) | ethos | this pattern matches an \`or\` of exactly 2 element(s) | open | [tests/conclusion-spec.eo:8](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/conclusion-spec.eo#L8) | 2026-09-16 | 2026-09-16 |
| 42d486abefc2fc62 | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | [tests/eo-definitions.eo:190](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/eo-definitions.eo#L190) | 2026-09-16 | 2026-09-16 |
| 70fa22c05a9635d8 | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | [tests/eo-definitions.eo:229](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/eo-definitions.eo#L229) | 2026-09-16 | 2026-09-16 |
| 8dbf440aca48da0c | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`-1\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | [tests/eo-definitions.eo:252](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/eo-definitions.eo#L252) | 2026-09-16 | 2026-09-16 |
| 6b2263f824b28bd0 | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | [tests/eo-definitions.eo:263](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/eo-definitions.eo#L263) | 2026-09-16 | 2026-09-16 |
| 584eda1d79a64b2c | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`""\` is a &lt;string&gt; literal, and this signature has no \`declare-consts &lt;string&gt;\` | open | [tests/right-assoc-variants.eo:62](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/right-assoc-variants.eo#L62) | 2026-09-16 | 2026-09-16 |
| 59e8abdd4478092d | [EO0071](../anoieu_analyzer/checks.md#eo0071) | ethos | \`0\` is a &lt;numeral&gt; literal, and this signature has no \`declare-consts &lt;numeral&gt;\` | open | [tests/right-assoc-variants.eo:48](https://github.com/cvc5/ethos/blob/6beeb8e6/tests/right-assoc-variants.eo#L48) | 2026-09-16 | 2026-09-16 |
| dcfaf1e214126aa3 | [EO0054](../anoieu_analyzer/checks.md#eo0054) | ethos | this pattern matches an \`cons\` of exactly 2 element(s) | open | tests/Nary.eo:157 | 2026-08-31 | 2026-08-31 |
| f52484ca50c98a65 | [EO0054](../anoieu_analyzer/checks.md#eo0054) | ethos | this pattern matches an \`cons\` of exactly 2 element(s) | open | tests/Nary.eo:90 | 2026-08-31 | 2026-08-31 |

## Fuzzer

| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9315026a26d2c2d0 | [FUZ0001](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | logos accepted what ethos refused: Error: &lt;path&gt;:N.N: Expected Eunoia command, got \`\_\` (LPAREN). | open | [tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-afbd92/case.cpc:2](../tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-afbd92/case.cpc#L2) | 2026-09-17 | 2026-09-17 |
