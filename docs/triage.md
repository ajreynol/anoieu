# Triage: what may change, and how it is written down

Static conventions, so the prompts in [`workflows.md`](workflows.md) can stay
short. Two things are fixed here: what an agent following up a response may do
to the findings report, and the shape everything written by hand takes — in both
directions, going out and coming back.

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
  what happened, and it needs evidence — which is what the write-up is for.

## The shape

Both directions use the same frame, and the frame is two labels:

```text
TRIAGE: ...

HUMAN RESPONSE:
```

**`TRIAGE:`** is what an assistant concluded. **`HUMAN RESPONSE:`** is what a
person decided. Keeping them apart is the entire point: a triage is a reading
made quickly, on somebody else's word, and a decision is not. When the two are
run together, a record ends up saying that something was settled when what
actually happened is that something was suggested.

`HUMAN RESPONSE:` comes last, always, so that reading a block top to bottom
arrives at the question rather than at an answer.

### A reply to a finding

What a project sends back uses the frame as it stands, one block per finding:

```text
## <id> — <check> — <path>:<line>

TRIAGE: triaged as fixed | not a defect | cannot tell, on branch <branch>,
pending review. What was changed, or why nothing was.

HUMAN RESPONSE:
```

### A follow-up write-up

What an agent here writes after reading a reply uses the same frame with two
more labels inside it, because it is reporting on work of its own:

```text
## <id> — <check> — <path>:<line>

TRIAGE: what came back, and from whom. Distinguish the assistant's draft from
the maintainer's own words wherever they differ, because they are worth
different amounts.

FOUND: what you established yourself. The re-check at the recorded version,
what the branch did in the end — merged, reworked, reverted, still open — and
anything you could not settle, named as unsettled rather than rounded off.

REPORT: what you changed in the report for this row, in one line. If you
changed nothing, say that.

HUMAN RESPONSE:
```

`TRIAGE`, `FOUND` and `REPORT` are claims of three different kinds: what
somebody else said, what you checked, what you did. Keep them apart. Most of
what goes wrong in a follow-up is one of the three quietly wearing another's
clothes.

One file per reply. It exists so a maintainer can rule on what an agent
concluded without re-reading the trail themselves, and so that ruling has an
obvious place to go. Nothing reads these files, so name one for the reply it is
about and put it where the review will find it. The only thing that has to be
consistent is what is inside.

### When the human defers the field

The default is that an agent leaves `HUMAN RESPONSE:` empty. But the person in
the session may hand it over — *you write it* — and an agent should take that
rather than refuse it. What it must not do is let its own wording become
somebody's decision without them seeing it. So, having written it:

- **Quote the field back exactly.** The text itself, character for character,
  not a description of it and not a paraphrase. "I recorded that the fix was
  accepted" is not a confirmation; the four lines you actually wrote are.
- **Say whose words they now are.** You are writing in their place and it will
  be read under their name.
- **Iterate until it is theirs.** Offer to change it, change it as often as
  asked, and quote it back each time. The field is finished when the person
  says it says what they mean, not when it reads well.

An agent that writes the field and summarizes it has done the one thing the
frame exists to prevent.

## What happens to it

The maintainer fills in each `HUMAN RESPONSE:`, and what they write is what goes
into the ledger — where a finding's history is readable end to end. The write-up
is the draft of that entry, not a second record to keep in step with it.
