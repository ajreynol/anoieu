# Reporting on code you do not own

The shared position of [anoieu](https://github.com/ajreynol/anoieu) and
[dokimasia](https://github.com/ajreynol/dokimasia). The tools have nothing in
common technically, but they are in the same situation: each reads somebody
else's work and says something about it that its owner did not ask for. That
situation has a discipline, and this page is it.

anoieu keeps the page; dependents reference it rather than restating it, so a
change of position is one argument in one place. Anything here that is wrong for
one tool is probably wrong for both.

**Where this sits.** Three documents govern the work rather than the tool.
[`policy.md`](policy.md) says how a repository is arranged.
[`vision.md`](vision.md) says what the development is aiming at. This one says
what may be *said about somebody else's code* — and it is the only one of the
three that binds a second repository, which is why it changes most carefully.
[`reporting-workflow.md`](reporting-workflow.md) is the procedure that
implements it: the conventions, the prompts, the CI integration.

**Citing and changing it.** Cite a position by name, not number — a reference to
*the settling artifact* can be checked by reading the sentence it sits in, and a
reference to "position 9" cannot. Append; never rename or renumber; retire a
position in place with a line saying why. Keep it free of mechanics: the test is
whether either tool, as it is today, could sign a sentence without pretending.

## What backs a position

[`vision.md`](vision.md) draws a line between what a machine decides and what
people argue about, and a page of positions is exactly where that line gets
blurred — a stated intention reads like a guarantee, and the reader cannot tell
them apart unless we say. So each position below carries a tier.

| tier | means |
| --- | --- |
| **enforced** | something fails when it is broken: a test, a CI job, or a generator that cannot express the violation |
| **structural** | the arrangement makes the failure hard rather than impossible. Nothing alarms, but you would have to work at it |
| **intention** | nothing but our record. Worth exactly what the log in [`reports.md`](reports.md) is worth, and no more |

Most of this page is **intention**, and that is not a defect to be apologised
for — *do not report a count you cannot calibrate* is not a thing a program can
check. It is a defect to be **shrunk**. Moving a position up a tier is the
ordinary way this page improves, and each one below says what would move it.

## What we publish

**1. Silence is never evidence.** *(intention.)* Where a check reports nothing,
the most that may be said is that *those checks reported nothing* — never that
anything is sound, consistent, or better than anything else. Our silence is weak
evidence and reads as strong, because every check is partial and each has been
narrowed until it stopped over-reporting. A reader who takes a quiet run for a
sound artifact has been misled by us, and the next effort inherits that
impression: **a false sense of security is much harder to withdraw than a wrong
finding.** Each tool says so where a reader arrives, in its own words, not on
the third click.

What this forbids is assurance *inferred from a tool falling silent*. An
assurance may be published as **an argument a reader can check** — one that says
what it covers, what it assumes, what would falsify it, and how to re-run it
without asking us. Arguing that a fragment of a system is free of a class of
defect is legitimate work, and is a different act from reporting that nothing
was found.

**2. Name the question you answer, and the one you do not.** *(intention.)*
anoieu asks whether a signature and its semantics say something coherent — not
whether a rule is valid. dokimasia asks whether any path through a solver can
produce no proof at all — not whether the proofs it does produce are valid. Both
sit one level below the question a reader cares about, and a tool that leaves
its scope vague is read as answering the larger one.

**3. Measure the subject, never our own coverage.** *(intention.)* How much of a
subject is reached by its own mechanisms is a finding like any other, often the
most useful one a tool produces. How much of it *we* looked at, or how many of
our checks passed, must never be published: nobody can calibrate that number,
**including us**. Counts of findings sit on the wrong side of the line often
enough to be worth naming — they say which of our checks tripped, not how much
of a subject is sound, and they are never comparable between subjects.

## What a finding is worth

**4. Publish a candidate; carry a finding.** *(structural.)* A finding is about
somebody else's file, so the tool is the smaller half of the work. Two acts, two
standards: a **candidate** may be published under our own name with whatever
evidence it has, labelled as unjudged — both tools' reports are mostly
candidates and pretending otherwise would empty them. A **finding** is carried
to the project that owns it only once confirmed: reproduced in the smallest
artifact that shows it, put to whatever the authority is, with the answer quoted.
What makes this structural rather than an intention is that the two live in
different files with different headers, so publishing a candidate as a finding
takes a deliberate act rather than a slip.

**5. Presence is not reachability.** *(intention.)* "This rule has no checker"
and "this rule has no checker and an ordinary run emits it" are different
claims, and only the second is worth somebody's time. Both tools learned this by
getting it wrong, which is why it belongs here and not in either one's notes.

**6. A false positive is ours — and so is anything we asked them to run.**
*(enforced, for the half that can be.)* A check that fired wrongly gets narrowed
until it stops, and the narrowing is recorded as what it was: something about
the subject we had wrong, in the terms the project used rather than kinder ones.
The enforced half is that a change *inventing* a false positive fails our own
build before it reaches anybody — CPC is pinned to a committed baseline with
warnings denied. The unenforced half is everything after that: whether the
narrowing was honest, and whether something of ours already in their tree gets
withdrawn when it misfires.

**7. Every claim is re-checkable without us.** *(enforced.)* A finding carries
the version it was measured at; a number carries whatever regenerates it. Not a
virtue but a testable property — a report about "the version on my laptop" is a
report about nothing, and a row nobody can re-measure cannot be argued with.
`tools/deps.lock` records the commits, and a CI job re-measures them and fails
when the report is no longer current for the versions it names. Argument is
exempt, being checkable by reading it; quantities are not.

## How the record moves

**8. Closing is a verdict, not an absence.** *(structural, with a known gap.)*
No row leaves the open list without one recorded, and "won't fix, because —" is
a verdict worth as much as a fix: it is usually a fact about the subject nobody
had written down. A finding that is merely no longer reported has not thereby
been fixed. The generator is additive and cannot delete a row, which is what
makes this structural — but nothing yet forbids a *hand* deletion, and closing
that gap is the first item in [`coherence.md`](coherence.md).

**9. A reply is triage; an artifact settles it.** *(intention.)* What comes back
from a project describes somebody's reading, made quickly and on our word. What
settles the matter is the artifact they produce — a merged change, a run that no
longer fails, an answer to a question — and which artifact counts is a property
of the claim, so each tool names its own. The half both tools get wrong under
pressure is the negative one: **failing to find a settling artifact settles
nothing.**

**10. Nothing crosses a repository boundary automatically.** *(structural, and
the strongest form available.)* No issue opened, no change filed, no comment
posted by machinery — not now, and not once there is tooling that could. It is
structural because no such code exists to be disabled: nothing in either tool
can post anywhere, and adding it would be a feature somebody would have to write
on purpose. Three reasons, in increasing order of importance. The cost falls on
the recipient, so spending their attention is a decision rather than a step. A
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
what the project says about itself** — [`policy.md`](policy.md) asks every
repository to end its README with a note on how its development is run — and
never by our impression of the code. Where there is no such note, the first
register applies, because guessing wrong in that direction is the cheaper error.

## What is claimed, and what is not

We do not control who runs these tools: they are public and read whatever they
are handed. These positions bind what *we* publish under our own name, which is
the part that was ours to decide.

Both are maintained largely by AI agents under light human supervision, stated
wherever output is published. *Light* is precise, not modest: a human directs the
work, reads what is published and decides what is filed, and **nobody vets the
internal design**. How a check works, and why it was narrowed the way it was,
has had no independent reviewer, and a defect there looks exactly like a defect
in the subject until somebody who knows the subject looks. That is a fact a
reader needs in order to weigh a finding, which is why it is here — not an
apology, and not a reason to discount the findings that carry a file and a line
number.

The audience is experts for the same reason. Someone who knows the subject can
read a finding, judge it in a minute and throw it out — and in throwing it out
has told us something that improves the tool. Someone who cannot is exposed
twice: to a wrong finding they cannot refute, and to a quiet run they cannot
interpret. These tools are also still being built, in the ordinary sense that
checks are added and removed week to week, so what they cover is what the last
stretch of work reached rather than a considered frontier. Ten readers who can
argue with us are worth more than a hundred who cannot.

## Dependents

Whoever edits a position should know what else moves.

| repository | how it adopts this |
| --- | --- |
| [anoieu](https://github.com/ajreynol/anoieu) | keeps the page; its own documents implement it |
| [dokimasia](https://github.com/ajreynol/dokimasia) | references it from its README, findings and workflow documents |

> **Outstanding.** This page was `docs/philosophy.md`, then
> `docs/reporting-philosophy.md`, and its positions have since been retiered and
> extended. dokimasia's links and any quotation of it are stale. Nothing here
> fixes that — position 10 forbids it — so it is a person's errand, and it is
> unfiled.
