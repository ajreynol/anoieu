# Reporting on code you do not own

The shared position of [anoieu](https://github.com/ajreynol/anoieu) and
[dokimasia](https://github.com/ajreynol/dokimasia). The two tools have nothing
in common technically — different inputs, different questions, no shared code —
but they are in the same situation: each reads somebody else's work and says
something about it that its owner did not ask for. That situation has a
discipline, and this page is it.

anoieu maintains this page. dokimasia references it rather than restating it, so
that a change of position is one argument in one place rather than a divergence
nobody notices. Anything here that turns out to be wrong for one tool is
probably wrong for both.

Eleven positions, in four parts.

## What we publish

**1. Defects, never assurances.** No "this is sound", no coverage score, no
"consistent", no ranking of one project against another. Where a check reports
nothing, the most that is ever said is that *those checks reported nothing*.

The reason is asymmetry. Our silence is weak evidence and reads as strong: every
check is partial by construction, whole classes of error have no check at all,
and each check has been narrowed until it stopped reporting things that were not
defects. A reader who takes a quiet run for a sound artifact has been misled by
us — and worse, the next analysis effort inherits that impression and starts out
believing the ground is already covered. **A false sense of security is much
harder to withdraw than a wrong finding.**

The one exception is discussion of an ecosystem as a whole, where the subject is
an arrangement and its trade-offs rather than an audit of anybody's artifact.

**2. Say it out loud, not in a footnote.**

> **A successful pass is not a clean bill of health.**
>
> When the tool reports nothing, that is a fact about the checks it ran, not
> about your code. A green run — here, in your CI, or at the end of a report —
> is not evidence that anything is correct, and nothing downstream should treat
> it as such.

That belongs where a reader meets the tool, not in a document they reach on the
third click. A caveat nobody reads is a caveat that does not exist.

**3. Name the question you answer, and the one you do not.** anoieu asks whether
a signature and its semantics say something coherent — not whether a rule is
valid. dokimasia asks whether a solver can justify what it decides — not whether
the decision is right. Both questions sit one level below the one a reader
actually cares about, and a tool that leaves its scope vague will be read as
answering the larger one. Saying which is which costs a sentence and buys the
right to be trusted on the smaller claim.

## What a finding is worth

**4. It is about somebody else's file, so the tool is the smaller half.** A
finding has to be published where its owner will read it, argued where they can
disagree with it, and tracked until it is resolved or declined. A tool that
finds something and has nowhere to put it has not finished.

**5. It was confirmed before it was filed.** Reproduced in the smallest artifact
that shows it, and run through whatever the authority is — the real checker, the
real solver — with the output quoted. A finding that has only been reasoned
about is a hypothesis.

**6. A false positive is our bug, not theirs.** The check gets narrowed until it
stops, and the narrowing is recorded as what it was: something about the subject
we had wrong. This is the most valuable thing that can come back to us, and it
should be written up in the terms the project used rather than in kinder ones.
A check that was wrong once will be wrong again for somebody with less patience.

**7. A finding is relative to a version.** Measured against recorded commits,
reproducible by anyone from the record alone. A report about "the version on my
laptop" is a report about nothing, and a row that cannot be re-measured cannot
be argued with.

**8. Declining is an outcome.** A finding can end in "won't fix" with a reason,
and that reason is often worth more than the fix — it is usually a fact about
the subject that nobody had written down. Both beat an argument repeated
monthly.

## How the record moves

**9. Generation adds; only a person removes.** The report is additive: the tool
writes a row and never deletes one, and a row leaves the open list because
somebody decided it should, with a verdict recorded. The asymmetry matters
because a generator that can delete can quietly delete a regression.

Two corollaries. **A finding that is no longer reported is not thereby fixed** —
it may have moved, or a check may have been narrowed. And **closing means
moving, not deleting**: a deleted row is found again on the next run, so only a
recorded verdict makes a decision stick.

**10. A reply is triage, not status.** What comes back from a project describes
somebody's reading, made quickly and on our word. What settles the matter is the
branch: whether it merged, what review did to it, what the commits after it look
like. So a reply opens a question rather than closing one.

This has a formatting consequence worth keeping: what an assistant concluded and
what a person decided go under separate labels and never run together. A record
that mixes them ends up claiming something was settled when what happened is
that something was suggested.

## Where the boundary is

**11. Nothing crosses a repository boundary automatically.** No issue opened, no
pull request filed, no comment posted by machinery — not now, and not once there
is tooling that could. A finding travels because a person carries it, and comes
back because a person sends it.

Three reasons, in increasing order of importance. The cost of a finding falls on
the recipient, not on us, and spending somebody's attention is a decision, not a
build step. A finding delivered by a person who can answer the follow-up
question gets read, and one delivered by a bot gets a bot's welcome. And the
finding you were most wrong about is the one automation would have filed
fastest, to the most people, with the most confidence.

**A note on what this does not claim.** We do not control who runs these tools:
they are public and read whatever they are handed. What these positions bind is
what *we* publish, under our own name — which is the part that was ours to
decide.

**And on how they are maintained:** largely by AI agents under human
supervision, which is stated wherever the output is published rather than left
to be discovered. Work is left staged for a person to review; the agent's part
and the person's part stay distinguishable in the record for the same reason
they do in a reply.

---

How each tool puts these into practice differs. anoieu's mechanics are in
[`triage.md`](triage.md) — the report, the ids, the shape of a reply — and the
workflow around them in [`workflows.md`](workflows.md); both are written so
another tool can adopt them by substituting its own files.
