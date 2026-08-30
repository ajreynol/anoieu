# What the report was measured against

Written by `tools/run.py`. Every project below is a clone this repository
manages under `deps/`, updated before the run that produced this file — not
a checkout on anyone's machine. A finding is only ever true of a version,
and the rows in [`open-findings.md`](open-findings.md) carry none of their
own, so this is what they are relative to.

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
