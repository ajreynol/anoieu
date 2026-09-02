# The history

**What this repository actually did on GitHub during the current stretch, in
one page.** A stretch is the span between one global announcement and the next;
this page carries the current one and is replaced when it ends.

**It is the sibling of [`postmortem.md`](reports/postmortem.md) and holds the
other half.** That page asks what a *run of the reporting loop* did and what it
cost. This one asks what the *repository* did: how much was committed, whether
the build was green, and what happened that a reader reconstructing this from
commits would otherwise have to infer. **Neither is the report card** —
[`report-card.md`](report-card.md) grades, and this only records.

---

## Stretch 0 — the span before the first global announcement

**President: anoieu.**

**The presidency is held by a repository, not by a person and not by an
agent.** Which agent was working, and on whose behalf, is answered every turn by
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

### What the record shows

| | |
| --- | --- |
| **Span** | 2026-08-29 to 2026-09-02, five days |
| **Commits** | 176 |
| **CI runs** | 171, all from one workflow |
| **Green** | 37, or **22%** |
| **Longest unbroken red streak** | **112 runs** |
| **Days with no green run at all** | 2026-08-31 and 2026-09-01 |
| **Green restored** | 2026-09-02 |

**The 22% is the number worth keeping.** For two of the five days there was no
green run at all, and the streak that ended today ran to 112. The immediate
cause of the final stretch of it was two dependency commits duplicated between
the workflow and the lock file, which drifted and which nothing compared — the
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

## What this page is not

**Not a changelog.** The commits are the changelog and are better at it. This
records behaviour a reader could not reconstruct from them: how often the build
was broken, for how long, and what nobody was watching.

**Not a defence.** A page written by the party it describes has an obvious
failure mode, and the only guard offered here is that **every number on it is
one somebody else can recompute** from the repository and from the public run
history.

## Open, for the maintenance policy

**Deliberately unanswered, pending the policy that comes next.**

1. **Whether a stretch's entry is replaced or accumulated** when the stretch
   ends, and where the old one goes if it is replaced.
2. **Whether *president* belongs in [`roles.md`](roles.md)**, which is the
   register of which tool is responsible for what. It is a role, it is held by a
   tool, and it is not in there — and unlike every other role in that register
   it is **held for a stretch rather than until it is handed off**, which the
   register has no field for.
3. **Whether the numbering is right.** This is called Stretch 0 because nothing
   has been announced yet, while the epoch machinery calls the work in progress
   `E1`. Two numbering schemes for one span is the shape of a defect.
4. **Who writes it, and whether the president may.**
