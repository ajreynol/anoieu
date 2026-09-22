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
| [Fuzzer](#fuzzer) | 8 |

## Static analyzer

| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7ca5c014646b8984 | [EO0083](../anoieu_analyzer/checks.md#eo0083) | cvc5 | rule \`arith-eq-elim-int\` matches exactly what \`arith-eq-elim-real\` matches | open | [proofs/eo/cpc/rules/Rewrites.eo:94](https://github.com/cvc5/cvc5/blob/aee8742/proofs/eo/cpc/rules/Rewrites.eo#L94) | 2026-09-16 | 2026-09-19 |

## Fuzzer

| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7836f9530ce4994c | [FUZ0002](../anoieu_fuzz/fuzzing.md#the-codes) | ethos | ethos crash, with nothing on either stream | open | [tests/fuzz/crash-ethos-af49e1/case.cpc:2](../tests/fuzz/crash-ethos-af49e1/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| d88112e31fcc646e | [FUZ0001](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | logos accepted what ethos refused: Error: &lt;path&gt;:N.N: Unexpected conclusion for rule contra: | open | [tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-un-1e92c8/case.cpc:2](../tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-un-1e92c8/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 1cc815407beb3759 | [FUZ0001](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | logos accepted what ethos refused: Error: &lt;path&gt;:N.N: Expected SMT-LIBv2 symbol, got \`\_\` (BINARY\_LITERAL). | open | [tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-7cc7d4/case.cpc:2](../tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-7cc7d4/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 4a419fe0339d88b6 | [FUZ0001](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | logos accepted what ethos refused: Error: &lt;path&gt;:N.N: A step of rule contra failed to check. | open | [tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-a--4aa4ad/case.cpc:2](../tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-a--4aa4ad/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 48d0d19946863a67 | [FUZ0005](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | ethos accepted what logos refused: Error parsing proof: Error: parametric datatype List (...) is not supported | open | [tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-147d8c/case.cpc:2](../tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-147d8c/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 4bdbda42c0bc7861 | [FUZ0005](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | ethos accepted what logos refused: Error parsing proof: Error: expected a symbol, an indexed symbol or a type ascription as the head of an application, got (...) | open | [tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-0e9250/case.cpc:2](../tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-0e9250/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 893a71805a2c431d | [FUZ0005](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | ethos accepted what logos refused: Error parsing proof: Error: no declaration of &lt;= takes N indices and N arguments | open | [tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-acb5d4/case.cpc:2](../tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-acb5d4/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
| 26af98b965618686 | [FUZ0005](../anoieu_fuzz/fuzzing.md#the-codes) | ethos+logos | ethos accepted what logos refused: Error parsing proof: Error: unrecognized command (declare-datatype Dsng ((...) (esng))), expected one of declare-const, declare-fun, declare-sort, declare-datat | open | [tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-889ea9/case.cpc:2](../tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-889ea9/case.cpc#L2) | 2026-09-22 | 2026-09-22 |
