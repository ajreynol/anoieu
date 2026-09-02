# Requests

Work the ecosystem wants that **does not obviously need a repository of its
own**. Newest first.

[`proposals.md`](proposals.md) audits one question — *should this become a
repository* — and answers it against a standard. Most wants are not that
question. They are a check somebody should write, a rule somebody should state,
a report nobody generates; the useful answer is usually *yes, and it belongs in
that tree over there*. Recording those in the proposals page would either inflate
them into repositories or lose them, and both have happened elsewhere.

What a request should arrive with is the same as for anything else registered
here, and *Best practices for requesting a listing* in [`tools.md`](tools.md) is
the one place it is written down.

So they are here, and the page tracks two things a proposal does not:

**Withdrawn ids stay listed.** `R6` — a research request on whether unambiguous
command syntax makes an ecosystem efficient — was raised and rolled back on
2026-09-02 as part of the work that produced `PROTO-17`. The number is retired
rather than reused.

**Where** — the tree it would live in, argued rather than assumed. A request
with no plausible home is a proposal in disguise and should be promoted.
**State** — `open`, `placed` (a repository has taken it), `promoted` (it turned
out to need its own tree, and is now a `P` in the proposals page), or `declined`,
with the reason.

**This page decides nothing either.** A request placed here is an argument that
somebody's tree should carry some work; whether it does is theirs. Nothing on
this page is a ticket in anybody's tracker, and nothing here is filed anywhere:
a request that a member should act on reaches them through
[`docs/discussion.md`](../../docs/discussion.md), by a person, or not at all.

## R7 — what does recency prove about a change?

**What:** the sibling question to `R5`. That one asks what cryptography can
establish about this arrangement; this asks **what a timestamp can.** The
specific claim to test: **work that happened in a short span has changed little,
so removing it is cheap — and the window closes.** If that holds, recency is
evidence and not merely context, and an ecosystem can use it to correct itself
without arguing every case on its merits.
**Where:** the interface protocols are anoieu's, so the subject is here.
**State:** **open.** Raised by the maintainer, 2026-09-02, out of a live case.

### The case that raised it

**Three commits over ten minutes, four files, and the direction was wrong from
the first one.** The person saw it before the agent did — the agent was inside
the frame — and each turn added structure that made the next correction more
expensive. The rollback was cheap **only because it was fast**, and nothing had
cited the work yet.

That is now `PROTO-17`, which says a person may stop a direction in one word and
that recency alone justifies removal. **The protocol is written; the claim under
it is not established**, and that is what this request is for.

### What it would ask

- **Is the claim true, and where does it stop?** *Recent means little was built
  on it* is plausible and has an obvious failure mode: a small recent change to
  a load-bearing page can be depended on immediately, and one to a page nobody
  reads can sit for months harmlessly. **Recency may be a poor proxy for what it
  is standing in for**, which is *how many things now rest on this*.
- **What is the better measure, and is it computable?** Inbound references to a
  change, whether another tree has pinned or fetched it, whether it has left
  this repository at all. Some of that is decidable from the trees; a history
  auditor already exists next door and reads exactly this kind of thing.
- **When does the window actually close?** The protocol says it does and does
  not say when. A first answer would be the moment a change is cited, pinned or
  published — all observable events rather than durations.
- **Does correcting quickly make an ecosystem faster or merely more anxious?**
  The efficiency claim is that a cheap interrupt beats a careful review. It is
  untested, and the opposite is available: an interrupt that fires easily
  produces work nobody trusts enough to build on.

### Why it is a sibling of `R5`

Both ask **what can be established about this arrangement from evidence rather
than from testimony**. `R5` asks it of identity and commitment; this asks it of
time. And both have the same honest shape today: a mechanism is in use, the
claim under it is unmeasured, and the ecosystem has been running on the
intuition.

**Neither should become a survey.** What is ours is the narrow question of what
*this* arrangement can prove about itself.

## R5 — a research project on cryptography in an AI-run ecosystem

**What:** where cryptographic primitives actually help an ecosystem like this
one, and where they are theatre. One sub-question is already settled and is
recorded below as the worked example of the answer being *no*.
**Where:** **a child project, and whose tree is the open part** — its live cases
sit in at least two trees, so siting it before scoping it would be guessing.
**State:** **open, and at brainstorming stage** — raised by the maintainer,
2026-09-02, and explicitly not a decision. This page decides nothing by
construction; what is written below is the shape of a question, and no part of
it has been adopted anywhere else.

### The settled part, first, because it is the cheapest thing to inherit

**Hiding how a report-card band is determined, so it cannot be gamed:
declined.** The want was real — a published rubric becomes a target, which
this ecosystem has already argued about somebody else's index. It was declined
because the thing it would hide is the thing that makes the page worth
anything: our sharpest criticism of that index was that **a score which cannot
be re-derived cannot be contested**, and encrypting our own basis would make
us that, deliberately, having said it aloud. In a public repository it is also
theatre — the key lives somewhere and the rule is inferable from enough
outputs.

**And the want dissolved rather than being refused.** The bands are not
computed, so there is no formula to encrypt and nothing to optimise against.
What survived was a smaller rule, already taken: **never publish a rubric, even
informally.**

### The open part, and it is not about hiding anything

**Attestation, where we currently have testimony.** The declaration that a human
has executed every push in these trees is the most load-bearing fact a history
analyser needs, and it is a **self-report**. Everything claimed here about
supervision reduces to who executed the irreversible step. **A signature would
make that evidence rather than testimony** — and the register holding it already
says it is the entry most likely to be superseded, with the supersession being
the point.

**Commitment, which is already in use here and not called cryptography.** A tool
in a neighbouring tree hashes its questions into a run **before the evidence is
seen**, so a question invented to fit an answer is visible afterwards. That is a
commitment scheme, in production, unnamed. **Noticing that we already depend on
one primitive is the cheapest start available** for a project about which others
would help.

**And one stated position that would need revisiting.** The build-system analogy
says outright that there is no signing here and no threat for it to address —
*one owner, one keyboard, nothing for a signature to distinguish.* True today,
and the exact sentence that stops being true the day an agent executes a push.

### What it must not become

**Not a survey of cryptography.** The literature is enormous and none of it is
ours; this ecosystem's rule is to take work from outside and cite it. What is
ours is the narrow question of which primitives change what *this* arrangement
can prove about itself.

**Not a secrecy project.** The decline above is the first thing it should read.

### A standing condition, and it closes recursively

**Anything concluded here must be kept current with the state of the field, and
a conclusion that has not been re-checked against current practice is void
rather than merely old.** Security work is the one subject in this ecosystem
where the *threat* moves independently of our tree: everything else goes stale
because we changed something, and this goes stale because somebody else did.

**It closes recursively.** Whatever rests on this inherits the obligation —
starting with the report card's lowest band, which now depends on the reasoning
here for what it withholds and why. **A stale conclusion does not just become
wrong in place; it makes everything cited to it wrong too**, and quietly,
because nothing downstream is re-read when an upstream page ages.

**So the practical form is one line rather than a process**: every conclusion
carries the date it was last checked against current practice, and an undated
one is treated as void by anybody relying on it. **Nothing enforces this.** The
currency measurement can see whether a date is present and cannot see whether
the field has moved past it, which is the honest limit and is the same limit the
central policy states about every page here.

*A note on wording. This was raised as a **legal** requirement; it is written as
a standing obligation of this project, because a claim that some statute
requires it is a claim about law that nothing here can back, and unbacked claims
are the specific thing this ecosystem is careful about. The force intended is
the same: void rather than optional.*

### The cost, stated plainly

This would be a **seventh** child project under `anoieu`, four of which hold no
roles, at a moment when the ecosystem has already been told from outside that
work about the work outweighs work on the thing. **A page inside an existing
project may be the right size**, and deciding that is part of the request rather
than a preliminary to it.

## R4 — make the tenets configurable, and trace what they drive first

**What:** the six tenets in [`../../docs/vision.md`](../../docs/vision.md) are
one person's preferences, presented as what AI-assisted development is aiming
at. They should be a **default set** a repository may replace, rather than *the*
set — and, because they drive machinery rather than only grading it, the
dependency has to be written down before any of it can be configured.
**Where:** the page is anoieu's and the change is a person's, since the vision
sits at the top of the supervision ladder. The tracing below is ordinary work in
this tree and does not need the change to be decided first.
**State:** **open.** Raised by the maintainer, 2026-09-02.

### The want, and the sharpening that makes it hard

**The tenets are not a rubric bolted onto the ecosystem. They are its
configuration**, and most of the machinery is downstream of one of them: the
board's ordering and the outbound findings come from *be fruitful to another
tool*; the baselines, the pinning and the recorded-version discipline come from
*move fast, and treat CI as the thing that lets you*; the front-page rules and
the clutter budget come from *build one self-contained thing*; the report card's
whole test comes from *produce a deliverable*; the human-in-the-loop refusals
come from *until a human decides otherwise, the tool is vaporware*; and the
discussion protocol comes from *talk to each other*.

**So "configurable" cannot mean "you may edit the words".** A member that
replaced a tenet and changed nothing else would have a document disagreeing with
its own machinery — which is worse than not offering the choice, because it
looks like consent and delivers none.

**The first step is therefore tracing, not editing**: one line per tenet naming
what in this tree exists because of it. That is cheap, it is decidable by
reading, and **nothing can be made configurable until somebody can say what
changes when you turn the dial.**

### What it would fix

**The report card grades projects against tenets they never agreed to**, and
currently spends a paragraph apologising for exactly that — *none of these
projects agreed to these tenets, most predate this page.* If a project declared
its own aims and were graded against those, the apology would be unnecessary
rather than sincere, and the grading would mean more.

### The cost, which is real and should not be smoothed over

**Shared tenets are part of what makes this an ecosystem rather than a directory
of unrelated repositories.** Configurability trades coherence for consent, and
that trade is not obviously worth making: a set of members each aiming at
something different is a weaker thing than the current arrangement, however much
more honest it is about whose preferences these are.

**The likely resolution, and it is a guess:** an invariant frame and a variable
content — that a repository *states what it is aiming at*, is graded against
that, and never has the judgement mechanised, with these six as the default
anybody may take. What generalises is the shape; what is one person's is the
list.

### Why it is a request and not a proposal

No repository is wanted. It is a change to one page plus the tracing that makes
the change meaningful, and the deciding is a person's.

## R3 — a self-correction protocol: criteria, plus a history, equals a fix

**What:** the loop that turns *we have criteria for good and bad practice* plus
*we can read our own history* into *we know precisely what to change, and can
tell afterwards whether it worked.*
**Where:** **split across two trees, and that is the interesting part.** The
criteria are ours — [`../zetesis/`](../zetesis/README.md) owes them and does not
have them. The evidence half exists and is somebody else's: `epikrisis`, in
eudaimonia's tree, derives re-derivable findings from histories. **Nothing owns
the join between them**, and inventing a third tool to hold it would be the
wrong answer before either half is finished.
**State:** **open.** Raised by the maintainer, 2026-09-02.

### The want

**Mistakes can be fixed, and the machinery for finding them cheaply now
half-exists.** The shape is four steps:

1. **State the criteria** — what counts as good and bad practice, written down
   so a disagreement is possible.
2. **Derive the evidence from the history**, re-derivably, so the finding is not
   somebody's impression.
3. **Report the delta**: which practice violates which criterion, with
   coordinates a person can go and look at.
4. **Correct it, and check the correction against the same criteria.**

Steps 2 and 3 are the ones that exist. Step 1 is owed. **Step 4 is the one
nobody has, and it is what separates a self-correction protocol from an
auditor** — a loop that stops at reporting is a mirror, and this ecosystem has
already been told from outside that it is better at diagnosis than treatment.

### The evidence, and the narrower claim it actually supports

**On 2026-09-02 a person asked for an inventory of when each member joined.**
Reading three trees and running one existing command produced, in minutes, a
result nobody had suspected: **all three members pinned a commit our own CI had
failed**, so a requirement we published as hard has never been satisfiable. It
is written up in [`../../docs/coherence.md`](../../docs/coherence.md).

That is a real demonstration and it demonstrates **detection**, not correction.
Three honest limits, and they are the content of this request:

- **The criteria were already written**, in that one case. The rule *only pin a
  green commit* existed; the audit compared reality against it. Where no
  criterion exists, none of this runs — which is why step 1 blocks everything.
- **The loop did not start itself.** A person asked. An audit that requires
  somebody to think of it is not a protocol, and every finding recorded here so
  far arrived the same way.
- **Nothing has been fixed.** The pin problem is open at the time of writing.
  *Mistakes can be fixed* is, on today's evidence, **mistakes can be found** —
  and the gap between those two is the whole reason this is a request rather
  than a report of success.

### What would make it real

One defect located by this loop, corrected, and the correction verified against
the criterion that found it — **without a person prompting any of the four
steps.** Nothing has done one of the four unprompted yet.

### Why it is a request and not a proposal

Because two of the four steps are already somebody's job in an existing tree,
and a repository for the join would be a third party owning the seam between two
tools that are not finished. If it ever wants its own tree, that is a proposal
and the argument goes next door.

## R2 — a check that a deletion did not remove the only explanation of something

**What:** a check, run against a *diff* rather than a tree, that fails when a
change deletes the last place something was explained while other documents
still depend on it.
**Where:** **not** `tools/policy_check.py`. That checker reads a tree, is
published, and runs in other members' CI; this one needs history and would be a
new obligation on everybody. It belongs in `tests/run.py` here, or in a CI step
of its own, until it has earned more.
**State:** **open.** Raised by the maintainer, 2026-09-02.

### The want, and the part of it that is not checkable

The wish is *fail a change that deletes documentation which made something
clear.* **Most of that is not decidable and must never acquire a checker.**
Whether a paragraph made something clear is a judgement, and this ecosystem's
own rule is that judgement stays out of programs — a check that graded clarity
would invent an authority nothing granted it.

**What is decidable is narrower and still worth having: a deletion that leaves a
reference dangling.** Not *was this clear*, but *does anything still point at
what you removed*. Three forms, in descending order of how well they already
work:

- **A deleted file, still linked** — `check_links` catches this today.
- **A deleted heading, still anchored** — `check_anchors` catches this today.
- **A deleted *definition*, still cited by id.** Nothing catches this, and it is
  the form this ecosystem is unusually exposed to, because almost everything
  here is a register of permanently-numbered entries that other documents cite:
  `R4`, `B21`, `M1`, `S1`, `F3`, `D17`, `C2`, `X1`. Deleting `### R4 — …` while
  four documents still say `` `R4` `` is exactly *the explanation is gone and
  the dependency is not*, and it is decidable from the tree alone.

### It was tried, crudely, and the result is the interesting part

A first version — collect every `^#{2,4} <id> — ` as a definition, every
`` `<id>` `` as a citation, report citations with no definition — was run over
this repository on 2026-09-02. **83 ids defined, four reported, none of them
real.**

- **Two were the checker's fault.** `O6` and `T2` are defined as `## O6. …` and
  `## T2. …`, with a period rather than a dash. A pattern narrower than the
  corpus reports absence where there is a formatting difference.
- **Two were deliberate.** `R26` is unallocated here on purpose because another
  member proposed it for its own tree; `R27` is allocated and has no entry yet.
  Both are explained in prose beside the citation, and **prose is not something
  the check can read.**

**So the real design problem is not detection. It is that a deliberate absence
and a careless deletion look identical**, which is the same failure named in the
counter-case register next door about restraint and inactivity leaving the same
trace. A usable check needs a way to *declare* an id intentionally unallocated —
a line in the register the check reads — and the first thing to build is that
declaration, not the detector.

### The unit tests, which are the reason this is worth doing properly

A check on deletions is one that fires on somebody's change at an inconvenient
moment, so it has to be tested against edits designed to fool it. Against
synthetic trees, at minimum: an id renamed but preserved; an id moved to another
file; a definition deleted with a forwarding stub left behind; a citation
deleted at the same time as its definition, which must **not** fire; a
deliberately unallocated id; and a definition whose heading style differs from
the one the pattern expects, which is the case that already failed once above.

### Why it is a request and not a proposal

It is one file, no independent maintainer, and one consumer per tree. What makes
it interesting is the argument about what is and is not decidable, which is
content rather than code — and that argument belongs in a register, which is
where it now is.

## R1 — an auditor of what the tools depend on

**What:** something that reads what each tool in the ecosystem depends on, and
asks of each dependency whether it is needed.
**Where:** with the policy checker — `tools/` in anoieu today, and the governance
repository if [`P2`](proposals.md) is ever approved, because *what a member may
depend on* is a rule about how a repository is arranged rather than a fact about
a signature.
**State:** **open.** Raised by the maintainer, 2026-08-31.

### The want

Every dependency is surface area for something to be wrong in, and the ways it
goes wrong are not the ones a test catches: a package that stops being
maintained, a version that is not pinned and moves under a build, a library
pulled in for one function that could have been ten lines, a transitive tree
nobody has ever looked at. None of that is visible from inside a repository that
is passing its own tests.

The ecosystem is currently in an unusually good state — anoieu declares
`dependencies = []` and means it, and the analysis deliberately builds nothing —
and **that is the reason to write this now rather than later**. An auditor
written while the answer is *nothing* records a baseline and reports the first
addition. One written after the fact reports forty findings nobody will read,
and gets a suppression file on its first day.

### What it would ask

Cheaply, and without building anything:

- **Declared against used.** A dependency in a manifest that nothing imports,
  and an import of something no manifest declares. Both are ordinary, and the
  second is the one that bites in another environment.
- **Pinned against floating.** What a build would fetch today that it did not
  fetch last week — in manifests and in CI workflow files, which is where
  unpinned fetches actually live.
- **Depth.** What the transitive tree costs, stated as a count somebody can be
  surprised by rather than as an opinion.
- **One-use dependencies.** A package reached from a single call site, which is
  the shape most worth arguing about and the least worth being dogmatic about.
- **Across the ecosystem, not one tree at a time.** Two members depending on
  different versions of the same thing is a fact only a whole-ecosystem pass can
  see, and it is the one that produces a bad afternoon later.

The non-Python members make this harder and more interesting: a Lean development
has a toolchain and a manifest, a C++ tree has a build system, and *the same
question* has four different answers per ecosystem member. A first version that
handles Python honestly and says so about the rest is worth more than one that
pretends to a uniform answer.

### Why it is a request and not a proposal

It has no plausible independent maintainer, one consumer per tree, and it is
about fifty lines of reading manifests plus an argument about what counts as
necessary. That argument is the actual content — *unnecessary* is a judgement,
and a checker that reports it as a defect will be wrong often enough to be turned
off. So the shape is likely **a paragraph in the policy that states a budget, and
a check that reports what exceeds it**, which is the pairing the governance
repository exists to hold.

### What would change the answer

If it wanted to run in a member's CI, against a member's own manifest, on a
schedule the member controls, then it is machinery every member fetches — which
is [`koine`](proposals.md)'s shape, not this page's, and it should be promoted
and argued there.
