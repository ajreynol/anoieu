# Experience: every interaction we have had with the projects we watch

One entry per episode, oldest first, numbered `E1` upward. **An episode is
something that passed between this repository and a project it reports on** — an
observation that project closed, an ask it accepted or rejected, or a correction
it put to us. Each is self-contained and carries what we learned from it.

Anoieu points two tools at four projects — cvc5, ethos, logos and eudaimonia —
and an entry names which project and which producer. The static analyzer and the
fuzzer share this page because they share a bug database and a reporting
discipline, and because the interesting entries are the ones where both were
answered at once.

**A mistake of ours is an episode only when the project was the one to catch
it.** `E2` is here because we filed sixteen rows against a file logos does not
own and logos said so. A claim we caught ourselves, a check that broke because
somebody renamed something, a baseline that was typed rather than generated —
those are defects in the tool, and **they are not tracked in prose at all**: the
correction lands in the code and in a test, which is the only record that cannot
go stale. The test this page applies is whether **a maintainer of that project
spent attention on it**.

Ids are allocated above the highest ever used and are never reused. Nothing is
edited away: an entry that turns out wrong gains a later entry correcting it,
and both stay. Instructions for adding one are at the foot.

This is not the record of an observation — that is
[`bug_db/`](../bug_db/README.md), which holds identities, dates, evidence and the
`closed_*` fields a closure adds. What may be said about any of it is the
[reporting policy](../bug_db/reporting-policy.md).

**5 episodes so far: three led to landed fixes, and two exposed reporting
mistakes.** Three projects have merged something on the strength of what these
tools reported, and all three named us — two in the commit body, one in the pull
request's title. The other episodes are logos correcting our ownership claims
and ethos explaining why ten reports did not warrant changes. **33 observations
have been closed by a change that landed upstream**: 25 by cvc5, 7 by ethos,
1 by logos. Ethos accepted two more fixes in `E5`; those are committed on a
topic branch and are not included in that landed count.

## E1: logos removed a semantics entry for a rule it does not declare, and tightened its parser against a disagreement the fuzzer found

| | |
| --- | --- |
| **When** | 2026-08-31 |
| **Kind** | positive — the first change any project made on our evidence |
| **Ours** | `eac7ccd4d5fb0953` (`TRI0002`, static analyzer), and a `FUZ0001` disagreement from the differential fuzzer |
| **Theirs** | logos [#457](https://github.com/cvc5/logos/pull/457), [`6cb59db5`](https://github.com/cvc5/logos/commit/6cb59db508dcdd4ea00d359aa44ae7e787717a6b), titled *Initial findings from anoieu* |
| **Outcome** | closed. `TRI0002` is `fixed and landed`; the parser change is logos moving toward ethos of its own accord |

**What happened.** Two unrelated repairs in one pull request.
`install/defs/Cpc.eos` carried a semantics entry for `str.indexof_re_split`, a
rule the signature beside it never declares — the triple check compares a
signature against its calculus semantics and its SMT semantics, and that is the
disagreement it exists to find. The entry is gone. Separately, `parseTermCore` in
`Logos/Parser.lean` read a parenthesized application head as a curried
application; ethos refuses that, so the two checkers accepted different files.
logos now throws, and the comment it wrote beside the change is the finding in
its own words: *"Reading a parenthesized head as a curried application would
accept files Ethos refuses to parse."* The same pull request added to
`docs/parser.md` that every `assume` must stand before the first proof step,
*"where Ethos accepts one anywhere"*.

**What we learned.** A differential fuzzer does not find a bug; it finds a
**disagreement**, and which side is wrong is the project's to decide. Both
directions were decided here and they went opposite ways — the application head
moved logos toward ethos, and the `assume` ordering stayed as it was and got a
sentence of documentation instead. That second one is the row we carry as
`FUZ0005`, `declined`, and **a decline that produces a documented sentence is
worth as much as a fix**: the sentence is a fact about the input format that
nobody had written down, and we got it by reporting a disagreement we could not
adjudicate. What would have made both easier is a reproducer that says which
direction the disagreement runs in; the fuzzer only learned to separate the two
directions afterwards, which is why one row here is `re-coded`.

## E2: logos told us that sixteen of our twenty rows were against a file it only vendors

| | |
| --- | --- |
| **When** | 2026-08-31 |
| **Kind** | negative — our error, and they were the ones to catch it |
| **Ours** | 17 rows against `install/defs/Cpc.cached.eo`, now `not audited` |
| **Theirs** | logos, in reply to the first full sweep |
| **Outcome** | conceded. The rows keep their entries and carry a verdict saying the ground truth is elsewhere |

**What happened.** Our first sweep of logos reported twenty rows. Sixteen were
against `install/defs/Cpc.cached.eo`, which is a **copy of cvc5's `Cpc.eo`** that
logos vendors in order to check proofs without fetching it. logos is not the
authority for a line in that file and cannot fix one; cvc5 is, and twelve of the
sixteen were already ruled on against cvc5 twenty lines down the same document we
sent. The rows are closed `not audited` — *the finding is against a file whose
ground truth is elsewhere* — and keeping the two copies in step is a
synchronization check in cvc5's CI rather than a finding of ours.

**What we learned.** **A target is a claim about ownership, and ours was a
directory.** `config/targets.json` points the analyzer at logos's `install/defs`,
which holds both the semantics logos owns and a vendored copy of somebody else's
signature, and nothing in the configuration distinguishes them — so the sweep
reported every line in the directory as logos's to answer for. That is still true
today: the target is still the whole directory, and what stops a repeat is a
verdict written after the fact rather than anything that runs. The cheaper half
was missed too — the cross-reference was computable here and empty, so the far
end re-derived by hand what we already knew. **A row that names the wrong owner
costs more than a row that is simply wrong**: the second gets refuted in a minute,
and the first sends somebody to read a file they cannot change.

## E3: ethos gave four bad signatures a fix and three fatal aborts a diagnostic

| | |
| --- | --- |
| **When** | 2026-09-18, on work committed 2026-08-31 |
| **Kind** | positive — seven observations closed, from both producers, citing us |
| **Ours** | `b742c6d3a4fa9d74` (`DOC0011`), `d0b325c24c13892a` (`DOC0012`), `b4b49bbcd0bffd3a` (`EO0040`), `5c38f46b13406872` (`EO0052`) from the analyzer; `147433b3e48ae9d6` (`FUZ0002`) and `918dbdb5f068f46c`, `f419f6265e79b94b` (`FUZ0003`) from the fuzzer |
| **Theirs** | ethos [#241](https://github.com/cvc5/ethos/pull/241), [`39f2f90c`](https://github.com/cvc5/ethos/commit/39f2f90c0c93b7b71e327c3c8e524b9da039d45b), whose body reads *"Reported in an initial sweep by https://github.com/ajreynol/anoieu"* |
| **Outcome** | landed on `main`. The database still records all seven as `accepted and fixed` against the branch; moving them to `fixed and landed` is a person's |

**What happened.** The static half was three kinds of wrong in a signature:
`symm`'s docstring headed a premise `; args:`, which made the documented and the
declared counts disagree two ways at once; `<` was marked `:right-assoc` while
typed `(-> Int Int Bool)`, and a relation cannot fold, so the attribute is
removed; and a case of `isPermutation` was shadowed by the case above it and is
deleted. The fuzzer half was three inputs on which ethos died without saying
where — `(->)`, an unclosed `assume-push`, and a repeated `declare-consts`. Each
now reports through the parser with a position instead of aborting, and **each
arrived with a regression file in `tests/`**, which is the part we did not ask
for.

**What we learned.** The fuzzer's finding is not *ethos crashes*. It is *ethos
leaves the input without a position*, and the repair is a **diagnostic** rather
than a guard — which is why all three fixes are in the parser and none is a
bounds check. Stating the finding that way in the first place would have made it
easier to act on.

**And this is the episode that caught our own audit out.** The work was committed
to a branch on 2026-08-31, we closed the seven rows as `accepted and fixed`
naming that branch, and the pull request landed **squashed into a single new
commit** on 2026-09-18. `verdicts.py --check` asked whether the branch commit was
an ancestor of `main`, which it will never be, and so reported the debt as
outstanding for a change that had already landed. It asks by patch identity now,
and names the commit that carries the change. **An audit that can never clear an
item is one people stop reading**, and this one was wrong in the safe direction,
which is the harder kind to notice.

## E4: cvc5 corrected the CPC signature's duplicate declarations, wrong return types and stale docstrings

| | |
| --- | --- |
| **When** | 2026-09-18 |
| **Kind** | positive — 25 observations closed in one change, citing us |
| **Ours** | 25 identities under `EO0031`, `EO0064`, `DOC0011` and `DOC0012`, all from the analyzer |
| **Theirs** | cvc5 [#12954](https://github.com/cvc5/cvc5/pull/12954), [`e69f77df`](https://github.com/cvc5/cvc5/commit/e69f77df20279026da20218831a6c7b4703d731d), whose body reads *"Reported by anoieu, https://github.com/ajreynol/anoieu"* |
| **Outcome** | closed, `fixed and landed`. One row of ours was not closed and is still open |

**What happened.** Three unrelated repairs to the CPC signature in one pull
request, across twelve files and no C++. The four virtual-term-substitution
skolems — `@arith_vts_delta`, `@arith_vts_delta_free`, `@arith_vts_infinity` and
`@arith_vts_infinity_free` — appeared twice in
`proofs/eo/cpc/expert/theories/ArithExt.eo`, a copy-pasted block repeating one a
few lines above it; the second block is deleted. `$is_seq_const_rec` and
`$is_seq_const` in `proofs/eo/cpc/programs/Strings.eo` returned `true` and
`false` out of a `:signature ((Seq T)) Int`; both now declare `Bool`. And
eighteen docstrings across ten files were brought back to their declarations, in
three shapes: **pattern variables documented as arguments**, where a name from
the program's parameter list that its `:signature` never takes was listed as one;
**documentation that had fallen behind**, where a program had gained an argument
or been reshaped to take a single equality; and **a premise headed `; args:`** in
`symm`, `not_implies_elim2` and `ite_elim2`, one word wrong each, which is why
those carried both a `DOC0011` and a `DOC0012` row.

The change reached further than us. Its body records that logos was brought into
step in [#465](https://github.com/cvc5/logos/pull/465) and that the work exposed
a gap in logos's own synchronization check, fixed in
[#466](https://github.com/cvc5/logos/pull/466).

**Not closed.** `7ca5c014646b8984`, the duplicate-rule observation against
`proofs/eo/cpc/rules/Rewrites.eo`. No commit in the window touches that file, and
`arith-eq-elim-int` and `arith-eq-elim-real` still stand at lines 94 and 90 with
the same arguments and the same conclusion.

**What we learned.** The documentation checks were pointing exactly where they
claimed, and what had held them up for three months was a **convention rather
than a disagreement**: an earlier round accepted the eighteen and deferred them
pending a decision about whether a program's pattern variables count as
documented arguments. cvc5 decided it the way `DOC0011` already reads, so the
check's contested assumption is now the project's stated one. Six of the eighteen
were that question; the rest were plain drift and three one-word slips, a better
ratio than the deferral implied.

What would have made them easier to act on is a sharper claim. `DOC0011` reports
a **count mismatch** and does not say which side is wrong or which items are the
surplus, so cvc5 had to re-derive per rule what we had already computed. *These
items are not in the signature* would have been actionable without deciding
anything. And `symm` is worth naming twice: ethos made the identical `; args:`
slip in its own copy of the rule and fixed it independently in `E3`, which is an
argument for a docstring check that no single row makes.

`EO0064` says less about the check than about us. It was right for three months
while our own record had it closed as *fixed upstream* on a change that never
landed, and what corrected that is the rule this page now runs on: **close on a
named commit, then re-read the source.**

## E5: ethos accepted two literal declarations, rejected ten reports and assigned the parser disagreement to logos

| | |
| --- | --- |
| **When** | 2026-09-19 |
| **Kind** | negative — ten reports did not warrant changes to ethos; two fixes were accepted in direct response to our report and await landing |
| **Ours** | Analyzer: `52b5ae926f12d4c9`, `7f3eb81581c1f0a1`, `74c6f064da7c2464` (`EO0084`); `516184abdc82d1df`, `dcfaf1e214126aa3`, `f52484ca50c98a65` (`EO0054`); `42d486abefc2fc62`, `70fa22c05a9635d8`, `8dbf440aca48da0c`, `6b2263f824b28bd0`, `59e8abdd4478092d`, `584eda1d79a64b2c` (`EO0071`). Fuzzer: `9315026a26d2c2d0` (`FUZ0001`) |
| **Theirs** | Ethos's supplied `ethos-response-to-anoieu.md`, reviewed against main at [`04a9b4d4`](https://github.com/cvc5/ethos/commit/04a9b4d41508fb0282567c5ad47b35f67afd48f7); fix [`8d8e0288`](https://github.com/cvc5/ethos/commit/8d8e0288792da76a5ee66af11a4529c86386fc5b) on `anoieu-0919`, titled *Anoieu response* |
| **Outcome** | 12 static rows closed: 6 `intentional`, 4 `declined`, 2 `accepted and fixed` with landing debt. The fuzzer row stays open, reassigned from `ethos+logos` to `logos` |

**What happened.** Ethos reviewed all thirteen open observations addressed to
it and explained what the flagged files were meant to test. Three identity
rules are deliberate: one models cvc5's builtin calculus, and two let binder
tests observe whether the checker considers terms identical. The split test
deliberately recognizes exactly two disjuncts. Two singleton cases in
`Nary.eo` are also deliberate, and our check had additionally mistaken a local
`cons` parameter for an operator declared by an includer. These six carry the
owner's `intentional` verdict. The four `declined` rows belong to an include
fragment: [`eo-definitions-test.eo`](https://github.com/cvc5/ethos/blob/04a9b4d41508fb0282567c5ad47b35f67afd48f7/tests/eo-definitions-test.eo#L3)
declares the numeral category before including `eo-definitions.eo` at line 31.
Checking that entry point produces none of the four literal findings.

The two accepted rows concern a standalone test. The fix adds numeral and
string declarations to [`right-assoc-variants.eo`](https://github.com/cvc5/ethos/blob/8d8e0288792da76a5ee66af11a4529c86386fc5b/tests/right-assoc-variants.eo#L3),
giving its `0` and empty string their intended `Int` and `String` sorts.
Re-reading the committed file confirms both declarations; our analyzer no
longer reports either row, and the available ethos binary reports `correct`.
Ethos reports a 190/190 test pass; we did not rerun its full suite.

The response's summary says seven intentional findings, but its individual
rulings name six: **6 + 4 + 2 + 1 = 13**. We recorded those individual rulings.
Its fix section also leaves the commit blank and names `main`; the actual remote
refs put the fix on `anoieu-0919`, with `main` still at the reviewed revision.
The two database entries name that branch and full commit in `awaiting_landing`.
The earlier pending notes remain as history, superseded by these dated rulings.

**Not closed.** `9315026a26d2c2d0`: the
[reproducer](../tests/fuzz/disagreement-ethos-reject-logos-accept-error-path-n-n-ex-afbd92/case.cpc#L2)
wraps a command sequence in an extra pair of parentheses. Ethos explains that
the wrapper is not a Eunoia command, so its rejection is correct. The finding
remains `FUZ0001` under `logos`, with the same identity, reproducer and recorded
outcomes. The response calls this `re-coded`, but our vocabulary uses that
verdict to close a row carried under another code; no code changed here. We
updated ownership in both the database and the promoted case's metadata. This
was an ownership ruling, not a replay or evidence of a Logos fix.

**What we learned.** A test input's purpose is part of the claim. An identity
rule can be the instrument that tests equality, and a two-element pattern can be
the specification. Excluding every test would also hide the useful literal
findings in this same response; owners need a way to exclude paths from selected
signature-quality checks while retaining other checks. That remains follow-up
work, along with selecting actual entry points for directory sweeps. Our loader
already follows includes; the error was also treating the included fragment as
an independent signature. Suppressing every file with an unresolved symbol
would conceal real unresolved-symbol errors and is not a substitute for knowing
the entry points.

The literal check overstated its conclusion. In
[`TypeChecker::getLiteralTypeRuleMaybeInit`](https://github.com/cvc5/ethos/blob/04a9b4d41508fb0282567c5ad47b35f67afd48f7/src/type_checker.cpp#L63),
an undeclared category receives its builtin type. A numeral is therefore typed
as `<numeral>`, which can conflict with `Int`; it is not untyped. We corrected
the check's explanation and diagnostic label. The accepted change improves the
test's intended sorts, but does not establish that the old file was ill-typed.

Several requested repairs need a more precise diagnosis. `EO0054` already
requires a nil-terminator declaration, skips parameter-bound heads and chooses
its article; its shadowing witness covers the old `Nary.eo` error. The difference
between `conclusion-spec.eo:7` and `:8` is visible before report deduplication:
the check only flags a bare parameter in the tail position, which is `F` on
line 8 but the compound `(not F)` on line 7. Coverage of compound fixed tails
remains a question for the check. Our fuzzer already treats an `Error:`
diagnostic followed by `SIGABRT` as rejection; preventing core dumps remains
separate harness work. Finally, the configured ethos target is now `main`, but
the old observations retain their original `found_at` on `ethosEoc3`. Future
evidence should record the branch alongside the commit, rather than asking a
recipient to reconstruct that context.

## How this page is maintained

**Who writes it.** [`prompts/close_bug_db`](../prompts/close_bug_db), which reads
a window of each project's history from the revision its open observations were
recorded at, and leaves this file and `bug_db/bugs.json` changed and uncommitted.
A maintainer reads the diff. No entry is written by hand, and none is written for
a closure the database does not carry.

**When an episode earns an entry.** One test, and it is about them rather than
about us: **a maintainer of that project spent attention on it.** They merged,
rejected or acted on something of ours, or they put a correction to us.

What is *not* an episode, with where each belongs instead:

| not an episode | why | where it goes |
| --- | --- | --- |
| a claim of ours we caught ourselves | nobody there saw it | nowhere in prose — the corrected tool and its test are the record |
| a check of ours broken by somebody's rename | they renamed their own tree; we broke unaided | [`history.md`](history.md), where a run's own lessons go |
| a branch of theirs that has not landed | the decision has not been taken | nowhere yet. It earns an entry when it lands, and `verdicts.py --check` is what watches for that |
| a check that found nothing | that is a result, not an interaction | [`bug_db/corpus.md`](../bug_db/corpus.md) |
| an observation nobody has ruled on | nothing has happened to it | the database, as `open` |

**The bar is deliberately high, and the page is short because of it.** A log
padded with our own corrections reads as activity and measures nothing; the count
of entries here is meant to be the count of times this repository was worth
somebody else's time. The one exception is a mistake **they** caught — that cost
them attention, so it counts, and `E2` is the first of them.

**The template.** Copy it exactly. The next id is one above the highest ever
used, including entries later corrected; ids are never reused, and an entry is
never deleted or rewritten to say something else — a later entry corrects it and
names the earlier one by id.

```text
## E<n>: <what the project did, as a sentence with the project as its subject>

| | |
| --- | --- |
| **When** | the date it landed, or the date the exchange happened |
| **Kind** | positive or negative, and in a few words why |
| **Ours** | the identities, their codes, and which producer found them |
| **Theirs** | the project, and the pull request or commit, linked |
| **Outcome** | what state it is in now |

**What happened.** The episode, for somebody who works on neither project: no
check codes in the first sentence, and enough of the mechanism that a reader
could go and check it. Name the commit or the file.

**Not closed.** Any observation the change was expected to close and did not,
with what was re-read to establish that. Omit the field when there is none.

**What we learned.** What this says about the check, the report or the judgement
behind it — what it over- or under-claimed, and what would have caught it
sooner. **This field is why the page exists.** An entry without it records that
something happened and nothing about what to do differently.
```

Each project's remote is in
[`config/deps.json`](../anoieu_analyzer/reporting/config/deps.json); a commit
link is that remote followed by `/commit/` and the full sha, and a pull request
by `/pull/` and the number. A reader checking a claim here against the diff
should not need a checkout.

**Two rules that keep it honest.** Attribution is recorded and never argued:
whether a project made a change because we reported it or found it
independently, the check was pointing at something real either way, and only the
first is also evidence that the *reporting* works. And a closure is a decision
about **their change**, never about a row going quiet — absence closes nothing,
and the claim has to be re-read in their current source rather than taken from a
commit message. `tests/run.py` compares the field list above with the prompt that
writes an entry; what a verdict may say is [Closure](../bug_db/README.md#closure).
