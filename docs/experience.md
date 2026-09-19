# Experience: what these projects did with what we found

Anoieu records observations about four projects it does not own — cvc5, ethos,
logos and eudaimonia. This page is the other half of that: **what each project
then did about one**, one section per change that closed an observation, newest
first.

**Why it exists.** A static analyzer and a differential fuzzer can produce
findings forever without any of them being worth producing. The one external
signal that a check points at something real is that somebody who did not run it
changed the code anyway. That signal is legible here, at a level somebody who
works on neither project can read. A check whose observations nothing ever closes
is measuring something nobody agrees is wrong, and that shows up here as silence.

**What is the record, and what is the story.** The record is
[`bug_db/`](../bug_db/README.md): the identity, the claim, the dates, and the
`closed_verdict` / `closed_why` / `closed_commit` fields a closure writes onto an
entry. The database says *that* a change closed an observation and which change
it was. This page says what it meant. An entry here without a closed identity
behind it is a story, and the database is what keeps it honest.

Commit and pull-request references link to the project they belong to, so a
reader can check any claim here against the diff without a checkout.

## Where this stands

**Read 2026-09-19.** 82 observations recorded, 68 ruled on, 14 still open: one
`EO0083` against cvc5, twelve against ethos (`EO0054`, `EO0071`, `EO0084`), and
one `FUZ0001` disagreement between ethos and logos. Seven ethos closures are
`accepted and fixed` on the branch `anoieu-findings` at
[`292201c2`](https://github.com/cvc5/ethos/commit/292201c2) and have **not
landed** on `main`; `python3 -m anoieu_analyzer.reporting.verdicts --check` is
what reads that debt back.

One change has closed anything. Three windows were read commit-first and in full:
cvc5, 35 commits, of which two touch the signature at all; ethos, the 7 commits
`main` has since a merge-base the recorded baseline is not on; logos, 5 commits.
Only cvc5 closed anything, and one commit did all of it. Twenty-three
observations carry a verdict migrated from the retired findings ledgers, with no
`closed_commit`, and so appear in no section below.

## The log

## 2026-09-19 — cvc5 [#12954](https://github.com/cvc5/cvc5/pull/12954) — the CPC signature's duplicate declarations, wrong return types and stale docstrings

**Commit:** [`e69f77df2027`](https://github.com/cvc5/cvc5/commit/e69f77df20279026da20218831a6c7b4703d731d) — Fix documentation and typing issues to Cpc.eo (#12954)

**Closed:** `deb8a1dbc6c6f079`, `79166e01d3bec111`, `2c740cb62dfc51b3`,
`852ee57154bcf6c4` (`EO0031`); `1d977d28576d3693`, `878038145dca690c`,
`6cc91770c5491971` (`EO0064`); `15dd9f5611325be2`, `946705a0916b7d39`,
`97e03d281eade336`, `dcd58a15ade5a630`, `49f2e4bd2c23568d`, `749c0a9f4fcfa766`,
`6d8e3eb5cafc93d4`, `734366e4de4d1648`, `fbc033a960a2aaa5`, `52912b691212cf81`,
`9810bf3bebb29000`, `f7d30b3481235f49`, `5b163f93e5077b90`, `abb6c825566b9322`
(`DOC0011`); `981948de279f158b`, `97999aad8798ca45`, `a1918d88fa051f11`,
`639aa3c1ad36dd73` (`DOC0012`)

**Summary:** Four constants in cvc5's proof calculus were declared twice over,
two of its programs claimed to return a number while returning a yes-or-no, and
eighteen rule descriptions listed the wrong inputs. All are now corrected.

**What the change did:** three unrelated repairs to the CPC signature, in one
pull request. The four virtual-term-substitution skolems —
`@arith_vts_delta`, `@arith_vts_delta_free`, `@arith_vts_infinity` and
`@arith_vts_infinity_free` — appeared twice in
`proofs/eo/cpc/expert/theories/ArithExt.eo`, a copy-pasted block at the end of
the file repeating one a few lines above it; the commit deletes the second
block, leaving one declaration each. `$is_seq_const_rec` and `$is_seq_const` in
`proofs/eo/cpc/programs/Strings.eo` returned `true` and `false` out of a
`:signature ((Seq T)) Int`; both now declare `Bool`. And eighteen docstrings
across ten files were brought back to their declarations, in three distinct
shapes: **pattern variables documented as arguments** (`$derivative` listed
`s1`, `s2` and `rr`; `$re_ac_merge` and `$re_concat_merge` listed `rr1` and
`rr2`; `$abconv_ubv_to_int_elim` listed `i` — every one a name from the
program's parameter list that its `:signature` never takes); **documentation
that had fallen behind** (`$substitute_simul_rec` had gained a `bvs` argument,
`$mk_dt_updater_elim_rhs` a `c`, `$re_rev_map_rev` an `acc` and
`string_decompose` a second premise, none written down, while
`arith_poly_norm`, `bv_poly_norm` and `quant_var_reordering` had been reshaped
to take a single equality and still documented the two sides separately); and
**a premise headed `; args:`** in `symm`, `not_implies_elim2` and `ite_elim2`,
one word wrong each, which is why each of those carried both a `DOC0011` and a
`DOC0012` observation. The commit touches twelve signature files and no C++.

**Not closed:** `7ca5c014646b8984`, the duplicate-rule observation against
`proofs/eo/cpc/rules/Rewrites.eo`. No commit in the window touches that file, and
`arith-eq-elim-int` and `arith-eq-elim-real` still stand at lines 94 and 90 with
the same arguments and the same conclusion.

**Attribution:** cites us. The commit message reads "Reported by anoieu,
https://github.com/ajreynol/anoieu", and records that logos was updated to match
in its PR #465 and that the work exposed a gap in logos's synchronization check,
fixed in its #466. No reply came back to us; cvc5 worked the rows and committed,
which is the stronger half of the evidence a reply was ever for.

**Learned:** the documentation checks were pointing exactly where they claimed,
and the thing that had held them up for three months was a *convention* rather
than a disagreement. An earlier round accepted these eighteen and deferred them
pending a decision about whether a program's pattern variables count as
documented arguments; cvc5 decided it the way `DOC0011` already reads — a
docstring documents the declared signature, not the parameter list — so the
check's contested assumption is now the project's stated one. Six of the
eighteen were that question; the rest were plain drift and three one-word slips,
which is a better ratio than the deferral implied. What would have made them
easier to act on is a sharper claim: `DOC0011` reports a count mismatch and does
not say which side is wrong or which items are the surplus, so cvc5 had to
re-derive per rule what we had already computed. A row naming *these items are
not in the signature* would have been actionable without deciding anything.
`symm` is worth naming twice — ethos made the identical `; args:` slip in its
own copy of the rule and fixed it independently, which is an argument for a
docstring check that no single row makes. `EO0064` says less about the check
than about us: it was right for three months while our own record had it closed
as fixed upstream on a change that never landed, and what corrected that is the
rule this page now runs on — close on a named commit, then re-read the source.

## What a run learned about itself

*What working a window taught us about how we work* — as against `Learned:`,
which is about the check that produced the observation. A window turns up facts
about our own tooling that belong to no pull request and so fit in no entry
above. Newest first, one line each; an empty section is the honest state when a
run turned up nothing.

**2026-09-19 — windows
[cvc5 `aee874240419..dbf176dfb71b`](https://github.com/cvc5/cvc5/compare/aee874240419...dbf176dfb71b),
[ethos `6beeb8e6..04a9b4d41508`](https://github.com/cvc5/ethos/compare/6beeb8e6...04a9b4d41508),
[logos `7ff136bb..c8165b2afd32`](https://github.com/ajreynol/logos/compare/7ff136bb...c8165b2afd32).**

- **Our own closure prompt sent the run to the wrong files.** Both
  `prompts/close_bug_db` and `bug_db/README.md` still directed a closure into the
  findings ledgers that had been deprecated the day before, so the run wrote
  those two files before being corrected. Both pages were rewritten on the same
  day and now describe the convention that ships: closure fields on the database
  entry, plus a section above. The general shape is that a workflow retired in
  one place keeps directing work from another until something compares them.
- **Every ethos observation is measured against a branch `main` does not
  contain.** The recorded baseline `6beeb8e6` is on `ethosEoc3`, 1344 commits off
  a merge-base of `8709609e4fad`, with seven commits of `main`'s own since. So
  the ethos half of the database can be neither closed nor refuted by reading
  `main` — the compare view says `diverged` rather than `ahead` if anybody looks.
  Thirteen observations are pinned that way. `config/deps.json` has since dropped
  the exception and watches `main`; moving the measurement takes a run, and
  `config/deps.lock` still records the branch it was measured on.
- **A closure was invisible in the browsing view.** The `bugs.md` generator
  rendered no `closed_*` field, so twenty-five closures changed the database and
  not one byte of the page readers are pointed at, which was *current* by
  `--check` the whole time. Both rendered views carry a status column as of
  2026-09-19, and the counts now say how many rows are open.
- **Eighteen rows waited three months on a convention, not on a disagreement.**
  cvc5 had accepted the documentation findings and deferred them pending a
  decision about whether a program's *pattern variables* count as documented
  arguments. When the decision came it went the way the check already read. The
  blocker was never whether the rows were right.
- **A reply is not evidence, and this is the second time that has cost us.**
  Four `EO0031` rows sat open for three months after a maintainer said they were
  fixed, because nobody re-read the tree; three `EO0064` rows sat *closed* for
  three months on a fix that never landed, for the same reason in the other
  direction. One commit-first pass settled both.

### Salvaged from the retired postmortem log

> [!NOTE]
> **The two rounds below were worked through a reporting workflow that no longer
> exists**, along with everything they name: the two findings ledgers, the
> `TRIAGE:` / `HUMAN RESPONSE:` reply shape, the `awaiting landing:` marker and
> the audit that read it, and the `check_anoieu` and `process_anoieu` prompts.
> They were a round of *correspondence* — rows sent to a project, a reply worked
> back here — which is not what a closure run does now. They are kept because
> the lessons outlived the machinery, and several of them are why the current
> arrangement is what it is. **Read them for what was learned, not for how
> anything works today.**

**2026-08-31 — ethos: nineteen rows, seven fixes, and a decline nobody signed.**
Seven were real and fixed on one commit, two were our own error, eight were
declined and two left undecided.

- **A check that resolves a name must resolve it in the scope that binds it**,
  and a flat symbol table makes the wrong answer the easy one. Two rows read a
  program's own `cons` *parameter* against a `:right-assoc-nil` `cons` declared
  by the file that includes it. `_walk_pattern` had the parameter list in hand
  and never asked it. Narrowing one call site did not fix the class: every other
  check that resolves a head through `resolve_decl` still has the hole.
- **The two triage outcomes are not symmetric, and the process was built as
  though they were.** Ten declined rows were all correct on the merits and none
  had been put to the maintainer in a way he could disagree with. A proposed
  *fix* cannot fail this way — somebody reads a diff. A proposed *decline* asks
  for nothing and gets it.
- **Read the branch, not the sentence.** The reply's header said its changes
  were uncommitted; the branch carried a commit and the tree was clean. It cost
  nothing that time because the error ran in the safe direction. It will not
  always.
- **The sentence that decides what *fixed* means belongs on the page a reader
  lands on**, not one link further in. That ethos aborts on ordinary errors too
  — so how a checker exits is not the finding — was load-bearing for three `FUZ`
  verdicts and was two hops from the report.
- **A finding can be true of the file and false about what the file is**, and
  the second half is the one a maintainer reads first. Four of the nineteen rows
  told an include fragment it was a signature. The judgement was right; the noun
  was not.
- **A shortcut traded for tempo is fine to take and not fine to forget**, and
  the difference is whether something mechanical is left behind that will
  notice. Closing before a change landed was the *fixed upstream* mistake
  adopted deliberately, so it got a marker, an audit and a test. That machinery
  is gone; the debt it tracked is now `awaiting_landing` on the database entry.

**2026-08-31 — logos: the first full sweep.** Two of twenty were real defects,
two were correctly declined, and sixteen were misfiled against a file logos only
vendors.

- **We shipped a hypothesis inside the same record as a measurement, with
  nothing marking which was which.** A promoted reproducer carried a note
  blaming a missing `_`; ethos had been refusing two lines earlier the whole
  time, on the file's own unmutated text, and our shrinker had made the cut the
  note described. Their agent disbelieved the note and was right. Bucketing also
  strips line numbers — correct for deciding whether two findings are one, wrong
  for what a reader is shown.
- **A closed row's *reason* is a claim about the world that nothing rechecks.**
  Re-measuring re-derives open rows only, so a wrong verdict and a live finding
  can coexist indefinitely with nothing going red. Three rows recorded as *fixed
  upstream* had never been fixed, and it was the assistant at the far end that
  caught it. A verdict this repository can settle by itself should never be
  recorded without doing so.
- **The cross-reference field was the highest-value one and was empty.** Twelve
  of sixteen rows were already ruled on against cvc5, twenty lines down the same
  document, and the far end found that only after fetching cvc5 three times and
  matching premise text by hand. It was computable here. Rows may share a cause,
  and saying so is most of the value.
- **"Fixed on branch X" is worth nothing until somebody looks at X**, and the
  looking takes ten seconds. The branch named in that reply was `main` with no
  commits of its own, and the fix was an uncommitted edit in one working tree.
  This is the case the commit-first rule exists for.

**The standing rules that log produced.** Four still bind and are why closure
works the way it does: *read the branch, not the reply*; *absence closes
nothing*; *a decline needs an explicit signature*; *a shortcut leaves something
mechanical behind that will notice*. The rest governed a correspondence loop
that no longer runs — the outbound prompt's feedback field, the reply shape, and
the rule that a person approves every prompt change — and went with it.

## How to maintain this page

**Who writes it.** [`prompts/close_bug_db`](../prompts/close_bug_db), in the same
run that writes the closure onto the database entry. It leaves this file and
`bug_db/bugs.json` changed and uncommitted for a maintainer to read as a diff. No
entry is written by hand, and none is written for a closure the database does not
carry.

**Three rules.**

1. **One section per change, not per observation.** The unit of what happened is
   the change; a section lists every identity it closed.
2. **A `FUZ` observation is not closable from here.** It is a claim about a
   program's behaviour, and reading a commit cannot falsify one — only
   `python3 -m anoieu_fuzz replay` against a build can. A commit that looks like
   the fix is a candidate for that replay and closes nothing, so it goes in the
   run notes rather than in a section.
3. **Attribution is recorded and is not the point.** Whether a project made the
   change because we reported it or found it themselves, the check was pointing
   at something real either way; only the first is also evidence that the
   *reporting* works. State which in one line and argue for no credit.

**Every entry has these fields, in this order.** Each project's remote is in
[`config/deps.json`](../anoieu_analyzer/reporting/config/deps.json); a commit
reference links to `<remote>/commit/<sha>` and a pull request to
`<remote>/pull/<n>`.

```text
## <date> — <project> [#<pr>](<remote>/pull/<pr>) — <what the change was>

**Commit:** [`<short sha>`](<remote>/commit/<full sha>) — <the commit subject>

**Closed:** <identity (code)>, <identity (code)>, …

**Summary:** what was actually wrong with the software, for somebody who works
on neither project: no identities, no check codes, no procedure. **Two
sentences, 250 characters at most.**

**What the change did:** the mechanism, at the level of the code somebody would
have had to read to write it. Long enough to be checkable against the diff.

**Not closed:** any observation this change was expected to close and did not,
with what was re-read to establish that. Omit the field when there is none.

**Attribution:** cites us | independent | cannot tell — and what that rests on.

**Learned:** what this says about the check that produced the observation —
whether it was pointing where we thought, what it over- or under-claimed, and
what would have made the row easier for the project to act on.
```

`Learned:` is what makes this a post-mortem rather than a changelog, and it is
the field a run drops first when a window is thin. A section without it records
that something happened and nothing about what to do differently.
