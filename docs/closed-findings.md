# Closed findings

**Internal.** Every finding that has been ruled on, with the verdict against it.
This is the half of the ledger nobody is asked to read: the report is
[`open-findings.md`](open-findings.md), and the reasoning behind each verdict is
in [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back).

Kept as a file, and kept in git, for three reasons.

1. **It is what makes a verdict stick.** `tools/gen_open_findings.py` skips any
   id listed here. A row simply deleted from the report would be found again on
   the next run, because the finding is still there to be found.
2. **A row is moved here, never deleted.** Closing is a judgement somebody
   signs, and the diff that moves a row is the record of it.
3. **A verdict is a claim about the world, and can go stale.** *fixed upstream*
   was recorded three times for a fix that never landed, and it went unnoticed
   for as long as it did because a closed id is one nothing re-derives. Where a
   verdict depends on somebody else's tree, it should say which commit it was
   checked at.

Written by hand, by the review step in
[`reporting-policy.md`](reporting-policy.md#the-workflow). The generator reads
it and rewrites it, and rewriting preserves every row.

| id | owner | code | where | what | verdict |
| --- | --- | --- | --- | --- | --- |
| `dd90590c7cc85916` | logos | EO0064 | `install/defs/Cpc.cached.eo:2252` | this case of `$is_seq_const_rec` returns Bool, and the program declares Int | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `af3e2426c03378f8` | logos | EO0064 | `install/defs/Cpc.cached.eo:2253` | this case of `$is_seq_const_rec` returns Bool, and the program declares Int | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `db3bebb3d118f2bd` | logos | EO0064 | `install/defs/Cpc.cached.eo:2259` | this case of `$is_seq_const` returns Bool, and the program declares Int | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `2e32230f53cd937e` | logos | EO0083 | `install/defs/Cpc.cached.eo:4444` | rule `arith-eq-elim-int` matches exactly what `arith-eq-elim-real` matches | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `5ae3d0404b0f5258` | logos | EO0054 | `install/defs/Cpc.cached.eo:3102` | this pattern matches an `*` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `2df8343d1a4b70b5` | logos | EO0054 | `install/defs/Cpc.cached.eo:3492` | this pattern matches an `str.++` of exactly 3 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `b27d3def22beb16e` | logos | EO0054 | `install/defs/Cpc.cached.eo:4749` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `2074c9351e4496a1` | logos | EO0054 | `install/defs/Cpc.cached.eo:4890` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `4309c49e54760e9c` | logos | EO0054 | `install/defs/Cpc.cached.eo:5082` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `9b576113aedf61f4` | logos | EO0054 | `install/defs/Cpc.cached.eo:5293` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `e621f59502bd9c65` | logos | EO0054 | `install/defs/Cpc.cached.eo:5298` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `b2ccb7c697fadccf` | logos | EO0054 | `install/defs/Cpc.cached.eo:5516` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `5e085563326ca740` | logos | EO0054 | `install/defs/Cpc.cached.eo:5595` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `80da672a81fa0705` | logos | EO0054 | `install/defs/Cpc.cached.eo:5600` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `890491ff8a770b03` | logos | EO0054 | `install/defs/Cpc.cached.eo:5605` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `9210e4d67854e3dd` | logos | EO0054 | `install/defs/Cpc.cached.eo:6096` | this pattern matches an `+` of exactly 2 element(s) | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `2a7b67b48b4b3bd6` | ethos+logos | FUZ0001 | `tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-78c094/case.cpc:2` | ethos accepted what logos refused: Error parsing proof: Error: assumption after the first proof step: (assume @p0 (not (= (str.len (str.++ "\u{a}" "\u{6f}rd")) N))) | re-coded `FUZ0005` — the fuzzer now separates the two directions of a disagreement; the same reproducer is `4de9bb965fa0c04b` |
| `ece08559e3edd79c` | cvc5 | EO0054 | `proofs/eo/cpc/programs/Strings.eo:1749` | this pattern matches an `*` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `cab3113f257de9c1` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1166` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `129a0fcb766be9f6` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1245` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `9913cf82395ba38e` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1250` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `abcbd61aac94dc78` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1255` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `90a380b8bdf7cb18` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:1746` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `c9887e6df81fcdb6` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:399` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `0a12b85457baceb9` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:540` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `b450c58122dec907` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:732` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `92bcba9c5a9aff47` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:943` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `246cda4bed0fcdf4` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Rewrites.eo:948` | this pattern matches an `+` of exactly 2 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `3061a2d9ac0d7ab8` | cvc5 | EO0054 | `proofs/eo/cpc/rules/Strings.eo:306` | this pattern matches an `str.++` of exactly 3 element(s) | intentional — cvc5: the reported CPC occurrences are deliberate |
| `a3e3ef689c03095f` | ethos | EO0077 | `tests/sorry.eo:4` | rule `trust` is admitted: it is marked `:sorry` | intentional — cvc5: `trust` is deliberately `:sorry` and documented as making a proof incomplete |
| `befab5e954ae823b` | logos | EO0077 | `install/defs/Cpc.cached.eo:6636` | rule `trust` is admitted: it is marked `:sorry` | not audited — `install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the ground truth; keeping the two in step is a sync check (planned, in cvc5's CI) rather than a finding here |
| `bf7a06476186d7c5` | cvc5 | EO0077 | `proofs/eo/cpc/Cpc.eo:555` | rule `trust` is admitted: it is marked `:sorry` | intentional — cvc5: `trust` is deliberately `:sorry` and documented as making a proof incomplete |
| `adc98aa79b4861bb` | ethos+logos | FUZ0001 | `tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-49a2cf/case.cpc:2` | logos accepted what ethos refused: Error: <path>:N.N: Expected Eunoia command, got `_` (SYMBOL). | declined — logos: `declare-fun` in a proof file is deliberate and documented, because logos ignores `include` and `reference` and a proof must carry its own declarations; the symbol gets the type ethos would give it from a reference file, and cvc5's `eo` printer emits `declare-const`, so the divergence cannot arise on real output. Still reproduces, by design |
| `3e271ee47343e758` | ethos+logos | FUZ0001 | `tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ty-bbdf0a/case.cpc:2` | logos accepted what ethos refused: Error: <path>:N.N: Type checking failed: | withdrawn — our error: the reproducer was an artefact of the shrinker, which deleted the `_` from line 4 of a committed seed while ethos's refusal was decided on line 3. Reproducer removed from `tests/fuzz/` |
| `4de9bb965fa0c04b` | ethos+logos | FUZ0005 | `tests/fuzz/disagreement-ethos-accept-logos-reject-error-parsing-pro-78c094/case.cpc:2` | ethos accepted what logos refused: Error parsing proof: Error: assumption after the first proof step: (assume @p0 (not (= (str.len (str.++ "\u{a}" "\u{6f}rd")) N))) | declined — logos: a proof is read as an assumption set plus the steps that refute it, which is what its correctness theorem is stated over, so the refusal is the input format and not a parser gap; `docs/parser.md` now records it. Still reproduces, by design |
