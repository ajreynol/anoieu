# The roles

**One entry per responsibility, across the Eunoia ecosystem.** A role is a
single self-contained thing somebody is accountable for; it has a permanent id;
and a tool holds as many of them as it holds. Four labelled fields each, no
argument, and no ordering that means anything.

[`board.md`](board.md) is the other half of the same pair, and the difference is
worth stating once: the board is **what is outstanding, in priority order**, and
this is **what everything is for, in no order at all**. A row here does not move
when the work does. It moves when responsibility does, which is rare and is
always a decision somebody made.

Nothing consumes this file yet. It is written to be *parsed later* rather than
parsed now: every entry carries the same four labels, in the same order, always
present, and a field with nothing in it says so in words rather than being left
out. That costs nothing to keep true by hand and is the whole of what a parser
would need.

## The philosophy

**The unit is the responsibility, not the tool.** A tool is where roles happen
to live at the moment; the role is the thing that survives being moved to a
different repository. So the entries here are roles, one per heading, and the
tool that holds one is a field on it rather than the other way round.

**No role is too small.** The count is not a budget and there is nothing to be
won by keeping it down. A clear seam between two responsibilities is worth far
more than a short page, so a role that could reasonably be split is split, and a
role that feels too slight to deserve an id gets one anyway. The cost of an
extra entry is four lines. The cost of two responsibilities sharing one is that
nobody can say which of them a change belongs to.

**A long list against one tool is the finding, not the failure of this page.**
The table below is at its most useful when a row is uncomfortable. Six roles
against one name means one of two things — a tool that has taken on more than it
should, or a tool that has not decided what it is — and neither is fixed by
merging entries until the row looks tidy. Read the length as the measurement it
is.

**Two tools holding one role is a seam that has not been cut yet.** Where the
same responsibility genuinely sits in two trees, the honest entry names both
holders and is a standing question rather than a description. `R16` is the
worked example: the reporting loop was implemented twice before anybody wrote
down that it was one role, and writing that down is what produced a repository
to hold it.

**An id is permanent.** `R4` stays `R4` wherever it appears on the page and
whoever ends up holding it, because decisions get recorded against ids and an id
that moves invalidates them silently. A role that is deprecated is **deleted**,
not marked dead — what happened to it lives in git — and its number is never
reused.

## How to read it, and how to edit it

**The order carries nothing.** Entries are grouped by the tool that holds them,
tools alphabetical, so ids appear out of order and that is correct rather than a
mistake to tidy. The page that ranks things is next door.

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

Each entry carries the same fields, in the same order:

| field | what it holds |
| --- | --- |
| **Held by** | the tool or tools accountable for it, by their ids in [`../tools/ecosystem.json`](../tools/ecosystem.json) |
| **Role** | the responsibility itself. Two sentences at most |
| **Owns** | the artifacts that are its to change, and therefore nobody else's |
| **Not this role** | the nearest neighbouring responsibility, and which role it is — or that it is nobody's |

## Who holds what

| tool | footing | roles | how many |
| --- | --- | --- | --- |
| `anoieu` | member | `R1`–`R6` | 6 |
| `cvc5` | served | `R7`, `R8` | 2 |
| `dokimasia` | member | `R9` | 1 |
| `ethos` | candidate | `R10`, `R11` | 2 |
| `ethos-eoc` | child of `ethos` | `R12`, `R13` | 2 |
| `eudaimonia` | member | `R14` | 1 |
| `euthyna` | child of `eudaimonia` | `R15` | 1 |
| `koine` | member | `R16` | 1 |
| `logos` | candidate | `R17`–`R19` | 3 |
| `sapheneia` | child of `anoieu` | `R20` | 1 |
| `ynoia` | child of `anoieu` | `R21`–`R24` | 4 |

Twenty-four roles across eleven tools. The two rows worth looking at are the
first and the last, and both are the page working rather than the page being
wrong.

---

## R1 — the bug report system

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

## R2 — the static analyzer

**Held by:** `anoieu`
**Role:** reading Eunoia signatures and semantic configuration files and
reporting what a checker accepts and should not — the front end, the checks, the
shallow typing pass and the desugarer. It is also the only thing that compares
the legs of the triple, which are owned by three different people.
**Owns:** the analyzer, the check registry, `docs/checks.md`, `docs/usage.md`,
and the committed baselines.
**Not this role:** what happens to a finding once it exists, which is `R1`, and
generating cases nobody wrote, which is `R3`.

## R3 — the fuzzer

**Held by:** `anoieu`
**Role:** writing Eunoia nobody would write, handing it to a checker, and
shrinking and bucketing what comes back into something that can be filed.
Deliberately a baseline rather than a research instrument, and it says so.
**Owns:** `anoieu_fuzz/`, `docs/fuzzing.md`, the seed corpus, and the promoted
reproducers under `tests/fuzz/`.
**Not this role:** reading a signature without running anything, which is `R2`,
and the research-quality successor, which is nobody's — it has a name,
`elenchos`, and no repository.

## R4 — the ecosystem's policy, and joining it

**Held by:** `anoieu`
**Role:** how a repository in this ecosystem is arranged, what its front page
must say about who is writing it, how tools talk to one another, and what a
child project may do. Written to be adopted rather than admired, and
machine-checked in every member's CI.
**Owns:** `docs/policy.md`, `tools/policy_check.py`, and the `init_eo`,
`join_eo`, `check_join_eo` and `global_audit` prompts.
**Not this role:** who is actually in the ecosystem, which is `R6`, and what the
work is *for*, which is `R5` and is argued rather than decided by a program.

## R5 — the development vision

**Held by:** `anoieu`
**Role:** what AI-assisted development in this ecosystem is aiming at — the
tenets, the record of what the tools have actually delivered to one another, and
a report card that is a judgement about somebody else's project. Written for
every repository, and argued rather than checked.
**Owns:** `docs/vision.md`, in full, including the report card.
**Not this role:** anything mechanical. Nothing may ever check this one, which
is the single rule in this ecosystem that forbids work rather than requiring it;
the checkable half is `R4`.

## R6 — the inventory, and getting the ecosystem onto a machine

**Held by:** `anoieu`
**Role:** who is in the ecosystem and on what footing, and the commands that
clone the rest of it beside a checkout, record where each one landed, and report
what has drifted.
**Owns:** `tools/ecosystem.json`, `tools/checkouts.json`, `tools/ecosystem.py`,
`scripts/install_eo`, `scripts/status_eo`, and the `welcome_eo` prompt.
**Not this role:** deciding membership — a status is changed by a person and no
script writes that file — and the rules a member is checked against, which are
`R4`.

## R7 — the solver, and the proofs

**Held by:** `cvc5`
**Role:** finding the answer and emitting the proof that justifies it. Every
artifact in the ecosystem is downstream of that output, and of decisions this
role made before any of the rest existed.
**Owns:** the solver, its proof production, and the proofs themselves.
**Not this role:** checking them — that is `R10` and `R17` — and adopting
anything from this ecosystem. It is not a candidate and is not asked.

## R8 — CPC, the calculus

**Held by:** `cvc5`
**Role:** maintaining the Cooperating Proof Calculus as a Eunoia signature: the
rules, their programs, and the file every checker here is built around.
**Owns:** `proofs/eo/cpc/`.
**Not this role:** the semantics of CPC, which is `R19` and lives in another
tree entirely, and the language the signature is written in, which is `R11`.

## R9 — what no proof step covers

**Held by:** `dokimasia`
**Role:** reads cvc5's proof-production C++ and asks which of it has no proof
step behind it — the scrutiny before office, applied to the code that emits
proofs rather than to what it emits.
**Owns:** its findings about cvc5's proof production.
**Not this role:** the calculus, the checkers, or the proofs. It reads the code
that produces a proof, never the proof.

## R10 — the proof checker

**Held by:** `ethos`
**Role:** the fast, unverified C++ checker that production runs against, and the
implementation every other reading of the language is compared to.
**Owns:** the checker, and its behaviour, which is the reference the rest of the
ecosystem measures itself against.
**Not this role:** saying what the language *is*, which is `R11` in the same
tree, and being verified, which is nobody's — the name `pathos` is reserved for
it and there is no repository.

## R11 — the Eunoia manual

**Held by:** `ethos`
**Role:** the one description of Eunoia there is, and the language's authority.
It is by construction a manual for a *program*, which is why the boundary
between *the language requires this* and *this implementation happens to do
this* is not drawn in it.
**Owns:** `user_manual.md`.
**Not this role:** drawing that boundary. A second reading is `R20`, and it is
additive: this role governs and that one does not.

## R12 — the Eunoia compiler

**Held by:** `ethos-eoc`
**Role:** turns a signature and its semantics into a Lean development — one
constructor, type rule, evaluator case and verification condition per symbol.
**Owns:** the compiler and its stages.
**Not this role:** what the emitted development goes on to prove, which is
`R17`, and carrying what a proof establishes into Lean's own terms, which is
nobody's.

## R13 — the shipped semantics sets

**Held by:** `ethos-eoc`
**Role:** maintains the `.eos` semantics sets it ships. In the absence of any
other definition, what a `.eos` file means is what this role makes of it, which
is a larger responsibility than it looks.
**Owns:** the semantics sets in its tree.
**Not this role:** `Cpc.eos`, which is `R19`, and any account of the semantics
that does not depend on this compiler, which is nobody's.

## R14 — the calculus template

**Held by:** `eudaimonia`
**Role:** the logos arrangement with the calculus taken out — bring a signature
and a semantics, get a Lake project with a checker, its proofs, its regression
suite and its documentation.
**Owns:** the template and its generators, and the profile a new calculus
declares about itself.
**Not this role:** any particular calculus. CPC is `R8`'s and its development is
`R17`'s; the subject here is the shape, never the content.

## R15 — the audit of logos's proof

**Held by:** `euthyna`
**Role:** reads the generated development logos carries and says what it is made
of and where its weight sits — what is dead, what repeats, and what is
structured in a way that will cost the next regeneration.
**Owns:** its own account, inside its own directory.
**Not this role:** maintaining or rewriting what it reads, which stays `R17`.
Anything it wants to say leaves through its parent, like any other finding.

## R16 — the shared machinery of the reporting loop

**Held by:** `koine`
**Role:** one implementation of the parts of the loop every member runs, rather
than one per member — the prompt-drift check first, then the branch-state
reporter and the reply finder. It exists because two tools wrote the same thing
before anybody had written down that it was one role.
**Owns:** what its owner decides it owns. The scope is theirs and is not set
here; what has been named for it is the machinery that already exists twice.
**Not this role:** the prompts, or what settles a row. Those differ per tool and
stay with the tool — `R1` here, and its counterpart in `R9`'s tree.

## R17 — the verified checker for CPC

**Held by:** `logos`
**Role:** an executable proof checker for CPC written in Lean, whose soundness
is proven against a correctness specification. It is the artifact the
ecosystem's trust argument actually rests on.
**Owns:** the generated development, and the soundness statement it establishes.
**Not this role:** speed, which is `R10`'s and is the reason two checkers exist,
and whether the development can be read by a person, which is `R15`'s subject.

## R18 — the model of SMT-LIB semantics in Lean

**Held by:** `logos`
**Role:** a standalone Lean formalization of what SMT-LIB terms mean,
independent of the checker and usable on its own. It is what a soundness
statement is stated *against*, which makes it load-bearing for `R17` and
separable from it.
**Owns:** `Cpc/SmtModel.lean` and its write-up.
**Not this role:** the Eunoia semantics of a calculus, which is `R13` and `R19`,
and carrying what it says into Lean's native logic, which is nobody's.

## R19 — the semantics of CPC

**Held by:** `logos`
**Role:** maintains `Cpc.eos`, the semantics the compiler reads for the calculus
cvc5 emits proofs in.
**Owns:** `Cpc.eos` and its cached form.
**Not this role:** the signature it is the semantics of, which is `R8` and sits
in a different tree under a different owner. Two legs of one triple, held apart
— which is exactly why something has to compare them, and that is `R2`.

## R20 — Eunoia as a language definition

**Held by:** `sapheneia`
**Role:** a second description of Eunoia, written as a language definition
rather than as a manual for a program: where the boundary falls between what the
language requires and what one implementation happens to do.
**Owns:** its own account, inside its own directory.
**Not this role:** governing. `R11` remains the authority and this account says
so on its own front page; where the two disagree, that disagreement is a finding
and it leaves through `R1`.

## R21 — the account of the arrangement

**Held by:** `ynoia`
**Role:** whether the ecosystem's arrangement earns its machinery — the case,
the case against, the general objections, the arrangements it could take
instead, and what would change our minds.
**Owns:** `why-eunoia.md`.
**Not this role:** deciding. The arrangements are options laid out fairly, and
nobody holding this role has the authority to rearrange anything.

## R22 — the register of names

**Held by:** `ynoia`
**Role:** what each reserved name was reserved *for*, which are taken, and how a
brand new repository picks one. It is consulted by `init_eo` when a repository
is started.
**Owns:** `names.md`.
**Not this role:** granting a name. A name is claimed when a person approves
one, and never by a document suggesting it.

## R23 — auditing whether an idea deserves a repository

**Held by:** `ynoia`
**Role:** *should this become a repository of its own*, answered against a
stated standard with a verdict attached — and, where the answer is no, an
argument about whose existing tree the work belongs in instead.
**Owns:** `proposals.md` and `requests.md`.
**Not this role:** approving anything, and creating anything. A repository is a
person's decision and a person's act, and this role produces an argument with a
recommendation at the end.

## R24 — the register of tools that do not exist

**Held by:** `ynoia`
**Role:** every tool the ecosystem has named and nobody has built, in priority
order, most promising first, with the argument for each position stated where it
can be disagreed with.
**Owns:** `tools.md`.
**Not this role:** committing anybody to build one, and ranking work that
already exists — that is the board's.
