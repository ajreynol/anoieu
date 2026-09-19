# The documentation

The written core is listed below, followed by generated reports and maintenance
documents. Each entry points to the page that owns its subject.

## Written

| document | its job |
| --- | --- |
| [`bug_db/README.md`](../bug_db/README.md) | **the shared bug database artifact**: setup, one-command updates from the analyzer and promoted fuzzer corpus, and the remaining closure work |
| [`experience.md`](experience.md) | **what the projects we watch did with what we found**: one section per upstream pull request that closed an observation, what the change meant, and what it says about the check underneath it. Also what each run taught us about our own tooling |
| [`usage.md`](usage.md) | **the analyzer's interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together. For work on this repository, start at [`maintenance.md`](maintenance.md) |
| [`policy_check/README.md`](../policy_check/README.md) | **policy-checking responsibilities and contract** — implementation, versioned requirements and severities, focused tests, maintenance guidance and the shared CI workflow |
| [`policy-checker.md`](policy-checker.md) | **a one-line pointer** at the row above, kept because other repositories link to this path |
| [`reporting-policy.md`](reporting-policy.md) | **what may be said about code we do not own**: what separates a candidate published under our own name from a finding carried to its owner, what may be taken as material, and what tier each position is enforced at. The mechanics are `bug_db/README.md`; this is the position |
| [`fuzzing.md`](fuzzing.md) | **the other half**: the anoieu fuzzer, which writes Eunoia nobody would write and hands it to a checker. What its oracle is, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker, and what it is deliberately not: a baseline, whose research-quality successor nobody has started |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the pages above belongs here |

## Generated

Written by a run, and the only files here a tool may edit.

| document | its job |
| --- | --- |
| [`corpus.md`](corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |
| [`bug_db/bugs.json`](../bug_db/bugs.json) | **the database, the raw data, and the only record of a verdict** — static findings and promoted fuzzer findings, one JSON object each. Every recording command calls [koine](https://github.com/ajreynol/koine)'s `koine_append_db`, which adds entries and updates ingestion dates while preserving existing content. A decision about a finding is the `closed_verdict` on its entry; see [Closure](../bug_db/README.md#closure). **Not reconstructible** — the verdicts and hand-written notes on it exist nowhere else |
| [`bug_db/bugs.md`](../bug_db/bugs.md) | **the GitHub browsing view**, rendered from the JSON for both producers with each finding's status and evidence links; refreshed by recording commands and checked by CI |
| [`bug_db/static-analysis.md`](../bug_db/static-analysis.md) | **the static subset rendered from the database**, with the verdict recorded against each row. Nothing here closes a finding. *Rewritten whole, from the database* |

> **The database is not like the others.** `corpus.md`, `checks.md` and the two
> rendered views are rewritten whole, so anything typed into one is lost on the
> next run. `bugs.json` is *additive*: koine adds entries and never removes or
> rewrites one, so every verdict, note and closure written onto an entry
> survives. The asymmetry is deliberate — a writer that could delete could
> quietly delete a regression.

## Maintenance and records

[`maintenance.md`](maintenance.md) is the entry point for work on anoieu: its
responsibilities, retained commands, required checks, and open technical work.
The [script catalogue](maintenance.md#the-scripts) lists the commands in
[`../scripts/`](../scripts) and the prompts in [`../prompts/`](../prompts).
[`close_bug_db`](../prompts/close_bug_db) is the one that writes a verdict;
[Closure](../bug_db/README.md#closure) defines what it may write.

[`discussion.md`](discussion.md) is anoieu's correspondence with the ecosystem
for requests, proposals and questions. Defect reports belong in the
[database](../bug_db/README.md). The shared
[discussion format](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#the-discussion-file)
defines those conventions.

How each tool stands against the shared tenets is
[stathmos](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/README.md)'s,
and its [report card](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/docs/report-card.md)
is the live edition — both paths read 2026-09-19. Nothing here grades a tool.

[`history.md`](history.md) records anoieu's development and presidency, including
the handoff. Its [presidential letter](letter-to-kanon.md) is addressed to its
successor. Dated quotations and covering notes describe their original
occasions.

`docs/` also holds documents rendered for an audience that will not clone this
repository, currently [`cpc-audit.html`](cpc-audit.html). They restate
findings from the sources above rather than adding any, so nothing is filed
twice. The generators are in [`anoieu_analyzer/reporting/`](../anoieu_analyzer/reporting), and each says at the top
of the file what it writes and what it refuses to do.
