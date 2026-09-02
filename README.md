# anoieu

A static analyzer for Eunoia signatures (`*.eo`) and Eunoia semantic
configuration files (`*.eos`) — the languages of the
[ethos](https://github.com/cvc5/ethos) proof checker and of `ethos-eoc`, the
Eunoia compiler on the `ethosEoc3` branch.

*Status: the front end, the checks that need no type checker, a shallow typing
pass, the desugarer and the CI plumbing are written, and run over CPC on every
push — where they have found three real bugs. A fuzzer for the checkers
themselves,* [the anoieu fuzzer](docs/fuzzing.md)*, is the newest part.*

## Three things this repository is

**A tool**, first: an analyzer you run over a signature, in an editor or in CI,
that reports what ethos accepts and should not.

**And a reporting system.** A finding is about *someone else's* file — a program in cvc5's calculus, a test
signature in ethos, a semantics set in logos, a gap in the language itself — so
it has to be published where its owner will read it, argued where they can
disagree with it, and tracked until it is resolved or declined. This repository
is that somewhere.

**And the place the Eunoia ecosystem's shared policy is kept.** How a repository
in this ecosystem is arranged, what its front page must say about who is writing
it, how tools talk to one another, and what may be kept in a tree that is not
part of what it ships — that is [`docs/policy.md`](docs/policy.md), written to
be adopted rather than admired. It is arguably the most useful thing here: the
analyzer reports on four projects, and the policy is what lets a fifth join
without anybody negotiating it from scratch.
[Joining](docs/policy.md#joining-the-eunoia-ecosystem) takes one sentence in
your README and one CI step, and anoieu checks it.

> **A successful pass is not a clean bill of health.**
>
> When anoieu reports nothing, that is a fact about the checks it ran, not about
> your signature. The analysis is partial by construction — whole classes of
> error have no check at all, the type reasoning is shallow, and every check has
> been narrowed until it stopped reporting things that were not defects. A green
> run here, or in your CI, or at the end of a report, is not evidence that a
> signature, a semantics or a triple is sound.
>
> We publish defects and never assurances, deliberately: a false sense of
> security is much harder to withdraw than a wrong finding. The position in full,
> shared with [dokimasia](https://github.com/ajreynol/dokimasia), is
> [`docs/reports/reporting-policy.md`](docs/reports/reporting-policy.md).

## What it finds

Without running a proof:

- **syntax and structure errors** — all of them at once, rather than the first;
- **invariants the manual states and no tool enforces**: a nil terminator of the
  wrong type, a chainable operator with a non-variadic combiner;
- **typing facts one level deeper**: a proof rule that can conclude a well-typed
  non-`Bool` term, a program case whose right-hand side does not have the
  program's declared return type, a case that no input can reach;
- **disagreements across the triple** — signature, calculus semantics, SMT
  semantics — which today surface, if at all, several tools downstream.

It does **not** look for soundness bugs. Whether a rule is *valid* is what the
verification conditions `ethos-eoc` emits are for; anoieu's question is the one
below that, whether a signature and its semantics say something coherent at all.
Ethos is lazy by design — a program case is type checked only when a proof
reaches it — so a signature can carry a latent error for as long as no proof
happens to exercise it. anoieu is the eager counterpart.

```text
theories/Bools.eo:4:22: error[EO0041]: the nil terminator of `or` has the wrong type
  |
4 | (declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
  |                                                        ^ this has type Int
  = note: `or` is marked `:right-assoc-nil`, so its nil must have type Bool
  = help: ethos accepts the declaration; the mismatch appears at the first
          application of the operator whose type is asked for
```

## The other half: the anoieu fuzzer

anoieu asks whether a signature is coherent. **The anoieu fuzzer** asks whether
the programs that *read* signatures behave when one is not — it writes Eunoia
nobody would write, hands it to a checker, and watches for the answer a checker
should never give. It is semantics-free by construction, because everything it
reports is a fact about two runs rather than about mathematics: two checkers
disagreeing about one file, a checker dying without saying why, a checker never
answering.

It is a **baseline**, deliberately: grammar-directed generation, mutation of a
seed corpus, five verdict-level oracles, and no instrumentation anywhere. What a
research-quality one would add — coverage guidance, derivations built from the
calculus, a soundness oracle, the generated Lean checker used as a second
implementation — is one of the
future projects nobody has started, and does not exist.

```bash
ETHOS=… LOGOS=… python3 -m anoieu_fuzz run --mode proof -n 2000       # ethos against logos, on CPC
ETHOS=…              python3 -m anoieu_fuzz run --mode signature      # arbitrary signatures, at ethos
```

Findings are shrunk to a reproducer, deduplicated into buckets, and then go into
**the same report as everything else** — the same ledger, the same fingerprints,
the same renderers — under codes `FUZ0001`–`FUZ0005`, which is the marker that
says a checker was provoked rather than a signature read. A checker accepting
what the reference refuses is an error; refusing what it accepts is a warning. The first few thousand
cases produced an uncaught C++ exception in ethos on `(declare-const f (->))`,
three proofs that ethos and logos answer differently — one of them a *committed
regression test* — and an ethos error path that skips its own `Error:`
convention. Six reproducers are committed under
[`tests/fuzz/`](tests/fuzz); nothing is filed upstream yet.
[`docs/fuzzing.md`](docs/fuzzing.md) has the caveats and what a third checker
has to do to join in.


## If you own a tool in the Eunoia ecosystem

[`docs/reports/reports.md`](docs/reports/reports.md) carries every open ask anoieu makes of
anyone, each with an id, a state, and the reasoning underneath it:

| you own | waiting for you |
| --- | --- |
| **cvc5** — the CPC signature | [2 requests they made of us; 1 finding fixed, and 1 we had recorded as fixed that never was](docs/reports/reports.md#cvc5--the-calculus-everything-downstream-is-built-from) |
| **ethos** — the proof checker | [3 confirmed defects, 3 diagnostics worth improving, 1 CI adoption, and 2 the fuzzer found: a crash and an error path with no location](docs/reports/reports.md#ethos--the-proof-checker-and-its-own-signatures) |
| **ethos-eoc** — the Eunoia compiler | [3 integrations, including the `is_list_nil` diff its own docs ask for](docs/reports/reports.md#ethos-eoc--the-eunoia-compiler) |
| **logos** — the Lean development | [1 regeneration, 1 CI adoption, and an open question about a regression test of theirs that ethos will not take; the dead entry is fixed and closed](docs/reports/reports.md#logos--the-lean-development) |
| **eudaimonia** — the calculus template | [2 preflight integrations](docs/reports/reports.md#eudaimonia--the-template-for-other-calculi) |
| **Eunoia** — the language and its manual | [7 proposed changes, from what writing the analyzer turned up](docs/reports/reports.md#eunoia-itself--the-language-and-its-manual) |

We would rather show you what is checked than promise anything. Every push runs:

| what is checked | the evidence |
| --- | --- |
| each check reports the minimal signature written for it, and stays silent on the one it should not | [`tests/witnesses/`](tests/witnesses) — one file per case, readable in a minute. The suite also prints which checks have no witness yet |
| what **ethos** says about every one of those files, unchanged since a real run recorded it | [`tests/oracle.json`](tests/oracle.json) — written by running ethos, never by hand. This is what backs "ethos accepts this and should not" |
| CPC reports exactly what a committed baseline says, warnings denied | [`tests/corpus/cpc-baseline.json`](tests/corpus/cpc-baseline.json) — a change that invents a false positive fails *this* build before it reaches yours |
| the report matches the commits it says it was measured against | [`docs/reports/corpus.md`](docs/reports/corpus.md) and `tools/deps.lock`, re-measured on every push |

Anything else we say about how we will behave — narrowing a check that fired
wrongly, filing nothing twice — is an intention rather than a guarantee. Those
are written down in [`docs/reports/reporting-policy.md`](docs/reports/reporting-policy.md), and worth
whatever our record of keeping them is worth; that record is the log in
[`docs/reports/reports.md`](docs/reports/reports.md).

Working one of these with an assistant is routine enough that we keep a prompt
for it. What comes back is your triage rather than a verdict, and we treat it
that way: nothing on our side files anything in your repository, and no reply
closes a row until the artifact it names says what happened.

## Starting from scratch

Everything anoieu reads belongs to somebody else, so a checkout of this
repository on its own has nothing to report on.
[`scripts/install_eo`](scripts/install_eo) fetches the rest of the ecosystem, and
is the first command to run:

```bash
git clone https://github.com/ajreynol/anoieu
cd anoieu
scripts/install_eo                   # clone the rest of the ecosystem, beside this
scripts/install_eo --dry-run         # ... or print those commands and run none
scripts/install_eo --status          # ... or say what is here, and what disagrees
```

It puts ethos, logos, eudaimonia, dokimasia and koine beside this checkout,
writes the map the other commands resolve a repo id through, and leaves cvc5 —
the one tree nothing here needs a working copy of — until you ask for it. **Only
a default branch is ever installed**, so where that is not the whole story it
says so rather than acting: cloning ethos tells you that `ethos-eoc`, the
compiler that lives in `ethos/tools/eoc`, has its current work on `ethosEoc3`,
and gives you the one line that gets it. `--status` is what to run afterwards,
and next month: it says which branch each tree is on, whether a child project is
the current copy, and what has drifted. The options are in
[`docs/usage.md`](docs/usage.md#the-rest-of-the-ecosystem); the other commands,
for welcoming a tool, joining, and carrying findings, are in
[`docs/coherence.md`](docs/coherence.md#the-scripts).

## The documentation

| | |
| --- | --- |
| [`docs/reports/reports.md`](docs/reports/reports.md) | what anoieu is asking of whom, how each finding was confirmed, and what came back |
| [`docs/reports/reporting-workflow.md`](docs/reports/reporting-workflow.md) | how a finding is handled: the conventions, the three prompts, and how to run these checks in your own CI |
| [`docs/usage.md`](docs/usage.md) | the interface — every command and option, configuration, baselines, suppression, and the test suite |
| [`docs/fuzzing.md`](docs/fuzzing.md) | the anoieu fuzzer, the fuzzer: what its oracle is, how a reproducer is shrunk, and how to point it at your checker |
| [`docs/reports/postmortem.md`](docs/reports/postmortem.md) | one round of the reporting loop, as a log: what the assistant at the far end did with each finding, what we got wrong, and what changed |
| [`docs/reports/reporting-policy.md`](docs/reports/reporting-policy.md) | what may be published about somebody else's code, and why |
| [`docs/notes.md`](docs/notes.md) | what ethos misses, what we have established about `.eo` and `.eos`, and the design |
| [`docs/README.md`](docs/README.md) | the index, and the files a run generates: the open findings, the corpus, the check catalogue |

## The name

**Eunoia** is *Eu·noi·a*. Read its syllables backwards and you get *a·noi·eu*,
which is spelled **anoieu** and pronounced **"annoy you"** (/əˈnɔɪ.juː/).

The joke doubles as the description. εὔνοια is Greek for *beautiful thinking*,
and for the goodwill a speaker extends to an audience. `anoieu` is the same six
letters read the other way, and the same goodwill pointed the other way: a tool
whose whole job is to annoy you now, in your editor, about the thing that would
otherwise annoy you in an hour — in Lean, or in cvc5, or in a proof-checking
failure on a benchmark that exercises the one program case nobody typed.

Reversal is the technically accurate description too. Ethos reads a signature
*forwards*: it takes what a proof exercises and checks that far, and no further.
anoieu reads the same signature *backwards*: it asks what the signature could
ever be asked to do, and checks all of it, with no proof in hand.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
repository policy — which it also keeps, in
[`docs/policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/policy.md).
Keeping it is not an exemption from it: this README is checked against that
policy on every push, by the same command any other repository would run.

**Written by AI agents, under light human supervision.** A human directs the
work, reads what is published and decides what is filed; nobody vets the
internal design, and nothing reaches another project's issue tracker without
review.

**And a human runs every `git push` and every `git clone`.** No commit has
entered the public history of this repository except by a person executing it,
so a human intention stands behind every one — which is the fact anything
reading this history needs in order to interpret it, and it is stated here
because it will not stay true by accident. **If that changes, this paragraph
changes with it**, and the change is announced rather than discovered. [`docs/reports/reporting-policy.md`](docs/reports/reporting-policy.md) says what that does and does
not cover, and why the intended audience is experts.
