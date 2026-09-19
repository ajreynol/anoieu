# Experience: what these projects did with what we found

A living log of **the upstream changes that closed a recorded observation** —
one section per pull request, newest first, written in the same run that marks
the closure in [`bug_db/bugs.json`](../bug_db/bugs.json). anoieu watches four
projects, so an entry names which one; the unit is the change, not the project
and not the row.

**What it is for.** A static analyzer and a differential fuzzer can produce
findings forever without any of them being worth producing. The one external
signal that a check points at something real is that somebody who did not run it
changed the code anyway. This file is where that signal is legible: each entry
is a change a project made, said at a level somebody who works on neither
project can read, with what it says about the check underneath it. A check whose
observations nothing ever closes is a check measuring something nobody agrees is
wrong, and that shows up here as silence.

**Attribution is secondary, and recorded anyway.** Whether a project made the
change because we reported it or found it themselves, the observation is closed
either way and the check was pointing at something real either way. Only the
first is also evidence that the *reporting* works. So the field says which, in
one line, and nothing here argues for credit.

**This is not the record of the claim.** That is
[`bug_db/`](../bug_db/README.md): the identity, the original claim, the dates,
the evidence, and the `closed_on` / `closed_commit` / `closed_pr` / `closed_why`
fields a closure adds to an entry. The database says *that* a change closed an
observation and which change it was; this file says what it meant. An entry here
without a closed identity behind it is a story, and the database is what keeps
it honest.

**A `FUZ` observation is not closable from here.** It is a claim about a
program's behaviour, and reading a commit cannot falsify one — only
`python3 -m anoieu_fuzz replay` against a build can. A commit that looks like the
fix is a candidate for that replay and closes nothing on its own, so it gets a
line in the run notes below rather than an entry.

**Who writes it.** The closure pass — [`prompts/close_bug_db`](../prompts/close_bug_db)
— which reads a window of each project's history from the revision its open
observations were recorded at, and leaves this file and `bug_db/bugs.json`
changed and uncommitted. A maintainer reads the diff. No entry is written by
hand, and none is written for a closure the database does not carry.

## What a run learned about itself

*What did working this run teach us about how we work* — as against `Learned:`,
which is about the check that produced the observation. A window turns up facts
about our own tooling that belong to no pull request and so fit in no entry
below. They go here, newest first, one line each, and an empty section is the
honest state when a run turned up nothing. This is not
[`reports/postmortem.md`](reports/postmortem.md), which is one section per
*reply* worked through `prompts/process_anoieu` and has its own enforced shape.

**2026-09-19 — windows `aee874240419..dbf176dfb71b` (cvc5), `6beeb8e6..04a9b4d41508` (ethos), `7ff136bb..c8165b2afd32` (logos).**

- **Our own closure prompt writes the deprecated ledgers.**
  `prompts/close_bug_db` and the *Closure and the reporting transition* section
  of `bug_db/README.md` both direct a closure into
  `docs/reports/closed-findings.md` and `reports.md`, under a workflow whose own
  banner says **DEPRECATED as of 2026-09-18**. This run followed them and wrote
  the wrong two files before being corrected. The convention that is actually
  current — closure fields on the database entry plus an entry here — is the one
  the sibling tool ships and nothing in this repository describes.
  `maintenance.md` lists the migration as pending; the prompt is part of it.
- **Every ethos observation is measured against a branch `main` does not
  contain.** The recorded baseline `6beeb8e6` is on `ethosEoc3`, 1344 commits
  off a merge-base of `8709609e4fad`; `main` has seven commits of its own since.
  So the ethos half of the database cannot be closed *or* refuted by reading
  `main` — a window that looks like a history is a divergence, and the compare
  view says `diverged` rather than `ahead` if anybody looks. Thirteen
  observations are pinned this way.
- **A closure is invisible in the browsing view.** The `bugs.md` generator
  renders no `closed_*` field, so twenty-five closures changed the database and
  not one byte of the page anybody is pointed at. The view is *current* by
  `--check`, which is the whole of what CI asks of it.
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

## The shape of an entry

One section per pull request, whatever number of observations it closed, because
the unit of the thing that happened is the change and not the row.

```text
## <date> — <project> #<pr> — <what the change was>

**Commit:** <full sha> — <the commit subject>

**Closed:** <identity (code)>, <identity (code)>, …

**Summary:** what was actually wrong with the software, for somebody who works
on neither project: no identities, no check codes, no procedure. **Two
sentences, 250 characters at most.**

**What the change did:** the mechanism, at the level of the code somebody would
have had to read to write it. Long enough to be checkable against the diff.

**Attribution:** cites us | independent | cannot tell — and what that rests on.

**Learned:** what this says about the check that produced the observation —
whether it was pointing where we thought, what it over- or under-claimed, and
what would have made the row easier for the project to act on.
```

`Learned:` is the field that makes this a post-mortem rather than a changelog,
and it is the one a run drops first when a window is thin. A section without it
records that something happened and nothing about what to do differently.

## Where this stands

**Twenty-five observations closed, out of 60 recorded.** Three windows were read
commit-first and in full: cvc5, 35 commits, of which two touch the signature at
all; ethos, the 7 commits `main` has since a merge-base the recorded baseline is
not on; logos, 5 commits. Only cvc5 closed anything, and one commit did all of
it. The twenty-three observations closed in the deprecated ledgers before this
convention existed carry no `closed_*` fields and are not counted above.

## The log

## 2026-09-19 — cvc5 #12954 — the CPC signature's duplicate declarations, wrong return types and stale docstrings

**Commit:** `e69f77df20279026da20218831a6c7b4703d731d` — Fix documentation and typing issues to Cpc.eo (#12954)

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
It closed nothing for `7ca5c014646b8984`, the duplicate-rule observation against
`rules/Rewrites.eo` — that file is touched by no commit in the window, and
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
than about us: it was right for three months while our own ledger recorded it as
fixed upstream on a change that never landed, and what corrected that was the
rule this file now runs on — close on a named commit, then re-read the source.
