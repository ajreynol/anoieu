# zetesis

A **child project** under [`docs/policy.md`](../../docs/policy.md). Started by a
human, read-only, unadvertised, and not part of what this repository ships.
Deleting this directory changes nothing anywhere else.

## The name

*ζήτησις — inquiry; the seeking, as against the having-found.* The word names
what this project is actually doing, which is looking for a standard rather than
holding one. It has none today and says so on every page; a name claiming
knowledge would have been the first thing here to be false.

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

The maintainer caught it. `martyria` — the name he had chosen two exchanges
earlier, and which the agent had substituted its own preference for — was then
given to **this project's sibling**, when the two halves were separated: the
deliberating half took it, and the general inquiry took this one.

**Both halves of that are kept because only the first half flatters.** An agent
testing a consequence rather than assuming it is worth something; an agent
checking one register, concluding a name was free, and never checking the trees
the register does not cover is the same agent being careless in the same hour.
The second is recorded as `X1` in
[`../martyria/witnessed.md`](../martyria/witnessed.md), which is where
this project keeps the occasions it did not pay a cost that was available.

## Its sibling, and the line between them

[`../martyria/`](../martyria/README.md) is the **actionable** half: one live
situation per entry, the evidence it rests on, and a stance somebody can act on.
It decides particular things and derives no general principles.

**This project is the general half and only that.** It asks what standard we are
held to and whether our record could ever show that we met it — questions that
would still be interesting if no situation had ever arisen. **It decides
nothing**, and where martyria needs a principle it takes one from here or
records that none exists, which is a finding for this page rather than a gap to
paper over there.

## The question

**Does this ecosystem's conduct meet a standard it can state — and could
somebody outside check that it does?**

**So yes: this is a research project in the ethics of AI-run software**, and it
is worth saying plainly because the scope section below is easy to misread as a
disclaimer that there is no such project. There is. What it does *not* do is
originate a framework — the standard is taken from work done outside and cited,
and the research is the narrower and more answerable question of whether a
particular ecosystem's conduct could be shown to meet one.

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
2. **The standard, taken from outside.** What we hold ourselves to — **found in
   existing work rather than derived here**, cited so a reader can go and
   check it, and stated so that somebody who disagrees has something to
   disagree with. **The reading has not been done**, and until it has, this
   project has no standard and says so rather than inventing a placeholder.
3. **What would have to be recorded**, per claim, for an outsider to check it
   without taking our word. Follows from 1 and 2 and is the deliverable that
   would matter.
4. **Stretch: the method for one worked instance.** How an exchange with an
   outside party could be judged from the joint histories of everyone in it,
   with nobody trusted — the hypothesis is in
   [`../../docs/science-fiction.md`](../../docs/science-fiction.md). The
   instances themselves are [`../martyria/`](../martyria/README.md)'s; what is
   owed here is the standard they would be judged against.

5. **Whether being ethical and being robust are the same investment.** Stated
   below, because it is the claim that says what this project is *for* beyond
   answering for itself. It is open, it is not close to settled, and it is
   expected to take a long time.

## Siblings, and the two speeds

**The claim is that this project and [`../../docs/vision.md`](../../docs/vision.md)
are siblings**, and it is worth being exact about the sense, because one reading
of it is true and load-bearing and another is false.

**True in subject.** The vision asks *what is this work for and how should it be
done*; this asks *what are we held to and could anybody check it*. Those are two
halves of one question and neither is derivable from the other. Read that way
they are peers.

**False in standing, and the difference is not a formality.** The vision is the
kernel: loaded first, governing everything else, and a checker for it would have
to sit above it and would therefore *be* it. This is a **child project** — no
users, nothing depends on it, unadvertised, and deleting the directory changes
nothing anywhere. **It governs nothing and may not.** A sibling in question is
not a sibling in authority, and an account here that started reading like a
second kernel would have quietly claimed standing nobody granted. If the
responsibility ever does become real, the honest route is the one the policy
already names — the work graduates out of `tools/` and becomes a document that
governs, decided by a person — and not a page here gradually acquiring weight.

### The vision accelerates; this brakes

**They pull in opposite directions on purpose, and both are right.** The vision
is an argument for speed, and the mechanism is not exhortation but the one
[`../../docs/ai-novelty.md`](../../docs/ai-novelty.md) sets out: clear, precise
writing is what makes an agent-run ecosystem fast, because the scarce resource
is attention over text and every ambiguity is a branch discovered late.

**Three brakes now exist and they are not the same brake**, which is worth
saying because the fourth one somebody invents will overlap unless the first
three are laid out. [`../../docs/science-fiction.md`](../../docs/science-fiction.md)
limits how far ahead we may **plan**;
[`../../docs/stretch-policy.md`](../../docs/stretch-policy.md) limits how fast we
may **move**, and its rule is *go only as fast as you understand*; this limits
what we may claim without being able to **show** it. Range, rate, evidence.
Against one accelerator, which is the kernel.

**This project costs time and is meant to.** Asking *what could an outsider
check* before acting is slower than acting, always, and there is no version of
it that is not. The justification is not that caution is a virtue. It is the
claim below.

### The claim: ethics and robustness may be the same investment

**Open, unproven, and the reason this is worth somebody's years.** The
suggestion is that conducting ourselves so that our claims are checkable has a
**by-product**: the ecosystem becomes robust. Three mechanisms make the
correlation plausible, and all three are mechanical rather than moral.

**They want the same artifact.** An ethical claim needs a record an outsider can
check; debugging needs a record you can reconstruct a failure from. Both reduce
to *the record must support a claim about the past*, so the same investment —
dated, attributable, contradictable evidence — serves both. This is the
strongest form of the correlation because nothing about it is about virtue.

**Refusal is least privilege.** The refusals here — no repository created,
nothing pushed, no acting on correspondence unbidden — are ethical constraints
that are also **capability limits**, and capability limits are the oldest
robustness mechanism there is. A system that cannot do a thing cannot do it by
accident either.

**Declining cheaply is reversibility.** The rule that declining must stay cheap,
which this ecosystem applies to everyone it deals with, is the same property as
*changes must be reversible* — a robustness requirement wearing an ethical
name.

**And the case against, which is not weak.** Ethics can *cost* robustness.
Refusing to rank or measure others deprives us of signal. Refusing automation
that would cross a repository boundary leaves failures uncaught. And a system
optimised for defensibility can become slower at fixing real defects — which is
not hypothetical here, since this ecosystem has already been told from outside
that the quality of its self-criticism functions as a substitute for the work.
**If the correlation is real it is not free, and it is not automatic.**

*What would settle it:* an incident where the record kept for ethical reasons
was what made a technical failure diagnosable — or the opposite, one where the
ethical constraint is what let a failure through. Neither has been recorded. The
registers next door are where either would land, and noticing them is a reason
those registers exist.

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

The register has three entries and **the standard is unwritten**, so
nothing here can yet answer the question at the top. The first finding is the
one that prompted the project: the record accounts for what this repository
produced and not for what it was asked, which is a gap in exactly the place an
ethical claim would need to be strongest.
