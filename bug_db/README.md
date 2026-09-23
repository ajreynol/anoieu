# Anoieu's bug database

[`bugs.json`](bugs.json) is the persistent artifact shared by the **static
analyzer and the fuzzer**. It contains every recorded finding, including ones
that have since been resolved. Koine's `bug_db_manager/koine_append_db` is its only
writer; Koine provides the tooling, and this directory holds anoieu's data.

**[Browse open bugs](bugs.md)** directly on GitHub. The generated page
shows open findings from both producers, their descriptions, ingestion dates, and
links to source locations or committed reproducers. Open the **Preview** tab if
GitHub shows the Markdown source. No server or local setup is needed to read it.
Both this page and [static-analysis.md](static-analysis.md) exclude every entry
carrying a `closed_verdict`, including declined and intentional (won't fix)
findings. Closed entries remain in `bugs.json`, preserving their evidence and
preventing a later import from making them appear open again.

The database moved here from `docs/reports/bugs.json` on 2026-09-18, preserving
every record and date.

## Update it

From the repository root, with Python 3.10 or later:

```bash
python3 scripts/update_bug_db.py --dry-run  # check setup and list inputs; write nothing
python3 scripts/update_bug_db.py --preview  # run analysis; preview the database changes
python3 scripts/update_bug_db.py            # record both sources in bug_db/bugs.json
```

**The last command is the routine update.** It runs the static checks over all
configured targets, combines their findings with the promoted fuzzer corpus in
[`tests/fuzz/`](../tests/fuzz), and gives one combined dump to Koine. It also
refreshes the [GitHub view](bugs.md) and the
[static table](static-analysis.md). It succeeds
only if recording succeeds. Repeating it adds no duplicate findings.

`--preview` writes the disposable dump `scratch/new-report-bugs.json` and asks
Koine for a dry run; it leaves the database and reports unchanged. The update
uses the source checkouts already on disk. It does not fetch newer targets,
start a fuzzing campaign, or replay the recorded fuzzer cases.

## Setup

- **Static inputs:** [`anoieu_analyzer/reporting/config/targets.json`](../anoieu_analyzer/reporting/config/targets.json) names the
  targets. Set their checkout paths in the gitignored `anoieu_analyzer/reporting/config/repos.local`
  (one `project /path/to/checkout` per line), or use the managed `deps/` clones.
  `python3 scripts/run.py --pinned` prepares those clones at the recorded
  commits and re-measures them into [`corpus.md`](corpus.md). The
  update command refuses missing configured input paths instead of silently
  recording a partial refresh.
- **Koine:** [`anoieu_analyzer/reporting/koine.py`](../anoieu_analyzer/reporting/koine.py) finds `$KOINE`, then
  `../koine`, then `deps/koine`. A normal update or preview can clone the commit
  in [`anoieu_analyzer/reporting/config/koine.lock`](../anoieu_analyzer/reporting/config/koine.lock) into `deps/koine` if needed;
  `--dry-run` only checks and reports missing setup. No package installation is
  needed. An existing checkout is used as-is, and the update prints its version.
- **Fuzzer evidence:** reporting the promoted corpus needs no checker binaries.
  Discovering new findings requires the checkers you want to compare, as
  described in the [fuzzer guide](../anoieu_fuzz/fuzzing.md).

## Add new fuzzer findings

```bash
scripts/anoieu_fuzzer --dry-run                # check binaries and signature
scripts/anoieu_fuzzer ethos logos 2000          # generate and reduce candidates
python3 -m anoieu_fuzz replay fuzz-findings/<bucket>/case.cpc
python3 -m anoieu_fuzz promote fuzz-findings/<bucket> --owner ethos --note "..."
```

Use the actual reproducer filename, and choose the owner and note after reviewing
the result. Promotion keeps the reproducer and immediately records it in this
same database. Raw candidates remain in `fuzz-findings/` until reviewed and
promoted. A later database update includes all promoted cases again.

For just one producer, `scripts/anoieu_analyzer` updates the static findings and
`python3 -m anoieu_fuzz report` records the promoted fuzzer corpus. Both accept
`--preview` and write to this same database.

The updater, the analyzer, and fuzzer reporting and promotion each refresh
`bugs.md` and `static-analysis.md` after a successful append. To render existing data without
running either producer, use `python3 -m anoieu_analyzer.reporting.database`. Its
`--check` mode detects either stale or missing report, and CI runs that check.
A direct append with the low-level Koine command, or any closure edit, needs
this render step. Commit both reports alongside the JSON.

## Read the artifact

The JSON has a top-level `bugs` array. Each entry carries a stable `id`, a
description, ownership and evidence fields, and ingestion dates.

| Producer | `tool` | Evidence |
| --- | --- | --- |
| Static analyzer | `anoieu` | diagnostic code, source location and measured commit |
| Fuzzer | `anoieu-fuzz` | committed reproducer, finding kind and recorded checker outcomes |

Koine preserves existing bug content, updates `last_seen` when an entry is
ingested again, and reports conflicting content without replacing the original.
For example, a newer source commit produces a `found_at` conflict: Koine keeps
the original measured commit and still records the new ingestion date.
`first_seen` and `last_seen` are ingestion dates; especially for fuzzer records,
they do not mean a fresh reproduction. Commit `bugs.json` with the supporting
reproducers and any regenerated static table. Runtime `*.lock` files are ignored.

## Closure

**A finding closes on a commit, not on a dump.** A finding absent from a later
export may have gone because an input was skipped, a check changed, or its
fingerprint moved; the updater never closes anything on absence, and a `FUZ`
finding closes only on replay evidence.

[`prompts/close_bug_db`](../prompts/close_bug_db) asks what each watched project
has since done about the findings still open against it -- one window per
project, from the revision those findings were recorded at to what the project
ships today, read commit-first in that project's own history:

```bash
prompts/close_bug_db --dry-run          # every baseline and window, resolved; nothing started
prompts/close_bug_db cvc5 ethos         # only these projects
prompts/close_bug_db --use-local ethos=/src/ethos
```

The launcher uses Koine's `koine_close_db` and `koine_window`, selected from
`$KOINE`, `../koine` or `deps/koine`. That checkout must contain the programs at
our [Koine pin](../anoieu_analyzer/reporting/config/koine.lock); this command
never fetches. Anoieu supplies its baselines and evidence rules to Koine. The
prompt includes `koine_check_db bug_db/bugs.json --also awaiting_landing`, which
checks that the diff against the committed database only adds closure fields to
previously open records. Invoke that checkout's program from Anoieu's root after
an assessment;
existing uncommitted ingestion or claim edits will also appear in that diff.

It closes a finding on exactly two conditions: **a named commit** somebody can
fetch, and **the claim re-read as false in the source today**. It writes two
authored records -- the closure fields on the entry here, and a section
in [`experience.md`](../docs/experience.md) saying what the change meant. Then
regenerate and check both reports, and the running tally in `experience.md`, so the closed rows disappear and the counts move:

```bash
python3 -m anoieu_analyzer.reporting.database
python3 -m anoieu_analyzer.reporting.database --check
```

For a won't fix decision, use the existing `declined` or `intentional` verdict
as appropriate. All closure verdicts remove the finding from both open reports;
`accepted and fixed` still owes a landing, tracked by the separate audit below.

### What a closure puts on an entry

| field | what it holds |
| --- | --- |
| `closed_verdict` | one of the seven words below, and nothing else |
| `closed_why` | why the claim no longer holds, and what was re-read to establish it |
| `closed_on` | the date the closure was recorded |
| `closed_commit`, `closed_pr` | the change it closed on, where that applies. One change may close several findings |
| `closed_by` | on a finding owned by two projects (`a+b`), the one whose change or ruling closed it; the running tally in `experience.md` counts it against that project alone |
| `awaiting_landing` | `{project, branch, commit}` -- required by `accepted and fixed`, forbidden on anything else |

**A verdict is one of seven words, and the list is the whole of it.** This is the
definition; [`anoieu_analyzer/reporting/verdicts.py`](../anoieu_analyzer/reporting/verdicts.py)
holds the copy that runs, and `tests/run.py` compares the two.

| a verdict is | what it means | what else the entry must carry |
| --- | --- | --- |
| `accepted and fixed` | a maintainer accepted it and the change is a commit on a named branch | `awaiting_landing` -- the debt below |
| `fixed and landed` | the change has reached the project's default branch | what landed it, and no `awaiting_landing` |
| `declined` | a maintainer read it and said no | nothing |
| `intentional` | the behaviour is deliberate and the finding was ours to withdraw | nothing |
| `not audited` | the finding is against a file whose ground truth is elsewhere | nothing |
| `withdrawn` | our error: the finding was not one | nothing |
| `re-coded` | the finding survives under a different code, which carries it | nothing |

**The vocabulary is closed because the debt has to stay checkable.** Closing on
`accepted and fixed` closes a finding before its change reaches the project's
default branch, which is exactly the mistake this repository made once and had
for three months -- three cvc5 findings recorded as *fixed upstream* on a fix
that never landed, unnoticed because a closed entry is one nothing re-derives.
A marker written in prose can be reworded out of existence; a required *word*
cannot. So the outcome is required, and `accepted and fixed` is the one that has
to say where the change is:

```bash
python3 -m anoieu_analyzer.reporting.verdicts          # what is outstanding
python3 -m anoieu_analyzer.reporting.verdicts --check  # ... and ask each checkout
```

That is a **separate pass with its own question** -- *did what we closed actually
land* -- asked on its own schedule against checkouts, deliberately not part of
recording a closure. The two get confused exactly when somebody is in a hurry,
which is when the wrong one is skipped. When a change lands, a person replaces
`awaiting_landing` with the commit that landed it.

### Where the old ledgers went

Until 2026-09-19 verdicts lived in `docs/reports/open-findings.md` and
`docs/reports/closed-findings.md`, under a reporting policy and workflow
deprecated on 2026-09-18. Both files, both generators, the landing audit that
read them and the `check_anoieu` / `process_anoieu` prompts are **removed**.
Every verdict, every hand-written note and every outstanding landing they held
was migrated onto the entries here and carries `migrated_from` saying so; the
reasoning that was in `reports.md` and `postmortem.md` is in
[`experience.md`](../docs/experience.md). Nothing was dropped, and nothing
outside this database records a verdict any more.
