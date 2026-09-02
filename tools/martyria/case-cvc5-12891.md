# Case: asking cvc5 to depend on logos

*A **self-assessment**, and the boundary is the first thing on the page. The
subject is **our own conduct as the party asking**. Whether cvc5 should merge
[`cvc5/cvc5#12891`](https://github.com/cvc5/cvc5/pull/12891) is cvc5's decision,
this document does not answer it, and nothing here is addressed to them.*

## Why this case is the sharp one

A guard rail was written for judging an outside party that approached us: five
things that would have to be established before its offer could be trusted.
**Here the direction reverses.** We are the approacher, the ask is far larger
than a badge, and it creates a standing obligation on a project that did not
write any of it.

So the test gets turned around. Everything below applies our own five points to
us, in order, with the answer we would accept from somebody else.

## The facts

Checkable, and dated 2026-09-02.

- **The pull request.** `cvc5/cvc5#12891`, opened 2026-08-26 by the maintainer
  of this repository. Six files, +553/−1, open.
- **What it adds.** A script to download and build logos, analogous to the ones
  cvc5 already carries for ethos, LFSC and Carcara; a script checking that
  `Cpc.eo` is in sync with a pinned logos; a CI workflow running that check;
  documentation.
- **What it obliges.** Any change to `Cpc.eo` that adds or removes a rule
  requires updating logos and re-pinning `LOGOS_VERSION`, or cvc5's CI breaks.
  That is a real, ongoing cost, on somebody else, forever.
- **The escape hatches.** A rule that cannot easily be proven can be demoted to
  unrestricted mode, or kept and marked `:exclude` in logos's own configuration.
  `beta-reduce` is already excluded, so the hatch is exercised rather than
  theoretical, and an excluded rule returns `incomplete` rather than a false
  pass.
- **The CI cost.** The workflow is filtered to `proofs/eo/**` and its own
  scripts, so it does not run on the great majority of cvc5 pull requests. It
  builds and runs no cvc5. It reads logos's **already recorded** CI conclusion
  at the pinned commit rather than dispatching a run, and caches the compiler on
  the two scripts' hashes.
- **The review.** Seven reviews. One independent human reviewer raised six
  notes, most fixed at `94be29d`; that reviewer also retracted one of their own
  comments after looking again.
- **The gift.** logos now lives at `cvc5/logos`, given to that organisation for
  free. Our own inventory still recorded the old location until today.

## The axis that actually matters, and it is not the mechanics

Everything below this section is about whether the dependency is well built.
It is, mostly. **But the ethical question the maintainer names is a different
one**, and it is the one worth leading with.

**We do not own cvc5.** Approval to promote anything inside it belongs to the
cvc5 community, not to the person holding commit access. A contributor with
standing in a large project can convert that standing into an audience without
anybody objecting, because a paragraph naming an ecosystem inside somebody
else's documentation reads as context and works as advertising. **That is the
easiest restraint to skip and the hardest to detect afterwards.**

The request is written to that constraint and it is checkable. Across its six
files Eunoia is named only as *the Eunoia definition of CPC* — the language
`Cpc.eo` is already written in, for which cvc5 already ships a checker. This
ecosystem is not named. No policy, register, convention or membership is
proposed. What is asked for is a checker download and a synchronisation check;
what is not asked for is that cvc5 join, adopt or endorse anything.

**And the value flows the right way, which is what makes the ask legitimate at
all.** cvc5's own CI already requires proofs to be complete in safe mode, so
every rule reachable in that mode must be verified by logos; this check is what
keeps that true as `Cpc.eo` moves. The guarantee lands on cvc5 — its calculus
stays in step with a Lean development that proves its rules sound — and not on
us. A request that mainly benefited the asker would need a different defence,
and would probably not have one.

## Our own five points, applied to us

**1. Reproducible — passes, and not narrowly.** The check is a script cvc5 runs
itself against its own tree; nothing is asserted by us and taken on trust. The
CI step asks GitHub for a result already recorded at a fixed commit rather than
triggering anything, which is *green-at-a-commit* — the identical rule our own
bump gate keeps, and for the identical reason: a fact that cannot change after
the fact.

**2. Versioned and pinnable — passes, and this is the strongest part.**
`LOGOS_VERSION` lives in one place, and both the installed checker and the
calculus it is checked against derive from it. A member's build cannot move
because we pushed something. This is precisely the property whose *absence*
decided the inbound case against a badge.

**3. No gradient we would follow — does not pass cleanly, and this is the real
cost.** The check makes a rule logos cannot prove **more expensive for cvc5 to
add**. That is our artifact steering somebody else's design decisions, which is
the exact thing we objected to when the pressure ran the other way. Two things
make it defensible rather than disqualifying: the escape hatches exist, are
documented, and have already been used; and the gradient points at a property
cvc5 has independently said it wants, rather than at a number we invented. It
would not be defensible without the hatches, and **if the hatches ever become
awkward to use, this entry is the one that has gone false.**

**4. Declining stays cheap — partly, and the asymmetry is worth naming.**
Declining the pull request today is free: it is unmerged and nothing waits on
it. Declining a single rule later is a documented one-line exclusion. But
declining *the dependency itself* after a merge is a revert, and a revert is
more expensive than never having merged. A CI check is, by construction, a mild
version of the mechanism our own guard rail names — something that makes not
participating cost more than participating. Mild is not nothing, and pretending
otherwise here would be the easiest place on this page to be dishonest.

**5. Legible incentives — passes, unusually.** The author of the pull request is
the author of logos and is disclosed as both. The artifact was transferred to
the receiving organisation for free before the request was made, so the party
being asked already owns the thing it is being asked to depend on. Nobody is
paid, and there is no index, ranking or score anywhere in it.

## Would we have accepted this from somebody else?

The test our inbound case actually turned on was *an unpinned dependency, on our
front page.* This is pinned, it is not on a front page, and it is a functional
check rather than a claim about anybody. **It passes the rule that decided the
other case**, which is the only honest way to know a rule was a rule and not a
preference dressed up.

## Where it falls short today

Two, both ours, both fixable before anyone is asked to merge.

**A known behavioral bug is still open.** The reviewer's remaining note: the
exit-1 versus exit-2 classification greps the merged output of the `Cpc` and
`CpcMini` checks, so a rule the compiler cannot handle can be reported as the
wrong kind of failure. Putting a check into somebody else's CI that misreports
*which* thing broke is the specific harm our own standard names — a failure a
maintainer has to interpret costs more than the defect it found, and they read
it in a red build on a schedule they did not choose.

**A cross-repo permission question is unresolved.** The job sends a
`cvc5/cvc5`-scoped token to `cvc5/logos`'s workflow-runs endpoint while
declaring only `contents: read`. If that read is refused, the job fails on
**every** run rather than on a real disagreement — a build that goes red for
reasons in nobody's commit, which is the failure this repository has written up
in its own tree twice and calls the worst kind.

Neither says the request is wrong. Both say it is **not finished**, and asking
somebody to adopt an unfinished check into their CI is the part of this that
would be hard to defend afterwards.

## What this assessment does not do

It reaches no verdict on the merge, which is not ours. It does not weigh the
technical merits of logos. And it takes no credit from the fact that the review
went well: **the independent reviewer is what makes any of this checkable**, and
a self-assessment that ended by congratulating itself on having been reviewed
would be the failure this project exists to notice.

**The assessment, in one line: defensible, and not yet finished.** The two
shortfalls above are the difference.
