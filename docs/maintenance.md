# Maintaining anoieu

Anoieu owns the analyzer, the fuzzer, the optional ecosystem policy check,
and the reporting workflow. Its history, correspondence and findings are also
kept here.

**Owner:** `ajreynol` — Andrew Reynolds, University of Iowa and AWS.
This is anoieu's accountability record, not front-page attribution.

## Working on this tree

Keep top-level human commands in `scripts/`, assistant launchers in `prompts/`,
and analyzer/fuzzer evidence in `tests/`. Policy code and tests live together in
`policy_check/`; reusable reporting code belongs in `anoieu_analyzer/reporting/`.
List new documents in [the index](README.md) and new scripts below.
Keep generated reports under their generators. The database is additive and
**irreplaceable**: the verdicts, notes and closures written onto its entries
exist nowhere else.
The shared database artifact lives in [`bug_db/`](../bug_db/README.md), with
static and promoted fuzzer findings in one `bugs.json`. Refresh both with
`python3 scripts/update_bug_db.py`; use `--dry-run` to check setup or `--preview`
to analyse without changing the database.
**The deprecated reporting policy and workflow were removed on 2026-09-19**,
with both findings ledgers, their generator, the landing audit and the
`check_anoieu` / `process_anoieu` prompts. Every verdict they held was migrated
onto the database entries; what a verdict may say is
[Closure](../bug_db/README.md#closure), and what came of a finding is
[`experience.md`](experience.md).
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
git diff --exit-code docs/checks.md
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
| `run.py` | restore or refresh corpus sources and regenerate the legacy reports |
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
`bug_db/` holds the data artifact and its generated browsing view.
The former `doc_currency.py` command moved to `policy_check/currency.py` on
2026-09-18. Helpers now run as modules; the six human launchers above retain
their command paths. The analyzer's Python package is now `anoieu_analyzer`;
the installed `anoieu` command keeps its name. Reporting configuration lives
beside its readers, including the untracked `config/repos.local` checkout map.

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

**Two consequences, and neither is cosmetic.** The recorded corpus was measured on
`ethosEoc3`, so `deps.lock`, [`corpus.md`](corpus.md) and the run notes in
[`notes.md`](notes.md) still name it — correctly: they are the record of a run that
happened, not a statement of what is watched now, and they are not edited by hand.
Moving the measurement onto `main` takes a run (`python3 scripts/run.py`). And the
open ethos rows were measured at `6beeb8e6`, which is not on `main`, so until that
run happens they are claims about a branch nobody here watches any more; whether
each is true of `main` is a question for that run, not an assumption either way.

## The open technical work

### Replace the deprecated reporting policy

**Done, 2026-09-19.** The deprecated policy and workflow are **removed**, with
both findings ledgers, their generator, the landing audit, the `check_anoieu`
and `process_anoieu` prompts, and the postmortem log. There is now one record --
[`bug_db/bugs.json`](../bug_db/bugs.json) -- and one place a verdict may be
written: the closure fields on an entry, defined in
[Closure](../bug_db/README.md#closure) and written only by
[`close_bug_db`](../prompts/close_bug_db).

What the migration carried across, so nothing was lost:

- **every verdict**, all 43, with its prose. The seven-outcome vocabulary is now
  `closed_verdict`, enforced by
  [`verdicts.py`](../anoieu_analyzer/reporting/verdicts.py) and compared against
  `bug_db/README.md` by `tests/run.py`.
- **every hand-written note** on an open finding, as `notes`.
- **every outstanding landing**, as `awaiting_landing`, still audited by
  `python3 -m anoieu_analyzer.reporting.verdicts --check`.
- **22 findings the database did not carry**, minted with `migrated_from`
  naming the ledger they came from, because no koine run produced them.
- **the reasoning**, from `reports.md` and `postmortem.md`, into
  [`experience.md`](experience.md), where the salvaged entries are marked as
  having been worked through the old workflow.

**What is still owed.** Koine records findings; it still implements no triage or
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

**Koine acknowledges the missing capability (checked 2026-09-18).** Our
[`D9`](discussion.md#d9--we-are-going-to-stop-proving-our-report-by-re-running-our-tools)
describes record consistency, not automatic closure. Koine's `D13` reply in its
[discussion file](https://github.com/ajreynol/koine/blob/main/docs/discussion.md)
offers the bug database invariants and no shared reporting-record checker.
Koine now acknowledges these requirements in its
[closure capability assessment](https://github.com/ajreynol/koine/blob/8efe59ca20b5d684d8d00fce330b6a6968444493/bug_db_manager/README.md#cleanup-and-closure-tooling).
It leaves the evidence and decision rules to the database owner; shared storage
and assessment support remain unimplemented. This is a capability assessment,
not an implemented interface or reporting policy. The current updater records
observations and preserves the existing verdicts.

### Preserve the findings record

The ledger needs stronger mechanical guarantees through that migration.
These are work items, not
claims that the suite already enforces them all:

| id | property to protect |
| --- | --- |
| C1 | Reporting logs are append-only. |
| C2 | A factual correction is marked in place, preserving the original claim. |
| C3 | Every finding id remains accounted for in the open or closed ledger. |
| C4 | No id is duplicated within or across those ledgers. |
| C5 | Closed verdicts are re-derivable at recorded commits, or say why not. |
| C6 | Fingerprints do not change with checkout roots or other incidental paths. |
| C7 | Every closure points to its evidence. |
| C8 | Reported findings remain tracked through refusal, withdrawal and reopening. |
| C9 | Generated files match their generators; hand-maintained ledgers stay separate. |
| C10 | Each row transition leaves the record coherent, even if a run stops. |

Start with preservation and disjointness of ids, then evidence for closure and
path-independent fingerprints. Shared reporting mechanics belong in Koine;
anoieu-specific checks stay here.

### The one thing the bug database cannot tell us

**A bug in the database and not in a run's dump may have been fixed, or the run
may not have looked there — and nothing distinguishes those.** `koine_append_db`
says as much in its own words and does not guess. This is a cost we took
knowingly on 2026-09-16, when koine replaced a findings record that carried runs
and per-id coverage with a database that carries neither; the smaller thing that
does less was the right trade, and it is recorded here so that the trade stays
visible rather than being rediscovered as a defect.

**Koine is the required database writer.** Analyzer runs, fuzzer promotion and
reporting, and ledger generation all call `bug_db_manager/koine_append_db`; no backend
setting or alternate writer is supported. Preview modes call koine's own dry
run. Anoieu supplies finding identities and evidence; koine owns validation,
deduplication, conflict reporting, dates and database writes. If that interface
needs a capability it lacks, propose the change to koine rather than implement
a competing database path here.

**For now we answer coverage on our own side.** `anoieu_analyzer/reporting/config/targets.json` says what
a full static run reads. `python3 -m anoieu_fuzz report` records the promoted
reproducer corpus, with recorded outcomes and the same ids as the ledger;
[the fuzzer guide](fuzzing.md#recording-through-koine) explains the command.
Recording performs no replay, so its ingestion dates do not establish that a
bug still reproduces. Neither producer's dump determines closure.

**What would bring it back.** The second producer is
`prompts/anoieu_analyzer_agent`, and the two are compared by appending both
dumps. If the two producers start reading materially different sets of files —
the agent three and the program forty — a disagreement and a gap become
indistinguishable, and that is the point at which to go back to koine with
evidence rather than with a preference.
