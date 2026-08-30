# What the report was measured against

Written by `tools/run.py`. A finding is only ever true of a version: the
rows in [`open-findings.md`](open-findings.md) carry none of their own, and
this is what they are relative to. A row that outlives the commit it was
found in is a row worth re-checking.

| tool | what it holds | branch | commit | dated |
| --- | --- | --- | --- | --- |
| **anoieu** | this analyzer | `main` | `caf13e5d8054` *(uncommitted changes)* | 2026-08-30 |
| **cvc5** | `proofs/eo`: the CPC signature and the expert extension | `main` | `aee874240419` | 2026-08-29 |
| **ethos** | three of the tools at once: the checker, `ethos-eoc`, and `user_manual.md`, which is where Eunoia is defined | `ethosEoc3` | `52bba6712ad0` *(uncommitted changes)* | 2026-08-30 |
| **logos** | the Lean development, and the CPC semantics it owns | `updateCompiler` | `47f29bfac93e` *(uncommitted changes)* | 2026-08-30 |
| **eudaimonia** | the template, and the example calculi we read | `main` | `d212079dd32c` *(uncommitted changes)* | 2026-08-30 |

The analyzer reports its own version as `0.2.0`; the commit above is
what actually ran.

A repository shown with uncommitted changes measured a working tree rather
than a commit, so its findings are not reproducible from the commit alone.
