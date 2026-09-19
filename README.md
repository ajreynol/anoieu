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
standard targets from `anoieu_analyzer/reporting/config/targets.json`, finds each project where
`anoieu_analyzer/reporting/config/repos.local` says it is on this machine, runs every check, and adds
whatever is new to [`bug_db/bugs.json`](bug_db/bugs.json) — the
database of every bug anoieu has found, appended to by
[koine](https://github.com/ajreynol/koine) and rendered as a table in
[`static-analysis.md`](bug_db/static-analysis.md). `--dry-run` runs no
checks: it prints the signature files a run would read, which is what tells a
run that found nothing apart from a run that read nothing.

`prompts/anoieu_analyzer_agent` puts the same question to an assistant, against
the same targets, in the same output shape — so the two can be compared.

**To check one signature of your own**, which is what another project wants, the
analyzer is a command in its own right and needs none of the above:

```bash
python3 -m anoieu_analyzer check path/to/signature.eo
python3 -m anoieu_analyzer check path/to/signature.eo --format github
```

Or install with `pip install -e .` and use `anoieu check`.

The checks cover:

- syntax and declaration structure;
- attribute contracts, such as an associative operator's nil having the wrong type;
- shallow typing, including program cases with incompatible return types;
- cases that cannot be reached;
- consistency across a signature, its calculus semantics and its SMT semantics.

Ethos checks some properties only when a proof exercises them — read against
ethos on 2026-09-17. Anoieu reads the signature ahead of that use, so it can
report errors in unexercised cases.

See [usage](anoieu_analyzer/usage.md) for inputs, output formats, configuration, suppression
and baselines, and the [check catalogue](anoieu_analyzer/checks.md) for each check's scope
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
[fuzzer guide](anoieu_fuzz/fuzzing.md) for setup, modes, oracles and adding a checker.
Committed [reproducers](tests/fuzz) show what it has found.

Promotion automatically records findings through koine in the same bug database
as the analyzer. `python3 -m anoieu_fuzz report` records the promoted corpus and
displays it; `--preview` calls koine's dry run. Koine is required, and a failed
append fails the command. See [recording through koine](anoieu_fuzz/fuzzing.md#recording-through-koine).

## Findings and reports

**The shared artifact is [`bug_db/`](bug_db/README.md): one database for the
static analyzer and promoted fuzzer findings.** Refresh both with one command:

```bash
python3 scripts/update_bug_db.py --dry-run  # check the inputs and Koine setup
python3 scripts/update_bug_db.py            # analyse and record both sources
```

Use `--preview` to analyse without changing the database. The
[database README](bug_db/README.md) covers setup, adding new fuzzer findings,
and what the ingestion dates mean.
**[Browse all recorded bugs on GitHub](bug_db/bugs.md)** in the generated
table, which carries each finding's status beside its claim — the verdict
recorded against it, or `open` where nobody has ruled — with links to source
locations, reproducers and the change a finding closed on. Recording commands
refresh it alongside the JSON.

The [bug database](bug_db/bugs.json) is the persistent record, and the only
one: static findings and promoted fuzzer findings, recorded exclusively through
koine, with the date each was first and last ingested, and — on an entry
somebody has ruled on — the verdict, the reasoning, and the commit it closed
against. Fuzzer records carry recorded outcomes; recording does not replay them.
Existing content is preserved on append. The
[corpus report](bug_db/corpus.md) identifies the source commits measured.

**A finding closes on a commit, not on a dump**, and never on absence. What each
project has since done about what we found is
[`experience.md`](docs/experience.md); what a verdict may say, and the audit
that reads the outstanding ones back, is
[Closure](bug_db/README.md#closure).

What may be said about code we do not own — what separates a candidate published
under our own name from a finding carried to its owner, and what may be taken as
material at all — is the [reporting policy](bug_db/reporting-policy.md).

## Optional ecosystem CI check

Eunoia ecosystem repositories can run the repository-policy checker against
their tree:

```bash
python3 scripts/policy_check.py --policy-version 1 --root path/to/repository
```

The implementation, contract and focused tests live in
[`policy_check/`](policy_check/README.md); the script is the stable human launcher.

It checks repository conventions, independently of the analyzer and fuzzer.
A repository with reason not to declare membership on its front page takes the
`associate` footing, recorded on its own `docs/maintenance.md` along with what
it holds itself to. It owes this ecosystem nothing; its tree is checked anyway,
against its own marker. It keeps a front page all the same, with a
maintenance note that has something under it, because nothing else about the
arrangement is advertised for a reader to find.
**A repository picks one of two forms and says which.** It pins a checker
commit, or it names a contract and follows the latest implementation through
[a shared CI workflow](.github/workflows/policy.yml). Within version 1 the
requirements, their applicability and the blocking/advisory split stay fixed;
checker bug fixes continue to arrive, so a contract consumer's build can go red
with nothing committed — which means a violation already in the tree has started
being reported, never a new requirement arriving. A pin moves only when its
repository moves it. The [contract page](policy_check/README.md) is the authority
on what each form fixes; kanon's joining instructions carry both, read
2026-09-17.

## The documentation index

**Every document in this repository is named here, and this is the only index.**
A document lives with the thing it describes: the analyzer's documents are in
`anoieu_analyzer/`, the fuzzer's in `anoieu_fuzz/`, the checker's in
`policy_check/`, and everything about findings in `bug_db/`. What is left in
`docs/` is the four records that are the repository's rather than any tool's.

### Written

| document | its job |
| --- | --- |
| [`anoieu_analyzer/README.md`](anoieu_analyzer/README.md) | **the analyzer's entry point**: what it is, how it is run, and what is in its directory |
| [`anoieu_analyzer/usage.md`](anoieu_analyzer/usage.md) | **the analyzer's interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together |
| [`anoieu_analyzer/notes.md`](anoieu_analyzer/notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open |
| [`anoieu_fuzz/README.md`](anoieu_fuzz/README.md) | **the fuzzer's entry point**: what it asks, what it is deliberately not, and how it came to be shipped rather than researched |
| [`anoieu_fuzz/fuzzing.md`](anoieu_fuzz/fuzzing.md) | **the fuzzer's manual**: its oracles, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker |
| [`policy_check/README.md`](policy_check/README.md) | **the policy checker's contract**: versioned requirements and severities, the two adoption forms, focused tests, and the shared CI workflow |
| [`policy_check/maintenance.md`](policy_check/maintenance.md) | **how a check is added or changed**, and which shapes of check are the expensive kind |
| [`bug_db/README.md`](bug_db/README.md) | **the shared findings artifact**: setup, one-command updates from both producers, and what a closure may write onto an entry |
| [`bug_db/reporting-policy.md`](bug_db/reporting-policy.md) | **what may be said about code we do not own**: what separates a candidate published under our own name from a finding carried to its owner, what may be taken as material, and what tier each position is enforced at |
| [`docs/experience.md`](docs/experience.md) | **every interaction we have had with the projects we watch**: one entry per episode, oldest first — a change they merged on our evidence, an ask they rejected, or a correction they put to us |
| [`docs/maintenance.md`](docs/maintenance.md) | **the maintainer's entry point**: responsibilities, the command catalogue, the checks before handing off a change, and the open technical work |
| [`docs/discussion.md`](docs/discussion.md) | **correspondence with the other tools**: live questions, proposals, notices and replies. A defect with a path and a line number is not here; it is a finding |
| [`docs/history.md`](docs/history.md) | **how things came to be**, and the only page that may carry an account of it |

**Two things here are deliberately outside this index.**
`docs/letter-to-kanon.md`, because a letter from one office-holder to the next is
an account rather than documentation and the law that requires it says so. And
any child project under `tools/`, because a child this repository does not
advertise gets no row here and no link inward — it keeps its own index inside its
own directory, and listing `tools/` is how it is meant to be found.

### Generated

Written by a run, and the only documents a tool may edit.

| document | its job |
| --- | --- |
| [`anoieu_analyzer/checks.md`](anoieu_analyzer/checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |
| [`bug_db/corpus.md`](bug_db/corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`bug_db/bugs.json`](bug_db/bugs.json) | **the database, and the only record of a verdict** — static findings and promoted fuzzer findings, one JSON object each. Every recording command calls [koine](https://github.com/ajreynol/koine)'s `koine_append_db`, which adds entries and updates ingestion dates while preserving existing content. **Not reconstructible**: the verdicts and hand-written notes on it exist nowhere else |
| [`bug_db/bugs.md`](bug_db/bugs.md) | **the GitHub browsing view**, rendered from the JSON for both producers with each finding's status and evidence links; refreshed by recording commands and checked by CI |
| [`bug_db/static-analysis.md`](bug_db/static-analysis.md) | **the static subset rendered from the database**, with the verdict recorded against each row. *Rewritten whole, from the database* |
| [`bug_db/cpc-audit.html`](bug_db/cpc-audit.html) | **a rendered report for a reader who will not clone this tree.** It restates findings from the sources above and adds none |

> **The database is not like the others.** Everything else above is rewritten
> whole, so anything typed into one is lost on the next run. `bugs.json` is
> *additive*: koine adds entries and never removes or rewrites one, so every
> verdict, note and closure written onto an entry survives. The asymmetry is
> deliberate — a writer that could delete could quietly delete a regression.

## Development

Run the local suite with `python3 tests/run.py`. Tests cover minimal witnesses,
CLI behavior and reporting; CI also checks the pinned corpus against committed
baselines. Oracle tests additionally require an ethos build.
[`docs/maintenance.md`](docs/maintenance.md) is where the work starts, and it
carries the command catalogue and the checks to run before handing off a change.

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

**Human maintainers:** [the current list in policy.md](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#human-maintainers).

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
changes with it**, and the change is announced rather than discovered. The discussion of that
scope and the intended expert audience is in
[`anoieu_analyzer/notes.md`](anoieu_analyzer/notes.md).
