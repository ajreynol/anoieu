# Reporting on code you do not own

The shared position of [anoieu](https://github.com/ajreynol/anoieu) and
[dokimasia](https://github.com/ajreynol/dokimasia). The tools have nothing in
common technically, but they are in the same situation: each reads somebody
else's work and says something about it that its owner did not ask for. That
situation has a discipline, and this page is it.

anoieu keeps the page; dependents reference it rather than restating it, so a
change of position is one argument in one place. Anything here that is wrong for
one tool is probably wrong for both.

**Citing and changing it.** Cite a position by name, not number — a reference to
*the settling artifact* can be checked by reading the sentence it sits in, and a
reference to "position 9" cannot. Append; never rename or renumber; retire a
position in place with a line saying why. And keep it free of mechanics: the
test is whether either tool, as it is today, could sign a sentence without
pretending.

## What we publish

**1. Silence is never evidence.** Where a check reports nothing, the most that
may be said is that *those checks reported nothing* — never that anything is
sound, consistent, or better than anything else. Our silence is weak evidence
and reads as strong, because every check is partial and each one has been
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

**2. Name the question you answer, and the one you do not.** anoieu asks whether
a signature and its semantics say something coherent — not whether a rule is
valid. dokimasia asks whether any path through a solver can produce no proof at
all — not whether the proofs it does produce are valid. Both sit one level below
the question a reader cares about, and a tool that leaves its scope vague is
read as answering the larger one.

**3. Measure the subject, never our own coverage.** How much of a subject is
reached by its own mechanisms is a finding like any other, often the most useful
one a tool produces. How much of it *we* looked at, or how many of our checks
passed, must never be published: nobody can calibrate that number, **including
us**. Counts of findings sit on the wrong side of the line often enough to be
worth naming — they say which of our checks tripped, not how much of a subject
is sound, and they are never comparable between subjects.

## What a finding is worth

**4. Publish a candidate; carry a finding.** A finding is about somebody else's
file, so the tool is the smaller half of the work. Two acts, two standards: a
**candidate** may be published under our own name with whatever evidence it has,
labelled as unjudged — both tools' reports are mostly candidates and pretending
otherwise would empty them. A **finding** is carried to the project that owns it
only once confirmed: reproduced in the smallest artifact that shows it, put to
whatever the authority is, with the answer quoted.

**5. Presence is not reachability.** "This rule has no checker" and "this rule
has no checker and an ordinary run emits it" are different claims, and only the
second is worth somebody's time. Both tools learned this by getting it wrong,
which is why it belongs here and not in either one's notes.

**6. A false positive is ours — and so is anything we asked them to run.** A
check that fired wrongly gets narrowed until it stops, and the narrowing is
recorded as what it was: something about the subject we had wrong, in the terms
the project used rather than kinder ones. The same obligation follows anything
of ours that ends up in their tree; if it fires spuriously, we narrow it or
withdraw it.

**7. Every claim is re-checkable without us.** A finding carries the version it
was measured at; a number carries whatever regenerates it. Not as a virtue but
as a testable property — a report about "the version on my laptop" is a report
about nothing, and a row nobody can re-measure cannot be argued with. Argument
is exempt, being checkable by reading it; quantities are not.

## How the record moves

**8. Closing is a verdict, not an absence.** No row leaves the open list without
one recorded, and "won't fix, because —" is a verdict worth as much as a fix: it
is usually a fact about the subject nobody had written down. A finding that is
merely no longer reported has not thereby been fixed.

**9. A reply is triage; an artifact settles it.** What comes back from a project
describes somebody's reading, made quickly and on our word. What settles the
matter is the artifact they produce — a merged change, a run that no longer
fails, an answer to a question — and which artifact counts is a property of the
claim, so each tool names its own. The half both tools get wrong under pressure
is the negative one: **failing to find a settling artifact settles nothing.**

**10. Nothing crosses a repository boundary automatically.** No issue opened, no
change filed, no comment posted by machinery — not now, and not once there is
tooling that could. Three reasons, in increasing order of importance. The cost
falls on the recipient, so spending their attention is a decision rather than a
step. A finding delivered by someone who can answer the follow-up gets read, and
one delivered by a bot gets a bot's welcome. And the finding you were most wrong
about is the one automation would have filed fastest, to the most people, with
the most confidence.

**11. Success is the check being deleted.** The end state is the invariant
moving *into* the subject and taking our check with it — enforced by the
project's own tools, at the point the mistake is made. A check that lives with
us and could have lived there is a design failure, however many findings it has
produced; the best findings come with the argument for where the invariant
belongs. An invariant that spans repositories has no single owner to hand it to
and stays with us, which is a limit on this rather than an exception.

## What is not claimed

We do not control who runs these tools: they are public and read whatever they
are handed. These positions bind what *we* publish under our own name, which is
the part that was ours to decide.

They are maintained largely by AI agents under light human supervision, stated
wherever output is published. *Light* covers less than a reader might assume: a
human directs the work, reads what is published and decides what is filed —
**nobody vets the internal design.** How a check works, and why it was narrowed
the way it was, has had no independent reviewer, and a defect there looks
exactly like a defect in the subject until somebody who knows the subject looks.

Which is why the audience is experts. Someone who knows the subject can read a
finding, judge it in a minute, and throw it out — and in throwing it out has
told us something that improves the tool. Someone who cannot is exposed twice
over: to a wrong finding they cannot refute, and to a quiet run they cannot
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
