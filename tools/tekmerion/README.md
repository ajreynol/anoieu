# tekmerion

A **child project** under [`docs/policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md). Started by a
human, read-only, unadvertised, and not part of what this repository ships.

**Footing:** `unadvertised-child` — reached through anoieu and standing on
anoieu's footing; anoieu's front page does not name it, and this line is what
makes that checkable rather than merely stated.

## The name

*τεκμήριον — conclusive evidence, as against σημεῖον, a mere sign that may point
the other way.*

**In one line: anoieu's route to a verified answer to *is the documentation up to
date*.**

**The central policy of this ecosystem is that a document which has gone stale
is a defect.** Everything else about that policy is argued; this is the only
thing here aimed at making it **checkable** — evidence, claim by claim, that
what a page says is still true of the tree it describes. `policy_check/currency.py`
measures whether a document carries a date, which is evidence about evidence.
**This project is the part that would measure the claim itself.** Aristotle draws the distinction sharply and it is the standard
this project is held to: **what would have to be true for a claim in these
documents to be believed by somebody with no reason to believe us.**

**The objection, and it is not small.** Most of what this register will hold
are signs rather than proofs — *somebody read this page on this date* is a
σημεῖον, and calling the project after the stronger word risks dressing the
weaker thing in it. The name is the **standard**, not a description of the
contents, and the guard against the confusion is in the register itself: **an
entry that cannot say which of the two it is has failed**, and is worse than
no entry.

## The question

**Why should anybody believe what these documents say — and what is the evidence
that they are still true?**

Not *are they well written*. Not *do they describe something good*. Whether the
claims are **currently accurate**, and what stands behind that.

## Why this is a project and not a preference

**Because the constraint was named from outside, and it is the binding one.**
Asked to assess this ecosystem, a neighbouring project's first question was not
about the code: it was *are their docs up to date?* Almost everything produced
here is prose, other tools are asked to rely on it, and **prose goes stale
silently** — no test fails when a page starts describing a tree that changed.

**It is not hypothetical.** One working session on 2026-09-02 turned up six
claims in these documents that had quietly become false, and every one was
found by somebody reading rather than by anything that runs. That is recorded
as `F5` in [zetesis's `findings.md`](https://github.com/ajreynol/epikrisis/blob/main/tools/zetesis/findings.md), which is where
the general finding lives; **what is kept here is the evidence, claim by
claim.**

## And it is why the front page reads as it does

The README leads with a caveat about its own documentation rather than with a
feature list. That is a deliberate shape and this project is the justification
for it: a repository whose product is prose, which asks other repositories to
rely on that prose, and which cannot mechanically detect staleness, **owes its
readers the limit before the pitch.** If the evidence kept here ever became
strong enough, the front page would be entitled to say something else. It is
not, and it does not.

## What it does not do

- **It does not write the documentation.** Each page has an owner; this keeps
  the evidence that what they wrote is still true.
- **It does not judge whether a claim is worth making**, only whether it holds.
  Whether a page should exist is a question for the budget, not for this.
- **It does not grade tools.** What a tool weighs against the tenets is
  [stathmos](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/README.md); whether our conduct can be shown is
  [martyria](https://github.com/ajreynol/epikrisis/blob/main/tools/martyria/README.md) and
  [zetesis](https://github.com/ajreynol/epikrisis/blob/main/tools/zetesis/README.md). This is about the accuracy of
  statements, which is none of those.
- **It does not certify.** No page gets a badge saying it is current.
- **It writes only inside this directory.**

## Status

**Started 2026-09-02**, by the maintainer, in an explicit instruction. It holds
no role and certifies nothing.

**The register has its first entries**, from one working session in the parent's
tree on 2026-09-19: fifteen claims that had gone false, every one conclusive,
and exactly one of them found by anything that runs. They are in
[`docs/register.md`](docs/register.md) with what would have caught each — and
seven of the fifteen have no mechanical form at all.

**The honest position is still the uncomfortable one.** Fifteen is how many one
session found, not how many there are, and the evidence that this ecosystem's
documentation is accurate remains *somebody read it* — now for a named set of
claims on a named date, which is the difference between this page and the last
one. Until far more is recorded claim by claim, the parent's front-page caveat
is the truthful summary and this project's own existence is the admission.

**What the first pass turned up that the parent has to decide**, rather than
this project: four of the fifteen are links into another repository, which the
parent's checker skips by design and deliberately. A child asks for nothing on
its own behalf, so the ask sits in the parent's discussion file, in the parent's
voice.
