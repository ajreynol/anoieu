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

## The run

One command does the whole cycle, and it is the command to use:

```bash
python3 tools/run.py            # fetch, report what has moved, measure, append
python3 tools/run.py --bump     # ... and fast-forward what can safely be moved
python3 tools/run.py --check    # verify without writing; what CI runs
```

Four steps, in order, each printing what it did:

1. **Bump.** The tools we find bugs in move, and yesterday's commit is not what
   anyone is running. Each watched checkout is fetched; with `--bump` it is also
   fast-forwarded onto its upstream. Nothing is ever forced — a tree with
   uncommitted work, without an upstream, or that would need a merge is left
   alone and says so, because these are trees other people work in.
2. **Versions.** [`versions.md`](versions.md) records what was read: branch,
   commit and date per repository, and whether the tree was dirty. A finding is
   only true of a version, and the rows carry none of their own.
3. **Counts.** [`corpus.md`](corpus.md), rewritten whole.
4. **Findings.** [`open-findings.md`](open-findings.md), appended to.

What is watched, and what is deliberately not:

| repository | what we read | what we do not |
| --- | --- | --- |
| **cvc5** | `proofs/eo` — the CPC signature and the expert extension | the solver, its build system and its proof-production code: whether cvc5 can *justify* what it decides is [dokimasia](https://github.com/ajreynol/dokimasia)'s question, not ours |
| **ethos** | the test signatures, and — as the triple's other legs — `tools/eoc/semantics` and the embedding | the C++ of the checker and the compiler |
| **logos** | `install/defs`: the installed signature and the CPC semantics it owns | the Lean development |
| **eudaimonia** | `examples/hello`, its own example calculus | `examples/cpc`, a vendored copy of cvc5's signature — checking it would report cvc5's findings under eudaimonia's name |

## Maintaining the report

Two files in `docs/` are generated, and the way they are maintained is the
medium-term plan rather than a stopgap.

[`corpus.md`](corpus.md) is counts, rewritten whole by
`tools/gen_corpus_table.py`; `--check` says whether it is current and CI runs
that. A failure means upstream moved or a check changed what it reports, and the
diff says which.

[`open-findings.md`](open-findings.md) is the report itself, one row per
finding, and it is **additive**:

- **`tools/gen_open_findings.py` adds and never removes.** A row is keyed by the
  same fingerprint a baseline uses — the code, the file, and the text of the
  line — so it survives edits elsewhere in the file. CI runs `--check`, which
  fails when a finding is unlisted and never when a row is extra.
- **Closing is a separate step, and it is a judgement.** A finding leaves the
  open table when it is fixed upstream, declined, or shown to be our error. The
  row *moves* to the Closed table with a verdict rather than being deleted:
  deletion would not stick, because the finding is still there to be found and
  the next generation would list it again. The Closed table is what makes the
  verdict durable.
- **For now the review is an AI process under human supervision.** It takes a
  row, reads the current state of the file it is about, and either leaves it or
  moves it with a verdict — writing the reasoning into
  [`upstream.md`](upstream.md), which is the prose half of the same ledger.
- **A finding that stops being reported is not evidence it was addressed.** It
  may have moved, or a check may have been narrowed. That is the whole reason
  the generator cannot delete.

The hand-written register in [`README.md`](README.md) is the first pass at all of
this and is kept as the worked example of a curated report. The generated file is
where the mechanical half now lives.

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
