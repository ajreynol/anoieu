# Fuzzing the checkers

**The anoieu fuzzer** writes Eunoia nobody would write, hands it to a proof
checker, and watches for the answer a checker should never give. It is the
other half of this repository's question: anoieu reads a signature and asks
whether it says something coherent; the fuzzer asks whether the programs that
*read* signatures behave when one is not.

```bash
python3 -m anoieu_fuzz run --mode proof        # ethos against a second checker, on a fixed signature
python3 -m anoieu_fuzz run --mode signature    # arbitrary signatures, at ethos alone
```

> **This is a baseline, deliberately.** Grammar-directed generation, mutation of
> a seed corpus, five verdict-level oracles, and no instrumentation anywhere. It
> is not coverage-guided, it does not build derivations that ought to be
> accepted, and it has no soundness oracle. Those belong to a research-quality
> successor, which is one of the
> [future projects](why-eunoia.md#six-projects-that-do-not-exist-yet-and-change-the-picture)
> in `why-eunoia.md` and does not exist.
>
> The floor is worth having on its own terms. In its first few thousand cases it
> found a crash in ethos, three proofs ethos and logos answer differently, and an
> ethos error path that carries no location — and a floor is what makes
> "research-quality" a measurable claim about a successor rather than an
> adjective.

## What it is, and what it is not

It is **semantics-free by construction.** It does not know what a proof means,
whether a rule is sound, or what CPC is for. Everything it reports is a fact
about two *runs*:

| kind | what happened | what it means |
| --- | --- | --- |
| **disagreement, the serious direction** | a checker **accepted** what the reference **refused** | the one to look at first. The checker took something outside the reference's definition of the language — and for a *verified* checker that means its theorem is about a term its parser invented rather than about the proof somebody wrote. Reported as an **error** |
| **disagreement, the other direction** | a checker **refused** what the reference **accepted** | a completeness gap. It costs its users a proof they cannot check and guarantees nothing false, so it is reported as a **warning** — often a documentation defect, where a checker has a deliberately narrower input format and has not said so |
| **crash** | a checker went down with nothing to say — a signal and an empty stream, an assertion, an uncaught exception | a bug in the checker |
| **unexplained** | a checker printed something and then failed anyway, outside the diagnostic convention it uses everywhere else | a bug in what the checker *says*: every tool downstream that reads its output misses this one |
| **timeout** | a checker never answered | suspect rather than certain — the generator can write a genuinely expensive file, and the finding says so |

None of the four needs a semantics, which is the point: the oracle is
comparison, and comparison is free.

It is **not** a soundness checker. It will not tell you a rule is invalid, and a
proof it generates proves nothing. It is not coverage-guided; there is no
instrumentation, no corpus feedback loop and no attempt at one. And a run that
finds nothing means the cases it wrote did not provoke anything —

> **A quiet run is not a clean bill of health.** The same caution
> [`philosophy.md`](philosophy.md) states for the analyzer holds here and holds
> harder: a fuzzer's silence is a fact about the inputs it happened to write.
> We publish reproducers and never assurances.

## The two modes

### `--mode proof` — a fixed signature, two checkers

Cases are proofs written against a signature the checkers already agree on
(CPC, by default). The file declares its own constants and then `assume`s and
`step`s. Both checkers read the same file; a disagreement is a finding.

```bash
ETHOS=<ethos>/build/src/ethos LOGOS=<logos>/.lake/build/bin/logos \
  python3 -m anoieu_fuzz run --mode proof -n 2000 \
    --signature <cvc5>/proofs/eo/cpc/Cpc.eo \
    --seed-corpus <logos>/test/regress/sexp
```

The vocabulary — which operators exist, what sorts they take, which rules take
how many premises — is read out of the signature by anoieu's own loader
(`anoieu_fuzz/vocab.py`). That is the only place the fuzzer touches the analyzer,
and it touches the front end rather than the checks. Types are used as
*shapes*, to pick an argument that is at least plausible; anything a shape does
not settle becomes a wildcard that matches everything. `--wild` says how often
to ignore even that.

> **Ethos is the reference, and which checker that is decides a disagreement's
> severity.** `"reference": "ethos"` in the configuration, `--reference` on the
> command line. Ethos holds the role because it is the implementation that
> defines, operationally, which files are Eunoia — not because it is more likely
> to be right, and `FUZ0001`'s page says what to do when it is the one at fault.
> A disagreement the reference did not take part in is reported as the serious
> direction, because assuming the mild reading of something nobody attributed is
> the wrong way to be wrong.

> **Ethos is run with `--require-proof-of-false`, and this is not optional.**
> Ethos by default does not care *what* a proof proves: it prints `correct` for
> any file whose steps check. Logos's `correct` means the assumptions are
> unsatisfiable — a refutation, or nothing. Compared as they stand the two
> disagree about almost every file and the fuzzer reports one fact forever. The
> flag is what makes the two words mean the same thing, so it is in the default
> configuration rather than behind an option.

### `--mode signature` — arbitrary Eunoia, one checker

Cases are signatures: `declare-const` with attributes that cannot hold,
`declare-rule`, `program`, `declare-datatype`, literal categories declared
twice. There is no second checker, so the oracle is the other three kinds —
crash, unexplained, timeout.

```bash
ETHOS=<ethos>/build/src/ethos \
  python3 -m anoieu_fuzz run --mode signature -n 5000 \
    --seed-corpus <ethos>/tests --jobs 6
```

`--metamorphic` adds the one differential question a *single* checker can be
asked: the same file, laid out differently — whitespace and comments, nothing
else — must get the same answer. The rewrite is deliberately timid, and
[`anoieu_fuzz/gen.py`](../anoieu_fuzz/gen.py) says exactly what it will not touch.

## Where cases come from

Two sources, and the run mixes them.

**Generated**, from the grammar in the manual's [full syntax
section](https://github.com/cvc5/ethos/blob/main/user_manual.md#full-syntax),
using the vocabulary above. This reaches the parser and the first layer past it.

**Mutated**, from a seed corpus of real files: drop a command, duplicate one,
swap two, splice a command out of another file, rename a symbol to another
symbol from the pool, truncate a term, insert a parenthesis, replace an atom
with a literal. This is what reaches everything *past* the parser, because it
starts from a file that already checks.

`--seed-corpus` takes a file or a directory, repeatably. **Every seed is checked
as it stands first**, before anything is generated or damaged — it is the
cheapest finding there is, and the first real disagreement this fuzzer reported
came from exactly there: a regression test of the checker it was about.

A seed's relative `include` and `reference` paths are rewritten to absolute
ones as it is read, because a case is run from a temporary file and would
otherwise be asking about a file that is not where it was.

## What comes out

Every finding is **shrunk** and then **bucketed**.

Shrinking is delta debugging over the command list, then three moves inside
each surviving command: drop a parenthesised span, replace one with the first
thing inside it, drop an atom. "Still the same finding" means the same bucket
rather than the same message, because dropping a command moves every line
number after it. In practice this is the difference between a reproducer
somebody reads and one somebody has to reduce by hand first:

```text
; 6 command(s) -> 1, 32 run(s): ethos crash: terminate called after throwing an
; instance of 'std::length_error'
(declare-const > (->))
```

Bucketing is what stops a thousand cases hitting one defect from becoming a
thousand directories. Two findings are the same finding when their kind, the
checkers involved and their *portable* detail agree — the diagnostic with paths,
line numbers and quoted symbols stripped out, since those vary between two
instances of one bug and the sentence around them does not.

```text
fuzz-findings/
  findings.jsonl                       one line per finding, appended
  crash-ethos-terminate-called-.../
    case.eo                            the shrunk reproducer, with its seed in a comment
    finding.json                       what each checker said, and how long it took
```

The directory is **append-only**, and across processes rather than only within
one: a bucket that already has a case on disk keeps the one it has, so
re-running over a wider seed range never overwrites a small reproducer somebody
already read, and a second run in a different mode never drops a `.cpc` beside
an `.eo` that the record no longer describes. `run` exits 1 when a bucket is
new, so a nightly job is one line.

## The other commands

```bash
python3 -m anoieu_fuzz checkers                  # what is configured, and what is on this machine
python3 -m anoieu_fuzz one --seed 7              # print one case; run nothing
python3 -m anoieu_fuzz replay case.cpc           # what each checker says about a file
python3 -m anoieu_fuzz shrink case.cpc           # cut a case down to what still provokes it
python3 -m anoieu_fuzz promote fuzz-findings/X   # keep one: move it into tests/fuzz/
python3 -m anoieu_fuzz report                    # every promoted finding, as diagnostics
python3 -m anoieu_fuzz verify                    # do they still do what the record says
python3 -m anoieu_fuzz explain FUZ0002           # what a code means
python3 -m anoieu_fuzz list-codes                # the four of them
```

`replay` is how a reproducer is confirmed on another machine, and `shrink` is
the same reduction applied to a file somebody else wrote. The last five are the
reporting half, and are what the next section is about.

`run` also takes `--format json|github|sarif`, which prints what it found as
diagnostics in the shapes `anoieu check` prints — the renderers are the same
ones, so a fuzzer finding lands in a GitHub annotation or a SARIF report looking
like what it is: a finding from this project, told apart by its code and by
nothing else it has to remember to do.

## Adding a checker

A checker in this ecosystem has a very small interface: hand it one file, read
one word. So a third one is a few lines of JSON rather than a plugin.

```json
{
  "checkers": {
    "ethos": {
      "env": "ETHOS",
      "modes": {
        "proof": ["ethos", "--include={signature}", "--require-proof-of-false", "{file}"],
        "signature": ["ethos", "{file}"]
      }
    },
    "logos": {"env": "LOGOS", "modes": {"proof": ["logos", "{file}"]}},
    "mine":  {"env": "MINE",  "modes": {"proof": ["/path/to/mine", "--check", "{file}"]}}
  },
  "signature": "/path/to/Cpc.eo",
  "reference": "ethos"
}
```

`{file}` is the case and `{signature}` the fixed signature; an argument naming
`{signature}` is dropped when no signature was given, because a case generated
without one carries its own declarations. `env` names an environment variable
that overrides the binary, which is the convention the rest of this repository
already uses (`ETHOS=`). A mode a checker has no entry for is a mode it sits
out, so a checker that only reads proofs simply says so.

**A file that names `checkers` replaces the default set rather than adding to
it.** Merging reads well until the day a run quietly also asks the two default
binaries about every case and reports a disagreement between one of them and
the checker somebody was testing on its own. `anoieu-fuzz checkers` prints the
defaults, so re-stating one is a copy.

What a checker has to do to be usable: print its verdict as the last line of
stdout (`correct`, `incomplete`, `incorrect`), and explain any refusal on a line
beginning `Error`. Anything else is read as a crash — which is the intended
reading, since a checker that fails without saying so is exactly what this is
looking for.

## From a candidate to a finding

A run writes what it found to `fuzz-findings/`, which is **not checked in**.
Nothing there is a finding in this project's sense yet: it has not been read, it
may be an artefact of this harness, and the binary it was found against may be
somebody's working tree. The first thing a run here ever reported was an
artefact — a mutated `include` pointing at a file that had never existed.

**Promotion is the step that makes it one**, and it is a command a person types:

```bash
python3 -m anoieu_fuzz replay  fuzz-findings/<bucket>/case.eo    # read it, confirm it
python3 -m anoieu_fuzz promote fuzz-findings/<bucket> --owner ethos --note "..."
python3 tools/gen_open_findings.py                               # give it a row
```

`promote` copies the reproducer into `tests/fuzz/`, where it is committed
evidence, beside `tests/witnesses/` which is the same idea for the checks. From
there it is a finding like any other: a code, an owner, a fingerprint, a row in
[`open-findings.md`](open-findings.md), and it leaves the open table only when
somebody rules on it.

### The codes

`EO`, `DOC` and `TRI` are what anoieu *read*. **`FUZ` is what the fuzzer
provoked**, which is the marker that says where a row came from.

| code | severity | what it says |
| --- | --- | --- |
| `FUZ0001` | error | a checker accepted what the reference refused |
| `FUZ0002` | error | a checker died with nothing to say |
| `FUZ0003` | warning | a checker failed outside its own diagnostic convention |
| `FUZ0004` | warning | a checker did not answer |
| `FUZ0005` | warning | a checker refused what the reference accepted |

`python3 -m anoieu_fuzz explain FUZ0002` is the page behind one, written beside
the code in [`../anoieu_fuzz/codes.py`](../anoieu_fuzz/codes.py) so the two
cannot drift. `list-codes` is the inventory.

### Where a finding is evidenced, and why it is different

A check's finding is re-derived by running the check: the evidence is the code
in this repository, and CI re-derives every one on every push. A fuzzer's
cannot be, because re-deriving it means running somebody else's binary, which
the job that generates the report does not have.

So the evidence is the committed reproducer plus the verdicts recorded beside
it — the same arrangement, for the same reason, as
[`../tests/oracle.json`](../tests/oracle.json): written by a real run, never by
hand, and checkable by anyone who has the binary.

```bash
python3 -m anoieu_fuzz report                    # every promoted finding, as diagnostics
python3 -m anoieu_fuzz report --format sarif     # ... and in the shapes anoieu prints
python3 -m anoieu_fuzz verify                    # re-run every one against the checkers here
```

`verify` is the re-measuring step. It replays each committed reproducer and
compares what each checker says now against what was recorded when it was
promoted; a checker that is not on the machine is skipped and said to be
skipped, and a run that compared nothing says so rather than passing quietly.
CI runs it in the job that builds ethos, and a verdict that has moved fails
that job — for the same reason the desugaring battery does. A finding that
stops reproducing is either fixed upstream or a checker having changed under
us, and both are things somebody should look at rather than let a row go stale.

The obligations that follow — confirm against a pinned build before filing, and
never let the tool assign an owner to a disagreement — are in
[`reporting-policy.md`](reporting-policy.md#a-finding-from-the-fuzzer).

## What the first runs turned up

Six findings are promoted, and they are in the ledger rather than here:
[`open-findings.md`](open-findings.md) has the rows, and
[`reports.md`](reports.md#the-register-what-anoieu-is-asking-and-of-whom) has
what is being asked of whom — `ethos-8` and `ethos-9`, `logos-4` and `logos-5`.
In short, from the first few thousand cases:

| kind | reproducer | what happens |
| --- | --- | --- |
| `FUZ0002` | `(declare-const f (->))` | ethos dies with an uncaught `std::length_error` — "cannot create `std::vector` larger than `max_size()`". A nullary arrow type |
| `FUZ0003` | `(declare-consts <numeral> Int)` then `… Bool` | aborts with an internal message carrying no `Error:`, no file and no line. Two more paths do the same: `assume-push` at the top level of a signature, and an `include` of a file that is not there |
| `FUZ0001` | `logos/test/regress/sexp/test-define.cpc`, **unmutated** | it uses `declare-fun`, an SMT-LIB command ethos accepts only in a reference file. Ethos refuses the file; logos checks it and says `correct` |
| `FUZ0001` | `(( extract 1 0) a)` — the indexed operator without its `_` | logos reads it as the indexed operator and accepts the proof; ethos type checks and refuses |
| `FUZ0005` | an `(assume …)` after the first `step` | ethos allows it; logos refuses to parse the file. The mild direction: logos refuses, so nothing unsound follows from it |

Not promoted, and worth saying so: a `(step #b1 …)` taking a binary literal
where a symbol belongs, a `(step … (=) :rule evaluate …)` whose stated
conclusion ethos refuses, and an `(include)` with no argument — each ethos
refuses and logos accepts, and all three are the same fact about logos ignoring
`include` or reading a term more loosely. One reproducer per *cause* is what the
ledger is for; one per bucket would be filing the same thing three times.

> **None of it is confirmed against the commits `tools/deps.lock` records.** It
> was produced against the binaries on the machine the fuzzer was written on —
> ethos 0.2.3 from a local build, logos from a local `lake build`. Re-run each
> reproducer against a pinned build before it is carried anywhere; that is what
> [`reporting-policy.md`](reporting-policy.md#a-finding-from-the-fuzzer)
> requires, and a fuzzer's output has no special standing.

## Running it in CI

Not on push. A fuzzer that fails a build finds a new bug and turns somebody's
unrelated pull request red, which is the one thing
[`philosophy.md`](philosophy.md) is most careful about. The `oracle` job already
builds ethos and caches it by commit, so the fuzzing steps hang off that job on
a schedule, upload what they find as an artifact, and warn rather than fail.

## The design, and what it does not do

Everything here is a decision to stay at the floor, so this section doubles as
the honest list of what a research-quality successor would have to add — the one
sketched among the
[future projects](why-eunoia.md#six-projects-that-do-not-exist-yet-and-change-the-picture)
in `why-eunoia.md`, which does not exist.

**No coverage guidance.** It would help, and it costs an instrumented build of
each checker, a corpus feedback loop and a scheduler. Generation plus mutation
against a real seed corpus found a crash and three divergences in the first few
thousand cases; that is the cheap end of the curve, and the expensive end can
wait until the cheap end stops paying.

**No generator that builds a derivation from the calculus.** Random Eunoia
bounces off the front end: in a differential run, roughly nineteen cases in
twenty are refused by both checkers before a rule is ever reached. Assembling a
proof step by step out of premises it has already produced is what would make
*refused* the finding rather than the default, and it is the single change that
would most raise what this reaches. It is also most of a proof-search engine.

**No soundness oracle.** "No checker may accept a refutation of a satisfiable
assumption set" needs a solver in the loop and is a claim about one checker
rather than about two. It is the class of finding the ecosystem most wants and
this tool cannot make.

**No type-correct generation.** A generator that produced only well-typed terms
would only ever ask a checker the questions it was built to answer. Types are
used to make an argument *plausible*, and `--wild` says how often to ignore even
that.

**Shrinking is syntactic**, over commands and then over parenthesised spans and
atoms. It will not, say, replace a rule with a simpler rule.

**A disagreement is not attributed.** The fuzzer says the two answers differ; it
never says which checker is wrong, because deciding that needs exactly the
semantics it does without.

**Cases are files, not streams.** Ethos also accepts a proof on stdin, and that
path is untested here.

## The code

| file | its job |
| --- | --- |
| [`anoieu_fuzz/vocab.py`](../anoieu_fuzz/vocab.py) | what a fixed signature offers the generator: operators, their argument shapes, rules and their arities, literal categories. The only place the fuzzer touches anoieu |
| [`anoieu_fuzz/gen.py`](../anoieu_fuzz/gen.py) | writing a case, damaging a case, splitting a file back into commands, and the one metamorphic rewrite |
| [`anoieu_fuzz/checkers.py`](../anoieu_fuzz/checkers.py) | running a checker and reducing what it said to `accept` / `reject` / `abnormal` |
| [`anoieu_fuzz/triage.py`](../anoieu_fuzz/triage.py) | the oracle, the buckets, the shrinker and the corpus |
| [`anoieu_fuzz/cli.py`](../anoieu_fuzz/cli.py) | `run`, `one`, `replay`, `shrink`, `checkers` |
| [`tests/fuzz_cases.py`](../tests/fuzz_cases.py) | the harness, against checkers written in the suite so that neither ethos nor logos has to be on the machine |
