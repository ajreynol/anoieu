# anoieu

A static analyzer for Eunoia signatures (`*.eo`) and Eunoia semantic
configuration files (`*.eos`) — the languages of the
[ethos](https://github.com/cvc5/ethos) proof checker and of `ethos-eoc`, the
Eunoia compiler on the `ethosEoc3` branch.

*Status: the front end, the checks that need no type checker, a shallow typing
pass, the desugarer and the CI plumbing are written, and run over CPC on every
push — where they have found three real bugs.*

**Start here:** [`docs/README.md`](docs/README.md) — what anoieu is for,
repository by repository, and how much of it exists today. Then
[`docs/usage.md`](docs/usage.md) to run it, [`docs/findings.md`](docs/findings.md)
for what it has found, and [`docs/ci.md`](docs/ci.md) for putting it in CI.

## Two things this repository is

**A tool**, first: an analyzer you run over a signature, in an editor or in CI,
that reports what ethos accepts and should not. That is the primary purpose and
everything else follows from it.

**And a reporting system.** Almost nothing anoieu finds is about anoieu. A
finding is about *someone else's* file — a program in cvc5's calculus, a test
signature in ethos, a semantics set in logos, a gap in the language itself — so
the findings have to be published somewhere their owners will read them, argued
where they can be disagreed with, and tracked until they are resolved or
declined. This repository is that somewhere.

Where those findings live, what we promise about each, and which of them are
waiting for you is [below](#where-the-findings-live).

### And the thing we will not tell you

> **A successful pass is not a clean bill of health.**
>
> When anoieu reports nothing, that is a fact about the checks it ran, not about
> your signature. The analysis is partial by construction — whole classes of
> error have no check at all, the type reasoning is shallow, and every check has
> been narrowed until it stopped reporting things that were not defects. A green
> run here, or in your CI, or at the end of a report, is not evidence that a
> signature, a semantics or a triple is sound, and nothing downstream should
> treat it as such.
>
> We publish defects and never assurances, deliberately: a false sense of
> security is much harder to withdraw than a wrong finding. See
> [What we do not publish](#what-we-do-not-publish).

## What it finds

anoieu reads a signature without running a proof, and reports:

- **syntax and structure errors** — all of them at once, rather than the first;
- **invariants the manual states and no tool enforces**: a nil terminator of the
  wrong type, a chainable operator with a non-variadic combiner;
- **typing facts one level deeper**: a proof rule that can conclude a well-typed
  non-`Bool` term, a program case whose right-hand side does not have the
  program's declared return type, a case that no input can reach;
- **disagreements across the triple** — signature, calculus semantics, SMT
  semantics — which today surface, if at all, several tools downstream.

It does **not** look for soundness bugs. Whether a rule is *valid* is what the
verification conditions `ethos-eoc` emits are for. anoieu's question is the one
below that: whether a signature and its semantics say something coherent at all.

### Why these are not caught already

Ethos is a proof checker, and it is lazy by design: a `define` body with no
`:type` is never type checked, a program case is type checked only when a proof
reaches it, and a rule whose conclusion is not a `Bool` is a legal declaration
until somebody writes the step that fails. That is the right trade for a checker
— it is what makes checking fast — and it means a signature can carry a latent
error for as long as no proof happens to exercise it.

anoieu is the eager counterpart: it asks what a signature could ever be asked to
do, rather than what one proof asked of it. What ethos misses, and by which
mechanism, is set out in
[`docs/what-ethos-misses.md`](docs/what-ethos-misses.md).

## The triple

The unit of analysis is not a file but a triple:

| leg | file | says |
| --- | --- | --- |
| **signature** | `Cpc.eo` | the calculus: sorts, symbols, their type rules, programs, proof rules |
| **calculus semantics** | `Cpc.eos` | what each symbol of the calculus becomes in the SMT embedding |
| **SMT semantics** | `smt.eos` | what each SMT-LIB symbol means to a model — its type, its value |

Each leg is checkable on its own, and the interesting findings are between legs:
a symbol the signature declares and the semantics never mentions, a transform
whose target does not exist in the SMT semantics, an `:is-list-nil` predicate
that is required and missing (or present and dead), an `:exclude` list that is
not closed under what it excludes.

## Using it

No dependencies; Python 3.10 or later. Full interface reference in
[`docs/usage.md`](docs/usage.md).

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo     # check a signature
python3 -m anoieu check Cpc.eo --pedantic               # ... and the quieter checks
python3 -m anoieu check Cpc.eo --format json            # or github, for CI
python3 -m anoieu desugar Cpc.eo --term '(or a b c)'    # what the parser builds from a term
python3 -m anoieu symbol str.++ Cpc.eo                 # one symbol: type, sugar, who names it
python3 -m anoieu explain EO0041                       # the manual page of a check
python3 -m anoieu list-checks                           # every check and what it says
python3 -m anoieu stats Cpc.eo                          # what a signature holds
```

A finding looks like this:

```text
theories/Bools.eo:4:22: error[EO0041]: the nil terminator of `or` has the wrong type
  |
4 | (declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
  |                                                        ^ this has type Int
  = note: `or` is marked `:right-assoc-nil`, so its nil must have type Bool
  = help: ethos accepts the declaration; the mismatch appears at the first
          application of the operator whose type is asked for
```

## Where the findings live

A finding is only worth anything where its owner will see it, so the record is
kept three ways, with different jobs:

| | where | what it is |
| --- | --- | --- |
| **Open findings** | [`docs/open-findings.md`](docs/open-findings.md) | every finding the checks report, one row each, generated and **additive** — the generator adds and never removes, and closing a row is a judgement made by review |
| **The curated register** | [`docs/README.md`](docs/README.md) | the first pass at the above, hand-written and argued, kept as the worked example of what a report should say |
| **The log** | [`docs/upstream.md`](docs/upstream.md) | what was reported and what came back — accepted, declined, deferred, and what the analyzer changed when a finding turned out to be wrong |

So far: **two findings fixed upstream in cvc5**, one declined because our
analysis was wrong, one impact claim overstated and corrected. The declined one
produced the most useful change in the tool — reachability is now asked per
*ordered profile*, the way a consumer actually loads a signature.

### If you own a tool in the Eunoia ecosystem, look here

**[`docs/README.md`](docs/README.md)** is the page. It carries every open ask
anoieu makes of anyone, each with an id, a state, and the reasoning underneath
it; anything already ruled on is in the log instead:

| you own | waiting for you | jump to |
| --- | --- | --- |
| **cvc5** — the CPC signature | 2 requests they made of us; 2 findings already fixed | [cvc5](docs/README.md#cvc5--the-calculus-everything-downstream-is-built-from) |
| **ethos** — the proof checker | 3 confirmed defects, 3 diagnostics worth improving, 1 CI adoption | [ethos](docs/README.md#ethos--the-proof-checker-and-its-own-signatures) |
| **ethos-eoc** — the Eunoia compiler | 3 integrations, including the `is_list_nil` diff its own docs ask for | [ethos-eoc](docs/README.md#ethos-eoc--the-eunoia-compiler) |
| **logos** — the Lean development | 1 dead entry, 1 regeneration, 1 CI adoption | [logos](docs/README.md#logos--the-lean-development) |
| **eudaimonia** — the calculus template | 2 preflight integrations | [eudaimonia](docs/README.md#eudaimonia--the-template-for-other-calculi) |
| **Eunoia** — the language and its manual | 7 proposed changes, from what writing the analyzer turned up | [Eunoia](docs/README.md#eunoia-itself--the-language-and-its-manual) |

Working through one of those with an assistant is a routine enough job that we
keep a suggested prompt for it: [`docs/workflows.md`](docs/workflows.md). What
comes back is your triage rather than a verdict, and we treat it that way —
nothing on our side files anything in your repository, and no reply closes a row
until the branch it names says what happened.

### What we promise about a finding

- **It was confirmed before it was filed.** Every defect in that table was
  reproduced in the smallest signature that shows it, and run through ethos, and
  the output is quoted. [`findings.md`](docs/findings.md) has the workings.
- **A false positive is our bug, not yours.** Every check that fired wrongly on
  CPC was narrowed until it stopped, and each narrowing is recorded as what it
  was: a fact about Eunoia we had got wrong. anoieu's own CI runs it over pinned
  checkouts of cvc5 and ethos, so a change that invents a false positive fails
  *this* build before it reaches yours.
- **Nothing is filed twice.** The table is the single record; a report written
  for a wider audience, like the [CPC audit](docs/report/cpc-audit.html), is
  rendered from the same findings rather than restating them.
- **Declining is an outcome.** A row can end in "won't fix" with a reason, and
  the check that produced it gets a suppression comment in your file or a
  `disable` in your config. Both are better than an argument repeated monthly.

## The name

**Eunoia** is *Eu·noi·a*. Read its syllables backwards and you get *a·noi·eu*,
which is spelled **anoieu** and pronounced **"annoy you"** (/əˈnɔɪ.juː/).

The joke doubles as the description. εὔνοια is Greek for *beautiful thinking*, and
for the goodwill a speaker extends to an audience. `anoieu` is the same six letters
read the other way, and the same goodwill pointed the other way: a tool whose whole
job is to annoy you now, in your editor, about the thing that would otherwise annoy
you in an hour — in Lean, or in cvc5, or in a proof-checking failure on a benchmark
that exercises the one program case nobody typed.

Reversal is the technically accurate description too. Ethos reads a signature
*forwards*: it takes what a proof exercises and checks that far, and no further.
anoieu reads the same signature *backwards*: it asks what the signature could
ever be asked to do, and checks all of it, with no proof in hand.

## The second goal: writing the languages down

The `.eos` language is new and specified mostly by prose and by the compiler
that reads it. Every check anoieu implements is a statement about what these
languages mean, so the analyzer and the specification are written together: a
check catalogue with a minimal witness per rule *is* an executable spec, and
disagreements between anoieu and ethos are bugs in exactly one of them, which is
how a second implementation earns its keep. See
[`docs/language-notes.md`](docs/language-notes.md).

## In CI

The long-term goal is for ethos, logos and cvc5 to run this on every push:
[`docs/ci.md`](docs/ci.md) sets out the arrangement — one versioned tool, a
policy file and a baseline owned by each repository, and a corpus job here that
fails *this* build when a change would invent a false positive in theirs.

## Running the report

```bash
python3 tools/run.py                   # move to each tip, then measure
python3 tools/run.py --pinned --check  # re-measure the recorded commits
```

Clones every project the report is about into `deps/` and updates it — shallow,
sparse, and never built, because the analysis reads text. Nothing reads a
checkout on your machine, so a report is a property of named commits rather than
of where it was produced. It then records what was read in
[`docs/versions.md`](docs/versions.md), rewrites the counts in
[`docs/corpus.md`](docs/corpus.md), and appends anything new to
[`docs/open-findings.md`](docs/open-findings.md) — which is additive: the
generator never removes a row. [`tools/deps.json`](tools/deps.json) says which
projects and which refs, and `tools/deps.lock` records the exact commits a
report was measured against — `--pinned` restores those, so the report can be
reproduced from nothing but this repository. `docs/ci.md` has the whole
arrangement.

## Testing it

```bash
python3 tests/run.py                    # every check against its witness files
ETHOS=<ethos>/build/src/ethos \
  python3 tests/run.py --oracle         # ... and what ethos says about each
python3 tools/sweep.py <dir>...         # run over a corpus; report crashes and counts
python3 tools/gen_checks_doc.py         # rewrite docs/checks.md from the registry
```

Every check owns a witness: a file that must be reported, and where the
distinction is interesting, one that must not be. `--oracle` runs ethos on the
same files, which is what says whether a finding is something ethos already
catches. Today it does not catch 43 of the 49.

## How this repository is maintained

**Written by an AI agent, under light human supervision.** The code, the checks, the
witnesses and the documents here were drafted by an agent working in this
repository; a human maintainer directs the work, reviews it, and decides what is
committed and what is filed elsewhere. Nothing reaches another project's issue
tracker without that review.

## What we do not publish

**No clean bills of health.** anoieu publishes defects. It does not publish
assurances about anyone's files — no "this signature is sound", no coverage
score, no "the triple is consistent", no ranking of one tool against another.
Where a check reports nothing, the most that is ever said is that *those checks
reported nothing*.

The reason is that our silence is weak evidence and reads as strong. Every check
here is partial by construction: the type analysis is shallow, whole classes of
error have no check at all, and each check has been narrowed until it stopped
reporting things that were not defects. A reader who takes a quiet run for a
sound artifact has been misled by us, and the next analysis effort that inherits
that impression is worse off than if we had published nothing. A false sense of
security is much harder to withdraw than a wrong finding.

The one exception is discussion of the ecosystem as a whole, where the subject
is the arrangement and its trade-offs rather than an audit of anyone's artifact.

## A suggested AI workflow for using anoieu

Guidance rather than machinery, at
[**`docs/workflows.md`**](docs/workflows.md): who runs each part, what a reply
from a project does and does not settle, and two prompts — one for the project
that owns a finding, one for the follow-up here. The conventions they rest on,
including the shape a reply takes and what an agent may change on the strength
of one, are in [`docs/triage.md`](docs/triage.md), and are written so another
analyzer can adopt them.
