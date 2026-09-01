# The interface

**How a person drives this repository.** One page, addressed to whoever is
sitting at the terminal.

Not to be confused with two neighbours. [`usage.md`](usage.md) is the
**analyzer's** interface — what the tool takes, what each option means — and is
for somebody running a program. [`coherence.md`](coherence.md) is the
**maintenance** entry point — what this repository is responsible for and what
standards the work is held to — and is for whoever is doing the work, human or
agent. This page is the seam between those two: what a person says to get work
done here, and what comes back.

## The interface, in one sentence

> **Work with anoieu to develop the next epoch.**

That is the whole of it, and the shortness is the design rather than an
omission. An **epoch** is the span between one global announcement and the next
— [`epoch-policy.md`](epoch-policy.md) — and designing one is a role this
repository holds. Everything else a person asks for is either ordinary work that
needs no framing at all, or one of the named session shapes below, which are
specialisations of that sentence rather than alternatives to it.

**And this boundary is a conjecture.** We are guessing that the epoch is the
right level of abstraction to drive this repository from — not concluding it. The
guess has an argument behind it: the epoch is the unit at which change gets
announced, so it is the unit at which cost lands on somebody who did not ask for
it, and framing work that way forces the question *what comes out* alongside
*what goes in*. It is also the smallest unit with a boundary anybody outside this
tree can see.

**What would show the guess is wrong**, in rough order of how likely each is:

- **Most sessions turn out to be single-artifact work anyway**, and the epoch
  framing is ceremony wrapped around a one-file change.
- **Epochs get declared faster than the trees move.** That is already the live
  criticism of this ecosystem from outside, and an abstraction whose main output
  is governance is confirming it rather than answering it. The rate is countable
  in [`epochs.md`](epochs.md).
- **A person finds themselves fighting the framing** to get ordinary work done,
  which is the cheapest signal and the one to say out loud.

The levels below and above are real and switching between them costs nothing, so
none of this is a commitment. If the default is wrong, the fix is one line in
this file.

**A second, separate conjecture: how much of this a downstream repository should
know.** *Epoch* is our word for our planning unit; *global announcement* is the
interface. Today they coincide one-to-one, which is exactly why the leak is hard
to see — and it has already happened once, in a topic addressed to members that
stated a rule about *their* build in terms of *our* calendar. What a member
demonstrably needs looks like two things and neither requires the word.

That question is open, it is recorded as open in
[`epoch-policy.md`](epoch-policy.md), and `D16` asks the members directly, since
a protocol's defects are visible where it is received rather than where it is
written. **The practical rule while it is open: text addressed to members states
the rule without the word.** Adding a vocabulary later costs a sentence;
withdrawing one other repositories have written into their own documents costs a
great deal more.

## The contract

**What you supply:** direction, and the decisions that are nobody else's to make.

**What comes back:** changed files left in the working tree, arguments you can
disagree with, and a summary saying what was done and what was left. Checks are
run and their output reported.

**What never comes back**, whatever you ask for: anything sent to another
repository, any repository created, anything pushed, posted or published. Those
are structural — no code here can do them — and the reason is in
[`coherence.md`](coherence.md): the path from an idea to a public artifact must
have a person in it.

### The decisions only you can make

These are the inputs the work stalls without. If a session seems to be waiting,
it is almost always waiting on one of these:

- **starting or ending a child project**, and changing its scope;
- **creating a repository**, which is a security boundary and not a convention;
- **a footing** in [`../tools/ecosystem.json`](../tools/ecosystem.json) — no
  script writes that file;
- **granting a role**, and approving a handoff;
- **changing a prompt template**;
- **carrying anything to another repository** — a finding, a topic, an
  announcement — and choosing which repositories, and whether at all;
- **naming which discussion topic** is to be acted on. The response gate needs
  the name, so "handle the koine topics" stalls where "answer `koine-D9`" does
  not;
- **a stance on publishing**, for this repository and for each child project;
- **who actually gets notified of an epoch.** The log lists which tools an epoch
  *involved* and suggests which of them a person might tell — those are two
  different questions, the first a fact and the second a judgement. The judgement
  is yours entirely: all of them, some, one, or none, in whatever words. Nothing
  records what you chose, and a tool never told has not been wronged.

### The one thing that is not a decision

**An epoch may only be adopted at a commit where this repository's CI is green,
and a downstream tool must refuse it otherwise.** That is a hard constraint
rather than a judgement call, it is stated in
[`epoch-policy.md`](epoch-policy.md#the-hard-constraint-a-red-epoch-is-not-deployable),
and `python3 tools/bump_check.py --rev <sha>` decides it.

The practical consequence for you: **an epoch is not finished when the documents
are written.** It is finished when they are committed and the build is green at
that commit, and until then the entry in [`epochs.md`](epochs.md) says so and the
epoch is adoptable by nobody. Asking *is this epoch deployable yet* is a
reasonable end-of-session question and has a one-command answer.

## The commands

**Ten today**, each a prompt on its own, typed as it appears here. **The set is
expected to grow** — adding one is `R29`'s to propose and a person's to accept,
and a new command arrives with its output shape defined, not discovered.

**This table is the ground truth for the command set.** Everything below that
lists commands is a copy of it, and `tests/run.py` compares them.

| command | what it does |
| --- | --- |
| `make epoch` | **not yet supported.** Would mean: make it better, *then* stage — the composite of doing the work and `epoch stage`. The one command not of the form `epoch <verb>` |
| `epoch help` | print the commands, and the ecosystem's health |
| `epoch status` | which level this epoch is at, and what the next one would take |
| `epoch advice` | what the agent thinks the most promising work for the next epoch is |
| `epoch plan` | attempt `brainstorm` → `planned`. Opens the protected rings again |
| `epoch stage` | attempt `planned` → `staged`. Needs an epoch with content |
| `epoch brainstorm` | drop to `brainstorm`. Always available, needs nobody |
| `epoch dry run` | evaluates every gate, emits the summary and block, **changes nothing** |
| `epoch deploy` | moves the epoch's status — and only to `deployed` on the build system's authority |
| `epoch double check` | **not yet supported.** Would mean: was a deployment received. [What that means is undefined](epoch-policy.md#after-deploying-epoch-double-check), which is why |

### `epoch status`

**It tells the person where they are and what to type**, in those words, before
anything else:

```text
epoch: E1

You are currently in "brainstorm".
Type "epoch plan" to move to "planned".

  in play ....... discussion.md, board.md, the ynoia registers, notes
  not in play ... vision.md (the kernel), policy.md, the checker, the prompts,
                  the reporting positions
  what it takes . a person's word — only our own files are at stake
```

**The second line names exactly one command**, the one that moves up from here,
because offering a menu at a status is how somebody ends up choosing a transition
rather than earning one. Where there is no command it says so instead:

| at | the second line |
| --- | --- |
| `brainstorm` | `Type "epoch plan" to move to "planned".` |
| `planned` | `Type "epoch stage" to move to "staged".` |
| `staged` | `Type "epoch deploy" to move to "deployed".` |
| `deployed` | `"installed" is observed in members' trees. There is no command for it.` |
| `installed` | `There is nothing above "installed".` |

**And below `brainstorm` there is nothing**, so at every other level it adds
`Type "epoch brainstorm" to drop back.` — down is free, and the one way out that
is always available should always be visible.

### `epoch help`

Printed as a command line prints it — terse, aligned, no prose:

```text
epoch — the Eunoia epoch build system

usage: epoch <command>
       commands may be chained with `;`                       (NOT YET SUPPORTED)

commands:
  make epoch           make it better, and stage a deployment   (NOT YET SUPPORTED)
  epoch help           print this list and the ecosystem's health
  epoch dry run        evaluate every gate; print the summary and the block; change nothing
  epoch deploy         move the epoch's status
  epoch status         which level this epoch is at
  epoch advice         what looks most promising for the next epoch
  epoch plan           attempt brainstorm -> planned; opens the protected rings
  epoch stage          attempt planned -> staged; needs something to stage
  epoch brainstorm     drop to `brainstorm` — always available
  epoch double check   was a deployment received                (NOT YET SUPPORTED)

health:  rendered at run time by `tools/ecosystem.py --health` — the values below
         are an example and are never the values

    members            4
  ! policy             3 of 4 passing
  ! topics owed to us  16
  ! epoch              E1, planned

status:  brainstorm -> planned -> staged -> deployed -> installed
         scrutiny rises left to right; `planned` says nothing
         up is earned and never asked for; down is free and needs nobody
         only the epoch build system role moves an epoch to `deployed`
         `installed` is read out of members' trees and may never be true

see:     docs/epoch-analogy.md   the short way in
         docs/interface.md       these commands
         docs/epoch-policy.md    what an epoch is, and the gates
```

**It no longer reads nothing, and that was a deliberate trade.** `help` used to
have an empty read set, which made it instant by construction; carrying the
health summary costs it one local command, measured at **1.3s** and entirely
offline. The trade was taken because a help text that tells you what you *could*
type while saying nothing about the state you are in is the less useful half of
the page.

**What it still does not do is ask the network.** Whether our build is green at a
commit is the bump gate's question and costs a round trip; that stays in
`epoch dry run`. The line is *cheap and local* rather than *free*.

**The health values are rendered, never stored.** The block in this document is an
example of the shape and is not the values — a help text carrying yesterday's
numbers would be the stale cache this repository keeps warning about, and the
only safe version is the one computed when the command runs.

**It is a cache, and that is why it is fast.** The text above is a precomputed
answer to *what can I do here*, written once instead of derived from four
documents each time somebody asks. Caching is what makes a command quick — and
the price of every cache is that it can go stale, so this one is compared against
its ground truth by `tests/run.py` on every run.

**The maintenance question, which is the one to actually ask:** *is the help
output still an accurate reflection of what these things do?* The comparison
answers only half of that — that the same commands are named in both places. It
cannot tell whether `deploy` still does what its one line says. That half is
read by a person, and it is worth asking whenever a command's behaviour changes
rather than only when its name does.

**Recognise them consistently, and do not invent variants.** The same prompt gets
the same reading every time.

**`make epoch` is not yet supported.** It is registered, named and listed so that
the shape is fixed before anything implements it, and typing it gets a reply
saying so:

```text
epoch: `make epoch` is recognised and not yet supported
       what it will mean: make it better, and stage a deployment
       nothing was run
```

**That is a different reply from a syntax error, and the difference matters.**
*Unrecognised* means the front end does not know what you asked for. *Recognised
and unsupported* means it does, and the thing is not built — which is
information, and tells you to stop trying rather than to check your spelling.

**`make epoch` is the one exception to the shape**, and it is deliberate: it is
what somebody types at a build system, and the whole arrangement is named after
that. One documented exception is affordable where a silent one would not be —
and it is why the scoping rule below is *a prompt that plainly meant to be a
command*, rather than *a prompt beginning with `epoch`*.

**It does not design the epoch.** Designing one is the person's and is not a role
here; `make epoch` assembles inside a direction already set, and everything it
produces goes through the feedback protocol below. Whether the designing could
ever be automated is [an open research
question](epoch-policy.md#make-epoch--and-the-research-question-it-is-a-probe-for),
and every run of this command is a data point for it.

**When a prompt plainly meant to be one of these and is not, say so and do
nothing else.** The model for the reply is a compiler error — name what was
typed, name what is accepted, stop:

```text
epoch: unrecognised command "dry-run"
       accepted: make epoch | epoch help | epoch dry run | epoch deploy | epoch status | epoch advice | epoch plan | epoch stage | epoch brainstorm | epoch double check
       did you mean: epoch dry run
       nothing was run
```

**Chaining with `;` is planned and not yet supported.** The design is settled so
that it is fixed before anything implements it: each command runs in order, each
prints its own output, and a refusal in one does not stop the next — `;` means
*and then*, not *and only if*, exactly as a shell does. Typing a chain today says
so and runs nothing.

**Each command will still do its one thing.** The chain is a property of the
*prompt*, not of the commands: nothing is merged, nothing is half-run, and two
chained commands produce exactly the two outputs they would have produced
separately. That is what makes it safe to add later without revisiting anything
above.

**What was considered and set aside.** Restricting chains to read-only commands
would have preserved a property worth naming — that a state-changing command is
typed by somebody who has just looked — but it is weaker than it first appears:
every consequential transition is gated on its own criteria, so acting on a stale
read cannot get past a gate that a fresh read would have stopped. The caution
survives as a caution rather than a rule.

**`&&` is the obvious next form and does not exist.** *Run the next only if this
one succeeded* is the semantics somebody will eventually want — chaining
`epoch plan && epoch stage` and meaning it — and adding it is a decision rather
than an omission.

**Where the typo is far enough off that no command is an obvious match**, drop
the guess and point at the list instead — *it looks like you were trying to use
the epoch build system; try `epoch help`*. One line, no speculation about which
command was meant, and still nothing run.

**The compiler is an aspiration, not an implementation**, and taking it literally
would be the mistake. Nothing parses these, no program enforces a grammar, and
reading this section as a specification would be the same error as reading the
approval block as a verification. What is being asked for is **consistency**: one
reading per prompt, a near miss named rather than guessed at, and no command ever
half-run.

**What is not a command is ordinary work.** A prompt that discusses epochs, asks
a question about one, or happens to mention a command inside a sentence is not a
command and gets no error — it gets answered. The error exists for the case where
somebody clearly meant to run one and it did not match, because that is where
guessing costs something: a protocol running that nobody asked for.

**Guessing is the failure, and *did you mean* is fine to say and never fine to
act on.** Same rule as the misaddressed-prompt paragraph and the response gate —
do not do the plausible thing.

**The one transition that matters is not protected by any of this.** Even a
perfectly typed `epoch deploy` cannot move an epoch to `deployed` on the front
end's say-so; that authority belongs to the build system alone. The commands are
a convenience for a person, not a source of permission.

## A command does its one thing

**Every command does what it says and stops.** A mode switch prints the
transition and nothing else; it does not also survey the ecosystem, list what is
outstanding, or say what should happen next. Those are answers to questions
nobody asked, arriving attached to a command that was asked — which makes them
hard to decline and easy to mistake for output.

**Advice in particular is never volunteered.** It has a command, and the command
is how it is requested. An agent that offers it unprompted is doing the thing the
response gate forbids in the other direction: acting on its own reading of what
would be useful.

### `epoch advice`

**What the agent thinks the most promising work for the next epoch is.** A few
candidates, ranked, each with why it is promising and what would move it.

Four things it must do:

- **Say it is a judgement**, because it is one. Nothing here is measured, and the
  ranking is an opinion of the same kind [`vision.md`](vision.md) reserves for
  people — offered so it can be argued with, not settled.
- **Cite what it read.** Every candidate names the evidence behind it, so a
  ranking can be checked rather than taken.
- **Name what it is not recommending, and why.** Advice that lists everything is
  a survey wearing a recommendation's clothes, and the omissions are where the
  judgement actually lives.
- **Say what would change the order.** A ranking with no falsifier is a
  preference.

> **It is not disinterested, and the command says so every time.** The agent
> giving the advice is the one that would do the work, so it will tend to favour
> what it finds tractable over what is most valuable — the same failure as asking
> a repository whether it should hold a role. **The reader should discount
> accordingly**, and the strongest correction available is that the advice names
> its omissions, which is the part hardest to fake.

**It changes nothing and starts nothing**, and it **works at every status** —
because it means something different at each. Advice that ignored the level would
wander into whatever the agent found interesting, which is exactly the failure the
conflict of interest above predicts.

| at | advise on |
| --- | --- |
| `brainstorm` | **research projects** — open questions worth pursuing, and which would change something if answered |
| `planned` | what has to be **settled** before this could be staged |
| `staged` | **how to clear the gates.** Almost always: how to fix CI |
| `deployed` | **how it gets installed** — what members would need, and what is standing in the way |
| `installed` | **nothing.** There is no advice to give about a finished epoch |

**`installed` returning nothing is not a gap.** The epoch is done, and there is
nothing useful to say about a finished one — the next thing worth anybody's
attention is what the next epoch should be, and that is a question for the
person, not advice about this one.

In `staged` it is the one thing that may exceed a simple actionable request,
because it was asked for — and even there it stays inside the level: **how to fix
the build, not what the build ought to have been.**

## How much is said depends on the level

**In `brainstorm`, explain everything.** Reasoning, trade-offs, what was
considered and dropped — that is the entire product of the level, and a
brainstorm that returned only conclusions has thrown away the part worth having.

**In `staged`, give simple actionable requests and nothing else.** The work has
been decided; what remains is a person doing specific things. One thing at a
time, in the fewest words that make it doable, with **no implementation detail**,
no account of what changed, and no reasoning unless it is asked for.

**A staged epoch that starts producing paragraphs has slipped a level without
saying so.** The honest response is `epoch brainstorm` — drop, explain, come back
up — rather than keep explaining from a level that is supposed to be past
explaining.

## What a command prints

Two things, in this order:

1. **The summary** — what this epoch is, in a form a person can argue with.
2. **The block** — where it stands against its gates.

The summary comes first because it is the part worth disagreeing with. Where the
epoch stands is only interesting once you accept it is the right epoch.

### The summary

**Commit-message shaped**: a subject line somebody can scan, then a short body
saying what members are asked for, what is only notice, and what changes for
nobody. It is written for **a person who has not read the announcement**, and if
it cannot be followed without one it has failed — and the fix is the summary,
never the reader.

**Brief, and linked.** It stays short by *pointing* rather than explaining: each
contract names where it is defined, so the summary carries the shape of the epoch
and the documents carry its content. A summary that grows until it is complete has
become a second copy of the announcement, which is the drift this repository
spends most of its discipline avoiding. **If a claim in it needs a paragraph, it
needs a link.**

**It is derived, not authored.** The protocols are what downstream agents
actually receive; the summary is a compressed view of them. Where the two
disagree, the protocols are what deploys — so **a summary that has drifted from
them is the most dangerous defect this interface can have.** A person approving a
summary that overstates or understates the epoch has approved something that is
not going to happen.

### The health summary — one abstraction, several surfaces

**A health summary is a short, fixed list of *indicators*.** Each is a name, a
value a person can read, and one of three verdicts. `tools/ecosystem.py --health`
computes it; `health()` returns it as data and `render_health()` draws it, so a
second surface adds a call rather than a second implementation.

| verdict | mark | means |
| --- | --- | --- |
| `ok` | *(blank)* | nothing to look at |
| `attention` | `!` | somebody should look |
| `unknown` | `?` | we could not find out |

**`unknown` sits with `attention`, never with `ok`** — the same reasoning as the
bump gate's three exit codes. *We asked and it is wrong* and *we could not ask*
are different facts, and neither is a pass. A summary that rendered an unknown as
a blank would be the most misleading thing this interface could print.

**Kept deliberately abstract, and short.** The indicator set today is four —
members, policy, topics owed, epoch — and it is expected to grow. Adding one is a
decision rather than a convenience, because **every surface shows all of them**:
a cheap indicator added here is paid for on every command that renders a summary.

**Everything in it is offline.** That is what lets any surface render it without
first deciding whether it can afford to. What costs a network round trip —
whether our build is green at a commit — is deliberately absent: that is the bump
gate's question, and `epoch dry run` is where it is asked.

**Where it is meant to appear**, beyond `epoch help`: the dry run's output, any
later command that reports state, and `ecosystem.py`'s own table. It is written
as shared infrastructure because it will be rendered in several places, and the
one thing that must not happen is two of them disagreeing about what *healthy*
means.

### The epoch feedback communication protocol

**Arguing with the summary is the named protocol by which a person gives feedback
on an epoch**, and it runs from here to the end of this section.

**This is why the summary is printed.** The front end is where a person gives
feedback on the epoch under consideration, and the summary is the handle: it lets
somebody steer a few thousand lines of protocol without reading them.

It is a **communication protocol** in the same sense as the others in the epoch
build system — a shape a message takes and a defined thing that happens next —
except that this one runs between a person and an agent rather than between two
repositories. That is the whole reason it is fussy about interpretation: the
other protocols move text, and this one moves *intent*, which does not survive
paraphrase.

Two kinds of argument, and telling them apart is the front end's first job:

| the argument is about | what it means | what changes |
| --- | --- | --- |
| **phrasing** | the description is unclear, mistoned, or misleading *as text* | the summary. The epoch itself does not change |
| **content** | you disagree with what the epoch **does** | **the communication protocols change**, so the agents who carry the epoch out receive it differently |

**A content argument is not a request to rewrite the summary.** It is an
instruction to change what agents are *told* — the announcement, the policy text,
the covering prompt — so that what they *do* is different. Rewriting the summary
in response is the worst outcome available: the description would change, the
epoch would not, and the two would then disagree in exactly the way the section
above calls the most dangerous defect here.

### Before acting on a content argument, say how you read it

**The translation from *I disagree with this sentence* to *these four documents
change* is where meaning gets lost**, so it happens out loud and is confirmed
before anything is edited. State, explicitly:

- **which kind** of argument it was taken to be, and why;
- **what the objection was understood to be**, in your own words rather than a
  paraphrase of theirs, so that a misreading is visible rather than agreeable;
- **which documents would change**, and what each would then say;
- **what a downstream agent would do differently** as a result — the actual test
  of whether the change is the one being asked for;
- **what would not change**, because a content argument usually touches less than
  it first appears to.

Then stop and wait. A misreading is cheap here and expensive one step later,
where the edits land in the documents members read.

**Afterwards, re-derive the summary and print it again.** Not *edit* it — derive
it from the changed protocols, so the round trip is what shows they changed in
the way the argument asked for. **A summary hand-edited to match an argument is a
wish; one re-derived from the documents is a description.**

## Session shapes

Each is a specialisation of the one sentence. The prompt is the short form; none
of them needs to be typed exactly.

| you want | say something like |
| --- | --- |
| **the default** — decide and build the next stretch of work | *work with anoieu to develop the next epoch* |
| **an inventory** — where the ecosystem stands, what is owed to us | *take an inventory of the ecosystem; check the children and what action items are given to us* |
| **one topic answered** | *answer `koine-D9`* — the id is what makes this legal |
| **a finding carried** | *file `ethos-8` and `ethos-9`* — and expect to be told it stops at a person |
| **a judgement, with nothing changed** | *take no action, just judge: <the thing>* |
| **a readiness pass before something goes out** | *are we ready to advertise `D14`? review it* |
| **anything to do with an epoch** | one of the three commands below, typed exactly |
| **ordinary work** | just ask. A check, a document, a test, a bug — no framing needed |

**The judgement shape is underused and is the cheapest one.** *Take no action,
just judge* returns an argument and changes nothing, which makes it the right
first move whenever you are unsure the work is a good idea. It is also the
shape that has most often changed what got built.

## The levels, and how to drop to a lower one

The epoch is the **default**, not the only altitude. Six levels, highest first,
and moving between them costs nothing — **you switch by saying so**, and no
session is committed to the level it started at.

| level | the unit | say something like | when it is the right one |
| --- | --- | --- | --- |
| **the vision** | what the work is *for* | *is this ecosystem aiming at the right thing* | rarely, and it is argued rather than decided here — a person has the most standing at this level and an agent the least |
| **the epoch** | a stretch, ending in one announcement | *develop the next epoch* | several things should change together, and somebody outside will need telling |
| **the board** | one outstanding item | *work `B3`* | the work is already identified and queued, and you want it done rather than reconsidered |
| **the role** | one responsibility | *work on the fuzzer* | a whole area needs attention and the items for it do not exist yet |
| **the artifact** | one document, check or witness | *add a check that a semantics block declares its sort* | most ordinary work |
| **the code** | a function, a test, a bug | just describe it | the majority of real sessions, and it needs no framing at all |

**Dropping down needs no permission and no ceremony.** *Forget the epoch, just
fix this* is a complete instruction. The lower levels are not a lesser use of the
repository — the bottom two are where anything gets built, and a week of them
with no epoch declared is a good week, not a stalled one.

**Going up is the expensive direction**, because the higher two levels produce
prose by construction. Ask for them when you want a decision or an argument, and
expect the diff to be documents.

### If you want the low-level details

Three concrete routes in, none of which involves this page's framing:

- **Read what is outstanding**, and pick: [`board.md`](board.md) is at most
  twenty items in priority order, each with the next thing to do already written.
  *Work the top item* is a complete session.
- **Read what everything is for**, and pick an area: [`roles.md`](roles.md), one
  entry per responsibility, with what each owns. *Work on what `R3` owns* scopes
  a session to the fuzzer and its corpus without naming a file.
- **Read what the machinery says about itself.** `python3
  tools/policy_check.py --coverage` prints every rule that is checked, every rule
  that is not, and why — and `python3 tools/ecosystem.py` prints the ecosystem as
  a table. Both take about a second, need no agent, and are the fastest way to
  see the actual state rather than a description of it.

### Signals you are at the wrong level

**Too high:** the diff is entirely documents and the summary is longer than the
change. If you asked for an epoch and got five pages and no code, either the
level was wrong or the epoch was empty and should have been declined.

**Too low:** a correct change that quietly contradicts a convention nobody
re-read — a check added without anybody asking whether it should be checkable at
all, a rule appended that a neighbouring document already forbids. This is the
failure the higher levels exist to catch, and it is the reason the default is not
the bottom of the table.

## Prompting advice

Learned from sessions that went wrong, in rough order of how much each cost.

**Say which repository the prompt is for.** These trees are alike on purpose and
sit side by side on one disk, and a prompt meant for one arriving in another is
a real failure with a real incident behind it — the rule is *A prompt may not be
for this repository* in [`policy.md`](policy.md). One clause at the top prevents
it.

**Never ask a repository whether it should hold something.** *Should koine own
the communication protocols* is a question koine cannot answer: an agent asked to
find the case for X will find it, and the result is indistinguishable from an
honest answer. Ask the register that would record it, or ask the repository the
different question — *what would you accept*.

**Name the topic, not the pile.** The response gate requires it, so this is the
difference between work happening and a clarifying question coming back.

**Say what you want back**: a judgement, a draft, or a change. The three have very
different costs and the wrong guess wastes a whole turn.

**Ask for removals, not only additions.** Every protocol here is held to *an
addition says what it removes*, and the counter that watches it has reported
three rounds and three increases. Nothing counts pages at all. A prompt that says
*what comes out* is the one that moves that number, and it is rarely asked for.

**State the conservatism you want.** *We are still testing whether this workflow
is safe* changes what gets done, not just how it is described — it is the
difference between a register being edited and a register being reported on.

**Correct mid-turn; it is cheap.** Several of the better outcomes here came from
a one-line correction landing while work was in flight — *exercise this in
moderation*, *iogos is a joke, it has a concrete scope*. Waiting until the end
costs a full turn of rework.

**Give the principle rather than the edit** where you can. *You can do anything
you want if the repository's policy says it is AI generated* produced a rule that
generalises; the equivalent list of permitted actions would not have.

## What you will have to correct

Said plainly, because knowing the failure modes is most of what makes the
interface usable.

**Overclaiming, in the direction that reads as progress.** The characteristic
error is recording something as settled when it is proposed — two repositories
were written into the inventory as holding a footing before the protocol that
grants it existed. **The tell is a register entry that asserts something nobody
outside this tree has agreed to.**

**Governance outgrowing the thing it governs.** This repository produces
documents faster than it produces analysis, it has been told so from outside, and
asking for a stretch of work will reliably produce more pages unless the ask says
otherwise. *What comes out* is the counterweight.

**Unverified numbers.** Counts, dates and "N rounds" claims are the ones to
distrust; a readiness pass has caught a wrong one. Asking *verify the claims*
before something is carried is worth the turn.

**Small mechanical slips in the conventions themselves.** A pinned topic ending
up below an unpinned one, twice, from the same cause. The conventions are
hand-kept and a check does not exist for most of them.

## Where this goes next

The interface is one sentence because the ecosystem is small and one repository
holds the governance. Designing the next epoch is `R27` in
[`roles.md`](roles.md), and it is listed as moving to the governance repository
when that exists — at which point this page describes an interface to a tree that
no longer decides what the next epoch is, and it should be rewritten or moved
rather than quietly left standing.
