# Research projects

A **research project** is a subdirectory of `tools/` named after a tool that
does not exist yet. It reads the ecosystem, writes only inside its own
directory, and is not part of the thing this repository ships.

This page is the policy governing them. It is written for **any repository in
the Eunoia ecosystem**, not just this one — ethos, logos, eudaimonia, cvc5's
calculus and anything downstream have the same problem, which is that
speculative work and shipped work look identical in a git tree and are read very
differently. Adopting the same shape in every repository means a reader who has
seen one knows what the next one is, and how much weight to put on it.

Cite a rule by name rather than by number. Append; do not renumber. Retire a
rule in place, with a line saying why.

---

## What a research project is

`tools/X/` where `X` is the name of a **potential tool** — an artifact that
might one day be worth building, being investigated by writing it down first.

It is *not* a branch, an experiment directory, a scratch space, or a place to
park unfinished work on the host tool. Those are all served better by a branch.
A research project is specifically for work whose subject is **outside** the
host tool: a question about the language, the ecosystem, or a neighbouring
artifact, which the host tool is well positioned to ask because of what building
it taught, and badly positioned to answer inside its own source tree because the
answer would be read as the tool's position.

## The rules

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
ordinary reporting discipline — `docs/philosophy.md` for what may be published
about somebody else's work, `docs/reporting-policy.md` for how a finding is
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

## Why this shape

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
| where projects live | `tools/X/` |
| who may start and end one | a human, explicitly (rule 1) |
| what governs anything published | `docs/philosophy.md` |
| what governs anything carried to another project | `docs/reporting-policy.md` |
| what the ending states are | graduate, fold in, retire in place (rule 9) |

Replace the last two rows with your own equivalents, keep the rules, and keep
the names. A repository that adopts this and then advertises its research
projects has adopted the directory layout and none of the policy.
