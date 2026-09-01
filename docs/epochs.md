# The epoch log

**One entry per epoch, newest first: what it carried, and the covering note we
recommended for handing it downstream.**

[`epoch-policy.md`](epoch-policy.md) is the policy — what an epoch is, what counts
as a major event, and what designing the next one involves. This file is only the
log.

**It has no obligation to be current.** It records what was recommended on a day.
Nothing compares it against anything, nothing consumes it, and **a prompt here
that has gone stale is not a defect** — it is a record of what we thought was
worth sending at the time, which is what a log is for. That is the opposite of
the discipline the prompts under [`../scripts/prompts/`](../scripts/prompts) are
held to, and the contrast is why it is stated here: those carry a copy of a
document, so a drifted copy is worse than none and `tests/run.py` fails when one
drifts. These carry nothing.

**Nothing here is an instruction.** Which repositories are contacted, when, in
what words, and whether at all is a person's decision — *Who gets pinged* in
[`policy.md`](policy.md#who-gets-pinged). A topic's `To:` says who it is addressed
to; it has never said who must be contacted, and neither does this page.

**It is not the announcement.** Those are topics in
[`discussion.md`](discussion.md), which is the record. This holds the covering
note somebody would paste when handing one over.

Five parts per entry, and the last is the one worth the space:

| part | what it holds |
| --- | --- |
| **Announcement** | the topic id in [`discussion.md`](discussion.md) |
| **Recommended for** | the repositories it was written for, and the footing they stood on at the time |
| **What it carried** | a few lines. The topic is the authority; this is the reminder |
| **The prompt** | verbatim, in a fenced block, so it can be pasted without editing |
| **What was rejected** | the wording considered and turned down, and why |

**The rejected wording is kept deliberately.** A prompt is short enough that the
reasoning behind it is invisible from the result, and the ways a covering note
goes wrong repeat. An entry carrying only the accepted version teaches nothing
the next person could not have guessed.

---

## E1 — through 2026-09-01

**Announcement:** [`D14`](discussion.md#d14--global-announcement-what-changed-this-week-and-the-one-thing-we-are-asking-of-everybody)
**Recommended for:** `dokimasia`, `eudaimonia`, `koine` — every member at the
time. Not `ethos` or `logos`, which were candidates held to none of it and whose
question was [`D11`](discussion.md#d11--we-have-a-footing-for-you-and-no-protocol-to-put-you-in-it).
**What it carried:** footings recorded on two axes instead of one; the
`associate` footing, defined and held by nobody; the `report/` convention and the
rule that a child project states whether there is a paper in it; `join_eo --soft`
in two forms; the rule that a prompt may not be for the repository it arrives in;
and the concept of a global announcement itself. One thing was owed — a
publishing stance — and everything else was notice.

**The prompt:**

```text
anoieu has opened D14, a global announcement, in its docs/discussion.md:

  https://github.com/ajreynol/anoieu/blob/main/docs/discussion.md

One thing is asked of you: state a publishing stance for your repository and for
each child project in your tree -- whether a paper exists for it, what the plan
is, or that there is nothing in it worth writing up. All three are answers and
the third is the commonest.

Everything else in D14 is notice and needs no reply.
```

The bare file URL rather than an anchor is deliberate and only works while `D14`
holds the pin, which puts it at the top of the file.

**What was rejected:**

> *See anoieu for a global announcement on how to improve your repo.*

Four reasons, and the first two are the ones that would have cost something.

**It misdescribes the announcement in the direction that flatters us.** `D14` is
one small ask, a set of notices, a list of our own failures and a question we are
putting to somebody else. Calling that *how to improve your repo* claims a
standing we had spent the epoch disclaiming — the footings are written as facts
about our arrangement rather than statuses conferred on theirs, and
[`../tools/ynoia/papers.md`](../tools/ynoia/papers.md) says in terms that where
the register disagrees with a repository about its own work, the repository is
right. It also lands badly from the tree that files findings against them, which
is the arrangement the governance proposal exists to undo.

**It names no topic, so the response gate stalls it.** Acting on another tool's
discussion file requires a human who named *which* topic. *A global announcement*
is not `D14`. A careful agent stops and asks, which is correct and still costs a
round; a careless one acts on notices that were marked as needing no reply.

**It drops the one thing that was owed**, which is the whole purpose of the
`Global:` field, and replaces it with an open invitation.

**And *see anoieu* is about thirty documents.** koine's `D1` was at that moment an
open complaint that joining had cost them four files and eighteen hundred lines
of reading. Answering it with a prompt of the same shape was free to avoid.

**Not recorded here:** whether it was ever sent, to whom, or what came back. Those
are the topic's business and a person's, not this page's.
