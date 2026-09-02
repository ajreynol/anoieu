# Methodology

**How a practice gets from this repository into somebody else's tree, and at
what rate.** The mechanism, operationally: what is distributed, by what means,
what a member has to do to consume it, and what stops any of it from being
imposed.

Three neighbours, so this page can stay narrow. [`linker.md`](linker.md) is what
this repository holds; [`ai-novelty.md`](ai-novelty.md) is why those mechanisms
are shaped as they are; [`science-fiction.md`](../science-fiction.md) is how far
ahead we may plan. This one is the distribution mechanism and nothing else.

## The problem

Six repositories, different owners, no shared build, no central authority, no
package to depend on, and most of the writing done by agents under light
supervision. Getting *code* between them is solved and boring. The question this
ecosystem actually has is harder: **how does a practice get into a tree whose
owner did not write it, without anybody being able to impose it?**

The two ordinary answers both fail here.

**A document fails because it is not executable.** A style guide, a contributing
page, a set of conventions — somebody has to read it, agree with it, and keep
agreeing with it while it changes underneath them. Nothing tells them when they
have drifted, and nothing tells us either.

**A service fails because it takes control.** A bot on the organisation, a
hosted check, a required status — these work, and they work by removing the
member's ability to decline. That is a fine trade in a company and the wrong one
between independent repositories, where the ability to decline is the thing that
makes adoption mean anything.

## The mechanism that already works

One thing in this ecosystem has actually crossed the boundary and is running in
other people's builds. It is worth describing exactly, because everything below
is a generalisation of it and of nothing else.

**`tools/policy_check.py`, fetched at a pinned commit and run by the member.**
In their own workflow, a member clones this repository at a commit they chose,
checks it out, and runs the checker against their own tree:

    ANOIEU_REV: <a commit of anoieu>
    git clone ... /tmp/anoieu && git -C /tmp/anoieu checkout "$ANOIEU_REV"
    python3 /tmp/anoieu/tools/policy_check.py --root .

Six properties make that work, and they are the whole of the method:

| property | what it buys |
| --- | --- |
| **it is a program, not a page** | agreement is not required; the exit code decides, and drift is reported the day it happens |
| **it takes the tree as an argument** — `--root` | it can run anywhere, against anything, including trees it was not written for |
| **it is pinned to a commit** | nothing moves under a member's build without a commit near them. A build that can turn green on its own is not evidence |
| **the member moves the pin** | at a moment they choose, or never. Declining a version costs them nothing |
| **the interface is tested here** | `tests/run.py` runs the checker against a synthetic compliant tree and a synthetic non-compliant one, so the published surface is exercised at home rather than trusted |
| **it prints what it cannot decide** | every run lists the rules no program can settle, so a pass never reads as more coverage than it was |

**And one negative property, which is load-bearing.** `tools/bump_check.py` —
the program that decides whether a member *may* move their pin — **must never
run in CI**, because it reads a remote and a build that can change colour
without a commit cannot be evidence. It is a command a person runs at the moment
of adoption. Distribution and verification are separate acts, on purpose.

## Distributing command line tools to members

**The generalisation, and it is not built.** Today the epoch commands exist in
exactly one tree. Reaching `staged` is something only this repository can do,
because both the machinery and the surface a person types at live here. Every
other member has the policy checker, the reporting loop, and no command line of
its own.

**What distributing them means, operationally.** A member should be able to run
a verb in its own tree, against its own state, and get an answer — with no
install step, no package, no registry, and no service:

1. **The definition stays in one place.** The command set and the status
   vocabulary are tables in this repository's documents, and `tests/run.py`
   compares every restatement of them against those tables. A member does not
   receive a copy of the table. It receives the tool that reads it.
2. **Git is the distribution channel**, because every member already has it and
   a commit is already a version. Clone shallow, check out the pinned revision,
   run out of the clone. There is nothing to install and nothing to uninstall.
3. **The command runs against the member's tree**, named as an argument the way
   `--root` already is. A command that assumes it is running inside its own
   repository cannot be distributed, and that is the single most common reason
   one cannot.
4. **Exit codes are the contract**, not the internals. `0` proceed, `1` refuse,
   `2` could not be established — the shape `bump_check.py` already publishes.
   A consumer scripts against those and never against the printed text.
5. **The printed shape is documented and compared.** Output that another tool or
   another agent reads is a surface, and a surface that restates a register is
   compared against it by a test that lives with the surface.
6. **Anything that reads a remote is a person's command.** It may be
   distributed; it may not be wired into a build.
7. **The member chooses the version, and may decline it.** Moving the pin is
   their act at their moment, `bump_check.py` decides whether the commit is
   eligible, and a member that never moves is in a supported state rather than
   a stale one.

**What makes a command distributable**, as a checklist, because most of the work
is deciding that a command is not yet:

- it takes the tree as an argument and reads only that tree;
- or it names the remote it reads, and then never runs in a build;
- its exit codes are documented and stable;
- its output shape is documented, and something compares any restatement of it;
- it keeps no state outside the tree it was pointed at;
- it fails closed — cannot-establish refuses rather than passes.

## Why this is worth writing down

Stated narrowly, because the broad version would be an overclaim.

**Pinned dependency distribution is ordinary.** Every package manager does it,
and nothing about the mechanism above is an invention. What is unusual is the
**thing being distributed**: not a library, but the rules a repository is judged
by — arriving as a program the judged party fetches, at a version they choose,
which they may decline, and whose author is subject to it too.

That produces a property most governance arrangements do not have. **The
standard cannot be changed under you.** A rule added here reaches a member when
they move a pin and not before, so the cost of a new rule lands at a moment they
picked. It also means a rule that nobody adopts is visibly unadopted, which is a
feedback signal a mandated standard destroys.

**The honest limit.** This is demonstrated for one program, across four trees,
by an ecosystem that wrote both ends. The epoch commands have zero members and
have never been distributed to anybody. A distribution mechanism with one
publisher and one artifact is a pattern, not a platform, and calling it a build
system today is the overclaim to watch for.

*What would show the generalisation is real:* a second tree running one of these
commands that it did not write, against its own state, and its maintainer acting
on the answer. Nothing has done this.

## The rate this runs at

**Go only as fast as you understand.** The principle is stated in full in
[`stretch-policy.md`](../stretch-policy.md), and it belongs on this page because it
is what stops the mechanism above from being used badly.

Distribution makes it cheap to push a change into other people's builds — that
is the point of it — and cheapness is exactly the property that turns a method
into a liability. The pin is the structural half of the answer: a member absorbs
a change when they choose. **The rate principle is the half that is ours.** No
stretch has been deployed yet, deliberately, because we were not sure the
abstraction was right, and shipping an abstraction you cannot explain is how the
mechanism above becomes a way of distributing confusion at scale. The diligence
owed before a deploy is **recursive** — the history behind a change and not only
the change — with a stated stopping rule so that it ends in a deployment rather
than in more reading; both are in
[`stretch-policy.md`](../stretch-policy.md).

Scope is the lever: a small change may move quickly, a large one may not, and
the size of a change between two announcements is a measurable property of a git
history rather than a feeling. What the build system should eventually do is
**report** that size and refuse nothing, because whether a change is
comprehensible is a judgement, and judgement here never acquires a checker.
