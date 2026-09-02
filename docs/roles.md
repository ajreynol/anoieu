# The roles

**One entry per responsibility, stratified by the tool that holds it.** A role
is a single self-contained thing somebody is accountable for; it has a permanent
id; and a tool holds as many of them as it holds, listed under its own heading
in the order it would least like to lose them. Four labelled fields each, no
argument, and nothing ranked across tools.

[`board.md`](board.md) is the other half of the same pair, and the difference is
worth stating once: the board is **what is outstanding**, and this is **what
everything is for**. A row here does not move when the work does. It moves when
responsibility does, which is rare and is always a decision somebody made.

Nothing consumes this file yet. It is written to be *parsed later* rather than
parsed now: below the rule, `##` is a tool and `###` is a role, every role
carries the same four labels in the same order, always present, and a field with
nothing in it says so in words rather than being left out. That costs nothing to
keep true by hand and is the whole of what a parser would need.

## The philosophy

**The unit is the responsibility, not the tool.** A tool is where roles happen
to live at the moment; the role is the thing that survives being moved to a
different repository. So a role keeps its id when it changes hands, and the
heading it sits under is the part that is allowed to change.

**No role is too small.** The count is not a budget and there is nothing to be
won by keeping it down. A clear seam between two responsibilities is worth far
more than a short page, so a role that could reasonably be split is split, and a
role that feels too slight to deserve an id gets one anyway. The cost of an
extra entry is four lines. The cost of two responsibilities sharing one is that
nobody can say which of them a change belongs to.

**A long section is the finding, not the failure of this page.** Stratifying by
tool is what makes that visible: six roles under one heading means one of two
things — a tool that has taken on more than it should, or a tool that has not
decided what it is — and neither is fixed by merging entries until the section
looks tidy. Read the length as the measurement it is.

**An empty section is a tool looking for work**, and is the same measurement
from the other end. A heading with no roles under it is not an omission and not
a mistake to tidy: it is a tool that has been named, is in the inventory, and is
accountable for nothing yet. Leaving the heading there is how that stays
visible.

**Two tools holding one role is a seam that has not been cut yet.** Where the
same responsibility genuinely sits in two trees, the honest entry names both
holders and appears under both headings, and it is a standing question rather
than a description. `R16` is the worked example: the reporting loop was
implemented twice before anybody wrote down that it was one role, and writing
that down is what produced a repository to hold it.

**An id is permanent.** `R4` stays `R4` wherever it appears and whoever ends up
holding it, because decisions get recorded against ids and an id that moves
invalidates them silently. A role that is deprecated is **deleted**, not marked
dead — what happened to it lives in git — and its number is never reused.

## How to read it, and how to edit it

**Within a tool, position is the priority.** The first role under a heading is
the one that tool is least able to drop; the last is the one whose loss would
cost least. Reordering is done by moving a block, and that is the main way a
person changes what a section says.

**Across tools, nothing is ranked.** The sections are alphabetical by the tool's
id, deliberately, because this page has no basis on which to say that one
repository matters more than another and the page that ranks things is next
door.

**Ids therefore appear out of order**, both because roles are added over time
and because a section gets reordered. That is correct rather than a mistake to
tidy.

**The tool ids are the inventory's**, spelled exactly as
[`../tools/ecosystem.json`](../tools/ecosystem.json) spells them. That file is
the authority on who is in the ecosystem and on what footing; this one adds only
what each is accountable for. Where the two disagree, the inventory is right and
this page is stale.

**A role is not a boundary until it says what it excludes**, which is what the
last field is for and why it is never left empty. The near miss is the expensive
one — a responsibility that is *nearly* somebody's is the one that gets acted on
without anybody asking — so the field names the neighbour and, where the
neighbour is a role, its id.

Each role carries the same fields, in the same order:

| field | what it holds |
| --- | --- |
| **Held by** | the tool or tools accountable for it, by their ids in [`../tools/ecosystem.json`](../tools/ecosystem.json). Usually the heading it sits under, and always where a role is held twice |
| **Role** | the responsibility itself. Two sentences at most |
| **Owns** | the artifacts that are its to change, and therefore nobody else's |
| **Not this role** | the nearest neighbouring responsibility, and which role it is — or that it is nobody's |

## How a role is handed off

**A handoff is the same role under a different heading.** The id does not
change, which is the whole reason ids here are permanent: a decision recorded
against `R4` stays recorded when `R4` moves, and a reader who finds the entry in
a new section can still tell it is the same responsibility.

Seven steps, in this order because each is cheap to get wrong and expensive to
discover later. **None of them is a gate** — see the end of this section.

**1. Name the roles, not the files.** A handoff is proposed as a list of ids. If
it cannot be stated that way, the roles are wrong and splitting them is the work
that comes first: a proposal phrased as a list of paths is a migration nobody
can hold an opinion about.

**2. Say what stays.** The losing tool's remaining section is part of the
proposal and is written out in full. A handoff that lists only what leaves has
not been thought through, and the line between the two halves is where every
argument about it is actually going to happen.

**3. Name the consumers.** Every tool that depends on one of the roles moving,
by its id in [`../tools/ecosystem.json`](../tools/ecosystem.json). Where a role
carries a CI contract that is *every member*, and the count is the cost: it
grows with each tool that joins before the handoff happens, which is usually the
strongest argument for doing it sooner.

**4. Put it on [`board.md`](board.md).** One item, the affected entities, the
`discussion` channel, and one prompt per entity. That is what makes a handoff
something other tools can **state an opinion on** rather than something they are
told about — a prompt written to be answered is a different artifact from an
announcement, and the board already knows how to carry one. Where the gaining
tool does not exist yet, it is named in the item's text and not in `Entities`,
which only takes ids the inventory has.

**5. Collect the opinions, and leave them where they landed.** A reply that
disagrees stays visible: in the item's `HUMAN FEEDBACK`, which outranks every
other field on it, or in the discussion topic it came back through. Afterwards,
a handoff nobody objected to and a handoff nobody was asked about look identical
unless the asking is on the record.

**6. Move the entry, and only the entry.** When it happens: the role's section
moves under the new tool's heading, `Held by` changes, `Owns` is re-pointed at
wherever the artifacts landed, and the id does not move. One commit, so that
this register is never half-handed-over.

**7. The pins move last, and each consumer picks when.** Nothing here reaches
into somebody else's workflow file. A consumer still pinned to the old holder is
not behind, it is correct, and that is the structural answer working as
intended.

**A role over human-authored work is not ours to move.** Where the artifact a
role covers was written by people who have not adopted
[`vision.md`](vision.md), no footing, no procedure and no argument here makes
reassigning it a handoff — it is a claim on somebody's authorship, and this
register records what tools are accountable for rather than deciding it for them.
The test is not *are they a member*: a member could employ authors who never
signed up to any of this, and a non-member's role could be perfectly movable if
the work is generated. **Ask who wrote it and what they agreed to**, not what
footing the repository holds. `R11` is the worked example.

**A child project graduating is a handoff, and the commonest one this page will
see.** The roles do not change; the heading over them does. `init_eo from-child`
is the step that starts it, and it is told to say the move is owed here rather
than to attempt it from inside a repository that cannot see this file: the entry
moves under the new tool's heading, `Held by` becomes the new id, and the number
does not change.

**A role handed off to nobody is deprecated rather than orphaned** — deleted
from this page, its number never reused. And a tool with an **empty section** is
where a handoff goes looking for a taker, which is what an empty section is for.

### It is not a gate, yet

**Nothing waits on any of this.** While the ecosystem is still settling, the
seven steps describe the honest way to hand a role over. They do not stop
anybody's work, block a commit, or require an answer before something can move,
and a tool that reorganises itself in an afternoon and writes the register up
afterwards has done nothing wrong.

What would change that is the ecosystem being **stable**: enough tools, pinned
deeply enough, that a handoff nobody was asked about costs somebody a red build
in a week they had planned otherwise. At that point the steps stop being a
description and become a requirement — and that is a decision for a person, made
once, and written down here when it is made.

### The worked example: anoieu to kanon

`B15` on the board proposes moving the ecosystem's governance out of the tool
that also files findings against members; the ynoia proposals page audits it as
`P2` and recommends it. It is **parked** by the maintainer, and nothing here
changes that — it is the worked example precisely because a deferred decision is
easier to read than a live one. In the terms of this page:

- **Moves:** `R4`, the policy and joining; `R6`, the inventory and the
  installer.
- **Stays:** `R1` the bug report system, `R2` the analyzer, `R3` the fuzzer,
  `R5` the vision.
- **Gains:** `kanon`, which has no repository, is not in the inventory, and is a
  name nobody has claimed.
- **Consumers:** every member, because joining *is* running the checker `R4`
  owns — four today, and one more with each tool that joins first.

The split falls where it does because the argument is about exactly one thing:
the repository that writes the rules a member is judged by should not also be
the one filing findings against them. `R1` is what does the filing, so it stays;
`R4` is what writes the rules, so it goes. `R6` follows `R4` because the audit
that reads across both wants the inventory beside the policy rather than beside
the ledger. And the position on what may be published, which is part of `R1`,
stays with the tool whose own behaviour it constrains — an answer that took an
audit to reach, and the reason step 2 is a step.

Two of the seven steps came out of that audit rather than being designed here:
*what does the losing repository keep* and *is either half left unable to answer
a question it used to answer alone*. A procedure that could not ask those would
keep producing confident answers to a question nobody had asked.

## How many each holds

Summarised from the sections below, which are the authority. The count is the
number worth looking at, in both directions.

| tool | footing | how many |
| --- | --- | --- |
| `anoieu` | member | 8 |
| `cvc5` | foundation | 2 |
| `dokimasia` | member | 1 |
| `ethos` | candidate | 2 |
| `ethos-eoc` | child of `ethos` | 2 |
| `eudaimonia` | member | 1 |
| `euthyna` | child of `eudaimonia` | 1 |
| `koine` | member | 1 |
| `logos` | candidate | 3 |
| `martyria` | child of `anoieu` | 0 |
| `sapheneia` | child of `anoieu` | 1 |
| `workflow-launcher` | child of `eudaimonia` | 0 |
| `ynoia` | child of `anoieu` | 5 |

Twenty-seven roles across thirteen tools, and two sections empty:
`workflow-launcher` and `martyria` hold nothing, which is not an omission — a
child project has no users, nothing depends on it, and it owes nobody an
artifact. The rows worth reading are the longest and the empty one, and both are
the page working rather than the page being wrong.

---

## anoieu

### R4 — the ecosystem's policy, and joining it

**Held by:** `anoieu`
**Role:** how a repository in this ecosystem is arranged, what its front page
must say about who is writing it, how tools talk to one another, and what a
child project may do. Written to be adopted rather than admired, and
machine-checked in every member's CI.
**Owns:** `docs/policy.md`, `tools/policy_check.py`, and the `init_eo`,
`join_eo`, `check_join_eo` and `global_audit` prompts.
**Not this role:** who is actually in the ecosystem, which is `R6`, and what the
work is *for*, which is `R5` and is argued rather than decided by a program.

### R1 — the bug report system

**Held by:** `anoieu`
**Role:** carrying a defect in somebody else's file from the check that found it
to whoever can fix it, and tracking it until it is resolved, declined or
withdrawn. It includes the position on what may be published about somebody
else's code, which is the standard the whole record is kept under.
**Owns:** the findings ledger and its two files, `docs/reports/reports.md`,
`docs/reports/reporting-workflow.md`, `docs/reports/reporting-policy.md`, and
the `check_anoieu` and `process_anoieu` prompts.
**Not this role:** producing the findings, which is `R2` and `R3`, or the shared
half of the loop that every member runs, which is `R16`.

### R2 — the static analyzer

**Held by:** `anoieu`
**Role:** reading Eunoia signatures and semantic configuration files and
reporting what a checker accepts and should not — the front end, the checks, the
shallow typing pass and the desugarer. It is also the only thing that compares
the legs of the triple, which are owned by three different people.
**Owns:** the analyzer, the check registry, `docs/checks.md`, `docs/usage.md`,
and the committed baselines.
**Not this role:** what happens to a finding once it exists, which is `R1`, and
generating cases nobody wrote, which is `R3`.

### R6 — the inventory, and getting the ecosystem onto a machine

**Held by:** `anoieu`
**Role:** who is in the ecosystem and on what footing, and the commands that
clone the rest of it beside a checkout, record where each one landed, and report
what has drifted.
**Owns:** `tools/ecosystem.json`, `tools/checkouts.json`, `tools/ecosystem.py`,
`scripts/install_eo`, `scripts/status_eo`, and the `welcome_eo` prompt.
**Not this role:** deciding membership — a status is changed by a person and no
script writes that file — and the rules a member is checked against, which are
`R4`.

### R3 — the fuzzer

**Held by:** `anoieu`
**Role:** writing Eunoia nobody would write, handing it to a checker, and
shrinking and bucketing what comes back into something that can be filed.
Deliberately a baseline rather than a research instrument, and it says so.
**Owns:** `anoieu_fuzz/`, `docs/fuzzing.md`, the seed corpus, and the promoted
reproducers under `tests/fuzz/`.
**Not this role:** reading a signature without running anything, which is `R2`,
and the research-quality successor, which is nobody's — it has a name,
`elenchos`, and no repository.

### R5 — the development vision

**Held by:** `anoieu`
**Role:** what AI-assisted development in this ecosystem is aiming at — the
tenets, the record of what the tools have actually delivered to one another, and
a report card that is a judgement about somebody else's project. Written for
every repository, and argued rather than checked.
**Owns:** `docs/vision.md`, and `docs/report-card.md`, which is the half of it
that is re-graded every round.
**Not this role:** anything mechanical. Nothing may ever check this one, which
is the single rule in this ecosystem that forbids work rather than requiring it;
the checkable half is `R4`.

### R29 — the epoch command front end

**Held by:** `anoieu`
**Role:** the surface a person drives a stretch through — the commands, how they
are recognised, what a command prints, and **the stretch feedback communication
protocol**: the summary a person argues with, and what happens to the stretch when
they argue with its content rather than its wording.
**Owns:** `docs/interface.md` — the commands, the summary's shape, and the
feedback protocol.
**Not this role:** the machinery the commands invoke, which is `R28` — the
feedback protocol sits here because it runs between a person and an agent, where
the rest of that family runs between repositories; what a stretch is *for*, which is
nobody's role and is the human's; and **the authority to move a stretch to
`deployed`**, which is the build system's alone — the front end may carry that
transition but never originate it.

> **Consistency here is an aspiration, not an implementation.** Nothing parses a
> command and no program enforces anything; the role is held by an agent reading a
> prompt. Saying otherwise would be the same overclaim as calling the approval
> block a verification.
>
> **This is a separate role from `R28` because the two are separable, and today
> they are not separated.** anoieu holds both: it is the front end a person types
> at *and* the build system the commands drive. When its planned maintainer `tekton` exists it
> takes the machinery, and the front end stays wherever a person is actually working — which
> may be neither this repository nor that one. Writing them as two entries now is
> what makes that a move rather than a rewrite.

### R28 — the epoch build system

**Held by:** `anoieu`
**Role:** the family of communication protocols by which a stretch is verified,
announced, approved and adopted — the global announcement, the approval block and
its dry run, the bump gate, and the shape of the log entry. Taken together they
are this ecosystem's **main verification system for its own governance**, which
is a claim worth stating plainly because it is unusual: what verifies a stretch is
a protocol, not a test suite.
**Owns:** `tools/bump_check.py`, the approval protocol in `docs/policy.md`,
`docs/stretch-policy.md` and `docs/stretches.md` — the gates, the block template,
the dry run, the statuses, and the log's entry format.
**Not this role:** **deciding what a stretch is *for*, which is not a role here
at all** — it is the human's, and `R27` was allocated to this repository for it
in error and has been deleted; whether it could ever be automated is an open
research question this role carries rather than answers; the policy a member is checked against and the
discussion protocol with its safety gate, both `R4`; and the low-level formats of
the reporting loop, which koine has asked for and this must not quietly absorb.

> **The standing goal, which outranks everything else this role does and always
> will.** The protocols exist so that **the tools give evidence to the agent, and
> the agent is properly informed** before it writes anything. Every other
> verification here checks an artifact; this is the only one aimed at whether the
> agent doing the work knows what it is talking about, and since agents do the
> work it sits upstream of all of them.
>
> It is **not verification** and the role's holder should never let it be
> described as such — nothing is proved, and what keeps the work inside its
> guardrails is that the loop keeps teaching us. The failure it guards against is
> **fluency substituting for knowledge**, which is invisible from outside: a block
> written from evidence and one written from memory read identically.
>
> Whatever else changes about the machinery, this does not get displaced.

> **Destined for `kanon`.** The protocols by which every member is
> told what is expected of them are governance, and they should not stay in the
> tree that also files findings against them.
>
> **And the tool for it does not exist.** What is held here is run by hand across
> four documents. Its **planned maintainer** is registered with
> `ynoia` as [`tekton`](../tools/ynoia/tools.md), at the top of the priority
> order, and it is deliberately **not** work for the current stretch.

`R26` is deliberately not allocated here: koine's `D8` proposes it for the
low-level formats of the reporting loop, and that request is open. An id claimed
in a proposal nobody has answered is not free, and taking it would make the reply
harder to write than skipping a number is.

## cvc5

### R7 — the solver, and the proofs

**Held by:** `cvc5`
**Role:** finding the answer and emitting the proof that justifies it. Every
artifact in the ecosystem is downstream of that output, and of decisions this
role made before any of the rest existed.
**Owns:** the solver, its proof production, and the proofs themselves.
**Not this role:** checking them — that is `R10` and `R17` — and adopting
anything from this ecosystem. Its footing is **foundation**: nothing here
constrains it and nothing here asks it for anything.

### R8 — CPC, the calculus

**Held by:** `cvc5`
**Role:** maintaining the Cooperating Proof Calculus as a Eunoia signature: the
rules, their programs, and the file every checker here is built around.
**Owns:** `proofs/eo/cpc/`.
**Not this role:** the semantics of CPC, which is `R19` and lives in another
tree entirely, and the language the signature is written in, which is `R11`.

## dokimasia

### R9 — what no proof step covers

**Held by:** `dokimasia`
**Role:** reads cvc5's proof-production C++ and asks which of it has no proof
step behind it — the scrutiny before office, applied to the code that emits
proofs rather than to what it emits.
**Owns:** its findings about cvc5's proof production.
**Not this role:** the calculus, the checkers, or the proofs. It reads the code
that produces a proof, never the proof.

## ethos

### R10 — the proof checker

**Held by:** `ethos`
**Role:** the fast, unverified C++ checker that production runs against, and the
implementation every other reading of the language is compared to.
**Owns:** the checker, and its behaviour, which is the reference the rest of the
ecosystem measures itself against.
**Not this role:** saying what the language *is*, which is `R11` in the same
tree, and being verified, which is nobody's — the name `pathos` is reserved for
it and there is no repository.

### R11 — the Eunoia manual

**Held by:** `ethos`
**Role:** the one description of Eunoia there is, and the language's authority.
It is by construction a manual for a *program*, which is why the boundary
between *the language requires this* and *this implementation happens to do
this* is not drawn in it.
**Owns:** `user_manual.md`.
**Not this role:** drawing that boundary. A second reading is `R20`, and it is
additive: this role governs and that one does not.

> **Aspired handoff: `R11` to `sapheneia`.** The direction this register hopes
> for is that this id moves under `sapheneia`'s heading, keeping its number, so
> that the authority on *what Eunoia requires* is a language definition rather
> than a manual for one program.
>
> **It would invert a boundary both entries currently assert**, and that is the
> honest size of it. This role says *this role governs and that one does not*;
> `R20` says *not this role: governing*. A handoff here does not move a
> responsibility to a better-placed holder — it reverses a stated position, and
> both entries would have to be rewritten rather than moved.
>
> **The blocker is authorship, and it does not clear if `ethos` joins.**
> `user_manual.md` has **human authors**, and they have not adopted
> [`vision.md`](vision.md) — the account of AI-assisted development everything in
> this register is written under. Moving authority over what they wrote to a tree
> written by agents, under a vision they never agreed to, is not a handoff. It is
> a claim on somebody's authorship, and a footing would not make it one.
>
> **So this stays where it is by right rather than by circumstance.** An earlier
> version of this note gave the blocker as *`ethos` is a candidate and there is no
> channel*, which was wrong in a way worth recording: it implied the aspiration
> unblocks when a repository joins. It does not. What would change it is those
> authors deciding, and nobody else — and a register kept by agents is the last
> place with standing to press for that.

## ethos-eoc

### R12 — the Eunoia compiler

**Held by:** `ethos-eoc`
**Role:** turns a signature and its semantics into a Lean development — one
constructor, type rule, evaluator case and verification condition per symbol.
**Owns:** the compiler and its stages.
**Not this role:** what the emitted development goes on to prove, which is
`R17`, and carrying what a proof establishes into Lean's own terms, which is
nobody's.

> **Aspired handoff: `R12` to `noesis`.** The direction hoped for is that this id
> moves under `noesis`, keeping its number: the semantics *defined in* Lean, and
> the compiler a metaprogram over those definitions rather than a translator into
> them.
>
> **The gaining tool does not exist**, which by the handoff procedure means it is
> named in the text and never in an `Entities` field. `noesis` is audited as `P3`
> in [`../tools/ynoia/proposals.md`](../tools/ynoia/proposals.md) with the verdict
> **not yet** — written zero times, and forking with `iogos`, which cannot hold in
> its strongest form at the same time.
>
> **Blocked, and the authorship point applies here too**, though less sharply
> than for `R11`: the compiler is human-written in a tree whose authors have not
> adopted [`vision.md`](vision.md), so deciding that their compiler stops holding
> this role is not ours to decide. What is different is that `noesis` would be a
> *second implementation* rather than a reassignment of the same artifact, and a
> role following the implementation that actually gets used is an ordinary way for
> one to move. That does not make it ours to schedule.
>
> `ethos-eoc` is also a child of `ethos` and is reached through its parent, which
> has joined nothing — a second, weaker blocker that would clear on a footing where
> the first would not.

### R13 — the shipped semantics sets

**Held by:** `ethos-eoc`
**Role:** maintains the `.eos` semantics sets it ships. In the absence of any
other definition, what a `.eos` file means is what this role makes of it, which
is a larger responsibility than it looks.
**Owns:** the semantics sets in its tree.
**Not this role:** `Cpc.eos`, which is `R19`, and any account of the semantics
that does not depend on this compiler, which is nobody's.

## eudaimonia

### R14 — the calculus template

**Held by:** `eudaimonia`
**Role:** the logos arrangement with the calculus taken out — bring a signature
and a semantics, get a Lake project with a checker, its proofs, its regression
suite and its documentation.
**Owns:** the template and its generators, and the profile a new calculus
declares about itself.
**Not this role:** any particular calculus. CPC is `R8`'s and its development is
`R17`'s; the subject here is the shape, never the content.

## euthyna

### R15 — the audit of logos's proof

**Held by:** `euthyna`
**Role:** reads the generated development logos carries and says what it is made
of and where its weight sits — what is dead, what repeats, and what is
structured in a way that will cost the next regeneration.
**Owns:** its own account, inside its own directory.
**Not this role:** maintaining or rewriting what it reads, which stays `R17`.
Anything it wants to say leaves through its parent, like any other finding.

## koine

### R16 — the shared machinery of the reporting loop

**Held by:** `koine`
**Role:** one implementation of the parts of the loop every member runs, rather
than one per member — the prompt-drift check first, then the branch-state
reporter and the reply finder. It exists because two tools wrote the same thing
before anybody had written down that it was one role.
**Owns:** what its owner decides it owns. The scope is theirs and is not set
here; what has been named for it is the machinery that already exists twice.
**Not this role:** the prompts, or what settles a row. Those differ per tool and
stay with the tool — `R1` here, and its counterpart in `R9`'s tree.

## logos

### R17 — the verified checker for CPC

**Held by:** `logos`
**Role:** an executable proof checker for CPC written in Lean, whose soundness
is proven against a correctness specification. It is the artifact the
ecosystem's trust argument actually rests on.
**Owns:** the generated development, and the soundness statement it establishes.
**Not this role:** speed, which is `R10`'s and is the reason two checkers exist,
and whether the development can be read by a person, which is `R15`'s subject.

### R18 — the model of SMT-LIB semantics in Lean

**Held by:** `logos`
**Role:** a standalone Lean formalization of what SMT-LIB terms mean,
independent of the checker and usable on its own. It is what a soundness
statement is stated *against*, which makes it load-bearing for `R17` and
separable from it.
**Owns:** `Cpc/SmtModel.lean` and its write-up.
**Not this role:** the Eunoia semantics of a calculus, which is `R13` and `R19`,
and carrying what it says into Lean's native logic, which is nobody's.

### R19 — the semantics of CPC

**Held by:** `logos`
**Role:** maintains `Cpc.eos`, the semantics the compiler reads for the calculus
cvc5 emits proofs in.
**Owns:** `Cpc.eos` and its cached form.
**Not this role:** the signature it is the semantics of, which is `R8` and sits
in a different tree under a different owner. Two legs of one triple, held apart
— which is exactly why something has to compare them, and that is `R2`.

## martyria

## sapheneia

### R20 — Eunoia as a language definition

**Held by:** `sapheneia`
**Role:** a second description of Eunoia, written as a language definition
rather than as a manual for a program: where the boundary falls between what the
language requires and what one implementation happens to do.
**Owns:** its own account, inside its own directory.
**Not this role:** governing. `R11` remains the authority and this account says
so on its own front page; where the two disagree, that disagreement is a finding
and it leaves through `R1`.

## workflow-launcher

## ynoia

### R22 — the register of names

**Held by:** `ynoia`
**Role:** what each reserved name was reserved *for*, which are taken, and how a
brand new repository picks one. It is consulted by `init_eo` when a repository
is started, which makes it the one thing here another script already depends on.
**Owns:** `names.md`.
**Not this role:** granting a name. A name is claimed when a person approves
one, and never by a document suggesting it.

### R23 — auditing whether an idea deserves a repository

**Held by:** `ynoia`
**Role:** *should this become a repository of its own*, answered against a
stated standard with a verdict attached — and, where the answer is no, an
argument about whose existing tree the work belongs in instead.
**Owns:** `proposals.md` and `requests.md`.
**Not this role:** approving anything, and creating anything. A repository is a
person's decision and a person's act, and this role produces an argument with a
recommendation at the end.

### R21 — the account of the arrangement

**Held by:** `ynoia`
**Role:** whether the ecosystem's arrangement earns its machinery — the case,
the case against, the general objections, the arrangements it could take
instead, and what would change our minds.
**Owns:** `why-eunoia.md`.
**Not this role:** deciding. The arrangements are options laid out fairly, and
nobody holding this role has the authority to rearrange anything.

### R24 — the register of tools that do not exist

**Held by:** `ynoia`
**Role:** every tool the ecosystem has named and nobody has built, in priority
order, most promising first, with the argument for each position stated where it
can be disagreed with.
**Owns:** `tools.md`.
**Not this role:** committing anybody to build one, and ranking work that
already exists — that is the board's.

### R25 — which projects are worth a paper

**Held by:** `ynoia`
**Role:** whether the work in a repository has a result worth writing up for a
human, in the `report/` the policy asks for — one entry per tool, against a
stated standard, with `no` as the commonest verdict.
**Owns:** `papers.md`.
**Not this role:** deciding whether anybody writes one. A repository's own stance
on publishing settles that for itself and outranks the register, which records
the disagreement rather than resolving it. Nor is it the findings ledger: that is
`R1`, it is about somebody else's code, and this is about our own.
