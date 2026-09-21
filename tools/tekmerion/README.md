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
as `F5` in [zetesis's `findings.md`](https://github.com/ajreynol/epikrisis/blob/main/tools/zetesis/docs/findings.md), which is where
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

**The register has two passes**, from working sessions in the parent's tree on
2026-09-19 and 2026-09-21: **twenty-nine claims that had gone false**, every one
conclusive, and exactly one of them found by anything that runs. They are in
[`docs/register.md`](docs/register.md) with what would have caught each — and
**eleven of the twenty-nine have no mechanical form at all**.

**The honest position is still the uncomfortable one.** Twenty-nine is how many
two sessions found, not how many there are, and the evidence that this ecosystem's
documentation is accurate remains *somebody read it* — now for a named set of
claims on named dates, which is the difference between this page and the last
one. Until far more is recorded claim by claim, the parent's front-page caveat
is the truthful summary and this project's own existence is the admission.

**The second pass found the shape the first one had not**, and it is the reason
the unmechanised share went up rather than down. Three of its eleven entries are
the parent's own **checker** describing the shared policy wrongly, in every member
repository's build — and one of those had recruited: eight child projects in five
trees carry a sentence about a rule that no longer exists, because a check asked
them for it. **A stale claim in a document is disbelieved; a stale claim in a check
is obeyed.** What no checker in this tree can reach is a *paraphrase* of another
repository's rule drifting while every name in it stays valid, and saying so is
more use than a check that would look like an answer.

**What the passes turned up that the parent has to decide**, rather than this
project. **Thirteen of the twenty-nine cannot be settled from the parent's tree
alone** — rows 1 to 4, 16, 17 and 26 to 29 name a path in another repository, and
rows 18, 20 and 21 paraphrase another repository's rule — and that is the whole
direction the parent's checker skips, by design and deliberately. A child asks for
nothing on its own behalf, so the ask sat in the parent's discussion file, in the
parent's voice. **Both halves of it have since moved, in opposite ways.**

- **The paths half is answered, and then the parent built the rest itself.** Kanon
  accepted the ask on 2026-09-19 and now carries an old-to-new table in every move
  notice, which repaired six of the parent's dead links and fourteen of its own.
  The parent then wrote `python3 -m policy_check.outbound`, which resolves its
  outbound links against local checkouts and found rows 26 to 29 on its first run.
  **Neither is a check and neither should be**: a gate that fails for somebody
  else's rename is exactly what was declined.
- **The paraphrase half is open, and is the harder one.** A move notice cannot help
  with a rule being *reworded* while every name in it stays valid English, which is
  what rows 18, 20 and 21 are. The parent has asked kanon for the one thing it
  cannot derive — a machine-readable list of the rule names the policy carries —
  and a decline is a complete answer there too, in which case the honest repair is
  for the parent to stop quoting a document it does not hold.
