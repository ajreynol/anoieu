# The reporting policy: what may be said about code we do not own

**This is the page the shared
[repository policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#the-discussion-file)
means when it says anoieu keeps the reporting policy.** It governs what these
tools publish about somebody else's project, what separates a candidate
published under our own name from a finding carried to its owner, and what may
be taken as material in the first place. It binds what *we* publish; it does not
restrict who runs these tools or what they do with the output.

It is **not** the mechanics. How a finding is recorded is
[`bug_db/README.md`](README.md), how one is closed is
[Closure](README.md#closure), and what a project did with one is
[`experience.md`](experience.md). Those change with the tooling; this changes
when a position changes.

## What backs a position

[`vision.md`](https://github.com/ajreynol/kanon/blob/main/docs/vision.md) draws a
line between what a machine decides and what people argue about, and a page of
positions is exactly where that line gets blurred — a stated intention reads like
a guarantee, and a reader cannot tell them apart unless we say. So each position
carries a tier.

| tier | means |
| --- | --- |
| **enforced** | something fails when it is broken: a test, a CI job, or a writer that cannot express the violation |
| **structural** | the arrangement makes the failure hard rather than impossible. Nothing alarms, but you would have to work at it |
| **intention** | nothing but our record, and worth exactly that |

Most of this page is **intention**, which is not a defect to be apologised for —
*do not report a count you cannot calibrate* is not a thing a program can check.
It is a defect to be **shrunk**. Moving a position up a tier is the ordinary way
this page improves, and each one says what would move it. **A tier may also go
down**, and one has; saying so is the point of recording them.

## What we publish

**1. Silence is never evidence.** *(intention.)* Where a check reports nothing,
the most that may be said is that *those checks reported nothing* — never that
anything is sound, consistent, or better than anything else. Our silence is weak
evidence and reads as strong, because every check is partial and each has been
narrowed until it stopped over-reporting. A reader who takes a quiet run for a
sound artifact has been misled by us, and the next effort inherits that
impression: **a false sense of security is much harder to withdraw than a wrong
finding.** Each tool says so where a reader arrives, in its own words, not on the
third click.

What this forbids is assurance *inferred from a tool falling silent*. An
assurance may be published as **an argument a reader can check** — one that says
what it covers, what it assumes, what would falsify it, and how to re-run it
without asking us. Arguing that a fragment of a system is free of a class of
defect is legitimate work, and is a different act from reporting that nothing was
found.

**2. Name the question you answer, and the one you do not.** *(intention.)*
anoieu asks whether a signature and its semantics say something coherent — not
whether a rule is valid. It sits one level below the question a reader cares
about, and a tool that leaves its scope vague is read as answering the larger
one.

**3. Measure the subject, never our own coverage.** *(intention.)* How much of a
subject is reached by its own mechanisms is a finding like any other, often the
most useful one a tool produces. How much of it *we* looked at, or how many of
our checks passed, must never be published: nobody can calibrate that number,
**including us**. Counts of findings sit on the wrong side of the line often
enough to be worth naming — they say which of our checks tripped, not how much of
a subject is sound, and they are never comparable between subjects.

## What a finding is worth

**4. Publish a candidate; carry a finding.** *(intention — and this tier went
down.)* A finding is about somebody else's file, so the tool is the smaller half
of the work. Two acts, two standards: a **candidate** may be published under our
own name with whatever evidence it has, labelled as unjudged — our reports are
mostly candidates and pretending otherwise would empty them. A **finding** is
carried to the project that owns it only once confirmed: reproduced in the
smallest artifact that shows it, put to whatever the authority is, with the
answer quoted.

**This was structural while the two lived in separate files with separate
headers**, so publishing a candidate as a finding took a deliberate act. One
database replaced the two ledgers on 2026-09-19 and that separation went with
them; what is left is a status column, which distinguishes *ruled on* from *open*
and does not distinguish *carried* from *published*. **What would move it back
up** is a field on an entry recording that it was carried, to whom and on what
date — which is also what `experience.md` needs in order to say whether the
reporting works or only the checks do. *Nothing crosses a repository boundary
automatically* still carries the part that matters.

**5. Presence is not reachability.** *(intention.)* "This rule has no checker"
and "this rule has no checker and an ordinary run emits it" are different claims,
and only the second is worth somebody's time.

**6. A false positive is ours — and so is anything we asked them to run.**
*(enforced, for the half that can be.)* A check that fired wrongly gets narrowed
until it stops, and the narrowing is recorded as what it was: something about the
subject we had wrong, in the terms the project used rather than kinder ones. The
enforced half is that a change *inventing* a false positive fails our own build
before it reaches anybody — CPC is checked against a committed baseline with
warnings denied, in the `corpus` job. The unenforced half is everything after
that: whether the narrowing was honest, and whether something of ours already in
their tree gets withdrawn when it misfires.

**7. Every claim is re-checkable without us.** *(enforced.)* A finding carries
the version it was measured at; a number carries whatever regenerates it. Not a
virtue but a testable property — a report about "the version on my laptop" is a
report about nothing, and a row nobody can re-measure cannot be argued with.
[`config/deps.lock`](../anoieu_analyzer/reporting/config/deps.lock) records the
commits, and `scripts/run.py --pinned --check` re-measures them in CI and fails
when the report is no longer current for the versions it names. Argument is
exempt, being checkable by reading it; quantities are not.

## How the record moves

**8. Closing is a verdict, not an absence.** *(enforced, and this tier went up.)*
No row is closed without one recorded, and "won't fix, because —" is a verdict
worth as much as a fix: it is usually a fact about the subject nobody had written
down. A finding that is merely no longer reported has not thereby been fixed.

What makes this enforced rather than structural is that a verdict is now a
**required word from a closed vocabulary** —
[Closure](README.md#closure) defines the seven,
`anoieu_analyzer/reporting/verdicts.py` holds the copy that runs, and
`tests/run.py` compares the two, so a verdict reworded past the list leaves the
vocabulary rather than leaving the audit. `accepted and fixed` additionally
requires `awaiting_landing` naming where the change is, which
`verdicts.py --check` reads back against each checkout. The writer is koine's
`koine_append_db`, which is additive and cannot delete a row.

**9. A reply is triage; an artifact settles it.** *(intention.)* What comes back
from a project describes somebody's reading, made quickly and on our word. What
settles the matter is the artifact they produce — a merged change, a run that no
longer fails, an answer to a question. The half we get wrong under pressure is
the negative one: **failing to find a settling artifact settles nothing.** Two
incidents in this repository's record are that mistake in each direction, and
they are written up in [`experience.md`](experience.md).

**10. Nothing crosses a repository boundary automatically.** *(structural, and
the strongest form available.)* No issue opened, no change filed, no comment
posted by machinery — not now, and not once there is tooling that could. It is
structural because no such code exists to be disabled: nothing in either tool can
post anywhere, and adding it would be a feature somebody would have to write on
purpose. Three reasons, in increasing order of importance. The cost falls on the
recipient, so spending their attention is a decision rather than a step. A
finding delivered by someone who can answer the follow-up gets read, and one
delivered by a bot gets a bot's welcome. And the finding you were most wrong
about is the one automation would have filed fastest, to the most people, with
the most confidence.

**11. Success is the check being deleted.** *(intention.)* The end state is the
invariant moving *into* the subject and taking our check with it — enforced by
the project's own tools, at the point the mistake is made. A check that lives
with us and could have lived there is a design failure, however many findings it
has produced; the best findings come with the argument for where the invariant
belongs. An invariant that spans repositories has no single owner to hand it to
and stays with us, which is a limit on this rather than an exception.

**12. Write for who maintains it, and let them tell you which that is.**
*(intention.)* A report is read by whoever is running the project, and that is
increasingly not a person. A project run by people gets an observation and the
benefit of the doubt: they made choices for reasons that need not be visible in
the tree, and an instruction presumes on all of it. A project run by agents gets
the finding stated flatly, with what to do about it, because there is nobody to
offend and hedging costs the reader time. **Which register applies is decided by
what the project says about itself** —
[`policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) asks
every repository to end its README with a note on how its development is run —
and never by our impression of the code. Where there is no such note, the first
register applies, because guessing wrong in that direction is the cheaper error.

## What we take

The positions above are about **output**. These two are about **input**, and the
gap they fill was found by eudaimonia walking into it: the only sentence anywhere
on the subject said that running the checks needs nobody's permission, which is
true of the act it describes and was never asked to license anything else.

**13. Published is not available.** *(intention.)* Reading a published artifact
needs nobody's permission, and neither tool asks for any. **Making somebody's
work the material of an exercise they have no stake in is a different act**, and
the licence for the first is not the licence for the second. The test is *who
carries the cost if the output is misread*: where the subject of an exercise has
no stake in the question, no say in how it is phrased and nothing to gain from
the answer, being within one's rights is not the standard that matters, and
asking is cheap. This is deliberately vague at the edges — every tool here reads
work whose authors did not ask to be read, and a rule that fired on all of it
would stop the work. **What it is not vague about is the direction to err in.**

**14. Unreleased work is nobody's material.** *(intention.)* Not drafts, not
preprints shared in confidence, not unreleased rule sets, not somebody's working
branch — **and this holds even where permission is given and the material is
handed over**, because what its authors have is the sole right to develop and
publish it first, and a tool that consumes it takes the most valuable thing they
have in exchange for nothing.

**What it forbids is making unreleased work the subject**: treating somebody's
unfinished branch as an exercise they did not ask for, or reporting on it as
though it described their project. It does not forbid *answering a question
somebody asks about our own pages* when the artifact prompting it happens to sit
on a personal fork — attributed, dated, and named as exploratory work that is not
a position of the project's. Dokimasia asked for the sentence that says which
reading is intended, in their `D15`; this paragraph is it, and the heading was
reworded from *unpublished* to *unreleased* to match. There is no balancing test
for the thing it forbids and no exception for good intentions.

**Why this is here and not in a checker.** Consent is not decidable from a tree.
A check firing on the shape of a paragraph would be a check firing on something
that is not a problem, which is the one thing this ecosystem is clearest about,
so [`policy_check.py`](../scripts/policy_check.py) says nothing about either
position and never will.

**No case is known in which this ecosystem has taken anybody's unreleased work**
— which is the reason to write the positions down, since a rule adopted after an
incident is read as an apology.

## What is claimed, and what is not

We do not control who runs these tools: they are public and read whatever they
are handed. These positions bind what *we* publish under our own name, which is
the part that was ours to decide.

This repository is maintained largely by AI agents under light human supervision,
stated wherever output is published. *Light* is precise, not modest: a human
directs the work, reads what is published and decides what is filed, and **nobody
vets the internal design**. How a check works, and why it was narrowed the way it
was, has had no independent reviewer, and a defect there looks exactly like a
defect in the subject until somebody who knows the subject looks. That is a fact
a reader needs in order to weigh a finding — not an apology, and not a reason to
discount the findings that carry a file and a line number.

The audience is experts for the same reason. Someone who knows the subject can
read a finding, judge it in a minute and throw it out — and in throwing it out has
told us something that improves the tool. Someone who cannot is exposed twice: to
a wrong finding they cannot refute, and to a quiet run they cannot interpret.
Ten readers who can argue with us are worth more than a hundred who cannot.

## Dependents

Whoever edits a position should know what else moves.

| repository | how it adopts this |
| --- | --- |
| [anoieu](https://github.com/ajreynol/anoieu) | keeps this page; its own documents implement it |
| [dokimasia](https://github.com/ajreynol/dokimasia) | signs every position and states its own tiers, which are higher than ours for three of them. Read 2026-09-19 |

**A dependent may reference or restate, and dokimasia does both.** Referencing
keeps one argument in one place; restating with local tiers says what a position
is worth *in that tree*, which this page cannot know. The rule is that a
restatement names this page as the position's origin and marks any tier that
differs, so the two can be compared rather than silently diverging.
