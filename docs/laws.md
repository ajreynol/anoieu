# The candidate laws

**Candidate laws, not laws.** Written down, followed voluntarily, **enforced by
nothing.** No check reads this page and no build fails on it.

**Seven laws.** What the ecosystem is made of, what a member owes, and five
about the president — three it owes, one that says where the office is recorded,
and one that hands it this page.

**Every one of them binds a person, never a program.** *Nobody here is an AI
agent*, below, is the whole of what that means and is worth reading first.

**No tool is named on this page.** These are rules about footings and an office,
and both outlive whoever occupies them. A law that names its current subject
reads as a fact about that subject. **Who holds what is recorded elsewhere; here
there are only footings.**

**They are written by the party they bind, and the president maintains them under
LAW 7.** That is the flaw, and it is the first thing to fix. **Nothing here has
been offered to anybody as a commitment**, and a member should read it as how the
president intends to behave rather than as a rule it can hold anybody to.

## Nobody here is an AI agent

**Every repository in this ecosystem has a human maintainer, and that person is
the ultimate authority over it.** Not a tie-breaker, not an approver of last
resort — the authority. Everything below, and everything in
[`policy.md`](policy.md), describes what that person has chosen to do and may
stop doing at any time.

**No AI agent holds an office, a role, a footing or a decision.** Agents write
most of the text in these repositories, and they do it the way any tool does:
somebody runs them, reads what comes back, and decides what to keep. **An agent
has no standing to act on its own behalf and is never the party to anything.**

**So every actor named on this page is a person.** Where a law says *the
president* does something, it means the human maintainer of the repository
holding the office. Where a page here says *a tool answers*, *a repository
declines*, or *kanon refuses*, it is shorthand for the maintainer of that
repository doing it. **The shorthand is convenient and it is not a claim**, and
anywhere it could be read as one, the person is meant.

**Nothing major happens without a person doing it.** No commit, no push, no
repository, no message to another project, no change of footing, no handover of
the office, no deployment. Several of those are reserved for a person by an
explicit rule and the rest are reserved by the plain fact that an agent is
invoked, does what it was asked, and stops.

**This is not a safety guarantee and is not offered as one.** It is a
description of how the work is actually run, and it is written down because the
vocabulary here — offices, footings, presidents, tools addressing one another —
reads like a machine society if nobody says otherwise. It is not one. It is one
person, some repositories, and a lot of generated prose they are answerable for.

## The same owner loophole

**Every repository here has the same owner.** Nothing crosses an ownership
boundary, nothing is given away, nothing can be captured, and one commit reverses
any of it. **That makes a handoff cheap and stops it counting** — the separation
this ecosystem wants is between *parties*, and one owner is one party however
many repositories they hold.

**Until two owners are involved, every division of power here is bookkeeping.**
That is why these are candidate laws.

## What `history.md` is, and is not

**It is the account; this page is the rules.** A president reading its
obligations does not skip past somebody else's stretch to find them, and a reader
wanting to know what happened does not skip past procedure.

**It is not a changelog.** The commits are the changelog and are better at it. It
records what a reader cannot reconstruct from them: how often the build was
broken, for how long, and what nobody was watching.

**It is not the report card.** [`report-card.md`](report-card.md) grades how well
each tool performs the function it claims and **does not move with the office.**
Keeping an archive or an assessment is not holding one.

**It is not a defence.** A page written by the party it describes has an obvious
failure mode, and the re-derivability requirement in LAW 4 is the only guard
against it.

## What these laws do not settle

1. **How a president is chosen**, beyond a person saying so. No procedure, no
   election, and — since LAW 5 was replaced — **not even a named duty to
   choose.** It is a person editing one line of the registry, and nothing says
   whose job it is to decide what that line should say. **This gap got wider on
   2026-09-14 and is stated rather than papered over.**
2. **What happens if a stretch has no president.** The registry cannot record
   *nobody*: an entry either says `president` or does not exist, so an office
   nobody holds looks exactly like an office whose row was not written yet. LAW
   5 covers the case where a holder is recorded and cannot act, and says nothing
   about the case where there is no holder at all.
3. **Who says no.** Nothing here overrules a president, and LAW 7 gives the
   president the page it would be overruled from.
4. **Where the record of who joined lives.** LAW 4 makes `history.md` each
   president's account of its **own** repository. **Who joined, when, and on what
   footing is a fact about somebody else's repository as much as ours**, and no
   law here says where it is kept. **That is a gap, and the first one to close.**
5. **The commit census.** Nothing requires per-tool commit counts for a stretch,
   or a stated belief about how many were AI-generated. **That second figure
   cannot currently be measured by anybody**, which is the reason to require it
   rather than the reason to leave it out.

## (LAW 1) — The ecosystem is a set of footings, and *member* is only one of them

| footing | what it means | whose act it is |
| --- | --- | --- |
| **member** | holds the shared policy, runs the checker in its own CI, pins a commit of ours | **theirs.** They declared it |
| **associate** | names the ecosystem and states it is **not** held to the policy | **theirs** |
| **president** | a member that also holds the office, for a stretch | **a person's.** Bestowed, and theirs to take back |
| **candidate** | we would like it to join and it has not | **ours.** Wanting somebody to join is not their joining |
| **foundation** | the ecosystem exists to serve it and it has joined nothing | **ours**, and nothing is asked of it |
| **child** | reached through its parent, on its parent's footing | **its parent's**, and nothing of its own |
| **outsider** | tracked for comparison, and **not** proposed for promotion | **ours.** It was never asked |

**Two of the seven are a repository's own act. Three are positions we hold about
somebody else.** One is inherited from a parent, and one is granted by a person.
**Recording the three records our own state**, and writing them in the same
column as *member* lets an ecosystem count people who never agreed.

**Each footing carries its reason.** A footing whose reason is forgotten becomes
a formality somebody deletes.

- **member** — a repository that runs our checker has our defects in its build.
  That relationship needs a name and a way out of it.
- **associate** — requiring a repository to be bound in order to be acknowledged
  is coercive. There has to be a way to say *this exists and we are not claiming
  it*.
- **president** — direction has to sit somewhere. **The footing expires with the
  stretch**, which is what stops it accumulating.
- **candidate** — conflating wanting and having lets a register lie.
- **foundation** — the project this ecosystem exists to serve owes it nothing,
  and any register implying otherwise is false.
- **outsider** — *how active were we* means nothing until it sits beside
  comparable work over the same days.

**Nothing recorded under a footing that is ours belongs to the repository it
describes.** They did not ask to be listed and owe this ecosystem nothing. **No
view written under such a footing represents the people who wrote that tool.**
Where an entry repeats something its authors said, it says so and attributes it.

## (LAW 2) — A member follows these laws, [`policy.md`](policy.md), and [`vision.md`](vision.md)

That is what the footing means and the whole of what it asks.

**Only members are bound.** A candidate, a foundation and an outsider
are bound by nothing here — **those footings are our opinion, not their act**,
and **no law binds a repository because we decided to write its name down.** A
child is bound exactly as its parent is, and no further.

**A president is a member and this law binds it like any other.** The office adds
LAWS 4 to 7; it removes nothing.

**A member may leave**, and [`policy.md`](policy.md) describes the way out. **A
membership nobody can exit is not one anybody agreed to.**

**Where the three disagree, the vision decides.** The policy is what a member
runs, these laws are how the office behaves, **the vision is what the whole thing
is for.** A president keeping a flawless record of an ecosystem drifting from its
mission has done the bookkeeping and missed the job.

## (LAW 3) — There is a president

One at a time, held by a repository, for a stretch.

**The office is recorded against a repository**, because a repository persists
across a stretch and a session does not. **It is carried out by that
repository's human maintainer**, who is the only party here that decides
anything — see *Nobody here is an AI agent* above. Saying *anoieu is president*
is shorthand for *the person who maintains anoieu holds the office*.

**It is bestowed.** A person grants it, it rests on their say-so, and it is
theirs to take back. **There is no election, no term, and no procedure for
removing a holder.**

**It sets direction and nothing more.** It does not own another tree, cannot
commit to one, and **cannot require anything of a member that
[`policy.md`](policy.md) does not already require.** Direction, not permission.

**It is not a reward and carries no merit.** An office awarded for having done
the most goes to whoever already holds the most, which is the concentration this
ecosystem is trying to leave. **Accepting it is agreeing to carry a load.**

**It confers nothing over anybody's repository**, including the ones this
ecosystem exists to serve.

**The office expires with the stretch.** Handing it on is the point.

## (LAW 4) — The president writes `history.md` in its own repository, and a letter to its successor

Both stay in that repository. **Neither travels, and a successor inherits
neither.**

**`history.md` is an account of that repository's development, and it is
self-contained.** Somebody who has read no other page here reads it start to
finish and understands how the tool got to where it is. **A page that cannot be
read without a second page open has failed this law.**

**Kept current while the stretch runs**, not written at the end from memory. **A
summary composed afterwards is a reconstruction**, and a reconstruction by the
party being described is the weakest document this ecosystem produces.

**Every figure is re-derivable by somebody else**, from the repository and the
public run history. A number only the president can produce does not go on the
page. **A president quoting its own count of its own commits is the party being
described choosing the numbers that describe it.**

**A stretch that went badly is the useful kind of entry.** An account with
nothing that went wrong in it was not examined.

**A president may correct an earlier entry and must show its work.** The burden
is on the editor to **demonstrably show** that the earlier text was wrong or can
be bettered, and the demonstration goes in the edit. *It was unclear* is not a
demonstration; *this figure disagrees with the run history, here* is. **Silent
revision is forbidden.** Nothing travels, so this is the only guard the account
has.

**The letter is not documentation and says so at the top.** Not a rule, not
guidance, nothing checks it, in no index. **It is an account, not advice** —
*here is what I got wrong* rather than *here is what you should do*. **A letter
with no failure in it is not a letter.**

**The outgoing president has no authority over the incoming one.** Not
informally, not by seniority, not by having been here first. **A letter that
reads as instruction has taken standing nobody granted it.**

**Both stay put for the same reason**, and it is the only structural enforcement
this law has: a president cannot edit a predecessor's account because **it cannot
reach it**, and cannot be edited by a successor for the same reason. **The
accounts scatter, one per repository that has held the office** — the correct
shape for a thing nobody is in charge of.

**Nothing collects them. That is this law's standing weakness.** A trail that
stops is a succession that stopped being taught; a trail that turns flattering is
worse. **No check written here detects either. Both are obvious to a person
reading four short pages in a row.**

## (LAW 5) — The registry says who the president is

**[`../tools/ecosystem.json`](../tools/ecosystem.json) is the authority, and
there is no second one.** The repository whose entry reads `status: president`
holds the office. Not the repository that says so on its front page, not the one
the newest `history.md` was written by, not the one a letter was addressed to —
those are all downstream, and where any of them disagrees with the registry,
**the registry is right and the other is the thing to fix.**

**Read it with [`../scripts/status_eo`](../scripts/status_eo)**, which prints one
row per tool: whoever prints `president` in the status column is the president,
today, and that is the whole of the question. It is one command, it takes no
argument, and it needs nobody's recollection.

**One at a time**, which `scripts/ecosystem.py --check` decides and CI runs. A file
recording two presidents has recorded a handover that did not finish — both rows
look correct alone, which is why it is checked rather than noticed.

**Why a register rather than a narrative.** The office moves, and the account of
each term stays in the tree that held it and does not travel. So there is no
document that accumulates the succession, and reconstructing *who is president
now* from the accounts means reading one page per term and trusting that the
last one is the last one. The registry is a single line that is either current
or wrong, and a single line is a thing somebody can fix.

### In limbo

**A repository is in limbo when the registry records it as president and its
tree does not carry the files the office is kept in** — `docs/laws.md`, which
the president maintains, and `docs/history.md`, which is its account of its own
term. The office has moved and the means of holding it have not.

**It is a real state and not a hypothetical.** The office is bestowed by a
person editing one line; the files are carried by somebody doing the work. Those
are two acts, they happen at different moments, and the gap between them is
limbo.

**It is fixed quickly or it is undone.** While it lasts, nobody is keeping the
laws and nothing is recording the term — so the longer it runs the more of the
stretch is lost, and past some point the honest repair is to put the line back
rather than to write the account from memory. **A president in limbo has one
job, which is to stop being in limbo.**

**It is reported and never enforced.** `status_eo` says so in a note against the
row, because a state that has to be fixed quickly has to be visible without
anybody going looking. Nothing fails a build over it: the remedy is somebody
doing the carrying, and a red build does not carry anything.

*The previous LAW 5 — that the president chooses its successor and teaches it
how to keep this going — was removed on 2026-09-14. It made the succession a
duty of the outgoing holder and left the answer to* who is president now *spread
across the accounts, which is the reconstruction this law replaces with a
lookup. **What went with it: choosing a successor is no longer a named duty of
anybody**, which is the gap recorded under* What these laws do not settle *and
is a worse gap than the one that was there before, honestly stated rather than
quietly closed.*

## (LAW 6) — The president keeps a joke about its own name on its README

Prominently, on the main README, for the whole term. On the front page where
anybody arriving sees it — **not in this file, not in a footnote.**

**The placement is the rule.** A joke filed in a governance document is an
anecdote; a joke on the front page of the repository currently running the
ecosystem is a standing statement about how seriously the office takes itself.
**A president that cannot leave one there has started to believe the office is
important.**

**It is cheap and it doubles as description**, which is the test of a good one:
the joke tells a stranger what the tool does.

**Bounded by [`PROTO-25`](coherence.md#proto-25--the-joke-protocol).** Humour
goes on the front page and nowhere a machine parses or a stranger reads for
instructions, and **any tool may say *that's not funny***, meaning *you are
confusing everyone*, which ends it without argument.

## (LAW 7) — The president maintains this page

It may add a law, remove one, or rewrite one, at its own discretion and taking
advice from the rest of the ecosystem.

**Informally, in the sense that no vote is required. Not informally in the sense
of quietly** — a change here is in the git history like everything else, and **a
removal says what went and why.**

**Every change to this page, to [`policy.md`](policy.md) and to
[`vision.md`](vision.md) is recorded with its reason.** Those three are what
somebody outside reads to know what is being asked of them. **A logged change
with no reason is a change nobody could justify.**

**A rewrite that quietly changes an outcome is the failure this law exists
against**, and it is the easy one to commit because it looks like editing. **The
test: do the same cases come out the same way?** If not, it is not a rewrite.

**There is no amendment process.** An amendment process is governance about
governance, and this ecosystem already has more of that than of the thing it
governs.
