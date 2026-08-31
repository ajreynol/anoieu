# Using anoieu

What the tool takes, what it does with it, and what every option means. Written
against 0.2.0: the front end, the checks that need no type checker, a shallow
typing pass, and the triple — a signature read together with its calculus
semantics and the SMT semantics, each `.eos` file read rather than merely
accepted.

## Installing

Python 3.10 or later, no dependencies. From a checkout:

```bash
python3 -m anoieu <command>          # run in place
pip install -e .                     # or install, which gives you `anoieu`
```

Both spellings are the same program; the examples below use the first.

## The input

**Profiles.** A consumer does not always name one file: cvc5 checks an expert
proof by including `Cpc.eo` and *then* `expert/CpcExpert.eo`, in that order, into
one symbol table. Several files given on the command line are read that way —
one ordered profile, one signature — and a repository with more than one
configuration writes them down:

```json
{"profiles": [
  {"name": "safe",   "includes": ["cpc/Cpc.eo"]},
  {"name": "expert", "includes": ["cpc/Cpc.eo", "cpc/expert/CpcExpert.eo"]}]}
```

`--profile NAME` runs one of them. Findings carry the profile they were found
in, and a reachability finding is reported only where it holds in every profile
that read the file its subject stands in — so "nothing reaches this" is never a
claim about a world nobody runs.

**Entry points, and their include graphs.** You name one or more signature
files, and anoieu reads each, follows every `(include "...")` and
`(reference "...")` from there, and analyses what those closures declare. A file
read under two entry points is read once, and a finding reported twice is
reported once:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo
python3 -m anoieu check <cvc5>/proofs/eo/cpc/{Cpc.eo,expert/CpcExpert.eo}
python3 -m anoieu check          # the entry points a nearby anoieu.json names
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

**The other two legs.** `--semantics` names a calculus's semantics and
`--smt-semantics` the SMT-LIB semantics it is written against; `--embedding`
names the `.eo` file that declares what the deep embedding *is*
(`plugins/model_smt/model_smt.eo`). Each check over the triple runs only when it
was given the legs it needs and says nothing otherwise, so a run with one leg
answers what one leg can answer:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo \
  --semantics <logos>/install/defs/Cpc.eos \
  --smt-semantics <ethos>/tools/eoc/semantics/smt.eos \
  --embedding <ethos>/plugins/model_smt/model_smt.eo
```

## The commands

### `check` — the one you will use

```bash
python3 -m anoieu check FILE [options]
```

Reads the signature, runs every check that is on, and prints what it found.

| option | what it does |
| --- | --- |
| `--pedantic` | also run the checks that are off by default (see below) |
| `--config FILE` | use this `anoieu.json` instead of the discovered one |
| `--profile NAME` | analyse only this profile; repeatable |
| `--baseline FILE` | hold back the findings the baseline records |
| `--update-baseline` | rewrite the baseline from this run |
| `--no-suppress` | ignore `; anoieu: allow` comments in the signature |
| `--max-per-check N` | hold back a check reporting more than this (default 25) |
| `--max-findings N` | hold back a run reporting more than this (default 200) |
| `--no-limits` | report everything, however much there is |
| `--only CODE` | run only this check; repeatable, and an unknown code is an error rather than silence |
| `--format text\|json\|github\|sarif` | how to print; `text` is the default |
| `--deny-warnings` | exit non-zero on warnings too, not only on errors |
| `--no-color` | plain text, which is also the default when stdout is not a terminal |
| `--semantics FILE` | the calculus semantics (`.eos`) |
| `--smt-semantics FILE` | the SMT-LIB semantics it is written against |
| `--embedding FILE` | the `.eo` declaring the deep embedding, which `TRI0005` needs |

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

## Configuration, baselines and suppression

A repository writes down what it checks and what it has agreed to live with, so
that its CI job is one line. See [`reporting-policy.md`](reporting-policy.md#running-it-in-ci) for the whole arrangement; the
short version:

```json
{
  "entry_points": ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
  "baseline": "proofs/eo/anoieu-baseline.json",
  "disable": ["DOC0011"],
  "severity": {"EO0054": "hint"},
  "pedantic": false
}
```

`anoieu.json` is discovered by walking up from the first entry point, and every
field can be overridden on the command line, because someone debugging one
finding should not have to edit the repository's policy to do it.

A **baseline** records today's findings so a run can fail on tomorrow's.
`--update-baseline` writes it; a finding is remembered by its code, its file and
the text of the line it points at, so it survives edits elsewhere in the file. A
run says how many findings the baseline held, and how many entries the baseline
remembers that nothing reports any more.

A **suppression comment** is the other way to keep a finding, and the better one
where the decision is local:

```lisp
; anoieu: allow EO0054  matching exactly two children is what this rule is about
(($contains (or l xs) l) true)
```

It governs the line beneath it, or the line it trails; `allow-file` governs the
file. A run reports how many it silenced, so they stay countable.

## When a run reports too much

A check that reports two hundred findings has almost certainly broken rather
than found two hundred defects — it happened here, when a change to how a
directory is read merged 191 unrelated test signatures into one symbol table and
three checks produced 253 findings that were artefacts of the merge. Nothing
failed; the run simply printed them.

So a run bounds what it reports. A check over `--max-per-check` (25) is held
back: three of its findings are kept as evidence and the rest are replaced by an
`ANO0001` **error** saying how many were not printed and how to see them
(`--only CODE --no-limits`). A run over `--max-findings` (200) is truncated the
same way, with `ANO0002`. Both are errors, so a flood fails a CI job instead of
filling it with annotations, and nothing is ever dropped silently.

Raise them in `anoieu.json` where the volume is real:

```json
{"limits": {"per_check": 60, "total": 400}}
```

## In a pipeline

```bash
python3 -m anoieu check Cpc.eo --format github     # annotations in GitHub Actions
python3 -m anoieu check Cpc.eo --format json | jq '.[] | select(.severity=="error")'
```

The JSON is a flat list, one object per finding, with `code`, `severity`,
`message`, `file`, `line`, `column`, `endLine`, `endColumn`, `label`, `notes`
and `help`. `--format sarif` writes SARIF 2.1.0 for GitHub code scanning.

## Developing on it

```bash
python3 tests/run.py                       # every check against its witnesses
ETHOS=<ethos>/build/src/ethos \
  python3 tests/run.py --oracle            # ... and assert what ethos says about each
ETHOS=<ethos>/build/src/ethos \
  python3 tests/run.py --oracle --record   # ... and re-record it after a change
python3 tools/sweep.py <dir>...            # run over a corpus: crashes and counts
python3 tools/gen_checks_doc.py            # rewrite docs/checks.md from the registry
python3 tools/landing.py --check           # did what we closed on a promise land?
ETHOS=<ethos>/build/src/ethos \
  python3 tools/oracle_desugar.py          # the desugarer against ethos, case by case
```

`--oracle` compares what ethos says about each witness against
`tests/oracle.json`, which is written only by `--record` from a real run and
never by hand. It is what lets a claim like *ethos accepts this and should not*
be checked rather than asserted — and it earns its keep: it caught a "good"
witness that ethos was refusing, because the file used `Int` without declaring
it. Re-record when a witness changes, and read the diff: a verdict that moves
without a witness moving is ethos having changed under us.

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
