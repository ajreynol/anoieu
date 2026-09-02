# The documentation

**Thirty documents and about 18,700 lines**, which is more than the *one
obvious place per question* this page was built on, and is being looked at.
Seven of them are the written core listed below and the rest are named further
down. **Which of them are load-bearing is not currently known**, and a tool to
measure that has been requested. If you are looking for content rather than for where
content lives, every row below leads somewhere better.

## Written

| document | its job |
| --- | --- |
| [`reports.md`](reports/reports.md) | **what anoieu has to say about other people's code**: what it is asking of each project, how each finding was confirmed, and what came back when it was filed |
| [`reporting-policy.md`](reports/reporting-policy.md) | **what may be published about somebody else's code, and why.** The position anoieu shares with [dokimasia](https://github.com/ajreynol/dokimasia) — twelve of them, each saying whether it is enforced, structural, or an intention nothing but our record backs |
| [`reporting-workflow.md`](reports/reporting-workflow.md) | **how a finding is handled**: the conventions governing the record, the workflow and prompts for carrying one to whoever can fix it, and for
sweeping the whole report, and what it takes for another repository to run these checks in its own CI |
| [`usage.md`](usage.md) | **the analyzer's interface.** What the tool takes, what every command and option means, and how configuration, baselines and suppression fit together. The *person's* interface to this repository is [`interface.md`](interface.md), below |
| [`fuzzing.md`](fuzzing.md) | **the other half**: the anoieu fuzzer, which writes Eunoia nobody would write and hands it to a checker. What its oracle is, how a case is shrunk, bucketed and promoted into a finding, how to point it at a third checker, and what it is deliberately not: a baseline, whose research-quality successor nobody has started |
| [`notes.md`](notes.md) | **the miscellany**: what ethos misses and why, what we have established about `.eo` and `.eos`, and the design — what is built, what was rejected, what is open. Anything that does not belong in the six above belongs here |

## Demoted

**[`misc/`](misc/) is where a document goes when cleaning it up properly would
cost more than it is worth today** — see `PROTO-22` in
[`coherence.md`](coherence.md). Still maintained, still linked, still checked;
what changes is that it is no longer offered as one of the places a question is
answered. **The practice is discouraged and a growing `misc/` is a symptom.**

| document | its job |
| --- | --- |
| [`ai-novelty.md`](misc/ai-novelty.md) | the mechanics of why this arrangement works, and a worked example of one refactor. Demoted 2026-09-02 |
| [`linker.md`](misc/linker.md) | the workflow resolved to where each rule is defined, for an agent to load. Demoted 2026-09-02 |
| [`methodology.md`](misc/methodology.md) | how a practice reaches somebody else's tree, and at what rate. Demoted 2026-09-02 |

## Generated

Written by a run, and the only files here a tool may edit — **except one.**
`closed-findings.md` sits in this table because it lives with the others and is
hand-maintained; being in this section is what once made it look disposable.

| document | its job |
| --- | --- |
| [`open-findings.md`](reports/open-findings.md) | **every finding currently reported**, one row each. *Additive* — see the caution below |
| [`closed-findings.md`](reports/closed-findings.md) | **internal, and NOT generated** — it is written by the review step and only *read* by the generator, which skips every id in it. **It is the ledger of verdicts and cannot be reconstructed**: delete it and every settled finding is reported to its project again, including the ones somebody already declined. It is listed here because it lives beside the other two, and `tools/policy_check.py` deliberately leaves it out of its generated list |
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

[`interface.md`](interface.md) is not in the table and is the page to read
**first if you are the person driving this repository** rather than reading about
it. What to say, what comes back, what never comes back, and the decisions that
are nobody's but yours. Its stated default — *work with anoieu to develop the
next stretch* — is a **conjecture about the right level of abstraction**, said so on
the page, with what would show it wrong and five other levels to drop to,
including the two where anything actually gets built. Distinct from
[`usage.md`](usage.md), which is the analyzer's command line, and from
[`coherence.md`](coherence.md), which is the standards the work is held to.

[`laws.md`](laws.md) is the rules for keeping [`history.md`](history.md) and
nothing else: who may write it, what a stretch entry must contain, and what
travels when the presidency changes hands. **They are candidate laws** —
written down, followed voluntarily, enforced by nothing — because the party they
bind also wrote them. A tool should hold this page eventually.

[`history.md`](history.md) is **what previous presidents did, and what the
current one is doing** — one section per stretch, oldest first, and no
procedure. Each names the **president** first, because a page about what
happened should say who was responsible for it, and carries how long the stretch
ran, who entered the ecosystem, what was committed and whether the build was
green. Distinct from [`report-card.md`](report-card.md), which grades, and from
[`postmortem.md`](reports/postmortem.md), which asks what one run of the
reporting loop cost. **It travels with the office; the report card does not.**

[`instructions.md`](instructions.md) is the other half of that page, and is
the only document here **addressed to you rather than to whoever maintains
this**. Where [`interface.md`](interface.md) tells an agent how to behave, this
tells the human — the person at the terminal — what is theirs to do, and it is
held to one rule the rest of the documentation is not: an instruction that
cannot be followed without first opening a file has failed. There is one so
far, about the hours you intend to work.

[`epoch-analogy.md`](epoch-analogy.md) is the shortest way in if the two below
look like a lot: the epoch build system mapped onto an ordinary build system —
sources, a dry run, a gate, an exit code, a version — and then the longer half,
**where the analogy stops being flattering**. A build is a function and this is
not; nothing type-checks; there is no linker; and `deployed` is not `installed`,
because every downstream effect is somebody else's voluntary act.

[`stretch-policy.md`](stretch-policy.md) and [`stretches.md`](stretches.md) are a pair and
are not in the table either. A **stretch** is the span between one global
announcement and the next. The policy says what one is, what counts as a major
event within it — a global announcement, and **a role changing hands**, which is
the one a reader reconstructing history from commits will not see — and what
*designing the next stretch* involves, which is a role here and is destined for the
governance repository. The log is the other half and is **the one document here
allowed to be out of date**: the covering note recommended for handing each
announcement downstream, with the wording that was rejected, which is the part
worth keeping. Nothing checks the log and a stale prompt in it is a record rather
than a defect. Which repositories are actually contacted, and whether any are, is
a person's decision: see *Who gets pinged* in
[`policy.md`](policy.md#who-gets-pinged).

[`methodology.md`](misc/methodology.md) is the **distribution mechanism**: how a
practice gets from this repository into a tree whose owner did not write it, and
at what rate. The worked case is the one thing here that has actually crossed
the boundary — the policy checker, fetched at a commit a member pins and runs
against its own tree — and the rest is what generalising that to a command line
would take, as a checklist rather than a plan. Nothing of it is built beyond the
one program, and the page says so.

[`science-fiction.md`](science-fiction.md) is **experimental** and is the only
page here that sets a limit rather than a direction: **the furthest this
ecosystem allows itself to plan**, with the contradiction against
[`vision.md`](vision.md) stated rather than smoothed over — the vision governs
direction and speed, this governs range, and where they conflict the vision
wins. Two scenarios, each ending in what it *forbids* rather than what it
enables, and one dated piece of evidence: the first outside approach this
ecosystem has received, why it is only a candidate for that, and why the posture
toward it is distrust regardless of who is behind it.

[`linker.md`](misc/linker.md) and [`ai-novelty.md`](misc/ai-novelty.md) are
**experimental and new**, a pair, and in the table above least of all. The
first is every rule this repository holds, each resolved to the file that
defines it and none of them restated — one page an agent can load before
starting work, so that the corpus gets read on demand rather than in advance.
It is derived and never authoritative: where a line disagrees with the file it
names, the file wins. The second is the account of why an artifact of that
shape is worth having — what the moving parts are and why each is shaped the
way it is, with what would show each claim false. Neither governs anything,
nothing consumes either, and both say on the page what would show they are not
worth keeping.

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
[`../prompts/`](../prompts) holds the ones that hand context to
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
