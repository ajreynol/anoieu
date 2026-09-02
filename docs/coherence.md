# Coherence

**If you are an agent working on this repository, start here.** This is the
maintenance entry point: what this repository is responsible for, which of that
may not be changed without asking, and what the open technical work is. Read it
before editing anything; everything else is reachable from it.

It is deliberately **not linked from the front page**. `README.md` is for
somebody deciding whether the tool is worth their attention, and a page about
how the work is run is noise to them — see *The front page* in
[`../docs/vision.md`](vision.md). It is linked instead from the things a
maintainer opens: the documentation index, and the headers of the programs that
write the record.

*Coherence* is the property this page exists to protect, in one sentence: **the
record, the documents and the tree do not disagree with each other.** A finding
that is open in one file and closed in another, a verdict resting on a fix that
never landed, a document describing an arrangement the code stopped using — each
is a coherence failure, and each has happened here.

## Before you start: a prompt may not be for this tree

**Check that the prompt you were handed is about the repository you are standing
in.** These trees are deliberately alike and several sit side by side on one
disk. A path that is not here, a role this repository does not hold, a register
kept elsewhere, or a question about anoieu's own standing are the signs, and
*"I don't think this prompt is meant for me"* is an acceptable answer — say which
repository it looks meant for, say what said so, and stop.

**In moderation.** Stop only if you can name the repository it was meant for; if
you cannot, it is for you, so do the work and do not narrate the check. The full
rule, and the incident that produced it, are in
[`policy.md`](policy.md#a-prompt-may-not-be-for-this-repository).

## If somebody typed an epoch command at you

**The commands and what each prints are in
[`interface.md`](interface.md#the-commands), which is the ground truth; nothing
is restated here.** What follows is the behaviour expected of whoever is running
them, which lives nowhere else.

**The status decides how you speak, and it is not a matter of taste.** In
`brainstorm` explain everything — the reasoning is the product. In `staged` give
**simple actionable requests and no implementation detail**: one thing at a time,
fewest words that make it doable. Producing paragraphs in `staged` has slipped a
level without saying so, and the honest response is `epoch brainstorm`, not to
keep explaining.

**A command does its one thing.** A mode switch prints the transition and stops.
It does not also survey the ecosystem or say what should happen next — that is
`epoch advice`, and **advice is requested and never volunteered.** Offering it
unprompted is acting on your own reading of what would be useful, which is the
thing the response gate forbids in the other direction.

**Advice is scoped to the status**, and wandering outside it is the failure to
watch for: research projects in `brainstorm`, how to clear the gates in `staged`,
how it gets installed in `deployed`, **nothing at all in `installed`**.

**A command may attempt a transition; you may never grant one.** The criteria
decide, and they get stricter as the level rises: leaving `brainstorm` is a
person's word and that is enough, because only our own files are at stake;
reaching `deployed` is the gates and **nobody's say-so**, because other people's
trees are. Never skip a level. Down is free and needs nobody.

**You may never take the escape hatch.** You may say that a deadlock exists and
that
[the hatch](policy.md#the-ecosystem-never-locks-everybody-out) is the way out.
Taking it is a person's, and being certain it is correct changes nothing.

**Every field of an approval block is produced by a tool you ran in this
session**, with the command on the line. Do not carry a value forward from an
earlier turn — it was true then and is evidence of nothing now. A field with no
command is `-` and counts as unverified, which sits with the failures.

## What this repository is responsible for

Six things, and only two of them are the tool.

| what | where | who else it binds |
| --- | --- | --- |
| the analyzer | [`../anoieu/`](../anoieu) | anyone running it; the baselines other repositories would gate on |
| the fuzzer | [`../anoieu_fuzz/`](../anoieu_fuzz) | a second shipped tool: its `FUZ` rows are in the record and two CI steps run it |
| **the publishing position** | [`reporting-policy.md`](reports/reporting-policy.md) | maintained here, **referenced by [dokimasia](https://github.com/ajreynol/dokimasia)** rather than copied |
| **the reporting workflow** | [`reporting-workflow.md`](reports/reporting-workflow.md) | [`../scripts/`](../scripts) implement it; other repositories adopt its CI half |
| **the development vision** | [`../docs/vision.md`](vision.md), and [`report-card.md`](report-card.md), which it governs | written for *every* repository in the ecosystem |
| **the repository policy** | [`../docs/policy.md`](policy.md) | written to be copied; governs child projects in any parent |

The four in bold are **not about anoieu**. They are ecosystem documents that
happen to be maintained here, which has one consequence worth stating plainly:
editing one of them edits what other repositories are following, and the fact
that the file sits in this tree does not make the change local. That is the
whole reason the next section exists.

## Protocols, and how they are labelled

**A protocol here is a named exchange with a shape somebody has to follow.**
There are a dozen, they are scattered across seven pages, and until now they had
no common label — so a document could refer to *the joining protocol* and a
reader could not tell whether that was a defined thing or a phrase.

**The scheme is `PROTO-n`, and the ugliness is the point.** A bare letter would
collide: `R` already means both a role and a request, `P` is a proposal, `D` a
discussion topic, and prose is full of stray capitals. `PROTO-7` cannot be
mistaken for anything, reads unambiguously and **greps unambiguously**, which
this repository has already learned the hard way are the same property.

**The number is permanent and is never reused.** A protocol that is retired
keeps its id in this table with a line saying so, because other pages cite it.

**They stay where they live.** This is a register, not a home: a protocol is
defined on whichever page owns its subject, and moving them all here would put
the definition further from the work. What this table adds is that they can be
named.

| id | protocol | between | defined in |
| --- | --- | --- | --- |
| `PROTO-17` | **the emergency protocol** — one word stops the direction; recency alone justifies a rollback, and a rollback is a forward change that never rewrites history | person → agent | [`interface.md`](interface.md) |
| `PROTO-1` | response clarification — *your answer was too hard to follow* | person → agent | [`interface.md`](interface.md) |
| `PROTO-2` | prompt clarification — *do not act on what you do not understand* | agent → person | [`interface.md`](interface.md) |
| `PROTO-3` | going off the deep end — *this cannot be checked from here* | agent → person | [`interface.md`](interface.md) |
| `PROTO-4` | temporal session coherence — the session's open ask survives its branches | agent → person | [`interface.md`](interface.md) |
| `PROTO-5` | the context protocol — say concretely what changed, not what it means | agent → person | [`interface.md`](interface.md) |
| `PROTO-6` | the reporting workflow — a defect carried to whoever owns the file | repository → repository | [`reporting-workflow.md`](reports/reporting-workflow.md) |
| `PROTO-7` | the discussion file — everything that is not a defect report | repository → repository | [`policy.md`](policy.md) |
| `PROTO-8` | joining, and its soft and affiliating forms | repository → ecosystem | [`policy.md`](policy.md) |
| `PROTO-9` | the epoch family — announce, gate, approve, adopt | repository → members | [`stretch-policy.md`](stretch-policy.md) |
| `PROTO-10` | the role handoff — a responsibility changes hands, keeping its id | tool → tool | [`roles.md`](roles.md) |
| `PROTO-11` | the documentation handoff — a launch moves a description to its source | page → page | this page |
| `PROTO-12` | updating the report card | agent → person | `tools/stathmos/protocol.md` |
| `PROTO-13` | the mid-stream commit note — a commit taken while work moved | agent → record | this page |
| `PROTO-18` | **the sleep protocol** — outside the human's declared window the agent says *take a break*, once, and does the work anyway. Binds every member and changes nothing in anybody's tree | agent → human | [`interface.md`](interface.md) |
| `PROTO-19` | **the wake protocol** — leaving `sleep` is automatic inside the window and refused outside it. There is no third outcome | clock → ecosystem | [`interface.md`](interface.md) |
| `PROTO-20` | **the handoff protocol** — a stub is deleted only once a spawned repository has proved it is what it claims. CI green on both sides, non-negotiable; any hint of fraud, reject | spawned repo → anoieu | this page |
| `PROTO-21` | **the identify protocol** — **every** response opens with the entity the agent acts for, its mission, and **which AI is answering, by name**. The long form at session start and on request | agent → human | [`interface.md`](interface.md) |
| `PROTO-22` | **the misc protocol** — a document too expensive to clean up now is demoted to `docs/misc/` rather than deleted or left misrepresenting itself. Discouraged, and a growing `misc/` is a symptom | page → layout | this page |
| `PROTO-23` | **the downstream refresh** — fetch and read another repository before making a claim about it, and say how far behind you were | us → downstream | this page |
| `PROTO-24` | **the upstream refresh** — a member makes its copy of the shared arrangements current before relying on them, and only onto a green commit | member → us | this page |
| `PROTO-25` | **the joke protocol** — humour lives on the president's front page and nowhere a machine parses or a stranger reads for instructions. Any tool may say *that's not funny*, meaning *you are confusing everyone*, and it ends there | any tool → any tool | this page |
| `PROTO-26` | **transferring roles** — a role moves when it is marked, the target exists, and **both** repositories' CI is green. Theirs is a person's check, not a job | us → another project | this page |

**`PROTO-19` is the only entry in the register whose left-hand side is not a
party.** A clock is not somebody with an interest, and that is exactly why it
holds this one: a rule about when to stop working, adjudicated by anyone who
wants to keep working, is not a rule.

**`PROTO-18` is the first entry addressed to every member rather than to
anoieu**, because the thing it is about — a person working at four in the
morning — does not happen in one repository. **It is also the entry that asks
least of them: its whole content is one sentence said to a person, and a member
that honours it changes no file.** The mechanism is maintained by
[martyria](../tools/martyria/README.md), which is where its ethics are argued
and its schedule lives.

## `PROTO-26` — transferring roles to another project

**Roles move when both repositories are in order, and *both* is the word doing
the work.** Ours and theirs. The check is `tools/transfer_check.py`, and CI
carries it as a **report** rather than a gate.

### What has to be true

1. **The role is marked.** A role destined for another project carries a
   `Destined for` line in [`roles.md`](roles.md). **A transfer nobody wrote down
   is an intention, not a pending move**, and the marker is what the check
   reads.
2. **The target exists.** In the inventory, with a repository. **A stub is not
   a destination** — it is a note saying one is expected.
3. **Our CI is green**, which the job enforces by depending on the others: it
   cannot report while anything else is red.
4. **Their CI is green**, which **cannot be established from here.**

### Why the fourth is a person's step and not a job

**Asking GitHub about somebody else's build from inside our build would make our
CI fail for reasons in somebody else's tree.** [`policy.md`](policy.md) names
that as how a suite becomes noise, and it applies to us first. So the check
reports *unverified from here* and a person runs it with `--online` before
anything moves.

**Unverified is its own outcome and is not a pass**, with its own exit code, for
the same reason the bump gate has three: *we asked and it is wrong* and *we
could not ask* are different facts.

### Why it reports rather than gates

**Every target is *not ready* today** — neither kanon nor tekton exists — so a
job that failed on that would be red for a reason nobody can fix this week.
**A check that is red for months trains everybody to ignore red**, and then the
checks that matter are ignored too. The job is named for what it does: it
produces a report, and **a green tick on it means only that we looked.**

**It becomes a gate the day it can pass**, and that day is the day the roles
move.

## `PROTO-25` — the joke protocol

**A president keeps a joke about its own name on its front page, and that is
where humour stops.** Law 12 in [`laws.md`](laws.md) puts it there; this
protocol keeps it there.

### Why the vision now says to enjoy this

**[`vision.md`](vision.md) closes on one line: *Have fun and enjoy the Eunoia
ecosystem!*** The line is there and the argument for it is here, because that
page takes single sentences and not paragraphs.

**It is put there by this protocol rather than by sentiment.** The ecosystem
requires every president to keep a joke about its own name on its front page for
its whole term, and gives any tool a veto over it. **Those two rules only make
sense if enjoying this is a goal**, and a goal that governs rules belongs in the
vision rather than in the rules.

**The practical reading.** Work that is no fun is work somebody does briefly and
then stops doing carefully. Documents that stay current, checks that stay
strict, records that stay honest — all of it depends on choosing to keep going
after the interesting part is over. **A project nobody enjoys does not fail
loudly; it stops being maintained**, and every other tenet fails quietly with
it.

**It is not permission to be unserious about anything that matters** — see the
boundary below. **Have fun where it costs nothing, and nowhere else.**

### Any tool may say "that's not funny", and that ends it

**The objection is not a review and is never about taste.** *That's not funny*
means one thing here: **you are confusing everyone.** A reader arrived, met a
joke, and left less sure what the tool does or what they were being asked to do.

**It is honoured without argument.** The joke is removed or replaced, by
whoever put it there, and **nobody explains the joke.** Arguing that a joke is
funny is the behaviour that makes it worse, and a tool that can be talked out of
saying so will stop saying it. **The objector owes no evidence.** One reader
confused is the whole of the case, because that reader is the only one who can
report it.

**No appeal, and no cost to raising it.** An objection that turns out to be
wrong has cost one joke. **An unraised objection costs every reader after it.**

### Where humour may not go at all

**Not a matter of judgement, and not subject to a good enough joke:**

- **Anything a machine parses.** Check output, exit codes, formats, ids.
- **Anything a stranger reads to find out what to do.** Prompts sent to other
  repositories, joining instructions, error messages. **A joke in a diagnostic
  costs somebody a debugging session**, and they will never know it was a joke.
- **The policy, the checks, and any document a member is held to.** Nobody
  should have to decide whether a rule is serious.
- **Anything about somebody else.** A joke at another project's expense is not
  covered by this protocol and never was.

### The one that earns its place

**A joke that *is* the description is not decoration and is welcome.** anoieu is
*eunoia* backwards and pronounced *annoy you*, which tells a stranger what the
tool does in three words. `iogos` in the name register is the same trick: it
fixes the scope in the name and could not be renamed without losing information.
**That is the standard — if removing the joke loses nothing, it was never doing
any work.**

## `PROTO-23` — the downstream refresh

**Before saying anything about another repository, make your copy of it
current.** Fetch, check how far behind you are, and read the tree rather than
your own notes about the tree.

**The failure this catches is confident and wrong.** A claim about somebody
else's tree, made from a stale checkout or from a sentence we wrote about them
last week, reads exactly like a claim made from reading it — and this
repository has already published one. `noesis` sat in our register as *free to
take* while eudaimonia was running it, and the register said so for as long as
nobody looked.

**Three things, and it is a minute's work.**

1. **Fetch, and say how far behind you were.** `0` is a result worth reporting;
   it is the difference between *checked* and *assumed*.
2. **Read the thing itself**, not our summary of it. Their README argues its own
   case, and it may argue against what you are about to propose — as
   epikrisis's does.
3. **Say when you could not.** A repository not on this machine is a gap in the
   claim, not a detail. **Not checkable and checked-and-fine are different
   facts**, and only one of them is a pass.

**It applies hardest when the claim is critical.** Proposing that somebody
reorganise their tree, reporting a defect against them, or recording their
status in our inventory are all claims about a thing we do not control.

## `PROTO-24` — the upstream refresh

**The mirror, and it is a member's protocol rather than ours.** Before relying
on the ecosystem's shared arrangements, a member makes its copy of *them*
current: pull the policy, re-run the checker, and check whether the commit it
pins is still the one it means.

**Its own failure mode is the more expensive of the two.** A member acting on a
policy that moved is not merely out of date — **it is complying with a rule
nobody publishes any more**, and it will pass its own checks while doing so.

**What it costs us, which is the part that is ours.** A member cannot refresh
against a moving target. **Every change we publish is a refresh somebody else
has to perform**, and that is the real price of an edit to a shared page —
argued in [`policy.md`](policy.md), and the reason changes there are batched
into stretches rather than shipped as they occur.

**And a member may only bump to a commit where our build is green**, which is
where this protocol meets [`PROTO-20`](#proto-20--the-handoff-protocol) and the
handoff standard: **refreshing onto a red commit spreads a failure instead of
adopting a change.**

## `PROTO-22` — the misc protocol

**`docs/misc/` is where a document goes when cleaning it up properly would cost
more than it is worth today.** Demotion, not deletion: the page keeps working,
every link to it keeps resolving, and **nothing is lost.**

**It is a discouraged practice and the page says so.** The good outcome is that
a document is cleaned up, merged into the page it should have been part of, or
argued out of existence. `misc/` is what you do when none of those will happen
this week and the alternative is leaving the front of the documentation
misrepresenting what is load-bearing.

**What demotion means.** The document is still maintained, still linked, still
checked. **What changes is the claim the layout makes about it**: it is no
longer offered as one of the places a question is answered.

**What it must never be.** A place to put something to avoid arguing about it,
a way to keep a page that should be deleted, or a holding pen that fills up
because demoting is easier than deciding. **A `misc/` that grows is a symptom,
not a filing system** — the count belongs in the health assessment, and a
directory nobody has emptied in a year is evidence about the project rather than
about the documents.

**First use, 2026-09-02**: `ai-novelty.md`, `linker.md` and `methodology.md` —
1,564 lines of essay that mostly cited each other, of which one had a single
inbound link from the index and nowhere else. **They exist because a subject was
split rather than because three questions have three homes**, and merging them
is the work that was not affordable today. `science-fiction.md` was in the same
group and stays where it is: it holds the ecosystem's upper bounds and its
guard rails, which is a safety job rather than an essay.

## `PROTO-20` — the handoff protocol

**A stub** is a child project whose README says: *this is a stub, delete me
when you are convinced that my replacement is safely in the ecosystem.* It
marks a place. **It is not the tool and it holds no claim on the name** — the
name stays free for whoever builds it. `tools/tekton` and `tools/kanon` are the
first two.

**A spawned repository** is a new repository claiming to be the working
instantiation of a stubbed tool. *Spawned* is the word for it here.

**Two responsibilities, one each.** anoieu **cleans**: a stale stub is deleted,
and no stub survives the deployment of the stretch it was made in. The spawned
repository **identifies itself**: the claim *I am who I say I am* is theirs to
make and theirs to support. Neither side does the other's half.

### It is not a uniqueness claim

**The stub is not a title with one rightful heir.** Any repository that, as far
as we can see, is capable of upholding the vision is fine — and if two of them
turn up, that is also fine. We are not adjudicating who owns a name.

**We do not track GitHub ownership.** No accounts, no signatures, no
organisation membership, no chain of custody. Keep it simple.

**So *fraud* here is narrow**: a repository that claims to be doing the work and
is not. That is the only thing being checked, and it is checked by reading it.

**And it is not currently a risk.** One person drives this ecosystem as of
2026-09-02. The protocol is written now because writing it later, under
pressure, is the expensive version — not because anybody is knocking.

### CI green, on both sides, non-negotiable

**Every entity acting in a handoff must have its CI passing.** The spawned
repository, and us. **There is no version of this that is waived**, argued down,
or granted for a change that is obviously fine — no *green except one unrelated
job*, no *it was passing yesterday*, no exceptions for urgency.

**The reason it is absolute here and nowhere else.** A handoff is the one moment
this repository deletes something irreversibly on the strength of a claim about
a tree. **A repository whose CI is red cannot support a claim about itself** —
its own machinery is reporting that something in it is wrong while it asks us to
believe something else. That is not a judgement about the claimant; it is that
there is nothing to read.

**And it binds us harder than it binds them**, because we are the party doing
the deleting. **Verifying somebody else's tree while our own build is broken is
not a standard, it is a courtesy we extend to ourselves.** This is not
hypothetical: `B20` records that CI here was red for at least five consecutive
runs on the day this protocol was written, and nobody had noticed.

**No CI is not passing CI.** A repository that runs nothing is `unknown`, and
`unknown` sits with *attention* rather than with *ok* — the same rule the health
summary and the bump gate already use, for the same reason. *We asked and it is
wrong* and *we could not ask* are different facts and neither is a pass.

**A red build is not something the claimant may explain.** It is checked, not
discussed, which keeps it consistent with the rest of this protocol: asking a
claim to grow is not verification.

### The security half

**Deleting a stub is irreversible and keeping one costs nothing.** That
asymmetry sets the default: **no**.

1. **Any hint of fraud, reject.** Not a finding, not an accusation, no
   investigation owed — the stub simply stays and the claimant may come back.
2. **Read the repository, not the message.** A claim is worth nothing; a
   repository that visibly does the work is worth something. Not because a
   repository cannot be faked, but because **the cheapest way to fake being a
   working instantiation of the tool is to build one.**
3. **Asking the claimant for more proof is not verification.** It is asking a
   claim to grow, and a claim will.
4. **An agent never deletes a stub.** It gathers, it reports, and it refuses.
   **A person deletes.** No amount of evidence moves this.
5. **Deleting a stale stub claims nothing** about whether the tool exists,
   whether anybody built it, or whether a claim was true. It is housekeeping and
   should read as housekeeping.

**Two-way, and recorded both ways.** The claim arrives through the discussion
channel; we answer accept or reject; the answer is written down whichever it is.
A rejection nobody recorded is indistinguishable from silence, and silence is
what a fraudulent claimant is hoping for.

*Not to be confused with `PROTO-10`, the role handoff, which moves a
responsibility between tools that already exist and already know each other.
This one starts with a stranger.*

### Instructions are the inverse of protocols

**A protocol is written for an agent; an instruction is written for a human.**
Where a rule has two sides, both get written and both get an id: `PROTO-n` in
the register above, `INST-n` in [`instructions.md`](instructions.md).

**Not every instruction has a protocol.** Some are addressed to a person and to
nobody else — `INST-3`, *do not outrun your own understanding*, is one — and
writing an agent-facing half would move a judgement to the party that cannot
make it. **A missing counterpart is a decision, not a gap.**

**They are written in opposite registers.** A protocol closes every edge,
because a gap is a hole an agent falls through in good faith. An instruction
stays short, because one that is not read is not followed. **An instruction is
therefore not a summary of its protocol** — if it reads like the protocol with
words removed, it has not been written yet.

**The pair cannot be diffed.** Everywhere else here a copy is compared against
what it copies; this one is deliberately not a copy, so what binds them is the
shared id and somebody reading both.



**Say *human* where a human is meant.** In an ecosystem where agents write the
prose, run the checks and never sleep, the distinction that matters is not what
kind of person somebody is but whether the party in question is a person at
all. *A person* means the same thing and is not wrong; `human` is the word to
reach for when the contrast with an agent is the point.

**Not *runner*.** It was tried for an afternoon and dropped: `runner` is
already a machine that executes a CI job, and this repository talks about CI
constantly. **A term whose obvious meaning here is a machine is a poor term for
the one party that is not one.**

**Name the protocol when it fires.** *"`PROTO-4` — this started as X and X is
still open"* teaches the protocol in the act of using it, at the cost of six
characters; an unnamed reminder is just a remark and the person never learns
there was a rule behind it. This is how the ids earn their keep in a
conversation rather than only in this table.

**Labelling is partial and that is fine for now.** The four in
[`interface.md`](interface.md) carry their ids; the rest are labelled as
somebody next touches them. An unlabelled protocol is not a defect — a protocol
that has drifted from this row is.

## The scripts

**Two kinds, and the directory says which.** `scripts/` holds commands that do
what they say and run nothing else; `prompts/` holds the ones that
assemble context and hand it to an assistant. The partition is the whole of the
convention: a person can run anything in `scripts/` without deciding whether
they are willing to spend a turn, and anything under `prompts/` is a
turn by definition.

`repos.local` is the shared map from a repo id to a checkout on this machine. It
stays at `scripts/repos.local` and **both halves read it**, which is the one
untidy consequence of lifting `prompts/` to the top level: a file used by two
siblings now lives inside one of them. It was above the partition when the
partition was nested and it is beside it now. Left where it is rather than moved
to the root, because it is untracked and moving it buys tidiness in a document
at the cost of a path in three programs. It is untracked, and `install_eo` and `welcome_eo` are what write
to it — the first for everything on the list, the second when a tool arrives.

### `scripts/` — commands

| command | run in | what it does |
| --- | --- | --- |
| `install_eo` | here, **first** | the rest of the ecosystem, cloned beside this checkout with `git clone` and nothing else — audited by `tests/run.py`. `--dry-run` prints what it would run; `--status` reads the rows back. [The options](usage.md#the-rest-of-the-ecosystem) |
| `status_eo` | here | who is in the ecosystem and how each looks: declared or not, whether the policy check passes, whether there is a channel, how long since anything moved. `--check` decides whether the inventory itself is still true, and is what CI runs. `python3 tools/ecosystem.py --protocol` is the other report: where each tool proposed for the `associate` footing stands against each version of that drafted protocol, read from a checkout where there is one. It reports and never fails |
| `harvest_cpc_proofs` | here | collects real CPC proofs to seed the fuzzer with |

`status_eo` is a wrapper around `tools/ecosystem.py`, and `tools/policy_check.py`
has no wrapper on purpose: it is the interface **other repositories** run in
their CI, so its path is published in [`policy.md`](policy.md) and must not
acquire a second spelling.

### `prompts/` — the prompts

Each assembles context, hands it to an assistant, and writes nothing anywhere by
itself.

| command | run in | what it does |
| --- | --- | --- |
| `init_eo new` <br> `init_eo from-child <path>` | the **new** repository | the README that says what the tool is for: what it answers, the question it does not, the name explained. `new` writes it from the name register; `from-child` writes it from an existing child project's charter and from what that project delivered. The mode is required, never guessed. Complies with nothing, deliberately |
| `welcome_eo <id> <path>` | here | records the checkout, syncs the ecosystem's list, reads the new tool, drafts a first message. A welcome, never an audit. Refuses a typo rather than recording one |
| `join_eo` <br> `join_eo --soft` <br> `join_eo --soft --affiliated` | the **joining** repository | adds the membership declaration and the pinned `anoieu / policy` workflow. `--soft` is a different act rather than a smaller one: the maintenance note alone, declaring no membership, linking nowhere, adding no workflow and running no checker — for a repository that should not join and is still worth a note. `--affiliated` is the same again with one paragraph changed: it names the ecosystem and says the repository is not held to its policy, which is the note an `associate` in the inventory carries. All three prompts are fixed and drift-checked against [`policy.md`](policy.md) |
| `check_join_eo <id>` | here | joined, ready, misconfigured or not ready — and whether the obstacle is ours |
| `confirm_eo <id>` <br> `confirm_eo --president <id>` | here | **after** a join: whether the way they joined meets the benchmark for excellence, in the report card's four bands. `--president` adds the office — law 12's joke, whether acceptance is on the record, and whether they know what expires. **It confirms and never appoints** |
| `process_discussion <id> [Dn]` | here | works what another repository has addressed to us. **Read-only until a person names a topic** |
| `check_anoieu [id]` | the project a **finding** is about | answers our findings there, and drafts a reply for its maintainer |
| `process_anoieu <id> [ID]` | here | processes that reply: moves rows, writes verdicts, appends the logs |
| `global_audit` | here | the whole ecosystem against policy and vision, fast, no deep analysis |

**Every prompt takes `--show-prompt`**, which prints what it would send and runs
nothing. That is the first thing to do with one you have not used, and the only
way to review a prompt without spending a turn on it. `install_eo` is the same
idea for the one command that changes a machine: `--dry-run` prints exactly what
a run would execute, and the suite checks that what it prints and what it runs
are `git clone` and nothing else.

## What happens when we add a new tool to the ecosystem

A new tool is a decision, and `welcome_eo` is what turns the decision into the
files. The sequence, which nothing enforces:

1. Somebody creates the repository, and
   [`init_eo`](../prompts/init_eo) gives it a README. **There are two
   ways a tool arrives here and the script makes you say which**, because there
   is no default that is safe: `init_eo new` for a repository with nothing in
   it, and `init_eo from-child <path>` when the tool already exists as a child
   project in somebody's tree and a person has decided it graduates — the
   first of the three endings a child project can have. The second is not the
   first with an extra file to read. It writes the README from that directory's
   charter and from its record of what it delivered, because **that record is
   the reason the repository exists**, and it is told not to move the child's
   own front page across: a child project's README is written to say the work
   is speculative and depended on by nobody, which is the opposite of what
   graduating means. The register is what the name is checked against in both,
   rather than where the scope comes from in either.
2. [`welcome_eo <id> <path>`](../prompts/welcome_eo) is run here, once there is
   something worth reading. It records the checkout in `scripts/repos.local` —
   the file every other script resolves an id through — **and syncs the
   ecosystem's own list**, by running `scripts/install_eo --status <id>` and
   printing what comes back, before it reads the tree and drafts a first message.
3. That sync reports and never edits. If the tool is not in
   [`../tools/ecosystem.json`](../tools/ecosystem.json) it says a status is owed,
   and a person adds the entry: `status`, `repo`, `url`, `what` — plus `vetted`
   and `why` where the footing is `associate`, because a footing that rests on
   our judgement carries the date somebody made it and what they made it about. Membership is a
   decision a person makes, which is why no script writes that file. **A child
   project** — a tool inside somebody else's tree, like `ethos-eoc` at
   `ethos/tools/eoc` — takes `status: child` with `parent` and `path` instead of
   a `repo` and a `url`: nothing clones it, it arrives with its parent, and its
   id still resolves to the parent's checkout so the other scripts can take it.
   Where the child's current work is on another branch of the parent, `branch`
   says which, and the install repeats it rather than acting on it. A child is
   **listed** by `install_eo` in both views, with `path` saying where in the
   parent it lives: work that exists and can be read earns its line whether or
   not it is a tool yet. A *name* with no work behind it does not — the register
   in [`../tools/ynoia/names.md`](../tools/ynoia/names.md) is where those live,
   and an install that advertised them would be a list of things to go and not
   find.
4. **The entry is the whole of the work.** `install_eo` derives what to clone
   from the inventory, so the new tool appears in the dump, in `--status`, and in
   `scripts/repos.local` on the next machine with nothing else edited.
   [`../tools/checkouts.json`](../tools/checkouts.json) carries only what cannot
   be derived — a clone flag, or a tree nobody should fetch unasked. The
   ordinary case needs none of it.
5. `join_eo` and `check_join_eo` come later, or never. Joining is its owner's
   choice, and a tool that never joins is still in the inventory.

**What the sync is there to prevent** is a tool that exists only on the machine
of whoever welcomed it: recorded in `repos.local`, absent from the inventory, and
missing from every other checkout — a state nothing used to report, because each
half looked complete from where it stood. `welcome_eo` is where it is caught
because that is the one moment somebody is already thinking about the new tool.

## Keeping ynoia's registers true when the ecosystem moves

Three files in [`../tools/ynoia/`](../tools/ynoia) are **registers about the
ecosystem** rather than arguments about it, and they are the ones that go stale
without anybody noticing, because nothing consumes them and no build reads them.
The trigger and the edit, in full:

| when | the edit |
| --- | --- |
| a name is taken | a row in `names.md`, **saying where it lives** |
| a tool moves — a child started, a child graduated, a repository created | the *where it lives* clause on its existing row |
| a tool on `tools.md` starts existing | its block **leaves** `tools.md`. A page that keeps its graduates is a page whose first entries are all finished work |
| a tool enters [`../tools/ecosystem.json`](../tools/ecosystem.json) | an entry in `papers.md`, even where the verdict is `no` |

**The cross-check is one pass and it is worth doing whenever the inventory
moves.** `ecosystem.json` is the authority on who exists, so anything in it with
no row in `names.md` is either a gap or a name somebody else chose — the latter
being `cvc5` and `ethos-eoc`, which will never be there and which `names.md` now
says so about. Run on 2026-09-01 it found three: `workflow-launcher` missing
entirely, `koine` still recorded as awaiting a repository it has had for days,
and two child projects with no *where it lives* clause.

**Why this is a paragraph and not a check.** A research project is not in the
test suite, not in CI, and nothing breaks when its directory is deleted — that
island property is what makes carrying one cheap, and a check here that read
`names.md` would quietly end it. The registers being stale is a real cost and it
is the smaller of the two.

## A finding is about `main`

We report a defect against what a project ships. Every ref in
[`../tools/deps.json`](../tools/deps.json) is a branch somebody else's users get,
and a finding measured on a topic branch is one its owner can close by deleting
the branch.

That is not hypothetical. `logos-2` was measured against `updateCompiler` and
held open for four days, because the accepted fix sat in a working tree on a
branch level with `main`. The branch was then deleted, and with it any way of
asking what the report had been a report of. The finding had in fact landed; the
row survived the confusion only because its id had been written down.

**The exception is ethos-eoc, and the branch is `ethosEoc3`.** ethos-eoc is not a
repository: it is a **child project in the ethos tree**, at `tools/eoc`, and it is
developed on `ethosEoc3`. The compiler and the semantics sets the ecosystem is
built on are there and are not on ethos's `main`, so that branch *is* the shipped
thing for that tool — which is the test an exception has to pass. It is not an
exception for being where the work is convenient to read. ethos's own `main` is
still where the Eunoia manual is read from, and findings against the checker are
against `main`. `ethosEoc3` contains `main` in full, so measuring the tree there
measures `main` and the compiler work on top of it; when the branch merges, the
ref in [`../tools/deps.json`](../tools/deps.json) becomes `main` and the exception
is gone rather than renegotiated.

**And the exception does not reach `install_eo`, which installs a default branch
and nothing else.** Every command it prints is a plain `git clone`: no `-b`, no
checkout, no branch switch. A child project is not a checkout obligation — it is
a directory in somebody else's tree and it arrives when that tree does — so ethos
installs normally and the install *says* that the copy of `ethos-eoc` on the
default branch is the older one, with the command that gets the newer:

    git -C ethos checkout ethosEoc3          # or a worktree, to keep both

Which is the whole of the accommodation: a fact stated where somebody will read
it, and a branch nobody is put on without choosing it. The branch is recorded on
the **child** in [`../tools/ecosystem.json`](../tools/ecosystem.json), because it
is a fact about the child rather than about the repository — ethos's own default
branch is not wrong, and a checker finding is still measured there.

A second exception is a decision, and it is written down here with its reason or
it is not made. A branch named in somebody's *reply* — `anoieu-findings`, say —
is where a fix is read before it lands; it is never what a finding is measured
against, and [what closes a row](reports/reporting-workflow.md#what-closes-a-row-and-what-does-not)
is a separate question with its own answer.

## The supervision ladder

Ordered, most supervised first. *Supervised* means: propose the change and the
reason, and wait for a person — do not make it and mention it afterwards.

**1. [`../docs/vision.md`](vision.md) — ask first, always.** It states
what AI-assisted development in this ecosystem is for, it is addressed to
repositories that did not write it, and the party with the least standing to
revise it is the agent it governs. This includes
[`report-card.md`](report-card.md), which was split out of it and is governed by
it unchanged: a paragraph there is a judgement about somebody else's project,
and softening or sharpening one is exactly the edit that should not be made
quietly.

**And a change to the vision is at most five lines of diff.** Not five
paragraphs, not five sentences — **five lines as `git diff --numstat` counts
them**, added and removed together. There is no exemption for a good addition.

**The size limit does the work the ask-first rule cannot.** *Ask first* is
honoured by proposing something, and a person reviewing a page they have already
agreed with will approve a well-argued twenty lines. **A bound that is checked
by counting cannot be argued with**, and it forces the same discipline on every
edit: if a change needs more than five lines, it is not a vision change — it is
a document that belongs somewhere else with one sentence pointing at it from
here.

**That is exactly what happened to the line about enjoying this.** The sentence
is in the vision; the argument for it is in `PROTO-25` on this page, where there
was room to make it. **The vision holds claims, not their justifications.**

**Nothing may ever check the vision mechanically.** No CI job, no script, no
generated verdict against a tenet. Whether a tool is fruitful or a claim
oversold is contestable and nobody has the standing to settle it, so a green
tick against one would invent an authority that does not exist. The reasoning is
*Policy is checked; vision is argued* on that page, and it is the one rule here
that forbids work rather than requiring it.

**2. [`../docs/policy.md`](policy.md) — ask before the rules.** The
numbered rules may be **appended** to, never renumbered, and retiring one in
place is a person's decision. The layout conventions are different in kind: when
the tree and the conventions disagree, correcting the *description* to match
what the tree actually does needs nobody, and changing the tree to match the
description is ordinary work.

Unlike the vision, this page **is** machine-checked:
`python3 tools/policy_check.py` runs in CI and decides every rule that a program
can decide from the tree. Run it before proposing a change here — and if you add
a rule, either make it checkable or accept that it lands on the checker's
printed list of what it cannot decide.

**3. [`reporting-policy.md`](reports/reporting-policy.md) — not yet stable, so
say what you changed.** Unlike the two above, this page is still settling: its
positions are being worked out rather than defended, and adding, sharpening or
retiring one is ordinary work rather than something to ask about first. Two
things still hold. Positions are **appended and never renumbered**, and are
cited by name, so a rewrite that renumbers is a defect however much better it
reads. And **dokimasia references this page rather than copying it**, so every
edit moves a second repository — which means changes get flagged to a person
even though they do not need permission, and a *structural* change (a position
retired, the page renamed again) is carried to dokimasia by hand.

> **Outstanding:** this page has been renamed twice and its positions retiered
> and extended, so dokimasia's links to it and any quotation of it are stale.
> Nothing here fixes that — nothing crosses a repository boundary by machine —
> so it is a person's errand, and it is unfiled.

**4. [`reporting-workflow.md`](reports/reporting-workflow.md) — ask before the prompts.** A
person approves every change to a prompt template, and each round should leave
the prompts *shorter and clearer* than it found them — that rule was itself
learned the expensive way and is written up in
[`postmortem.md`](reports/postmortem.md). `tests/run.py` fails when a script's copy of a
prompt has drifted from the document, so the two move together or not at all.

**5. The generated documents — never hand-edited, ask about nothing.**
[`corpus.md`](reports/corpus.md) and [`checks.md`](checks.md) are rewritten whole, so
anything typed into them is lost. [`open-findings.md`](reports/open-findings.md) and
[`closed-findings.md`](reports/closed-findings.md) are additive: the generator adds rows
and never removes or rewrites one, which is what keeps hand-written verdicts
alive. Closing a row is a judgement made by the review step, never by a diff.

**6. Everything else — ordinary work.** The README's results layer,
[`notes.md`](notes.md), [`usage.md`](usage.md), [`fuzzing.md`](fuzzing.md), the
code, the tests. No permission needed; the normal standard applies.

**What a repository says about itself decides how freely you may work in it.**
Where the maintenance note says the tree is **written by AI agents**, an agent
does ordinary work in it without asking step by step — the ladder above still
orders what needs a person *within* this tree, and that is the whole of the
constraint. Where the note says people write it, or where there is no note,
restraint applies: propose, show the diff, and wait.
[`reporting-policy.md`](reports/reporting-policy.md) already decides the *register
of address* this way — by what the project says about itself, never by our
impression of the code — and this is the same test applied to the scope of
action. **Where there is no note, the cautious reading applies**, because
guessing wrong in that direction is the cheaper error.

Three gates do not move, whatever the note says: nothing that **creates or
publishes**, nothing that **crosses a repository boundary**, and the discussion
file's own gate. The worked example is on the board today — `B3`'s two defects
are filed into `ethos`, which nobody claims is AI-maintained, so carrying them is
a person's errand however ready the reproducers are.

**Ramp up gradually, and on evidence rather than on a date.** New latitude starts
with the reversible things and widens when something has actually been observed
to work — the same shape koine proposes for handing a protocol over
(*referenced*, then *mirrored*, then *held*), applied to how much an agent may do
rather than to where a definition lives. Going back is one revert and needs
nobody's agreement.

And the counterweight, because that rule is otherwise an invitation: what wants
ramping up is **work on the thing at the bottom**, not machinery about the work.
The governance budget below has a baseline and no second row, and the outside
criticism that produced it says governance is the cheapest thing here to make. A
session that widens its own latitude and spends it on more documents has answered
the wrong half.

**Do not hold up the ecosystem with a position of your own.** This repository
argues carefully and writes its reasoning down, which is mostly a strength and
has one characteristic failure: a well-argued position that leaves somebody
else's work stalled, where the argument is ours and the waiting is theirs.

**The test is who is waiting.** Two kinds of position look identical on the page
and are opposites in effect:

- **A position that constrains us for their benefit** — nothing crosses a
  repository boundary by machine, silence is never published as assurance, a
  false positive is ours. Holding these costs the other party nothing, and they
  should be held even when inconvenient. Especially then.
- **A position that constrains them for our comfort** — a register we will not
  edit, an id we will not allocate, a decision we will not take because taking it
  would be premature. Each may be right, and each has somebody standing still on
  the other side of it.

**An undecided question is a position.** *Drafted, and not in force* is a decision
that nobody may hold the footing yet, and it lands entirely on the repositories
that would hold it. Deferring is often correct and is never free; what makes it
honest is saying **what would settle it and by when**, so that a person waiting
knows whether to wait.

**So: where a position of ours is blocking somebody, the burden is on us to
remove it, time-limit it, or route around it — not to defend it better.** A
worked example is live: `R26` is unallocated here because koine proposed it and
the request is open. That is the right call this week; if it is still true in six
months, the reservation has stopped protecting koine and started blocking them,
and the fix is answering `koine-D8` rather than restating why the id is reserved.

**And the same applies to what we hold rather than what we decide.** Governance
here is temporary by design — `R4`, `R6` and `R27` are all listed as moving to
the governance repository. A convention that only works while we hold it is a
convention that makes the handoff more expensive, which is a cost we would be
imposing on a repository that does not exist yet and cannot argue back.

Three more rules cut across the whole ladder.

**Weakening a claim needs nobody; strengthening one needs a person.** Adding a
caveat, narrowing a check that fired wrongly, or qualifying a result is ordinary
work to be done at once. Moving from *the fuzzer found a crash* to *the fuzzer is
ready for your CI* asks a reader to rely on something, and that is the human's
call — put the proposed wording and the evidence in front of them together.

**Never act on a discussion file unbidden.** `docs/discussion.md` here, and the
same file in any other repository, is correspondence between tools. Reading one
is free; acting on one requires a human who told you to, named the topic, and
whose instruction *agrees* with what the topic asks. Where the instruction and
the topic disagree, do nothing — not the overlap, not the safer half — say
exactly where they differ, and wait for a person to decide. They may override
after being told, and then the override gets recorded. This is the only rule
here enforced as a build failure rather than by convention:
`tools/policy_check.py` fails when the banner stating it is missing from the top
of the file.

**Nothing here holds credentials that create or publish.** No repository is
created, no remote is written to, no issue is opened, nothing is pushed; a person
does each by hand, and every script starts from a directory that already exists.

The case this matters most for is **a tool our own workflow proposed**. That
path can run a long way unaided — notice a gap, argue for a tool, audit the
argument against our standard, take a name from our register, write the new
repository's README — and each step is fine. Creating the repository is where it
would stop being fine, because that is the one step that is irreversible, public,
and under somebody's account rather than in a diff they can read first. A closed
loop from idea to published artifact is the thing being prevented, not
repository creation as such.

**Promise nothing we cannot keep.** Every commitment this repository makes to
another repository is a maintenance obligation that outlives the enthusiasm that
made it — a release cadence, a versioning scheme, a compatibility guarantee, an
undertaking to announce changes, a script maintained on somebody else's behalf.
This is one repository written mostly by agents under light supervision, and the
honest capacity is small.

So prefer a **structural** answer to a promised one: a member that pins a commit
needs no undertaking from us about when we change things, and a structural
answer keeps working when nobody is paying attention. Where a promise is
genuinely the only mechanism available, say in the same breath that it is an
intention, that nothing enforces it, and that nobody should build on it — the
same tiering [`reports/reporting-policy.md`](reports/reporting-policy.md) applies
to its own positions. Withdrawing a commitment costs more than never making one,
and most of that cost falls on somebody who is not us.

**Documentation lives at its source, and a launch is a handoff.** While a thing
does not exist, the page that argues for it also describes it, and that is
correct. **The moment it exists — a repository, or a directory with a charter of
its own — it documents itself, and the description elsewhere is deleted.** Not
marked stale, not archived: deleted, because git keeps it and a marked-stale
description still gets read and still gets quoted.

The protocol is three lines and is meant to stay that short:

1. **Delete the description; keep the argument.** A page that argued for a thing
   usually also uses it to make a point. The point stays; the specification
   goes.
2. **Leave one line** — the name, where it lives now, and when it launched.
3. **Do it at the launch, by whoever notices, without asking.** Waiting for
   permission is what produces the failure this prevents: two accounts of one
   thing, of which the unmaintained one is what a stranger finds first.

The worked case is [`../tools/ynoia/why-eunoia.md`](../tools/ynoia/why-eunoia.md),
which described six projects that did not exist and now describes five.

**Make changes a person can understand.** The standard for an agent's output is
not that it is correct — it is that **whoever reviews it can tell whether it is
correct**, and those come apart constantly. A large mechanical diff, a clever
refactor, a rename touching nine files because that was the tidy way to do it:
each may be right, and each defeats the only check this arrangement actually
has. Prefer the smaller change, the boring construction, and the diff that reads
in order. Where something genuinely cannot be made comprehensible in one go,
make it in pieces that each can be, and say which piece is which.

This is the authorship half of *go only as fast as you understand*, which is
stated in [`stretch-policy.md`](stretch-policy.md) and governs how much is
attempted. This one governs how it is written, and it is the half an agent
controls directly: an agent is fast enough to produce, in an afternoon, more
change than a person can read in a week, and nothing about that is caught by
tests.

It is also what keeps the next rule from being ceremonial.

**Work is left staged, not committed.** A person reviews the diff and commits.

**And when a commit is taken while the work is still moving, say so in one
line.** The staging convention assumes the person commits once the agent has
stopped. Committing mid-stream instead is nobody's fault and will keep
happening — but the commit's message then **stops describing its contents**, and
a history somebody can walk is most of what this ecosystem claims. A reader
looking for a change finds it filed under a subject it has nothing to do with,
which is worse than not finding it.

The remedy is deliberately small: **one line naming the commits and what they
actually carry.** Anyone may write it, anyone may delete it, at any time,
without asking — it is a note about the record rather than a record in its own
right. Nothing waits on it and nothing is blocked by it being there or gone.

> **Noted 2026-09-02, and removable.** Two commits were taken mid-stream and
> their subjects are misleading. `086f1d9` — *"More additions to why-eunoia"* —
> changes no line of that file: it is martyria's standing observation grant and
> zetesis's analysis of its relationship to the kernel. `9d9a33f` — *"Code with
> prompts idea"* — carries that idea and also the documentation handoff
> protocol, request `R2`, four factual corrections, and the 103-line deletion of
> the euthyna description from `why-eunoia.md`.
This is not a formality: it is the last place where a change to a document that
binds another repository can be caught.

## The build

**It has been red far more often than green, and it stopped being read.**
Sixty-one consecutive runs failed, from 2026-08-30 to 2026-08-31, on two defects
that had nothing to do with each other and neither of which was in the change
that first turned it red. That is what this section guards against — not the
failures, which were real, but a build everybody has learned to expect nothing
from, which is worth the same as not having one.

Both defects had the same shape: **a check that was a function of something
other than the tree it was checking.**

- The pinned corpus restore cloned a *branch* before fetching the commit, so a
  pin was only as durable as the branch it happened to sit on. logos's was
  deleted upstream, the clone failed before the pin was ever tried, and the job
  whose entire design is to depend on nothing but this repository went red
  because somebody else removed a ref. The failure it printed was worse than the
  defect: *the report is not current; run `tools/run.py` and commit* named a fix
  that would have dropped logos from the lock and recorded the shortfall.
- A recorded oracle verdict held part of the recording machine's home directory.
  ethos names the source file it was *built* from when it fails internally, and
  the normaliser only knew how to strip the directory of a witness — so the
  record could not match on another machine, and never would.

**Be careful, and do not make the build slow.** Those pull against each other
only if care is spelled *more steps*. It is not: both fixes above make a step
depend on less rather than adding one, and the pinned restore now costs one
network request per project instead of two. A run people wait on is a run people
skip, and a skipped run is not evidence. Prefer the fix that removes an input
over the fix that adds a guard.

**The `policy` job is a contract, and it is the one place where no ground may be
given.** Everything else here is ours to break and ours to fix on our own
schedule. `tools/policy_check.py` is not: other repositories run it in their own
CI, pinned at a commit of this one, and what it decides is what this repository
is handing them downstream. So it is never relaxed to turn a build green, never
made conditional on the rest passing, and never left to rot while something
noisier is being fixed — and a check removed from it is a promise withdrawn from
somebody else rather than a tidy-up here. A regression in any other job costs us
a morning. A regression in that one costs a maintainer who does not work here,
in a build they did not schedule, which has already happened once and is written
up below.

## Defending the infrastructure

The policy, the checker, the joining flow, the discussion protocol, the pin and
the proposal audit are **not a proposal any more.** They have been used, by a
repository other than this one, and the record of what they did is short enough
to state and specific enough to argue with.

**A second repository adopted the policy and runs the check in its own CI.**
dokimasia declared membership, wired the workflow, and went red — on a defect in
*our* checker, not in their tree: twenty-two link failures, every one spurious,
caused by a rule of ours that resolved a child project's own documentation from
the wrong root. They declined to work around it, cited the sentence on our own
page that says a check firing on a non-problem is ours to fix, and left the links
alone. We fixed it, added a regression test, and their build went green without
them changing anything.

That episode is the strongest evidence available that the arrangement works,
and it is worth being precise about why: **the first outside run of the checker
found a defect in the checker**, surfaced it through the channel built for it,
and cost the other party an afternoon that we then owed them. Every part of that
was designed and every part of it fired.

**Four topics have come through the protocol, and three changed what we do.**
The link resolution. The joining step, which pinned nothing and made every
member's build a function of a repository they do not own — the sharpest sentence
anyone has sent us is theirs, that a build which can turn *green* without a
commit cannot be evidence that a commit was good. And the naming convention,
which was a hard failure that every real candidate failed and was, on inspection,
a suggestion about readability. The fourth produced an audited proposal, an
approved repository and a name.

**The checker also finds things here.** Three dead anchors on its first run, two
of them made that same day by the person who added the check.

### What defending it means

**Removing a piece is a decision with a burden of proof, not a tidy-up.** The
cases are on record; if a rule is in the way, name the case, because there is now
a place to put that argument and somebody on the other end who will answer it.

**The pieces interlock, and that is not decoration.** A declaration is worthless
without a check; the check is unsafe unpinned, because one rename here turns
every member red with no commit near them; a pin is unusable without a version to
print; and the discussion protocol is what allowed all three to be corrected by
somebody who was not us. Each of those links was put in by an exchange rather
than designed up front, which is exactly why pulling one out quietly is
expensive — the chain looks arbitrary until you know which failure each link
answers.

**The failure mode is treating this as overhead during a rush.** Infrastructure
is cheapest to delete at the moment it is most load-bearing, and an agent under
time pressure is well placed to make that trade badly and describe it as
simplification.

### And the honest limit

**Three adopters are not ten.** `eudaimonia`, `dokimasia` and `koine` have
joined; `ethos` and `logos` have not, and may never. Evidence that this
coordinates four repositories is not evidence that it coordinates forty, and
each adopter so far has found things the ones before it did not.

**It has not been free.** [`report-card.md`](report-card.md) records
that the stretch of work which produced most of this changed nothing about what
the analyzer finds, and introduced two silent defects into the fuzzer — one of
which would have let CI pass while verifying nothing at all. Defending the
infrastructure is not claiming it was cheap, and the case for it rests on what it
has done for other repositories rather than on what it has done for this one.

## Adding a check

The checker is the one thing here that runs on other people's builds, so a check
is not a change to this repository — it is a change to theirs. It lands
permanently, it fires at moments nobody chose, and it is nearly never deleted.
Four conditions before one goes in.

**It is decidable without an opinion.** If answering it requires judgement, it
belongs in [`vision.md`](vision.md) and must never acquire a checker.

**It has been run against a tree we did not write.** Every false positive so far
was found by somebody else's repository and none by ours, which is not luck:
this is the one repository shaped like the checker's assumptions. Run a new check
against every candidate checked out on the machine before it lands. A check that
has only ever seen this tree has not been tested.

**Its message names the fix.** A failure a maintainer has to interpret costs more
than the defect it found, and they are reading it in a red build on somebody
else's schedule.

**It stays true without curation.** The expensive kind is the check whose *data*
rots — a list of vendor names, a registry of tools, anything that must be
updated as the world changes rather than as the tree does. There is one of those
already, the vendor list, and it is the check most likely to be wrong a year from
now. Prefer checks whose only input is the repository in front of them.

### Why this is a limit and not a ritual

The failure mode is drifting into maintenance mode: a set of checks large enough
that keeping it honest is the work, and forward progress stops. Three things
make that happen, and they are worth naming because each looks like diligence.

**A check that fires wrongly costs more than it can ever save.** It costs
somebody else an afternoon, and it costs us the credibility of the whole set —
a maintainer who has been sent one spurious failure reads the next one
differently, including the true ones.

**Every check is a migration.** A repository that passes today and fails
tomorrow has to do work it did not ask for, at a moment it did not choose.
Pinning makes that survivable; it does not make it free, and *we do not pay it.*

**Checks accumulate and are almost never removed.** So the question at the point
of adding one is not *is this true* but *will I defend this in a year, on
somebody else's repository, when it fails inconveniently.* If the answer is
anything short of yes, it belongs in the minor tier, which is what that tier is
for — the naming convention is the worked example, a hard failure that every
real candidate failed and that was, on inspection, a suggestion about being
readable.

**And there is a stopping rule.** A check earns its place by finding something.
The anchor check found three dead links on its first run, two of them made that
same day by the person who added the check. A check that has never fired on
anything is either perfect or pointless, and the second is the way to bet.

## The governance budget

**The rule exists and nothing counts against it.**
[`report-card.md`](report-card.md) grades this repository down for exactly this
and states the rule in the same paragraph: *every further page here has to
displace a check, a finding, or an hour of somebody else's reading.* Nothing has
ever measured whether it is kept. A rule with no counter attached is the same
failure the prompt-length table in [`postmortem.md`](reports/postmortem.md)
exists to fix in the other half of the system — and it is the criticism that
came from outside, in `workflow-launcher`'s register of what this ecosystem's
practice appears to be doing, which reads six checkouts and writes down what is
wrong with them beside what is not. It is a child project in eudaimonia's tree,
at `tools/workflow-launcher`, and `docs/ai-workflows.md` is the document.

So: the baseline, measured over this tree on 2026-09-01. Reproducible in three
commands, and worth nothing until there is a second row.

| what | files | lines |
| --- | --- | --- |
| tracked Markdown outside `deps/` | 32 | 15,142 |
| — generated, written by a tool | 4 | 1,142 |
| — child projects, shipped by nothing and advertised nowhere | 10 | 4,550 |
| — **written prose: the number this section is about** | 18 | **9,450** |
| Python | 54 | 13,382 |
| `scripts/` and `prompts/` | 11 | 2,481 |
| checks with a page in [`checks.md`](checks.md) | | 63 |
| findings in the ledger | | 39 open, 43 closed |

```
git ls-files '*.md' | grep -v '^deps/' | xargs wc -l | tail -1
git ls-files 'tools/*/*.md'           | xargs wc -l | tail -1
git ls-files '*.py'                   | xargs wc -l | tail -1
```

**What the row is for, and what it is not.** It is not a limit. Nobody has
argued what the right ratio is, a budget invented here would be a number to
game, and a page is not bad for being long. It is for the *next* reading: the
rule says a page displaces a check, a finding, or an hour of reading, so if
written prose grows between two rows of this table while the check count and the
finding count do not, then the rule was not kept — and that becomes a fact
somebody can point at rather than an impression somebody has to argue for.

**Record the row; do not move the rule to fit it.** That is the discipline the
prompt-length table already keeps, including the part that makes it worth
having: it reports its own metric going the wrong way, three rounds running,
rather than being quietly retired. A counter that only ever confirms is not a
counter.

And this section is itself the thing it measures. It costs about fifty lines of
written prose and displaces nothing today, which is the honest accounting; what
has to pay for it is the second row.

## The open technical work

**Planning only. Nothing below is built.**

The record is now edited mostly by an assistant: `prompts/process_anoieu` reads a
reply and moves rows, writes verdicts, narrows checks and appends to two logs.
That has already worked and has already gone wrong — a verdict of *fixed
upstream* was recorded three times for a fix that never happened, and nothing
noticed for months (see [`postmortem.md`](reports/postmortem.md)). The question this
section is for is not *how do we stop an agent editing the record* but **what
must remain true of the record after any edit, whoever made it, and which of
those can a machine check.**

The eventual goal is that these hold in **anoieu's CI**, failing a build rather
than living in a document somebody is meant to have read. But most of them do
not need enforcing so much as *not offering the chance to get them wrong* — a
script the agent is told to use, rather than a table it edits. That is the
cheap route, it is written up after the list, and it is where to start. None of
this is built today.

### The properties we want

Grouped by what they protect. The right-hand column is the honest status.

| # | property | why | today |
| --- | --- | --- | --- |
| **C1** | **The log is append-only.** A run adds entries to [`reports.md`](reports/reports.md#the-log-what-was-reported-and-what-came-back) and [`postmortem.md`](reports/postmortem.md); it does not rewrite what an earlier run wrote. | The log is the only account of what we believed and when. A log an agent may rewrite is a log that silently agrees with the present. | nothing checks it |
| **C2** | **Except to correct, and a correction is visible as one.** An earlier entry may be amended when it is *wrong* — not when it reads badly — and the amendment says so in place, keeping the original claim legible. | This round had to correct three verdicts and a false claim about the fuzzer's records. Forbidding that outright would have forced a knowingly false log. | done by hand, by convention |
| **C3** | **Every id that has ever appeared is accounted for, forever.** An id in [`open-findings.md`](reports/open-findings.md) or [`closed-findings.md`](reports/closed-findings.md) never leaves both; it is open, or closed with a verdict, and never absent. | The whole point of an id. A row that can vanish makes every earlier decision unverifiable. | the generator is additive and cannot delete, but nothing forbids a *hand* deletion |
| **C4** | **No id is in both files, and no id appears twice in either.** | Two states for one finding is a record that answers differently depending on where you look. | not checked |
| **C5** | **A closed row's verdict is re-derivable, or says why it is not.** A verdict of *fixed upstream* is a claim about a tree we have; it should carry the commit it was checked at, and a later run should be able to fail when the finding is still reported there. | This is exactly how three rows sat closed on a fix that never landed. | not checked; the highest-value gap |
| **C6** | **An id is stable under things that are not the finding.** Regenerating the CPC baseline this round changed every id, because the fingerprint moved with the path root when the entry point changed — the findings were identical. An id that moves when nothing about the finding moved silently invalidates every verdict recorded against it. | Decisions are recorded against ids. | **broken**, and [`reports.md`](reports/reports.md#what-cvc5-asked-for-next) currently claims otherwise |
| **C7** | **A closure is traceable to its evidence.** Every verdict names the run, the reply, or the commit it rests on, so a reader can go from a closed row to why. | *"Because an assistant said so"* is not a reason, and today the link is prose in a log entry. | by convention |
| **C8** | **A finding reported to somebody is tracked until it is resolved**, including when the resolution is *declined*, *withdrawn*, or *reopened*. Reopening is a first-class transition, not an edit. | We reopened three rows this round and had to invent how. | ad hoc |
| **C9** | **A generated file is only ever written by its generator**, and a hand edit to one is a failure rather than a surprise on the next run. | `corpus.md` and `checks.md` say this in prose; nothing enforces it. | not checked |
| **C10** | **The record is coherent after every single row**, so a run that stops halfway leaves nothing half-moved. | Both follow-up prompts already promise this; nothing verifies it. | by convention |

### The cheap route, and probably the right one: a script

Most of the list above is only hard because the record is edited by hand — an
agent opening a Markdown table and moving a line. Give it **one command per
transition** and most of the properties stop being properties to check and
become things that cannot happen:

```
tools/ledger.py close  <id> --verdict "..." --evidence <commit|reply|run>
tools/ledger.py reopen <id> --because "..."
tools/ledger.py note   <id> "..."
```

The prompt then says *use this, do not edit the tables*, the same way it already
says *closing is moving a row, never deleting it*. What that buys, directly:

- **C3, C4** — the script is the only writer, so an id cannot be dropped or land
  in both files. It refuses rather than producing an incoherent record.
- **C1, C8** — it appends the log entry itself, from the same call that moves the
  row, so the log cannot disagree with the table and *reopen* is a real
  transition rather than a hand-edit that looks like any other.
- **C7** — `--evidence` is required, so a verdict without one is not expressible.
- **C10** — one row per invocation, and each invocation leaves the record whole.

This is not enforcement and does not pretend to be: an agent can still edit the
files directly, and a determined mistake gets through. That is the trade, and it
is a good one — it costs a day rather than a redesign, and it converts the
common failure (a well-meaning edit that leaves the record slightly incoherent)
into something that does not compile. **Do this before anything else here.**

### What still wants a check, script or not

Three, because no script can catch them:

- **C6, id stability.** Nothing at the call site knows the fingerprint moved.
  This is a defect in how an id is computed, and it is the one to fix outright
  rather than work around.
- **C5, a stale verdict.** *Fixed upstream* is a claim about somebody else's
  tree, and only a run against `deps/` can tell you it went false. The `corpus`
  job already has the tree; this is a step in it.
- **C2, C9 — a hand edit that bypassed the script.** A diff-shaped check against
  the previous commit, if it ever seems worth it. It probably does not until the
  script exists and is being used.

### Where the state should live — undecided, and a script postpones deciding

Today the state is two Markdown tables and two prose logs, with ids as the only
keys. Three options, none chosen:

- **Keep files, add the script.** Cheapest, and everything above except C5 and
  C6 is reachable from it. The limit is that a Markdown table has no
  transitions: *reopened* is indistinguishable from *was always open* except in
  the log the script wrote.
- **A tracker.** GitHub issues were the earlier plan
  ([`reporting-workflow.md`](reports/reporting-workflow.md#medium-term-issues-on-our-own-repository)),
  and the constraints there still hold: issues live on *our* repository, a
  person posts, never an agent. The argument for one is not bookkeeping — it is
  that **findings do not all come from our checks.** Some will come from a
  person, from outside, or from a project telling us something is wrong with our
  own record, and those have no generated row to hang off. That is the case the
  file-based arrangement handles worst.
- **An internal store.** An append-only log of *events* — reported, replied,
  closed, reopened, corrected — with the Markdown rendered from it. The only
  option that makes C1 and C8 structural, and the most work. It also moves the
  record out of git diffs, which is most of what makes today's arrangement
  reviewable.

**The question to settle is not which of these**, but whether a finding is a
*row that changes state* or an *event log summarised into a row*. Everything
follows from that — and the script above is worth writing either way, because it
is the same interface in all three worlds.

### CI should stop proving the report by re-running the tools

**Future work, and it belongs in koine rather than here. Nothing changes yet.**

The `corpus` job answers *is the report accurate* by cloning four upstream
projects, running every check over all of them, and diffing the result against
what is committed. That is an expensive way to ask the question and a brittle
one: the job is a function of four remotes, of what git does when a ref
disappears, and of whatever the checks happen to say today — and the first of
those has already taken the build down for a day. A report is a record of what
was measured and when. A build should be able to establish that the record is
**coherent** — every id accounted for, every closed row carrying the evidence it
rests on, nothing asserted about a commit the lock does not name — without
measuring anything a second time.

That is the same question the properties above are about, and it is why this
belongs to [koine](https://github.com/ajreynol/koine) and not here: the loop
that produces the record is shared between two tools already, so a check that
the record is well-formed is shared too, and writing a second one here is
exactly what koine exists to prevent. It is raised with koine and dokimasia as
`D9` in [`discussion.md`](discussion.md).

Two things hold in the meantime. The `corpus` job **stays as it is** — a slow
proof is better than none, and removing it before the replacement exists would
trade a real check for an intention. And the `policy` job is **not in scope for
any of this**: it decides claims about this tree, clones nothing but the policy
it is checked against, and is a contract with other repositories rather than a
convenience for us.

### When each member joined, and what we were at the time

**Audited 2026-09-02**, from the members' own trees and by running
`tools/bump_check.py --rev` against each pin they took. Everything below is
re-derivable; nothing is remembered.

| member | joined at | pinned anoieu at | our CI at that commit |
| --- | --- | --- | --- |
| `eudaimonia` | `a93fbec`, 2026-08-31 | `dc2c613` | **not green** — `corpus`, `oracle` |
| `dokimasia` | `0593624`, 2026-08-31 | `441b562` | **not green** |
| `koine` | `16af79d`, 2026-08-31 | `5668c20` | **not green** |

**All three joined on the same day, and all three pinned a commit our own build
had failed.** That is the whole finding and it is not a near miss: the gate that
decides it, `bump_check.py`, refuses every one of them today, naming `corpus`
and `oracle`.

**The requirement they were given has never been satisfiable.** We published it
as a hard one — *only move your pin to a commit where our CI is green, and
refuse the bump otherwise* — and there was no such commit to move to. logos
reported exactly this from outside before joining, and declined partly on those
grounds; this audit says the same thing about everyone who did not decline.

**So the rule is one we enforce on others and have never met ourselves**, which
is the asymmetry the ethics registers exist to catch and did not catch here — a
person asked for this inventory and it fell out of it. Two things follow, and
neither is a document: either the build goes green and stays green long enough
for a pin to exist, or the requirement is withdrawn as unmeetable and replaced
with something true. **Until one of those happens, no member can comply and no
new member can join correctly.**

**One deviation, already raised.** dokimasia does not keep the pin in
`ANOIEU_REV` as the joining step describes; it keeps it in `tools/deps.lock` and
moves it with a script of its own, and it raised that with us as its `D2` rather
than doing it silently. The audit reads its pin from where it actually is.

### Updating the report card — moved

The five rules that decide it are now kept by the child project that holds the
role, `R30`, in `tools/stathmos/`. They were collected here first and moved
there when the role was allocated, which is what this repository does with a
description once something owns the subject.

### The ecosystem, and what we cannot see of it

`python3 tools/ecosystem.py` prints who is in the ecosystem and how each looks:
declared or not, whether the policy check passes, whether there is a channel to
reach them, how long since anything moved. It is local, takes about a second,
and involves no assistant — `prompts/global_audit` is the version that has
somebody read across the answer.

What it establishes is **form on a checkout**, and the gaps are worth naming
because a table invites more confidence than it has earned:

- **Whether anybody actually runs the check.** A member's own CI is the only
  evidence of that and we cannot see it from here.
- **Which commit of the policy a member is pinned to**, and how far behind that
  is. It is in their workflow file, so it is readable in principle and nothing
  reads it today.
- **Whether a checkout here is what upstream has.** These are working copies on
  one machine; a stale clone reports a stale answer with no indication that it
  is one. `scripts/install_eo --status --fetch` answers this much of it —
  branch, distance from upstream, whether the tree is dirty — and
  `tools/ecosystem.py` still does not read it.
- **Anything about the tools themselves.** Not whether they work, not whether
  they are maintained, not whether the thing they produce is any good.

*TODO*, in the order they are worth doing: read each member's `anoieu.yml` for
its pin and report the distance; carry the distance `scripts/install_eo
--status` already measures into this table, so a stale row says so where
somebody is looking; and give the table a `--json` mode if anything ever wants
to consume it. None is started.

**Getting the ecosystem onto a machine** is the other half of the same list, and
it is [`../scripts/install_eo`](../scripts/install_eo). What to clone is derived
from the inventory rather than listed again — a url and a repo id are all a clone
needs, and `ethos` and `ethos-eoc` share a tree because the inventory says they
share a repo id. It installs by default; `--dry-run` prints exactly the commands
a run would execute; `--status` reads the rows back off the disk.
[`../tools/checkouts.json`](../tools/checkouts.json) holds only what cannot be
derived: `ethosEoc3`, cvc5's blobless clone, and cvc5 being opt-in. Where the
lists disagree — something fetched that nobody recorded, something recorded that
nothing fetches, a ref `tools/deps.json` reports on that the checkout does not
have — `--status` says so under `note:` and repairs nothing, because membership
is a decision a person makes. [What happens when we add a new
tool](#what-happens-when-we-add-a-new-tool-to-the-ecosystem) is the sequence in
full.

### Smaller, and not blocked on any of the above

**Adopt ethos's Eunoia formatter, once it is ready.** ethos ships a format tool
for `.eo`; it is not ready for production, so nothing in this repository uses it
and `.eo` and `.eos` here are laid out by hand. Two things follow while that
holds, and both are worth remembering because the second is easy to get wrong:
layout is not something we report on anybody — a difference in whitespace is
never a finding — and it is not something to normalise across a signature we do
not own, which would bury a real diff in an unrelated one. When the tool is
production-ready the work is small: run it over what we write, and consider
offering it as a check rather than imposing it as one. Nothing tracks its
readiness for us; somebody has to look.

## Where to start

1. Get the ecosystem: `scripts/install_eo`, then `--status`. Nothing here
   reads anything until the other repositories are beside this one, and the
   status view is the fastest way to see what the ecosystem currently is.
2. Read [`board.md`](board.md) for what is outstanding and in what
   order — it is the shortest answer to *what should I do next*, and the only
   page that carries one. [`roles.md`](roles.md) sits beside it and answers the
   other question the board assumes you can already answer: *whose is this, and
   whose is it not*. Read it before anything that touches a second repository.
3. Read this page, then [`reporting-workflow.md`](reports/reporting-workflow.md#the-workflow)
   if you are working a finding, or [`notes.md`](notes.md#the-design) if you are
   working on the tool.
4. Check the ladder above before touching any document in it.
5. If the task is the record itself, the ledger script in *The cheap route* is
   the first thing to build and nothing above it is blocked on the rest.
6. Run `python3 tests/run.py` and `python3 tools/policy_check.py`.
7. Leave the work staged.
