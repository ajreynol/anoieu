# Coherence

**If you are an agent working on this repository, start here.** This is the
maintenance entry point: what this repository is responsible for, which of that
may not be changed without asking, and what the open technical work is. Read it
before editing anything; everything else is reachable from it.

It is deliberately **not linked from the front page**. `README.md` is for
somebody deciding whether the tool is worth their attention, and a page about
how the work is run is noise to them — see *The front page* in
[`../tools/vision.md`](../tools/vision.md). It is linked instead from the things
an agent actually opens: [`../CLAUDE.md`](../CLAUDE.md), and the headers of the
programs that write the record.

*Coherence* is the property this page exists to protect, in one sentence: **the
record, the documents and the tree do not disagree with each other.** A finding
that is open in one file and closed in another, a verdict resting on a fix that
never landed, a document describing an arrangement the code stopped using — each
is a coherence failure, and each has happened here.

## What this repository is responsible for

Six things, and only two of them are the tool.

| what | where | who else it binds |
| --- | --- | --- |
| the analyzer | [`../anoieu/`](../anoieu) | anyone running it; the baselines other repositories would gate on |
| the fuzzer, a **child project** that has earned its keep | [`../tools/anoieu_fuzz/`](../tools/anoieu_fuzz) | its `FUZ` rows are in the record and two CI steps run it — see rule 10 of [`../tools/policy.md`](../tools/policy.md) |
| **the publishing position** | [`reporting-philosophy.md`](reporting-philosophy.md) | maintained here, **referenced by [dokimasia](https://github.com/ajreynol/dokimasia)** rather than copied |
| **the reporting workflow** | [`reporting-policy.md`](reporting-policy.md) | [`../scripts/`](../scripts) implement it; other repositories adopt its CI half |
| **the development vision** | [`../tools/vision.md`](../tools/vision.md) | written for *every* repository in the ecosystem |
| **the repository policy** | [`../tools/policy.md`](../tools/policy.md) | written to be copied; governs child projects in any parent |

The four in bold are **not about anoieu**. They are ecosystem documents that
happen to be maintained here, which has one consequence worth stating plainly:
editing one of them edits what other repositories are following, and the fact
that the file sits in this tree does not make the change local. That is the
whole reason the next section exists.

## The supervision ladder

Ordered, most supervised first. *Supervised* means: propose the change and the
reason, and wait for a person — do not make it and mention it afterwards.

**1. [`../tools/vision.md`](../tools/vision.md) — ask first, always.** It states
what AI-assisted development in this ecosystem is for, it is addressed to
repositories that did not write it, and the party with the least standing to
revise it is the agent it governs. This includes the report card at the bottom:
a paragraph there is a judgement about somebody else's project, and softening or
sharpening one is exactly the edit that should not be made quietly.

**2. [`../tools/policy.md`](../tools/policy.md) — ask before the rules.** The
numbered rules may be **appended** to, never renumbered, and retiring one in
place is a person's decision. The layout conventions are different in kind: when
the tree and the conventions disagree, correcting the *description* to match
what the tree actually does needs nobody, and changing the tree to match the
description is ordinary work.

**3. [`reporting-philosophy.md`](reporting-philosophy.md) — not yet stable, so
say what you changed.** Unlike the two above, this page is still settling: its
positions are being worked out rather than defended, and adding, sharpening or
retiring one is ordinary work rather than something to ask about first. Two
things still hold. Positions are **appended and never renumbered**, and are
cited by name, so a rewrite that renumbers is a defect however much better it
reads. And **dokimasia references this page rather than copying it**, so every
edit moves a second repository — which means changes get flagged to a person
even though they do not need permission, and a *structural* change (a position
retired, the page renamed again) is carried to dokimasia by hand.

> **Outstanding, from the rename to `reporting-philosophy.md`:** dokimasia's
> links to the old `docs/philosophy.md` are now dead. Nothing here fixes that —
> nothing crosses a repository boundary by machine — so it is a person's errand,
> and it is unfiled.

**4. [`reporting-policy.md`](reporting-policy.md) — ask before the prompts.** A
person approves every change to a prompt template, and each round should leave
the prompts *shorter and clearer* than it found them — that rule was itself
learned the expensive way and is written up in
[`postmortem.md`](postmortem.md). `tests/run.py` fails when a script's copy of a
prompt has drifted from the document, so the two move together or not at all.

**5. The generated documents — never hand-edited, ask about nothing.**
[`corpus.md`](corpus.md) and [`checks.md`](checks.md) are rewritten whole, so
anything typed into them is lost. [`open-findings.md`](open-findings.md) and
[`closed-findings.md`](closed-findings.md) are additive: the generator adds rows
and never removes or rewrites one, which is what keeps hand-written verdicts
alive. Closing a row is a judgement made by the review step, never by a diff.

**6. Everything else — ordinary work.** The README's results layer,
[`notes.md`](notes.md), [`usage.md`](usage.md), [`fuzzing.md`](fuzzing.md), the
code, the tests. No permission needed; the normal standard applies.

Two rules cut across the whole ladder.

**Weakening a claim needs nobody; strengthening one needs a person.** Adding a
caveat, narrowing a check that fired wrongly, or qualifying a result is ordinary
work to be done at once. Moving from *the fuzzer found a crash* to *the fuzzer is
ready for your CI* asks a reader to rely on something, and that is the human's
call — put the proposed wording and the evidence in front of them together.

**Work is left staged, not committed.** A person reviews the diff and commits.
This is not a formality: it is the last place where a change to a document that
binds another repository can be caught.

## The open technical work

**Planning only. Nothing below is built.**

The record is now edited mostly by an assistant: `scripts/process_anoieu` reads a
reply and moves rows, writes verdicts, narrows checks and appends to two logs.
That has already worked and has already gone wrong — a verdict of *fixed
upstream* was recorded three times for a fix that never happened, and nothing
noticed for months (see [`postmortem.md`](postmortem.md)). The question this
section is for is not *how do we stop an agent editing the record* but **what
must remain true of the record after any edit, whoever made it, and which of
those can a machine check.**

The eventual goal is that these hold in **anoieu's CI**, failing a build rather
than living in a document somebody is meant to have read. But most of them do
not need enforcing so much as *not offering the chance to get them wrong* — a
script the agent is told to use, rather than a table it edits. That is the
cheap route, it is written up after the list, and it is where to start. None of
this is built today.

### The properties we want

Grouped by what they protect. The right-hand column is the honest status.

| # | property | why | today |
| --- | --- | --- | --- |
| **C1** | **The log is append-only.** A run adds entries to [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) and [`postmortem.md`](postmortem.md); it does not rewrite what an earlier run wrote. | The log is the only account of what we believed and when. A log an agent may rewrite is a log that silently agrees with the present. | nothing checks it |
| **C2** | **Except to correct, and a correction is visible as one.** An earlier entry may be amended when it is *wrong* — not when it reads badly — and the amendment says so in place, keeping the original claim legible. | This round had to correct three verdicts and a false claim about the fuzzer's records. Forbidding that outright would have forced a knowingly false log. | done by hand, by convention |
| **C3** | **Every id that has ever appeared is accounted for, forever.** An id in [`open-findings.md`](open-findings.md) or [`closed-findings.md`](closed-findings.md) never leaves both; it is open, or closed with a verdict, and never absent. | The whole point of an id. A row that can vanish makes every earlier decision unverifiable. | the generator is additive and cannot delete, but nothing forbids a *hand* deletion |
| **C4** | **No id is in both files, and no id appears twice in either.** | Two states for one finding is a record that answers differently depending on where you look. | not checked |
| **C5** | **A closed row's verdict is re-derivable, or says why it is not.** A verdict of *fixed upstream* is a claim about a tree we have; it should carry the commit it was checked at, and a later run should be able to fail when the finding is still reported there. | This is exactly how three rows sat closed on a fix that never landed. | not checked; the highest-value gap |
| **C6** | **An id is stable under things that are not the finding.** Regenerating the CPC baseline this round changed every id, because the fingerprint moved with the path root when the entry point changed — the findings were identical. An id that moves when nothing about the finding moved silently invalidates every verdict recorded against it. | Decisions are recorded against ids. | **broken**, and [`reports.md`](reports.md#what-cvc5-asked-for-next) currently claims otherwise |
| **C7** | **A closure is traceable to its evidence.** Every verdict names the run, the reply, or the commit it rests on, so a reader can go from a closed row to why. | *"Because an assistant said so"* is not a reason, and today the link is prose in a log entry. | by convention |
| **C8** | **A finding reported to somebody is tracked until it is resolved**, including when the resolution is *declined*, *withdrawn*, or *reopened*. Reopening is a first-class transition, not an edit. | We reopened three rows this round and had to invent how. | ad hoc |
| **C9** | **A generated file is only ever written by its generator**, and a hand edit to one is a failure rather than a surprise on the next run. | `corpus.md` and `checks.md` say this in prose; nothing enforces it. | not checked |
| **C10** | **The record is coherent after every single row**, so a run that stops halfway leaves nothing half-moved. | Both follow-up prompts already promise this; nothing verifies it. | by convention |

### The cheap route, and probably the right one: a script

Most of the list above is only hard because the record is edited by hand — an
agent opening a Markdown table and moving a line. Give it **one command per
transition** and most of the properties stop being properties to check and
become things that cannot happen:

```
tools/ledger.py close  <id> --verdict "..." --evidence <commit|reply|run>
tools/ledger.py reopen <id> --because "..."
tools/ledger.py note   <id> "..."
```

The prompt then says *use this, do not edit the tables*, the same way it already
says *closing is moving a row, never deleting it*. What that buys, directly:

- **C3, C4** — the script is the only writer, so an id cannot be dropped or land
  in both files. It refuses rather than producing an incoherent record.
- **C1, C8** — it appends the log entry itself, from the same call that moves the
  row, so the log cannot disagree with the table and *reopen* is a real
  transition rather than a hand-edit that looks like any other.
- **C7** — `--evidence` is required, so a verdict without one is not expressible.
- **C10** — one row per invocation, and each invocation leaves the record whole.

This is not enforcement and does not pretend to be: an agent can still edit the
files directly, and a determined mistake gets through. That is the trade, and it
is a good one — it costs a day rather than a redesign, and it converts the
common failure (a well-meaning edit that leaves the record slightly incoherent)
into something that does not compile. **Do this before anything else here.**

### What still wants a check, script or not

Three, because no script can catch them:

- **C6, id stability.** Nothing at the call site knows the fingerprint moved.
  This is a defect in how an id is computed, and it is the one to fix outright
  rather than work around.
- **C5, a stale verdict.** *Fixed upstream* is a claim about somebody else's
  tree, and only a run against `deps/` can tell you it went false. The `corpus`
  job already has the tree; this is a step in it.
- **C2, C9 — a hand edit that bypassed the script.** A diff-shaped check against
  the previous commit, if it ever seems worth it. It probably does not until the
  script exists and is being used.

### Where the state should live — undecided, and a script postpones deciding

Today the state is two Markdown tables and two prose logs, with ids as the only
keys. Three options, none chosen:

- **Keep files, add the script.** Cheapest, and everything above except C5 and
  C6 is reachable from it. The limit is that a Markdown table has no
  transitions: *reopened* is indistinguishable from *was always open* except in
  the log the script wrote.
- **A tracker.** GitHub issues were the earlier plan
  ([`reporting-policy.md`](reporting-policy.md#medium-term-issues-on-our-own-repository)),
  and the constraints there still hold: issues live on *our* repository, a
  person posts, never an agent. The argument for one is not bookkeeping — it is
  that **findings do not all come from our checks.** Some will come from a
  person, from outside, or from a project telling us something is wrong with our
  own record, and those have no generated row to hang off. That is the case the
  file-based arrangement handles worst.
- **An internal store.** An append-only log of *events* — reported, replied,
  closed, reopened, corrected — with the Markdown rendered from it. The only
  option that makes C1 and C8 structural, and the most work. It also moves the
  record out of git diffs, which is most of what makes today's arrangement
  reviewable.

**The question to settle is not which of these**, but whether a finding is a
*row that changes state* or an *event log summarised into a row*. Everything
follows from that — and the script above is worth writing either way, because it
is the same interface in all three worlds.

## Where to start

1. Read this page, then [`reporting-policy.md`](reporting-policy.md#the-workflow)
   if you are working a finding, or [`notes.md`](notes.md#the-design) if you are
   working on the tool.
2. Check the ladder above before touching any document in it.
3. If the task is the record itself, the ledger script in *The cheap route* is
   the first thing to build and nothing above it is blocked on the rest.
4. Leave the work staged.
