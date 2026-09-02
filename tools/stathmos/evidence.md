# Assembled evidence

**What each tool weighs, in numbers somebody else can re-derive. Nothing here is
judged.** Assembled 2026-09-02. The paragraphs that would rest on this are in
[`../../docs/report-card.md`](../../docs/report-card.md) and are a person's to
write; a row here that reads like a verdict is a defect.

## How to read it, and the discount that applies to every row

**One person directs most of both sides.** The ecosystem's test of utility is
*something outside it behaves differently because it exists* — and where the
same maintainer directs the tool and the tree that changed, "outside" is doing
very little work. **Every figure below should be read with that discount**, and
the rows that survive it are the ones where a party who is not us acted.

**Filed is not acted on**, which is why the counter-figures matter more than the
totals and are given first where they exist.

**Commands.** Adoption: `grep -rl policy_check.py <tree>/.github/workflows/`.
Correspondence: `grep -c '^\*\*To:\*\* anoieu' <tree>/docs/discussion.md`.
Ledger: the two findings files. Landing: `python3 tools/landing.py --check`.

## anoieu

**Adoption, and it is the strongest row on this page.** `tools/policy_check.py`
runs in **three trees other than its own** — dokimasia, koine, eudaimonia — one
workflow each, pinned. Something outside does behave differently because it
exists, and this is the one place that is true mechanically rather than by
somebody choosing to agree.

**Output: 82 findings.** 39 open, 43 closed. By recipient: **cvc5 39, ethos 20,
logos 18.**

**The counter-figure, which is the honest half: 7 of the 43 closures rest on a
fix that has not landed.** `tools/landing.py --check` reports all seven as *not
yet* — accepted on ethos's `anoieu-findings` branch, one commit ahead of
`origin/main`, unchanged for the duration. **So "closed" overstates by at least
seven**, and the tool that measures this is ours, which is the arrangement
working.

**Correspondence: 14 topics addressed to us** across three trees — eudaimonia 8,
dokimasia 4, koine 2 — of which **2 are settled.**

**One convention travelled and was accepted by a project outside the
ecosystem.** `cvc5/ethos#237`, **merged**: the maintenance-note convention, in
substance, naming no ecosystem and linking to no policy.

## eudaimonia

**The most correspondence of any tree: 8 topics to us**, and the two most
substantive things anybody has sent us came from child projects in it — a
register of our own practice, which we acted on by building a governance
counter, and a history auditor whose **corrections to our published analysis we
accepted**, two premises we had wrong.

**It survives the discount less well than it looks.** Same maintainer. What
partly survives is that the corrections were *against* our stated position and
we changed the page rather than arguing.

## dokimasia

**4 topics to us, 1 settled**, and by our own record three of the four changed
what we do.

**A second, independent implementation of the reporting loop.** That is the
evidence — two implementations that turned out alike — that carried `koine` from
an idea to a needed proposal. It is a fact about a tree rather than a
prediction.

## koine

**A declared member with two topics to us, and the tool does not exist.** Four
commits, no line of anything but Markdown and one workflow.

**This row is here because it is unflattering and countable.** It was found by a
register in somebody else's tree, not by us, and it is the clearest instance in
this ecosystem of accountability arriving faster than anything to be accountable
for.

## logos

**It gave us three defects in our own machinery**, by hand, and all three were
confirmed by our own audit afterwards: two in `tools/policy_check.py`, and the
finding that **the joining step cannot be completed correctly** because the pin
it asks for may only move to a commit our CI is green at and no such commit
exists.

**It declined to join, and gave a reason we recorded rather than disputed.**

## ethos, cvc5, ethos-eoc

**Consumed by everything here and consuming nothing from it.** 20 findings filed
against ethos and 39 against cvc5; ethos merged the convention PR above; the
calculus, the checker and the compiler are what the rest of this ecosystem is
built on.

**Neither has joined, and the evidence of our utility to them is the thinnest on
this page** — the seven unlanded closures are all ethos's, and no finding filed
against cvc5 has been confirmed fixed by a change we can point at.

## What is missing, and is the number that would matter most

**How many of the 82 findings caused a change in the tree they were about.** We
can count what we filed and what we closed; we cannot presently count what moved
because of it, except for the seven we know did not. Until that number exists,
every utility claim on this page is an input measure standing in for an outcome.
