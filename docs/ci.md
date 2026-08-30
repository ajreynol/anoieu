# Running anoieu in CI

The long-term goal is for ethos, logos and cvc5 to run this on every push. This
is how that should be arranged, and what has to be true before each step.

## The model: one tool, three thin integrations

anoieu stays one repository and ships as one versioned package. Each repository
that uses it owns three things and nothing else:

| the repository owns | written as | why there |
| --- | --- | --- |
| which signatures it has | `entry_points` in `anoieu.json` | only that repository knows |
| what it has agreed to live with | a baseline file, committed | a record of decisions, reviewed like code |
| which checks it runs, and how loudly | `enable` / `disable` / `severity` | policy differs per repository |

Everything else — the checks, their severities by default, the manual pages —
lives here. A repository's CI job is then one line, and its policy is a file its
own reviewers can read.

**The inversion that makes this safe:** anoieu's own CI checks out cvc5 and
ethos at pinned refs and runs the analyzer over them against a baseline
committed *here* (`tests/corpus/cpc-baseline.json`). A change that invents a
false positive fails **anoieu's** build, before it can fail anyone else's. That
job is the reason downstream repositories can pin a version and forget about it.

## What each repository would check

| repository | entry points | what it buys |
| --- | --- | --- |
| **cvc5** | `proofs/eo/cpc/Cpc.eo`, `proofs/eo/cpc/expert/CpcExpert.eo` | the calculus everything downstream is built from; this is where the findings so far are |
| **ethos** | `tests/*.eo` | its test signatures are small, numerous and lightly exercised — the `<` `:right-assoc` bug lives in one of them |
| **logos** | `install/defs/Cpc.eo`, and `Cpc.eos` once the triple checks land | the flattened copies the Lean development is built from, and the semantics beside them |
| **eudaimonia** | whatever calculus a generated checker is for | the template's whole promise is that a new calculus compiles; this says so earlier |

Two exclusions worth stating: the compiler's `$MARKER$` templates under
`plugins/` are not signatures and will report as such, and generated artifacts
(`Cpc.cached.eo`) repeat whatever their source says, so checking both files
reports everything twice.

## The rollout ladder

Turning this on as a blocking check on day one fails the build on findings
nobody has triaged. Four steps, each safe to stop at:

**1. Report only.** Annotations appear on pull requests; nothing fails.

```yaml
- run: python3 -m anoieu check <entry points> --format github
  continue-on-error: true
```

**2. Baseline, and fail on new errors.** Record today, block tomorrow's:

```bash
python3 -m anoieu check <entry points> --baseline .anoieu-baseline.json --update-baseline
git add .anoieu-baseline.json
```

```yaml
- run: python3 -m anoieu check --baseline .anoieu-baseline.json
```

**3. Fail on new warnings too**, by adding `--deny-warnings`. Do this once the
first month of new findings has been all true positives.

**4. Burn the baseline down and delete it.** Each entry removed is a defect
fixed or a decision recorded as a suppression comment, which is better than a
line in a file because it sits where the decision applies:

```lisp
; anoieu: allow EO0054  matching exactly two children is what this rule is about
(($contains (or l xs) l) true)
```

A run reports how many findings its comments silenced, so this does not become a
way to lose track of them.

## Pinning

Each repository pins a version:

```yaml
- run: pip install anoieu==0.2.*
```

A new check then reaches a repository only when someone there bumps the pin,
which is the point: the analyzer's release cadence is not allowed to break other
people's builds. Versioning follows from that — a new check or a widened
existing one is a **minor** bump with a line in the release notes; a removal or
a renumbering is **major**; a fix that narrows a check is a **patch**, because it
can only reduce what a repository sees.

For a repository that would rather not take a PyPI dependency, anoieu is pure
Python with no dependencies of its own: a git submodule and `python3 -m anoieu`
works identically.

## Severity policy, per repository

The default severities are a claim about the language, not about anyone's
codebase, so a repository may re-pitch them. What we would suggest:

| family | default | cvc5 | ethos | logos |
| --- | --- | --- | --- | --- |
| correctness — `EO0040`–`EO0066` | error / warning | as-is | as-is | as-is |
| documentation — `DOC0010`–`DOC0012` | warning | as-is: the docstrings are a real convention there | `"disable"` — its tests are not documented that way | as-is |
| taste — `EO0054`, `EO0056`, `EO0060`, `DOC0001` | hint / off | on for review, not for CI | off | off |

```json
{
  "entry_points": ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
  "baseline": "proofs/eo/anoieu-baseline.json",
  "severity": {"EO0054": "hint"}
}
```

Put that at the repository root, or beside the signatures — discovery walks up
from the entry point — and the CI job becomes `python3 -m anoieu check`.

## What a job looks like

```yaml
name: signatures
on: [push, pull_request]
jobs:
  anoieu:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install anoieu==0.2.*
      - run: anoieu check --format github
      - run: anoieu check          # the same run, for the exit code
```

Two invocations because the annotation format prints no summary; a job that only
wants the exit code can drop the first.

For GitHub code scanning instead of inline annotations:

```yaml
      - run: anoieu check --format sarif > anoieu.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: anoieu.sarif }
```

## Costs

A whole-of-CPC run reads 51 files and finishes in well under a second, with no
build, no solver and no proof. There is nothing to cache and nothing to
parallelize; the job is dominated by checking out the repository.

## The order to do this in

1. **ethos first.** It is the smallest surface, its maintainers are the audience
   for the language findings, and its own test suite already holds one.
2. **cvc5 next, report-only**, so the three real findings get triaged with no
   pressure on the build.
3. **cvc5 blocking, with a baseline**, once those are resolved.
4. **logos last**, and after the triple checks land — which is the point at which
   anoieu says something logos cannot get anywhere else: whether the signature,
   the calculus semantics and the SMT semantics agree.

## One open question, worth deciding early

The triple checks (M4) need a signature *and* its `.eos` semantics, and those
live in different repositories: CPC's signature is in cvc5, its official
semantics in logos. Whichever repository runs that job needs both checked out.
logos already vendors ethos and consumes cvc5's signature, so it is the natural
home — which means the most valuable check anoieu will have runs in the
repository furthest from where its findings are usually fixed. Worth agreeing on
before it is built: either logos runs it and files issues against cvc5, or cvc5
grows a job that checks out logos for its semantics.
