# anoieu_fuzz

A second tool shipped from this repository, beside the analyzer. It began as a
child project under [`docs/policy.md`](../docs/policy.md) and was **folded into
the parent** once it had earned its keep: the island rules it had to break in
order to be useful were the sign that it had stopped being research.

## The name

Its parent's name and the word for what it does. The ecosystem names along a
Greek convention; this is a program with a command line, and somebody looking
for the fuzzer should find it by looking for the fuzzer.

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
  [ynoia](../tools/ynoia/why-eunoia.md) and do not exist.
- **Not a judgement about which checker is wrong.** A disagreement has a
  direction and nothing more; the reference being stricter than the language
  requires is a live explanation for any of them.
- **Not a soundness argument.** A quiet run says the oracles stayed quiet.

## What it has found

An uncaught C++ exception in ethos on `(declare-const f (->))`, an error path
that skips ethos's own `Error:` convention, and three proofs ethos and logos
answer differently — one of them now a committed regression test. Six
reproducers are under [`../tests/fuzz/`](../tests/fuzz), and each is verified
against a real build on every push.

Nothing it found has been filed upstream yet, which is a fact about us rather
than about the findings.

## Running it

    python3 -m anoieu_fuzz run --mode proof        # ethos against a second checker
    python3 -m anoieu_fuzz run --mode signature    # arbitrary signatures, at ethos alone

[`../../docs/fuzzing.md`](../docs/fuzzing.md) is the manual: the oracle, how a
case is shrunk and promoted, and what a third checker has to do to join in.
