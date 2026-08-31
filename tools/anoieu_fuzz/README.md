# anoieu_fuzz

A child project of anoieu, under [`docs/policy.md`](../../docs/policy.md). Started by a
human; it lives in `tools/` and is not part of what this repository ships.

## The name

Descriptive, and **deliberately not Greek** — which is a departure from rule 4 of
[`docs/policy.md`](../../docs/policy.md), recorded below with the others. It is its
parent's name and the word for what it does, because the convention exists to
make a *research account* legible by its title, and this is not one: it is a
program with a command line, and a reader looking for the fuzzer should find it
by looking for the fuzzer. A Greek name here would be decoration, which rule 4
says to avoid in the same breath as it asks for the convention.

## The question

anoieu asks whether a *signature* is coherent. This asks whether the **programs
that read signatures** behave when one is not: it writes Eunoia nobody would
write, hands it to a checker, and watches for the answer a checker should never
give.

It is semantics-free by construction. Everything it reports is a fact about two
runs rather than about mathematics — two checkers disagreeing about one file, a
checker dying without saying why, a checker never answering — which is why it
can say something about `ethos` and `logos` without having a position on what
either of them ought to prove.

## What it is not

- **Not a research-quality fuzzer.** It is a deliberate baseline: grammar-directed
  generation, mutation of a seed corpus, five verdict-level oracles, and no
  instrumentation anywhere. Coverage guidance, derivations built from the
  calculus and a soundness oracle are named in
  [ynoia](../ynoia/why-eunoia.md) and do not exist.
- **Not a judgement about which checker is wrong.** A disagreement has a
  direction and nothing more; the reference being stricter than the language
  requires is a live explanation for any of them.
- **Not a soundness argument.** A quiet run says the oracles stayed quiet.

## Status under rule 10

It has **earned its keep**: an uncaught C++ exception in ethos on
`(declare-const f (->))`, an error path that skips ethos's own `Error:`
convention, and three proofs ethos and logos answer differently — one now a
committed regression test. Six reproducers are under
[`../../tests/fuzz/`](../../tests/fuzz).

It therefore **breaks the island rules, and the breaks are named** rather than
repaired:

| rule | how it is broken |
| --- | --- |
| **2**, imports nothing from the parent | it imports `anoieu.diagnostics` and `anoieu.fingerprint` |
| **2**, the parent imports nothing from it | `tools/gen_open_findings.py` imports its `report` module |
| **2**, not in CI | two CI steps run it |
| **2**, deleting it changes nothing | deleting it fails the build |
| **3**, not advertised | it is on the front page and in the documentation index |
| **4**, named along the convention | the name is descriptive rather than Greek — see *The name* above |

**The promotion decision is open**, and it is the maintainer's: either its own
repository, or folding into the parent as a second shipped tool. Until somebody
takes it, this is a child project that does not fit the definition, held in that
state deliberately.

## Running it

    python3 -m tools.anoieu_fuzz run --mode proof        # ethos against a second checker
    python3 -m tools.anoieu_fuzz run --mode signature    # arbitrary signatures, at ethos alone

[`../../docs/fuzzing.md`](../../docs/fuzzing.md) is the manual: the oracle, how a
case is shrunk and promoted, and what a third checker has to do to join in.
