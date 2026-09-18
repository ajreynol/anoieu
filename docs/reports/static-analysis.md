# Static analysis

Every static finding the checks have found on the standard targets, rendered from
[`bug_db/bugs.json`](../../bug_db/bugs.json) -- which is the database itself, and the file to read if
you want the data rather than the table. The analyzer and ledger generator
render this static subset. The database also records
[promoted fuzzer findings](../fuzzing.md#recording-through-koine); it
is maintained exclusively by [koine](https://github.com/ajreynol/koine)'s `koine_append_db`,
which adds what is new and never edits or removes what is already there.

**This page is the new workflow and it is not yet the report.** The report is
[`open-findings.md`](open-findings.md), generated the way it always was. Nothing
here closes a bug and no verdict reached this file: a bug that has been fixed is
still in the database, with the date it was last seen. What a finding is and what
settles one stay ours -- see [`reporting-workflow.md`](reporting-workflow.md).

A second producer, an agent driven by
[`prompts/anoieu_analyzer_agent`](../../prompts/anoieu_analyzer_agent), writes
a dump in the same shape and appends to the same database.


## Every static finding recorded (54)

| bug | owner | code | where | description | first seen | last seen |
| --- | --- | --- | --- | --- | --- | --- |
| `DOC0011-Booleans.eo-363` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Booleans.eo:363` | rule `not_implies_elim2` takes 0 argument(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Booleans.eo-463` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Booleans.eo:463` | rule `ite_elim2` takes 0 argument(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Uf.eo-31` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Uf.eo:31` | rule `symm` takes 0 argument(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Arith.eo-509` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Arith.eo:509` | rule `arith_poly_norm` takes 1 argument(s), and its docstring lists 2 | 2026-09-16 | 2026-09-16 |
| `DOC0011-BitVectors.eo-240` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/BitVectors.eo:240` | rule `bv_poly_norm` takes 1 argument(s), and its docstring lists 2 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Strings.eo-191` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Strings.eo:191` | rule `string_decompose` takes 2 premise(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Quantifiers.eo-148` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Quantifiers.eo:148` | rule `quant_var_reordering` takes 0 premise(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Quantifiers.eo-95` | cvc5 | DOC0011 | `proofs/eo/cpc/programs/Quantifiers.eo:95` | program `$substitute_simul_rec` takes 5 argument(s), and its docstring lists 4 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Strings.eo-202` | cvc5 | DOC0011 | `proofs/eo/cpc/programs/Strings.eo:202` | program `$re_ac_merge` takes 3 argument(s), and its docstring lists 5 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Strings.eo-224` | cvc5 | DOC0011 | `proofs/eo/cpc/programs/Strings.eo:224` | program `$re_concat_merge` takes 2 argument(s), and its docstring lists 4 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Strings.eo-244` | cvc5 | DOC0011 | `proofs/eo/cpc/programs/Strings.eo:244` | program `$derivative` takes 2 argument(s), and its docstring lists 5 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Strings.eo-1233` | cvc5 | DOC0011 | `proofs/eo/cpc/programs/Strings.eo:1233` | program `$re_rev_map_rev` takes 2 argument(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0011-ArithBvConv.eo-9` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/ArithBvConv.eo:9` | program `$abconv_ubv_to_int_elim` takes 3 argument(s), and its docstring lists 4 | 2026-09-16 | 2026-09-16 |
| `DOC0011-Datatypes.eo-360` | cvc5 | DOC0011 | `proofs/eo/cpc/rules/Datatypes.eo:360` | program `$mk_dt_updater_elim_rhs` takes 3 argument(s), and its docstring lists 2 | 2026-09-16 | 2026-09-16 |
| `DOC0012-Booleans.eo-363` | cvc5 | DOC0012 | `proofs/eo/cpc/rules/Booleans.eo:363` | rule `not_implies_elim2` has no args, and its docstring documents one | 2026-09-16 | 2026-09-16 |
| `DOC0012-Booleans.eo-463` | cvc5 | DOC0012 | `proofs/eo/cpc/rules/Booleans.eo:463` | rule `ite_elim2` has no args, and its docstring documents one | 2026-09-16 | 2026-09-16 |
| `DOC0012-Uf.eo-31` | cvc5 | DOC0012 | `proofs/eo/cpc/rules/Uf.eo:31` | rule `symm` has no args, and its docstring documents one | 2026-09-16 | 2026-09-16 |
| `DOC0012-Quantifiers.eo-148` | cvc5 | DOC0012 | `proofs/eo/cpc/rules/Quantifiers.eo:148` | rule `quant_var_reordering` has no premises, and its docstring documents one | 2026-09-16 | 2026-09-16 |
| `EO0054-Strings.eo-1749` | cvc5 | EO0054 | `proofs/eo/cpc/programs/Strings.eo:1749` | this pattern matches a `*` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Strings.eo-306` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Strings.eo:306` | this pattern matches a `str.++` of exactly 3 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-399` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:399` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-540` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:540` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-732` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:732` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-943` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:943` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-948` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:948` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-1166` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1166` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-1245` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1245` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-1250` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1250` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-1255` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1255` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0054-Rewrites.eo-1746` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1746` | this pattern matches a `+` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0077-Cpc.eo-555` | cvc5 | EO0077 | `proofs/eo/cpc/Cpc.eo:555` | rule `trust` is admitted: it is marked `:sorry` | 2026-09-16 | 2026-09-16 |
| `EO0083-Rewrites.eo-94` | cvc5 | EO0083 | `proofs/eo/cpc/rules/Rewrites.eo:94` | rule `arith-eq-elim-int` matches exactly what `arith-eq-elim-real` matches | 2026-09-16 | 2026-09-16 |
| `EO0064-Strings.eo-46` | cvc5 | EO0064 | `proofs/eo/cpc/programs/Strings.eo:46` | this case of `$is_seq_const_rec` returns Bool, and the program declares Int | 2026-09-16 | 2026-09-16 |
| `EO0064-Strings.eo-47` | cvc5 | EO0064 | `proofs/eo/cpc/programs/Strings.eo:47` | this case of `$is_seq_const_rec` returns Bool, and the program declares Int | 2026-09-16 | 2026-09-16 |
| `EO0064-Strings.eo-58` | cvc5 | EO0064 | `proofs/eo/cpc/programs/Strings.eo:58` | this case of `$is_seq_const` returns Bool, and the program declares Int | 2026-09-16 | 2026-09-16 |
| `EO0031-ArithExt.eo-17` | cvc5 | EO0031 | `proofs/eo/cpc/expert/theories/ArithExt.eo:17` | `@arith_vts_delta` is declared twice with the type Real | 2026-09-16 | 2026-09-16 |
| `EO0031-ArithExt.eo-18` | cvc5 | EO0031 | `proofs/eo/cpc/expert/theories/ArithExt.eo:18` | `@arith_vts_delta_free` is declared twice with the type Real | 2026-09-16 | 2026-09-16 |
| `EO0031-ArithExt.eo-19` | cvc5 | EO0031 | `proofs/eo/cpc/expert/theories/ArithExt.eo:19` | `@arith_vts_infinity` is declared twice with the type T | 2026-09-16 | 2026-09-16 |
| `EO0031-ArithExt.eo-20` | cvc5 | EO0031 | `proofs/eo/cpc/expert/theories/ArithExt.eo:20` | `@arith_vts_infinity_free` is declared twice with the type T | 2026-09-16 | 2026-09-16 |
| `EO0084-Builtin-rules.eo-61` | ethos | EO0084 | `tests/Builtin-rules.eo:61` | rule `identity` concludes one of its own premises | 2026-09-16 | 2026-09-16 |
| `DOC0011-Uf-rules.eo-25` | ethos | DOC0011 | `tests/Uf-rules.eo:25` | rule `symm` takes 0 argument(s), and its docstring lists 1 | 2026-09-16 | 2026-09-16 |
| `DOC0012-Uf-rules.eo-25` | ethos | DOC0012 | `tests/Uf-rules.eo:25` | rule `symm` has no args, and its docstring documents one | 2026-09-16 | 2026-09-16 |
| `EO0084-binder-ex.eo-10` | ethos | EO0084 | `tests/binder-ex.eo:10` | rule `id` concludes one of its own premises | 2026-09-16 | 2026-09-16 |
| `EO0084-binder-subterm-share.eo-8` | ethos | EO0084 | `tests/binder-subterm-share.eo:8` | rule `id` concludes one of its own premises | 2026-09-16 | 2026-09-16 |
| `EO0054-conclusion-spec.eo-8` | ethos | EO0054 | `tests/conclusion-spec.eo:8` | this pattern matches an `or` of exactly 2 element(s) | 2026-09-16 | 2026-09-16 |
| `EO0071-eo-definitions.eo-190` | ethos | EO0071 | `tests/eo-definitions.eo:190` | `0` is a <numeral> literal, and this signature has no `declare-consts <numeral>` | 2026-09-16 | 2026-09-16 |
| `EO0071-eo-definitions.eo-229` | ethos | EO0071 | `tests/eo-definitions.eo:229` | `0` is a <numeral> literal, and this signature has no `declare-consts <numeral>` | 2026-09-16 | 2026-09-16 |
| `EO0071-eo-definitions.eo-252` | ethos | EO0071 | `tests/eo-definitions.eo:252` | `-1` is a <numeral> literal, and this signature has no `declare-consts <numeral>` | 2026-09-16 | 2026-09-16 |
| `EO0071-eo-definitions.eo-263` | ethos | EO0071 | `tests/eo-definitions.eo:263` | `0` is a <numeral> literal, and this signature has no `declare-consts <numeral>` | 2026-09-16 | 2026-09-16 |
| `EO0040-match-simple.eo-11` | ethos | EO0040 | `tests/match-simple.eo:11` | `<` is marked `:right-assoc`, so its second argument and its return type must agree | 2026-09-16 | 2026-09-16 |
| `EO0052-naive-nary.eo-182` | ethos | EO0052 | `tests/naive-nary.eo:182` | this case of `isPermutation` can never be reached | 2026-09-16 | 2026-09-16 |
| `EO0071-right-assoc-variants.eo-62` | ethos | EO0071 | `tests/right-assoc-variants.eo:62` | `""` is a <string> literal, and this signature has no `declare-consts <string>` | 2026-09-16 | 2026-09-16 |
| `EO0071-right-assoc-variants.eo-48` | ethos | EO0071 | `tests/right-assoc-variants.eo:48` | `0` is a <numeral> literal, and this signature has no `declare-consts <numeral>` | 2026-09-16 | 2026-09-16 |
| `EO0077-sorry.eo-4` | ethos | EO0077 | `tests/sorry.eo:4` | rule `trust` is admitted: it is marked `:sorry` | 2026-09-16 | 2026-09-16 |
