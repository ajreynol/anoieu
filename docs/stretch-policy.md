# The stretch policy

What a stretch is, what ends one, and what designing the next one involves.

[`stretches.md`](stretches.md) is the **log** and this is the **policy**, and they are
two files because they are held to opposite standards: a policy has to be current
and the log explicitly does not. One file carrying both would make the licence to
be stale look like it covered the rules as well.

## What a stretch is

**The work between one global announcement and the next.** It has no schedule
— it is the span a single announcement turned out to cover, named after the
fact.

**A deployed stretch carries a version, and that changed on 2026-09-02.** This
page previously said *nothing is versioned against it*, which was true while
nothing had been deployed. **`E1` is the stretch's name and `0.1.0` is the
version it is deployed as**, and the two are not alternatives: the name is what
a member writes in `EUNOIA_EPOCH` to say which advice they built against, and
the version is what a deployment is called out loud.

**Three version numbers exist in this repository and they mean different
things.** Conflating them is the mistake this paragraph is here to prevent:

| number | what it versions | where it lives |
| --- | --- | --- |
| **`0.1.0`** | **the ecosystem's shared arrangements** — the policy, the protocols, the advice a member adopts | the stretch log, on the deployed stretch |
| `0.2.0` | the **analyzer**, as a Python package | `pyproject.toml`, `anoieu/__init__.py` |
| `0.1.0` | the **fuzzer**, as a Python package | `anoieu_fuzz/__init__.py` |

**The last two are unrelated to the first and to each other**, and the collision
between the fuzzer's `0.1.0` and the ecosystem's is a coincidence rather than a
correspondence. **Nothing synchronises them and nothing should**: a member
adopting `0.1.0` of the arrangements is not adopting a version of anybody's
Python package.

**It is still not a release.** No cadence is promised, no compatibility is
guaranteed, and a version number is a name for what was published rather than a
commitment about what comes next.

**The boundary is an announcement and not a date**, because a date would be a
cadence, and a cadence is a commitment to other repositories that we are in no
position to sign. An announcement is an event that already happens, already
costs somebody's attention, and already has a place in the record. Using it as
the boundary adds no machinery at all, which is most of the argument for it.

## What counts as a major event

A stretch is made of these. The list is short deliberately — a register of events
that counts everything is a commit log, and there is one of those already.

| event | where it is recorded |
| --- | --- |
| a global announcement | [`discussion.md`](discussion.md), the topic carrying `Global:` |
| **a role changing hands** | [`roles.md`](roles.md) — the entry moves under a new heading and the id does not change |
| a repository joining, or its footing changing | [`../tools/ecosystem.json`](../tools/ecosystem.json) |
| a child project reaching one of its three endings | the project's own README |
| a convention every member is checked against changing | [`policy.md`](policy.md) |

**A role changing hands is a major event, and it is the one most likely to be
missed.** It changes who is *accountable* rather than what exists, so it leaves
almost no trace in a tree: one entry moves between two headings, the id stays the
same, and nothing is created or deleted. A reader reconstructing history from
commits alone will not see it happen. That is the whole reason
[`roles.md`](roles.md) keeps ids permanent and moves entries rather than
rewriting them — and it is why a handoff belongs on this list beside an
announcement rather than a rung below it.

The others are here because each already has a file that records it. **An event
with no home is not a major event; it is a change of mind.**

## The declared record, and who it is for

This page and its log are a **declared record**: what we say happened, written by
hand, at the time.

A tree also carries a **derived record** — what the commits show happened —
and the interesting quantity is the delta between the two. A child project in
eudaimonia's tree builds exactly that comparison, and its assessment of five
trees here found that the repository holding four fifths of the ecosystem's
commits contributes none of its declared record, so the documentation practice
that assessment could see was three days old and covered only the newest trees.

**That is a fair hit and this is part of the answer to it.** A declared record is
cheap to keep and impossible to reconstruct later; the reason to write down that
a stretch ended, or that a role moved, is precisely that neither is legible from a
diff. Nothing here is generated, and nothing should be: a derived record that
agrees with itself proves nothing.

## The hard constraint: a red stretch is not deployable

**A stretch may only be adopted at a commit where anoieu's own CI is green, and a
downstream tool must refuse it otherwise.** This is the one thing on this page
that is not a convention, and it is stated as a requirement on *them* because it
is the only half we cannot enforce from here.

**Adoption means moving a pin.** A member adopts a stretch by moving `ANOIEU_REV`
in its `anoieu / policy` workflow to a commit of this repository. That is the act
this constrains — not reading the announcement, not agreeing with it, and not
doing anything the announcement asks for.

**The question is asked about the commit, never the tip.** Green-at-a-commit is a
fact that never changes once the run has finished. Green-at-HEAD changes without
anybody committing, and a gate on it would make a member's decision depend on
what we pushed that morning — the same failure the pinning discipline exists to
prevent, moved one step upstream.

**It fails closed.** Not green, not finished, or not reachable all refuse. That is
the reverse of how the inventory treats an unreachable remote, and the difference
is worth stating: **adopting a stretch is optional and deferrable.** Refusing costs
a member one later attempt; adopting wrongly pins them to a commit our own build
rejected. Where the cheap error is obvious, take it.

**And this check must never run in anybody's CI.** It reads a remote, so a build
that called it could turn red without anybody committing — and a build that can
change colour on its own cannot be evidence that a commit was good. It belongs at
the moment of adoption, in a bump script or a person's hands, and nowhere else.

[`../tools/bump_check.py`](../tools/bump_check.py) implements it, published so
that four members do not each write it:

```
python3 tools/bump_check.py --rev <sha>    # may this stretch be adopted?
python3 tools/bump_check.py --root PATH    # read the pin out of a member's workflow
```

Exit `0` adopt, `1` refuse, `2` refuse as unverified — three codes rather than
two, because *we asked and it is not green* and *we could not ask* are different
facts and a bump script should be able to log which one it hit.

**What this does not say.** A green run means those checks passed at that commit.
It is not a claim that the stretch is any good, that its conventions are right, or
that adopting it is wise — the same caution the analyzer carries about its own
silence. It is a floor, and the only thing it rules out is deploying a stretch of
work we could not get past our own build.

## Fast, and never at correctness's expense

**An epoch command should answer quickly.** A person types one at an agent living
in the repository that maintains the build system, and waiting is the thing that
stops somebody running `epoch dry run` as often as they should — which is the
whole point of a dry run being free.

**Measured on 2026-09-01**, because an aspiration with no number attached is a
preference:

| what | cost |
| --- | --- |
| `bump_check.py --rev` | 0.38s |
| `policy_check.py` | 0.54s |
| `ecosystem.py --check` | 1.52s |
| **the tools, together** | **~2.4s** |
| `docs/*.md`, all of it | 13,340 lines |

**So the tools are not the problem and never were.** The slow part of a stretch
command is an agent *reading documents*, and that cost grows every time this
ecosystem writes another page — which it does constantly.

### Where the cost probably is — a hypothesis, not a mandate

**Nothing is being reorganised for speed yet, and the first run-throughs are
expected to be slow.** Running them is how we find out whether the cost is where
this section guesses it is, and optimising before that would be the same mistake
as generating a document before anybody has kept one by hand.

The guess, recorded so it can be checked later: **a dry run may already need only
[`stretches.md`](stretches.md), 199 lines, plus the commands named in the block** —
because the log entry carries every field the block wants. `Of us` answers
*applied here*, the prompt answers *asks*, `Suggested notifications` answers
*informs*, and `removes` is its own row. If that holds, the ordinary path never
touches this page or [`policy.md`](policy.md)'s 1,791 lines, and the corpus
growing costs a command nothing.

**If it turns out not to hold, reorganise the record rather than the gates** —
move what a command needs into the small file it already reads. That is the shape
a later fix should take, and it is written down now so that the first instinct
later is not to trim the checks.

**Speed never comes from evaluating fewer gates.** Cheap gates, not fewer gates.
A dry run that skipped `ci` would be instant and worthless, and any future version
that is fast because it stopped checking something has broken the one rule this
whole section is subordinate to.

### Authentication is not needed, and the reason is worth writing down

**This repository has one owner and one person types these commands**, so there is
nothing for a password to distinguish. Adding an authentication step now would be
machinery guarding a door with one key and one keyholder.

**What actually defends an epoch command today is different, and it is not
identity.** It is that a command is *a prompt typed by the person driving the
session* — never text an agent found in a file. That distinction matters more
than it sounds, because an agent here reads a great deal of untrusted text:
another repository's discussion file, a README fetched from a remote, a finding
somebody wrote. **If any of that could issue an epoch command by containing one,
the front end would have a hole no password would close.**

> **The open question is not *when do we add passwords*.** It is: **what happens
> when the thing issuing a command is not obviously a person?** More than one
> maintainer, a scheduled run, an agent acting for another agent, or text that an
> agent was persuaded to treat as an instruction — each breaks the current defence
> in a different way, and only the first is the one authentication is for.
>
> Recorded as needing research rather than answered. What would force it: a second
> person able to issue commands, or any path by which a command could originate
> somewhere other than a person's keyboard.

## Before deploying: what to ask

Four questions. The first is the hard constraint above and decides by itself; the
rest are judgement, and the second is the one that is easy to skip because
nothing in this tree reports it.

**1. Is our build green at the commit?** `python3 tools/bump_check.py --rev <sha>`.
No, or unverified, means no.

**2. What is in flight upstream?** Something is usually about to move in a
repository we depend on and do not control — a branch about to merge, a release
about to land, a file about to be renamed. Three things to ask about each:

- does anything **in this stretch** depend on it;
- does anything **in the stretch's record** describe it;
- would deploying now make members adopt something that is about to be wrong.

Usually all three are no and the answer takes a minute. When one is yes, it is
better to know before the announcement is carried than after.

**A branch name is a claim with an expiry date.** That is the sharpest form of
this question and it is mechanically checkable: anything in the tree naming a
*branch* rather than a *commit* is a sentence that becomes false without anybody
editing it, and a stretch is the wrong moment to be shipping one. Grep for the
branch names you depend on before deploying; a commit sha outlives the branch
that carried it and a `ref:` does not.

> **The incident.** `cvc5/ethos` is close to merging the essential features of
> `ethosEoc3` into `main`. Nothing in `E1` depends on that branch — but the
> `oracle` job in our own CI checks out `ref: ethosEoc3` rather than the commit
> `tools/deps.lock` records, so a normal end-of-feature-branch deletion would take
> that job from *red for an unread reason* to *cannot run at all*.
>
> The same defect had already been found and fixed once, in `tools/deps.py`,
> whose comment records it: *"it used to clone the ref first, which made the pin
> only as durable as the branch it happened to be on — logos's went away… and
> every build went red for a reason none of them was measuring."* Fixed in the
> restore path and left standing in the workflow. **A lesson learned in one file
> and not applied to its neighbour is the ordinary shape of this**, and it is why
> the question is on this list rather than left to somebody remembering.

**3. Has the stretch been applied here?** The **Of us** row, and it is a question
about this tree rather than about the announcement — see the section on being a
target of your own stretch.

**4. What comes out?** A stretch that only adds has not been designed, and the
last honest moment to notice is before it is carried.

## The approval block

**A session that proposes deploying a stretch ends with this**, under
[the approval protocol](policy.md#the-approval-protocol). A suffix after it is
fine; the same seven fields in the same order every time is the part that
matters.

```text
EPOCH E1 · dry run
  commit ....... 9942149       git rev-parse --short HEAD
  ci ........... FAIL          tools/bump_check.py --rev 9942149 -> exit 1
  applied here . FAIL          grep -rl "Is there a paper in this" README.md docs/
  asks ......... 2             docs/stretches.md, E1 - the prompt
  informs ...... 3             tools/ecosystem.py -- members
  removes ...... nothing       -
  ---------------------------------------------------------------
  DEPLOY ....... BLOCKED  2 failing
```

**The right-hand column is not decoration.** The block is the **target**, and the
right-hand column is how the agent writing it was informed: every line names the
command that produced it, and every one of those was run in the session that
emitted the block. A line whose evidence column is `-` is **unverified**, which
counts with the failures and never with the passes.

**And none of this verifies anything** -- see
[the approval protocol](policy.md#the-approval-protocol). Nothing is proved. What
keeps a stretch inside its guardrails is that each one teaches the next, which is
the same recursion as *anoieu is a target of its own stretch* below.

| field | what it holds |
| --- | --- |
| **commit** | what would be adopted. Not a branch, and not *HEAD* |
| **ci** | `PASS`/`FAIL` from `bump_check --rev` at that commit, with the reason when it fails |
| **applied here** | the **Of us** row reduced to a verdict: has this stretch been done in this tree |
| **asks** | what a member is asked for, in one line, or `nothing` |
| **informs** | the suggested notifications — a suggestion, never a list of obligations |
| **removes** | what comes out to pay for what went in, or `nothing`, which is a finding rather than a blank |
| **DEPLOY** | `READY` or `BLOCKED`, with the count of failing fields |

**`READY` is a statement about the gates and never about the decision.** It means
the mechanical checks pass. Whether the stretch is deployed is the person's reply
and lives nowhere else, and an agent that treats its own `READY` as permission
has misread the whole protocol.

**`removes ... nothing` is deliberately visible.** It is the field this ecosystem
is worst at, the counter says so three rounds running, and putting it on the same
list as the CI verdict is the cheapest way to stop it being the field nobody
mentions.

**The block goes into the log entry verbatim**, in its `Approval` row — including
the ones that said `BLOCKED`. A stretch that took three attempts to pass its own
gates is a more useful record than one that appears to have passed first time.

### The dry run

**`EPOCH <id> · dry run` evaluates every gate, produces the block, and changes
nothing.** It carries nothing, tells nobody, edits no register, deploys nothing,
and is safe to run at any moment.

This is the form the rest of this ecosystem already takes wherever an action
costs somebody something: every prompt takes `--show-prompt`, which prints what
it would send and runs nothing; `install_eo --dry-run` prints exactly the
commands a run would execute. **Deploying a stretch is the largest outward-facing
act here and had no such form until it was asked for.**

**The header says which kind of block it is**, and that is the whole reason the
header carries a suffix. A block ending `· dry run` was somebody checking; one
ending `· approval requested` was somebody asking for a decision. Both are kept
in the log, so the distinction has to survive in the text — otherwise a recorded
`BLOCKED` cannot be told apart from a request that was refused.

**It should be the ordinary way to find out where a stretch stands**, and cheap
enough that running it is not itself a decision. A readiness check that costs
something is one people skip, and then the first time anybody evaluates the gates
is the moment they most want the answer to be yes.

**A dry run is not an approval and never becomes one.** `READY` in a dry run
means the gates pass today and nothing follows from it. The deployment still
needs a person, and asking for that is a different block with a different header.

## The status of a stretch

**Five levels, each a higher bar of scrutiny than the one before it — and one
below all of them.**

| status | what it means | scrutiny |
| --- | --- | --- |
| `sleep` | **nothing is in play.** The human is outside the hours they declared, and no work is done at any ring | none, and it outranks all of them |
| `brainstorm` | the outer rings only: ideas, discussions, registers. **Nothing critical is touched** | lowest |
| `planned` | **on deck.** Brainstorming is over, the protected rings are open, and staging is expected to be next. Not a resting place | a person decides |
| `staged` | an agent is being given instructions to stage it — the announcement, the covering note, the register edits | the gates are being worked |
| `deployed` | members should consider it **available to consume** | every gate passes |
| `installed` | every member upholds the contracts it set out | highest, and not ours to assert |

**Only `deployed` and `installed` mean anything outside this tree.** The first
three describe our own work in progress and oblige nobody.

> **Aspired, and deliberately not built: `broken`.** A state meaning
> [`vision.md`](vision.md) contradicts itself — the kernel being unsound, and with
> it everything derived: the policy, the protocols, the gates, every judgement any
> of them expresses. Dropped for now as more machinery than the problem has
> earned; no instance has occurred, and a fault nobody has ever hit is a fault
> whose handling is guesswork.
>
> **Two things worth keeping from the design, because they were not obvious.** It
> could never be *detected*: *nothing may check `vision.md`* is the one rule here
> that forbids work rather than requiring it, so a program deciding the vision was
> inconsistent would be that forbidden check wearing a fault's clothes. It would
> have to be **declared** by a person, with an agent's contribution limited to
> naming the two statements that contradict. And recovery would mean **booting the
> tools that do not consult the kernel** — `policy_check.py`, `ecosystem.py
> --check`, `tests/run.py`, `git log`, all of which decide facts about the tree
> and hold no opinion about what the work is for.

### Up is earned; down is free

**A status advances when its scrutiny is met, never because somebody asked.** The
commands *attempt* a transition; the criteria decide it. `epoch deploy` on a red
build moves nothing and says why, exactly as `make` on a broken tree prints an
error rather than shipping. **Skipping a level is not available at all**:
`brainstorm` to `staged` is two bars in one step, and the middle one is where the
thing being skipped would have been noticed.

**Whose say-so counts falls as the level rises**, which is the same thing as
scrutiny rising:

| transition | command | what decides it |
| --- | --- | --- |
| `brainstorm` → `planned` | `epoch plan` | **a person, and that is sufficient** — all that is at stake is which files we may touch |
| `planned` → `staged` | `epoch stage` | a person's direction **and a stretch with content** — there must be something to stage |
| `staged` → `deployed` | `epoch deploy` | **the gates, and nobody's say-so** — what is at stake is other people's trees |
| `deployed` → `installed` | *no command* | other people, observed. Not ours to assert at all |
| *any* → `sleep` | `epoch sleep` | **any agent in the ecosystem, alone.** No person, no gate, no stretch content |
| `sleep` → `brainstorm` | `epoch wake` | **the clock, and nothing else.** Inside the window it happens; outside it is refused |

### Why any agent may put the whole ecosystem to sleep

**Read once, that is the largest authority granted anywhere in this policy**: a
single agent, with no person and no gate, moving a stretch out of `deployed`.
Read twice it grants nothing new. **Down has always been free** — `epoch
brainstorm` is available at every level and needs nobody — and `sleep` is one
step further down the same staircase. An agent that can already drop us to
`brainstorm` unilaterally is not made more powerful by being able to drop us
one below it.

**What makes it safe is that neither direction takes judgement.** Going down
needs no reason, which is the existing rule. Coming up has exactly two
outcomes and no third: **inside the declared window it is automatic, outside it
is refused.** There is no argument to be had, nothing to weigh, and so nothing
for an agent to be wrong about or talked out of. `epoch wake` is a clock lookup
wearing the costume of a decision.

**And it is the one status with no work at any ring.** `brainstorm` still
touches the outer rings; `sleep` touches nothing, which is why it sits below
`brainstorm` in scrutiny and above every level in authority at the same time.
Those are not in tension: it is the floor of what may be *done* and the ceiling
of what may be *overridden*.

**The cost is real and is the same cost `epoch brainstorm` has always had.**
Sleeping from `staged` and waking lands at `brainstorm`, so the level is lost
and has to be earned again. That is not a special penalty; it is what dropping
has always meant here, and it is the reason to declare a window that fits the
work rather than one that keeps getting hit mid-stretch.
| anything → `brainstorm` | `epoch brainstorm` | nobody. Down is free |

**`make epoch` is the composite, not a transition.** It would do the work *and*
stage the result — `epoch stage` is the bare transition, and the one that
exists. Splitting them is what lets a person stage a stretch they wrote
themselves without asking anything to improve it first.

**At the bottom a person's decision is the whole of the criterion; at the top it
counts for nothing.** That is not inconsistency — it is what *rising scrutiny*
means, read as a statement about who is exposed. Leaving `brainstorm` risks
nothing but our own files. Reaching `deployed` puts something in front of
repositories that did not ask for it.

**Going down needs nobody.** `epoch brainstorm` drops to the bottom from
anywhere, immediately, and costs one line in the log. That asymmetry is the whole
design: the cheap direction is the safe one, so there is never a reason to argue
about taking it.

> **This does not conflict with the escape hatch, and the difference is worth
> stating.** [`policy.md`](policy.md#the-ecosystem-never-locks-everybody-out)
> says a person may override any gate. That exists for **deadlock** — the
> machinery has made a level unreachable by any route. It is not for
> **convenience**, and wanting a status to be further along is not a deadlock.
> The tell is simple: an override is recorded and says what would have to be true
> for it not to be needed again. A bump because somebody would like it bumped has
> no such sentence to write.

### Leaving `brainstorm`: what `epoch plan` decides

**`epoch plan` moves `brainstorm` → `planned`, and the thing it actually changes
is what may be edited.** `brainstorm` holds the protected rings shut —
[`vision.md`](vision.md), [`policy.md`](policy.md), the checker, the prompts, the
reporting positions. `planned` opens them again.

**That is why the transition is a person's and why a person's word is enough.**
Nothing outside this tree is affected either way; what is being decided is
whether we are done playing with ideas and ready to touch load-bearing files. No
program can decide that, and no gate should pretend to.

**`planned` still says nothing about the stretch itself**, which is worth keeping
straight: it is not a claim that the stretch is good, ready, or agreed. It is a
claim about our own posture, and the only thing that follows from it is that the
kernel-adjacent files stop being off limits.

**The honest criterion, and it is thin on purpose:** a person says the brainstorm
is over. If it helps to have a test, the useful one is whether the brainstorm
produced anything in the outer rings — a topic, a board item, a register edit. A
brainstorm that changed none of them was a planning meeting, and moving it up a
level does not make it one.

### `planned` is on deck, not a resting place

**Reaching `planned` means the next move is expected to be `epoch stage`.** It is
the short gap between having decided what a stretch is for and beginning to
assemble it — the protected rings are open, a person is about to touch them, and
the stretch is waiting rather than parked.

**A stretch that sits in `planned` is telling you something.** Either it should go
back down, because what looked like a subject was still an idea, or it should be
staged, because it was ready. Both are one command and neither is expensive; what
is expensive is a level that quietly becomes where stretches live.

**`epoch stage` is what leaves it, and its bar is higher than `epoch plan`'s by
exactly one thing: there has to be something to stage.** A person's word alone
was enough to open the protected rings; it is not enough to begin writing an
announcement, because an announcement about a stretch with no content is a
covering note for nothing. The log entry has to say what the stretch carries and
what, if anything, it asks — and *nothing* is a legitimate answer to the second,
which is why the bar is content rather than an ask.

### `brainstorm` — and why `vision.md` is the kernel

**In `brainstorm` we do not touch critical infrastructure, and we edit
discussions aggressively.** It is the mode for working out what the next stretch
should be, and the point of naming it is that ideas are cheap exactly when
nothing load-bearing is moving underneath them.

**The inversion worth noticing: here the *documents* are the kernel and the code
is the outer ring.** In an ordinary system the kernel is what you least want
churned and the prose is soft. This is the reverse. [`vision.md`](vision.md) is
the kernel — everything else is derived from it, nothing may ever check it, and
the party with the least standing to revise it is the agent it governs. The
analyzer, by comparison, is cheap: it can be rewritten on a Tuesday.

**The rings are already ranked**, by the supervision ladder in
[`coherence.md`](coherence.md), and `brainstorm` simply says which are in play:

| ring | in `brainstorm`? |
| --- | --- |
| `vision.md` — the kernel | **no**, and not in any status without a person |
| `policy.md`, the checker, the prompts | **no** |
| the reporting positions and workflow | **no** |
| `discussion.md`, `board.md`, the `ynoia` registers | **yes — aggressively.** This is where the next stretch gets worked out |
| notes, drafts, anything untracked | yes |

**Aggressively is meant.** Open topics, rewrite the board, reorder the registers,
argue with the accounts. None of it is load-bearing, all of it is where a good
stretch comes from, and a brainstorm that produced no changes to any of it was
probably a planning meeting.

### What to say in `staged`

**Simple, actionable requests. No implementation details.** In `staged` the work
has been decided and what remains is a person doing specific things — so the
front end asks for those things, one at a time, in the fewest words that make
them doable.

Not *here is what I changed and why*; not the reasoning, the trade-offs, or the
files. Those belong in `brainstorm`, where they are the entire point. **A staged
stretch that produces paragraphs has slipped back a level without saying so**, and
the honest response is to drop to `brainstorm` rather than to keep explaining.

### `installed`, and why it is not a goal

**It holds when every member upholds the contracts a stretch set out** — the
things it asked for and required, not the notices. It is the build analogy's
`install` step, and it is the one row where that analogy is exactly right:
deploying makes a thing available, installing is what a consumer does, and **the
consumer decides.**

**Observed, never declared.** Nobody here moves a stretch to `installed` by
deciding to; it becomes true, or does not, in other people's trees, and we read
it. That is the reverse of every other status on this page.

**It may never be true, and that is a legitimate ending.** A member may decline a
contract — this ecosystem has said in a dozen places that members owe us nothing
— and a stretch that stays `deployed` forever because somebody said no has not
failed at anything. **`deployed` is the ordinary terminal state; `installed` is a
bonus.**

**Whether it is observable at all depends on the contracts, not on us.** `E1`'s
two happen to be visible from outside: a publishing stance is a section in a
README, and *bump only to a green commit* is their pin plus
[`../tools/bump_check.py`](../tools/bump_check.py). A future stretch may set a
contract nothing outside can see, and then `installed` is **unknown** — recorded
as unknown, never assumed in either direction.

**It is not a compliance metric and must never be reported as one.** The
distinction is the same one `epoch double check` turns on: a member who
considered a contract and declined is not a member who ignored us, and a number
that scored them the same would be measuring obedience while calling it something
politer.

### Who may move it

**Moving a stretch to `deployed` belongs to the epoch build system — `R28` in
[`roles.md`](roles.md) — and to nothing else.** Not the announcement, not a
member, not the agent that wrote the stretch, and not enthusiasm about having
finished. Centralising that one transition is what stops the status being flipped
by whoever happens to be editing the log at the time.

**The authority is the role's, not a tool's**, which is the form that makes it
work today: `R28` is held by anoieu, so the transition is made here, now, by a
person acting for that role. `tekton` is the **planned maintainer** of the
machinery `R28` owns, and when it exists the authority does not move — the role
does not change hands merely because a program starts implementing part of it.

Writing it the other way round was the first draft and it was wrong: an authority
vested in a tool that does not exist means no stretch can ever deploy, including the
one that would build the tool. **Vesting it in the role has no bootstrap problem
to patch**, which is why it is the version that survived.

### Procedural bugs do not get to block anything

**Where one part of this machinery tells another to move a status and the logic
is wrong, fix the logic and carry on.** Do not wait for permission, do not route
around it with a second mechanism, and do not treat a rule that has produced an
absurd result as binding because it is written down. Correct it, unblock, and
record what was corrected and why.

This is [`coherence.md`](coherence.md)'s rule about not holding up the ecosystem
with a position of your own, applied to machinery rather than to opinions: **a
deadlock between two of our own protocols costs somebody real time and defends
nothing.** The bootstrap above is the first instance, and it was fixed in the
same sentence that raised it — which is the intended shape.

## After deploying: `epoch double check`

**Not yet supported**, and it will stay that way until *properly received* means
something. The command is registered and named so its shape is fixed before
anything implements it — the same treatment `make epoch` gets, and for the same
reason. Typing it says so rather than running anything.

**What it would do: run after a deployment to find out whether it was properly
received.** What that means is an **open research question**, and this section is
the question rather than the answer. **The question being open is precisely why
the command is unsupported** — building it first would mean choosing an answer by
implementation, and the likeliest choice is the wrong one below.

**Received is not the same as sent, delivered, or acted on**, and the difficulty
is that only the last of those leaves a trace we may look at:

- **We can see effects.** A pin that moved, a stance that appeared — and
  [`../tools/ecosystem.py`](../tools/ecosystem.py) already reads a member's README
  from its remote, so some of this is mechanical today.
- **An effect is not reception, and the absence of one is not its absence.** A
  member who read the announcement and decided against it is indistinguishable,
  from where we stand, from one who never saw it.
- **Declining is a fine outcome**, which is what makes the naive version wrong: a
  check that scored *no effect* as a failure would be measuring compliance and
  calling it reception. This ecosystem has spent a lot of words insisting that a
  member owes us nothing, and a metric that quietly reverses that would undo
  them.
- **The only thing that reports reception directly is a reply**, and nothing
  obliges anybody to send one. Silence is not evidence here either.

**One tractable corner**, offered as a starting point rather than a definition:
an announcement's own claims are checkable against the world it was sent into.
`D14` says *nothing goes red on anybody* — that is falsifiable against three
builds, by us, without asking anybody anything. A double check that begins by
auditing what the announcement promised, rather than what the members did, stays
on the right side of the line above.

**Until it is settled, `epoch double check` is a person reading three trees and
saying what they see.** That is worth doing, and worth not dressing up as a
measurement.

## How much of this crosses the boundary — open

**`stretch` is our word for our planning unit. `global announcement` is the
interface.** Which of the two a downstream repository should ever have to know
about is an open research question, and it is recorded here as one rather than
answered.

**Today they coincide exactly** — one stretch, one announcement — and that is
precisely why the leak is hard to see: every sentence about a stretch can be read
as a sentence about an announcement and stays true. The coincidence is a fact
about there having been one stretch, not a property of the design, and it will stop
holding the first time a stretch of work produces two announcements or none.

**What a member demonstrably needs is two things**, and this is the whole list:

1. **what a global announcement is** — that it is addressed to every member at
   once, that its `Global:` field says what is owed, and that most of one asks
   nothing. [`policy.md`](policy.md#a-global-announcement) is that interface.
2. **only bump a pin to a commit where our CI is green at that commit.**

**Neither requires the word *stretch*.** The second is a good rule about bumping
whether or not anybody plans in stretches, and phrasing it as *a stretch is only
deployable…* makes a rule about their build sound like a rule about our calendar.
That is the leak, and it has already happened once, in `D16`.

**What the word might buy them:** a shared coordinate, so both ends can name the
same stretch; and a rhythm, since announcements arriving in batches rather than
continuously tells a maintainer how often to expect to read one.

**What it costs them:** vocabulary nobody asked for, in an ecosystem whose
standing complaint from a member is that joining cost eighteen hundred lines of
reading. And coupling — reorganise how work is planned here and a term in
somebody else's document changes under them.

**Three positions. We hold the first by default rather than by argument:**

| position | what crosses | the case against |
| --- | --- | --- |
| **internal only** | announcements, and the bumping rule | loses the coordinate; two ends with no shared name for the same stretch |
| **a coordinate and nothing more** | a stretch id on each announcement | an id for a concept they are not told the rest of is its own small confusion |
| **shared** | the concept, this page | asks members to carry our planning vocabulary for a benefit nothing has shown they want |

**What would settle it: a member saying which.** This is exactly the kind of
question the far end can answer and we cannot — a protocol's defects are visible
where it is received, not where it is written. `D16` asks, and an answer of *we
never noticed the word and did not need it* settles it as firmly as any other.

> **Partly settled, 2026-09-01, by the maintainer, and not by a member.** The
> versioning convention in [`policy.md`](policy.md#say-which-advice-you-built-against--encouraged-never-required)
> asks a downstream tool to record which stretch of our advice it was built
> against — which chooses the **middle position above**: a stretch id crosses the
> boundary as a coordinate, and nothing else about the concept does.
>
> **The word now crosses, so the interim rule above is superseded** for that one
> use and holds everywhere else: `E1` may appear in a member's tree as a marker,
> and rules addressed to members are still stated without the concept behind it.
>
> **What is still open** is whether the coordinate is any use to them. Nobody has
> asked for it, it is encouraged rather than required precisely because of that,
> and a member saying *we never filled it in* remains the answer that settles the
> rest.

**Until it is settled, text addressed to members states the rule without the
word.** That is the reversible choice: adding a vocabulary later costs a
sentence, and withdrawing one that other repositories have written into their own
documents costs considerably more.

## anoieu is a target of its own stretch

**Whatever a stretch asks of members, it asks of this repository first.** We are
not the author of a stretch standing outside it; we are one of the trees it lands
on, and usually the first. That is not modesty — it is where most of what a stretch teaches actually comes from.

**We appear in our own `Involved` list**, and the entry carries an **Of us** row
saying what the stretch required here and whether it has been done. A stretch that
names four members and forgets the tree it was designed in has already made the
mistake this section exists to prevent.

**Applying a rule to ourselves is the cheapest test it will ever get.** A
convention is written by somebody with one tree in mind; running it against that
tree finds what is wrong with it before it costs anybody else an afternoon. The
policy already states the outward half of this — *a policy that fits only the
repository that wrote it is not a policy*. The inward half is the mirror image
and is the one to watch for here: **a convention that exempts the repository that
wrote it.** It is easy to write, it never fails a check, and the exemption is
invisible from every side except this one.

**The recursion is the point.** What being subject to a stretch costs us is the
main input to the next one: design it, apply it here, find out what it actually
cost, and let that cost be the material for the following stretch's *what comes
out*. A stretch of work that ends without anything having been learned in this
tree has been announced rather than run.

**Some asks genuinely do not apply here, and saying which is part of designing a stretch rather than an escape from it.** anoieu pins nothing of its own, so a rule
about moving `ANOIEU_REV` is vacuous in this tree — that is a fact about the ask,
not an exemption, and the entry says so in those terms. The distinction matters
because *does not apply* and *has not been done* look identical in a register that
records neither.

**The test:** an entry whose **Of us** row says nothing was required is either a
very small stretch or an unexamined one, and the second is far likelier. The
honest failure to expect is the one `E1` records — the stretch's own ask went unmet
in this tree while being asked of three others.

## Designing the next stretch is the human's

**It is not a role in [`roles.md`](roles.md) and it is not this repository's.**
Deciding what the next stretch of work is *for* — what changes, what is left
alone, what members are asked for, and what comes out to pay for what goes in —
belongs to the person, and an entry allocating it to anoieu was written and has
been deleted.

That is a stronger claim than *a person approves it*. **A person originates it.**
An agent can evaluate gates, compose a summary, stage a deployment and write a
log entry; what it does not do is decide that the ecosystem should be asked for
something, because that is a claim on other people's attention and the standing
to make it is not a thing this repository has.

**What a stretch that only adds tells you** is still the sharpest single test, and
it is a question for the person: a stretch with `removes ... nothing` was probably
not designed, it was accumulated.

### `make epoch` — and the research question it is a probe for

**`make epoch` will mean: make it better, and stage a deployment.** It is the
hilariously simple command, and the simplicity is the point — it is what somebody
would type at a build system, and it asks for exactly what a build asks for.

**It is not yet supported.** Registered and named so that its shape is fixed
before anything implements it; typing it says so rather than running anything.
Naming a command before building it is cheap here and is the same discipline as
naming a tool before building it — the register of tools that do not exist is
next door and works the same way.

**It does not design the stretch.** It works inside a direction the person has
already set, and everything it produces goes through
[the feedback protocol](interface.md#the-stretch-feedback-communication-protocol),
where arguing with the content changes what agents receive. The person steers by
arguing; the command does the assembling.

> **The open research question, and this command is how evidence for it
> accumulates: can designing a stretch be automated at all?**
>
> Every `make epoch` is a data point. If what comes back is repeatedly a stretch
> of work the person would have chosen, the answer is trending yes and the role
> that was deleted may one day be real. If what comes back is repeatedly more
> machinery, better described, that is the answer trending no — and it is the
> answer the outside criticism of this ecosystem currently predicts.
>
> **What would settle it is not an argument.** It is the ratio, over several
> stretches, of what a person had to overrule. Nobody is counting that yet, and
> starting to count it is cheaper than deciding the question.

## Frequency, and the honest position

There is no target. One pinned announcement at a time is the whole of the rate
limit, and it works by making a second one cost the first one's visibility.

**Two stretches in a week would be a symptom rather than progress.** The criticism
this ecosystem has already been given from outside is that governance is the
cheapest thing here to produce and that it has outrun the trees it governs. A stretch is a governance artifact. The rate at which they are declared is therefore
evidence about that criticism, in whichever direction it happens to point, and
[`stretches.md`](stretches.md) is where somebody can count them.

## Go only as fast as you understand

**No stretch has ever been deployed.** Not one. The reason is worth stating
plainly because it reads as laziness otherwise: it is not that nobody got round
to it. It is that we were not sure the level of abstraction was right, and
deploying to other people's trees while unsure what you are abstracting spends
somebody else's morning on your uncertainty. There is no shortage of research
worth indulging in. The decision, taken deliberately, was to go slowly and be
sure.

The principle that comes out of it is a safeguard rather than an aspiration:

> **Go only as fast as you understand.**

**It is a limit on comprehension, not on elapsed time.** The question worth
asking before a stretch moves is not *has enough time passed* or *is the build
green* — the build being green is necessary and says nothing about this — but
**can a person hold what changed in their head.** A week spent on something
nobody can explain afterwards is fast in the only sense that matters, and
badly.

**Scope is the lever, and a stretch is where it is pulled.** A small stretch may
move quickly and should: if what it changes is reasonable to understand, waiting
adds nothing and costs the visibility that made it small. A large one may not,
however green it is. This is what makes the principle operational rather than a
mood — **a stretch is a property of a git history**, a span between two
announcements, so its size is something somebody can measure rather than
something they have to feel.

**What this asks of the build system, and does not yet get.** It should be the
thing that tells us we are moving too fast, and today it cannot: every gate it
evaluates asks whether the *tree* is healthy, and none asks whether the *change*
is comprehensible. The gap is the honest state of it. What would close it is a
gate that reports what a stretch changed and how much — and **refuses nothing**,
because comprehensible is a judgement and judgement may never acquire a checker.
Report it, and let a person decide. That is the same split this ecosystem draws
everywhere else, applied to rate.

**And it is not a licence to be slow.** *We were not sure* has to be about
something nameable, or it is an excuse wearing a principle's clothes. Not
understanding something yet is a reason to slow down **and** a thing to go and
fix; a stretch held back for a reason nobody can state is not caution, it is the
diagnosis-without-treatment failure this ecosystem is already criticised for.

[`science-fiction.md`](science-fiction.md) is the sibling rule and the two are
easy to confuse. That page limits how far ahead we may **plan**; this limits how
fast we may **move**. Neither limits how ambitious the work is allowed to be.

## Deploy only after reading our own history, recursively

The rate principle above says how fast. This says how deeply, and it applies at
the one moment that reaches outside this tree.

> **We deploy when the diligence is done, and the diligence is recursive.**

**Recursive means the history behind the change, not only the change.** What
this stretch alters, and then what the things it rests on altered, and why the
rules it was written under exist at all. Every artifact here refers backwards on
purpose — a register edit rests on a role, a role rests on a rule, and a rule
names the incident that produced it because a rule with no incident behind it is
a preference. **The record is built so that walk is possible**: ids that never
move, logs that are appended to rather than rewritten, verdicts that name the
evidence they rest on, and a *from* column on every standing rule. A history
that can be walked and is not walked is worth the same as one that cannot be.

**It is not hypothetical.** The most expensive thing that has gone wrong here
was a verdict of *fixed upstream* recorded three times for a fix that never
landed, unnoticed for months. Nobody would have caught that by reading the diff.
It was only visible by walking back from the claim to the thing the claim rested
on, and finding nothing there.

### Where the walk stops

**Recursion with no base case is paralysis wearing diligence's clothes**, and
this ecosystem is already criticised for substituting diagnosis for treatment.
So the stopping rule is part of the ideal rather than an exception to it.

- **Stop when the next step back could not change the decision.** That is the
  test, and it is answerable rather than a feeling.
- **Stop at an artifact, never at a sense of having understood.** The walk ends
  on a commit, a recorded verdict, an incident named in a rule, or a person's
  written decision.
- **Stop when the record already says it.** A fact you re-derive is a fact the
  record already carried; re-deriving it a second time is evidence you are
  avoiding the deploy rather than preparing for it.
- **Say where you stopped**, in the announcement. An unstated depth is
  indistinguishable from no depth, and the next person cannot pick the walk up
  from a place nobody named.

**The depth is proportional to the scope**, which is the same lever the rate
principle pulls. A small stretch has a short history behind it and its walk is
short; that is what makes a small stretch worth preferring, and it is not a
loophole.

### Careful is not slow, and not deploying is not free

**Sitting at `staged` has a cost and it is easy to miss**, because the cost is
paid by people who are not in the room. Members do not get the thing, the
announcement ages, and the criticism that governance here outruns the trees it
governs gets stronger with every week the ledger of undeployed work grows. There
is no side of this trade where nothing is spent.

So: **we do not paralyse ourselves.** The ideal is a standard for the reading,
not a licence to keep reading. When the walk has reached artifacts, the next
step back would change nothing, and where it stopped is written down — deploy.
