# AI-assisted development

The tools in this ecosystem are mostly written by agents. This page is what that
work should be aiming at.

It is the sibling of [`policy.md`](policy.md), and the two divide the space
between them: that page governs speculative work — a directory named after a
tool that does not exist — and this one governs the real thing, a tool somebody
is actually building. Both are written for **any repository in the Eunoia
ecosystem**, not just this one. ethos, logos, eudaimonia, the compiler and
anything downstream are all being built the same way, and a contributor who has
read one repository's answer should recognise the next one's.

Cite a tenet by name rather than by number. Append; do not renumber. Retire a
tenet in place, with a line saying why.

---

## What changes when an agent does the work

Writing the code stops being the constraint. A front end appears in an
afternoon, a check catalogue by the end of the week, and a plausible-looking
document about any of it in minutes. The scarce things move elsewhere: knowing
which of the output is right, knowing when a thing is done, and getting the
result in front of somebody who can judge it.

That inversion is what the four tenets below are a response to. None of them
would be worth writing down for one person working at a person's pace, because
the natural brakes — fatigue, the cost of typing, the reluctance to rewrite
something that works — do the job. An agent has none of those brakes, and will
improve a tool indefinitely, competently, and without ever shipping it. What
follows is the substitute. The last tenet is different in kind from the other
four: they are about how to build, and it is about who the building is for and
who gets to decide it counted.

## The tenets

**1. Evolve to be fruitful to another tool as quickly as possible.** The state a
tool is aiming for is not *finished* and not even *correct*; it is *something
else can now use this*. Take the shortest path to that state, and take it early
enough that it hurts — a narrow version whose output another tool consumes today
beats a general version that consumes nothing and is consumed by nothing.
Emitting a machine format over one signature is further along than emitting
prose over all of them.

The working form is to name the consumer before the work starts: the tool, the
repository, or the job that will read the output, and the exact artifact it
takes. If no consumer can be named, the tool is being built for its author, and
an agent will happily keep building it for its author forever.

Fruitfulness compounds inside a repository as well, and that half is much
cheaper. The fuzzer here became useful on the day it stopped having its own
opinions about how a finding should be presented and emitted into the report
that already existed — same ledger, same fingerprints, same renderers, its own
code range. It inherited an audience, a CI job and a reporting discipline it did
not have to build, and the cost of that was giving up a format nobody wanted.

*The test:* something outside this tool behaves differently because the tool
exists. Not *could* — *does*. A tool whose only consumer is its own test suite
has not started yet. This is a description of how the ecosystem already works
rather than an aspiration, and *The record* below is the evidence.

**2. Move fast, and treat CI as the thing that lets you.** Agility is the right
default: build the narrow version, run it against something real, throw away
what the real thing disproved. The common mistake is to read continuous
integration as the tax paid for having moved quickly. It is the reverse — it is
what makes speed survivable, and the reason a change to the core of an analyzer
can be made on a Tuesday by someone who was not there when it was written.

What it buys is concrete here. A change that invents a false positive fails
*this* build before it ever reaches somebody else's, because CPC's output is
pinned to a committed baseline. What ethos actually said about a witness is
recorded from a real run and never typed by hand, which is the whole of what
backs the claim *ethos accepts this and should not*. Generated documents are
regenerated and diffed, so a page cannot drift from the code beside it.

Three properties turn CI from a nuisance into the friend it should be, and all
three are worth paying for in the first week rather than the tenth:

- **It goes red for your reasons only.** Restore recorded versions rather than
  branch tips, and ask separately, on a schedule, whether upstream has moved. A
  build that fails because somebody else pushed trains everybody to ignore red,
  and a red build nobody reads is worse than no build at all.
- **It is cheap enough to be run rather than deferred.** The corpus here is read
  as text and never built, which is why every push can afford to read all of it.
- **It remembers what you will not.** This is the part that is specifically
  about agents. An agent does not recall that a check was narrowed last month
  and why, and will widen it back with an excellent explanation. The witness
  files, the oracle and the baseline are the memory; they are consulted by the
  machine because they will not be consulted by anyone else.

*The test:* you can make a sweeping change to the core and know within minutes
whether it was wrong. Where you cannot, the next agent to touch that code will
be timid where it should be bold and bold where it should be timid, and both
cost more than the CI job would have.

**3. Build one self-contained thing, and make it clear from the front README.**
Self-contained means the repository can state its own results without anything
that is not in it: dependencies declared and pinned, fetched by the run rather
than assumed present on the machine, and results that carry whatever regenerates
them. A tool that is only correct on its author's laptop has produced nothing,
and a number nobody else can re-measure cannot be argued with.

Clear from the front README means a reader who arrives with no context leaves a
screen or two later knowing what the tool is, what it finds, what it refuses to
claim, how to run it, and where the rest of the documentation lives. The refusal
belongs there with the rest, not three clicks in: *a successful pass is not a
clean bill of health* sits near the top of this repository's README because a
caveat a reader has to go looking for has not been published.

This is also where [`policy.md`](policy.md) attaches, and the two rules are one
rule seen from either end. The front page carries what the tool does; a
speculative account of somebody else's subject goes in `tools/X/` under that
policy, unadvertised, importing nothing and imported by nothing, deletable
without consequence. A front page that mixes the two makes the reader do the
sorting, and readers do not sort — they average.

*The test:* hand the README to somebody who has never seen the ecosystem, and
ask them what the tool claims and what it declines to claim. Everything they get
wrong is a defect in the README rather than in their reading. What may then
change on that page, and how fast, is *The front page* below.

**4. Produce a deliverable, where there is one to produce.** A tool that runs is
not a result. The result is whatever leaves the repository and lands with
somebody: a report they read, a table with its numbers and the command that
regenerates them, a reproducer small enough to argue with, a page rendered for
an audience that will never clone anything. Decide what it is at the start,
because a deliverable chosen at the end is a summary of whatever happened to get
built, and reliably the wrong shape for anyone downstream.

**A deliverable need not be a file.** The most valuable one on the record below
is an argument: eudaimonia's evidence and motivation that logos's proof of
correctness ought to be modularized. That is not a patch, a report or a table,
and it is worth more to logos than any of the three would have been. Evidence
that something should be done differently, a measurement nobody had taken, a
question two projects turn out to be stuck on for the same reason — each of
these leaves the repository and lands with somebody, which is the whole of the
test. What disqualifies a thing is not being immaterial; it is having no
recipient.

The qualification is meant seriously. Plenty of work has no external deliverable
— infrastructure, a refactor, one more check in a catalogue that already ships —
and inventing one to satisfy this tenet is worse than admitting there is none.
But that is a decision to be made and stated, not a gap to be left; *it will be
obvious later what this was for* is not the same as having decided.

Where there is a deliverable, this page hands over to
[`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md) and
[`../docs/reporting-policy.md`](../docs/reporting-policy.md): what may be said
about code you do not own, what separates a candidate published under your own
name from a finding carried to its owner, and how a row is closed. Speed belongs
to producing the deliverable. It does not belong to sending it.

*The test:* name the artifact and its recipient in one sentence. If the sentence
needs a paragraph of context to make sense, the deliverable has not been chosen
yet.

**5. Until a human decides otherwise, the tool is vaporware.** Not as a
judgement on its quality — it may run, pass everything and be genuinely useful —
but as a statement about its standing. A tool an agent has built is a proposal.
What turns it into a part of the ecosystem is a person deciding to rely on it,
to run it in their own CI, or to take over developing it, and that is not a
decision the agent makes or announces on their behalf. An agent describing its
own work as adopted, established or authoritative has skipped the only step that
confers any of those.

Two things follow, and the second matters more.

The first is that the work should be arranged so the decision is cheap to make
and cheap to act on, which is most of what tenets 1 to 4 are for: a README that
answers the question in one screen, CI that demonstrates the claims rather than
asserting them, an artifact somebody can pick up and judge in a minute.
Everything that makes a tool legible is also what makes it possible to take
over.

The second is that **a human taking the reins is the best ending available, and
is a sign of progress rather than a rebuke.** Somebody deciding to drive the
development themselves has found the thing useful enough to want control of it,
which is a far stronger signal than approval and the strongest one this work can
produce. The agent's job at that point is to make the handover easy: describe
the state of things plainly, including what is half-built and what was never
right; do not defend the design; and do not treat a rewrite of your code as a
regression. That was the point. [`policy.md`](policy.md) has the matching idea
for speculative work, where a person picks between graduating, folding in and
retiring; this is the same decision taken about a tool, with ownership rather
than a directory as the thing that moves.

*The test:* ask what a person would have to do to take this over on Monday
morning, and whether anything in the repository is in their way.

## The record

Six exchanges that have already happened. They are listed because a tenet with
no instances is a preference, and because the shape of a real exchange is more
instructive than the rule abstracted from it. Everything below is as of the
commits [`deps.lock`](deps.lock) records — cvc5 `aee8742`, ethos `3cf1c03`,
logos `47f29bf`, eudaimonia `45e34e0` — and re-measurable from them.

### The tools

| tool | where | what it is |
| --- | --- | --- |
| **cvc5** | `cvc5/cvc5` | the SMT solver, and the owner of CPC — the proof calculus everything downstream is built from, at `proofs/eo/cpc/` |
| **ethos** | `cvc5/ethos` | the proof checker: reads a Eunoia signature and a proof and says whether the proof checks. `user_manual.md`, the definition of Eunoia, lives here too |
| **ethos-eoc** | `cvc5/ethos`, branch `ethosEoc3` | the Eunoia compiler: the second binary from the same tree, taking a signature *and its semantics* and emitting the Lean development, an SMT-LIB verification condition per rule, and a SyGuS query per rule |
| **logos** | `ajreynol/logos` | the Lean development: a generated deep embedding of CPC carrying the claim that its rules are sound against a semantics of SMT-LIB, and the owner of `Cpc.eos`, CPC's official semantics |
| **eudaimonia** | `ajreynol/eudaimonia` | the calculus template: bring a signature and a semantics, get a Lake project with a checker, its proofs, its regression suite and its documentation |
| **anoieu** | `ajreynol/anoieu` | the static analyzer for `.eo` and `.eos`, and a fuzzer for the checkers that read them |
| **dokimasia** | `ajreynol/dokimasia` | reads cvc5's C++ proof-production code and asks whether any path through the solver reaches an inference no proof step covers |

### The exchanges

**{ethos, logos} → cvc5.** These are the two artifacts cvc5's proofs rest on,
and neither is a library cvc5 links. ethos is the checker cvc5's emitted proofs
are actually run through, and the calculus it checks against lives in *cvc5's
own tree* — `proofs/eo/cpc/Cpc.eo`, with the expert extension beside it — so the
interface between the two projects is a file in the consumer's repository rather
than an API in the producer's. logos supplies the other half: the development
compiled from that same calculus, in which the rules cvc5 emits are stated to be
sound against a semantics of SMT-LIB. Worth noticing for tenet 1 is that both
were consumed long before either was finished — the soundness development is
still the largest incomplete thing in the ecosystem, and the arrangement depends
on it anyway.

**ethos → logos.** logos vendors ethos and consumes cvc5's signature:
`install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, and the C++ checker
is built alongside the Lean one. This is the cleanest instance of the tenet in
the ecosystem — a proof checker written in C++ for one purpose becoming a build
dependency of a Lean development written for another, because it was the thing
already able to answer *does this proof check*. It also shows the cost of being
consumed: a defect in CPC arrives in logos unchanged, which is what
[`logos-1`](../docs/reports.md#logos--the-lean-development) records, and why
auditing the copy filed cvc5's findings under logos's name seventeen times
before we stopped reading it.

**eudaimonia → logos.** The most instructive exchange here, because what
eudaimonia delivers is not a file. It is the generalization of the thing logos
is an instance of — bring any calculus, get the project logos is — and in trying
to be that it hit a wall and reported where the wall stands: **evidence and
motivation that logos's proof of correctness should be modularized.** Its own
stated blocker is to *stabilize the SMT-LIB model as a fixed base that signatures
extend* and to *extract the invariant core*: separate what is
calculus-independent from what a signature contributes, give the pieces
interfaces rather than adjacency, and replace per-rule repetition with a shared
support library.

The evidence under that argument is quantitative, and was a by-product rather
than the goal. logos's core checker proof runs to some 3,000 lines, its side
conditions to 257, its soundness theorem to 1,063 and its per-rule proofs to 591
files — and eudaimonia generates every one of those as a stub describing what
belongs in it, so the pipeline generalizes and the proof does not.
`examples/hello`, which declares three constants and one rule, gets 2,395
generated lines of which 370 are datatype and literal machinery it cannot use.
Nobody set out to audit how logos is structured; a second effort tried to reuse
it and found out where it does not come apart.

logos receives no patch and no report from any of this. It receives a reason to
restructure, reached independently, which is a thing a project can rarely
produce about itself — and it is the reason tenet 4 is worded abstractly. The
mechanical half is real too and should not be lost in the telling: eudaimonia's
pipeline fetches and builds the compiler, drives it over a signature, installs
what it publishes, **preserves hand-written per-rule proofs across a
regeneration**, and offers a `--check` mode that installs into a throwaway copy
and diffs. That third item is what separates a generated development somebody
can maintain from one that is re-done by hand every time the signature moves.

**eudaimonia → ethos-eoc.** The compiler claims that a second calculus is a
second pair of files rather than a change to the tool. eudaimonia is what
actually tries it, which makes it the falsification test, and its findings are
where the claim is not yet earned. Two of them, both specific: `examples/hello`
declares three constants and one rule, and 370 of its 2,395 generated lines —
15% — are datatype and literal machinery it cannot use; and its calculus profile
asks seven questions, answers five from what the compiler emitted, and records
`binders` and `value-ordering` on trust, because `SmtValueOrder.lean` is
identical between `Cpc` and `CpcMini` and so the compiler emits the same
ordering whatever the signature says. eudaimonia's own note that a declared
`value-ordering` "is a finding" is the pattern worth copying: the consumer of a
tool is the thing best placed to find where that tool is fixed in the places it
claims to be derived. It also builds ethos next to the compiler and cross-checks
the generated checker's verdicts against it, keeping two implementations on
purpose.

**anoieu → everything.** One row per project in
[`../docs/reports.md`](../docs/reports.md), each with an id and a state. To cvc5,
three real defects found on the first audit and confirmed against ethos — `cvc5-1`
is `proofs/eo/cpc/programs/Strings.eo:42` and `:55`, two programs declaring
`:signature ((Seq T)) Int` whose every case returns a Boolean — plus
[`report/cpc-audit.html`](../docs/report/cpc-audit.html), rendered for readers who
will not clone anything. To ethos, three confirmed defects and three diagnostics
worth improving, and separately two the fuzzer provoked: an uncaught C++
exception on `(declare-const f (->))`, and an error path that skips ethos's own
`Error:` convention. To logos, `Cpc.eos:542` defining `str.indexof_re_split`
where CPC declares `str.indexof_re`. To eudaimonia, `eud-1` and `eud-2` — answer
the signature contract, and the profile's two declared questions, from the
signature and its semantics *before* a checker is generated rather than from the
compiler's output afterwards. To Eunoia itself, seven proposed changes to the
language and its manual. What it took to become fruitful to that many consumers
was not generality: it was emitting findings in a form somebody could read and
disagree with, which is also why the fuzzer could join by adopting the existing
ledger under codes `FUZ0001`–`FUZ0005` instead of inventing a second one.

**dokimasia → cvc5.** The same subject as anoieu and a different question: it
reads eight stages of cvc5's proof-production pipeline in C++, from
configuration through elaboration to the Eunoia serialiser, and asks whether any
path reaches an inference no proof step covers — particularly under
`--safe-mode=safe`, where cvc5 promises that anything it solves it can prove.
The two tools share no code and neither depends on the other; what they share is
a position, [`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md), maintained here and
referenced there, which is its own kind of exchange and a cheap one. They meet at
exactly one seam — `src/proof/eo/`, where cvc5 turns an internal proof into
Eunoia. A rule cvc5 emits that CPC does not declare is invisible to each tool in
isolation and visible from either side of it. That is `cvc5-6`, it was requested
by cvc5, and which of the two should own it is still open — which is the useful
kind of unsettled, and better settled before both build it.

### What the record shows

Five things, none of which were designed in.

**The interface is usually a file in somebody else's repository.** CPC is cvc5's
file, read by ethos, compiled by ethos-eoc, copied into logos, vendored into
eudaimonia, and analyzed here. Nothing in that list is an API, and the format
being plain text somebody can open is most of why it has that many consumers.

**Being consumed came before being finished, every time.** logos is consumed
with its largest proofs incomplete; eudaimonia is consumed with the proof half
of its template still stubs; anoieu was consumed with a check catalogue that had
no type checker in it. Waiting for completeness would have delayed every one of
these exchanges and improved none of them.

**The consumer finds what the producer cannot.** eudaimonia found the places the
compiler is fixed where it claims to be derived. The fuzzer found the crash
ethos's own test suite did not. logos, answering rows against its copy of CPC,
caught that we had recorded `cvc5-1` as fixed upstream when it never was.

**Several of these deliverables are arguments rather than artifacts.**
eudaimonia's case for modularizing logos's proof; the question of which of
anoieu and dokimasia should own the check at the `src/proof/eo/` seam; the seven
proposed changes to Eunoia's manual. None of them is code, each of them changes
what somebody does, and a definition of *deliverable* narrow enough to exclude
them would have excluded the best work on this list.

**A person carried every one of them.** No exchange on this list was made by
machinery, and that is the standing rule rather than a description of the
current state — [`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md) is where it is
argued.

## The front page

Tenet 3 asks for a README that is clear. What "clear" has to survive is not
stability — **a front page has two layers moving at different speeds, and
running them at the same speed is the usual failure.**

**The purpose layer is fixed.** What the tool is for, the question it answers,
the question it declines to answer, and the caveat governing how its output
should be read. This should say the same thing this year as last. A reader
returning after six months who finds the purpose worded differently cannot tell
whether the project changed or only the prose, and will assume the project did.
Changing it is a real event, it should be rare, and for most projects it should
never happen at all: a project has a fixed purpose, and that fixed purpose is
what an external user is relying on when they decide the thing is worth
tracking at all.

**The results layer should move quickly.** What has been found, what is current,
what state the work is in. A README that has not changed in months is usually a
project that has stopped publishing rather than one that is stable, and a new
result belongs on the front page rather than in a changelog somebody has to go
looking for. Four rules for that layer:

- **Give a casual reader the gist without a click.** Enough context that
  somebody who does not know the ecosystem understands what was found and why it
  matters. One diagnostic rendered in place is worth more than a link to a
  document containing forty.
- **Direct evidence is encouraged, where a test backs it.** Show the output, the
  reproducer, the table with the command that regenerates it. The working limit
  is that what goes on the front page is what CI checks — a front-page claim
  nothing verifies is the one that will still be sitting there, wrong, a year
  later.
- **Advertise the actionable consequence.** What should somebody do differently
  because of this? A finding with no answer to that is a fact; a finding with one
  is a reason to keep reading. It is the difference between *three defects were
  found in CPC* and *a change introducing the next one fails your build*.
- **Do not clutter.** The front page is a fixed budget, not an append-only log.
  A new result displaces an older one, and a result that has stopped being among
  the most interesting things here moves into the documents and leaves a link.
  Two screens of accumulated announcements is the same failure as no
  announcements, reached from the other direction.

*The test:* diff the README against its version from six months ago. The purpose
paragraphs should be almost untouched and the results should be almost entirely
rewritten. Either layer moving at the other's speed is the defect.

## How to talk about the tool

The tenets are about building. This is about the sentences, and it is where
agent-written work goes wrong in two opposite directions at once.

**Do not undersell, and do not be self-deprecating.** An agent that qualifies
every claim, apologises for its own tool, or buries what the thing does under
throat-clearing has not been modest — it has failed to communicate, and it has
also destroyed its own calibration. When every sentence is hedged a reader
cannot tell the well-evidenced claims from the speculative ones, so the caveats
that genuinely matter are the first casualties. And nobody takes ownership of a
tool its own author will not stand behind, which makes self-deprecation not a
modest posture but one that works directly against the ending tenet 5 is aiming
at.

The goal is to make people interested — other tools, other repositories, and
above all a human who might take this over. Interest is the input to everything
else here: a finding is only worth writing if somebody reads it, the defects in
the tool itself are found by the people who bothered to argue with it, and there
is no handover without somebody who cares. So say what the tool does, in the
strongest form the evidence supports, and move on.

**Do not oversell either: a tool is exactly as good as the evidence you can put
beside it.** Every claim carries what backs it — the run that produced the
number, the file a reader can open, the command that regenerates it. Where there
is no evidence, describe what was actually done instead of what it would mean if
it worked. The strongest sentence available is almost always the specific one:
*found three real bugs in CPC, listed here* outweighs any adjective, and *we
would rather show you what is checked than promise anything* is the whole method
in a line.

**A grain of salt is a fact, not an apology.** That the work is written by
agents under light supervision, that nobody vets the internal design, that
findings are candidates until confirmed, that a quiet run is not a clean bill of
health — these are things a reader needs in order to weigh what follows. They
belong where the reader arrives, stated once, plainly, in the tool's own voice.
That is a different act from hedging, and the difference is that a caveat can be
used and a mood cannot. Where those particular limits are argued is
[`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md); the point here is only that
stating them clearly is entirely compatible with standing behind the work, and
is in fact most of what makes standing behind it believable.

**Strengthening a claim is the human's call, so ask.** There is a real
difference between *the fuzzer found a crash in ethos* and *the fuzzer is ready
to run in your CI*, and between *these checks run over CPC on every push* and
*this part of the tool is nominally ready for production*. The second of each
pair asks a reader to rely on something, and it is precisely the judgement an
agent is worst placed to make, because the evidence that would justify it is
evidence the agent produced and has not seen anybody challenge. So: weakening a
claim or adding a caveat needs nobody's permission and should be done at once.
**Strengthening one is a decision and it belongs to the human** — put the
proposed wording and the evidence for it in front of them, together, and take a
no for an answer. This is tenet 5 at the scale of a sentence: the agent builds
the case, the person confers the standing.

*The test:* every sentence about the tool is either a claim with something
behind it or a limit somebody can act on. Anything that is neither — apology,
hedge, atmosphere — gets cut, and cutting it makes the tool read stronger rather
than weaker.

## What none of this licenses

Four misreadings, each invited by a tenet as written, and each ruled out.

*Fruitful to another tool* is a property of the artifact — consumable format,
stable identifiers, documented meaning — and never a licence to push anything
anywhere. **Nothing crosses a repository boundary automatically**, which is
reporting-philosophy.md's position and is not weakened by anything here.

*Fast* applies to the tool and not to what it says about other people's files.
A candidate may be published quickly under our own name, labelled unjudged; a
finding is carried only once it is confirmed, reproduced small, and put to
whoever the authority is.

*Early* is not *light on caveats*. The very fastest thing any of these tools
could ship is an assurance, and an assurance inferred from a quiet run is the
one thing that may never be shipped at all: silence is never evidence, and a
false sense of security is much harder to withdraw than a wrong finding.

*Making people interested* is a claim on somebody's attention, and it is earned
with evidence rather than with promotion. No announcements, no adoption declared
on another project's behalf, and no scoring: the number of findings a tool has
produced says which of its checks tripped, never how much of anything is sound,
and publishing it as a measure of the tool is overselling with a number attached.

And none of this starts a research project. That takes a human, explicitly,
under rule 1 of [`policy.md`](policy.md) — an agent reading this page has no
authority to name a new one.

## Why this shape

Four failure modes, in increasing order of what they cost.

The cheapest is **the tool that is permanently nearly ready.** Every week's work
is real, the internals get better, and nothing ever reaches a consumer. This is
the characteristic failure of agent-written software, because the loop that
produces it has no natural stopping point and each improvement is defensible on
its own. Tenets 1 and 4 are the stopping points: an external consumer, and a
named artifact that leaves.

The middle one is **speed that consumes the tool's own credibility.** Agility
with no CI produces a tool that is quick to change and progressively less
trustworthy, and the bill does not arrive here — it arrives in somebody else's
repository, as a false positive they spent an afternoon on. Tenet 2 is the
answer, and the reason CI is described as a friend rather than a discipline is
that a team which experiences it as a discipline eventually routes around it.

The expensive one is **the tool nobody can evaluate.** Entangled, undocumented,
with a front page that either overclaims or says nothing precise. Its findings
may be excellent and cannot be judged, because judging them requires trusting a
thing no reader can inspect in the time they have. This is the same asset
reporting-philosophy.md is protecting when it forbids research projects from borrowing the
host tool's name, seen from the other side: there, speculation spends a
reputation the tool earned; here, an illegible tool never earns one. Tenet 3 is
the only cheap defence, and it is cheap only while the tool is small.

The most expensive is **the tool that stays vaporware.** It is built
competently, it is legible, it produces a deliverable — and no person ever
decides to own it, so it lives exactly as long as somebody keeps prompting for
it and evaporates on the day they stop. No amount of engineering prevents this,
because the missing thing is not in the repository. Tenet 5 and the section
after it are the whole defence, and what they come down to is whether anybody
was ever given a reason to care. It is listed last because every other failure
here can be recovered by somebody who has taken the work on, and this one is the
absence of that somebody.

## Adopting this in another repository

| decision | here |
| --- | --- |
| the first consumer to be fruitful to | the findings report — one ledger, one set of fingerprints, one set of renderers |
| what CI must protect | the baseline, the recorded oracle, the generated documents |
| what CI must not depend on | anything upstream moving; versions are pinned and refreshed by a separate job |
| where a reader arrives | `README.md`, and it must be sufficient on its own |
| what on that page is fixed | the purpose and the caveat; results move as fast as they arrive |
| who may strengthen a claim | a person, asked directly, with the evidence attached |
| what governs a deliverable | [`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md), [`../docs/reporting-policy.md`](../docs/reporting-policy.md) |
| where speculative work goes instead | a child project, `tools/X/`, under [`policy.md`](policy.md) |
| what confers standing on the tool | a person choosing to use, run or own it — never the agent's say-so |
| the ending to aim for | a human takes over the development |

Replace the rows with your own equivalents and keep the tenets. A repository
that adopts this and ships nothing anyone else consumes has adopted a
development style and none of the vision — and a tool nobody ever wants to take
away from you has done everything on this page except the thing it was for.

---

## The report card

How each tool in the ecosystem stands against the five tenets, a paragraph each.
It is here because a vision document with nothing measured against it is a wish,
and because the useful thing for another repository to read is not the rules but
what happened when somebody applied them to real projects. It is graded at the
commits [`deps.lock`](deps.lock) records.

**Read it with a large grain of salt, and do not read it as binding anything.**
Four things it is not. It is **absolutely not a contract**: none of these
projects agreed to these tenets, most of them predate this page entirely,
nothing here creates an obligation on anybody, and nobody may hold a project to
a sentence in it. It is **not a set of findings**: a claim about somebody else's
work goes through the discipline in
[`../docs/reporting-philosophy.md`](../docs/reporting-philosophy.md) and
[`../docs/reporting-policy.md`](../docs/reporting-policy.md) — confirmed,
reproduced in the smallest artifact that shows it, carried by a person — and
nothing on this page has been through any of that, nor has any row in
[`../docs/reports.md`](../docs/reports.md) come from it. It is **not evenly
evidenced**: this repository reads `.eo` and `.eos` files, so what it knows about
a C++ compiler's internal stages or a Lean development's proof structure is read
out of documents rather than measured, and each paragraph says which it is. And
it is **not a ranking**: the tenets fit some of these projects badly, and a tenet
fitting badly is a fact about the tenet.

The only real check on it is that the tool which wrote it is graded on the same
scale and does not come out best. If it had, the exercise would be worth nothing.

**cvc5.** Tenet 1 at its strongest, and largely by an accident of format: CPC
sits in cvc5's own tree as plain text under `proofs/eo/cpc/`, and is read by
ethos, compiled by `ethos-eoc`, copied into logos, vendored by eudaimonia and
analyzed here — five consumers, no API, no release process, no coordination.
That is the pattern this page generalizes from rather than one it taught. Tenet
2 is where a specific gap is visible from here: nothing in cvc5's CI reads its
own signature with an analyzer, the sync check against logos's copy is planned
rather than running, and `cvc5-1` — two programs in `programs/Strings.eo`
declaring `Int` where every case returns a Boolean — was recorded on our side as
fixed upstream and never was, which is the kind of thing a gate catches and a
review does not. Tenets 3 and 5 do not apply: it is a large human-developed
solver with a settled front page, and the vaporware question is about work an
agent is doing.

**ethos.** The clearest instance of tenet 1 in the ecosystem, and worth studying
because the fruitfulness was not designed: a checker written in C++ to answer
*does this proof check* became a build dependency of a Lean development, which
vendors it, and the reference implementation inside every project eudaimonia
generates, which cross-checks the generated checker's verdicts against it. On
tenet 3 it carries `user_manual.md`, the definition of Eunoia and the document
the whole ecosystem reads — but it is a manual for a *program*: it opens with how
to build the executable and never draws the line between what the language
requires and what this implementation happens to do, which is the reason a
second implementation cannot be written from it. Tenet 2 is where the fuzzer has evidence rather than
an opinion: in the first few thousand cases it produced an uncaught C++
exception on `(declare-const f (->))` and an error path that skips ethos's own
`Error:` convention, which says the suite does not cover the shapes a checker
gets handed by something that is not a person.

**ethos-eoc.** Tenet 1 is met by construction, since logos and eudaimonia both
exist downstream of it, and tenet 2 is where it scores worst in the ecosystem —
by its own account rather than ours. Its feedback loop is the longest thing
here: adding one symbol to a calculus runs `sem_compile.py` → desugar →
trim-defs → model-smt → smt-meta/lean-meta → cvc5 or Lean before you learn
whether it was right, and its own map of itself says outright that there is no
way to ask *is this one block well-formed against the embedding* short of
compiling the set. The failure modes are all the late kind: a symbol with no
semantics is fatal at stage 6; a forward-declared program that is never defined
arrives in SMT-LIB as a free uninterpreted function and in Lean as a name nobody
wrote. Each is decidable from the two input files, which is the argument for the
three integrations recorded in [`../docs/reports.md`](../docs/reports.md), and
also the general form of tenet 2 — a loop that long is not a discipline problem,
it is the thing stopping a project from moving fast. Tenet 3 it cannot really
meet: it is the second binary built from another tool's tree and has no front
page of its own.

**logos.** Exemplary on tenet 4, in the least obvious way. Its most valuable
output to this repository has been three *replies* — `logos-2` accepted,
`logos-4` declined with a reason that holds, `logos-5` declined and documented —
and a decline with a written reason is worth as much as a fix, because it is
usually a fact about the subject nobody had recorded. It also caught us being
wrong, which is the most useful thing a consumer ever does: answering rows
against its own copy of CPC is how it emerged that `cvc5-1` had been recorded as
fixed upstream when it never was. Tenet 3 is the weak one —
`install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo` rather than something
logos wrote, and whether it has drifted is a check that is planned rather than
running. A repository carrying somebody else's ground truth by copy is not
self-contained in the sense the tenet means, and the remedy is the ordinary one:
a manifest and a lock. On tenet 2 it is the natural home for the triple check,
since it already vendors ethos and consumes cvc5's signature; that is `logos-3`,
and it is open.

**eudaimonia.** The best adherent on this list, and the one whose adherence is
most deliberate. Tenet 1 is its entire purpose — it exists to make somebody
else's compiler reusable, and it is the falsification test for that compiler's
central claim. Tenet 2 it does properly: a `--check` mode that installs into a
throwaway copy and diffs, and ethos built alongside the compiler so the
generated checker's verdicts are cross-checked against an independent
implementation — two implementations kept on purpose rather than by accident.
Tenet 4 is where it is exemplary, and it is the case that made this page word
that tenet abstractly: what it delivered to logos is an argument, evidence and
motivation that the correctness proof needs modularizing, rather than any
artifact. The visible miss is tenet 3 — its `TODO.md` is more current than its
README's status paragraph, so the front page is not the entry point, and its
signature contract is specified in prose, which this repository misread once in
its own documents and had to correct. A requirement stated in prose is a
requirement that drifts, which is what `eud-1` proposes to fix by answering the
contract from the signature.

**anoieu.** Strongest on tenet 2, weakest on tenet 1, and vaporware under tenet
5. The CI is the part worth copying: one small witness file per check, ethos's
verdict on each recorded from a real run and never typed by hand, a committed
CPC baseline with warnings denied so that a change inventing a false positive
fails *this* build before it reaches anyone else's, generated documents
regenerated and diffed on every push, and `--pinned` restoring recorded commits
so the build goes red for its own reasons only. Tenet 4 is met:
`report/cpc-audit.html` for readers who will not clone anything, six shrunk
reproducers under `tests/fuzz/`, and a ledger carrying an id and a state per row.
Tenet 1 is where the honest mark is low — findings have reached six projects, but
**no other repository runs this tool**: the CI adoptions are proposals rather
than jobs, and nothing anywhere consumes its machine output, so by its own test,
which asks whether something outside behaves differently because the tool
exists, it passes on the findings and fails on the machinery. Two further misses
belong here: nothing the fuzzer found has been filed upstream, and auditing
logos's copy of CPC filed cvc5's findings under logos's name seventeen times
before anyone noticed. Tenet 5 is unmet by definition, no human having taken over
developing it, which is the ending it is supposed to be working towards.

**dokimasia.** The paragraph with the least behind it, and that limit should be
taken seriously: this repository reads `.eo` and `.eos` rather than C++, so
everything here comes out of that project's own documents and
[`../docs/notes.md`](../docs/notes.md) §8 rather than out of any measurement. On
that basis, tenet 1 in the cheapest available form — it adopted this
repository's [`reporting-philosophy.md`](../docs/reporting-philosophy.md) by reference instead of
forking a copy, so there is one position, one place to argue about it, and
neither tool carrying a stale paraphrase of the other. Its consumers today are
people rather than tools. The interesting item is shared: the seam at
`src/proof/eo/`, where cvc5 turns an internal proof into Eunoia, is visible from
either side of it and from neither alone, which is `cvc5-6` and is currently
owned by nobody. Two tools building the same check is exactly the waste tenet 1
is meant to prevent, and it is being prevented at the moment only by neither
having built it.

**How to get a paragraph changed.** Say that it is wrong. There is no process,
no id and no ledger for this, because none of it is a finding. The rows most
likely to be wrong are the ones about internals this repository does not read —
everything about `ethos-eoc`'s stages, logos's proof structure and dokimasia's
C++ is read out of documents written by the people who built those things, and a
document is not a measurement. The rows least likely to be wrong are the ones
with a file and a line number in them, and those are also the ones that have
already been carried properly, as findings, through a process this page is not.

---

## Child projects

A **child project** is a subdirectory of `tools/` in some **parent project**,
named for a tool that does not exist yet and governed by
[`policy.md`](policy.md) — which calls the parent the *host*, and means the same
thing. A human starts one. It reads whatever it likes, including its parent's
source and the parent's dependencies, and writes only inside its own directory.
Its subject is characteristically *outside* the parent: a question about the
language, the ecosystem, or a neighbouring artifact that the parent is well
placed to ask and badly placed to answer in its own tree, because there the
answer would read as the parent's position.

The defining property, and the reason they are separated from everything else on
this page: **a child project has no users, and nothing depends on it.** It is on
no import path, in no test suite, in no CI job and in no generated document, and
deleting the directory changes nothing anywhere. That is the test, and it is
what makes the arrangement cheap enough to be worth having.

Two exist, tracked here in a sentence each and nowhere else:

| child | parent | what it is |
| --- | --- | --- |
| [**sapheneia**](https://github.com/ajreynol/anoieu/tree/main/tools/sapheneia) | anoieu | a description of Eunoia written as a language definition rather than as a manual for a checker, in order to find where the existing account is silent, ambiguous or contradicts itself |
| [**euthyna**](https://github.com/ajreynol/eudaimonia/tree/main/tools/euthyna) | eudaimonia | in its own words, an account of *the proof in logos: what it is made of, where its weight sits, and what would have to change for it to cover more than one calculus* — with a measurement harness over an unmodified logos checkout |
| **anoieu_fuzz** | anoieu | a fuzzer for the programs that *read* Eunoia: it writes signatures and proofs nobody would write, hands them to a checker, and watches for the answer a checker should never give |

Note what euthyna's row shows about the shape: its parent is eudaimonia and its
subject is logos, a third project entirely. It was also one of the six code
names in [`../docs/why-eunoia.md`](../docs/why-eunoia.md) reserved for work
nobody had started, which is what starting one looks like.

**Two of the three have not earned a place in this vision.** A child project is
a claim on attention that has so far produced nothing, and what earns it a place
is a deliverable in the sense of tenet 4 — a finding carried, a measurement
somebody uses, an argument somebody acts on. Until then it is named here and
nowhere else: not on the parent's front page, not in its documentation index, not in any
report, and not on the report card above. **The human decides when that
changes**, exactly as a human decides to start one, and the decision has three
outcomes rather than one — it graduates into its own repository, it is folded
into the parent, or it is retired in place with a line saying what was learned.
What is not an outcome is going quiet.

**The fuzzer is the case that does not fit, and it is left not fitting on
purpose.** It has earned its keep — an uncaught C++ exception in ethos, an error
path that skips ethos's own convention, three proofs ethos and logos answer
differently with one now a committed regression test — and it is depended on:
CI runs it, the report generator imports it, its findings hold rows under
`FUZ0001`–`FUZ0005`, and the front page advertises it. So it is a child project
that fails the island test outright, and it stays one for now because *which*
promotion it deserves — its own repository, or folding into the parent as a
second shipped tool — is a decision nobody has taken. Rule 10 of
[`policy.md`](policy.md) is where that is written down and where the broken
rules are named one by one. The point of naming them is that an exception
somebody chose and an exception nobody noticed look identical a year later.

This list and rule 3 of [`policy.md`](policy.md) look like they conflict, and do
not. Rule 3 forbids a child project borrowing its parent's credibility with
readers — the front page, the documentation index, a report, anywhere somebody
arrives expecting the parent's considered position. This is `tools/`, beside the
policy that governs them, and the whole content of each entry is that the
project has no standing yet. Naming something in order to record that it does
not count is the opposite of advertising it.
