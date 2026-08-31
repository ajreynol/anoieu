# Repository policy

How a repository in the Eunoia ecosystem is arranged: where things go, what the
front page must say about who is writing it, and what may be kept in the tree
that is not part of what the repository ships.

It is written for **any repository in the ecosystem**, not just this one —
ethos, logos, eudaimonia, cvc5's calculus and anything downstream. The reason to
converge is the same in every case. Someone who has found their way around one
of these repositories should already know their way around the next, and should
be able to tell at a glance which parts of it are load-bearing and which are
somebody thinking out loud. Those two look identical in a git tree and are read
very differently.

Its sibling is [`vision.md`](vision.md), which governs what the development is
aiming at: this page is about the arrangement, that one about the point of it.

Cite a rule or a convention by name rather than by number. Append; do not
renumber. Retire either in place, with a line saying why.

---

## The layout

| path | what it holds |
| --- | --- |
| `README.md` | the front page, and the whole of what any other document may assume has been read |
| `docs/` | every written document, indexed by `docs/README.md`, together with the documents a run generates |
| `tools/` | the harness: generators, the runner, the dependency manifest — and child projects |
| `tests/` | the evidence: the cases, the recorded behaviour of other people's programs, the committed baselines |
| `scripts/` | executable versions of workflows the documents define |
| `deps/` | other people's repositories, fetched by a run and never committed |
| `.github/workflows/` | what runs on every push |
| the package itself | at the top level, named after the tool |

The conventions that go with it.

**There is one entry point, and it is the front page.** `README.md` carries what
the tool is, what it finds, what it refuses to claim, how to run it, and a route
to everything else; every other document may assume it has been read. Nothing
competes for that role — no second overview in `docs/`, no wiki, no
`INTRODUCTION.md`. This is the same requirement as tenet 3 of
[`vision.md`](vision.md), seen from the filesystem rather than from the work.

**The maintenance entry point is not the front page.** The README is written
for somebody deciding whether the tool is worth their attention; how the work is
run is noise to them and buried treasure to whoever is doing it. Keep the second
audience a separate document — here [`../docs/coherence.md`](coherence.md)
— reachable from the things a maintainer opens (the agent brief at the
repository root, the headers of the programs that write the record) and not
linked from the front page.

**Every repository explains its own name.** A short section on the front page
with the etymology and why the word fits, written so somebody could disagree
with it. The ecosystem names along a convention — Greek, and from the vocabulary
it already draws on — and a convention nobody explains decays into decoration
within about two repositories.

**`docs/` has an index, and the index is itself a document.** One row per
document saying what that document is *for*, in a sentence, so that a question
has one obvious place to be answered. Adding a document means adding a row, and
a document not worth a row is not worth adding.

**Written and generated documents are separated and labelled.** A generated
document says at the top that it is generated and by what, and generators write
nothing else — the files a person maintains are never machine-edited. Within the
generated ones, say which of two disciplines applies: *rewritten whole*, where
anything typed in is lost on the next run, or *additive*, where the generator
may add rows and never remove or rewrite one, so hand-written verdicts survive.
The asymmetry is deliberate and worth stating wherever it applies, because a
generator that is allowed to delete can quietly delete a regression.

**`tools/` is the harness, not the product.** Everything that produces, checks
or measures the repository's own claims, and nothing a user of the tool ever
invokes. Each generator states at the top of its own file what it writes and
what it refuses to write, which is the cheapest available defence against a
script quietly acquiring an opinion. Child projects live here too, for the
adjacent reason: neither the harness nor a child project is part of what the
repository ships.

**The documents that govern the work live with the documents.** This page and
[`vision.md`](vision.md) sit in `docs/` rather than beside the code they govern,
because they are read far more often than the harness is, and by people who are
not editing anything. A governing document filed under `tools/` is a document
somebody has to know to look for.

**`tests/` holds the evidence, not only the tests.** The property to preserve is
that a person can open one file and see in a minute what a claim rests on: one
small case per check, the output of somebody else's program recorded from a real
run rather than written from memory, a committed baseline that fails *this*
repository's build when a change invents a false positive. Evidence that exists
only as a passing assertion is evidence nobody can read, and every claim the
front page makes should be traceable to a file somebody could open.

**Dependencies are fetched and pinned, never vendored.** A manifest and a lock
in `tools/`, restored by the run that needs them. Two consequences worth having:
the repository stays small enough to read, and the build can go red for its own
reasons only — with a separate scheduled job asking the different question of
whether anything upstream has moved.

**A workflow is defined in prose and implemented in `scripts/`.** Where a
procedure is worth automating, the document stays the definition and the script
is one way of running it; where both exist, CI checks that the script's copy of
the text has not drifted from the document it came from.

**Working space is untracked, and says so.** `scratch/` for anything transient,
and the `*.local.md` suffix for a document that is deliberately not committed. A
file kept out of git carries a line at the top saying so and why, so that a
reader who finds it knows they are looking at an intention rather than an
oversight.

## The maintenance note

**Every repository's README ends with a short section stating how the
development is currently being run.** Not how it works, not what it has
achieved — who is writing it, under what supervision, and what that supervision
covers. anoieu's is the model, reproduced here for the phrasing rather than for
the content:

> ## How this repository is maintained
>
> **Written by AI agents, under light human supervision.** A human directs the
> work, reads what is published and decides what is filed; nobody vets the
> internal design, and nothing reaches another project's issue tracker without
> review. [`docs/reporting-policy.md`](reporting-policy.md) says what that does and
> does not cover, and why the intended audience is experts.

Four properties, of which the third is the one that gets dropped and the fourth
the one that gets violated.

**It is last.** By the time a reader reaches it they have seen what the tool
claims, and this is the note that tells them how to weigh all of it. At the top
it would be a disclaimer to be got past; at the bottom it is what they leave
with.

**It is about the process, in the present tense.** Who does the work, who
supervises, and what happens before anything is published or carried to another
project. It describes the arrangement as it currently stands — not as it was
when the repository started, and not as it is hoped to become.

**It says what the supervision does not cover.** Readers are generous with the
word *supervision* and will assume more of it than is there. Naming the gap
plainly — *nobody vets the internal design* — is the entire value of the note,
and it is also the sentence that gets softened first, because it is the one that
costs something to write.

**It carries no technical detail.** Not what CI runs, not the layout, not the
check catalogue, not the current state of the work. All of that changes weekly
and is covered elsewhere; the note describes the arrangement that produces it,
and should be stable for months. A maintenance note that has to be updated
alongside the code has stopped being one.

**When it changes.** It changes when the policy changes and at no other time,
which makes it the one place a reader can discover that the arrangement has
moved. A human taking over the development of a tool — the ending
[`vision.md`](vision.md) aims at — is exactly such a change, and rewriting this
section is how that becomes visible to everybody who was not in the room. A note
that has drifted from the truth is worse than no note at all, since the whole of
its value is that it can be relied on without being checked.

## Research projects

A **research project** is a subdirectory of `tools/` named after a tool that
does not exist yet. It reads the ecosystem, writes only inside its own
directory, and is not part of the thing the repository ships. Speculative work
and shipped work are the pair this repository is most often asked to keep apart,
and the rest of this page is how.

[`vision.md`](vision.md) calls these **child projects** and calls the repository
that carries one the **parent project**; where this page says *host tool* or
*host repository*, it means the parent. Same arrangement, two vocabularies, and
the shorter one is winning.

### What a research project is

`tools/X/` where `X` is the name of a **potential tool** — an artifact that
might one day be worth building, being investigated by writing it down first.

It is *not* a branch, an experiment directory, a scratch space, or a place to
park unfinished work on the host tool. Those are all served better by a branch.
A research project is specifically for work whose subject is **outside** the
host tool: a question about the language, the ecosystem, or a neighbouring
artifact, which the host tool is well positioned to ask because of what building
it taught, and badly positioned to answer inside its own source tree because the
answer would be read as the tool's position.

### The rules

**1. A human starts one.** A research project may only be initiated by a person,
in an explicit instruction, and the same is true of ending one. No agent, no
script and no workflow creates `tools/X/` on its own initiative, or promotes a
directory of notes into one. The reason is that a research project is a claim on
attention and a name in a shared namespace; both are cheap to spend and
expensive to withdraw. Everything *inside* one, once started, may be written by
whoever is doing the work.

**2. It is an island, and the island is read-only.** A research project reads
whatever it likes — the host tool's source, the checked-out dependencies, the
manuals — and writes **only inside its own directory**. It imports nothing from
the host tool and the host tool imports nothing from it. It is not on the import
path, not in the test suite, not in CI, not in any generated document, and
nothing anywhere breaks if the directory is deleted. Deleting it is the test: if
removing `tools/X/` changes what the tool does or what CI says, it was not an
island and the coupling is a defect to be removed rather than documented.

**3. It is not advertised.** No entry in the repository README, no row in the
documentation index, no mention in a report, no announcement, no link inward
from anything a user reads. The directory listing of `tools/` is the whole of
the index, deliberately: a registry file is one more thing to keep true, and the
filesystem already answers the question. This is not secrecy — the work is
committed in the open and anyone reading the tree will find it. It is a refusal
to *borrow the host tool's credibility* for work that has not earned any of its
own. A speculative account that arrives with the tool's name on the front page
is read as the tool's position, and withdrawing that impression later costs more
than the work is worth.

**4. The name is part of the work.** Projects are named along the ecosystem's
convention — Greek, and preferably from the vocabulary the ecosystem already
draws on: *eunoia*, *ethos*, *logos*, *eudaimonia* are the tools that exist;
*pathos*, *hermeneia*, *noesis*, *iogos*, *euthyna* and *elenchos* are already
spoken for as code names for future projects. Pick a word that **describes the
work** rather than decorating it, and write the etymology down in the project's
own README, in a sentence somebody can disagree with. A name that needs no
explanation is not fitting the convention; a name whose explanation is a stretch
is a sign the project's scope has not been decided yet.

**5. It carries a charter, and the charter names what it will not do.** The
project's README states, before anything else: the question it is trying to
answer, the goals in order, the **stretch goal** if there is one, and — the part
that does the work — an explicit list of what is *out of scope*. A research
project with no stated boundary expands until it is a second tool, at which
point it is neither research nor a tool. The charter is the thing a human agreed
to in rule 1, so changing its scope is a decision for a human, exactly like
starting one.

**6. It is additive, never authoritative.** A research project may produce an
account of something that already has an account — a second manual, a second
model, a rival description. This is legitimate and is often the point: two
independent descriptions of the same artifact disagree in the places the artifact
is genuinely unclear, and that disagreement is the finding. But the existing
account **remains the authority**, and the project's own output says so, on its
own front page, in its own words. *Authority* here means that the existing
account governs and the new one does not — it does not mean the existing one is
presumed correct, and a project that resolves every disagreement in the
incumbent's favour has stopped being a second reading and become a paraphrase. "An alternative source of truth" means a
second thing a reader may consult and check the first against — never a
replacement, and never something a reader could mistake for the specification.

**7. Nothing leaves the island by machine.** Anything a research project wants
to say to the project that owns its subject is subject to the host repository's
ordinary reporting discipline — `docs/reporting-policy.md` for what may be published
about somebody else's work, `docs/reporting-workflow.md` for how a finding is
carried, confirmed and closed. A research project has no separate channel and no
lighter standard. In particular the *settling artifact* rule holds: a reply is
somebody's triage, and only an artifact settles anything. What the project may
do on its own is accumulate a **ledger** of candidate feedback inside its own
directory; a person decides when and whether any of it is carried anywhere.

**8. It builds on what the host tool learned, and says where.** The reason to
run a research project inside a working tool's repository, rather than in a new
one, is that the tool has *evidence* — cases it ran, behaviours it verified,
places it found the documentation and the implementation to disagree. A research
project that does not use that evidence should be its own repository. One that
does must cite it: every claim inherited from the host tool's notes carries a
pointer to where it was established, so a reader can tell what was checked from
what was reasoned.

**9. It ends with a verdict.** Three endings, and a person picks: it
**graduates** into its own repository, it is **folded** into the host tool, or it
is **retired in place** with a line in its README saying what was learned and
why it stopped. What is not an ending is going quiet. A directory that has not
moved in a long time is a claim nobody is standing behind, and the honest form of
that is a retirement note, not silence.

**10. A child project that has earned its keep says so, and names what it broke.**
A child project may deliver — a finding carried, a measurement somebody uses, an
argument somebody acts on — long before anybody is ready to decide which of rule
9's three endings applies. When that happens the honest move is not to pretend
the island still holds. The project stays in `tools/`, and its own README states
three things: **what it delivered**, **which of the rules above have stopped
being true of it**, and **that the promotion decision is open, and with whom**.
A named exception is a decision somebody made and can defend; an unnamed one is
drift, and the difference between them is the whole of this rule. The holding
state is legitimate and is not a licence to go quiet — rule 9 still applies, and
a project sitting here without a person standing behind it is retired, not
parked.

The instance here is the fuzzer, `tools/anoieu_fuzz/`. It has provoked defects
in ethos and disagreements between ethos and logos, one of them now a committed
regression test, so it has earned its keep. It also breaks **rule 2** in three
ways — it imports `anoieu.diagnostics` and `anoieu.fingerprint`, the report
generator imports it back, and it runs in CI — and breaks **rule 3**, being
advertised on the front page and holding a row in the documentation index.
Deleting the directory would break the build, which is exactly the test rule 2
sets, and it fails it. That is recorded rather than fixed, because the fix is a
promotion decision and that belongs to a person.

## What is checked

Every rule and convention on this page is a claim about *this tree*, which means
a program can decide it without holding an opinion — and
[`tools/policy_check.py`](../tools/policy_check.py) decides the ones that are currently
decidable, on every push. That is the property to preserve when adding to this
page: **a rule nobody can check is a rule worded loosely enough to be
tightened**, or one that belongs in [`vision.md`](vision.md) instead. The
dividing line, and why the vision must never acquire a checker of its own, is
*Policy is checked; vision is argued* on that page.

    python3 tools/policy_check.py              # check; exit 1 on any failure
    python3 tools/policy_check.py --coverage   # what is checked, and what is not

The run prints the rules it **cannot** decide alongside the ones it can, each
with the reason — intent, tone, elapsed time, editorial judgement. That list is
part of the output rather than a footnote, because a checker that reports only
its own passes reads as coverage it does not have. Shrinking it is ordinary
work; a rule moving off it because it was reworded is the intended way this page
improves.

### Why this shape

Three failures this is arranged against, in increasing order of how much they
cost.

The cheapest is **scope drift** — a research project quietly becoming a second
tool, with dependencies, tests, and a stake in the host's CI. Rules 2 and 5
handle it, and the deletion test in rule 2 is what makes rule 2 checkable rather
than aspirational.

The middle one is **stale speculation read as current**. Research work is mostly
wrong, which is fine, and it is committed in the open, which is also fine; the
problem is a reader arriving at a two-year-old sketch through a link on the front
page and taking it for a position. Rules 3 and 9 are the answer: nothing links
inward, and nothing stays open without somebody standing behind it.

The expensive one is **borrowed credibility**. A tool that reports defects in
other people's files accumulates exactly one asset, which is that its findings
are worth reading. Publishing a speculative account under the same name spends
that asset on work that has not been checked, and — worse — makes the *next*
finding harder to argue with, because the audience has learned that this name
covers both. Rules 3, 6 and 7 exist for this and are the ones worth defending
when they are inconvenient.

## Adopting this in another repository

The policy is written to be copied. What another repository has to decide:

| decision | here |
| --- | --- |
| how the tree is arranged | the table in *The layout* |
| where the maintenance note goes | the last section of `README.md` |
| where a maintainer starts | `docs/coherence.md`, linked from tooling and not from the front page |
| where projects live | `tools/X/` |
| who may start and end one | a human, explicitly (rule 1) |
| what governs anything published | `docs/reporting-policy.md` |
| what governs anything carried to another project | `docs/reporting-workflow.md` |
| what the ending states are | graduate, fold in, retire in place (rule 9) |

Replace the rows that name documents with your own equivalents, keep the rules,
and keep the names. A repository that adopts this and then advertises its research
projects has adopted the directory layout and none of the policy.
