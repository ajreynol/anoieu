# Triage: what may change, and how it is written down

Static conventions, so the prompts in [`workflows.md`](workflows.md) can stay
short. Two things are fixed here: what an agent following up a response may do
to the findings report, and the shape of the write-up it leaves behind.

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
- **A finding that is no longer reported is not thereby closed.** It may only
  have moved, or a check may have been narrowed. Closing is a judgement about
  what happened, and it needs evidence — which is what the write-up is for.

## The write-up

One file per response. It exists so a maintainer can rule on what an agent
concluded without re-reading the trail themselves, and so that ruling has an
obvious place to go.

**One block per row, always these four labels, always in this order:**

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

`HUMAN RESPONSE:` is left **empty**. It is the space for the maintainer's
decision, and an agent filling it in — even with a suggestion — defeats the one
thing the file is for. It comes last so that reading a block top to bottom
arrives at the question rather than at an answer.

The three above it are claims of different kinds: what somebody else said, what
you checked, what you did. Keep them apart. Most of what goes wrong in a
follow-up is one of the three quietly wearing another's clothes.

Nothing reads these files, so name the file for the response and put it where
the review will find it. The only thing that has to be consistent is what is
inside.

## What happens to it

The maintainer fills in each `HUMAN RESPONSE:`, and what they write is what goes
into the ledger — where a finding's history is readable end to end. The write-up
is the draft of that entry, not a second record to keep in step with it.
