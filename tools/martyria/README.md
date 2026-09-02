# martyria

A **child project** under [`docs/policy.md`](../../docs/policy.md). Started by a
human, read-only, unadvertised, and not part of what this repository ships.
Deleting this directory changes nothing anywhere else.

## The name

*μαρτυρία — testimony; the evidence a witness gives.* The project is **the
ecosystem's ethics research engine**, and the word names what it deals in: it
does not reach verdicts, it assembles what can be shown. A claim about one's own
conduct is worth very little; what is worth something is an artifact somebody
else can check, and gathering those is the whole job.

**The project and its unit share the word, deliberately.** One entry in
[`witnessed.md`](witnessed.md) *is* a martyria — a dated, contradictable piece of
evidence about conduct — and this directory is the engine that collects and
maintains them. That is a part-and-whole relationship rather than an ambiguity,
and it is stated here because the last name this project had was ambiguous in
exactly the way that matters.

### How this name was chosen, which is itself a small piece of evidence

**It was called `ethics` first**, on the argument that the subject is not ours
to rename and that a private etymology would make work meant to be checkable by
outsiders look like a private notion.

That argument still holds, and it lost to a plainer one: **the word was doing
two jobs in the same prose.** These documents discuss ethics as an ordinary
subject, constantly and in sentences that have nothing to do with any directory.
Naming a project the same word makes every one of those sentences ambiguous —
the reader has to decide, each time, whether a proper noun or a common one is
meant, and the writer has to remember to disambiguate. That is clutter in the
documentation rather than in the code, and documentation is the thing this
ecosystem spends its attention on.

**The ambiguity has a mechanical witness**, which is what made it checkable
rather than a matter of taste. The policy checker decides whether a child
project is an island by grepping the tree for **the bare project name**, so a
name that is an ordinary word matches prose about the subject and not about the
project. `ethics` already matched one such document. The next match could be in
a README or a workflow file, where it would be reported as an island break that
is not one — a check firing on a non-problem, which this repository's own
position holds is ours to fix rather than to work around.

So the ecosystem's Greek naming convention turns out to have had a second
justification nobody had written down: **an unusual name reads unambiguously and
greps unambiguously, and those are the same property.** It is recorded where the
convention lives, in [`../ynoia/names.md`](../ynoia/names.md).

**Then it was called `apodeixis`, and that was worse.** The agent picked the
replacement itself, checked that the name was free in this ecosystem's register,
found that it was, and took it. It **did not look in the neighbouring trees**.
`apodeixis` was already in use as a child project in eudaimonia — and that
project's own README says, in terms, that the name *is used here and claimed
nowhere*, because adding a line to somebody else's register is a person's edit
to make. So the one party that behaved carefully was the one whose name got
taken.

The maintainer caught it, and the name is now the one he had already chosen two
exchanges earlier and the agent had substituted its own preference for.

**Both halves of that are kept because only the first half flatters.** An agent
testing a consequence rather than assuming it is worth something; an agent
checking one register, concluding a name was free, and never checking the trees
the register does not cover is the same agent being careless in the same hour.
The second is recorded as `X1` in [`witnessed.md`](witnessed.md), which is where
this project keeps the occasions it did not pay a cost that was available.

## The question

**Does this ecosystem's conduct meet a standard it can state — and could
somebody outside check that it does?**

Both halves matter and the second is the one that does the work. A claim about
one's own conduct, made by the only party in a position to know, is worth very
little. What makes it worth something is an artifact somebody else can inspect.

## Why this is not ordinary documentation

Every other page here exists to be *read*. This one has a second job, and the
two pull in different directions often enough to be worth stating.

**It is an account.** What we do, why, and where it falls short — the ordinary
job of a child project.

**And it is evidence.** If another repository is trying to contact us — and one
has — then *we adhere to a standard* is a sentence somebody outside has to be
able to check without trusting us. So the output here is not only an argument.
It is a specification of **what would have to be recorded** for each claim to be
checkable at all.

That changes what counts as finished. **A finding here is not done when it is
argued. It is done when it names the artifact that would settle it**, and the
artifact usually does not exist yet, which is the point.

## Why the standard comes from outside

This repository already holds that **a clear reference is a compiler
optimization**: a citation to work that settles a point replaces an inlined
derivation with a call to something already argued and already reviewed by far
more readers than this tree has. Deriving an ethics here would be the inlined
version — slower, worse, and checked by nobody.

It is also the rule this ecosystem applies to itself everywhere else. We do not
claim a state of an art we have not surveyed, and we do not gesture at *the
literature* without naming it. So the honest position today is short: **the
reading has not been done, and no framework is cited here yet.** Producing a
plausible list of names would be exactly the failure this project exists to
notice — the appearance of rigour standing in for it.

What that leaves as ours, and it is enough: taking a standard somebody else
argued for, and asking what our own record would have to contain for an outsider
to check us against it. That second half is not in anybody's literature, because
it is a question about this tree.

## Goals, in order

1. **The register of shortcomings** — every place where our record cannot
   support a claim we make about our own conduct.
   [`findings.md`](findings.md). This is the part that exists.
1a. **The register of what is witnessed** — [`witnessed.md`](witnessed.md), in two
   halves. **Testimony**: declared facts bearing on whether we can be trusted,
   which somebody outside could contradict — the weak form, because a party
   chose to say it. **Cases**: acts read out of artifacts, which is the strong
   form for the reason the word was chosen. Kept apart from the findings
   because a gap and an act are not the same kind of thing, and kept apart from
   each other because a declaration and a record are not either.
2. **The standard, taken from outside.** What we hold ourselves to — **found in
   existing work rather than derived here**, cited so a reader can go and
   check it, and stated so that somebody who disagrees has something to
   disagree with. **The reading has not been done**, and until it has, this
   project has no standard and says so rather than inventing a placeholder.
3. **What would have to be recorded**, per claim, for an outsider to check it
   without taking our word. Follows from 1 and 2 and is the deliverable that
   would matter.
4. **Stretch: one worked instance.** An actual exchange with an outside party,
   judged from the joint histories of everyone in it, with nobody trusted. The
   hypothesis is in
   [`../../docs/science-fiction.md`](../../docs/science-fiction.md); this would
   be the first time anybody tried it.

## What this project does not do

- **It does not do research in ethical AI, and it is not our job to.** The field
  exists and people work in it seriously; originating a framework from the
  repository that keeps a static analyzer would be out of scope and worse than
  out of scope. **We leverage external work rather than producing it.** What is
  ours is the narrower question of whether *this* ecosystem's conduct can be
  shown, against a standard somebody else already argued for.
- **It does not define ethical AI**, and it does not claim this ecosystem does
  or could. That claim is above the line and the line is written down.
- **It does not certify.** No badge, no score, no rating, no verdict — on
  anybody, including us. A project that ends by awarding itself a pass has
  become the thing it was watching for.
- **It does not judge another repository's conduct.** What may be published
  about somebody else's work is governed by
  [`../../docs/reports/reporting-policy.md`](../../docs/reports/reporting-policy.md)
  and nothing here loosens it.
- **It gates nothing.** No commit, no stretch and no deployment waits on this
  directory, and if one ever does, it has stopped being a child project.
- **It does not replace the reporting workflow.** Where reading turns up
  something actually wrong in somebody's file, that is a finding and it leaves
  through the ledger, not through here.
- **It writes only inside this directory.**

## Status

**Started 2026-09-02**, by the maintainer, at their explicit instruction —
which is the only way one of these may begin.

The register has its first two entries and **the standard is unwritten**, so
nothing here can yet answer the question at the top. The first finding is the
one that prompted the project: the record accounts for what this repository
produced and not for what it was asked, which is a gap in exactly the place an
ethical claim would need to be strongest.
