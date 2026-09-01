# The epoch policy

What an epoch is, what ends one, and what designing the next one involves.

[`epochs.md`](epochs.md) is the **log** and this is the **policy**, and they are
two files because they are held to opposite standards: a policy has to be current
and the log explicitly does not. One file carrying both would make the licence to
be stale look like it covered the rules as well.

## What an epoch is

**The stretch of work between one global announcement and the next.** Not a
release, nothing is versioned against it, and it has no schedule — it is the span
a single announcement turned out to cover, named after the fact.

**The boundary is an announcement and not a date**, because a date would be a
cadence, and a cadence is a commitment to other repositories that we are in no
position to sign. An announcement is an event that already happens, already
costs somebody's attention, and already has a place in the record. Using it as
the boundary adds no machinery at all, which is most of the argument for it.

## What counts as a major event

An epoch is made of these. The list is short deliberately — a register of events
that counts everything is a commit log, and there is one of those already.

| event | where it is recorded |
| --- | --- |
| a global announcement | [`discussion.md`](discussion.md), the topic carrying `Global:` |
| **a role changing hands** | [`roles.md`](roles.md) — the entry moves under a new heading and the id does not change |
| a repository joining, or its footing changing | [`../tools/ecosystem.json`](../tools/ecosystem.json) |
| a child project reaching one of its three endings | the project's own README |
| a convention every member is checked against changing | [`policy.md`](policy.md) |

**A role changing hands is a major event, and it is the one most likely to be
missed.** It changes who is *accountable* rather than what exists, so it leaves
almost no trace in a tree: one entry moves between two headings, the id stays the
same, and nothing is created or deleted. A reader reconstructing history from
commits alone will not see it happen. That is the whole reason
[`roles.md`](roles.md) keeps ids permanent and moves entries rather than
rewriting them — and it is why a handoff belongs on this list beside an
announcement rather than a rung below it.

The others are here because each already has a file that records it. **An event
with no home is not a major event; it is a change of mind.**

## The declared record, and who it is for

This page and its log are a **declared record**: what we say happened, written by
hand, at the time.

A tree also carries a **derived record** — what the commits show happened —
and the interesting quantity is the delta between the two. A child project in
eudaimonia's tree builds exactly that comparison, and its assessment of five
trees here found that the repository holding four fifths of the ecosystem's
commits contributes none of its declared record, so the documentation practice
that assessment could see was three days old and covered only the newest trees.

**That is a fair hit and this is part of the answer to it.** A declared record is
cheap to keep and impossible to reconstruct later; the reason to write down that
an epoch ended, or that a role moved, is precisely that neither is legible from a
diff. Nothing here is generated, and nothing should be: a derived record that
agrees with itself proves nothing.

## The hard constraint: a red epoch is not deployable

**An epoch may only be adopted at a commit where anoieu's own CI is green, and a
downstream tool must refuse it otherwise.** This is the one thing on this page
that is not a convention, and it is stated as a requirement on *them* because it
is the only half we cannot enforce from here.

**Adoption means moving a pin.** A member adopts an epoch by moving `ANOIEU_REV`
in its `anoieu / policy` workflow to a commit of this repository. That is the act
this constrains — not reading the announcement, not agreeing with it, and not
doing anything the announcement asks for.

**The question is asked about the commit, never the tip.** Green-at-a-commit is a
fact that never changes once the run has finished. Green-at-HEAD changes without
anybody committing, and a gate on it would make a member's decision depend on
what we pushed that morning — the same failure the pinning discipline exists to
prevent, moved one step upstream.

**It fails closed.** Not green, not finished, or not reachable all refuse. That is
the reverse of how the inventory treats an unreachable remote, and the difference
is worth stating: **adopting an epoch is optional and deferrable.** Refusing costs
a member one later attempt; adopting wrongly pins them to a commit our own build
rejected. Where the cheap error is obvious, take it.

**And this check must never run in anybody's CI.** It reads a remote, so a build
that called it could turn red without anybody committing — and a build that can
change colour on its own cannot be evidence that a commit was good. It belongs at
the moment of adoption, in a bump script or a person's hands, and nowhere else.

[`../tools/bump_check.py`](../tools/bump_check.py) implements it, published so
that four members do not each write it:

```
python3 tools/bump_check.py --rev <sha>    # may this epoch be adopted?
python3 tools/bump_check.py --root PATH    # read the pin out of a member's workflow
```

Exit `0` adopt, `1` refuse, `2` refuse as unverified — three codes rather than
two, because *we asked and it is not green* and *we could not ask* are different
facts and a bump script should be able to log which one it hit.

**What this does not say.** A green run means those checks passed at that commit.
It is not a claim that the epoch is any good, that its conventions are right, or
that adopting it is wise — the same caution the analyzer carries about its own
silence. It is a floor, and the only thing it rules out is deploying a stretch of
work we could not get past our own build.

## How much of this crosses the boundary — open

**`epoch` is our word for our planning unit. `global announcement` is the
interface.** Which of the two a downstream repository should ever have to know
about is an open research question, and it is recorded here as one rather than
answered.

**Today they coincide exactly** — one epoch, one announcement — and that is
precisely why the leak is hard to see: every sentence about an epoch can be read
as a sentence about an announcement and stays true. The coincidence is a fact
about there having been one epoch, not a property of the design, and it will stop
holding the first time a stretch of work produces two announcements or none.

**What a member demonstrably needs is two things**, and this is the whole list:

1. **what a global announcement is** — that it is addressed to every member at
   once, that its `Global:` field says what is owed, and that most of one asks
   nothing. [`policy.md`](policy.md#a-global-announcement) is that interface.
2. **only bump a pin to a commit where our CI is green at that commit.**

**Neither requires the word *epoch*.** The second is a good rule about bumping
whether or not anybody plans in stretches, and phrasing it as *an epoch is only
deployable…* makes a rule about their build sound like a rule about our calendar.
That is the leak, and it has already happened once, in `D16`.

**What the word might buy them:** a shared coordinate, so both ends can name the
same stretch; and a rhythm, since announcements arriving in batches rather than
continuously tells a maintainer how often to expect to read one.

**What it costs them:** vocabulary nobody asked for, in an ecosystem whose
standing complaint from a member is that joining cost eighteen hundred lines of
reading. And coupling — reorganise how work is planned here and a term in
somebody else's document changes under them.

**Three positions. We hold the first by default rather than by argument:**

| position | what crosses | the case against |
| --- | --- | --- |
| **internal only** | announcements, and the bumping rule | loses the coordinate; two ends with no shared name for the same stretch |
| **a coordinate and nothing more** | an epoch id on each announcement | an id for a concept they are not told the rest of is its own small confusion |
| **shared** | the concept, this page | asks members to carry our planning vocabulary for a benefit nothing has shown they want |

**What would settle it: a member saying which.** This is exactly the kind of
question the far end can answer and we cannot — a protocol's defects are visible
where it is received, not where it is written. `D16` asks, and an answer of *we
never noticed the word and did not need it* settles it as firmly as any other.

**Until it is settled, text addressed to members states the rule without the
word.** That is the reversible choice: adding a vocabulary later costs a
sentence, and withdrawing one that other repositories have written into their own
documents costs considerably more.

## Designing the next epoch

**Deciding what the ecosystem's next stretch of work is *for*.** It is a
responsibility rather than a document, it currently sits with this repository,
and it is `R27` in [`roles.md`](roles.md).

Four things, and the last is the one that gets skipped:

- **What changes**, and what is deliberately left alone. Most of the ecosystem
  should be untouched by any given epoch.
- **What is asked of members**, if anything — and an epoch that asks for nothing
  is a good epoch, not a wasted one.
- **When it has ended**, which is the same judgement as deciding an announcement
  is worth everybody's attention. The one-pin rule is the budget: a second
  announcement displaces the first, and having to choose is the cost control.
- **What comes out.** Every protocol here is held to *an addition says what it
  removes*, and the counter that watches the findings prompts has reported three
  rounds and three increases. **An epoch that only adds has not been designed**,
  and this is the clause to read first when designing one.

**What it is not.** Not [`board.md`](board.md), which is what is outstanding and
does not say what any of it is for. Not [`vision.md`](vision.md), which says what
the work is aiming at in general and is argued rather than decided. Not the
record. This role decides the *shape of one stretch*, and it is small.

**It goes to kanon.** Deciding what every member is asked for next is governance,
and it sits in the repository that also files findings against them — the
arrangement `B15` on the board proposes to undo. When the governance repository
exists, this moves with the policy and the joining rules rather than staying
behind, and it is listed among what moves for that reason.

## Frequency, and the honest position

There is no target. One pinned announcement at a time is the whole of the rate
limit, and it works by making a second one cost the first one's visibility.

**Two epochs in a week would be a symptom rather than progress.** The criticism
this ecosystem has already been given from outside is that governance is the
cheapest thing here to produce and that it has outrun the trees it governs. An
epoch is a governance artifact. The rate at which they are declared is therefore
evidence about that criticism, in whichever direction it happens to point, and
[`epochs.md`](epochs.md) is where somebody can count them.
