# The corpus: what was measured, and what the checks report

Written by `tools/run.py`. Nothing here is typed by hand, and anything
that is will be lost on the next run.

## The versions

Every project below is a clone this repository manages under `deps/`,
restored to the commit named before the run that produced this file — not
a checkout on anyone's machine. A finding is only ever true of a version,
and the rows in [`open-findings.md`](open-findings.md) carry none of their
own, so these are what they are relative to.

| project | ref | commit | dated | what is read |
| --- | --- | --- | --- | --- |
| **cvc5** | `main` | `aee874240419` | 2026-08-29 | the CPC signature and the expert extension; the solver's own proof machinery is dokimasia's subject, not ours |
| **ethos** | `ethosEoc3` | `3cf1c03fdfd0` | 2026-08-30 | the test signatures, the semantics sets the compiler ships, and the deep embedding. The manual that defines Eunoia lives here too, and is read by people rather than by this tool |
| **logos** | `updateCompiler` | `47f29bfac93e` | 2026-08-30 | the installed signature and the CPC semantics logos owns |
| **eudaimonia** | `main` | `45e34e0d6c2d` | 2026-08-30 | its own example calculus; examples/cpc is a vendored copy of cvc5's signature and is deliberately not read |

Produced by anoieu `0.2.0`. Which commit of anoieu produced it is
the commit this file is committed in, and is deliberately not written here:
recording it would make the file stale the moment it was committed.

The clones are shallow and sparse: only the paths `tools/deps.json` names
are checked out, and nothing is built, because the analysis reads text.

## The counts

Every number here is a count of *findings*, at the severities that are on by
default.

**This is not a score, and not a comparison between repositories.** These
numbers say which of our checks tripped, not how much of a subject is sound, so
a corpus with fewer findings has not been shown to be better. See *measure the
subject, never our own coverage* in [`reporting-policy.md`](reporting-policy.md).


| corpus | files | errors | warnings | hints |
| --- | ---: | ---: | ---: | ---: |
| CPC | 35 | 3 | 19 | 15 |
| CPC with the expert signature | 51 | 3 | 23 | 15 |
| ethos test signatures | 202 | 7 | 6 | 2 |
| logos installed definitions | 0 | 0 | 0 | 0 |
| eudaimonia examples | 1 | 0 | 0 | 0 |
| the CPC triple | 35 | 3 | 20 | 15 |

## By check

**CPC**

| code | severity | count |
| --- | --- | ---: |
| DOC0011 | warning | 14 |
| EO0054 | hint | 14 |
| DOC0012 | warning | 4 |
| EO0064 | error | 3 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |

**CPC with the expert signature**

| code | severity | count |
| --- | --- | ---: |
| DOC0011 | warning | 14 |
| EO0054 | hint | 14 |
| DOC0012 | warning | 4 |
| EO0031 | warning | 4 |
| EO0064 | error | 3 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |

**ethos test signatures**

| code | severity | count |
| --- | --- | ---: |
| EO0071 | error | 6 |
| EO0084 | warning | 3 |
| DOC0011 | warning | 1 |
| DOC0012 | warning | 1 |
| EO0040 | error | 1 |
| EO0052 | warning | 1 |
| EO0054 | hint | 1 |
| EO0077 | hint | 1 |

**logos installed definitions**

Nothing reported by the checks that are on by default.

**eudaimonia examples**

Nothing reported by the checks that are on by default.

**the CPC triple**

| code | severity | count |
| --- | --- | ---: |
| DOC0011 | warning | 14 |
| EO0054 | hint | 14 |
| DOC0012 | warning | 4 |
| EO0064 | error | 3 |
| EO0077 | hint | 1 |
| EO0083 | warning | 1 |
| TRI0002 | warning | 1 |
