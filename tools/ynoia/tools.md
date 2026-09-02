# The tools that do not exist

**Every tool this project has named and nobody has built, in priority order —
most promising first.** Seven labelled fields each, the same seven every time,
and no argument on the page: the argument for each is in
[`why-eunoia.md`](why-eunoia.md) or in [`proposals.md`](proposals.md), and this
page links to it rather than restating it.

It exists because naming work that does not exist is most of what this project
produces, and until now the names were spread across an account nobody reads end
to end, a register that deliberately says nothing about merit, and an audit page
ordered by date. None of those answers the question somebody with an afternoon
actually has, which is *which one of these is worth starting*.

**This page decides nothing**, like every other page here. An ordering is a
judgement, it is this project's judgement, and the whole of what it costs to
disagree is moving a block.

## What is on it, and what is not

| page | its question |
| --- | --- |
| [`names.md`](names.md) | what does this name mean, and is it free |
| [`proposals.md`](proposals.md) | should this be a repository of its own |
| [`requests.md`](requests.md) | whose tree should this work live in |
| [`papers.md`](papers.md) | which tool that *does* exist has a result worth writing up |
| **this page** | **which of them is worth building first** |

**A tool is on this page when it does not exist and would be its own artifact.**
Work that belongs inside somebody's existing tree is a request and is next door;
that is the line, and it is why the dependency auditor `R1` is not here.

**A tool leaves this page when it exists**, rather than being marked done and
kept. **euthyna** left when eudaimonia started it and **koine** left when its
repository existed; both are now in
[`../../docs/roles.md`](../../docs/roles.md), which is where a tool with a role
is described. A page that keeps its graduates is a page whose first entries are
all finished work.

## How to read it, and how to edit it

**Position is the priority**, exactly as on
[`../../docs/board.md`](../../docs/board.md). The first entry is the one most
worth starting; the last is the least. Reordering is done by moving a block, and
that is the main way a person changes what this page says.

**The name is the id, and it is stable.** There are no numbers here because
there is already a register of names, and inventing a second key for the same
things would be one more thing to keep in step. A name is taken from
[`names.md`](names.md) and never reused for different work.

**Most promising means what it would change, weighed against whether anybody
could start it.** Both halves are load-bearing. A page ordered only by what a
tool would change puts the largest one first every time and is useless to
somebody with an afternoon; a page ordered only by cheapness is a list of things
not worth doing. Where the two pull apart, the entry's last field says so in
words rather than hiding it in the position.

**The ordering is the part to argue with.** Every other field is a summary of
something argued elsewhere, and correcting one is bookkeeping. **Why here** is
this page's own claim, it is the field that changes when an entry moves, and it
is the only thing here worth an afternoon of disagreement.

Nothing consumes this file yet. It is written to be *parsed later* rather than
parsed now: the same seven labels, in the same order, always present, and a
field with nothing in it says `nothing` rather than being left out.

| field | what it holds |
| --- | --- |
| **What** | one line: the artifact, not the case for it |
| **State** | `named`, `audited`, or `parked` — plus one clause saying by whom or since when |
| **Settles** | which arguments, objections, open questions or arrangements it moves, by their ids in [`why-eunoia.md`](why-eunoia.md) |
| **Costs** | where the difficulty actually sits. One line, and not a schedule |
| **Before it** | what has to be decided or built first, or `nothing` |
| **Today** | what stands in its place, or `nothing` |
| **Why here** | the argument for this position, which is the field that changes when the entry moves |

## Best practices for requesting a listing

**Somebody wants a tool named here.** Sometimes it is a person with an
afternoon; more often it is a repository that has noticed a hole next to itself
and wants the hole registered. Either is welcome, and none of what follows is a
gate — a request that arrives with none of it is still read, and the worst
outcome is an entry whose fields say `nothing` in several places, which is
information rather than a rejection.

**The one thing worth having first is the vision.** Not the code, not a design,
not a schedule: a written statement of what the tool is *for* — the artifact it
would produce, the consumer that would read that artifact, what it refuses to
answer, and what would show the idea was wrong. This page judges *which of these
is worth starting*, and the judgement is made against the vision. Where there is
none, the audit has to invent one in order to have something to weigh, and an
audit that invents what it is judging is grading its own work. That is the whole
of the argument, and everything below is it applied to two different situations.

### An internal project: have it hashed out already

An **internal** project is one this ecosystem would build, host or depend on —
a child project in somebody's tree, a tool a member would fetch, a piece of
shared machinery. For these the recommendation is strong, and it costs nothing,
because **the vision is already owed elsewhere**. The policy asks a child project
to open with the question it is trying to answer, the goals in order, the
wishue, and an explicit list of what is out of scope; the ecosystem's vision asks
that the consumer be named before the work starts, by tool and by artifact. A
request that arrives with those answered can be judged the day it arrives.

What it buys, concretely:

- **The verdict is about the idea rather than about the request.** Every field
  on this page is a summary of something settled elsewhere. When nothing has been
  settled, the entry becomes a paraphrase of a conversation, and the first person
  to disagree with it has to reconstruct what was actually proposed.
- **It survives being audited as a repository.** The standard in
  [`proposals.md`](proposals.md) opens by asking whether the thing exists
  anywhere yet and how many consumers it really has. Both are unanswerable
  without a stated scope, and an audit that reaches them with nothing to read
  produces *not yet* by default — which looks like a judgement and is not one.
- **It is the cheapest place to find out the scope is undecided.** A vision that
  is hard to write is not a writing problem. Where the name needs a paragraph of
  explanation and the paragraph does not come, what is unclear is what the tool
  does, and finding that out before a repository exists costs an afternoon rather
  than a namespace.

### A standalone project: less clear, deliberately

A **standalone** project is one that would be its own repository with its own
maintainer, possibly somebody who has never heard of this ecosystem and owes it
nothing. Here the recommendation is much weaker, and the asymmetry is on purpose.

**The vision would be theirs to write, and asking for it first inverts the
order.** A person who is going to build a thing finds out what it is by starting
it; requiring a settled scope before the repository exists asks them to commit to
a shape before they have the artifact that would tell them which shape is right.
Several entries on this page were named with no vision at all — a Greek word, a
paragraph in an account, and an argument that their absence distorts something —
and they are better for it. What is registered in that case is **a name and a
claim about priority**, not a plan, and the `named` state says exactly that.

So for a standalone tool the honest minimum is smaller: one line on the artifact,
and one line on what its existence would change. If the requester can also say
what stands in its place today, the entry is complete enough to be argued with.
Anything more is welcome and nothing more is expected.

The line between the two cases is **who ends up holding it**, which is the same
question the proposals standard has learned to ask last and should ask first. A
tool this ecosystem would depend on is one we are committing to read, pin and
live with, and we are entitled to have read its scope before doing that. A tool
somebody else is going to build for their own reasons is theirs, and a register
that demanded a business case from them would be a register nobody sends anything
to.

### What a request carries

Enough to fill the seven fields, or an honest gap where it cannot:

- **A name**, taken from [`names.md`](names.md) or proposed there. Never a
  second name for work already listed under one.
- **One line on the artifact** — what would exist that does not. Not the case
  for it; that goes somewhere it can be disagreed with.
- **What it would settle**, by the ids in [`why-eunoia.md`](why-eunoia.md) where
  it touches the account, and in words where it does not.
- **What stands in its place today**, including `nothing`. This is the field
  requests most often omit and the one that most often changes the position.
- **Where the vision is written down** — a charter, a README, a proposal, a
  message — or `nothing`, said plainly.

**A request with no vision is still listed**, as `named`, with the missing
statement recorded as the first thing standing in the way. What it cannot be is
*audited*: [`proposals.md`](proposals.md) asks four questions that a scope has to
exist to answer, and an audit run against a gap would return a verdict about this
project's imagination. That is the concrete consequence, and it is the reason the
recommendation is worth making at all.

---

## tekton — the epoch build system

**What:** one program behind the family of protocols by which a stretch is
verified, announced, approved and adopted — it evaluates every gate, runs the
tool for each, and delivers the evidence an agent composes the approval block
from. It also **holds the one authority nothing else may hold: moving a stretch's
status to `deployed`**, which is what tells the ecosystem the work is available
to consume.
**State:** `named` — requested by anoieu on 2026-09-01 as its highest priority,
and to be built and used in the **second** stretch, explicitly not this one. Until
it exists, the `deployed` transition is made by whoever holds `R28` on its behalf,
which is a stated bootstrap exception that ends when this ships. The vision was written down
first: the protocols exist, are in use, and are run by hand, so what is being
asked for is a tool and not a design.
**Settles:** nothing in [`why-eunoia.md`](why-eunoia.md) — it is not an argument
about the proof pipeline. What it settles is that this ecosystem's **main
verification system for its own governance** is currently four documents and one
person's attention, and that the artifact a person actually reads is assembled by
hand each time.
**Costs:** **it must not emit the finished block**, and that constraint is the
whole design. A program that printed one would let an agent pass it through
untouched -- identical output, an agent exactly as uninformed as before, and the
appearance of verification automated. Its job is to *deliver evidence to the
agent*; composing the target is the agent's, because composing it is where being
informed happens. A tool built the obvious way would defeat its own purpose.

Beyond that, the mechanical gates are cheap and the judgement fields are not.
*What comes out* and *has this been applied here* are decided by a person, and a
tool that guessed them would emit something that reads like a check and is not
one — which is worse than emitting nothing, because the shape carries authority
the content would not have earned.
**Also in its remit, and unsettled:** `epoch double check` — whether a
deployment was *properly received*. That is an open research question rather than
a feature: effects in a member's tree are observable and reception is not, and a
check that scored *no effect* as failure would be measuring compliance while
calling it something else.
**Before it:** the block's fields settling. They have changed twice in a day, and
a program written against a template still moving would be rewritten more often
than run. `nothing` else.
**Today:** [`../../tools/bump_check.py`](../../tools/bump_check.py) for one gate
of six; `git`, `grep` and a person for the rest; and the block typed out by hand.
**Why here:** **first, displacing `kanon`, and the two are not close.** Every
other entry on this page is work whose consumer does not exist yet. This one has
a consumer today, running the thing by hand, every time a stretch is considered —
and the cost of its absence is paid on exactly the occasions when getting it
wrong is most expensive. `kanon` remains parked by a person and its position
below is a statement about *when*, not about merit.

## kanon — the ecosystem's governance, out of the analyzer

**What:** the policy, its checker, the inventory and the joining scripts, in a
repository that is not also the tool that files findings against you.
**State:** `parked` — audited as `P2` in [`proposals.md`](proposals.md) with the
verdict **needed**; the maintainer is inclined and has said explicitly that it
is not actionable until they raise it again.
**Settles:** nothing in [`why-eunoia.md`](why-eunoia.md) — it is not an argument
about the proof pipeline. What it settles is that one repository currently
writes the rules a member is judged by *and* files the findings against them.
**Costs:** every member's pin moves once, at a moment each of them chooses, and
the cost grows with every member that joins before it happens.
**Before it:** `install_eo` settling, so that the audit which reads across the
policy and the findings is a one-line problem rather than two checkouts.
**Today:** all of it, inside anoieu — `docs/policy.md`, `tools/policy_check.py`,
`tools/ecosystem.json` and the `*_eo` scripts, already consumed by four trees.
**Why here:** first, and not being worked on, which is the split this field
exists to make. It is the only entry on this page whose consumers already exist
and already depend on the thing; nothing else here has a user at all. That it is
parked is a fact about *when*, decided by a person, and not a fact about how
promising it is.

## epikrisis — a repository of its own, and not ours to grant

**What:** the tool that audits how these repositories have changed over time,
with every claim resting on evidence a reader can re-derive, **promoted out of
its parent into a repository of its own.** It is the ecosystem's only source of
GitHub history analysis, and `docs/laws.md` already requires a president to
quote it rather than count for itself.
**State:** `proposed` — suggested by the maintainer, 2026-09-02. **Unlike every
other entry on this page, the thing already exists and works.** What is proposed
is a move, not a build.
**Settles:** that the ecosystem's history analysis lives **two levels down
inside another tool**, at `tools/workflow-launcher/tools/`, which our own
inventory validator rejects as malformed — a child whose parent is a child.
Nothing fails today only because it is not in the inventory. **A tool three
repositories are expected to rely on should not be reachable only by knowing
where somebody filed it.**
**Costs:** eudaimonia loses a child project it started, and whatever the parent
was getting from having it close. **We do not know what that is**, which is
itself a reason the decision is not ours.
**Before it:** nothing technical. **The one prerequisite is a person in
eudaimonia agreeing**, which is the whole of the difficulty — and there is an
argument to answer first. **epikrisis has already explained why it sits where it
does**, in a section of its own README headed *Why it is here rather than one
level up*: its host asks a question it has no instrument for, and epikrisis is
that instrument. **That is a reason, not an accident**, and a proposal to move it
has to beat it rather than ignore it.

**And there may be a cheaper fix that gets us what we actually want.** Our
complaint is that the ecosystem's only source of history analysis is
unregistered and reachable only by knowing where somebody filed it. **That is
solved by putting it in the inventory, not by moving it** — which would need our
validator's rule against a child of a child revisited, and that rule is ours.
**If registration is enough, the move is a want and not a need**, and this entry
should be read that way.
**Today:** running, unregistered, and depended on by two laws written in this
repository before anybody asked it whether it wanted the job. The second is the
sharper one: **a stretch's record must state how many commits each tool took and
how many are believed AI-generated**, and the second half of that is a
measurement nobody in this ecosystem can currently make. Across 323 commits this
stretch, every one is authored by a human and three name an agent. **A project
whose subject is how repositories evolve is where that question belongs**, and
naming it may do more to focus the tool than the promotion would.
**Why here:** **staged beside `kanon` and `tekton`, and not the same kind of
item as either.** Those two are `init_eo new` — nothing exists, and starting
them is ours to do. This is `init_eo from-child`, the work exists, and
**graduating a child project is its parent's decision.** It sits on this page as
something we want and have asked for, never as something we have planned.

*On the name: chosen in eudaimonia's tree, not ours. It is recorded in
[`names.md`](names.md) under names in use elsewhere, which is the section that
exists because this register once called a name free while a neighbouring tree
was already using it.*

## nomophylax — the laws, out of the hands of the party they bind

**What:** the tool that maintains `docs/laws.md` — the rules under which a
president writes the ecosystem's history — and checks that a closed stretch
entry was written the way the laws say. **Not a lawgiver:** amendments stay a
person's, and this holds the page, watches compliance, and proposes.
**State:** `named` — suggested 2026-09-02, the day the laws were first written
down. Not audited; there is no proposal for it yet.
**Settles:** nothing in [`why-eunoia.md`](why-eunoia.md). What it settles is a
defect `laws.md` states about itself in its first paragraph: **the president
writes the record and also the rules the record is kept under.** That is the
whole of the case for it, and the page makes the case better than this entry
does.
**Costs:** little today, because nothing depends on `laws.md` yet. **The cost is
in waiting** — the longer one party holds both, the more of the record was
produced under rules its own author could have shaped.
**Before it:** a second president. With one, the separation is theatre: there is
nobody yet whose stretch was judged by rules somebody else wrote. `kanon`
taking Stretch 1 is what makes this real rather than tidy.
**Today:** `docs/laws.md`, held by anoieu, which is the president it binds. It
says so on the page rather than hiding it.
**Why here:** **third, behind `tekton` and `kanon`, and ahead of everything
else.** It is not urgent — one stretch, one president, and the maintainer
reviews every commit, which is real oversight even if it is not independence.
It is placed above the research tools because **the defect it fixes gets worse
with every stretch that closes**, and the entries written before it exists
cannot be revisited later.

*On the name: νομοφύλαξ, guardian of the laws — an office that held the statutes
and checked that magistrates acted within them. It completes a family this
ecosystem already has by accident: `dokimasia` is the scrutiny **before** office
and `euthyna` the audit **after** it; this is the one that watches **during**.
`thesmos` — θεσμός, that which is laid down — was the alternative and is the
better name if the thing turns out to be a register of rules rather than an
office that guards them.*

## euboulia — the ethical advisor to whoever holds the laws

**What:** the ethics of this ecosystem, gathered into one place and given a
reader: **`nomophylax`**, the tool that holds `docs/laws.md`. It advises and
does not decide — **the laws are held by one party, amended by a person, and
advised by this one**, and none of the three is the other.
**State:** `named` — suggested 2026-09-02, alongside `nomophylax`. Not audited;
there is no proposal for it yet, and there is a real question below that a
proposal would have to answer first.
**Settles:** nothing in [`why-eunoia.md`](why-eunoia.md). What it settles is
that this repository's ethics work is **scattered across child projects of the
tool it is meant to hold to account**, which is the same defect `kanon` and
`nomophylax` each fix in their own area, in the one area where it is least
comfortable to say so.
**Costs:** the two ethics child projects here move out —
[`martyria`](../martyria/README.md), the actionable half, and
[`zetesis`](../zetesis/README.md), the general one — and **what they are
advising changes with them.** Today they examine anoieu's conduct. Under this
they would advise an office. **That is not a smaller job or a bigger one, it is
a different one**, and a proposal has to say whether both belong or only one.
**Before it:** `nomophylax`, obviously — an advisor with nobody to advise is a
register with extra steps. And a second president, for the same reason that one
gives.
**Today:** `tools/martyria/` and `tools/zetesis/`, inside anoieu, each a child
project of the repository whose conduct they assess. Both say so on their own
front pages; neither is thereby fixed.
**Why here:** **fourth, behind `nomophylax`.** It cannot be built before the
thing it advises exists, and it is placed above the research tools for the same
reason: what it fixes gets quietly worse while nothing is done, because every
stretch that closes was assessed by a project living inside the assessed.

*On the name: εὐβουλία, good counsel — the quality of deliberating well, as
against the deliberating itself. Chosen for what it claims and does not: it
names an advisor's virtue rather than an authority, which is the whole of the
office. It shares its prefix with **eunoia** by construction rather than by
accident. Its near neighbour `bouleusis` — deliberation about particulars —
stays free and stays the better name for anything that decides cases, which
this does not; `martyria` already holds particulars, and if this ever starts
deciding them, it has taken the wrong job.*

## elenchos — differential fuzzing as a derived artifact

**What:** a research-quality fuzzer for the ecosystem's checkers — coverage
guidance, a generator that assembles derivations which *should* be accepted, and
the semantics itself as an oracle.
**State:** `named` — reserved in [`names.md`](names.md), described in the
account, and started by nobody.
**Settles:** **O6**. The arrangement manufactures its own second implementation
and the claim that this is close to free has never been tested against the other
half: whether the free second implementation is *worth having*, measured in
defects it finds in the first.
**Costs:** a differential finding names a direction and never a culprit, so
every one costs a person's judgement before it can be filed — and the generated
checker is less independent than the argument wants, since it reads the same
signature through the same compiler.
**Before it:** `nothing`. It is the only entry here that can start without a
decision being made first.
**Today:** the baseline, [`../../docs/fuzzing.md`](../../docs/fuzzing.md) —
grammar-directed generation, a mutated seed corpus, three verdict-level oracles,
and no instrumentation anywhere. It is deliberately the floor, which is what
makes *research-quality* a measurable claim rather than an adjective.
**Why here:** highest of the account's projects because it is the one somebody
could start on a Monday. It has a floor already built, it needs no question
settled first, and it is the only one that would pay for the generation column
in a currency other than trust.

## noesis — the semantics and the compiler, defined in Lean

**What:** `.eos` written as Lean definitions over the model logos already
carries, the compiler as a Lean metaprogram over those definitions, and a
theorem relating what it emits to what they say.
**State:** **started, elsewhere** — a child project in eudaimonia, with a
charter and docs, whose stated goal is a verified Eunoia compiler in Lean. The
`P3` audit in [`proposals.md`](proposals.md) returned **not yet** on the
*repository* question and that verdict stands; what has changed is that "it has
been written zero times" is no longer true, and this listing said so for longer
than it was accurate. **This entry is now a description of somebody else's
work** and should be read for what it wants rather than as a plan of ours.
**Settles:** **O2**, **O3** and **O6**, each of which currently has a convention
where it wants a statement; and **open question 3**, by building it. Arrangement
**B** is the shape.
**Costs:** not the target language, where a proof assistant is by construction
good at this, but the source. A compiler-correctness theorem needs a semantics
of *Eunoia* and there is not one — what matching checks, how `:list` desugars
under each attribute, what `eo::define` binds and in what order.
**Before it:** **open question 7**, where the line falls between the invariant
core and what a signature contributes, because the theorem quantifies over
signatures and cannot be stated without it; and the fork with `iogos`, which
cannot both hold in their strongest forms.
**Today:** `ethos-eoc`, which is the hypothesis — what a `.eos` file means is
what the compiler makes of it, and everything downstream reasons from that and
none of it can examine it.
**Why here:** the highest leverage on the page and the lowest readiness. It
would settle open question 3 rather than accrue against it, and it is what makes
`hermeneia` cheap. It sits below `elenchos` because it cannot start before a
fork is decided, and its first task is writing down a language nobody has
written down.

## hermeneia — from the embedded semantics to Lean's own logic

**What:** a correspondence between the SMT-LIB semantics logos carries and
Lean's native logic, symbol by symbol and sort by sort, so that what a proof
establishes can be restated as an ordinary Lean proposition.
**State:** `named`.
**Settles:** **O5**, more directly than anything else on this page: it adds a
kind of consumer the arrangement does not have at all — a Lean development that
ends with a theorem in its own terms rather than with a checker's verdict. It
answers **open question 2** from the other end, by making the reference seam
unnecessary in one direction rather than by verifying it.
**Costs:** choosing what corresponds to what where the two disagree. SMT-LIB's
operations are total and Lean's native ones are not, or are total differently —
division by zero, an out-of-range `str.substr`, a bit-vector of width zero. Each
is a design decision, not a lemma.
**Before it:** `nothing` strictly. `noesis` makes it far cheaper, which is the
whole of why it sits below.
**Today:** `nothing`. A Lean user who wants a conclusion about Lean's own `Int`,
`BitVec` or `String` bridges the gap themselves, and there is no bridge.
**Why here:** below `noesis` because it is the same work twice as hard while the
semantics is still `.eos` text rendered by a compiler written in C++ and Python
— a correspondence between two Lean definitions is a far easier thing to state
and maintain. Above `pathos` because what it adds is an audience the ecosystem
has never had, and `pathos` improves something it already has.

## pathos — an efficient verified proof checker

**What:** a checker that is both fast and verified, removing the choice the
ecosystem currently offers between ethos and the generated Lean checker.
**State:** `named`.
**Settles:** reason **4** and **open question 5**, by dissolving the trade-off
rather than measuring it, and arrangement **D**, whose only stated blocker is
that measurement. The trusted base becomes the kernel, the parser and the
statement rather than a C++ program about which nothing is proved.
**Costs:** efficiency under verification is hash consing, term sharing and
mutable state, whose invariants are the hard part of the proof. That is why the
two words have historically been alternatives, and it is where the work would
go.
**Before it:** `nothing`, and nothing else here waits on it.
**Today:** two half-answers — ethos, fast and unverified, and the generated Lean
checker, verified and unmeasured.
**Why here:** the promise is real and entirely local. It improves the
arrangement's weakest artifact and touches nothing else, so every other open
question in the account is exactly as open the day after it lands — which is
worth saying, because *we are building a verified checker* is easily heard as
*the rest is settled*.

## iogos — logos in a second proof assistant

**What:** an Isabelle/HOL backend for `ethos-eoc`, and the logos development
redone against it: the same calculus, the same semantics and the same soundness
argument, carried by a second kernel.
**State:** `named`.
**Settles:** reason **6**, as its falsification test. The claim that the Lean
side is *generated rather than chosen* is what lets the arrangement count a
proof-assistant justification as a derived artifact, and nothing has ever tested
whether a second prover is a second backend or a second project.
**Costs:** Eunoia's types are dependent where SMT-LIB's are, and Isabelle/HOL
cannot follow that shape — widths become fields with well-formedness conditions
carried through every operation, which is a redesign of the part of logos that
is hardest to get right rather than a port of it.
**Before it:** the fork with `noesis`, decided. Noesis moves the authoritative
semantics into a prover and iogos needs it outside every prover; both cannot
hold in their strongest forms, and that wants settling before either starts.
**Today:** one development, one kernel, and no measurement of how much of it is
Lean rather than calculus.
**Why here:** last, and still on the page. Its largest present value is not as
work to do but as the thing `noesis` has to be decided *against* — a page that
dropped it for being expensive would lose the fork, which is the most
consequential open decision on this page.
