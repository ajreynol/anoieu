# Using anoieu

What the tool takes, what it does with it, and what every option means. Written
against 0.1.0, which is the front end, the checks that need no type checker, and
a shallow typing pass; the `.eos` side is accepted on the command line and not
read yet.

## Installing

Python 3.10 or later, no dependencies. From a checkout:

```bash
python3 -m anoieu <command>          # run in place
pip install -e .                     # or install, which gives you `anoieu`
```

Both spellings are the same program; the examples below use the first.

## The input

**One entry point, and its include graph.** You name a signature file, and
anoieu reads it, follows every `(include "...")` and `(reference "...")` from
there, and analyses what that closure declares:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo
```

Three things follow from that.

- **Include paths resolve against the file that includes them**, the way ethos
  resolves them, so a run gives the same answer from any working directory.
- **The entry point is part of the question.** `Cpc.eo` and
  `expert/CpcExpert.eo` are two different signatures, and a finding like "this
  program is declared and never defined" is true of one and not the other. Check
  each entry point a proof might name.
- **A file read via `reference` is read as SMT-LIB**, not as Eunoia, so
  `declare-fun` and `assert` in a `.smt2` are ordinary there and an error in a
  signature.

`--semantics` and `--smt-semantics` name the two `.eos` sets of a triple. They
are accepted, and a run that passes one says on stderr that it is not read yet:
the checks over a triple are M4, see [`design.md`](design.md).

## The commands

### `check` — the one you will use

```bash
python3 -m anoieu check FILE [options]
```

Reads the signature, runs every check that is on, and prints what it found.

| option | what it does |
| --- | --- |
| `--pedantic` | also run the checks that are off by default (see below) |
| `--only CODE` | run only this check; repeatable, and an unknown code is an error rather than silence |
| `--format text\|json\|github` | how to print; `text` is the default |
| `--deny-warnings` | exit non-zero on warnings too, not only on errors |
| `--no-color` | plain text, which is also the default when stdout is not a terminal |
| `--semantics FILE`, `--smt-semantics FILE` | the other two legs of the triple; accepted, not read yet |

Exit codes: **0** nothing worse than a warning, **1** at least one error (or a
warning under `--deny-warnings`), **2** the command itself was wrong.

### `explain` — the manual page of a check

```bash
python3 -m anoieu explain EO0041
```

Prints what the check says, why it is a check, what ethos does with the same
file, and how to fix it. The page is written beside the check in the source, so
the two cannot drift, and `docs/checks.md` is the whole set rendered by
`tools/gen_checks_doc.py`.

### `list-checks` — the inventory

```bash
python3 -m anoieu list-checks
```

Every code, one line each, marked when it is off by default.

### `desugar` — what the parser builds

```bash
python3 -m anoieu desugar Cpc.eo --term '(or a b c)' --curried
python3 -m anoieu desugar Cpc.eo --term '(or x xs)' --params '((x Bool) (xs Bool :list))'
```

```text
-- in the scope of context.eo
   written    (or a b c)
   desugared  (or a (or b (or c false)))
   curried    (_ (or a) (_ (or b) (_ (or c) false)))
```

The term is read in the signature's scope, so every attribute that shapes an
application applies: nil terminators, `:list` parameters folded in with
`eo::list_concat`, chains expanded through their combining operator, binders
turned into variable lists, `eo::define` inlined. `--params` gives the term a
parameter list to be read under, which is what a `:list` annotation needs;
`--curried` also prints the core form, the one ethos prints in its errors.

### `symbol` — one symbol, and everything a run knows about it

```bash
python3 -m anoieu symbol str.++ Cpc.eo
```

```text
-- str.++
   declared   theories/Strings.eo:68  (parameterized-const)
   type       (-> (Seq T) (Seq T) (Seq T))
   parameter  T Type  :implicit
   attribute  :right-assoc-nil ($seq_empty (Seq T))
   applied
     (str.++ t1)                  ->  (str.++ t1 (eo::nil str.++ (eo::typeof t1)))
     (str.++ t1 t2)               ->  (str.++ t1 (str.++ t2 (eo::nil str.++ (eo::typeof t1))))
   nil        ($seq_empty (Seq T))  (depends on the type)
   obligation this operator needs an `:is-list-nil` case in the calculus semantics
   named by   60: program $str_eval_str_in_re_rec, ... and 54 more
```

### `stats` — what a signature holds

```bash
python3 -m anoieu stats <cvc5>/proofs/eo/cpc/Cpc.eo
```

```text
-- Cpc.eo
   files          35
   declarations   190  (33 n-ary)
   definitions    150
   programs       241
   proof rules    593
   literal kinds  4
   documented     166/593 rules
```

## Reading a finding

```text
theories/Bools.eo:4:22: error[EO0041]: the nil terminator of `or` has the wrong type
  |
4 | (declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
  |                                                        ^ this has type Int
  = note: `or` is marked `:right-assoc-nil`, so its nil must have type Bool
  = help: ethos accepts the declaration; the mismatch appears at the first
          application of the operator whose type is asked for
```

Paths are relative to the entry point's directory, so a log reads the same
whichever machine wrote it. The caret is on the text that produced the finding,
which for a desugared term is the surface it was written as. `note` lines carry
the reasoning and the second location where there is one; `help` says what to do.
Every finding ends up somewhere in `anoieu explain <CODE>`.

**Severities.** `error` is wrong under every reading — no instantiation makes it
work. `warning` is almost certainly a mistake but a reading exists. `hint` states
a fact about the signature and leaves the judgement to you. Anything anoieu
cannot decide it says nothing about, which is why a check will go quiet rather
than guess.

**On by default** is everything except the checks whose findings are a matter of
taste on a signature that is already written — the missing-docstring check, the
unused-parameter check, the dead-program check. `--pedantic` turns those on.

## In a pipeline

```bash
python3 -m anoieu check Cpc.eo --format github     # annotations in GitHub Actions
python3 -m anoieu check Cpc.eo --format json | jq '.[] | select(.severity=="error")'
```

The JSON is a flat list, one object per finding, with `code`, `severity`,
`message`, `file`, `line`, `column`, `endLine`, `endColumn`, `label`, `notes`
and `help`. A CI job that wants to fail only on new findings has no baseline
file yet — that is on the roadmap and is the thing to build before turning this
on over a large existing calculus.

## Developing on it

```bash
python3 tests/run.py                       # every check against its witnesses
ETHOS=<ethos>/build/src/ethos \
  python3 tests/run.py --oracle            # ... and what ethos says about each
python3 tools/sweep.py <dir>...            # run over a corpus: crashes and counts
python3 tools/gen_checks_doc.py            # rewrite docs/checks.md from the registry
ETHOS=<ethos>/build/src/ethos \
  python3 tools/oracle_desugar.py          # the desugarer against ethos, case by case
```

`oracle_desugar.py` is the harness that keeps the desugarer honest. Ethos has no
command that prints a desugared term, so each case is compiled into a definition
whose `:type` cannot hold, and the term is read back out of the error message;
both sides are then un-curried and compared as terms. The battery lives in
`tests/desugar/cases.txt`, one line per case, and the context they are read in is
`tests/desugar/context.eo` — one declaration per policy the parser implements.
Adding a case is adding a line.

**Adding a check** is one function and one witness pair:

```python
@check("EO0099", "what it says in the list", page="""
Why it is a check, what ethos does with the same file, and how to fix it.
""")
def my_check(ctx: Context) -> Iterator[Diagnostic]:
    for prog in ctx.signature.programs:
        ...
        yield Diagnostic(code="EO0099", severity=Severity.WARNING, ...)
```

`ctx.signature` is the whole include closure: `decls`, `programs`, `rules`,
`defines`, `literals`, and the indexes over them. `anoieu/resolve.py` is how you
get from a name to what it means -- it follows `define` aliases and knows the
builtin signature -- and `anoieu/typing.py` answers what type a term has where
its head settles it, or `None`, which is the answer to respect.

Then write `tests/witnesses/EO0099-bad.eo` with a `; expect: EO0099` line, and a
`-good.eo` beside it where the distinction is interesting, and
`python3 tests/run.py` picks both up with no registration anywhere.
