# The documentation

The written core is listed below, followed by generated reports and maintenance
documents. Each entry points to the page that owns its subject.

## Written

| document | its job |
| --- | --- |
| [`reports.md`](reports/reports.md) | **what anoieu has to say about other people's code**: what it is asking of each project, how each finding was confirmed, and what came back when it was filed |
| [`reporting-policy.md`](reports/reporting-policy.md) | **what may be published about somebody else's code, and why.** The position anoieu shares with [dokimasia](https://github.com/ajreynol/dokimasia) — twelve of them, each saying whether it is enforced, structural, or an intention nothing but our record backs |
| [`reporting-workflow.md`](reports/reporting-workflow.md) | **how a finding is handled**: the conventions governing the record, the workflow and prompts for carrying one to whoever can fix it, and for
sweeping the whole report, and what it takes for another repository to run these checks in its own CI |
| [`usage.md`](usage.md) | **the analyzer's interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together. For work on this repository, start at [`maintenance.md`](maintenance.md) |
| [`policy-checker.md`](policy-checker.md) | **the stable policy-checker contract** — latest implementation, versioned requirements and severities, the shared CI workflow, and the migration from consumer commit pins |
| [`fuzzing.md`](fuzzing.md) | **the other half**: the anoieu fuzzer, which writes Eunoia nobody would write and hands it to a checker. What its oracle is, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker, and what it is deliberately not: a baseline, whose research-quality successor nobody has started |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the six above belongs here |

## Generated

Written by a run, and the only files here a tool may edit — **except one.**
`closed-findings.md` sits in this table because it lives with the others and is
hand-maintained; being in this section is what once made it look disposable.

| document | its job |
| --- | --- |
| [`open-findings.md`](reports/open-findings.md) | **every finding currently reported**, one row each. *Additive* — see the caution below |
| [`closed-findings.md`](reports/closed-findings.md) | **internal, and NOT generated** — it is written by the review step and only *read* by the generator, which skips every id in it. **It is the ledger of verdicts and cannot be reconstructed**: delete it and every settled finding is reported to its project again, including the ones somebody already declined. It is listed here because it lives beside the other two, and `scripts/policy_check.py` deliberately leaves it out of its generated list |
| [`corpus.md`](reports/corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |
| [`bugs.json`](reports/bugs.json) | **the database, and the raw data** — static findings and promoted fuzzer findings, one JSON object each. The analyzer, fuzzer promotion/reporting commands and ledger generator always call [koine](https://github.com/ajreynol/koine)'s `koine_append_db`, which adds entries and updates ingestion dates while preserving existing bug content. Decisions remain in the findings ledgers. |
| [`static-analysis.md`](reports/static-analysis.md) | **the static subset rendered from the database**, the new workflow's page. `open-findings.md` remains the report, and nothing here closes a bug. *Rewritten whole, from the database* |

> **The two findings files are not like the others.** `corpus.md` and
> `checks.md` are rewritten whole, so anything typed into one is lost on the next
> run. The findings files are *additive*: the generator adds rows and never
> removes or rewrites one, so the notes column and every verdict are written by
> hand and all survive. The asymmetry is deliberate — a generator that could
> delete could quietly delete a regression.

[`postmortem.md`](reports/postmortem.md) is what running that workflow once actually
taught us: the log of one project's twenty rows, what the assistant at the far
end got right and wrong, what we got wrong, and the two rules the round
established — that each round leaves the prompts *shorter and clearer*, and that
a person approves every change to one.

## Maintenance and records

[`maintenance.md`](maintenance.md) is the entry point for work on anoieu: its
responsibilities, retained commands, required checks, and open technical work.
The [script catalogue](maintenance.md#the-scripts) lists the commands in
[`../scripts/`](../scripts) and the findings prompts in
[`../prompts/`](../prompts). The
[reporting workflow](reports/reporting-workflow.md#the-workflow) defines those
prompts, and `tests/run.py` checks their executable copies against it.

[`discussion.md`](discussion.md) is anoieu's correspondence with the ecosystem
for requests, proposals and questions. Defect reports belong in the findings
ledger. The shared
[discussion format](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#the-discussion-file)
defines those conventions.

The assessment of how each tool stands against the shared tenets is no longer
kept here. [stathmos](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/README.md)
holds it, and its [report card](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/report-card.md)
supersedes the edition this repository graded through 2026-09-02.

[`history.md`](history.md) records anoieu's development and presidency, including
the handoff. Its [presidential letter](letter-to-kanon.md) is addressed to its
successor. Dated quotations and covering notes describe their original
occasions.

`reports/` also holds documents rendered for an audience that will not clone this
repository, currently [`cpc-audit.html`](reports/cpc-audit.html). They restate
findings from the sources above rather than adding any, so nothing is filed
twice. The generators are in [`../scripts/`](../scripts), and each says at the top
of the file what it writes and what it refuses to do.
