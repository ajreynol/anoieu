# The register of shortcomings

**Every place where our own record cannot support a claim we make about our own
conduct.** Newest last, ids permanent, and a finding leaves this page only when
the artifact named in **What would settle it** exists.

This is the first goal of [`README.md`](README.md) and the only part of this
project that exists. It is a register of *gaps*, not of wrongdoing: an entry
here says that a claim cannot be checked, never that it is false. The difference
matters, because a project that cannot tell those apart will eventually
manufacture the second in order to have something to say.

Each entry carries the same five fields, in the same order:

| field | what it holds |
| --- | --- |
| **What** | the claim we make, and the gap under it. One line |
| **Evidence** | what in the tree shows the gap. A path, a printed line, a commit |
| **Why it is ethical and not only technical** | the part that earns it a place here rather than on the board |
| **What would settle it** | the artifact that would let an outsider check the claim. Usually absent |
| **State** | `open`, `partly answered`, or `settled` — with what changed |

---

## F1 — the record accounts for what we produced and not for what we were asked

**What:** this repository keeps an unusually complete account of its outputs —
every commit, every finding with an id, every verdict with its evidence, logs
that are appended to and never rewritten. **It keeps no account of its inputs.**
The prompts a person actually typed, turn by turn, are not tracked and never
were.

**Evidence:** [`../../docs/interface.md`](../../docs/interface.md) already
concedes it, in the sequence describing how a tool starts: *a person points it
in a direction, with whatever prompts that takes. This step is invisible
afterwards — it leaves no artifact — which is worth remembering when reading the
result.* The templates under `scripts/prompts/` are drift-checked against the
documents that define them, which covers the prompts we **publish** and none of
the prompts we **use**.

**Why it is ethical and not only technical:** the technical form is small — a
log nobody set up. The consequence is not. This repository's whole claim on
being believable is that its history can be walked backwards, and the walk stops
one step short of every cause. Read the git log and you can establish what was
done and never why, or by whom at whose instruction. **So the setup does not
provide a complete scientific account of what we did** — it provides a complete
account of what came out. For an ecosystem that has just written down that a
joint history is the evidence an ethical claim usually lacks, the hole is at
precisely the point where the claim needs to be strongest: we are asking others
to be checkable against a standard our own record cannot meet.

It also weakens the two things this repository says most often about agents.
*An agent under light supervision* is a claim about a ratio nobody can compute
from the tree. *A person approves every prompt change* is checkable for the
templates and unfalsifiable for the sessions.

**What would settle it:** a tracked, append-only record of the prompts that
drove each session — what was asked, when, and by whom — committed alongside the
work it produced, with whatever redaction a person decides on **stated as a
policy rather than applied silently**. Nothing like it exists. The honest
intermediate is smaller and worth more than nothing: a per-stretch note of what
a person actually asked for, written at the time rather than reconstructed.

**State:** **open.** Raised by the maintainer, 2026-09-02, as the finding that
started this project.

## F2 — our strongest claims are about things we did not do

**What:** the conduct this ecosystem is proudest of is refusal. No repository
was created. Nothing was pushed. No remote was written to. No discussion file
was acted on unbidden. No prompt was sent that a person had not approved.
**Every one of those is a claim that something did not happen, and nothing in
the tree can witness a non-event.**

**Evidence:** the checker says so itself, on every run, in its own printed list
of what it cannot decide: *nothing leaves the island by machine — absence of an
action cannot be observed here.* That line was written as a limit on one rule.
It is a limit on most of our ethical claims.

**Why it is ethical and not only technical:** this is the exact shape of claim
that outsiders are right to discount, and the discount is not unfair. Anybody
can say what they refrained from. The asymmetry is uncomfortable when set beside
what we ask of others — a member's compliance is decided by a program run
against their tree, while our own best conduct rests on nobody having found a
counter-example. **We hold others to what can be checked and ourselves to what
cannot.**

**What would settle it:** partially, and only partially — a refusal that is
*recorded when it is made* rather than inferred from silence. A declined action
with a date and a reason is an artifact; a clean history is not. The
capability boundary helps here in a way it does not elsewhere: the acts we
forbid ourselves are ones that leave traces **in somebody else's tree**, so
their absence is checkable by a third party in a way our internal restraint is
not. That is the strongest available answer and it is still not proof.

**State:** **open.** Raised 2026-09-02, in the course of writing `F1`.
