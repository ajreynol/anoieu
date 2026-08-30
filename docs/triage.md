# Triage: what may change, and how it is written down

Static conventions, so the prompts in [`workflows.md`](workflows.md) can stay
short. Two things are fixed here: what an agent following up a response may do
to the findings report, and the shape a reply takes coming back.

Neither is enforced by any tool, and both are expected to be followed exactly —
the whole purpose is that a maintainer can read a hundred of these without
learning a new layout each time.

**This is written to transfer.** Nothing below is really about anoieu: it is
about any analyzer that publishes findings against somebody else's files and has
to keep track of what came back. A sibling tool — [dokimasia](https://github.com/ajreynol/dokimasia),
say, which asks a different question about cvc5 — can adopt these conventions by
filling the same slots with its own files:

| the slot | what it is for | anoieu's |
| --- | --- | --- |
| **the report** | every finding currently reported, one row each, generated and additive | [`open-findings.md`](open-findings.md) |
| **the id** | a fingerprint stable across edits elsewhere in the file, which everything else refers to | the check's code, the file, and the text of the line |
| **the catalogue** | what each check assumes, and therefore how it can be wrong | [`checks.md`](checks.md) |
| **re-measuring** | one command that restores the exact versions the report was measured against | `python3 tools/run.py --pinned` |
| **the regression** | where a case goes that would have prevented a wrong finding | `tests/witnesses/` |
| **the ledger** | the prose history of what was reported and what came of it | [`upstream.md`](upstream.md) |
| **the frame** | two labels separating what an assistant concluded from what a person decided | `TRIAGE:` and `HUMAN RESPONSE:`, below |

An analyzer missing one of those has a gap to close before the rest of this
means much. The two that carry the most weight are *the id*, because a decision
recorded against an unstable id is lost on the next run, and *re-measuring*,
because a follow-up that cannot reproduce the original finding is guessing.

## The findings report

Two tables and one rule.

**Open** — every finding the checks currently report, one row each, with an id,
the project the file belongs to, the check that reported it, where, what it said,
and a **notes** column that no generator ever writes to: anything in it was put
there by hand and stays.

**Closed** — rows that have been ruled on. The same columns, except the last is a
*verdict* rather than notes: what was decided, in a few words.

**The rule is that generation adds and never removes.** So:

- **Move a row; never delete one.** A deleted row is reported again on the next
  run, because the finding is still there to be found. The Closed table is the
  only thing that makes a verdict stick — generation skips any id already listed
  in the file, in either table.
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

## The shape of a reply

What a project sends back has two labels, and the distinction between them is
the only formality anywhere in this workflow:

```text
## <id> — <check> — <path>:<line>

TRIAGE: triaged as fixed | not a defect | cannot tell, on branch <branch>,
pending review. What was changed, or why nothing was.

HUMAN RESPONSE:
```

**`TRIAGE:`** is what an assistant concluded — a reading made quickly, on
somebody else's word, sometimes without knowing what the file was for.
**`HUMAN RESPONSE:`** is what a person decided. Keeping them apart is the entire
point: when the two run together, a record ends up saying that something was
settled when what actually happened is that something was suggested.

`HUMAN RESPONSE:` comes last so that reading a block top to bottom arrives at
the question rather than at an answer, and a reply that carries only a triage is
a proposal rather than a result.

### When the human defers the field

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

## The follow-up

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

## What happens to a decision

`HUMAN RESPONSE:` is what goes into the ledger — where a finding's history is
readable end to end. The reply is the draft of that entry, not a second record
to keep in step with it.
