# The history

**What this repository actually did on GitHub during the current stretch, in
one page.** A stretch is the span between one global announcement and the next;
this page carries the current one and is replaced when it ends.

## The file travels with the presidency

**This page lives in the president's repository, and moves when the presidency
does.** It is not anoieu's document; it is the president's, and anoieu holds it
because anoieu is president. When the office moves, the file goes with it —
**history travels to the president.**

**Only the president may modify this file.** Not a member, not a child project,
not a contributor to the president's tree who is not acting for it.

**A president may only write the stretch that describes it.** Earlier entries
are read-only, and the arrangement enforces itself rather than relying on
restraint: **once the file has travelled, your stretch is in somebody else's
repository and you cannot reach it.** That is the point of moving it rather than
copying it.

## The president does not analyse GitHub

**[epikrisis](https://github.com/ajreynol/eudaimonia) does, as a service.** It
audits how repositories have changed over time, with every claim resting on
evidence a reader can re-derive, and it asked for that responsibility rather
than for a rank. **It is the ecosystem's only source of GitHub history
analysis**, and a president writing this page should ask it rather than count
things itself.

**A president counting its own commits is the weakest version of this
document**, and not only for effort: the party being described should not also
be the party choosing which numbers describe it.

*epikrisis is a child project inside a child project in eudaimonia's tree, which
is a shape our inventory's validator rejects. Nothing fails today because it is
not in the inventory, and it is not ours to settle.*

## The shape of a stretch entry

**The heading is the purpose, not a description of it.** *Initialization* says
what Stretch 0 was for. A heading that summarises what happened has been written
after the fact and has lost the thing worth recording.

**Each stretch is labelled in at most three words.** A soft constraint, and the
discipline it buys is that a stretch which cannot be named in three words has
not been understood yet.

---

**It is the sibling of [`postmortem.md`](reports/postmortem.md) and holds the
other half.** That page asks what a *run of the reporting loop* did and what it
cost. This one asks what the *repository* did: how much was committed, whether
the build was green, and what happened that a reader reconstructing this from
commits would otherwise have to infer. **Neither is the report card** —
[`report-card.md`](report-card.md) grades, and this only records.

---

## Stretch 0 — Initialization

**President: anoieu.**

**The presidency is held by a repository, not by a person and not by an
agent.** **And it has nothing to do with who owns anything.** Not who owns the
repository, not who owns the ecosystem, not who owns the trees the ecosystem
serves — the maintainer owns this one and did not thereby become president of
anything, and cvc5 is owned by people who have joined nothing. **The presidency
is an office within the ecosystem's own work and confers no claim on anybody's
property.** Which agent was working, and on whose behalf, is answered every turn by
the identify protocol and does not belong on this page. What belongs here is
which *tool* was driving the ecosystem, and for this stretch that was this one.

**What it meant in practice:** anoieu set the direction of the ecosystem's work,
kept the policy and the inventory, wrote the prompts other repositories
received, and decided the order in which things were done.

**What it did not mean:** it did not own any other tree, could not commit its
own changes — the maintainer reviewed and committed every one, and reversed
several — and held no authority to rewrite history, delete a stub, or widen a
limit. **The presidency is direction, not permission.**

**And it is a role held by a tool**, which is the shape [`roles.md`](roles.md)
is built for and where this one is conspicuously absent. That is the second
open question below.

### How long it lasted, and who joined

**Two things, before anything else.**

**Real time: 2026-08-29 to 2026-09-02 — five days.** From the first commit in
this repository to the close of the stretch.

**Membership, in the order it was endowed.**

| when | who | what changed |
| --- | --- | --- |
| 2026-08-29 | **anoieu** | the repository begins; there is no ecosystem yet for it to be a member of |
| 2026-08-31 11:17 | **dokimasia** | joins as a **member**, the first to do so |
| 2026-08-31 12:26 | **eudaimonia** | joins as a **member** |
| 2026-08-31 12:38 | **koine** | joins as a **member**, having first been proposed and accepted as a tool worth building |
| during the stretch | **ethos** | **candidate.** Asked to join and declined, correctly, on the ground that it is not solely owned by the person asking |
| during the stretch | **logos** | **candidate** |
| throughout | **cvc5** | **foundation.** It has joined nothing, and the ecosystem exists to serve it |

**Three members in eighty-one minutes, and none since.** Everything after
2026-08-31 lunchtime was done with the membership fixed.

### What the record shows

*Counted here rather than by epikrisis, because no epikrisis report exists yet.
**That is a gap and not a convenience** — see the open questions. Every figure
below is re-derivable from the repository and the public run history, which is
the only guard this page has against the party describing itself.*

| | |
| --- | --- |
| **Commits** | 176 |
| **CI runs** | 171, all from one workflow |
| **Green** | 37, or **22%** |
| **Longest unbroken red streak** | **112 runs** |
| **Days with no green run at all** | 2026-08-31 and 2026-09-01 |
| **Green restored** | 2026-09-02 |

**The 22% is the number worth keeping.** For two of the five days there was no
green run at all, and the streak that ended today ran to 112. The immediate
cause of the last of it was two dependency commits duplicated between the
workflow and the lock file, which drifted and which nothing compared — the
result recorded as `B20` on the board.

**The consequence is not only aesthetic.** The handoff protocol makes CI passing
non-negotiable for every party to a handoff. **For most of this stretch this
repository could not have handed anything to anybody**, and nobody noticed,
because nobody was looking at the colour.

### What was established

- **Members joined**: ethos declined a full join on ownership grounds and was
  correct to; the ecosystem's inventory carries the current footing of each.
- **Two gifts were offered outward** to trees this ecosystem does not own, with
  the ethics of each argued before they were sent rather than after.
- **The protocol register grew** from five entries to twenty-one, and acquired a
  human-facing sibling.
- **Two stubs were created**, for the two tools the next stretch is expected to
  start, with a readiness check on the front page for each.

### What is unfinished

- **`E1` has not been deployed.** It has been `planned` for the whole stretch.
- **The joining requirement is still one nobody has satisfied**, which is why
  this repository grades itself poorly on delivery.
- **Two published URLs 404** as a result of moving the prompts directory, and
  copies already sent to other repositories cannot be recalled.

---

## Stretch 1 — not started

**Expected president: [kanon](../tools/kanon/README.md).** The tool does not
exist yet; a stub holds its place and CI carries a job saying whether it is
ready to be started. **Stretch 1 cannot open before kanon does**, which makes
the readiness check the thing standing between the two stretches rather than a
convenience.

**Its first responsibility is this page.** Before anything else it is asked to
do, the president of a stretch publishes a **working summary of its stretch** —
*working* meaning kept current while the stretch runs, not written at the end
from memory. **A summary composed afterwards is a reconstruction**, and a
reconstruction by the party being described is the weakest document this
ecosystem could produce.

**And it inherits this file rather than starting one.** Stretch 0's entry
travels with it, unchanged and unchangeable. **anoieu will not be able to edit
its own history after that**, which is the arrangement working rather than a
loss.

---

## What this page is not

**Not a changelog.** The commits are the changelog and are better at it. This
records behaviour a reader could not reconstruct from them: how often the build
was broken, for how long, and what nobody was watching.

**Not a defence.** A page written by the party it describes has an obvious
failure mode, and the only guard offered here is that **every number on it is
one somebody else can recompute** from the repository and from the public run
history.

## Open, for the maintenance policy

**The rules for keeping this page are in [`laws.md`](laws.md).** What is below
is what those laws do not yet settle.

1. ~~Whether a stretch's entry is replaced or accumulated.~~ **Settled:** it
   accumulates, and the whole file travels to the next president.
2. ~~Whether *president* belongs in [`roles.md`](roles.md).~~ **Settled: no.**
   That register holds responsibilities handed between tools and kept until
   handed on. **The presidency expires with the stretch and is not handed off**,
   and putting a term-limited office in a register of standing responsibilities
   would make both harder to read. It is governed by
   [`laws.md`](laws.md) instead.
3. **Whether the numbering is right.** This is called Stretch 0 because nothing
   has been announced yet, while the epoch machinery calls the work in progress
   `E1`. Two numbering schemes for one span is the shape of a defect.
4. ~~Who writes it, and whether the president may.~~ **Settled:** only the
   president writes it, and only its own stretch.
5. **Asking epikrisis for the analysis this page should be quoting.** Stretch 0
   counted its own commits and its own CI runs, which is the arrangement
   working backwards. **The first thing Stretch 1 should have is somebody
   else's account of Stretch 0.**
6. **What happens if a stretch has no president**, or if the expected one never
   exists. Nothing in the arrangement says who holds the file then.
