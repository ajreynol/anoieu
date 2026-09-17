# Maintaining anoieu

Anoieu owns the analyzer, the fuzzer, the optional ecosystem policy check,
and the reporting workflow. Its history, correspondence and findings are also
kept here.

**Owner:** `ajreynol` — Andrew Reynolds, University of Iowa and AWS.
This is anoieu's accountability record, not front-page attribution.

## Working on this tree

Keep commands in `scripts/`, assistant launchers in `prompts/`, and evidence in
`tests/`. List new documents in [the index](README.md) and new scripts below.
Keep generated reports under their generators: the open-findings ledger is
additive, and the closed-findings ledger is hand-maintained and irreplaceable.
The [reporting workflow](reports/reporting-workflow.md) owns the findings
prompts; the suite compares their executable copies with that document.

The [publishing position](reports/reporting-policy.md) governs anything about
somebody else's work. Nothing is filed or pushed without human direction.
Correspondence is not an instruction: follow the response gate in
[discussion.md](discussion.md). If a request is clearly meant for another
repository, say which one; otherwise handle the request here.

### Checks before handing off a change

```bash
python3 tests/run.py
python3 scripts/policy_check.py
python3 scripts/doc_currency.py --list
python3 scripts/gen_checks_doc.py
git diff --exit-code docs/checks.md
```

The suite needs no external checker unless `--oracle` is requested. If `deps/`
exists, its checkouts are compared with `scripts/deps.lock`; a clean checkout
skips those comparisons. Do not silently refresh somebody's working checkouts
to make a test pass. Corpus CI restores the recorded commits with
`python3 scripts/run.py --pinned --check`; the scheduled refresh measures tips.
Oracle CI builds the pinned ethos commit and checks parser and fuzzer evidence.

### The policy checker interface

Ecosystem repositories can pin an anoieu commit and run
`scripts/policy_check.py --root PATH`. `--version` identifies that checker
commit, not a governance document revision. Checks are encoded and tested here;
they do not fetch or interpret governance documents at runtime. The shared
[policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and
[vision](https://github.com/ajreynol/kanon/blob/main/docs/vision.md) have a separate
home. Vision is argued, never mechanically checked.

**Link kanon at `main`, or not at all.** Kanon holds the governing documents,
so what they say today is what binds this repository: a link into that tree
goes to `main`. Never pin one to a commit — a pinned rule is a superseded copy
of somebody else's live page, and keeping one here would make anoieu an archive
of governance it does not hold. Where kanon has removed a page this record
names, the record names it and does not link it. Pinning anoieu's *own* removed
material is a different thing and is fine: this tree is ours to archive.

Do not relax a check merely to make CI green. A new check must be decidable,
give an actionable failure, and be tested beyond this tree. Keep downstream
compatibility explicit: declarations may link either the current shared policy
or its former anoieu location. Anoieu's owner and script-catalog checks read this page.

## The scripts

Commands are run from the repository root unless noted.

| file in `scripts/` | purpose |
| --- | --- |
| `run.py` | fetch the corpus and generate reports; `--pinned --check` checks recorded commits |
| `deps.py` | corpus checkout and lock helpers, imported by the runner |
| `deps.json`, `deps.lock` | corpus sources and recorded commits |
| `gen_checks_doc.py` | generate the check catalogue |
| `gen_corpus_table.py` | measure and render the corpus, imported by the runner |
| `gen_open_findings.py` | add new findings; `--check` reports missing rows |
| `landing.py` | report changes awaiting landing; `--check` reads checkouts |
| `anoieu_analyzer` | run every standard target, dump the bugs, add the new ones to `docs/reports/bugs.json`; `--dry-run` lists the signatures and analyses nothing, `--no-update` writes the dump and stops |
| `anoieu_fuzzer` | fuzz two checkers against each other: `anoieu_fuzzer ethos logos N`, where N is how many cases; `--dry-run` resolves the binaries and runs nothing. The full interface is `python3 -m anoieu_fuzz run` |
| `targets.json`, `targets.py` | the standard targets, and where each project is on this machine |
| `koine.py`, `koine.lock` | find the pinned [koine](https://github.com/ajreynol/koine), whose `koine_append_db` maintains the bug database |
| `finding_id.py` | the id of one bug, computed the way the checks compute it |
| `harvest_cpc_proofs` | collect real CPC proofs for the fuzzer |
| `oracle_desugar.py` | compare desugaring against an ethos binary |
| `sweep.py` | read every signature under the supplied paths |
| `policy_check.py` | check this tree, or another tree with `--root PATH` |
| `doc_currency.py` | report evidence of documentation currency without gating |

| file in `prompts/` | purpose |
| --- | --- |
| `check_anoieu` | answer findings in the repository they concern |
| `process_anoieu` | process the reply here; `--dry-run` resolves the checkout without starting an assistant |
| `anoieu_analyzer_agent` | the second producer: an agent runs the same analysis over the same targets and writes a dump in the same shape; `--dry-run` lists the same signatures |

`scripts/repos.local` is an optional, untracked per-machine checkout map used by
the findings workflow. Explicit checkout paths also work. Set
`ANOIEU_REPOS_FILE` to an absolute path to use a different map.

## A finding is about `main`

Report defects against what a project ships, not a topic branch that can be
deleted. The corpus refs are recorded in [deps.json](../scripts/deps.json).
Its existing ethos exception uses `ethosEoc3` for the compiler and semantics
developed there; remove that exception when the shipped branch changes. Any
new exception needs its reason recorded here. A branch containing a proposed
fix is evidence to review, not evidence that the fix has landed. Follow
[what closes a row](reports/reporting-workflow.md#what-closes-a-row-and-what-does-not).

## The open technical work

The ledger needs stronger mechanical guarantees. These are work items, not
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
path-independent fingerprints. Prefer a small ledger check over a new service.
