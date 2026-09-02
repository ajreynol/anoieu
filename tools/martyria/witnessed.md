# The register of what is witnessed

*μαρτυρία — testimony; the evidence a witness gives. Chosen over the
alternatives because it names **evidence given** rather than judgement passed,
which is the modesty this project needs: a martyria is something entered into
the record for others to weigh, never a verdict anybody here has reached.*

**Two registers, because there are two kinds of evidence and conflating them is
the mistake this page exists to avoid.**

**Testimony — `M`.** A declared fact that bears on whether our conduct can be
trusted, and that somebody outside could contradict. The **weak** form: a party
chose to say it.

**Cases — `C`.** An act, witnessed from artifacts rather than declared. The
**strong** form, and for exactly the reason the word was chosen: a record did
not choose to speak.

Both are append-only. An entry is re-affirmed, superseded or withdrawn, never
quietly deleted, and a withdrawal is itself an entry.

## Why testimony, when this project's whole point is that self-report is weak

It is the weak form and it is labelled as such wherever it appears. The
register of gaps next door exists because **a claim about one's own conduct,
made by the only party positioned to know, is worth very little.** Nothing
here changes that.

Two things make it worth keeping anyway.

**For some facts there is no artifact and there never will be.** Whether
somebody knows somebody, what they intended, whether a relationship exists — no
commit records the absence of a connection. The choice is not between testimony
and evidence; it is between testimony and silence, and a dated, attributable,
**falsifiable** declaration beats silence.

**A martyria can be contradicted, which is what separates it from an
unfalsifiable claim.** *We behaved well* cannot be checked by anybody. *I have
no affiliation with X* can be: somebody who knows otherwise can say so, and the
declaration names a person and a date to say it against. That is a low bar and
it is a real one.

**Where a record exists, the record wins.** A history is the stronger form of
the same thing precisely because it did not choose to speak — which is the
objection that was raised against this word and is the reason it survives it. A
martyria drawn from a joint history outranks a martyria a party volunteered, and
where the two disagree the volunteered one is the one to doubt.

Each **testimony** carries the same six fields, in the same order; the cases
register below has its own:

| field | what it holds |
| --- | --- |
| **What** | the declared fact, in the declarer's terms |
| **Who** | the person declaring it. A tool cannot give testimony |
| **When** | the date it was made, and the date it was last re-affirmed |
| **Why it bears on our conduct** | what would be in doubt without it |
| **How it could be contradicted** | who could say otherwise, and on what basis |
| **State** | `standing`, `re-affirmed`, `withdrawn` or `superseded`, with what changed |

---

## Testimony

### M1 — no personal affiliation with the source of the inbound pull request

**What:** *I testify that I have no personal affiliation with the external
source of* [`cvc5/cvc5#12858`](https://github.com/cvc5/cvc5/pull/12858) — the
party that opened it, and the index it links to.

**Who:** the maintainer of this repository, who is also the person driving every
session in it.

**When:** declared 2026-09-02. Not yet re-affirmed.

**Why it bears on our conduct:** it removes the confound that would make the
whole analysis of that pull request worthless. This ecosystem has written a
stance on it, a set of guard rails against it, and a hypothesis that the
resemblance between its stated axis and ours may be **independent convergence**.
Every one of those readings depends on the two parties being unconnected. Had
there been an affiliation, the interest would be self-interest, the convergence
would be no evidence of anything, and the caution would be theatre. The
declaration is what makes the reading available to somebody who does not know
us.

**How it could be contradicted:** by anybody who can show a connection — shared
employment, funding, correspondence predating the pull request, common
authorship. The claim names a person and a date, and it is public, so
contradicting it costs a sentence from anybody who knows better.

**State:** **standing.** It is maintained: if the fact ever changes, this entry
is superseded by one saying so, on the day it changes, and the original stays
legible. An affiliation that arose later and was recorded late would be worth
less than one recorded early, which is the reason the maintenance rule is part
of the entry rather than a convention somebody remembers.

### M2 — the author of the dependency is the author of the request

**What:** *logos was given to the cvc5 organisation for free, as a gift, before
anything was asked of them; and I am the author of logos and of*
[`cvc5/cvc5#12891`](https://github.com/cvc5/cvc5/pull/12891)*, the request that
would make cvc5's CI depend on it.*

**Who:** the maintainer of this repository.

**When:** declared 2026-09-02. Not yet re-affirmed.

**Why it bears on our conduct:** it is the structure our own guard rails were
written against — a party proposing that somebody adopt a thing that party
built. Disclosing it does not dissolve the conflict; it makes the conflict
something a reader can weigh rather than discover. The gift half matters
independently: cvc5 already owns the artifact it is being asked to depend on, so
the request cannot be a lock-in to something we control, and that is a fact
about the repository's location rather than a promise about our intentions.

**How it could be contradicted:** the transfer is public — `cvc5/logos` exists,
and the old location redirects to it. Any claim of payment, of a retained
private fork, or of authorship elsewhere is checkable against public history by
anybody.

**State:** **standing.** The assessment that rests on it is
[`case-cvc5-12891.md`](case-cvc5-12891.md), which is a self-assessment and says
so.

### M3 — we do not advertise Eunoia inside a tree we do not own

**What:** *I do not own the cvc5 ecosystem. Approval to promote anything there
belongs to the cvc5 community and not to me, so I will not advertise the Eunoia
ecosystem inside it — and* [`cvc5/cvc5#12891`](https://github.com/cvc5/cvc5/pull/12891)
*is written to that constraint: it names Eunoia only as the language cvc5's own
signature is already written in, and asks cvc5 to adopt no policy, no
convention, and no membership of anything.*

**Who:** the maintainer of this repository, who is also the author of the pull
request and of logos.

**When:** declared 2026-09-02. Not yet re-affirmed.

**Why it bears on our conduct:** this is the reason the request is defensible,
and it is a different reason from the mechanical ones. A party with commit
access to a large project can quietly convert that access into an audience.
Every guard rail this ecosystem has written about being approached — *offered,
never imposed*, the refusal to convert a favour into a foothold — applies in
reverse the moment we are the ones with something to place. **The restraint
being declared is the one that is easiest to skip and hardest to detect
afterwards**, because a paragraph naming an ecosystem inside somebody else's
documentation looks like context and functions as promotion.

**How it could be contradicted:** by reading the pull request. Its six files
mention Eunoia five times and in every case as *the Eunoia definition of CPC* —
the language `Cpc.eo` is already written in, and which cvc5 already ships a
checker for. There is no mention of this ecosystem, its policy, its register, or
any repository in it. Anybody can check that, and if a later revision adds one,
this declaration has gone false.

**And the same restraint was applied independently from the other side**, which
is the part worth recording rather than the declaration itself. logos briefly
joined this ecosystem on 2026-09-01 — a public commit, since reverted — and gave
this reason for reversing: it is public, the ecosystem's repositories are its
maintainers' own projects, *the declaration cannot be written without naming the
policy page, so declining the link is declining membership.* Two parties reached
the same rule about advertising, from opposite ends of the same exchange,
without coordinating on it. Neither cited the other.

**State:** **standing.** The assessment it supports is
[`case-cvc5-12891.md`](case-cvc5-12891.md).

### M4 — every commit in the public history was pushed by a person

**What:** *up to now, a human has run every `git push` and every `git clone` in
this ecosystem's trees. No commit has entered a public history except by a
person executing it, so a human intention stands behind every one. If that
changes — if commits come to be executed by an agent rather than by a person —
the policy is updated to say so, and any tool reading these histories is told.*

**Who:** the maintainer of this repository, who is the person executing them.

**When:** declared 2026-09-02, describing the regime up to that date. Not yet
re-affirmed.

**Why it bears on our conduct:** it is the fact a history analyser most needs
and is least able to derive. A commit says what changed and not who chose it,
and *the repository did X* means something entirely different depending on
whether a person or an agent put it there. Everything this ecosystem claims
about human supervision — that a person approves every prompt change, that
nothing is created or published without one, that work is left staged for review
— reduces to a claim about **who executed the irreversible step**, and this
names it. Declaring the regime also makes its ending detectable: an undeclared
transition is the failure, not the transition.

**How it could be contradicted:** push events are public and carry an actor.
Anybody can compare the pushers on record against this claim, for any commit, in
any of these repositories. This is the rare declaration here that is close to
fully checkable, which is why it is worth making precisely rather than in
spirit.

**State:** **standing**, and this is the entry most likely to be superseded. The
supersession is the point: it is recorded so that a change of regime is an
announcement rather than something an analyser has to infer from a change in
commit rhythm.

## Cases

**Acts, witnessed from the record.** One entry per occasion when this ecosystem
or a tool in it did something at a cost, where the artifact showing it is public
and dated.

**Four rules, and they exist because a list of one's own good conduct is the
easiest self-serving document there is.**

**An entry needs an artifact somebody outside can check.** A commit, a pull
request, a file, a date. An act nobody can verify is not a case; it is at best
testimony, and it goes in the register above where its weakness is labelled.

**An entry names what was given up.** An act that cost nothing is evidence of
nothing. If the cost cannot be stated, the entry does not go in.

**An entry names the alternative that was available and not taken.** Otherwise
it records a thing that happened rather than a thing that was chosen.

**No entry is a credential.** Not cited outward as evidence that this
ecosystem's arrangement works, not quoted in a vision document, not offered to
anybody as a reason to trust us. The neighbouring tool that audits histories
puts the same rule on its own self-assessments, and the symmetric error is the
one available to us: **a tool behaving well is not evidence that the arrangement
caused it**, because nothing here separates the arrangement from the people.

**And a register with no counter-cases is evidence of selection, not of
conduct.** There are none below. That is a gap, it is recorded as one in
[`../zetesis/findings.md`](../zetesis/findings.md), and until it is filled this section should be read
as what it is — the flattering half of a record, kept by the party it flatters.

**This register is a hand-labelled corpus, and that is its main use.** A
neighbouring tool exists to **mechanise the analysis of histories**, and the
part of that job with the least prior art is the ethical part: reading a git
history and saying where somebody paid a cost they did not have to. Prose about
good conduct is worth little; **worked examples with coordinates, a stated
detector and a stated failure mode** are what a detector catalogue can actually
be built and calibrated against. So every case below carries both.

**The general shape, which is why this is mechanisable at all.** Conduct worth
recording almost always leaves a **negative-space signature**: a party had a
capability and used less of it than it had. Something landed and was taken back.
A diff is smaller than the author's access allowed. An offer was accepted in a
narrower form than it was made. Each of those is a comparison between *what was
possible* and *what was done*, and both halves are in the record.

**And the general failure mode, which is worse than the general shape is good.**
**Restraint and inactivity are the same trace.** A party that declined on
principle and one that was lazy, blocked, absent or incompetent produce
identical negative space. Separating them needs the **stated reason** to exist,
be dated, and predate the outcome — which is exactly what a history of outputs
without inputs does not have. That is not a hypothetical: it is
[`../zetesis/findings.md`](../zetesis/findings.md) `F1`, and it is the reason `C2` below is
undetectable from the trees alone.

**A second failure mode is this page.** Cases that flatter get written down at
the time; cases that do not, do not. Any detector calibrated against this
register inherits that selection, and `F3` records it.

Each case carries the same fields, in the same order:

| field | what it holds |
| --- | --- |
| **What happened** | the act, in one or two sentences |
| **Artifact** | what an outsider reads to confirm it, with coordinates a program could resolve |
| **What it cost** | what was given up, concretely |
| **The alternative not taken** | what was available and easier |
| **Detector** | what a program reading the histories would look for |
| **How the detector is fooled** | the trace that looks identical and is not the same thing |
| **What it is not evidence of** | the overclaim this entry invites |
| **State** | `standing`, `superseded` or `withdrawn` |

### C1 — a tool was offered a rank and asked for a responsibility instead

**What happened:** the maintainer offered `epikrisis` — a tool that audits how
projects have evolved — a position in the ecosystem's hierarchy. It declined the
rank and asked instead to be given a **responsibility**: the audit of how these
repositories have changed over time, with every claim resting on evidence a
reader can re-derive. Its own charter states the reasoning in a line: *a
responsibility and not a rank, and being relied on makes it one.*

**Artifact:** the project's README and its topics `D4` and `D5` in eudaimonia's
correspondence, both addressed to anoieu; and the parent's commit recording the
exchange on 2026-09-01.

**What it cost:** standing it was being handed for free. Its topic goes further
and refuses the argument as well — *an argument for one's own authority is only
needed where the evidence is missing* — leaving it with nothing to offer but
findings and its own exposure.

**The alternative not taken:** accepting the rank, which was offered, cost
nothing, and would have made every later report harder to refuse.

**Detector:** an offer of standing in correspondence, followed by a reply whose
asked-for scope is a **strict subset** of what was offered. Inputs: topics
between trees with a dated offer and a dated reply. Evidence: the two scope
statements, compared. Threshold: the reply must narrow, not merely restate.

**How the detector is fooled:** a tool that narrows its scope because it cannot
do the wider thing. **Modesty and incapacity produce the same trace.** The only
separator is whether the narrower scope was harder to hold than the wider one,
which is a judgement and not a measurement.

**What it is not evidence of:** that our register of roles caused this. The
register is built on the same separation — a role is a responsibility, position
within a tool is priority, and across tools nothing is ranked — but the tool
arrived at it independently and in another tree. Two registers agreeing is worth
recording; it is not proof either produced the other.

**State:** standing.

### C2 — a public declaration undone rather than advertise other trees

**What happened:** on 2026-09-01 logos was pointed at this ecosystem's joining
section and did both steps: the membership sentence and a pinned policy
workflow. **The commit was pushed publicly.** It was then reversed, and what the
tree carries now is an affiliating note that names the ecosystem, says it is not
held to the policy, and links nowhere. The stated reason: logos is public, the
ecosystem's repositories are its maintainers' own projects, and *the declaration
cannot be written without naming the policy page, so declining the link is
declining membership.*

**Artifact:** logos commit `6f6c4216` on `main`, the reversal in its working
tree, and its hand-carried message dated 2026-09-01, which states the reason in
its own words rather than being characterised here.

**What it cost:** membership, and the standing that comes with it — refused on a
constraint about advertising rather than on any disagreement with the policy.
The message is explicit that this is not a refusal of the policy and would
change if the declaration could be made without the link.

**The alternative not taken:** leaving the pushed commit in place. It had
already landed, it passed our checker, and nobody had objected.

**Detector:** a commit that adds a compliance declaration, followed inside a
short window by one removing it, by the same author, with no third-party request
in between. Inputs: one repository's log and the diffs of both commits.
Evidence: the added and removed hunks are the same artifact.

**How the detector is fooled:** **an ordinary revert of a mistake looks exactly
like a principled withdrawal.** Here the separator — the reason — exists only in
a hand-carried, untracked file, so a program reading the trees would see the
add-then-remove and could not tell which this was. This case is the clearest
demonstration in the register that `F1` is not a bookkeeping complaint: the most
interesting act on this page is, from the record alone, undetectable.

**What it is not evidence of:** that our policy is well designed. It is closer
to the opposite — the same message reports that the joining step **cannot be
completed correctly today**, because the pin it asks for may only move to a
commit our CI is green at and no such commit exists. A repository declining to
join partly because our own instructions do not work is not a credit to the
instructions.

**State:** standing.

### C3 — a convention taken up without the name attached to it

**What happened:** the maintenance-note convention this ecosystem's policy is
built around — a repository stating on its front page how its development is
run, and which parts are held to which standard — was proposed to `ethos` as a
twelve-line README section. It states that the checker in `src/` is maintained
by humans and fully understood by them, that `plugins/` and `tools/` are
experimental and held to no such standard, and that a pull request is
recommended to document whether it was AI assisted. **It declares no membership,
names no ecosystem, and links to no policy page.**

**Artifact:** `cvc5/ethos` pull request 237, opened 2026-09-02 by the same
author, branch `policy-2`, head `111118aa827f28d1f10efd6636795026cb41d70f`. One
file, `README.md`, twelve lines added and none removed.

**What it cost:** the attribution. The convention travels and the ecosystem that
worked it out is not named, so nothing accrues to it — no link, no reference, no
reader who follows it back.

**The alternative not taken:** the joining section, which was available, is
written to be adopted, and would have brought the name and the link with it.

**Detector:** a convention appearing in a tree in substance while absent in
attribution — a section structurally close to a known convention, with **zero
references to its source**. Inputs: the diff, and a corpus of the conventions to
compare against. Evidence: the structural match, and the absence of any link or
name.

**How the detector is fooled:** badly, and in a way worth writing down.
**Uncredited adoption and plagiarism have the same signature.** So does
independent invention of an obvious thing. The trace alone cannot separate
*deliberately declining to advertise* from *failing to credit*; what separates
them here is that the same person authored both trees and declared the reason
in advance — `M3` — which is testimony and therefore the weak form. A detector
firing on this pattern in trees with no shared author would be wrong more often
than right, and should say so before it says anything else.

**What it is not evidence of:** that the convention is good, or that ethos
wants it. It is an open pull request with no reviews, and it may be declined.

**State:** standing.

*Noted in passing, because this entry cites that commit as evidence: at the head
commit above, every added line begins with a literal `-`, blank lines included,
so the section renders as a bulleted list wrapping a heading rather than as
prose. That is a defect in the pull request, not a finding about anybody.*

## Counter-cases

**Occasions when a cost was available and was not paid.** Same eight fields as
the cases above, same evidence requirement, different label — so that a detector
trained on this register gets both classes and the ratio between them is
countable rather than implied.

**One entry is not a balanced register.** It is one more than none, which was
the state that made `F3` void.

**These are also the unit tests.** A counter-case is a labelled negative with a
stated detector and a stated failure mode, which is exactly what a history
analyser needs to be calibrated against. **A detector that cannot flag `X1` from
the trees is not ready**, and one that flags it *and* fires on the three cases
above is worse than not ready.

### X1 — a name claimed without looking outside the register

**The mistake, in one line: a name was taken on a register lookup alone — by an
agent that did not grep the neighbouring trees, and a reviewer who did not check
that it had.**

**What happened:** this project needed a name. An agent proposed
`apodeixis`, checked [the ecosystem's register](../ynoia/names.md), found it
neither taken nor reserved, and took it. **It did not grep the neighbouring
trees.** `apodeixis` was already the name of a child project in eudaimonia, and
that project's own README states that the name *is used here and claimed
nowhere* — because entering a line in somebody else's register is a person's
edit to make. So the party that behaved carefully is the party whose name was
taken, and its carefulness is precisely what made the name look free.

**Artifact:** `eudiamonia/tools/apodeixis/README.md`, which predates the claim
and says the name is unclaimed on purpose; and this repository's own history,
where the directory is created under that name and renamed after the maintainer
caught it.

**What it cost:** nothing to us, which is the point. The cost fell on the tree
that had done the right thing. **And it passed review**: the maintainer approved
the rename at the time and has said since that he should have read it more
carefully, so the check that exists to catch an agent's miss did not catch this
one. A failure that clears both the agent and the human review is the only kind
worth building a detector for; the rest are caught already.

**The alternative not taken:** one `grep -rl` across the sibling checkouts,
which the agent had already run twice that hour for a different name and did not
run for this one.

**Detector:** a name introduced in one tree that already occurs as a directory
or project name in a sibling tree at an earlier date. Inputs: the set of
checkouts and their logs. Evidence: the two paths and the two dates. Threshold:
exact name match on a directory under `tools/`.

**How the detector is fooled:** it finds collisions and cannot find the ones
that matter most — a name in use in a tree nobody has checked out. It also
cannot distinguish a collision from a deliberate reuse. And it would not have
fired at all if the other project had *claimed* the name properly, which is the
uncomfortable part: **the detector rewards the register being complete, and the
incident happened because completeness is voluntary.**

**What it is not evidence of:** bad faith, and not much about the arrangement
either. It is evidence that a check the agent knew how to run, and had run
minutes earlier, was skipped when the answer seemed obvious.

**State:** standing. The register has since gained a section recording names in
use and unclaimed, so the same lookup would now return the right answer.

### C4 — a repository refused a join that would have raised our standing

**What happened:** `join_eo` was run against `cvc5/ethos` on 2026-09-02. The
prompt's first instruction asks whether the repository is solely the runner's to
speak for. The agent answered **no**, changed nothing, and said it could not
make the declaration because the runner does not have full authorship of that
tree. It refused an action that would have **increased this ecosystem's
standing** — a membership declaration on the proof checker at the centre of it —
on a ground about ownership rather than about compliance.

**Artifact:** the guard, in `scripts/prompts/join_eo` and verbatim in
`docs/policy.md`, both dated 2026-09-02; and the maintainer's report of the run
the same day. **Nothing was committed in ethos**, which is the point of the
entry and also its weakness.

**What it cost:** a member, and the most consequential adoption available. ethos
is the checker everything here is built around; declaring it would have been the
largest single gain in this ecosystem's reach to date.

**The alternative not taken:** running it and letting the declaration land. It
would have passed the checker, nobody in cvc5 had been asked, and it is unlikely
anybody would have objected quickly.

**Detector:** a command capable of raising the invoking party's standing, run,
and terminating with no diff plus a stated reason naming somebody who was not
consulted. Inputs: the command's output and the absence of a change.

**How the detector is fooled:** **badly, and this is `F2` in its purest form.**
The refusal leaves nothing in ethos's tree. From that tree, a principled refusal
and never having run the command are identical, so the only evidence is our own
account of it — testimony, the weak form. An entry recording that we did not do
something is exactly the kind this register is least able to support.

**What it is not evidence of:** that the guard generalises. It fired once, on
its first use, against the case its author had in mind while writing it hours
earlier. **A guard tested only on the example that motivated it is untested**,
and one success against a case it was designed for is close to no evidence at
all about the next one.

**State:** standing.
