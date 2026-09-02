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
