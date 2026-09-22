# anoieu_fuzz

A second tool shipped from this repository, beside the analyzer. It began as a
child project under [`docs/policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and was **folded into
the parent** once it had earned its keep: it was emitting into the report that
already existed, running in the parent's CI and being called by the parent's
commands, which is what *shipping* looks like rather than research. The reasoning
at the time leaned on an isolation rule the shared policy has since retired —
a child may now share all three of those — so the fold is recorded here as what
happened and not as what any rule required. See
[`docs/history.md`](../docs/history.md).

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
  [ynoia](https://github.com/ajreynol/kanon/blob/main/tools/ynoia/docs/why-eunoia.md) and do not exist.
- **Not a judgement about which checker is wrong.** A disagreement has a
  direction and nothing more; the reference being stricter than the language
  requires is a live explanation for any of them.
- **Not a soundness argument.** A quiet run says the oracles stayed quiet.

## What it has found

An uncaught C++ exception in ethos on `(declare-const f (->))`, an error path
that skips ethos's own `Error:` convention, and three proofs ethos and logos
answer differently — one of them now a committed regression test. Then, once
proof cases were assembled around one construct at a time rather than written
from the grammar alone: a **segfault** in ethos on `(declare-const y (_))`;
logos accepting a step whose stated conclusion the rule does not derive, and a
binary literal where a constructor name belongs; and logos refusing parametric
datatypes and binders, both of which cvc5 emits. Fourteen reproducers are under
[`../tests/fuzz/`](../tests/fuzz), and each is verified against a real build on
every push.

The counts are of *our* rows and calibrate nothing about either checker — see
[what may be said](../bug_db/reporting-policy.md#what-we-publish). Where a
construct was found in cvc5's own output, the entry says how often, because
"logos does not parse this" and "logos does not parse this and cvc5 prints it"
are different claims and only the second is worth somebody's afternoon.

**Three of them have been carried, accepted and fixed** — the crash and two
error paths that reached no `Error: <file>:<line>` — on ethos's `anoieu-findings`
branch at `292201c2`, read 2026-09-17. They are closed here **before the change
has landed**, which is a debt rather than a result:
[`verdicts.py`](../anoieu_analyzer/reporting/verdicts.py) is the audit that reads it back, and it
answers *not yet* for all three. What closes a row is in
[Closure](../bug_db/README.md#closure).

## Running it

    python3 -m anoieu_fuzz run --mode proof        # ethos against a second checker
    python3 -m anoieu_fuzz run --mode signature    # arbitrary signatures, at ethos alone

[`fuzzing.md`](fuzzing.md) is the manual: the oracle, how a
case is shrunk and promoted, and what a third checker has to do to join in.
