# Reporting policy

How a finding is handled from the moment a check reports it: the record it
goes into, the conventions that govern that record, the workflow for carrying it
to whoever can fix it, and what it takes for another repository to run these
checks itself. The position underneath all of it — what may be published about
somebody else's code at all — is [`philosophy.md`](philosophy.md).

Three parts, in the order you need them: the conventions, then the workflow that
uses them, then adoption.

## The conventions

Static conventions, so the prompts in [`reporting-policy.md`](reporting-policy.md#the-workflow) can stay
short. Two things are fixed here: what an agent following up a response may do
to the findings report, and the shape a reply takes coming back.

Neither is enforced by any tool, and both are expected to be followed exactly —
the whole purpose is that a maintainer can read a hundred of these without
learning a new layout each time.

**This is written to transfer.** Nothing below is really about anoieu: it is
about any analyzer that publishes findings against somebody else's files and has
to keep track of what came back. These are the mechanics;
[`philosophy.md`](philosophy.md) is the position they implement, and is shared
with [dokimasia](https://github.com/ajreynol/dokimasia) outright. A sibling tool
can adopt the conventions below by filling the same slots with its own files:

| the slot | what it is for | anoieu's |
| --- | --- | --- |
| **the report** | every finding currently reported, one row each, generated and additive | [`open-findings.md`](open-findings.md) |
| **the verdicts** | the internal half: every row that has been ruled on, and what was decided | [`closed-findings.md`](closed-findings.md) |
| **the id** | a fingerprint stable across edits elsewhere in the file, which everything else refers to | the check's code, the file, and the text of the line |
| **the catalogue** | what each check assumes, and therefore how it can be wrong | [`checks.md`](checks.md) |
| **re-measuring** | one command that restores the exact versions the report was measured against | `python3 tools/run.py --pinned` |
| **the regression** | where a case goes that would have prevented a wrong finding | `tests/witnesses/` |
| **the ledger** | the prose history of what was reported and what came of it | [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) |
| **the frame** | two labels separating what an assistant concluded from what a person decided | `TRIAGE:` and `HUMAN RESPONSE:`, below |

An analyzer missing one of those has a gap to close before the rest of this
means much. The two that carry the most weight are *the id*, because a decision
recorded against an unstable id is lost on the next run, and *re-measuring*,
because a follow-up that cannot reproduce the original finding is guessing.

### A finding from the fuzzer

The [anoieu fuzzer](fuzzing.md) fills the same slots, and differs in exactly one
of them — which is worth stating rather than leaving a reader to infer, because
it is the slot that carries the most weight.

| the slot | how the fuzzer fills it |
| --- | --- |
| **the report** | the same [`open-findings.md`](open-findings.md), under codes `FUZ0001`–`FUZ0005` |
| **the id** | the same fingerprint, over the committed reproducer rather than over somebody's signature |
| **the catalogue** | `python3 -m anoieu_fuzz explain FUZ0002`; five codes, one page each |
| **re-measuring** | **different.** `python3 -m anoieu_fuzz verify` replays every reproducer against a build of the checker and compares with what was recorded |
| **the regression** | `tests/fuzz/`, one directory per finding, beside `tests/witnesses/` |
| **the ledger** | the same [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) |
| **the frame** | the same two labels |

**Re-measuring is the difference and it changes what a run can promise.** A
check's finding is re-derived by running the check, so CI here re-derives every
one on every push, and a row that has gone stale shows up as a row nothing
reports. A fuzzer's finding cannot be: re-deriving it means running ethos or
logos, which the job that generates the report does not have. So the evidence is
the *reproducer*, committed, plus the verdicts recorded beside it — the same
arrangement as [`../tests/oracle.json`](../tests/oracle.json), written by a real
run and never by hand.

Three obligations follow, and they are on us rather than on anybody upstream.

1. **A candidate is not a finding.** A run writes to a scratch directory that is
   not checked in. Nothing there has a code, an id or a row until somebody reads
   it and runs `anoieu-fuzz promote`, and the first thing a run ever reported
   here was an artefact of the harness rather than a defect — a mutated
   `include` pointing at a file that had never existed.
2. **Confirm against a pinned build before filing.** A crash in whatever binary
   was on the machine that found it is not news. `tools/deps.lock` records the
   commit the rest of the report is measured against; a `FUZ` row filed upstream
   should have been reproduced against a build of it, and the row should say so.
3. **A disagreement has no owner until somebody gives it one.** The generated
   ledger files it against both checkers, because saying which of the two is
   wrong is precisely the judgement the fuzzer cannot make. What it *can* say is
   which direction the disagreement runs in, and that is the difference between
   `FUZ0001` and `FUZ0005`: accepting what the reference refuses is an error and
   refusing what it accepts is a warning. Severity is not attribution — the
   error may still turn out to be the reference's fault. Assigning it is a
   review step, and it happens in [`reports.md`](reports.md#the-register-what-anoieu-is-asking-and-of-whom) where a person signs for it.

Everything else — the reply format, the three prompts, what happens to a
decision — is unchanged. A `FUZ` row is followed up exactly like an `EO` one,
with the reproducer's path where a signature's path would be.

### The findings report

Two tables and one rule.

**The report**, [`open-findings.md`](open-findings.md) — every finding the checks
currently report, one row each, with an id, the project the file belongs to, the
check that reported it, where, what it said, and a **notes** column that no
generator ever writes to: anything in it was put there by hand and stays.

**The verdicts**, [`closed-findings.md`](closed-findings.md) — rows that have
been ruled on. The same columns, except the last is a *verdict* rather than
notes: what was decided, in a few words. It is **internal**: nobody outside is
asked to read it, and the report is what a project is pointed at.

Two files rather than two tables in one, because they are read by different
people for different reasons, and because a report whose second half is a
hundred rows of bookkeeping is a report people skim. The split has a cost that is
worth naming: the first project to work a full sweep of its rows found *twelve of
its sixteen answers* in the Closed table, by hand, because a row and its already-
settled twin were twenty lines apart. Moving the table further away makes that
worse unless the correspondence is in the `notes` column instead — which is where
it belonged in the first place. See
[`postmortem.md`](postmortem.md).

**The rule is that generation adds and never removes.** So:

- **Move a row; never delete one.** A deleted row is reported again on the next
  run, because the finding is still there to be found.
  [`closed-findings.md`](closed-findings.md) is the only thing that makes a
  verdict stick — generation skips any id already listed in either file.
- **Touch only the rows the response is about.** Not the ones next to them, not
  ones that look stale, not ones whose wording could be better. A tidying pass
  over rows nobody asked about is how a report quietly stops being trustworthy,
  and there is no way to tell afterwards which edits were considered.
- **Do not reformat, sort, or re-align anything.** The diff should read as a
  list of decisions.
- **Do not add a row by hand.** Generation does that, and a hand-written row has
  no fingerprint anybody can reproduce. Writing in the notes column of a row
  that is already there is the intended way to annotate one.
- **Never touch an issue tracker.** Not here, not anywhere: no opening, no
  commenting, no closing, no labelling, on this repository or on anybody's. An
  agent working under these conventions edits files and stops. Everything that
  reaches a person who did not ask for it is sent by a person.
- **A finding that is no longer reported is not thereby closed.** It may only
  have moved, or a check may have been narrowed. Closing is a judgement about
  what happened, and it needs evidence: the branch, and what the ledger records
  of it.

### The shape of a reply

One block per row, and one section at the end that is not about any row:

```text
## <id> — <check> — <path>:<line>

TRIAGE: triaged as fixed | not a defect | cannot tell, on branch <branch>,
pending review. What was changed, or why nothing was.

OBSERVED, NOT ACTED ON: optional. Anything true that was found and left alone.

HUMAN RESPONSE:

...

FEEDBACK TO ANOIEU

Where the time went; what a row should have carried; what in the prompt was
unclear or untrue; what else would be worth looking for.
```

**`TRIAGE:`** is what an assistant concluded — a reading made quickly, on
somebody else's word, sometimes without knowing what the file was for.
**`HUMAN RESPONSE:`** is what a person decided. Keeping them apart is the entire
point: when the two run together, a record ends up saying that something was
settled when what actually happened is that something was suggested.

`HUMAN RESPONSE:` comes last so that reading a block top to bottom arrives at
the question rather than at an answer, and a reply that carries only a triage is
a proposal rather than a result.

**A decline needs a signature, not an absence of objection.** The failure mode
is specific to *not a defect*: an assistant proposes that nothing needs doing,
nobody objects, and the silence is read back as agreement — where a proposed
*fix* would have had to survive somebody reading a diff. So prompt one now
requires the decline to be put to the maintainer in as many words and answered
before it is recorded, and an unconfirmed decline is reported as *cannot tell*.
On our side the consequence is the same either way: a row whose `HUMAN
RESPONSE:` records no explicit confirmation is not closed. This came from the
ethos maintainer, who noticed it about his own reply after sending it — ten
declines that were all correct and none of which he had pushed back on.

**`OBSERVED, NOT ACTED ON:`** is where a true thing goes that the row did not
ask about. *Fix nothing else you notice* is the right rule and it leaves nothing
to do with what you noticed; without a field, it either goes in prose or goes
nowhere. The first round produced three of these — a second checker disagreement
behind a reproducer, a documentation sentence two rows both undermined, and a
verdict of ours that was three months stale — and all three arrived only because
one assistant chose to write them down.

**`FEEDBACK TO ANOIEU`** is the loop closing, and it is the subject of the next
section.

#### When the human defers the field

The default is that an assistant leaves `HUMAN RESPONSE:` empty. But the person
in the session may hand it over — *you write it* — and an assistant should take
that rather than refuse it. What it must not do is let its own wording become
somebody's decision without them seeing it. So, having written it:

- **Quote the field back exactly.** The text itself, character for character,
  not a description of it and not a paraphrase. "I recorded that the fix was
  accepted" is not a confirmation; the lines you actually wrote are.
- **Say whose words they now are.** You are writing in their place and it will
  be read under their name.
- **Iterate until it is theirs.** Offer to change it, change it as often as
  asked, and quote it back each time. The field is finished when the person says
  it says what they mean, not when it reads well.

An assistant that writes the field and summarises it back has done the one thing
the shape exists to prevent.

### Feedback, both ways

**The prompt is the product, and the far end is the only place its defects are
visible.** An assistant working a row in somebody else's repository knows which
part of the request was unanswerable, which detail was missing, which sentence
sent it the wrong way, and what each of those cost. None of that is visible from
here. So the outbound prompt asks for it by name, under `FEEDBACK TO ANOIEU`,
and asks for one thing more: what *else* would be worth looking for — a check, a
mutation, a comparison — by somebody who has just spent a day on the output of
the ones that exist.

Four rules keep the loop from turning into drift.

1. **Every round makes the prompts clearer, more actionable and shorter to act
   on.** Feedback arrives as a list of things to add, and a prompt that grows
   every round ends as a document nobody finishes reading — which is the failure
   it exists to prevent. An addition has to earn its place and usually something
   comes out to pay for it. The measure is how fast its reader can start, and
   how often it sends them somewhere useless.
2. **A prompt is procedural. Technical detail is a link.** What to do, how to
   confirm before acting, what not to touch, how to report back — that is the
   prompt. What a code means, what a record contains, what the reply format is
   for: those live in the docs, and the prompt points at them. When a reader
   arrives unprepared, the fix is a better landing page, not a longer prompt.
3. **A person approves every change to a prompt template.** An assistant may
   draft one, argue for it and show the diff; it may not adopt it. A prompt is
   what every future project is answered against, and a template that rewrote
   itself from its own experience would drift with nobody having agreed to the
   direction. `tests/run.py` fails when the scripts drift from this document —
   that guards against accident; this rule guards against intent.
4. **Feedback about the report is acted on; feedback about the prompt is
   proposed.** The first is data. The second is a change to what everybody is
   asked, and goes to a person with the evidence attached.

Neither shortening nor linking touches the guardrails. *Fix nothing else you
notice*, *do not summarise anoieu's other results*, *touch no issue tracker*,
*leave everything staged and commit nothing* — those stay written out in full, in
every round, in both directions. They are what keep an agent inside the scope
somebody agreed to, and they cost four sentences.

What one round of this produced, in full, is
[`postmortem.md`](postmortem.md) — including the five suggestions we have not
acted on and why.

### The follow-up

An agent reading a reply *here* leaves three things and no more: the change to
the findings report, an entry in the ledger, and a reply in the session saying
what it did.

There is deliberately no write-up file and no field for a maintainer to sign.
The staged diff is already the review — every row moved, every note written,
every check narrowed is in it, beside the reasoning in the ledger — and a
document restating that would be a second record to keep in step with the first.
What the agent owes the session is the decisive action it took and why, not a
summary of the reply it read.

It should come back to the person it is working with in two cases only:

- **it disagrees with how the reply classified the resolution** — the reply says
  *fixed* and the branch does not bear that out, or says *not a defect* for a
  reason that does not hold;
- **it cannot tell whether the finding is resolved** — the branch is unmerged,
  the change does not touch what the row is about, or the trail runs out.

Both leave the row open, because both are the same fact: nobody knows yet. What
those cases need from a person is a decision, not a review, and asking for one
is cheaper than recording a guess.

### What happens to a decision

`HUMAN RESPONSE:` is what goes into the ledger — where a finding's history is
readable end to end. The reply is the draft of that entry, not a second record
to keep in step with it.


## The workflow

How to work a single finding with an assistant, from the report to whoever can
fix it and back. The arrangement is not specific to anoieu — the conventions it
rests on are set out separately, in [`reporting-policy.md`](reporting-policy.md#the-conventions), so that another
analyzer that reports findings against somebody else's files can adopt them by
substituting its own, and the position they implement is stated once, for both
tools, in [`philosophy.md`](philosophy.md). What is anoieu-specific here is
confined to the prompts — the tool's name, the report's URL, and a handful of paths and
commands — and to the right-hand column of the table on that page.

**Guidelines, not machinery.** Nothing in this repository files anything
anywhere: a finding travels because a person carries it, and comes back because
a person sends it. What follows is what we suggest that person do, and the two
prompts worth keeping around — one for the project that owns the finding, one
for the follow-up here.

It assumes an expert — somebody who knows the file being looked at. Nothing here
is a substitute for that.

### Who runs what

Running the checks needs no permission from anybody: the tool reads what you
point it at, writes nothing, and needs no network. Verifying a published report
is equally open — `tools/run.py --pinned --check` restores the recorded commits,
so the answer does not depend on who is asking.

Two things are ours: **regenerating the report**, which is a maintainer here
moving what it is measured against, and **closing a row**, which is a judgement
somebody signs. The generator cannot delete a row, so it can never be the thing
that closes one.

We do not control who runs the tool — it is public and reads whatever it is
handed. What we control is what is published *here* as a report, and the
top-level README says what CI checks about it rather than promising anything.

### A reply is somebody's triage, not the status

This is the part that is easy to get wrong, and the reason the prompts below are
worded the way they are.

An assistant working in cvc5 or ethos or logos can read a finding and propose a
change. It cannot settle anything. **The person on that project decides what to
say to us, and what they say describes their triage** — where their reading
landed, often under time pressure, on our word, sometimes without having written
the file in question.

So the authority on what happened is not the reply. It is **the branch**:
whether the change is merged, what review does to it, and what the commits that
follow it look like. A fix can be accepted and then quietly reverted; a decline
can be reversed by the next person to read the file; and the case we care about
most — our analysis being wrong — usually only becomes clear in review, when
somebody who knows what the file was for objects to the fix rather than to the
finding.

Which gives the rule for our side: **a reply opens a question here, it does not
close one.** Record the branch against the row, leave the row open, and go back
to the branch later to find out what actually happened — which is the whole job
of the second prompt. A row closed on a triage is a row closed on a guess, and
the log then reads as more settled than it is.

### Prompt one: in the project that owns the finding

Fixed text. The only things that change between uses are the branch and *which
rows* — one id, or every open row the project owns. It is written for whatever
assistant you already work with, run however you already run it. Paste it in a
checkout of the project the finding is about.

It deliberately says nothing about what kind of thing the finding is about. A
row may be about a signature, a semantics set, a configuration, an inconsistency
between two of them, or something anoieu learns to check next year, and a prompt
that named one of those would quietly narrow what the reader looks for.

**Two forms, and the difference is one line.** Naming an id addresses that
finding. Naming none sweeps every open row the project owns, one at a time —
which is what you want the first time a project is asked anything, and after a
long gap. The sweep form is not a bulk operation: each row still gets its own
verdict and its own paragraph, and an assistant that answers ten rows with one
sentence has not done the job.

**The prompt is procedural; the technical detail is a link away.** What it says
is what to do: which rows, confirm before you act, the three outcomes, the
guardrails, and how to report back. What a row *is*, how each code is confirmed,
and which page explains which — all of that is in the header of
[`open-findings.md`](open-findings.md), which is the one link the prompt opens
with and the page every other link hangs off. That header is written for somebody
who has just been handed a row and knows nothing else, and it is the place to
improve when a reader arrives unprepared.

Detail restated inside a prompt is detail that goes stale in a place nobody
maintains. The first round shipped a sentence claiming a `FUZ` row's notes
"carry the command each checker was given"; they carried nothing, the far end
lost time discovering it, and the sentence had been wrong for as long as it had
existed. A link cannot drift from the thing it points at.

**The guardrails stay, every round.** *Fix nothing else you notice*, *do not
summarise anoieu's other results*, *touch no issue tracker*, and — on the way
back — *leave everything staged, commit nothing*. These are the constraints that
keep an agent from turning a triage into a spree or a claim into somebody's
inbox, and they are the first thing a shortening pass will be tempted to cut.
They are not padding, and they are cheap: four sentences.

```text
anoieu is a static analyzer for the Eunoia languages. It has reported findings
against this project:

  https://github.com/ajreynol/anoieu/blob/main/docs/open-findings.md

Start there. That page says what a row is, how to confirm one for each code, and
links the page behind each code -- read the one page your row points at rather
than the catalogue behind it.

Address ID.
  -- or, for the sweep form --
Address every row whose owner names PROJECT, including a shared owner like
"ethos+logos". Work from the ids; that file is regenerated and rows move. Rows
may share a cause -- say so, and still rule on each in its own block. Answering
ten rows with one sentence is not doing this.

On branch BRANCH, one row at a time, and only what the rows name:

1. Decide whether it is real -- by reading the file, or by running the
   reproducer -- rather than by trusting the row. Some of what anoieu reports is
   wrong. Say which build you ran.
2. If it is real: make the smallest change that fixes it, and say in one
   sentence what a reader of that file, or a user of that program, would see
   differently.
3. If it is not, or you cannot tell: change nothing and say why. "I cannot tell"
   is the honest answer when you do not know what the file was meant to say.
   Then put the decline to the maintainer in as many words and wait for an
   answer -- not fixing something is a decision somebody signs, and silence is
   not a signature. Unconfirmed, it is "cannot tell", never "not a defect".

Fix nothing else you notice; each finding is reported separately. Do not
summarise anoieu's other results: a check that reports nothing is not evidence
that anything is right. Touch no issue tracker -- not ours, not yours, not
anybody's. Everything that reaches a person who did not ask for it is sent by a
person.

Then draft a reply for a maintainer to review and send, in anoieu-response.md at
the root of this repository, appending and leaving any block already there
alone. One block per row:

  ## ID -- <code> -- <what the row names>

  TRIAGE: fixed | not a defect | cannot tell, on branch BRANCH, pending review.
  <What you changed, or why you changed nothing.>

  OBSERVED, NOT ACTED ON: <optional -- anything true you found and left alone.>

  HUMAN RESPONSE:

Commit your work to the branch: that, not the reply, is what settles this. Leave
HUMAN RESPONSE empty; the report page links what to do if they hand it to you.

End with one section, FEEDBACK TO ANOIEU. It is asked for, and blunt is useful:
where the time went and what would have made it fast; what a row should have
carried, and anything here that was unclear or untrue; what else is worth
looking for that anoieu does not do.
```

### Prompt two: the follow-up, here

The reply from prompt one names a branch. That branch is the thing worth
reading, and reading it is a job in this repository rather than in theirs — so
the second prompt is for an assistant working in a checkout of **anoieu**, and
the only thing that changes between uses is a link.

The link can be to the branch, the pull request, or wherever the triage was
written down. It is a pointer to where the answer will be, not the answer.

What arrives is part assistant and part human — prompt one ends by handing its
draft to a maintainer, who reviews it, edits it and sends it — and telling those
apart is the one thing the prompt below spends words on. The rest of the job is
small on purpose: read the reply, work out what actually
happened, clean up **only the rows it is about**, and say what was done. There
is no write-up file and no second sign-off — the staged diff is the review, and
an agent that has moved three rows and narrowed a check has already shown its
work. What it may change, and the two cases where it should stop and ask, are in
[`reporting-policy.md`](reporting-policy.md#the-conventions) rather than in the prompt.

```text
A project we reported findings to has responded:

  LINK

TRIAGE: is an assistant's reading, made quickly and on our word. HUMAN RESPONSE:
is a maintainer's decision. Where they differ the decision counts, and a block
carrying only a triage is a proposal rather than a result.

Working in the anoieu repository, on the block about ID -- or, for the sweep
form, on every block, one at a time, leaving the record consistent after each so
that stopping partway is safe.

docs/reporting-policy.md is the authority on what you may change. The steps:

1. Find the rows the reply names, by id, in docs/open-findings.md and
   docs/closed-findings.md. A row is in scope because the reply names it --
   whoever owns it, closed or not. A reply disputing a verdict names a closed row.
2. Establish what actually happened, which is not what the triage predicted.
   - EO, DOC, TRI: re-check with `python3 tools/run.py --pinned`. It re-derives
     open rows only; a disputed closed row you check by reading deps/ yourself.
   - FUZ: re-run with `python3 -m anoieu_fuzz verify`, $ETHOS and $LOGOS pointed
     at builds. A finding that no longer reproduces is strong evidence -- but
     establish *why*: stopped reproducing for a reason other than the one on the
     row is a bad reproducer, not a fix, and never reproduced against their
     build is a third outcome again.
   - Look at the branch rather than taking it: compare it to its base and read
     what is on it. A branch level with main, or a change left uncommitted, is
     not a fix.
3. Clean up those rows and no others. Closing moves a row from
   docs/open-findings.md to docs/closed-findings.md with a verdict, never
   deleting it; reopening is the same move back, noting what the verdict missed.
4. If our analysis was wrong, fix what produced it rather than the row: narrow
   the check, add a witness under tests/witnesses/, and record the wrong
   assumption in docs/reports.md. A FUZ finding has no check to narrow -- what
   it may have is a reproducer that was an artefact of the harness, or a
   comparison that was never fair. Say which, remove the directory under
   tests/fuzz/, and ask whether the harness should have refused to report it.
5. Write what happened in docs/reports.md under the log, and update the
   project's section under the register if what we are asking has changed.
6. Read FEEDBACK TO ANOIEU and any OBSERVED, NOT ACTED ON. Act on what concerns
   the report or the tools. What concerns the prompts goes to docs/postmortem.md
   with its evidence and then to me: a person approves every prompt edit, and
   each round leaves them shorter and more procedural, so a proposal that adds
   says what it removes, and technical detail belongs in the docs a prompt links
   to rather than in the prompt.

7. Write a postmortem entry for this run, whether or not anything changed.
  -- or, with --no-postm --
7. Decide whether this earned a postmortem entry. It did if handling it changed
   how anoieu works -- a check, the harness, the report, a prompt. If nothing
   here changed, say so and write nothing.

   Entries go at the top of docs/postmortem.md, in the shape that file sets out
   -- short, and only what happened and what the workflow learned; the reasoning
   at length belongs in docs/reports.md. Update "Where the workflow stands" in
   the same file if this round changed what is outstanding.

Leave everything staged and commit nothing -- the diff is the review, and it is
mine to approve. Touch no issue tracker, here or anywhere. Say what you decided
and why: the action you took, not a summary of what you read. Come back to me
only if you disagree with how the reply classified the resolution, or cannot
tell whether the finding is resolved -- leave the row open and say what you
would need to know.
```

#### One way to run the two

[`scripts/check_anoieu`](../scripts/check_anoieu) and
[`scripts/process_anoieu`](../scripts/process_anoieu) are *an* implementation of
the two prompts above — a pair of shell scripts that hold the text with the
scope filled in, so that running one is a command rather than a paste. They are
not the workflow; the prompts are, and any other way of putting them in front of
an assistant is as good.

```bash
scripts/check_anoieu [ID]              # in a checkout of ethos, logos, cvc5 …
scripts/process_anoieu <project> [ID]  # here, once that project has replied
```

Naming a finding id addresses that one, and naming none sweeps. Everything else
they can do — running codex instead of claude, printing the prompt without
running anything, reporting what became of a branch, saying where each project
is checked out on this machine — is in `--help` and in the header of each file,
rather than here.

**The document is the authority.** The scripts hold a copy of the prompt text,
and `tests/run.py` fails when the copy has drifted from what is written above,
because the text above is what every project was promised.

### Prompt three: the sweep

The two prompts above each handle one finding. This one handles all of them: a
pass over every open row in [`open-findings.md`](open-findings.md), across every
project the manifest tracks, working out what has become of each. Run it rarely —
after a large upstream move, or before publishing a report — and expect it to
take a while.

Three things make it slow, and none of them can be skipped. It re-measures
against the *tips* rather than the recorded commits, so it moves what the report
is measured against. Establishing what became of a row usually means reading
history, and the clones are shallow, so history has to be fetched for whichever
project is being worked on. And the judgement is per row: fifty-odd of them, each
needing an answer that is not "it stopped being reported".

That last point is the whole risk. A sweep is where bulk-closing is tempting, and
where being wrong is cheapest to do and most expensive to discover — so the
prompt is built around refusing it. It is also written to be interrupted: rows
are handled one at a time and the record is left consistent after each, so
stopping halfway is safe and the next run picks up whatever is left.

```text
Bring the whole report up to date. This is a sweep over every open row in
docs/open-findings.md, across every project tools/deps.json tracks. It will take
a while. Work one row at a time and leave the record consistent after each, so
that stopping partway is safe.

Start by measuring the projects as they are now:

  python3 tools/run.py

That moves every clone to the tip of its ref and appends anything newly
reported. Rows it adds are new findings and are not this sweep's business. Rows
already listed that the checks no longer report are.

For each of those, work out what became of it. The clones are shallow, so fetch
history for the project you are looking at when you need it -- deepen it in
steps rather than fetching the whole thing. The answer is one of:

- the code changed. Find the commit that changed the line the row names and
  read it. If it fixed the finding, close the row with that commit as the
  verdict. If the construct simply went away for unrelated reasons, close it
  saying that instead -- those are different outcomes and only one of them is
  somebody having agreed with us.
- the finding moved. The same defect now sits at a different line or in a
  different file, and has been re-reported under a new id. Close the old row by
  pointing at the new one, and say they are the same finding.
- a check of ours changed -- narrowed, disabled or deleted. That is our doing,
  not theirs; close the row saying so. Then check the narrowing was deliberate:
  a check that quietly stopped reporting a real defect is a regression here, and
  matters more than any row in the table.
- you cannot tell. Leave the row open and note what you looked at. This is the
  expected answer for some of them, and an open row costs nothing.

Never close a row merely because it stopped being reported. That is not
evidence that anything was fixed, and a sweep is exactly where that mistake
gets made at scale.

Rows the checks still report need nothing unless something around them has gone
stale -- a file renamed, an owner now wrong. Fix those in place and leave the
rest alone.

When you finish, or when you stop:

- say how many rows you closed, how many you left open, and how many you could
  not settle;
- write it up in docs/reports.md, under the log, as one entry per project
  rather than one per row: a sweep is a single event and reads better as one;
- leave everything staged.

Come back to me if a check has stopped reporting something it should still
report, or if a project's entry in the manifest now points somewhere that no
longer exists.
```

#### Keeping the pair in step

The first two prompts are one contract seen from two sides: the first one's
output is the second one's input. If the reply's shape changes in one it has to change in the
other, and in [`reporting-policy.md`](reporting-policy.md#the-conventions), which is where the shape is actually
defined — all three or none.

This now spans repositories rather than files: another tool that adopts these
conventions has its own pair of prompts, and the shape they agree on is the same
shape. All of them move together or none does.

The failure is quiet, which is why it is worth saying: an agent asked to read a
format nobody produces any more will not stop, it will improvise. It will find
something in the trail that looks close enough, act on it, and report having
done so. Nothing errors, and the first sign of trouble is a row closed on a
misreading. Changing one prompt and not the other is the cheapest way to break
this workflow.

Neither prompt gives anybody a way to say that a file is clean — not the project
replying to us, and not the agent recording what came of it. The top-level README
explains why we do not accept that as a result, including from somebody offering
it in good faith.

### Medium term: issues, on our own repository

A table in a file is a poor place to hold a conversation. It has no threads, no
notifications, and no way for somebody who has not cloned the repository to
reply — so today a finding is discussed wherever the person carrying it happens
to be, and the ledger entry is written afterwards from whatever survived. The
intended fix is to give a finding a GitHub issue, and let the reply be a comment
on it.

Three constraints on that, worth writing down before anything is built:

**The issues live here, never on the project the finding is about.** An issue
filed in somebody else's tracker puts our claim in their queue, under our name,
where they have to dispose of it — and a wrong one is expensive for them to get
rid of. On our own tracker the same text is an invitation: they can ignore it,
argue with it, or link it from their own issue if they think it deserves one.
The asymmetry is the point, and it is the same reason nothing here files
anything anywhere today.

**A person posts, always.** The step from a file to a notification in somebody's
inbox is outward-facing and effectively irreversible, and it is not one an agent
should take on its own judgement — nor one it should hold the credential for.
What we would build is a script a maintainer runs over rows they have picked,
which opens an issue here for each and records its number against the row. One
command, deliberately, by the person whose name is on it. Reading the resulting
thread stays an agent's job; writing to it does not.

**Not yet.** Machinery that speaks on someone's behalf has to be right the first
time, and we are not at the point where the report changes often enough to need
it. The conventions above are built to survive the change rather than to be
replaced by it: a row is already the body of an issue, its id is already the key
an issue would be recorded against, and a reply is already shaped like the
comment that would answer one — `TRIAGE:` from an assistant, `HUMAN RESPONSE:`
from a person, in a thread instead of an email. Until then, the file is the
record.


## Running it in CI

The long-term goal is for ethos, logos and cvc5 to run this on every push. This
is how that should be arranged, and what has to be true before each step.

Two audiences, in that order: everything up to *Our own side of it* is for a
repository deciding to switch anoieu on, and what follows it is how this
repository generates the report in the first place.

### The model: one tool, three thin integrations

anoieu stays one repository and ships as one versioned package. Each repository
that uses it owns three things and nothing else:

| the repository owns | written as | why there |
| --- | --- | --- |
| which signatures it has | `entry_points` in `anoieu.json` | only that repository knows |
| what it has agreed to live with | a baseline file, committed | a record of decisions, reviewed like code |
| which checks it runs, and how loudly | `enable` / `disable` / `severity` | policy differs per repository |

Everything else — the checks, their severities by default, the manual pages —
lives here. A repository's CI job is then one line, and its policy is a file its
own reviewers can read.

**The inversion that makes this safe:** anoieu's own CI checks out cvc5 and
ethos at pinned refs and runs the analyzer over them against a baseline
committed *here* (`tests/corpus/cpc-baseline.json`). A change that invents a
false positive fails **anoieu's** build, before it can fail anyone else's. That
job is the reason downstream repositories can pin a version and forget about it.

### What each repository would check

| repository | entry points | what it buys |
| --- | --- | --- |
| **cvc5** | `proofs/eo/cpc/Cpc.eo`, `proofs/eo/cpc/expert/CpcExpert.eo` | the calculus everything downstream is built from; this is where the findings so far are |
| **ethos** | `tests/*.eo` | its test signatures are small, numerous and lightly exercised — the `<` `:right-assoc` bug lives in one of them |
| **logos** | `install/defs/Cpc.eo`, and `Cpc.eos` once the triple checks land | the flattened copies the Lean development is built from, and the semantics beside them |
| **eudaimonia** | whatever calculus a generated checker is for | the template's whole promise is that a new calculus compiles; this says so earlier |

Two exclusions worth stating: the compiler's `$MARKER$` templates under
`plugins/` are not signatures and will report as such, and generated artifacts
(`Cpc.cached.eo`) repeat whatever their source says, so checking both files
reports everything twice.

### The rollout ladder

Turning this on as a blocking check on day one fails the build on findings
nobody has triaged. Four steps, each safe to stop at:

**1. Report only.** Annotations appear on pull requests; nothing fails.

```yaml
- run: python3 -m anoieu check <entry points> --format github
  continue-on-error: true
```

**2. Baseline, and fail on new errors.** Record today, block tomorrow's:

```bash
python3 -m anoieu check <entry points> --baseline .anoieu-baseline.json --update-baseline
git add .anoieu-baseline.json
```

```yaml
- run: python3 -m anoieu check --baseline .anoieu-baseline.json
```

**3. Fail on new warnings too**, by adding `--deny-warnings`. Do this once the
first month of new findings has been all true positives.

**4. Burn the baseline down and delete it.** Each entry removed is a defect
fixed or a decision recorded as a suppression comment, which is better than a
line in a file because it sits where the decision applies:

```lisp
; anoieu: allow EO0054  matching exactly two children is what this rule is about
(($contains (or l xs) l) true)
```

A run reports how many findings its comments silenced, so this does not become a
way to lose track of them.

### Pinning

Each repository pins a version:

```yaml
- run: pip install anoieu==0.2.*
```

A new check then reaches a repository only when someone there bumps the pin,
which is the point: the analyzer's release cadence is not allowed to break other
people's builds. Versioning follows from that — a new check or a widened
existing one is a **minor** bump with a line in the release notes; a removal or
a renumbering is **major**; a fix that narrows a check is a **patch**, because it
can only reduce what a repository sees.

For a repository that would rather not take a PyPI dependency, anoieu is pure
Python with no dependencies of its own: a git submodule and `python3 -m anoieu`
works identically.

### Severity policy, per repository

The default severities are a claim about the language, not about anyone's
codebase, so a repository may re-pitch them. What we would suggest:

| family | default | cvc5 | ethos | logos |
| --- | --- | --- | --- | --- |
| correctness — `EO0040`–`EO0066` | error / warning | as-is | as-is | as-is |
| documentation — `DOC0010`–`DOC0012` | warning | as-is: the docstrings are a real convention there | `"disable"` — its tests are not documented that way | as-is |
| taste — `EO0054`, `EO0056`, `EO0060`, `DOC0001` | hint / off | on for review, not for CI | off | off |

```json
{
  "entry_points": ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
  "baseline": "proofs/eo/anoieu-baseline.json",
  "severity": {"EO0054": "hint"}
}
```

Put that at the repository root, or beside the signatures — discovery walks up
from the entry point — and the CI job becomes `python3 -m anoieu check`.

### What a job looks like

```yaml
name: signatures
on: [push, pull_request]
jobs:
  anoieu:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install anoieu==0.2.*
      - run: anoieu check --format github
      - run: anoieu check          # the same run, for the exit code
```

Two invocations because the annotation format prints no summary; a job that only
wants the exit code can drop the first.

For GitHub code scanning instead of inline annotations:

```yaml
      - run: anoieu check --format sarif > anoieu.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: anoieu.sarif }
```

### Costs

A whole-of-CPC run reads 51 files and finishes in well under a second, with no
build, no solver and no proof. There is nothing to cache and nothing to
parallelize; the job is dominated by fetching the sources, which is itself
about six megabytes across four shallow, sparse clones and a few seconds. A
repository checking its own signatures pays even less, because it has them
checked out already and fetches nothing.

### The order to do this in

1. **ethos first.** It is the smallest surface, its maintainers are the audience
   for the language findings, and its own test suite already holds one.
2. **cvc5 next, report-only**, so the three real findings get triaged with no
   pressure on the build.
3. **cvc5 blocking, with a baseline**, once those are resolved.
4. **logos last**, and after the triple checks land — which is the point at which
   anoieu says something logos cannot get anywhere else: whether the signature,
   the calculus semantics and the SMT semantics agree.

### One open question, worth deciding early

The triple checks (M4) need a signature *and* its `.eos` semantics, and those
live in different repositories: CPC's signature is in cvc5, its official
semantics in logos. Whichever repository runs that job needs both checked out.
logos already vendors ethos and consumes cvc5's signature, so it is the natural
home — which means the most valuable check anoieu will have runs in the
repository furthest from where its findings are usually fixed. Worth agreeing on
before it is built: either logos runs it and files issues against cvc5, or cvc5
grows a job that checks out logos for its semantics.

### Our own side of it

Everything above is for a repository adopting anoieu. The rest of this page is
how *this* repository produces the report those findings come from — separate
machinery, separate audience, and nothing an adopting repository has to run.

### The run

One command does the whole cycle:

```bash
python3 tools/run.py                   # move to each tip, then measure
python3 tools/run.py --pinned --check  # re-measure the recorded commits
python3 tools/run.py --offline         # measure whatever deps/ already holds
```

Three steps, each printing what it did:

1. **Sync.** Every project a report is about is cloned into `deps/` and moved to
   a commit. **Nothing reads a checkout anybody owns**, so a report is a
   property of named commits rather than of the machine that produced it.
2. **Measure.** [`corpus.md`](corpus.md), rewritten whole: the ref, commit and
   date of each project, and what the checks report on it.
   [`../tools/deps.lock`](../tools/deps.lock) records the same commits in full,
   for a machine. A finding is only true of a version, and the rows in the
   report carry none of their own.
3. **Findings.** [`open-findings.md`](open-findings.md), appended to.

#### Two different questions

Without `--pinned` a run asks **what is true of these projects now**. It moves
every clone to the tip of its ref, so it can turn up findings nobody has seen and
can change the counts. That is what produces a new report, and CI does it on a
schedule rather than on a push.

With `--pinned` it asks **do the recorded versions still report what the report
says**. It restores the commits in `deps.lock` exactly, so it depends on nothing
outside this repository: it goes red when a check changes what it reports, and
never because somebody upstream pushed. That is the one a push runs, and it is
what makes the corpus job a regression test rather than a news feed.

The distinction matters because the two failures deserve opposite responses. A
pinned failure is a bug in this tool, to be fixed before merging. An unpinned
failure is upstream moving — a diff to read and, quite possibly, findings to
file.

**Nothing is built.** The analysis reads signatures, semantics and configuration
as text, so the clones are shallow and sparse — one commit, and only the paths
each project's entry names — and need no toolchain. The whole of `deps/` is
about six megabytes and takes a few seconds to create. The one thing that does
need a built ethos is the differential oracle (`tests/run.py --oracle`), which is
a separate job.

What is read, and what is deliberately not, is [`tools/deps.json`](../tools/deps.json):

| project | ref | what we read | what we do not |
| --- | --- | --- | --- |
| **cvc5** | `main` | `proofs/eo` — the CPC signature and the expert extension | the solver, its build system, its proof-production code: whether cvc5 can *justify* what it decides is [dokimasia](https://github.com/ajreynol/dokimasia)'s question |
| **ethos** | `ethosEoc3` | the test signatures, `tools/eoc/semantics`, and the deep embedding | the C++ of the checker and the compiler |
| **logos** | `updateCompiler` | `install/defs` — the installed signature and the CPC semantics | the Lean development |
| **eudaimonia** | `main` | `examples/hello`, its own example calculus | `examples/cpc`, a vendored copy of cvc5's signature: reading it would report cvc5's findings under eudaimonia's name |

A ref in that file is a choice rather than a fact — it says which branch the
findings are about, and changing one changes what the report is a report of.

### Maintaining the report

Two files in `docs/` are generated, and the way they are maintained is the
medium-term plan rather than a stopgap.

[`corpus.md`](corpus.md) is versions and counts, rewritten whole by a run;
`--check` says whether it is current and CI runs that. A failure means upstream moved or a check changed what it reports, and the
diff says which.

[`open-findings.md`](open-findings.md) is the report itself, one row per
finding, and it is **additive**:

- **`tools/gen_open_findings.py` adds and never removes.** A row is keyed by the
  same fingerprint a baseline uses — the code, the file, and the text of the
  line — so it survives edits elsewhere in the file. CI runs `--check`, which
  fails when a finding is unlisted and never when a row is extra.
- **Closing is a separate step, and it is a judgement.** A finding leaves the
  open table when it is fixed upstream, declined, or shown to be our error. The
  row *moves* to [`closed-findings.md`](closed-findings.md) with a verdict
  rather than being deleted: deletion would not stick, because the finding is
  still there to be found and the next generation would list it again. That file
  is what makes the verdict durable — and, because nothing re-derives a closed
  row, it is also where a wrong verdict can sit unnoticed. A verdict that is a
  claim about somebody else's tree should say which commit it was checked at.
- **For now the review is an AI process under human supervision.** It takes a
  row, reads the current state of the file it is about, and either leaves it or
  moves it with a verdict — writing the reasoning into
  [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back), which is the prose half of the same ledger. Which
  rows are ready for that is [`reporting-policy.md`](reporting-policy.md#the-workflow)'s subject: a reply
  from a project is its triage, and the branch it names — not the reply — is
  what closes a row. What that review may change, and how it writes down what it
  did, is [`reporting-policy.md`](reporting-policy.md#the-conventions).
- **A finding that stops being reported is not evidence it was addressed.** It
  may have moved, or a check may have been narrowed. That is the whole reason
  the generator cannot delete.

The hand-written register in [`reports.md`](reports.md#the-register-what-anoieu-is-asking-and-of-whom) is the first pass at all of
this and is kept as the worked example of a curated report. The generated file is
where the mechanical half now lives.
