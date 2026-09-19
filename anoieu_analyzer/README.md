# anoieu_analyzer

The static analyzer: it reads Eunoia signatures (`.eo`) and semantic
configurations (`.eos`) as text and reports what it can decide without running a
proof. The [front page](../README.md) says what the repository is; this is the
entry point for the analyzer itself.

```bash
python3 -m anoieu_analyzer check path/to/signature.eo
python3 -m anoieu_analyzer check path/to/signature.eo --format github
scripts/anoieu_analyzer                      # every standard target, into the bug database
```

## Its documents

| document | its job |
| --- | --- |
| [`usage.md`](usage.md) | **the interface.** Every command and option, and how configuration, baselines and suppression fit together |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. *Generated from the registry, rewritten whole* |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — built, rejected, open |

What a run *finds* is not here. Findings are recorded in
[`bug_db/`](../bug_db/README.md), what may be said about them is the
[reporting policy](../bug_db/reporting-policy.md), and what the projects did
about them is [`experience.md`](../docs/experience.md).

## What is in this directory

`checks/` holds one module per family of checks, each registering the codes it
owns; `diagnostics.py` defines a finding and the output formats; `reporting/`
holds the machinery a run uses — target selection, checkout management, the koine
adapter, the generators and the verdict audit. `reporting/config/` carries the
committed manifests and locks that say what a run reads and at which commit.

Working on it? Start at [`docs/maintenance.md`](../docs/maintenance.md).
This page was read against the code on 2026-09-19.
