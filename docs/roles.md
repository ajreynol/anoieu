# The roles

**Who is responsible for what, across the Eunoia ecosystem.** One entry per row
of [`../tools/ecosystem.json`](../tools/ecosystem.json), four labelled fields
each, and no argument anywhere on the page. It answers *whose is this* and
*whose is this not*, and nothing else.

[`board.md`](board.md) is the other half of the same pair, and the difference is
worth stating once: the board is **what is outstanding, in priority order**, and
this is **what each tool is for, in no order at all**. A row here does not move
when the work does. It moves when responsibility does, which is rare and is
always a decision somebody made.

Nothing consumes this file yet. It is written to be *parsed later* rather than
parsed now: every entry carries the same four labels, in the same order, always
present, and a field with nothing in it says so in words rather than being left
out. That costs nothing to keep true by hand and is the whole of what a parser
would need.

## How to read it, and how to edit it

**The order carries nothing.** Entries are alphabetical by id, which is the
clearest available way of saying that this page ranks nothing. A register of
responsibilities that is ordered is making a claim it has not argued, and the
page that ranks things is next door.

**The heading is the id**, spelled exactly as
[`../tools/ecosystem.json`](../tools/ecosystem.json) spells it. That file is the
authority on who is in the ecosystem and on what footing; this one adds only
what each is *for*. Where the two disagree, the inventory is right and this page
is stale.

**An entry is added when the inventory gains a row, and removed when it loses
one.** A tool that is retired leaves rather than being marked dead: what
happened to it lives in git and in the record, and a register that keeps its
dead is one nobody trusts to be current.

**A role is not a boundary until it says what it excludes**, which is what the
last field is for and why it is not optional. The near miss is the expensive
one — a responsibility that is *nearly* somebody's is the one that gets acted on
without anybody asking.

Each entry carries the same fields, in the same order:

| field | what it holds |
| --- | --- |
| **Footing** | `member`, `candidate`, `served`, or `child of <id>` — repeated from the inventory, because a role cannot be read without it |
| **Role** | what this tool is responsible for. Two sentences at most |
| **Owns** | the artifacts that are its to change, and therefore nobody else's |
| **Not its job** | the nearest thing it is *not* responsible for, and whose it is instead |

---

## anoieu

**Footing:** member
**Role:** the static analyzer for `.eo` and `.eos`, the fuzzer that writes
Eunoia nobody would write, and the reporting system that carries what either
finds to whoever owns the file. It also keeps the ecosystem's shared policy, the
inventory of who is in it, and the scripts by which a tool joins.
**Owns:** the checks and their registry; the findings ledger and the workflow
that moves a row through it; `docs/policy.md` and `tools/policy_check.py`;
`docs/vision.md`; `docs/reports/reporting-policy.md`; `tools/ecosystem.json`;
the `*_eo` scripts; and this page.
**Not its job:** deciding what Eunoia means — the manual in `ethos` is the
authority — or settling a finding it has filed, which only an artifact does.
The governance half is audited for a move out, under the name `kanon`.

## cvc5

**Footing:** served
**Role:** the solver, and the author of the proofs everything downstream checks.
It owns CPC, the calculus the rest of the ecosystem is arranged around, and
every tool here is downstream of decisions it made first.
**Owns:** `proofs/eo/cpc/` — the CPC signature and its programs — and the proof
output every checker in the ecosystem consumes.
**Not its job:** adopting anything from this ecosystem. It is not a candidate
and is not asked; the ecosystem exists to serve it, and the arrows point that
way rather than back.

## dokimasia

**Footing:** member
**Role:** reads cvc5's proof-production C++ and asks what no proof step covers —
the scrutiny before office, applied to the code that emits the proofs.
**Owns:** its findings about cvc5's proof production, and the second
implementation of the reporting loop, which is the evidence that the protocol is
shared rather than local.
**Not its job:** the calculus, the checkers, or the proofs themselves. It reads
the code that produces a proof, not the proof.

## ethos

**Footing:** candidate
**Role:** the proof checker: the fast, unverified C++ implementation that
production runs against. It is also the home of the Eunoia manual, which is the
language's authority.
**Owns:** the checker, `user_manual.md`, and the tree the `ethos-eoc` child
project lives in.
**Not its job:** the semantics sets, which are `ethos-eoc`'s, and the Lean side,
which is `logos`'s. A finding about the manual is a finding about the language;
one about the binary is not.

## ethos-eoc

**Footing:** child of `ethos`
**Role:** the Eunoia compiler: it turns a signature and its semantics into a
Lean development, one constructor, type rule, evaluator case and verification
condition per symbol. It also ships the semantics sets the ecosystem is built
on.
**Owns:** the compiler, and the `.eos` semantics sets it ships.
**Not its job:** what a proof means in Lean's *own* terms. It compiles an
embedding and stops there; carrying the meaning across is named work that
nobody has started.

## eudaimonia

**Footing:** member
**Role:** the calculus template — the logos arrangement with the calculus taken
out. Bring a signature and a semantics, get a Lake project with a checker, its
proofs, its regression suite and its documentation.
**Owns:** the template and its generators, the profile a new calculus declares,
and the `euthyna` child project in its tree.
**Not its job:** any particular calculus. CPC is cvc5's and its development is
logos's; the template's subject is the shape, never the content.

## euthyna

**Footing:** child of `eudaimonia`
**Role:** reads the proof logos carries and says what it is made of and where
its weight sits — what is dead, what repeats, and what is structured in a way
that will cost the next regeneration.
**Owns:** its own account, and nothing else. Anything it wants to say to logos
leaves through its parent's reporting discipline, like any other finding.
**Not its job:** maintaining or rewriting the development it reads. It advises
the people who do, and they decide.

## koine

**Footing:** member
**Role:** the shared machinery of the reporting loop, so the protocol has one
implementation rather than one per member — the prompt-drift check first, then
the branch-state reporter and the reply finder.
**Owns:** what its owner decides it owns. The scope is theirs and is not set
here; what has been named for it is the machinery two members already wrote
twice.
**Not its job:** the prompts, or what settles a row. Those differ per tool, and
each tool names its own.

## logos

**Footing:** candidate
**Role:** the Lean development: an executable proof checker for CPC whose
soundness is proven against an independent Lean model of SMT-LIB semantics. It
owns the semantics the compiler reads.
**Owns:** `Cpc.eos` and its cached form, `Cpc/SmtModel.lean`, and the generated
development the ecosystem's trust rests on.
**Not its job:** the signature. CPC is cvc5's file; logos reads it and does not
maintain it.

## sapheneia

**Footing:** child of `anoieu`
**Role:** describes Eunoia as a language definition rather than as a checker's
manual — where the boundary falls between what the language requires and what
one implementation happens to do.
**Owns:** its own account, which is additive: `user_manual.md` in `ethos`
remains the authority, and the account says so on its own front page.
**Not its job:** deciding anything about the language, or reporting a defect.
Where a second reading turns up something actually wrong, it leaves through the
parent's ledger.

## ynoia

**Footing:** child of `anoieu`
**Role:** asks whether the ecosystem's arrangement earns its machinery. It keeps
the account, the register of names, the audit of whether an idea deserves a
repository of its own, the register of work that belongs in somebody else's
tree, and the register of tools that do not exist yet.
**Owns:** `why-eunoia.md`, `names.md`, `proposals.md`, `requests.md` and
`tools.md`, all inside its own directory.
**Not its job:** deciding, approving, or committing anybody to anything. Its
output is an argument with a recommendation at the end; a person decides, and a
repository is created by hand or not at all.
