# Anoieu's bug database

[`bugs.json`](bugs.json) is the persistent artifact shared by the **static
analyzer and the fuzzer**. It contains every recorded finding, including ones
that have since been resolved. Koine's `bug_db/koine_append_db` is its only
writer; Koine provides the tooling, and this directory holds anoieu's data.

**[Browse the bug database](bugs.md)** directly on GitHub. The generated page
shows both producers, diagnostic descriptions, ingestion dates, and links to
source locations or committed reproducers. Open the **Preview** tab if GitHub
shows the Markdown source. No server or local setup is needed to read it.

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
[static table](../docs/reports/static-analysis.md). It succeeds
only if recording succeeds. Repeating it adds no duplicate findings.

`--preview` writes the disposable dump `scratch/new-report-bugs.json` and asks
Koine for a dry run; it leaves the database and reports unchanged. The update
uses the source checkouts already on disk. It does not fetch newer targets,
start a fuzzing campaign, or replay the recorded fuzzer cases.

## Setup

- **Static inputs:** [`config/targets.json`](../config/targets.json) names the
  targets. Set their checkout paths in the gitignored `config/repos.local`
  (one `project /path/to/checkout` per line), or use the managed `deps/` clones.
  `python3 scripts/run.py --pinned` prepares those clones at the recorded commits
  and regenerates the legacy reports too. The update command refuses missing
  configured input paths instead of silently recording a partial refresh.
- **Koine:** [`anoieu/reporting/koine.py`](../anoieu/reporting/koine.py) finds `$KOINE`, then
  `../koine`, then `deps/koine`. A normal update or preview can clone the commit
  in [`config/koine.lock`](../config/koine.lock) into `deps/koine` if needed;
  `--dry-run` only checks and reports missing setup. No package installation is
  needed. An existing checkout is used as-is, and the update prints its version.
- **Fuzzer evidence:** reporting the promoted corpus needs no checker binaries.
  Discovering new findings requires the checkers you want to compare, as
  described in the [fuzzer guide](../docs/fuzzing.md).

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

The updater, analyzer, fuzzer reporting/promotion and legacy ledger generator
refresh `bugs.md` after a successful append. To render existing data without
running either producer, use `python3 -m anoieu.reporting.database`. Its
`--check` mode detects a stale view, and CI runs that check. A direct append with
the low-level Koine command needs this render step. Commit `bugs.md` alongside
the JSON so GitHub displays the matching view.

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

## Closure and the reporting transition

**Database recording is ready; automatic closure assessment is not implemented.**
A finding absent from a later dump may have disappeared because an input was
skipped, a check changed, or its fingerprint changed. The updater never closes a
finding based on absence. Fuzzer closure requires replay evidence, not another
export of its stored outcomes.

Verdicts and their evidence remain in the existing
[open](../docs/reports/open-findings.md) and
[closed](../docs/reports/closed-findings.md) ledgers. The old
[reporting policy](../docs/reports/reporting-policy.md) is deprecated; the
[replacement work](../docs/maintenance.md#replace-the-deprecated-reporting-policy)
tracks the formal policy and the Koine capabilities needed to assess closure
from complete, comparable runs while retaining history.
