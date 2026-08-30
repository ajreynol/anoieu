# What anoieu is for

A sketch of the value this tool is meant to deliver, repository by repository,
and a record of how much of it exists. Kept current: every capability below
carries a status, and a milestone that lands one moves its row rather than
adding a paragraph somewhere else.

- ✅ **live** — written, tested, and run over the corpus
- ◐ **partial** — the useful half exists and the limit is stated
- ○ **sketched** — designed in [`design.md`](design.md), not written

---

## The claim

Ethos is a proof checker, and a good one *because* it is lazy: it computes a
type when something asks, checks the program case a proof reaches, and says
nothing about the rest. The consequence is that a *signature* — as opposed to a
proof — is nobody's job. A `define` body with no `:type` is never typed, a
program case is checked when a proof gets there, and a proof rule that can only
ever fail is a legal declaration until someone writes the step that finds out.

anoieu is the eager reader of the same files. It asks about every declaration,
with no proof in hand, no build, and no solver, in under a second. Of the 23
witness files in its suite — each holding one deliberate mistake — **ethos
accepts 19 and answers `correct`**. That number is the whole argument.

The second thing it is for is slower and possibly worth more: every check is a
statement about what Eunoia means, so the check catalogue, its witnesses, and
the differential harness against ethos amount to an executable account of a
language whose `.eos` half is specified today by one README and the compiler
that reads it. See [`language-notes.md`](language-notes.md).

## Status at a glance

| capability | answers | status |
| --- | --- | --- |
| parsing, includes, structure | is this a well-formed signature at all, and where exactly is it not | ✅ |
| attribute contracts | does `:right-assoc-nil`, `:chainable`, `:arg-list`, `:opaque` mean what this declaration can support | ✅ |
| the `:list` and n-ary hazards | does this pattern match the tail, or exactly two elements; can it be matched at all | ✅ |
| dead and unreachable code | which case can never fire, which program nothing reaches, which forward declaration was never defined | ✅ |
| shallow typing | is a rule's conclusion a `Bool`, does a program case return what it declares, is a symbol over-applied | ◐ — where the head settles it; a term whose head is a parameter, or that needs `eo::` evaluation, is not answered |
| desugaring | what does the parser build from what I wrote | ✅ — 33 cases agreeing with ethos term for term |
| documentation | does the docstring still describe the rule | ✅ |
| CI plumbing | baselines, suppression comments, config files, SARIF, many entry points | ✅ |
| full type checking | which rules *may* conclude a non-`Bool` through a program's cases | ○ — [M3](design.md#7-roadmap) |
| the triple | does the signature agree with its `.eos` semantics, and those with SMT-LIB | ○ — [M4](design.md#7-roadmap) |
| solver-backed obligations | is this `:is-list-nil` predicate actually the operator's nil | ○ — [Tier 5](design.md#46-tier-5--opt-in-deeper) |
| editor integration | the same findings while typing, with hover types and cross-triple jumps | ○ — [M5](design.md#7-roadmap) |

---

## cvc5 — the calculus everything downstream is built from

**Today.** Three real defects, found on the first audit and confirmed against
ethos: two programs in `programs/Strings.eo` declaring `Int` and returning
`Bool`, four skolem declarations duplicated verbatim in
`expert/theories/ArithExt.eo`, and 18 docstrings that no longer describe their
rule. Full write-up in [`findings.md`](findings.md); the shareable version is
[`report/cpc-audit.html`](report/cpc-audit.html).

**Why it matters here more than anywhere.** CPC is the input to the Lean
development, to the VC generator, and to every proof cvc5 emits. A defect in it
propagates: the same three findings appear in `logos/install/defs/Cpc.eo`,
because that file is CPC flattened.

**What it gets next.** The triple checks, which is where the rest of the value
is for a calculus this size: every symbol having a semantics, every transform
naming something that exists, and the `:is-list-nil` obligations computed from
the signature rather than discovered when a stage fails.

**The honest limit.** Once the current findings are fixed, CPC will mostly be
clean, and anoieu's value there becomes regression protection: it fires on the
pull request that introduces the next one, which is worth having and is worth
less than the first run.

## ethos — the language, and its own signatures

**Today.** The `<` declared `:right-assoc` with a `Bool` return in
`tests/match-simple.eo` — inert since the file was written, because that test
only ever applies it to two arguments. More generally: ethos's test signatures
are small, numerous, and each exercised by exactly one proof, which is the
condition latent errors need. Plus better messages for four things ethos does
catch (it reports a misordered `declare-rule` field as a missing conclusion,
several lines away), and all of them at once instead of the first.

**The other half.** The specification work belongs to ethos as much as to us.
Each check ships with a manual page explaining what the language requires and
what ethos does with a file that breaks it; each has a witness; the desugarer is
validated case by case against the real parser. Where the two disagree, exactly
one is wrong, and the record of every narrowing so far is in
[`findings.md`](findings.md) — it reads as a list of facts about Eunoia that were
not written down anywhere.

**A possibility worth naming.** A check that proves uncontroversial is a check
ethos could adopt natively — the attribute contracts are declaration-time
properties it could enforce in twenty lines, and it would then need no external
tool for them. That would be a good outcome, not a loss.

## logos — the Lean development

**Today.** Little that is specific: the signatures it installs are flattened
copies of CPC, so it inherits CPC's findings and adds none of its own.

**What it gets next, and it is the largest single item on the roadmap.** logos
owns `Cpc.eos`, the official semantics, and the triple is where the compiler's
own documented gaps live — `ethos/docs/README.md` calls `is_list_nil` "the worst
thing in the compiler" and asks, in its own directions #2 and #5, for exactly two
checks: diff the operators the desugar stage forward-declares against the
`:is-list-nil` blocks a human wrote, and close the `:exclude` list under what it
excludes. anoieu can do the first from the signature alone, because whether a
nil is ground is syntactic — no stage run, no build. `anoieu symbol str.++`
already prints the obligation; what is missing is the other side of the diff.

Beyond those: which symbols have no semantics block, which blocks name symbols
nothing declares, whether the two type rules agree at the sort level, and which
programs will need a hand-written `:lean` termination clause — today discovered
by regenerating a Lean package.

## eudaimonia — the template for other calculi

**Today.** Nothing beyond what any signature gets.

**What it is for.** eudaimonia's promise is that you bring a calculus and get a
checker. Its README lists a *signature contract* — an `and` declared
`:right-assoc-nil true` and translated to `SmtTerm.and`, `true`/`false`
literals — and says outright that a signature which declares `and` and
translates it elsewhere "would break soundness silently: nothing downstream
re-checks that seam." That is a preflight check, and it is the shape of check
anoieu already runs. A `eudaimonia check` that says *your calculus meets the
framework, or here is the line that does not* is the natural fit, and it needs
the triple front end and nothing else.

---

## How the four fit together

**One tool, three thin integrations.** anoieu stays one repository, released as
one versioned package. Each consuming repository owns exactly three things — its
entry points, its baseline, its severity policy — in one `anoieu.json` its own
reviewers can read. The CI job is then one line. Everything else lives here.

**The risk sits here, not there.** anoieu's own CI checks out cvc5 and ethos at
pinned refs and runs the analyzer against a baseline committed in this
repository. A change that invents a false positive fails *this* build before it
can fail anyone else's. That inversion is what earns the right to ask three
repositories to run this on every push.

**Pin a version.** A new check reaches a repository only when someone there
bumps the pin. Widening a check is a minor release, narrowing one is a patch,
renumbering is major.

**Four rungs, stop at any of them.** Report-only annotations → baseline and fail
on new errors → fail on new warnings → burn the baseline down and delete it.

**Order: ethos, cvc5 report-only, cvc5 blocking, logos.** Ethos is the smallest
surface and the right audience for language findings. cvc5 goes report-only
first so its three findings get triaged without build pressure. logos comes last
because its value arrives with the triple.

The whole arrangement, with the workflow files and per-repository configuration,
is [`ci.md`](ci.md).

---

## What this is not

- **Not soundness.** Whether a proof rule is *valid* is what the verification
  conditions `ethos-eoc` emits are for. anoieu's question is the one below that:
  whether a signature and its semantics say something coherent at all.
- **Not a second checker.** Where a judgement needs the type checker or the
  evaluator, ethos is the authority, and anoieu says nothing rather than
  guessing. Every check that fired falsely on CPC was narrowed until it stopped;
  that record is the reason to believe the ones that remain.
- **Not a style tool.** The checks that are matters of taste on a signature that
  is already written are off by default.

## Open questions we are tracking

| question | why it matters | state |
| --- | --- | --- |
| Where does the triple job run? CPC's signature is in cvc5, its semantics in logos. | The most valuable check will run in the repository furthest from where its findings get fixed. | open; shapes what the `.eos` loader takes as input |
| Does cvc5 want its docstring convention enforced? | 18 findings today, and a doc generator would make them matter. | open |
| Should ethos absorb the declaration-time checks? | They are twenty lines there and would need no external tool. | open, and a good outcome either way |
| How stable are check numbers? | Baselines and per-repository policy refer to them by code. | codes are permanent once released; a narrowed check keeps its number |
| Generated signatures in a corpus. | `Cpc.cached.eo` repeats what CPC says, so checking both reports everything twice. | resolved by convention: check sources, not artifacts |

## The documents

| file | what it is |
| --- | --- |
| [`usage.md`](usage.md) | the interface: inputs, commands, options, exit codes |
| [`ci.md`](ci.md) | running this in ethos, logos and cvc5 |
| [`checks.md`](checks.md) | every check and its manual page, generated from the registry |
| [`findings.md`](findings.md) | what the first runs found, and every false positive that had to be shed first |
| [`what-ethos-misses.md`](what-ethos-misses.md) | why ethos does not report these itself, by mechanism |
| [`language-notes.md`](language-notes.md) | what we have established about `.eo` and `.eos`, and where they are unsettled |
| [`design.md`](design.md) | the roadmap, the check catalogue, the architecture |
| [`report/cpc-audit.html`](report/cpc-audit.html) | the CPC audit, written for a reader outside the project |
