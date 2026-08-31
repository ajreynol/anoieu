# Requests

Work the ecosystem wants that **does not obviously need a repository of its
own**. Newest first.

[`proposals.md`](proposals.md) audits one question — *should this become a
repository* — and answers it against a standard. Most wants are not that
question. They are a check somebody should write, a rule somebody should state,
a report nobody generates; the useful answer is usually *yes, and it belongs in
that tree over there*. Recording those in the proposals page would either inflate
them into repositories or lose them, and both have happened elsewhere.

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
