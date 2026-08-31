# The documentation

Seven documents, so that a question has one obvious place to be answered, plus
the files a run generates. If you are looking for content rather than for where
content lives, every row below leads somewhere better.

## Written

| document | its job |
| --- | --- |
| [`philosophy.md`](philosophy.md) | **what may be published about somebody else's code, and why.** The position anoieu shares with [dokimasia](https://github.com/ajreynol/dokimasia) — anoieu maintains it, dokimasia references it — including what "maintained by AI under light supervision" does and does not cover |
| [`reports.md`](reports.md) | **what anoieu has to say about other people's code**: what it is asking of each project, how each finding was confirmed, and what came back when it was filed |
| [`reporting-policy.md`](reporting-policy.md) | **how a finding is handled**: the conventions governing the record, the workflow and prompts for carrying one to whoever can fix it, and for
sweeping the whole report, and what it takes for another repository to run these checks in its own CI |
| [`usage.md`](usage.md) | **the interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together |
| [`fuzzing.md`](fuzzing.md) | **the other half**: the anoieu fuzzer, which writes Eunoia nobody would write and hands it to a checker. What its oracle is, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker, and what it is deliberately not: a baseline, whose research-quality successor is one of the future projects in [`why-eunoia.md`](why-eunoia.md#six-projects-that-do-not-exist-yet-and-change-the-picture) |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the six above belongs here |

## Generated

Written by a run, and the only files here a tool may edit.

| document | its job |
| --- | --- |
| [`open-findings.md`](open-findings.md) | **every finding currently reported**, one row each. *Additive* — see the caution below |
| [`closed-findings.md`](closed-findings.md) | **internal**: every row already ruled on, and the verdict against it. What stops a settled finding being listed again |
| [`corpus.md`](corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |

> **The two findings files are not like the others.** `corpus.md` and
> `checks.md` are rewritten whole, so anything typed into one is lost on the next
> run. The findings files are *additive*: the generator adds rows and never
> removes or rewrites one, so the notes column and every verdict are written by
> hand and all survive. The asymmetry is deliberate — a generator that could
> delete could quietly delete a regression.

[`postmortem.md`](postmortem.md) is what running that workflow once actually
taught us: the log of one project's twenty rows, what the assistant at the far
end got right and wrong, what we got wrong, and the two rules the round
established — that each round leaves the prompts *shorter and clearer*, and that
a person approves every change to one.

[`../scripts/`](../scripts) holds one implementation of the workflow
[`reporting-policy.md`](reporting-policy.md#the-workflow) defines: `check_anoieu`
to run in the project a finding is about, `process_anoieu` here once it has
replied. The prompts are the workflow; the scripts are a way of running them,
and `tests/run.py` fails when their copy of the text has drifted from it.

`report/` holds documents rendered for an audience that will not clone this
repository, currently [`cpc-audit.html`](report/cpc-audit.html). They restate
findings from the sources above rather than adding any, so nothing is filed
twice. The generators are in [`../tools/`](../tools), and each says at the top
of the file what it writes and what it refuses to do.
