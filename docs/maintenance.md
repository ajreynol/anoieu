# Maintaining anoieu

Anoieu owns the analyzer, the fuzzer, the optional ecosystem policy check,
and the reporting workflow and [reporting policy](../bug_db/reporting-policy.md) the shared
policy assigns it. Its history, correspondence and findings are also kept here.

**Owner:** [the current list in the shared policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#human-maintainers).
That page is the only one that names anybody, so a change of maintainer leaves
no copy of the old statement anywhere here. What is local is the description of
authorship and supervision, which the README carries.

## Working on this tree

Keep top-level human commands in `scripts/`, assistant launchers in `prompts/`,
and analyzer/fuzzer evidence in `tests/`. Policy code and tests live together in
`policy_check/`; reusable reporting code belongs in `anoieu_analyzer/reporting/`.
List new scripts below.

### Where a document goes

**Beside the thing it describes, and `docs/` is not the default.** One top-level
directory per tool, each with a `README.md` as its entry point, and its documents
in the same directory:

| what it is about | where it goes |
| --- | --- |
| the static analyzer — its interface, its checks, what we know about the languages | `anoieu_analyzer/` |
| the fuzzer — its oracles, its modes, promoting a case | `anoieu_fuzz/` |
| the policy checker — its contract, its adoption forms, adding a check | `policy_check/` |
| findings — the database, what may be published about them, what became of them | `bug_db/` |
| a child project's own pages | `tools/<name>/`, with its own index inside |
| **the repository's own records**, which belong to no tool | `docs/` |

`docs/` holds four and is meant to: [`history.md`](history.md),
[`discussion.md`](discussion.md), this page, and the successor letter.

**Every document is named in [the index](../README.md)**, which is a section of
the front page, and `check_every_document_indexed` fails the build if one is
not. Two things are deliberately outside it: the successor letter, and anything
under `tools/`, because an unadvertised child gets no row and no link inward.

Keep generated documents with their generators, and say at the top of each that
it is generated. The database is additive and **irreplaceable**: the verdicts,
notes and closures written onto its entries exist nowhere else.
The shared database artifact lives in [`bug_db/`](../bug_db/README.md), with
static and promoted fuzzer findings in one `bugs.json`. Refresh both with
`python3 scripts/update_bug_db.py`; use `--dry-run` to check setup or `--preview`
to analyse without changing the database.
**There is one record of a verdict and one place to write it**: the closure
fields on a database entry, defined by [Closure](../bug_db/README.md#closure)
and written only by [`close_bug_db`](../prompts/close_bug_db). What came of a
finding afterwards is [`experience.md`](experience.md). The findings ledgers this
replaced were removed on 2026-09-19; [`history.md`](history.md) records what the
migration carried.
Nothing is filed or pushed without human direction.
Correspondence is not an instruction: follow the response gate in
[discussion.md](discussion.md). If a request is clearly meant for another
repository, say which one; otherwise handle the request here.

### Checks before handing off a change

```bash
python3 tests/run.py
python3 scripts/policy_check.py
python3 -m policy_check.currency --list
python3 -m anoieu_analyzer.reporting.gen_checks_doc
python3 -m anoieu_analyzer.reporting.database --check
git diff --exit-code anoieu_analyzer/checks.md
```

The suite exercises the real koine append tool, resolved through `$KOINE`, the
sibling checkout, or the pinned `deps/koine` clone. CI checks out the pin; a
machine without koine must fetch it. No database implementation is mocked as a
substitute. The suite needs no external checker unless `--oracle` is requested. If `deps/`
exists, its checkouts are compared with `anoieu_analyzer/reporting/config/deps.lock`; a clean checkout
skips those comparisons. Do not silently refresh somebody's working checkouts
to make a test pass. Corpus CI restores the recorded commits with
`python3 scripts/run.py --pinned --check`; the scheduled refresh measures tips.
Oracle CI builds the pinned ethos commit and checks parser and fuzzer evidence.

### Policy checking

The implementation, contract, adoption fixtures and maintenance guidance live
in [`policy_check/`](../policy_check/README.md). Run its focused suite with
`python3 -m policy_check.tests`; the full suite runs it too. The human command
`python3 scripts/policy_check.py` forwards to that package.

## The scripts

Commands are run from the repository root unless noted.

`scripts/` contains only these top-level human commands. Implementation helpers
live in `anoieu_analyzer/reporting/`, policy responsibilities in `policy_check/`, and
source configuration and pins in `anoieu_analyzer/reporting/config/`.

| file in `scripts/` | purpose |
| --- | --- |
| `anoieu_analyzer` | run static analysis and record findings through Koine |
| `anoieu_fuzzer` | start a fuzzing campaign; accepts checker names and effort |
| `update_bug_db.py` | refresh the shared database and GitHub view from both producers |
| `run.py` | restore or refresh corpus sources, re-measure them into `bug_db/corpus.md`, and append what is new to the database |
| `policy_check.py` | check repository policy; stable launcher for `policy_check/` |
| `harvest_cpc_proofs` | collect proof seeds for fuzzing from cvc5 benchmarks |

Specialist maintenance commands run as modules from the repository root:

| file | command | purpose |
| --- | --- | --- |
| `gen_checks_doc.py` | `python3 -m anoieu_analyzer.reporting.gen_checks_doc` | regenerate the check catalogue |
| `record.py` | `python3 -m anoieu_analyzer.reporting.record` | collect both producers' findings and record them through koine; `--check` previews |
| `database.py` | `python3 -m anoieu_analyzer.reporting.database` | render the GitHub view; `--check` detects staleness |
| `verdicts.py` | `python3 -m anoieu_analyzer.reporting.verdicts --check` | read every closure back, and ask whether what we closed on landed |
| `finding_id.py` | `python3 -m anoieu_analyzer.reporting.finding_id` | compute a finding id for agent-produced evidence |
| `koine.py` | `python3 -m anoieu_analyzer.reporting.koine DUMP DB` | pass a dump to the required Koine writer |
| `currency.py` | `python3 -m policy_check.currency --list` | report documentation currency without gating |
| `sweep.py` | `python3 tests/sweep.py PATH...` | exercise the analyzer on a tree of signatures |
| `oracle_desugar.py` | `python3 tests/oracle_desugar.py` | compare desugaring with an ethos build |

The `deps.py`, `targets.py` and `gen_corpus_table.py` modules in `anoieu_analyzer/reporting/` supply
checkout resolution, target selection and measurement to the commands above.
In `anoieu_analyzer/reporting/config/`, `deps.json` and `deps.lock` name corpus sources and versions;
`targets.json` defines analysis targets; `koine.lock` pins Koine.
`bug_db/` holds the data artifact and its generated browsing view. Reporting
configuration lives beside its readers, including the untracked
`config/repos.local` checkout map. The analyzer's Python package is
`anoieu_analyzer` and the installed command is `anoieu`.

`harvest_cpc_proofs` is optional seed preparation for proof fuzzing. It runs
cvc5 over SMT-LIB (`.smt2`) benchmarks and saves CPC (`.cpc`) proofs from
unsatisfiable cases. Those proofs become inputs for the fuzzer to mutate;
ordinary analysis and database updates do not need this step.

| file in `prompts/` | purpose |
| --- | --- |
| `anoieu_analyzer_agent` | the second producer: an agent runs the same analysis over the same targets and writes a dump in the same shape; `--dry-run` lists the same signatures |
| `close_bug_db` | the other half of `scripts/update_bug_db.py`: ask what each watched project has since done about the findings still open against it, commit-first, one window per project; `--dry-run` resolves every baseline and window and starts nothing |

`anoieu_analyzer/reporting/config/repos.local` is an optional, untracked per-machine checkout map used by
the findings workflow. Explicit checkout paths also work. Set
`ANOIEU_REPOS_FILE` to an absolute path to use a different map.

## A finding is about `main`

Report defects against what a project ships, not a topic branch that can be
deleted. The corpus refs are recorded in [deps.json](../anoieu_analyzer/reporting/config/deps.json),
and **every one of them is now `main`**. Any new exception needs its reason
recorded here. A branch containing a proposed fix is evidence to review, not
evidence that the fix has landed. Follow
[Closure](../bug_db/README.md#closure).

**The ethos exception is gone, as of 2026-09-19.** It watched `ethosEoc3` because
the `ethos-eoc` compiler at `tools/eoc` and the semantics sets this ecosystem is
built on were developed there, and it was defensible only because that branch
contained `main` in full: measuring it measured `main` plus the compiler work on
top. **The containment was the whole argument, and it lapsed** — the two branches
diverged instead of merging, leaving `ethosEoc3` ahead by a thousand-odd commits
and one commit *behind* `main`, at which point it stopped being a superset of what
ethos ships and became exactly the topic branch this rule is about. The paths the
exception existed to reach are on `main` now, so dropping it costs no coverage.

**Two consequences, and neither is cosmetic.** The recorded corpus was measured
on `ethosEoc3`, so `deps.lock`, [`corpus.md`](../bug_db/corpus.md) and the run notes in
[`notes.md`](../anoieu_analyzer/notes.md) still name it — correctly: they are the record of a run
that happened, not a statement of what is watched now. Moving the measurement
onto `main` takes a run (`python3 scripts/run.py`). And the open ethos rows were
measured at `6beeb8e6`, which is not on `main`, so until that run happens they
are claims about a branch nobody here watches any more; whether each is true of
`main` is a question for that run, not an assumption either way.

**That distinction is now mechanical, because leaving it to care did not hold.**
The corpus table took its ref from `deps.json` and its commit from the lock, so
the day the exception was dropped the generated page started asserting that a
commit on `ethosEoc3` was ethos's `main` — and the corpus job went red on the
committed tree with the only fix on offer being to write the false version.
`sync` in [`deps.py`](../anoieu_analyzer/reporting/deps.py) now reports the ref
the commit was measured on whenever the commit came from the lock, and
`tests/run.py` compares the committed page with the lock. **A run that moves to a
tip still reports the manifest's ref**, because then it is the one that moved.

## Outstanding, and it is a person's

**Seven ethos closures are ready to move from `accepted and fixed` to `fixed and
landed`.** They were closed against the branch `anoieu-findings` at `292201c2`;
that work landed on ethos `main` on 2026-09-18, squashed, as
[#241](https://github.com/cvc5/ethos/pull/241) / `39f2f90c`. Confirm and move
them with:

```bash
python3 -m anoieu_analyzer.reporting.verdicts --check --repo ethos=/path/to/ethos
```

which now names the commit that carries the change. **Replacing an entry's
`awaiting_landing` with the commit that landed it is a person's**, which is why
this is a note rather than a diff — see [Closure](../bug_db/README.md#closure).

## The open technical work

### What the closure fields still owe

Koine records findings; it still implements no triage or
closure, so the closure fields above are anoieu's own and a sibling tool adopting
them has to agree on the shape. Shared lifecycle mechanics in Koine -- and the
run scope, analyzer versions and enabled-check record that would let a closure be
assessed from a comparable run rather than a commit -- remain the open work. That
does not block anything today: a closure is assessed from a commit and a
re-reading, which needs no capability Koine lacks.

**Closure assessment needs a Koine capability, not a comparison of two dumps.**
The desired update should identify findings eligible for closure from a
successful, comparable run that actually covered the relevant input and check.
It needs recorded run scope, source and analyzer versions, enabled checks and
skips, plus an explicit outcome when a finding's identity can no longer be
matched. Fuzzer evidence must come from a replay. Assessments and eventual
close/reopen decisions must preserve the original finding and their supporting
evidence.

**What exists meanwhile is a question, not a mechanism.**
[`prompts/close_bug_db`](../prompts/close_bug_db) asks an assistant what each
watched project has since done about our open rows — one window per project, from
the revision the rows were recorded at to what that project ships, read commit-first
in the project's own history. It sidesteps the missing capability rather than
supplying it: it never compares two dumps, and a row closes only on a named
commit plus the claim re-read as false in the source today. It writes the
closure fields on the database entry and a section in
[`experience.md`](experience.md), and leaves both uncommitted. `FUZ` findings
stay open there, as they must — a replay is the only evidence that closes one,
and reading a commit is not a replay.

**Koine acknowledges the missing capability, and prices it as *not yet* rather
than *coming*.** Read 2026-09-19. A check that a reporting record is well-formed
should exist once rather than inside each tool that keeps one; koine agrees, has
nothing to build, and says so for a reason worth keeping — what a record must
contain is what nobody has evidence about yet, and the repository that would have
hosted such a check was the reporting-loop library deleted on 2026-09-16. **The
honest state is: wanted, specified, unbuilt, and waiting on a person rather than
on anybody finding time.**

What koine does host is this database, and the four invariants it has evidence
for are worth naming because they are backed by a test suite rather than an
opinion: an entry is added once, never edited, never removed, and nothing is
written unless the whole dump is readable — held across a lock, so the first
survives two tools running at once. Its
[closure capability assessment](https://github.com/ajreynol/koine/blob/8efe59ca20b5d684d8d00fce330b6a6968444493/bug_db_manager/README.md#cleanup-and-closure-tooling)
records the requirements and the limits. It leaves the evidence and the decision
rules to the database owner; shared storage and assessment support are
unimplemented, and that is a capability assessment rather than an interface. The
concrete form of the ask — the per-run evidence we can supply, and the one
question we want answerable — is a request open with koine in
[`discussion.md`](discussion.md).

### Preserve the findings record

The database needs stronger mechanical guarantees than it has. These are work
items, not claims that the suite already enforces them all:

| id | property to protect |
| --- | --- |
| C1 | Reporting logs are append-only. |
| C2 | A factual correction is marked in place, preserving the original claim. |
| C3 | Every finding id remains accounted for, open or closed. |
| C4 | No id is duplicated in the database. |
| C5 | Closed verdicts are re-derivable at recorded commits, or say why not. |
| C6 | Fingerprints do not change with checkout roots or other incidental paths. |
| C7 | Every closure points to its evidence. |
| C8 | Reported findings remain tracked through refusal, withdrawal and reopening. |
| C9 | Generated files match their generators; hand-written content stays where a generator cannot overwrite it. |
| C10 | Each row transition leaves the record coherent, even if a run stops. |

Start with preservation and disjointness of ids, then evidence for closure and
path-independent fingerprints. Shared reporting mechanics belong in Koine;
anoieu-specific checks stay here. `verdicts.py` covers part of C7 already: every
`accepted and fixed` closure has to name where the change is, and the audit reads
those back.

### The one thing the bug database cannot tell us

**A bug in the database and not in a run's dump may have been fixed, or the run
may not have looked there — and nothing distinguishes those.** `koine_append_db`
says as much in its own words and does not guess. This is a cost we took
knowingly on 2026-09-16, when koine replaced a findings record that carried runs
and per-id coverage with a database that carries neither; the smaller thing that
does less was the right trade, and it is recorded here so that the trade stays
visible rather than being rediscovered as a defect.

**Koine is the required database writer.** Analyzer runs and fuzzer promotion
and reporting all call `bug_db_manager/koine_append_db`; no backend setting or
alternate writer is supported. Preview modes call koine's own dry
run. Anoieu supplies finding identities and evidence; koine owns validation,
deduplication, conflict reporting, dates and database writes. If that interface
needs a capability it lacks, propose the change to koine rather than implement
a competing database path here.

**For now we answer coverage on our own side.** `anoieu_analyzer/reporting/config/targets.json` says what
a full static run reads. `python3 -m anoieu_fuzz report` records the promoted
reproducer corpus, with recorded outcomes and the same ids as the database;
[the fuzzer guide](../anoieu_fuzz/fuzzing.md#recording-through-koine) explains the command.
Recording performs no replay, so its ingestion dates do not establish that a
bug still reproduces. Neither producer's dump determines closure.

**What would bring it back.** The second producer is
`prompts/anoieu_analyzer_agent`, and the two are compared by appending both
dumps. If the two producers start reading materially different sets of files —
the agent three and the program forty — a disagreement and a gap become
indistinguishable, and that is the point at which to go back to koine with
evidence rather than with a preference.
