# anoieu

A static analyzer for Eunoia signatures (`*.eo`) and Eunoia semantic
configuration files (`*.eos`) — the languages of the
[ethos](https://github.com/cvc5/ethos) proof checker and of `ethos-eoc`, the
Eunoia compiler on the `ethosEoc3` branch.

*Status: the front end and the checks that need no type checker are written and
run on CPC. See [`docs/design.md`](docs/design.md) for where this is going,
[`docs/checks.md`](docs/checks.md) for what it reports today,
[`docs/findings.md`](docs/findings.md) for what it found on the first run,
[`docs/what-ethos-misses.md`](docs/what-ethos-misses.md) for why ethos does not
report these itself, and
[`docs/language-notes.md`](docs/language-notes.md) for what we have established
about the two languages.*

## The name

**Eunoia** is *Eu·noi·a*. Read its syllables backwards and you get *a·noi·eu*,
which is spelled **anoieu** and pronounced **"annoy you"** (/əˈnɔɪ.juː/).

The joke doubles as the description. εὔνοια is Greek for *beautiful thinking*, and
for the goodwill a speaker extends to an audience; it is the shortest English word
containing all five vowels. `anoieu` is the same six letters read the other way,
and the same goodwill pointed the other way: a tool whose whole job is to annoy
you now, in your editor, about the thing that would otherwise annoy you in an
hour — in Lean, or in cvc5, or in a proof-checking failure on a benchmark that
exercises the one program case nobody typed.

Reversal is the technically accurate description too. Ethos reads a signature
*forwards*: it takes what a proof exercises and checks that far, and no further.
anoieu reads the same signature *backwards*: it asks what the signature could
ever be asked to do, and checks all of it, with no proof in hand.

## What it is for

Ethos is a proof checker, and it is lazy by design: a `define` body with no
`:type` is never type checked, a program case is type checked only when a proof
reaches it, and a proof rule whose conclusion is not a `Bool` is a perfectly
legal declaration until somebody writes the step that fails. That laziness is
right for a checker — it is what makes checking fast — and it means a signature
can carry latent errors indefinitely.

anoieu is the eager counterpart. It reports, without running a proof:

- syntax and structure errors, all of them at once rather than the first;
- the invariants the manual states and no tool enforces (a nil terminator of the
  wrong type, a chainable operator with a non-variadic combiner);
- typing facts one level deeper: **a proof rule that can conclude a well-typed
  non-`Bool` term**, a program case whose right-hand side does not have the
  program's declared return type, a case that no input can reach;
- consistency across the *triple* — signature, calculus semantics, SMT semantics
  — which today is checked, when it is checked at all, several tools downstream.

What ethos misses and why is set out by mechanism in
[`docs/what-ethos-misses.md`](docs/what-ethos-misses.md).

It does **not** look for soundness bugs. Whether a rule is *valid* is what the
verification conditions `ethos-eoc` emits are for. anoieu's question is the one
below that: whether the signature and its semantics say something coherent at
all.

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

## The second goal

The `.eos` language is new and specified mostly by prose and by the compiler
that reads it. Every check anoieu implements is a statement about what these
languages mean, so the analyzer and the specification are written together: a
check catalogue with a minimal witness per rule *is* an executable spec, and
disagreements between anoieu and ethos are bugs in exactly one of them, which is
how a second implementation earns its keep. See
[`docs/language-notes.md`](docs/language-notes.md).


## Using it

No dependencies; Python 3.10 or later.

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo     # check a signature
python3 -m anoieu check Cpc.eo --pedantic               # ... and the quieter checks
python3 -m anoieu check Cpc.eo --format json            # or github, for CI
python3 -m anoieu explain EO0041                        # the manual page of a check
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
catches. Today it does not catch 14 of the 18.
