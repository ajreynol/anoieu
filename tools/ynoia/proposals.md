# Proposals

Ideas that might deserve a repository of their own, audited here, one section
each. Newest first.

**Nothing on this page approves anything.** A proposal is a claim on a name in a
shared namespace and on somebody's attention for years, and the policy reserves
that decision for a person. What this page produces is an argument with a
recommendation at the end, written so that agreeing or disagreeing with it takes
a minute rather than an afternoon.

This is the third thing ynoia does. The account asks whether the ecosystem's
arrangement earns its machinery; the register keeps the names; and this audits
the specific question *should this become a repository*, which is the same
question the account asks in general, applied to one case with a decision
attached.

## The standard

Four questions, in order. A proposal that fails an early one does not need the
later ones answered.

1. **Does it exist anywhere yet?** Code that has been written twice is evidence;
   code that has been written once is a design, and a design does not need a
   repository. The strongest signal available is two implementations that turned
   out identical, because that is a fact rather than a prediction.
2. **How many consumers, really?** Two is the number at which sharing looks
   obviously right and usually is not: the second consumer is the one that
   discovers what is actually shared, and a third is what shows whether the
   answer generalises or was a coincidence between two.
3. **What does a repository buy that `tools/` in an existing one does not?**
   Isolation, a release surface, an independent maintainer. Each is real and
   each is also a cost. The ecosystem already has a mechanism for sharing code —
   a member pins a commit and fetches — so the question is never *how would
   anyone get it* but *what breaks if it lives in somebody's tree*.
4. **Who maintains it when the enthusiasm is gone?** A repository is a standing
   obligation. If the answer is "whoever needs it next", the proposal is for a
   directory, not a repository.

The likeliest right answer, most of the time, is **not yet, and here is what
would change that** — a threshold somebody can watch for, rather than a refusal.

## P1 — central tooling for reporting

**Proposed by** dokimasia, in its `D4`, and carried here by a person.
**Audited** 2026-08-31, at anoieu `441b562`.
**Recommendation: not a repository. Put the shared piece in anoieu's `tools/`,
and revisit at a third consumer.** For a person to accept or reject.

**The proposal.** Both anoieu and dokimasia have now built the same reporting
loop: a script run in the project a finding is about, a script run at home once
it has replied, prompts defined in a document, a drift check that the script's
copy has not diverged from that document, and a postmortem log with one block
per run. dokimasia built theirs in an afternoon by reading ours, which is the
observation that prompted the topic — the second implementation of a protocol is
the moment to ask whether it should have been one.

**Against the standard.**

*Does it exist?* Yes, twice, which is the strongest form of the evidence. The
shared surface is also already identified rather than guessed at: the drift
check is around sixty lines and is a copy in one direction, the reply-file
finder and the branch-state reporter are pure git and identical, and the reply
format is fixed by prose both sides already follow. What is *not* shared is
equally clear — the prompts, because the subjects differ, and what settles a
row, which each tool must name for itself.

*How many consumers?* Two. This is the question that decides it. Two consumers
that copied one from the other cannot distinguish *what is shared* from *what
one of us happened to write first*, and dokimasia says as much about its own
register: it knows two of its slots are weak, and ours is generated where theirs
is curated. Fixing a format now would fix it before either side has evidence
that its format is right.

*What would a repository buy?* Almost nothing that is not already available. A
member pins a commit of anoieu and fetches it — that is how `policy_check.py`
already reaches dokimasia's CI — so a shared implementation under anoieu's
`tools/` reaches a member by a path that exists, is understood, and is already
pinned. A repository would add a second thing to pin, a second version to track
against the first, and a second place where a policy change has to land, in
exchange for isolation nobody currently needs.

*Who maintains it?* Unanswered, and that is the point. anoieu is written mostly
by agents under light supervision and has already declined to sign a maintenance
contract it cannot keep. A repository whose maintainer is "whoever needs it
next" is a directory with extra ceremony.

**The recommendation, and the threshold.** Take dokimasia's own smallest piece
first: the prompt-drift check, into anoieu's `tools/`, fetched the way the policy
checker is. It is the piece that is purely about the shared format and touches
nothing either tool owns, and it is the one guaranteed to rot otherwise, because
it exists precisely to catch the divergence that two copies of it will produce.
The branch-state reporter and the reply finder follow, in that order, each on
the same test: **share code only where two implementations turned out
identical**, applied per piece rather than decided once.

Revisit the repository question at a **third consumer**, or when the shared code
is large enough that living in anoieu's tree distorts anoieu. Neither has
happened. Until one does, no name should be taken for this — a reserved name is
itself a claim, and taking one early is the cheapest way to make a directory
feel like an obligation.

**What the audit is not.** It is not a judgement on dokimasia's implementation,
which was not asked about, and it is not a decision. If a person disagrees, the
place to say so is the recommendation line above; the argument beneath it is
what there is to disagree with.
