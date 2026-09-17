# anoieu

A static analyzer and differential fuzzer for **Eunoia**, the signature (`.eo`)
and semantic configuration (`.eos`) languages used by
[ethos](https://github.com/cvc5/ethos) and its Eunoia compiler.

- **The analyzer** — `scripts/anoieu_analyzer` — reads signatures and semantics
  without running a proof. It finds structural errors, type inconsistencies,
  unreachable program cases, and disagreements between a signature and its
  semantics.
- **The fuzzer** — `scripts/anoieu_fuzzer` — generates and mutates inputs, runs
  checkers, and reduces crashes or disagreements to small reproducers.

Both take `--dry-run`, which resolves everything a run would touch and runs
nothing. Both are one command over a fuller interface that is still there.

There is also an optional repository-policy check for CI in Eunoia ecosystem
projects.

**A clean run means only that the checks found nothing.** The analysis is
partial, its type reasoning is shallow, and it does not establish soundness.
The fuzzer compares behavior; agreement between checkers is not a proof of
correctness.

## Run the analyzer

Python 3.10 or later; no Python dependencies. From a checkout:

```bash
scripts/anoieu_analyzer                 # every standard target, into the bug database
scripts/anoieu_analyzer --dry-run       # which signatures that means, concretely
scripts/anoieu_analyzer --preview       # find the bugs and ask koine to preview the append
```

That is the entry point for running anoieu over what it watches. It reads the
standard targets from `scripts/targets.json`, finds each project where
`scripts/repos.local` says it is on this machine, runs every check, and adds
whatever is new to [`docs/reports/bugs.json`](docs/reports/bugs.json) — the
database of every bug anoieu has found, appended to by
[koine](https://github.com/ajreynol/koine) and rendered as a table in
[`static-analysis.md`](docs/reports/static-analysis.md). `--dry-run` runs no
checks: it prints the signature files a run would read, which is what tells a
run that found nothing apart from a run that read nothing.

`prompts/anoieu_analyzer_agent` puts the same question to an assistant, against
the same targets, in the same output shape — so the two can be compared.

**To check one signature of your own**, which is what another project wants, the
analyzer is a command in its own right and needs none of the above:

```bash
python3 -m anoieu check path/to/signature.eo
python3 -m anoieu check path/to/signature.eo --format github
```

Or install with `pip install -e .` and use `anoieu check`.

The checks cover:

- syntax and declaration structure;
- attribute contracts, such as an associative operator's nil having the wrong type;
- shallow typing, including program cases with incompatible return types;
- cases that cannot be reached;
- consistency across a signature, its calculus semantics and its SMT semantics.

Ethos checks some properties only when a proof exercises them. Anoieu reads the
signature ahead of that use, so it can report errors in unexercised cases.

See [usage](docs/usage.md) for inputs, output formats, configuration, suppression
and baselines, and the [check catalogue](docs/checks.md) for each check's scope
and limitations.

## Run the fuzzer

Two names and a number: the checkers to compare, and how many cases to write.

```bash
scripts/anoieu_fuzzer                   # ethos against logos, 200 cases
scripts/anoieu_fuzzer ethos logos 2000  # the same, working harder
scripts/anoieu_fuzzer --dry-run         # which binaries, which signature, run nothing
```

The first name is the reference — the checker a disagreement's direction is
measured against, which is what makes accepting what it refuses the serious
result. Binaries are found from `$ETHOS`-style variables, from a build inside the
checkout, or on `PATH`, and `--dry-run` says which won. `anoieu_fuzzer --help`
explains what N buys, with the measured cost of a case.

Everything that face does not carry is still reachable underneath:

```bash
ETHOS=/path/to/ethos LOGOS=/path/to/logos \
  python3 -m anoieu_fuzz run --mode proof -n 2000
ETHOS=/path/to/ethos \
  python3 -m anoieu_fuzz run --mode signature
```

The fuzzer uses grammar-based generation and seed mutation. It detects crashes,
timeouts, malformed diagnostics and disagreements between checkers, then shrinks
and deduplicates the results. It is a baseline fuzzer, without coverage guidance
or a soundness oracle.

Findings use the same reporting workflow as the analyzer. See the
[fuzzer guide](docs/fuzzing.md) for setup, modes, oracles and adding a checker.
Committed [reproducers](tests/fuzz) show what it has found.

Promotion automatically records findings through koine in the same bug database
as the analyzer. `python3 -m anoieu_fuzz report` records the promoted corpus and
displays it; `--preview` calls koine's dry run. Koine is required, and a failed
append fails the command. See [recording through koine](docs/fuzzing.md#recording-through-koine).

## Findings and reports

The [report register](docs/reports/reports.md) records what anoieu is asking of
each project, the evidence, and the response. The
[open findings](docs/reports/open-findings.md) list current reports; the
[corpus report](docs/reports/corpus.md) identifies the source commits measured.

The [bug database](docs/reports/bugs.json) is the other half, and a newer one:
static findings and promoted fuzzer findings, recorded exclusively through
koine, with the date each was first and last ingested. Fuzzer records carry
recorded outcomes; recording does not replay them. Existing bug content is
preserved on append. The database carries no verdicts — a bug
somebody has ruled on is still in it — so the open findings remain the report,
and the database remains the record of what was found.

A reply is triage. A finding closes when the relevant artifact establishes what
happened. The [reporting workflow](docs/reports/reporting-workflow.md) explains
how to reproduce, answer and resolve findings, and how to run the analyzer in
another project's CI.

## Optional ecosystem CI check

Eunoia ecosystem repositories can run the repository-policy checker against
their tree:

```bash
python3 scripts/policy_check.py --root path/to/repository
```

It checks repository conventions, independently of the analyzer and fuzzer.
A repository with reason not to declare membership on its front page takes the
`associate` footing, recorded on its own `docs/maintenance.md` along with what
it holds itself to. It owes this ecosystem nothing; its tree is checked anyway,
against its own marker. It keeps a front page all the same, with a
maintenance note that has something under it, because nothing else about the
arrangement is advertised for a reader to find.
The [maintenance guide](docs/maintenance.md#the-policy-checker-interface)
describes the interface and how consumers pin it.

## Documentation and development

| Document | Contents |
| --- | --- |
| [Usage](docs/usage.md) | analyzer commands, options and configuration |
| [Fuzzing](docs/fuzzing.md) | running the fuzzer and interpreting its findings |
| [Checks](docs/checks.md) | every diagnostic and its limitations |
| [Design notes](docs/notes.md) | language behavior, implementation and open work |
| [Maintenance](docs/maintenance.md) | development commands and required checks |
| [Documentation index](docs/README.md) | reports, records and remaining documentation |

Run the local suite with `python3 tests/run.py`. Tests cover minimal witnesses,
CLI behavior and reporting; CI also checks the pinned corpus against committed
baselines. Oracle tests additionally require an ethos build.

Documentation can lag behind the code. Generated reports identify their inputs;
handwritten claims are only as current as their last review.

## The name

Read **Eu·noi·a** backwards: **a·noi·eu**, pronounced **"annoy you"**
(/əˈnɔɪ.juː/). Eunoia means beautiful thinking or goodwill; this tool aims that
goodwill at the error you would rather discover before running a proof.

## How this repository is maintained

This repository is part of the **Eunoia ecosystem** and follows its shared
[repository policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md).
This README is checked against that policy on every push, by the same command
any other repository would run.

**Written by AI agents, under light human supervision.** A human directs the
work, reads what is published and decides what is filed; nobody vets the
internal design, and nothing reaches another project's issue tracker without
review.

**The human maintainer is the authority here, and the agents are tools.** They
write most of the text and hold none of it: no decision, no role, no say. Where
this tree says a repository does something, a person did it.

**And a human runs every `git push` and every `git clone`.** No commit has
entered the public history of this repository except by a person executing it,
so a human intention stands behind every one — which is the fact anything
reading this history needs in order to interpret it, and it is stated here
because it will not stay true by accident. **If that changes, this paragraph
changes with it**, and the change is announced rather than discovered. [`docs/reports/reporting-policy.md`](docs/reports/reporting-policy.md) says what that does and does
not cover, and why the intended audience is experts.
