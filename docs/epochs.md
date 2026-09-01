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

Seven parts per entry, and the last is the one worth the space:

| part | what it holds |
| --- | --- |
| **Announcement** | the topic id or ids in [`discussion.md`](discussion.md) |
| **At** | the commit this epoch is adopted at, and whether our CI was green there |
| **Involved** | every tool the epoch actually touched, and in what way. A fact about the epoch |
| **Suggested notifications** | which of those a person might tell, and why each. **A suggestion and never a list of obligations** |
| **What it carried** | a few lines. The topic is the authority; this is the reminder |
| **The prompt** | verbatim, in a fenced block, so it can be pasted without editing |
| **What was rejected** | the wording considered and turned down, and why |

**Involved and suggested are two different questions, which is why they are two
rows.** A tool is *involved* if the epoch changed something that touches it —
that is a fact, and getting it wrong is an error. Whether anybody *tells* it is a
judgement, and it is **entirely the human's**: they may notify all of them, some,
one, or none, in whatever words they like, and none of that is recorded here.

**An epoch is only deployable where our CI is green at its commit**, which is why
**At** is a row rather than a footnote — see *The hard constraint* in
[`epoch-policy.md`](epoch-policy.md#the-hard-constraint-a-red-epoch-is-not-deployable).
The value here is what we assert; `python3 tools/bump_check.py --rev <sha>` is
how somebody checks it without taking our word for it.

**The rejected wording is kept deliberately.** A prompt is short enough that the
reasoning behind it is invisible from the result, and the ways a covering note
goes wrong repeat. An entry carrying only the accepted version teaches nothing
the next person could not have guessed.

---

## E1 — through 2026-09-01

**Announcement:** [`D14`](discussion.md#d14--global-announcement-what-changed-this-week-and-the-one-thing-we-are-asking-of-everybody),
and [`D16`](discussion.md#d16--only-move-your-pin-to-a-commit-where-our-ci-is-green)
for the hard constraint, which arrived after `D14` was written.
**At:** not yet fixed. The epoch is adopted at whatever commit carries these
documents, and it is deployable only if `python3 tools/bump_check.py --rev <sha>`
says our CI is green there. **This row is filled in when the commit exists**, and
until it does the epoch is not adoptable by anybody.
**Involved:** `dokimasia`, `eudaimonia`, `koine` — members, and the ask lands on
all three. `ethos`, `logos` — named in the footings work, and their own question
is [`D11`](discussion.md#d11--we-have-a-footing-for-you-and-no-protocol-to-put-you-in-it),
not this. `cvc5` — its footing changed to `foundation`, which constrains it with
nothing and asks it for nothing. `epikrisis`, through `eudaimonia` — two event
classes it cannot derive, and a question about where it sits.
**Suggested notifications:** the three members, because the ask is theirs and the
CI constraint changes how they bump. `eudaimonia` twice over, since the epikrisis
question is theirs to settle. **Not** `ethos` or `logos` — they are held to none
of this and telling them would blur a boundary the epoch spent its length
drawing. **Not** `cvc5`, ever, by the same reasoning the `foundation` footing is
written under. *All of that is a suggestion; who is actually told is the human's
decision and is not recorded here.*
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

Two things are asked of you, and D16 in the same file is the second.

1. State a publishing stance for your repository and for each child project in
   your tree -- whether a paper exists for it, what the plan is, or that there is
   nothing in it worth writing up. All three are answers, and the third is the
   commonest.

2. Only move your ANOIEU_REV pin to a commit where anoieu's CI is green at that
   commit, and refuse the bump otherwise. D16 says why, and ships the check.
   It must not run in your CI.

Everything else in D14 is notice and needs no reply.
```

The bare file URL rather than an anchor is deliberate and only works while `D14`
holds the pin, which puts it at the top of the file.

**Revised, before it was sent to anybody.** The first version of this prompt said
*one thing is asked of you*, which was true when it was written and stopped being
true when `D16` landed. Recorded rather than quietly corrected, because a log
whose entries are silently updated to stay right is not a log.

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
