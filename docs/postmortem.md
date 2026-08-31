# Postmortem log

A living log of what handling findings has taught anoieu about **its own
workflow**. One section per **iteration** — one run of the loop, one reply
worked — with the findings that changed how this repository works listed under
it: a check narrowed, the harness fixed, the report reshaped, a prompt
rewritten. Newest first.

**This is not where a finding is written up.** That is
[`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back), which
carries the reasoning, the commits and the evidence at whatever length they
need. Entries here are short and point there. The two files answer different
questions: *what happened to this finding* is the log in `reports.md`; *what
this run taught us about working findings* is here.

## The procedure

**Whose job.** The anoieu maintainer processing a reply — step 7 of prompt two in
[`reporting-workflow.md`](reporting-workflow.md#prompt-two-the-follow-up), which is
what [`scripts/process_anoieu`](../scripts/process_anoieu) runs. Not the project
that owns the finding: they send feedback, we decide what it changed here.

**When.** Every run, by default. The test an entry used to have to pass — did
processing this reply **change how anoieu works** — turned out to be the wrong
default: a round that changes nothing here is still a round whose *reasoning*
about why it changed nothing is worth having, and the judgement call cost more
than the entry.

    scripts/process_anoieu <project> [ID]              # an entry is written
    scripts/process_anoieu --no-postm <project> [ID]   # the agent decides

`--no-postm` restores the older behaviour for a run: the agent applies the test
above and says which way it went. A run that changed nothing here still writes
its `Resolution:`, and simply has no sections beneath it.

**The shape of an entry.** One heading per **run of anoieu** — one project, one
reply worked — and **one** `Tool:` / `Summary:` / `Resolution:` block under it,
describing the run. A run usually settles several findings; those are sections
beneath, and they carry detail rather than fields of their own.

```text
## <date> — <project>: <what this run was>

**Tool:** the project the findings were reported to. This is the repository name
passed to `scripts/process_anoieu`, so it is never a judgement call.

**Summary:** **what the nature of the findings was**, most important first —
what was actually wrong with the software, not what the exchange consisted of.
Written for somebody who does not work on either project: no codes, no ids, no
counts, no procedure. **Two sentences, 250 characters at most.**

**Resolution:** how it came out, as a breakdown — how many were real defects and
of what kind, how many were deliberate and declined, how many were ours to fix
— and what changed here as a result. Counts and links belong in this field, not
in the summary.

### <finding id, or a phrase for a group of them> — <what it was>

<What happened — only enough to make the resolution make sense.>

**Learned:** <the general fact, stated so it applies to the next finding rather
than to this one.>
```

`tests/run.py` enforces the shape: one field block per run, none on the sections
beneath it, and a summary inside the limit.

**Read the entries below before writing one.** They are the worked examples of
what a good report looks like here — how much detail a finding needs before its
resolution makes sense, how a summary reads when it describes the software
rather than the correspondence, and what a `Learned:` line is for. They also
show the two failure modes worth avoiding: an entry that restates
[`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) at
length, and one that records an outcome without saying what it changes for the
next finding.

Keep only text that makes clear **what happened** and **what the workflow
learned**. Everything else — the commits, the reproduction, the argument — goes
in [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) and is
linked. A finding settled on its merits with nothing changed here does not need
a section; say so in the run's `Resolution:`.

## Standing rules this log has produced

Stated in full in
[`reporting-workflow.md`](reporting-workflow.md#feedback-both-ways); listed here with
the entry that produced each, because a rule with no incident behind it is a
preference.

| rule | from |
| --- | --- |
| the outbound prompt asks for `FEEDBACK TO ANOIEU`, and the reply has a field for what was noticed but not acted on | the whole first round: everything we learned arrived as prose in a reply with nowhere to put it |
| every round leaves the prompts clearer, more actionable and shorter | the first revision grew both and had to be cut back twice |
| a prompt is procedural; technical detail is a link | 2026-08-31, `3e271ee47343e758` — a sentence inlined in the prompt had been untrue for as long as it had existed |
| a person approves every change to a prompt template | standing; a template that rewrote itself from its own experience drifts with nobody agreeing to the direction |
| the guardrails are never traded for brevity | standing: *fix nothing else*, *do not summarise other results*, *touch no issue tracker*, *leave everything staged* |
| a decline is confirmed explicitly, and an unconfirmed one is *cannot tell* | 2026-08-31, ethos — ten declined rows, all correct, none of which the maintainer had been asked to push back on |
| a postmortem entry is written every round, not only when something changed | 2026-08-31, ethos — the judgement call cost more than the entry, and a round that changes nothing still has reasoning worth keeping |
| a merge does not close a row; a maintainer's acceptance plus a commit on a named branch does | 2026-08-31, ethos — seven fixes held open on somebody else's review queue, which is not information about the finding |
| a shortcut taken for tempo leaves something mechanical behind that will notice | 2026-08-31, ethos — closing on a promise is the `fixed upstream` mistake on purpose, so it got a marker, an audit and a test |

## Where the workflow stands

Updated each round. This is the part to read if you want to know whether the loop
is paying for itself.

**What is working.** Re-measuring is exact and is one command each way —
`tools/run.py --pinned` for the checks, `tools.anoieu_fuzz verify` for the reproducers
— so *does this still hold* is a question with an answer rather than a judgement.
Moving a row is a two-line edit. The two labels, `TRIAGE:` and `HUMAN RESPONSE:`,
survived contact with a real reply and did the work they exist for. Naming the
escape hatch in advance — *the serious direction may still end with the reference
being stricter than the language requires* — is what let the far end decline a
row confidently instead of hedging.

**What changed most recently.** A merge is no longer what closes a row — a
maintainer's acceptance and a commit on a named branch are, and whether the
change reached anybody's default branch is now a separate pass,
`tools/landing.py`, asked of the commit rather than of the person. The loop got
faster and took on a debt to do it; the debt is the seven rows that pass
currently answers *not yet* for.

**What is hard, and it is all judgement.** Closing a row on the strength of a
persuasive paragraph: two of three substantive replies were correct on the merits
and one of them still could not be closed. Deciding scope, when a reply corrects
something belonging to a third project. And a finding that stops reproducing
looking like a fix when it is a bad reproducer. The ethos round added a fourth,
and it is the one that has cost the most: **a decline is accepted by default.**
Nineteen rows came back, seven fixed and ten declined, and it was the ten that
needed the process work — a fix has to survive somebody reading a diff, and a
"nothing needs doing" has to survive nobody saying anything.

**Outstanding.** Seven suggestions from the far end, none yet built, each a change
to what a finding *is* rather than a tidy-up — the first five in logos's words, in
`anoieu-dev-response.md` in that repository, and the last two from ethos. A
further thread, from this side:
the record is now edited mostly by an assistant, and what must stay true of it
after such an edit is planned — not built — in
[`notes.md`](notes.md#7a-maintenance-coherence--todo).

| what | why it matters | cost of not doing it |
| --- | --- | --- |
| warn when a closed row's finding is still reported at the pinned commits | a verdict is a claim about the world and nothing rechecks it | three rows sat closed on a fix that never landed |
| put the cross-corpus correspondence in the `notes` column mechanically | the twin is already computed here | sixteen rows and forty minutes of somebody matching text by hand |
| record the argv, checker version and signature revision with each promoted finding | the record is not self-contained enough to replay | the far end had to guess the invocation, and the guess turned out to matter |
| mark a `note` as a reading rather than a measurement | a hypothesis ships beside a measurement, indistinguishable | one confident, wrong note nearly produced a confident, wrong triage |
| keep the raw detail beside the portable one | bucketing erases what the reader needs | `<path>:N.N` hid which line the reference actually refused |
| a reverse include edge across the corpus | a row against a file something else includes should say so, and `EO0071` should not call it a signature | four of ethos's nineteen rows were one wrong word, and the maintainer spent most of the round reconstructing what each file was |
| resolve a name in the scope that binds it, everywhere | `EO0054` is narrowed; every other check that resolves a head through the flat table has the same hole | two rows against ethos claimed a program's own parameter was somebody else's n-ary operator |

**Prompt size, by round.** The rule is that these come down; the number is how it
is kept honest.

| round | prompt one | prompt two | what was removed to pay for additions |
| --- | ---: | ---: | --- |
| 1 (2026-08-31) | 60 → 54 | 39 → 63 | prompt one lost the inlined explanation of what each code means and how each is confirmed, which moved to the header of [`open-findings.md`](open-findings.md) where it can be maintained. Prompt two grew, and that is the honest number: it gained the postmortem step and its `--postm` alternative, the branch check, the closed-row scope rule, and the caveat on a reproducer that stops reproducing. It is the one number in this table going the wrong way. Next round's candidate for removal is step 4, which is procedure that could be a link |
| 2 (2026-08-31) | 54 → 56 | 63 → 63 | prompt one grew by two lines and nothing came out to pay for it, which is the second round running that the number has gone the wrong way. What it bought is the decline confirmation, and the trade offered against it — folding the two sentences on `HUMAN RESPONSE` into one — paid back only one line of the three. Prompt two is unchanged: making `--postm` the default swapped which side of the alternatives block is the default and cost nothing. Step 4 of prompt two is still the candidate for removal, and is now overdue |
| 3 (2026-08-31) | 56 → 59 | 63 → 67 | the branch workflow: prompt one gained a paragraph on branching, committing locally and pushing nothing, and a `WHAT THIS NEEDS FROM YOU` section that says what the maintainer has to do for a finding to settle. That was +9 before a tightening pass took 6 back — the landing-page pointer, the reply-file sentence, the standalone `HUMAN RESPONSE` note folded into the template line, and the handover section cut by a third. Prompt two gained the new closing rule and the marker a closed-before-landing row carries. **Three rounds, three increases**, and the pass above is the first time a round has cut anything without being asked to. Both prompts should be read end to end for removals before round 4 rather than trimmed at the edges again; step 4 of prompt two remains the named candidate and is now two rounds overdue |

---

---

## 2026-08-31 — ethos: nineteen rows, seven fixes, and a decline nobody signed

**Tool:** ethos

**Summary:** Ethos aborted with a C++ runtime error on a malformed type, and
three of its error paths reported without a file or a line. Its test signatures
also carried a mis-declared operator, an unreachable program case and a
docstring naming the wrong field.

**Resolution:** 7 of the 19 were real and are fixed on one commit —
[four in the signatures and three in the checker
itself](reports.md#ethos--the-checker-and-its-test-signatures), the latter all
the same shape: a message that never reached the `Error: <file>:<line>.<col>:`
convention everything else uses. Those 7 are **closed**. 2 were
[ours](#the-two-naryeo-rows--a-name-that-meant-two-things), a check reading a
program's parameter as somebody else's operator; the check is narrowed and has a
witness. 8 were deliberate and declined, and 2 the maintainer deliberately left
open; those 12 stay open, because the declines turned out to rest on
[silence](#ten-declines-and-none-of-them-pushed-back-on). Two rules changed
underneath this round rather than because of any one finding: a decline now has
to be [confirmed](#ten-declines-and-none-of-them-pushed-back-on) before it is
recorded, and a fix no longer has to be
[merged](#closing-on-a-promise-and-the-audit-that-pays-for-it) before its row
closes. Also here: `--postm` is on by default, and `EO0054` says which
declaration it read an attribute from.

### The two `Nary.eo` rows — a name that meant two things

Two rows said a pattern matched a `cons` of exactly two elements. `cons` was a
*parameter* of the enclosing program, and the `:right-assoc-nil` `cons` the
check had resolved it against was declared in a different file — the one that
`(include "Nary.eo")`s it, seven lines below the include, shadowed by the
parameter and not yet in existence when the program was parsed. Checking
`Nary.eo` on its own reports neither row.

`resolve_decl` reads one flat table per signature and has no notion of a local
scope; `_walk_pattern` had the parameter list in hand and never asked it. It now
returns as soon as a pattern's head is a name the parameter list binds.

**Learned:** a check that resolves a name must resolve it in the scope that
binds it, and the flat symbol table makes the wrong answer the easy one. The
same hole is open in any other check that resolves a head through
`resolve_decl` — narrowing one call site is not fixing the class.

### Ten declines, and none of them pushed back on

Every declined row in this reply was correct on the merits. What was missing was
anywhere for the maintainer to have *disagreed*: the assistant wrote "not a
defect", nobody objected, and the block was sent with the objection-shaped hole
still in it. Asked afterwards, he said he had not pushed back on any of them —
so the ten verdicts are his answers to a question that was never really put.

A proposed fix cannot fail this way, because somebody has to read a diff before
it lands. A proposed *decline* asks for nothing and gets it.

**Learned:** the two triage outcomes are not symmetric, and the process was
built as though they were. "Nothing needs doing" is the cheapest thing an
assistant can conclude and the hardest for a reviewer to notice they have
accepted, so it is the one that needs an explicit signature. None of the ten
rows is closed on this round's evidence.

### The reply said nothing was committed, and something was

The reply's header stated that its changes sat unstaged in the working tree. The
branch carried a commit and the tree was clean — the header described a state
the session had already moved past. It cost nothing, because the follow-up reads
the branch rather than the sentence.

**Learned:** the instruction to read the branch rather than the reply earned its
place on a round where the reply was wrong about the branch in the *safe*
direction. It will not always be the safe direction.

### What was fixed here, from the feedback

`EO0054` now names the declaration it took `:right-assoc-nil` from, which is the
one line that would have made the `Nary.eo` mismatch visible without an
experiment, and says "a `cons`" rather than "an `cons`".
[`fuzzing.md`](fuzzing.md#the-codes) now carries the fact that decides what
*fixed* means for every `FUZ` row — that ethos aborts on ordinary errors too, so
how a checker exits is not the finding — which was in `codes.py`, two hops from
the report, and which the maintainer called out as load-bearing for all three of
his `FUZ` verdicts.

**Learned:** the sentence that decides what "fixed" means belongs on the page a
reader lands on, not one link further in.

### What was not fixed, and why

`EO0071` told four rows that "this signature has no `declare-consts <numeral>`"
about a file that is an include fragment and is never checked on its own — we
check it standalone only because a corpus directory is one profile per file. The
check's judgement was right on all seven of its rows; the word *signature* was
not. Suppressing it needs to know that something else in the corpus includes the
file, and that reverse edge does not exist: `include_edges` runs forward from
the entry point and profiles are independent by construction.

**Learned:** a finding can be true of the file and false about what the file is,
and the second is the half a maintainer reads first. Four of nineteen rows were
that one word.

### Closing on a promise, and the audit that pays for it

The seven fixes sat closed-in-all-but-name for a day, on a rule that a change had
to be merged before its row could close. The maintainer's objection was about
tempo: waiting on a pull request measures somebody else's review queue, not the
finding, and while the checks are still moving that is the wrong thing to be
blocked on. A developer's word that the change will be merged now closes the row.

What that is, precisely, is the mistake this repository has already made once —
three cvc5 rows closed as *fixed upstream* on a fix that never landed, unnoticed
for three months because a closed id is one nothing re-derives — adopted on
purpose. So it is booked rather than assumed away. A row closed before its change
has landed ends its verdict with `awaiting landing: <project> <branch> <commit>`;
[`tools/landing.py`](../tools/landing.py) reads those back and asks each
project's checkout whether the commit has reached its default branch; and
`tests/run.py` fails if a verdict is reworded into a marker the audit cannot
parse, which is the only way a row could leave the audit while still owing it.

The condition that replaced *merged* is not *accepted*. It is **accepted, and
committed on a named branch** — which is what separates ethos's seven from
logos's `logos-2`, accepted two rounds ago and still open because the change has
only ever existed as a dirty working tree. That is the right answer for the right
reason: we can read a commit, and we cannot read an intention.

**Learned:** a shortcut that trades correctness for tempo is fine to take and not
fine to forget, and the difference between the two is whether something
mechanical is left behind that will notice. The rule changed in one sentence; the
audit, the marker and the test that guards it are what the sentence cost.

---

## 2026-08-31 — logos: the first full sweep

**Tool:** logos

**Summary:** Logos and Ethos disagreed about which proof files are valid, each
accepting proofs the other refuses. Logos's semantics also described an operator
its calculus does not define.

**Resolution:** 2 of the 20 were real defects in Logos — [a parser
bug](#3e271ee47343e758--a-reproducer-we-damaged-ourselves) and [a dead semantics
entry](#eac7ccd4d5fb0953--a-fix-that-had-not-landed) — both fixed, neither
merged yet. 2 were deliberate design choices, correctly
[declined](reports.md#logos--the-parser-and-the-semantics). The other
[16](#sixteen-rows-against-a-file-logos-does-not-write) were misfiled: they
describe cvc5's calculus, which Logos only vendors and cannot change. Two of the
faults turned out to be ours — the evidence behind the parser bug was wrong even
though the bug was real, so we withdrew that report; and Logos caught [three
findings we had recorded as fixed
upstream](#1d977d28576d3693-878038145dca690c-6cc91770c5491971--a-verdict-that-was-never-true)
that had never been fixed. What changed here: the fuzzer no longer damages the
files it borrows, settled verdicts moved out of the report into their own file,
both prompts were rewritten, and this log began.

### `3e271ee47343e758` — a reproducer we damaged ourselves

The case was one of logos's own regression tests, `test-indexed-op.cpc`, run as
a seed *as it stands*. logos accepted it, ethos refused it, and it was promoted
under a note blaming the missing `_` in `(( extract 1 0) a)`. logos narrowed a
parser that read any parenthesised head as a curried application, and the case
stopped reproducing — but their agent disbelieved our note and said so. It was
right: ethos had been refusing at **line 3** throughout, on the file's own
unmutated SMT-LIB spelling. Our shrinker had cut the `_` from line 4 and the
bucket held, because a bucket says nothing about *where* a refusal happened.
`shrink` now refuses to touch a seed run as it stands, with a guard in
`tests/fuzz_cases.py`. Detail in
[`reports.md`](reports.md#logos-4-the-indexed-operator-what-we-got-wrong).

**Learned:** we shipped a *hypothesis* — the note — inside the same record as a
*measurement* — the outcomes — with nothing marking which was which, and the
next reader nearly took it as given. And bucketing strips line numbers, which is
right for deciding whether two findings are one and wrong for what a reader is
shown: the stripped `N.N` is exactly what hid which line failed.

### `1d977d28576d3693`, `878038145dca690c`, `6cc91770c5491971` — a verdict that was never true

Nothing of ours found this. The assistant at the far end, checking whether the
copy it maintains would pick up a fix at the next bump, read what the copy is a
copy *of* and told us our own Closed table was wrong. It was worse than stale:
both programs declare `Int` at the commit the finding was reported against and
at the pinned tip, and they entered `programs/Strings.eo` already declaring
`Int`. The verdict was written from an assessment of the change we *proposed*,
never from the tree afterwards. Detail in
[`reports.md`](reports.md#cvc5-1-what-we-recorded-as-fixed).

**Learned:** the generator adds and never removes, which works — the hole is one
level in. A closed row correctly stays closed, but its *reason* is a claim about
the world that nothing rechecks, and `--pinned` re-derives open rows only. So a
wrong verdict and a live finding can coexist indefinitely with nothing red.
*Fixed upstream* is the one verdict this repository can settle by itself, from
`deps/`, and should never be recorded without doing so.

### Sixteen rows against a file logos does not write

`install/defs/Cpc.cached.eo` is a byte-exact copy of cvc5's signature, and our
checks filed what they found in it against logos. The rows cost nothing here and
a great deal at the far end: it read the file's
header, fetched cvc5 three times, matched premise text line by line, and only
then found that twelve of the sixteen were **already ruled on, against cvc5,
twenty lines further down the same document** — then wrote sixteen
near-identical blocks, correctly, because the prompt said each row gets its own.

**Learned:** the `notes` column is the highest-value field in the report and was
empty on all twenty rows, when *same source line as `c9887e6df81fcdb6` (cvc5,
closed: intentional)* was already computable here. The prompt also asserted the
rows were unrelated; sixteen of twenty shared one cause. It now says rows may
share a cause and to say so. The mechanical cross-reference is still not built.

### `eac7ccd4d5fb0953` — a fix that had not landed

`TRI0002` reported that logos's semantics declares an entry for a symbol CPC
does not declare. It was real: a target-vocabulary symbol given an input-side
entry by mistake,
and they proved it dead rather than merely unused by showing the generated Lean
byte-identical without it. The branch named in the reply was `main` with no
commits of its own, and the deletion was an uncommitted edit in one working
tree.

**Learned:** *"fixed on branch X"* is worth nothing until somebody looks at X,
and the looking takes ten seconds. Prompt two now says to compare the branch to
its base and read what is on it, and that a branch level with main, or a change
left uncommitted, is not a fix. This is the case the workflow's central claim —
the branch is the authority, not the reply — exists for.
