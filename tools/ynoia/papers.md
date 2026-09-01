# Which projects are worth a paper

**One entry per tool in the ecosystem, saying whether the work in it has a paper
in it.** [`../../docs/policy.md`](../../docs/policy.md) asks a repository with a
result to write it up as a LaTeX document in `report/` — eight to twenty pages,
addressed to a human who will never clone the tree — and
[`../../docs/vision.md`](../../docs/vision.md) argues why. Neither says which
repositories have one. This page is that judgement, and it is a judgement, which
is why it is here rather than in either of them.

**The artifact is a *paper* and the directory is `report/`.** Both words are
already in use: this ecosystem's *reports* are the findings ledgers under
`docs/reports/`, which are about somebody else's code and are read by whoever
owns it. A paper is the opposite artifact — it is about our own work, it is read
by somebody with no stake in it, and nothing generates it. Where this page says
*paper* it always means the second.

**This page decides nothing**, like every other page here, and it decides less
than most. A repository's own stance settles the question for that repository: a
maintainer who says *there is nothing here worth writing up* has applied the
convention rather than failed it, and this page records the disagreement without
resolving it. Nobody here can commission a paper, and nobody here writes one.

## What is on it, and what is not

| page | its question |
| --- | --- |
| [`names.md`](names.md) | what does this name mean, and is it free |
| [`proposals.md`](proposals.md) | should this be a repository of its own |
| [`requests.md`](requests.md) | whose tree should this work live in |
| [`tools.md`](tools.md) | which tool that does not exist is worth building first |
| **this page** | **which tool that does exist has a result worth writing up** |

The sibling to notice is `tools.md`. That page ranks work nobody has done; this
one ranks work somebody has. They ask the same question from opposite ends —
*is there something here* — and a tool appearing on both would be a contradiction
rather than a coincidence.

## The standard

Four questions, in order. A tool that fails an early one does not need the later
ones answered.

1. **Is there a result, or only a tool?** A working tool is not a paper. The
   question is whether something is now *true* that was not known before — a
   defect class nobody had named, a measurement nobody had taken, a construction
   nobody had shown was possible. A document describing what the tool does is
   documentation, and the repository already has some.
2. **Would somebody outside read it?** The reader is a human who does not carry
   this ecosystem in their head and owes it nothing. If the result cannot be
   stated without first explaining four of our repositories, it is an
   arrangement's internal news rather than a finding.
3. **Can every number in it be re-taken?** Argument is checkable by reading;
   quantities are not. A paper whose measurements cannot be regenerated from
   recorded commits is worse than no paper, because it converts a soft claim into
   a citable one.
4. **Is it a paper, or somebody else's chapter?** Two tools that produced one
   result between them should write one paper, and which tree it lives in is
   their decision and not this page's. The commonest wrong answer here is two
   thin papers where the honest artifact is one.

The likeliest right answer is **no**, and that is the point of asking. Most
repositories are successes with nothing publishable in them, and a page that
found a paper in every tool would have stopped being a judgement.

## How to read it, and how to edit it

**Position is the priority**, as on [`tools.md`](tools.md) and
[`../../docs/board.md`](../../docs/board.md): the first entry has the most
paper in it. Reordering is done by moving a block.

Four labelled fields each, the same four every time, always present, and a field
with nothing in it says so in words:

| field | what it holds |
| --- | --- |
| **Stance** | what the repository itself says about publishing, quoted or summarised — or `unstated`. It outranks everything else in the entry |
| **Verdict** | `write it`, `not yet`, or `no` |
| **The paper** | one line: what it would be about. Not the case for it |
| **Why** | the argument for the verdict and for the position, which is the field worth disagreeing with |

**A stance outranks a verdict.** Where a repository has said it does not intend
to publish and this page says `write it`, the repository is right and the entry
stays as a recorded disagreement. That is not deference for its own sake: the
cost of writing eight pages falls entirely on them, and a register that could
spend somebody else's fortnight would need an authority nobody here has.

---

## dokimasia — what no proof step covers

**Stance:** `unstated`.
**Verdict:** **write it.**
**The paper:** how much of a production solver's proof production has no proof
step behind it, measured by reading the code that emits proofs rather than the
proofs it emits.
**Why:** first, because it is the only entry whose question survives the second
test with nothing stripped out. *Which parts of this solver can reach a
conclusion it cannot justify* is legible to anybody who works on solvers, needs
none of this ecosystem explained, and is a question people ask about systems that
have nothing to do with Eunoia. The evidence is a real codebase at recorded
commits, so the third test is a matter of citing the lock rather than of building
anything. Its risk is the second half of the reporting position it shares with
anoieu — presence is not reachability — and a paper that reports uncovered
inferences without saying which are reachable would be the most quotable wrong
number this ecosystem has produced.

## logos and ethos-eoc — one result, two trees

**Stance:** `unstated`, in both. Neither has joined the ecosystem, which makes
this entry weaker than the one above rather than stronger: nothing here is a
claim on either tree.
**Verdict:** **write it**, once — and which of the two trees carries it is
theirs to decide, not this page's.
**The paper:** a proof calculus and its semantics compiled into a proof
assistant, with the soundness of every rule stated and discharged in the emitted
development — what the construction is, what the statement actually covers, and
what it costs to regenerate when the calculus moves.
**Why:** the largest genuinely new thing in the ecosystem, and the answer to the
fourth question is what puts it here rather than first. The compiler without the
development is machinery with nothing established by it; the development without
the compiler is one large Lean project whose interesting property — that it was
*generated rather than chosen* — is invisible. Two papers would each be missing
the other's half. What holds it back from the top position is the second
question, not the first: the construction is real, and the incompleteness of the
soundness development is the fact the paper has to open with rather than work
around. **euthyna**, the child project measuring exactly that, is why the paper
is closer than it looks.

## anoieu — a checker's silence, read as a defect

**Stance:** `unstated`, and this repository keeps the page that asks for one,
which makes the omission worse rather than excusable.
**Verdict:** **write it.**
**The paper:** what can be found by reading a proof calculus's signature, its
semantics and its embedding against one another — three artifacts with three
owners that nothing else compares — and what class of defect that catches which
running the checker does not.
**Why:** it has the material and not the frame. One round of findings was carried
to a project that answered, the verdicts are recorded, and the postmortem of that
round is more honest than most published evaluations. What is missing is the
sentence a paper is built on: what *kind* of defect lives in the gap between a
signature and its semantics, and why a checker cannot report it. Until that is
written the paper is a tool description with a findings table, which is the shape
the first question exists to refuse. The counts also need care — this repository's
own position forbids publishing coverage of its own checks, and a paper is
exactly where that rule is hardest to keep.

## sapheneia — where a manual is silent

**Stance:** `unstated`. It is a child project and speaks through its parent.
**Verdict:** **not yet.**
**The paper:** what two independent descriptions of one language disagree about,
and what that says about where the language is actually undefined.
**Why:** the shape is good and the evidence is not there yet. A second reading of
a language becomes a result when the disagreements are enumerated, carried to
whoever owns the first reading, and answered — the disagreement is the finding,
and an unfiled disagreement is one project's opinion of another's prose. **What
would change it:** a counted set of divergences between the manual and the
definition, with the answers that came back.

## eudaimonia — the template with one instance

**Stance:** `unstated`.
**Verdict:** **not yet.**
**The paper:** what generalises across calculi when the calculus is taken out of
a verified checker and its proofs, and what turns out to have been specific to
the first one.
**Why:** it has one instantiation, and a template with one instance is a design.
Everything the paper would claim about generality is currently a prediction made
by the people who wrote it, which is the weakest evidence available. **What would
change it:** a second calculus, from somebody who did not write the template —
at which point the paper is worth more than either of the entries above it,
because it would be the only one here reporting a negative result somebody could
not have guessed.

## euthyna — a chapter, not a paper

**Stance:** `unstated`.
**Verdict:** **no**, on the fourth question.
**The paper:** `nothing` on its own. What it has established — what the generated
development is made of and where its weight sits — is the section the logos and
compiler paper needs and cannot write about itself.
**Why:** this is the verdict the fourth question exists to produce, and it is a
compliment rather than a dismissal. An audit of somebody else's proof is the
measurement that makes their claim credible, and splitting it into its own paper
would leave both halves weaker: theirs unmeasured, and this one a set of numbers
about a development the reader has not been shown.

## koine — shared machinery, and nothing to report

**Stance:** expected to be that there is nothing here worth writing up, and this
page expects it to be right. `unstated` until its maintainer states it.
**Verdict:** **no.**
**The paper:** `nothing`.
**Why:** it is one implementation of a protocol several repositories were already
running by hand. That is a real success and it is entirely local: nobody outside
this ecosystem has the problem, and the solution is the obvious one. It is the
worked example this page needs — a working, useful, well-scoped tool with no
paper in it — and a register that could not return this verdict cleanly would be
a register that finds a paper wherever it looks.

## ynoia — argument is not a result

**Stance:** there is nothing here worth writing up, and this page says so about
itself first so that the verdicts above are readable as judgements rather than as
modesty spent on others.
**Verdict:** **no.**
**The paper:** `nothing`.
**Why:** this project's output is argument, and it has taken no measurement.
A paper assembled from it would be a position piece about how to arrange an
ecosystem, written by the ecosystem, with nothing in it a reader could check.
The account is worth reading and it is worth disagreeing with; neither of those
makes it a result.

## workflow-launcher — too early to ask

**Stance:** `unstated`.
**Verdict:** **no**, and the first question is where it stops.
**The paper:** `nothing`.
**Why:** its own front page says it holds no responsibilities and that nothing
depends on it. There is no result because there is not yet any work whose result
it could be, and asking this question of it now would be the register
manufacturing an entry to look complete.

## The ones this page does not judge

**cvc5** is outside the ecosystem and the ecosystem exists to serve it. It has
its own governance, its own scale and an audience that is not ours, and the
policy's position on it is that we do not ask it to adopt anything — which
includes this. No entry, deliberately.

**ethos** is not a member either, and it has maintainers, a manual and a
publication history that were settled long before any of this. Nothing here is
asking it for a paper, and an entry judging whether it has one would be this
register mistaking a page nobody consumes for a standing somebody has to answer.

## The one with no tree

The most publishable idea in this ecosystem belongs to no repository in it:
**why a proof calculus in a small language, checked by a small checker, and
*separately* compiled into a proof assistant — rather than emitting proof-assistant
proofs directly.** That is a real design question with two coherent answers, real
consequences either way, and an audience well outside these trees.

It is nobody's paper, which is why nobody will write it. Every repository here
holds one half of the argument and would be writing about its own decision, and
the account that states both halves — [`why-eunoia.md`](why-eunoia.md) — has
already returned the verdict `no` on itself above, for the reason that it has
measured nothing. **This is the gap worth recording rather than a task anybody is
being set.** What would close it is not a decision here: it is one of the tools
on [`tools.md`](tools.md) existing, so that the choice has been made twice and
the comparison is evidence rather than argument.
