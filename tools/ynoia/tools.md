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

---

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
**State:** `named` — audited as `P3` in [`proposals.md`](proposals.md) with
the verdict **not yet**: it has been written zero times, and two of its three
prerequisites already have owners in trees that are not it. The repository
question returns when they meet.
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
