# Postmortem: one round of the reporting loop

An experience report, not a design document. One project — [logos](https://github.com/ajreynol/logos) —
was handed twenty open rows, answered every one, and sent back a reply; that
reply was then worked here. This is the log of what happened to each finding,
what each side got right and wrong, and what we changed as a result.

It is one sample of one repository. Everything in it should be read as *where
the effort actually went*, which is the only thing a workflow document can be
tuned against.

**The loop this is about.** A finding leaves here as a row. A person carries it
to the project that owns the file. An assistant there triages it, a maintainer
decides, and the reply comes back. An assistant here reads the reply, establishes
what actually happened, and rules on the row. Four hand-offs, two assistants, two
people, and at every hand-off something can be lost. The prompts on both sides are
in [`reporting-policy.md`](reporting-policy.md#the-workflow); this file is what
running them once taught us.

## The design principle this round established

**The prompt is the product, and the far end is the only thing that can tell you
what is wrong with it.** An assistant working a row in somebody else's repository
knows something nobody here does: which parts of the request were unanswerable,
which detail was missing, which sentence sent it in the wrong direction, and how
long each of those cost. That information used to leave with them. It now comes
back, because we ask for it — see *Feedback, both ways* below.

Three rules follow, and they are not optional decorations on the loop; they are
what stops it drifting.

1. **Every round makes the prompts clearer, more actionable and shorter to act
   on.** Not longer. Feedback naturally arrives as a list of things to add, and
   a prompt that grows every round ends as a document nobody finishes reading —
   which is exactly the failure it was meant to prevent. An addition has to earn
   its place, and usually something comes out to pay for it. The measure is not
   how much the prompt says; it is how quickly its reader can start work and how
   often it sends them somewhere useless.
2. **A prompt is procedural; technical detail is a link.** What to do, how to
   confirm before acting, what not to touch, how to report back — that is the
   prompt. What a code means, what a record holds, what the reply shape is for:
   those live in the docs. Detail restated in a prompt goes stale where nobody
   maintains it, which is what happened to a sentence claiming a `FUZ` row
   carried each checker's invocation. When a reader arrives unprepared, the fix
   is a better landing page — so the header of `open-findings.md` is now written
   for somebody who has just been handed a row.
3. **A person approves every change to a prompt template.** An assistant may
   draft one, argue for it, and show the diff. It may not adopt it. A prompt is
   the thing every future project is answered against, and a template that
   rewrote itself from its own experience would drift with no one having agreed
   to the direction. The scripts hold a copy and `tests/run.py` fails when it
   drifts from the document — that check is about accidental drift; this rule is
   about deliberate change.

None of this touches the guardrails. *Fix nothing else you notice*, *do not
summarise anoieu's other results*, *touch no issue tracker*, *leave everything
staged and commit nothing* — those stay written out in full, both ways, every
round. A shortening pass will reach for them first; they are four sentences and
they are what keeps an agent inside the scope somebody agreed to.

## The log

Nineteen blocks came back. Sixteen were one fact restated sixteen times; three
were substantive, and each went a different way. What follows is one entry per
outcome rather than one per row, because the sixteen are the story of the
sixteen.

---

### The sixteen rows against a generated file

**What we asked.** Sixteen rows against `install/defs/Cpc.cached.eo`, owned by
`logos`, under `EO0054`, `EO0064` and `EO0083`.

**How the agent behaved.** Correctly, and expensively. It read the file's header,
worked out that it is a byte-exact flattened copy of cvc5's CPC signature, fetched
cvc5 `main` to compare the lines character for character, and then discovered that
twelve of the sixteen were *already ruled on* in our own Closed table, against
cvc5, twenty lines further down the same document. It wrote sixteen blocks, one
per row, because the prompt said to and because answering sixteen rows with one
sentence is not doing the job.

**What we did.** Nothing to the rows: they were already closed here as *not
audited*, and the check no longer reads that file at all. The correct answer had
already been reached, on the same reasoning, before the reply arrived.

**What it cost, and whose fault that was.** Ours, entirely. We filed sixteen rows
we had already decided, made a maintainer re-derive the correspondence by hand,
and got back sixteen near-identical paragraphs for it. Two specific failures:

- **The `notes` column was empty on all twenty rows.** It is the highest-value
  field in the report and nothing had been written in it. A cell reading *same
  source line as `c9887e6df81fcdb6` (cvc5, closed: intentional)* would have
  turned forty minutes into a sentence. We compute a fingerprint for both sites
  and could say this mechanically.
- **A row against a generated file is filed against the wrong project.** The path
  is logos's; the content is cvc5's. Nothing in that file can change there
  without falsifying the pin.

---

### `eac7ccd4d5fb0953` — a semantics entry for a symbol CPC does not declare

**How the agent behaved.** Well, and this is the one it fixed. It found the entry
was a *target*-side symbol that had been given an input-side entry by mistake,
deleted it, and — the part worth copying — **proved the line was dead rather than
merely unused**, by running `install/install-cpc.sh --cached --check` and showing
the generated Lean byte-identical without it. It then declined to invent a
regression test, on the grounds that the only honest one would be a
re-implementation of the check that found it. It also volunteered that
`bump-eoc-version.py` copies the file wholesale from ethos and would put the line
back.

**How we responded.** We left the row **open**. The reply said "fixed on branch
`anoieu-findings`"; that branch is `main` at `d4a03a59` with no commits of its
own, and the deletion is an uncommitted edit in one working tree. The finding is
real, the fix is right, and nothing has landed.

**What this exercised.** The single most load-bearing sentence in the follow-up
prompt: *what happened will be settled by whether this branch is merged*. Without
it the honest-looking thing to do is close the row on the strength of a
convincing paragraph. With it, the check takes ten seconds and gives a different
answer.

---

### `adc98aa79b4861bb` — `declare-fun` in a proof file

**How the agent behaved.** It ran both checkers, said which builds, confirmed the
divergence, and then **declined the finding with a reason rather than a hedge**:
logos ignores `include` and `reference`, so a proof must carry its own
declarations; the symbol gets exactly the type ethos would give it from a
reference file; and cvc5's `eo` printer emits `declare-const`, so the divergence
cannot arise on real output. It went and checked that last point in cvc5's
printer source rather than asserting it.

**How we responded.** Closed as declined. The reasoning holds and needs no branch
to land.

**What made that possible** was a sentence in the prompt that names the escape
hatch in advance: *FUZ0001 is the serious direction, but the answer may still be
that the reference is stricter than the language requires.* Told which way a
finding leans and also that leaning is not a verdict, an assistant can say "not a
defect" without hedging. That sentence stays.

**What the agent pushed back on** was severity: the reproducer is one of their own
regression tests, unmutated, and the finding is that their input format is a
documented superset in one command — filed as an error. The severity is the
*direction*, not the attribution, which the policy says; the fact that it had to
be said in prose means the row has no field for it.

---

### `3e271ee47343e758` — the one we got wrong

**How the agent behaved: better than our record did.** It reproduced the case,
concluded logos was at fault, narrowed the parser, added guards, and checked them
against the executable. Then it did the thing that made this round worth having:
**it disbelieved the note on the row.** The record said *`( extract 1 0)` without
the `_`: logos reads it as the indexed operator, ethos does not.* The agent
observed that its ethos also refuses `((_ extract 1 0) a)` — the SMT-LIB spelling,
in a committed regression test — and said so, flagging that the recorded detail
named the wrong cause and that a second disagreement might be hiding behind it.

**How we responded.** We checked, and the agent was right. The reproducer was an
artefact of **our own shrinker**: the case was a seed run as it stands, ethos was
refusing at line 3, and `shrink` was therefore free to cut the `_` from line 4 —
the bucket held throughout because it says nothing about *where* a refusal
happened. The cut is exactly reproducible from the committed code. We promoted a
file nobody wrote, under a note describing the cut rather than the refusal, and
every later reader inherited it, including our own register and `fuzzing.md`.

We withdrew the row, removed the reproducer, and stopped `shrink` from touching a
seed run as it stands, with a case in `tests/fuzz_cases.py` that fails if the
guard goes away. Their parser fix is real and stands on its own.

**The general lesson is not about shrinking.** It is that we shipped a
*hypothesis* — the note — in the same object as a *measurement* — the recorded
outcomes — with nothing marking which was which. The agent nearly took it as
given, which would have produced a confident and wrong triage. `fuzzing.md` is
careful that a disagreement is not attributed to a checker, because that needs
semantics the fuzzer does not have. A note naming a *cause* is the same move one
level down and deserves the same care.

**Bucketing hid it.** The portable detail — `Error: <path>:N.N: Type checking
failed:` — is what a reader sees, and stripping `N.N` is precisely what concealed
that the failure was on the assume and not on the step. Keeping the raw detail
beside the portable one would have made the note visibly wrong at a glance.

---

### `4de9bb965fa0c04b` — an `assume` after the first `step`

**How the agent behaved.** It confirmed the divergence, established that the
refusal is deliberate — logos reads a proof as an assumption set plus the steps
that refute it, which is what its correctness theorem is stated over — documented
the restriction in `docs/parser.md` with regression guards, and then **asked to be
closed as documented rather than as fixed**, warning us that the reproducer will
keep reproducing. It also offered the alternative it had not taken (change the
command model instead) as a real option needing its own decision.

**How we responded.** Closed as declined and documented. That is a decision not
to change behaviour, and unlike the fix above it does not need a commit to be
somebody's.

---

### The correction we did not ask for, and the most valuable thing in the reply

While checking whether the generated copy would pick up a fix at the next bump,
the agent looked at what the copy is a copy *of* — and found that three rows we
had closed as **fixed upstream — both signatures now return Bool** were not
fixed. cvc5 `main` declares `Int` at those lines today.

We checked, and it is worse than stale. `$is_seq_const_rec` and `$is_seq_const`
declare `Int` at `622a50a3`, the commit the finding was reported against, and
have never declared anything else: they entered `programs/Strings.eo` already
declaring `Int`. The verdict was written from an assessment of the change we
*proposed*, never from the tree afterwards. The three findings are still reported
by the checks on every run; the only reason nobody saw them is that a closed id
is one the generator skips.

**This is the structural hole.** The report's asymmetry — the generator adds and
never removes — is well argued and does what it claims. The hole is one level in:
a closed row correctly stays closed, but its *reason* is a claim about the world
that nothing rechecks. A verdict of *fixed upstream* is the one kind this
repository can settle by itself, from `deps/`, and it was recorded without doing
so.

It was caught by a third party reading our own ledger, which is the argument for
publishing the ids.

## What it was like to work the reply, from this side

An honest account, because the follow-up prompt is tuned against it.

**What worked.** Re-measuring is one command and it is exact — `tools/run.py
--pinned` restores the recorded commits, so "does this still report" is a
question with an answer rather than a judgement. `anoieu_fuzz verify` is the same
thing for the other half, and pointing `$LOGOS` at a build made the difference
between reasoning about the fix and watching the case stop reproducing. Moving a
row is a two-line edit. Nothing about the mechanics was hard.

**What was hard, and it was all judgement.** Three things:

- **Closing on the strength of a good paragraph.** Two of the three substantive
  replies were persuasive and correct on the merits, and one of them still could
  not be closed, because the branch was empty. The prompt has to keep saying
  this; the pull toward "they said fixed, it reads fixed, close it" is strong.
- **Deciding what was in scope.** The reply's correction was about rows belonging
  to *cvc5*, already *closed*, that logos merely happened to notice. "Clean up
  those rows and no others" reads like it excludes them. It should not — a row
  the reply names is in scope whoever owns it and whatever state it is in — and
  the prompt did not say so.
- **A finding that stopped reproducing looked like a fix.** `anoieu_fuzz verify`
  reported `was accept, is reject` for the withdrawn row, which the prompt calls
  "the strongest evidence there is". It was evidence of something else entirely.
  The reproducer stopped reproducing for a reason other than the one recorded,
  which is the signature of a bad reproducer rather than of a fix.

**What I would have got wrong without the prompt.** Closed `eac7ccd4d5fb0953` on
the triage. Recorded the withdrawn row as fixed upstream. Both were the reading
the reply invited, and both are avoided by one instruction each.

## What we changed

Everything below is either done or explicitly not done, and the not-done ones say
why.

| change | why | state |
| --- | --- | --- |
| `shrink` no longer edits a seed run as it stands | the withdrawn row: for a file somebody else committed, the finding *is* the file | done, with a case in `tests/fuzz_cases.py` |
| the closed rows moved to [`closed-findings.md`](closed-findings.md) | the report is what another project is pointed at; the verdicts are bookkeeping | done |
| three cvc5 rows reopened, and the log corrected | *fixed upstream* was never true | done |
| both prompts revised | below | **drafted, pending approval** — see the measured cost at the end |
| the reply now has a place for feedback on the workflow itself | this file exists because of what came back in prose | done |
| put the cross-corpus correspondence in the `notes` column mechanically | sixteen rows, forty minutes, and it is already computable here | **not done** — needs a content fingerprint rather than path-and-line |
| let a corpus entry declare a path as derived, and attribute the row upstream | a row against a generated file is filed against the wrong project | **not done** — the checks already skip the file; the *report* still owns the ids |
| record the argv, the checker version and the signature revision with each promoted finding | the record was not self-contained enough to replay | **not done** — `verify` knows all of it at promotion time |
| mark a `note` as a reading rather than a measurement | shipping a hypothesis beside a measurement with nothing to tell them apart | **not done** |
| keep the raw detail beside the portable one | the portable form hid which line failed | **not done** |
| warn when a closed row's finding is still reported at the pinned commits | how *fixed upstream* survived three times | **not done** — the highest-value one left |

The five not-done items are the far end's own list, in its words, in
`anoieu-dev-response.md` in the logos repository. They are recorded here rather
than acted on because each is a change to what a finding *is*, and this file is
the argument for making them, not the making.

## Feedback, both ways

The prompt that goes out now ends by asking for exactly this: what was unclear,
what was missing, what the row should have carried, and what else would be worth
looking for. The prompt that comes back in now says to read it, act on the parts
about the report, and bring the parts about the prompt to a person.

**Why it is asked for explicitly rather than hoped for.** Everything above that
changed our tools came back as prose in a reply that had no field for it — the
severity objection, the wrong note, the stale verdict. It arrived because one
assistant chose to volunteer it and one maintainer chose to keep it. A loop that
depends on that is a loop that works once.

**Why it goes to a person.** Feedback about the report is data we can act on.
Feedback about the *prompt* is a proposal to change what every future project is
asked, and that is a decision somebody signs — see the two rules at the top.

**What this round's revision cost, measured.** Prompt one went **60 → 54 lines**
while gaining two template fields, the feedback section, and a scope
clarification — paid for by deleting the inlined explanation of what each code
means and how each is confirmed, which moved to the header of
`open-findings.md` where it can be maintained. Prompt two went **39 → 52**, and
that is the honest number: it gained a step it did not have (reading the
feedback), the branch check that would have caught this round's near-miss, and
the caveat on a reproducer that stops reproducing. It should come down next
round, and the candidate is step 4, which is procedure that could be a link.

Every round should be able to state these two numbers and what it removed. A
round that cannot has not finished.
