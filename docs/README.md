# The documentation

Six documents, so that a question has one obvious place to be answered, plus the
files a run generates. If you are looking for content rather than for where
content lives, every row below leads somewhere better.

## Written

| document | its job |
| --- | --- |
| [`philosophy.md`](philosophy.md) | **what may be published about somebody else's code, and why.** The position anoieu shares with [dokimasia](https://github.com/ajreynol/dokimasia) — anoieu maintains it, dokimasia references it — including what "maintained by AI under light supervision" does and does not cover |
| [`reports.md`](reports.md) | **what anoieu has to say about other people's code**: what it is asking of each project, how each finding was confirmed, and what came back when it was filed |
| [`reporting-policy.md`](reporting-policy.md) | **how a finding is handled**: the conventions governing the record, the workflow and prompts for carrying one to whoever can fix it, and what it takes for another repository to run these checks in its own CI |
| [`usage.md`](usage.md) | **the interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the five above belongs here |

## Generated

Written by a run, and the only files here a tool may edit.

| document | its job |
| --- | --- |
| [`open-findings.md`](open-findings.md) | **every finding currently reported**, one row each, plus the ones already ruled on. *Additive* — see the caution below |
| [`corpus.md`](corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |

> **`open-findings.md` is not like the other two.** They are rewritten whole, so
> anything typed into one is lost on the next run. It is *additive*: the
> generator adds rows and never removes or rewrites one, so the notes column,
> the verdicts and the *Closed* table are all written by hand and all survive.
> The asymmetry is deliberate — a generator that could delete could quietly
> delete a regression.

`report/` holds documents rendered for an audience that will not clone this
repository, currently [`cpc-audit.html`](report/cpc-audit.html). They restate
findings from the sources above rather than adding any, so nothing is filed
twice. The generators are in [`../tools/`](../tools), and each says at the top
of the file what it writes and what it refuses to do.
