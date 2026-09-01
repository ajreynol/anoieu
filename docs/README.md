# The documentation

Seven documents, so that a question has one obvious place to be answered, plus
the files a run generates. If you are looking for content rather than for where
content lives, every row below leads somewhere better.

## Written

| document | its job |
| --- | --- |
| [`reports.md`](reports/reports.md) | **what anoieu has to say about other people's code**: what it is asking of each project, how each finding was confirmed, and what came back when it was filed |
| [`reporting-policy.md`](reports/reporting-policy.md) | **what may be published about somebody else's code, and why.** The position anoieu shares with [dokimasia](https://github.com/ajreynol/dokimasia) — twelve of them, each saying whether it is enforced, structural, or an intention nothing but our record backs |
| [`reporting-workflow.md`](reports/reporting-workflow.md) | **how a finding is handled**: the conventions governing the record, the workflow and prompts for carrying one to whoever can fix it, and for
sweeping the whole report, and what it takes for another repository to run these checks in its own CI |
| [`usage.md`](usage.md) | **the interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together |
| [`fuzzing.md`](fuzzing.md) | **the other half**: the anoieu fuzzer, which writes Eunoia nobody would write and hands it to a checker. What its oracle is, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker, and what it is deliberately not: a baseline, whose research-quality successor nobody has started |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the six above belongs here |

## Generated

Written by a run, and the only files here a tool may edit.

| document | its job |
| --- | --- |
| [`open-findings.md`](reports/open-findings.md) | **every finding currently reported**, one row each. *Additive* — see the caution below |
| [`closed-findings.md`](reports/closed-findings.md) | **internal**: every row already ruled on, and the verdict against it. What stops a settled finding being listed again |
| [`corpus.md`](reports/corpus.md) | **what was measured, and what the checks reported on it**: the commits each project was restored to, and the counts taken from them. *Rewritten whole* |
| [`checks.md`](checks.md) | **one page per check** — what it reports, what it assumes, and what it deliberately does not. Rendered from the registry, so a page cannot drift from the code beside it. *Rewritten whole* |

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

Two more govern **how the work is done** rather than what it found, and are
written for every repository in the Eunoia ecosystem rather than only this one.
They live here because a governing document filed beside the code is one
somebody has to know to look for.

| document | its job |
| --- | --- |
| [`policy.md`](policy.md) | **how a repository is arranged**: the layout, the maintenance note every README ends with, and the rules for child projects. Machine-checked by `tools/policy_check.py` on every push |
| [`vision.md`](vision.md) | **what AI-assisted development is aiming at**: six tenets, and the record of what the ecosystem's tools have actually delivered to one another. Argued, never checked — the dividing line is stated on the page |
| [`report-card.md`](report-card.md) | **how each tool stands against those tenets**, in the register its own README chooses, graded at the commits the lock records. Governed by `vision.md` and split out of it because it is the half that moves — a paragraph is still changed by a person, and it binds nobody |

[`discussion.md`](discussion.md) is the standing channel to the rest of the
ecosystem for anything that is **not** a defect report — a request, a proposal,
a question about somebody's intent, a notice that something here is moving under
them. Its format, and the reason it is kept apart from the findings ledger, are
in [`policy.md`](policy.md#the-discussion-file).

`python3 tools/ecosystem.py` prints the ecosystem as a table — who is in it,
whether each passes the policy check, and how long since anything moved. Local,
about a second, no assistant involved.

[`../scripts/install_eo`](../scripts/install_eo) is the same ecosystem from the
other side, and the first command to run on a new machine: it clones the rest of
the ecosystem into siblings of this checkout. `--dry-run` prints exactly the
commands a run would execute — only `git clone`, which the suite checks — and
`--status` reads the rows back off the disk and says what has drifted. Its options are in
[`usage.md`](usage.md#the-rest-of-the-ecosystem), and the sequence for adding a
tool to the list is in
[`coherence.md`](coherence.md#what-happens-when-we-add-a-new-tool-to-the-ecosystem).

[`board.md`](board.md) is not in the table above either: it is **what is
outstanding across the ecosystem, in priority order** — at most twenty items,
each with the next thing to do, the repositories involved, and a prompt for each
of them. It is kept by hand, `HUMAN FEEDBACK` on an item outranks everything else
on it, and nothing consumes the file yet.

[`epoch-policy.md`](epoch-policy.md) and [`epochs.md`](epochs.md) are a pair and
are not in the table either. An **epoch** is the span between one global
announcement and the next. The policy says what one is, what counts as a major
event within it — a global announcement, and **a role changing hands**, which is
the one a reader reconstructing history from commits will not see — and what
*designing the next epoch* involves, which is a role here and is destined for the
governance repository. The log is the other half and is **the one document here
allowed to be out of date**: the covering note recommended for handing each
announcement downstream, with the wording that was rejected, which is the part
worth keeping. Nothing checks the log and a stale prompt in it is a record rather
than a defect. Which repositories are actually contacted, and whether any are, is
a person's decision: see *Who gets pinged* in
[`policy.md`](policy.md#who-gets-pinged).

[`roles.md`](roles.md) is the companion to it and is not in the table either:
**one entry per responsibility**, each with a permanent id, what it owns, and —
the field that does most of the work — the nearest thing that is *not* it. The
page is stratified by the tool that holds each one, and no role is too small: a
clear seam between two responsibilities is worth more than a short page, so a
long section is a measurement rather than an untidiness, and an empty one is a
tool looking for work. Within a section position is the priority; across
sections nothing is ranked. The board says what is outstanding and in what
order; this says what everything is for. It also carries the procedure for
handing a role from one tool to another — proposed on the board so the
repositories it costs something can disagree with it, and gating nothing while
the ecosystem is still settling. Kept by hand, and nothing consumes it either.

[`coherence.md`](coherence.md) is not in the table above and is not written for
a reader of the tool: it is the **maintenance entry point**, for whoever is
doing the work. What this repository is responsible for, which documents may not
be changed without asking, and the open technical work on the record itself.

[`../scripts/`](../scripts) holds the commands that run something —
`install_eo`, `status_eo`, `harvest_cpc_proofs` — and
[`../scripts/prompts/`](../scripts/prompts) holds the ones that hand context to
an assistant: starting a tool, welcoming it, joining, working correspondence, and
carrying findings both ways. The directory is the whole of the distinction, and
it is there so that running something never means deciding whether to spend a
turn. **The table of what each one does, and where it is run, is in
[`coherence.md`](coherence.md#the-scripts)**, which is also where a new one has to
be listed. The prompts are the workflow and the scripts are a way of running
them: [`reporting-workflow.md`](reports/reporting-workflow.md#the-workflow) and
[`policy.md`](policy.md#joining-the-eunoia-ecosystem) are the documents that
define them, and `tests/run.py` fails when a script's copy of a prompt has
drifted from the document it came from.

`reports/` also holds documents rendered for an audience that will not clone this
repository, currently [`cpc-audit.html`](reports/cpc-audit.html). They restate
findings from the sources above rather than adding any, so nothing is filed
twice. The generators are in [`../tools/`](../tools), and each says at the top
of the file what it writes and what it refuses to do.
