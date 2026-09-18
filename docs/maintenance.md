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
The [deprecated reporting workflow](reports/reporting-workflow.md) still documents
the existing findings prompts; the suite compares their executable copies with
that document until they are migrated.

The [reporting policy](reports/reporting-policy.md) is **deprecated**; its formal
replacement will use Koine's shared tooling. See the
[replacement work](#replace-the-deprecated-reporting-policy).
Nothing is filed or pushed without human direction.
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

The suite exercises the real koine append tool, resolved through `$KOINE`, the
sibling checkout, or the pinned `deps/koine` clone. CI checks out the pin; a
machine without koine must fetch it. No database implementation is mocked as a
substitute. The suite needs no external checker unless `--oracle` is requested. If `deps/`
exists, its checkouts are compared with `scripts/deps.lock`; a clean checkout
skips those comparisons. Do not silently refresh somebody's working checkouts
to make a test pass. Corpus CI restores the recorded commits with
`python3 scripts/run.py --pinned --check`; the scheduled refresh measures tips.
Oracle CI builds the pinned ethos commit and checks parser and fuzzer evidence.

### The policy checker interface

The supported interface is the latest anoieu implementation with a stable
mechanical contract: `scripts/policy_check.py --policy-version 1 --root PATH`.
Requirements, applicability and severity remain stable within that version;
checker bug fixes are allowed. New obligations require a new contract while
version 1 remains supported. The default stays 1. See the
[compatibility contract and shared CI workflow](policy-checker.md), including
the migration still needed in kanon's adoption instructions.

`--version` identifies the checker implementation commit, not the contract or
a governance document revision. Every run logs the implementation commit and
contract. Checks are encoded and tested here; they do not fetch or interpret
governance documents at runtime. The shared
[policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and
[vision](https://github.com/ajreynol/kanon/blob/main/docs/vision.md) have a separate
home. Vision is argued, never mechanically checked.

**A membership need not be advertised, and `associate` is the footing for it.**
The usual arrangement pairs a front-page declaration with a tree that backs it
and refuses either alone. A repository with reason not to announce it — not
published yet, one person's working tree, an arrangement it would oversell —
writes `**Footing:** ` and the name `associate` on its own `docs/maintenance.md`
instead, followed by what it holds itself to. That page is where this convention
already puts what a repository declines to advertise, so the claim moves there
rather than being dropped, and the checker skips the two declaration checks **by
name** rather than passing them quietly.

**An associate owes this ecosystem nothing.** The obligation on that page is
self-imposed, so the checks run and what they find is read against the marker
rather than against anything we are due — running them is reading its own claim
back to it. Whose fault a number is is **not decided here**: the shared register
knows each repository's footing and prints an associate's count as `tracked`
rather than `failing`. This checker says which tree it is looking at, words its
own summary the same way, and leaves the exit code alone — a checker that went
green on a marker in the tree it is checking would hand every repository a way
to pass by editing one line.

**One thing is still asked of an associate, and it is not a debt.** The front
page is the only thing a reader arriving at the repository has, since nothing
about the arrangement is advertised anywhere else — so it carries a
`How this repository is maintained` heading with something actually under it.
That is the floor the footing needs in order to mean anything, and it asks for
nothing the shared policy does not: its associate protocol already says that for
a tree adopting none of this, the ask is still that one heading. A tree below it
is reported like any other number found on an associate — as `tracked`, with
nobody at fault.

**Explaining the name is not part of the floor.** It is recommended for every
repository and required of none, and a footing is not a reason to read that
differently: an associate with no name section is told so as a minor finding,
exactly as a member is, and neither is failed for it.

A child project its parent's front page does not name records `unadvertised-child`
in its own README; that claim is about the parent and is checked against it.

**Link kanon at `main`, or not at all.** Kanon holds the governing documents,
so what they say today is what binds this repository: a link into that tree
goes to `main`. Never pin one to a commit — a pinned rule is a superseded copy
of somebody else's live page, and keeping one here would make anoieu an archive
of governance it does not hold. Where kanon has removed a page this record
names, the record names it and does not link it. Pinning anoieu's *own* removed
material is a different thing and is fine: this tree is ours to archive.

Do not relax a check merely to make CI green; what a new one owes is below,
under [adding a check](#adding-a-check-to-the-policy-checker). Keep downstream
compatibility explicit: declarations may link either the current shared policy
or its former anoieu location. Anoieu's owner and script-catalog checks read this page.

## Adding a check to the policy checker

The checker is the one program here that runs on other people's builds, so a
check is not a change to this repository — it is a change to theirs. It lands
permanently, it fires at moments nobody chose, and it is nearly never deleted.
**And it is a change to a published contract**: a new obligation, or an existing
one applied to more repositories, needs a new
[policy version](policy-checker.md), never a bug fix. Four conditions before one
goes in.

**It is decidable without an opinion.** Where answering it needs judgement it
belongs in the shared vision, which must never acquire a checker.

**It has been run against a tree this repository did not write.** Every false
positive so far was found by somebody else's repository and none by ours, which is
not luck: this is the one tree shaped like the checker's assumptions. Run a new
check against every checkout on the machine before it lands. A check that has only
ever seen this tree has not been tested.

**Its message names the fix.** A failure somebody has to interpret costs more than
the defect it found, and they are reading it in a red build on a schedule that is
not theirs.

**It stays true without curation.** The expensive kind is the check whose *data*
rots — a list of vendor names, a registry of tools, anything that has to be updated
as the world changes rather than as the tree does. There is one of those already,
`VENDORS`, and it is the check most likely to be wrong a year from now. Prefer a
check whose only input is the repository in front of it.

### Why this is a limit and not a ritual

The failure mode is a set of checks large enough that keeping it honest is the
work. Three things produce it, and each looks like diligence.

**A check that fires wrongly costs more than it can ever save** — somebody else's
afternoon, and the credibility of the whole set, because a maintainer who has been
sent one spurious failure reads the next one differently, including the true ones.

**Every check is a migration**, and *we do not pay it*. A repository that passes
today and fails tomorrow does work it did not ask for at a moment it did not
choose; the contract makes that survivable and does not make it free.

**Checks accumulate and are almost never removed.** So the question at the point of
adding one is not *is this true* but *will I defend this in a year, on somebody
else's repository, when it fails inconveniently*. Anything short of yes belongs in
the minor tier, which is what that tier is for.

**And there is a stopping rule.** A check earns its place by finding something. The
anchor check found three dead links on its first run. A check that has never fired
on anything is either perfect or pointless, and the second is the way to bet.

*This section is kanon's text, offered in their `D10` and taken.*

## The scripts

Commands are run from the repository root unless noted.

| file in `scripts/` | purpose |
| --- | --- |
| `run.py` | fetch the corpus and generate reports; `--pinned --check` checks recorded commits |
| `deps.py` | corpus checkout and lock helpers, imported by the runner |
| `deps.json`, `deps.lock` | corpus sources and recorded commits |
| `gen_checks_doc.py` | generate the check catalogue |
| `gen_corpus_table.py` | measure and render the corpus, imported by the runner |
| `gen_open_findings.py` | record findings through koine, add ledger rows and render the static table; `--check` previews through koine and reports missing rows |
| `landing.py` | report changes awaiting landing, and read every closed verdict against [the verdict vocabulary](reports/reporting-workflow.md#the-verdict-vocabulary-and-why-it-is-closed); `--check` reads checkouts |
| `anoieu_analyzer` | run every standard target, dump the bugs, append through koine; `--dry-run` lists signatures and analyses nothing, `--preview` runs the analysis and koine's dry run |
| `anoieu_fuzzer` | fuzz two checkers against each other: `anoieu_fuzzer ethos logos N`, where N is how many cases; `--dry-run` resolves the binaries and runs nothing. The full interface is `python3 -m anoieu_fuzz run` |
| `targets.json`, `targets.py` | the standard targets, and where each project is on this machine |
| `koine.py`, `koine.lock` | resolve the required [koine](https://github.com/ajreynol/koine), falling back to a clone at the pin; delegate its CLI unchanged to `bug_db/koine_append_db` |
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

### Replace the deprecated reporting policy

**Pending, recorded 2026-09-18.** Replace the deprecated policy and workflow with
a formal reporting policy built around
[Koine's shared tooling](https://github.com/ajreynol/koine). The current
`bug_db/koine_append_db` integration records findings; it does not implement
triage, verdicts or closure. The replacement needs to:

- Define the reporting lifecycle, evidence required for each transition, and
  which decisions belong to a human.
- Use Koine for shared reporting mechanics, identifying any missing capabilities
  there before migrating anoieu's commands and prompts.
- Preserve existing finding ids, verdicts, evidence and history, and update the
  entry-point documentation and checks when the replacement is ready.

Until then, keep using the existing commands and preserving the current records.
Marking the documents deprecated is not a completed migration.

### Preserve the findings record

The ledger needs stronger mechanical guarantees through that migration.
These are work items, not
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
path-independent fingerprints. Shared reporting mechanics belong in Koine;
anoieu-specific checks stay here.

### The one thing the bug database cannot tell us

**A bug in the database and not in a run's dump may have been fixed, or the run
may not have looked there — and nothing distinguishes those.** `koine_append_db`
says as much in its own words and does not guess. This is a cost we took
knowingly on 2026-09-16, when koine replaced a findings record that carried runs
and per-id coverage with a database that carries neither; the smaller thing that
does less was the right trade, and it is recorded here so that the trade stays
visible rather than being rediscovered as a defect.

**Koine is the required database writer.** Analyzer runs, fuzzer promotion and
reporting, and ledger generation all call `bug_db/koine_append_db`; no backend
setting or alternate writer is supported. Preview modes call koine's own dry
run. Anoieu supplies finding identities and evidence; koine owns validation,
deduplication, conflict reporting, dates and database writes. If that interface
needs a capability it lacks, propose the change to koine rather than implement
a competing database path here.

**For now we answer coverage on our own side.** `scripts/targets.json` says what
a full static run reads. `python3 -m anoieu_fuzz report` records the promoted
reproducer corpus, with recorded outcomes and the same ids as the ledger;
[the fuzzer guide](fuzzing.md#recording-through-koine) explains the command.
Recording performs no replay, so its ingestion dates do not establish that a
bug still reproduces. Neither producer's dump determines closure.

**What would bring it back.** The second producer is
`prompts/anoieu_analyzer_agent`, and the two are compared by appending both
dumps. If the two producers start reading materially different sets of files —
the agent three and the program forty — a disagreement and a gap become
indistinguishable, and that is the point at which to go back to koine with
evidence rather than with a preference.
