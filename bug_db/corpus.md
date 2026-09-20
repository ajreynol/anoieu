# The corpus: what was measured, and what the checks report

Written by `scripts/run.py`. Nothing here is typed by hand, and anything
that is will be lost on the next run.

## The versions

Every project below is a clone this repository manages under `deps/`,
restored to the commit named before the run that produced this file — not
a checkout on anyone's machine. A finding is only ever true of a version,
and the entries in [`bugs.json`](bugs.json) carry none of their
own, so these are what they are relative to.

| project | ref | commit | dated | what is read |
| --- | --- | --- | --- | --- |
| **cvc5** | `main` | `dbf176dfb71b` | 2026-09-19 | the CPC signature and the expert extension; the solver's own proof machinery is dokimasia's subject, not ours |
| **ethos** | `main` | `04a9b4d41508` | 2026-09-19 | the test signatures, the semantics sets the compiler ships, and the deep embedding. The manual that defines Eunoia lives here too, and is read by people rather than by this tool |
| **logos** | `main` | `c8165b2afd32` | 2026-09-18 | the installed signature and the CPC semantics logos owns |
| **eudaimonia** | `main` | `b465b9d954bb` | 2026-09-19 | its hello and scoped example calculi; new_checker/examples/cpc is a vendored copy of cvc5's signature and is deliberately not read |

Produced by anoieu `0.2.0`. Which commit of anoieu produced it is
the commit this file is committed in, and is deliberately not written here:
recording it would make the file stale the moment it was committed.

The clones are shallow and sparse: only the paths `anoieu_analyzer/reporting/config/deps.json` names
are checked out, and nothing is built, because the analysis reads text.

## The counts

Every number here is a count of *findings*, at the severities that are on by
default.

**This is not a score, and not a comparison between repositories.** These
numbers say which of our checks tripped, not how much of a subject is sound, so
a corpus with fewer findings has not been shown to be better. See *Measure the
subject, never our own coverage* in the
[reporting policy](reporting-policy.md#what-we-publish).


| corpus | files | errors | warnings | hints |
| --- | ---: | ---: | ---: | ---: |
| CPC | 35 | 0 | 1 | 15 |
| CPC with the expert signature | 51 | 0 | 1 | 15 |
| ethos test signatures | 205 | 2 | 0 | 1 |
| logos installed definitions | 0 | 0 | 0 | 0 |
| eudaimonia examples | 2 | 0 | 0 | 0 |
| the CPC triple | 35 | 0 | 1 | 15 |

## By check

**CPC**

| code | severity | count |
| --- | --- | ---: |
| EO0054 | hint | 14 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |

**CPC with the expert signature**

| code | severity | count |
| --- | --- | ---: |
| EO0054 | hint | 14 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |

**ethos test signatures**

| code | severity | count |
| --- | --- | ---: |
| EO0071 | error | 2 |
| EO0077 | hint | 1 |

**logos installed definitions**

Nothing reported by the checks that are on by default.

**eudaimonia examples**

Nothing reported by the checks that are on by default.

**the CPC triple**

| code | severity | count |
| --- | --- | ---: |
| EO0054 | hint | 14 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |
