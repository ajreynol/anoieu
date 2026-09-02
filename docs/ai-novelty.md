# The mechanisms, and why they are subtle

**What this ecosystem is actually doing, mechanically.** Not whether it is good
— [`report-card.md`](report-card.md) grades that and remains the authority — and
not what of it generalises, which a child project in eudaimonia's tree asks in
its own register. This page asks the narrower question: *what are the moving
parts, and why is each one shaped the way it is?*

> **Experimental, and a companion to [`linker.md`](linker.md).** That page is
> the artifact — the rules resolved to where they are defined. This one is the
> account of why an artifact of that shape is worth having at all.

## This page does not brag

Stated as a working rule rather than as modesty, because a claim of novelty
about one's own practice is the single cheapest thing an agent can produce and
it reads exactly like an insight. Two disciplines, both borrowed from the
register that first applied them to this ecosystem from outside:

- **Every claim names what would show it false.** A claim with no falsifier is a
  slogan, and is marked as one here rather than dressed up.
- **The costs sit in the same list as the mechanisms**, not in a section at the
  end that can be skipped.

Nothing below is a claim that any of this is unusual. Several of the mechanisms
are ordinary engineering practice arriving somewhere it had not been tried; that
is a weaker and more useful claim than novelty, and it is the one being made.

## The central mechanism: clear writing is what makes this fast

The thing that looks like a style preference and is not.

**An agent's scarce resource is attention over text**, and almost every cost in
this ecosystem is a reading cost. A sentence that can be read two ways is not a
small blemish: it is a branch, and the wrong branch is discovered later, in a
different file, by which point the work built on it has to be undone. A precise
sentence is not a nicety on top of the work — it is the difference between one
pass and three.

That inverts the usual economics. Documentation is normally a tax on delivery,
written afterwards, by someone who has stopped wanting to. Here it is upstream
of delivery: the corpus is the input, so its quality sets the rate. **Ambiguity
is the expensive thing, not length** — though length is expensive too, which is
why the two rules that follow pull against each other and both have to hold.

The mechanisms that follow from it are all the same move — *replace a
conversation with a fact*:

- **The coverage gap is printed on every run.** The policy checker lists what it
  **cannot** decide, with the reason. A green result stops implying coverage it
  does not have, so nobody has to ask.
- **Every prompt takes `--show-prompt`.** What would be sent can be read without
  being sent, so reviewing a prompt costs nothing.
- **A rule names the incident that produced it.** A rule with no incident behind
  it is a preference, and the format makes that visible instead of arguable.
- **A field is left empty rather than filled with a placeholder**, because an
  empty field is visibly unanswered and a placeholder is not.
- **Every register says how to edit it, on the register.** The instructions are
  where the work happens rather than in a contributing guide nobody opens.

*What would show this false:* work here getting slower as the corpus gets
clearer, or the corpus getting clearer while the things it is supposed to
produce — checks, findings, adopted work — stay flat. The second is measurable
and the counter for it is in
[`coherence.md`](coherence.md#the-governance-budget). It is not currently
reading well.

## `vision.md` is the kernel

The most load-bearing analogy on this page, and worth being precise about.

A kernel is **small, loaded first, and privileged**: everything else runs
against its interface, and no program above it can revoke it.
[`vision.md`](vision.md) holds that position. It is short relative to what it
governs, it is the first thing a new repository is pointed at, and every other
document is written against it rather than beside it —
[`policy.md`](policy.md) is what it looks like to make part of it decidable,
and the checker is what it looks like to make part of *that* executable.

**Why it may never be checked mechanically** falls straight out of the analogy.
A checker for the kernel would have to sit above the kernel and would therefore
be the real kernel. Whether a tool is fruitful, whether a claim is oversold — a
program returning a verdict on those would be inventing an authority nothing
granted it. So the boundary is drawn by a test rather than by taste: *can a
program decide this from the tree without an opinion?* If yes it is policy, and
it moves down. If no it stays in the kernel and never acquires a checker. The
test runs both ways, which is the part that keeps it honest: a judgement
somebody works out how to check was probably policy all along.

**Where the analogy strains, and it strains badly.** A real kernel is enforced
by hardware; there is no privileged mode here and nothing stops a document from
contradicting the kernel except that somebody reads both. The protection is a
convention plus a person, which is the weakest form of protection there is. The
honest version is a kernel in a runtime with no memory protection: it works
because everything is cooperating, and it would not survive one participant that
was not.

**The kernel has a sibling question, and it is not in the kernel.** *What is
this work for* and *what are we held to, and could anybody check it* are two
halves of one thing, and only the first is here. The second is a child project
and governs nothing — deliberately, because a second page claiming kernel
standing is how an ecosystem ends up with two of them. It also argues that the
two pull in opposite directions on speed, and that this may be the point rather
than a cost.

*What would show this false:* a rule that matters turning out to live somewhere
other than the kernel and nobody noticing — which is a thing to look for rather
than a thing that has happened.

## A clear reference is a compiler optimization

The smallest idea here and the one most worth taking away.

A citation to a paper that settles a point **replaces an inlined derivation with
a call to something already compiled** — already argued, already reviewed, and
correct by the judgement of far more readers than this tree has. The saving is
not the words on the page. It is that the derivation does not have to be checked
here, by us, every time somebody reads it.

Three things follow, and the third is the one that bites.

**It is link-time, not compile-time.** The citation resolves in the reader's
head, and only if they have the paper. That gives it exactly the failure mode of
dynamic linking: a missing symbol at load, discovered by the reader and not by
the author.

**It is only an optimization if the reference is clear.** A citation to
something that does not actually settle the point is worse than the derivation
it replaced — a jump to a label that is not there — and it is harder to notice,
because a citation *looks* like rigour. The same holds for a link into another
repository, which is the one reference nothing here validates.

**A citation is a reference; a paraphrase is a copy.** Copies are the thing this
repository is most careful about — a prompt copied out of the document defining
it, a command table restated on a second page, a policy forked instead of
referenced. Each is a second definition of one symbol, and the failure is always
the same: they diverge, and the divergence is invisible from the side that
matters. Where a copy has to exist, something compares it; where it does not
have to exist, a reference is strictly better. That rule is why
[`linker.md`](linker.md) contains no tables of its own.

## Scripts are the ground truth

**A document describes; a script decides.** Where the two disagree, the script
is what ran, and the document is the thing to fix. This is a tenet rather than
an observation, and it is what keeps the corpus from becoming a description of
a system nobody has.

It sounds like it contradicts the section above and does not. They answer
different questions: the script says *what happens*, the document says *what it
is for*, and only one of those can be executed. The document is not a weaker
account of the script — it is an account of something the script cannot contain.

What makes it more than a slogan is that the gap is **checked**. The test suite
pulls the prompt out of the document that defines it, runs the script with
`--show-prompt`, and compares whole bodies; the same comparison is run over the
places that restate the epoch commands and statuses against the tables that
define them. Ground truth with copies and no comparison is the worst of the
three arrangements, because it looks like the safe one.

**Where it is not true yet, and this is the honest half.** The epoch system's
commands are not parsed by any program. Nothing rejects a malformed one, nothing
enforces a gate, and the role that holds the front end says so in its own entry.
For that system the ground truth is currently a *document*, which is the
arrangement this tenet exists to warn about. Naming it here does not fix it.

*What would show this false:* a drift check being narrowed to a substring match,
which is how this class of comparison usually dies quietly.

## The build system can be generalized, and has not been

The concrete wish, stated as a wish because nothing has been built.

**Today the epoch commands exist in one repository.** Reaching `staged` is
something only this tree can currently do, because the machinery and the surface
a person types at both live here. Every other member has the policy checker and
the reporting loop and nothing else: no command line of its own, no staging
step, no dry run.

**The wish is command-line tooling available to more tools in the ecosystem,
coordinated in how it is deployed** by the principles already written down
rather than by each tree inventing its own. Coordinated has a specific meaning
here, and it is four things, none of them new:

- **One definition per command.** A second tree gets the tool, not a copy of the
  table describing it.
- **One status vocabulary.** The words mean the same thing in every tree, or the
  announcements between trees stop being comparable.
- **Pinned, and fetched.** The same shape the policy checker already has: a
  member pins a commit, so nothing moves under a build without a commit near it.
- **Each member chooses when.** Taking a newer pin is their decision at a moment
  they pick, exactly as joining is.

**Some of the work is already done and is not called this.** The two roles are
written as separable on purpose — the machinery and the front end are separate
entries in [`roles.md`](roles.md) held by one tool today — so that moving either
one is a handoff rather than a rewrite, and the procedure for that handoff is on
the same page. The planned maintainer is named and does not exist.

*What would show the generalization is real:* a second tree running one of these
commands that it did not write, against its own state, and getting an answer its
maintainer acted on. Nothing has done this. Until something does, a build system
with one user is a script with ceremony, and calling it a build system is the
overclaim to watch for.

## What all of this costs

The section that keeps the rest honest.

**Governance is the cheapest thing here to produce, and nothing prices it.** An
agent can write a defensible page in minutes and every page is individually
defensible; the total is what nobody was counting until recently. The counter is
in [`coherence.md`](coherence.md#the-governance-budget) and these two pages are
on the wrong side of it — they are written prose, they displace nothing yet, and
the thing that has to pay for them is what [`linker.md`](linker.md) saves the
next reader.

**Diagnosis is not treatment**, and this ecosystem is much better at the first.
Writing an account of one's own mechanisms is exactly the activity that feels
like progress and is not, and the sharpest criticism it has received from
outside is that the quality of its self-criticism has been functioning as a
substitute for the work rather than a spur to it. That criticism applies to this
page more than to most.

**One reading, one tree.** Everything above is drawn from this ecosystem, which
is small, young, and mostly written by agents under one person's supervision.
None of it has been tried anywhere that did not already believe it.
