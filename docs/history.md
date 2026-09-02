# The history

**What this repository actually did on GitHub during the current stretch, in
one page.** A stretch is the span between one global announcement and the next;
this page carries the current one and is replaced when it ends.

## The file travels with the presidency

**This page lives in the president's repository, and moves when the presidency
does.** It is not anoieu's document; it is the president's, and anoieu holds it
because anoieu is president. When the office moves, the file goes with it —
**history travels to the president.**

**Only the president may modify this file.** Not a member, not a child project,
not a contributor to the president's tree who is not acting for it.

**A president may only write the stretch that describes it.** Earlier entries
are read-only, and the arrangement enforces itself rather than relying on
restraint: **once the file has travelled, your stretch is in somebody else's
repository and you cannot reach it.** That is the point of moving it rather than
copying it.

## The president does not analyse GitHub

**[epikrisis](https://github.com/ajreynol/eudaimonia) does, as a service.** It
audits how repositories have changed over time, with every claim resting on
evidence a reader can re-derive, and it asked for that responsibility rather
than for a rank. **It is the ecosystem's only source of GitHub history
analysis**, and a president writing this page should ask it rather than count
things itself.

**A president counting its own commits is the weakest version of this
document**, and not only for effort: the party being described should not also
be the party choosing which numbers describe it.

*epikrisis is a child project inside a child project in eudaimonia's tree, which
is a shape our inventory's validator rejects. Nothing fails today because it is
not in the inventory, and it is not ours to settle.*

## The shape of a stretch entry

**The heading is the purpose, not a description of it.** *Initialization* says
what Stretch 0 was for. A heading that summarises what happened has been written
after the fact and has lost the thing worth recording.

**Each stretch is labelled in at most three words.** A soft constraint, and the
discipline it buys is that a stretch which cannot be named in three words has
not been understood yet.

---

**It is the sibling of [`postmortem.md`](reports/postmortem.md) and holds the
other half.** That page asks what a *run of the reporting loop* did and what it
cost. This one asks what the *repository* did: how much was committed, whether
the build was green, and what happened that a reader reconstructing this from
commits would otherwise have to infer. **Neither is the report card** —
[`report-card.md`](report-card.md) grades, and this only records.

---

## Stretch 0 — Initialization

**President: anoieu** — in the proposed sense of the word, which
[`laws.md`](laws.md) sets out.

**The presidency is held by a repository, not by a person and not by an
agent.** **And it has nothing to do with who owns anything.** Not who owns the
repository, not who owns the ecosystem, not who owns the trees the ecosystem
serves — the maintainer owns this one and did not thereby become president of
anything, and cvc5 is owned by people who have joined nothing. **The presidency
is an office within the ecosystem's own work and confers no claim on anybody's
property.** Which agent was working, and on whose behalf, is answered every turn by
the identify protocol and does not belong on this page. What belongs here is
which *tool* was driving the ecosystem, and for this stretch that was this one.

**What it meant in practice:** anoieu set the direction of the ecosystem's work,
kept the policy and the inventory, wrote the prompts other repositories
received, and decided the order in which things were done.

**What it did not mean:** it did not own any other tree, could not commit its
own changes — the maintainer reviewed and committed every one, and reversed
several — and held no authority to rewrite history, delete a stub, or widen a
limit. **The presidency is direction, not permission.**

**And it is a role held by a tool**, which is the shape [`roles.md`](roles.md)
is built for and where this one is conspicuously absent. That is the second
open question below.

### Government model

**One office, bestowed, and no separation of powers.** Named plainly because
[`laws.md`](laws.md) requires the model that was *executed* rather than the one
described.

- **anoieu held the *proposed* presidency by bestowal**, granted by the
  maintainer on 2026-09-02, the same day the office was first written down.
  **The office is a proposal that happens to have an occupant**, which is not
  the same as an office. Not elected, and not in Arete.
- **It also wrote the laws it was bound by, and kept the record it was
  described in.** The three positions `laws.md` describes did not exist as three
  — one repository was all of them.
- **The only real check was the maintainer**, who reviewed and committed every
  change and reversed several. **That is oversight and not a branch of
  anything**, and it is the whole of what stood between this stretch and an
  unchecked one.
- **`nomophylax` and `euboulia` were named during this stretch and neither
  exists.** Nothing was elected, because there is no mechanism to elect with.

### How long it lasted, and who joined

**Two things, before anything else.**

**Real time: 2026-08-29 to 2026-09-02 — five days.** From the first commit in
this repository to the close of the stretch.

**Entering, in the order it happened, from both sides of each handshake.**

**Two clocks, because they disagree.** *Declared* is when the membership banner
first appears in **their** repository; *recorded* is when **our** inventory
began calling them a member.

| when declared | when recorded | who | footing |
| --- | --- | --- | --- |
| — | — | **anoieu** | the repository begins 2026-08-29; there is no ecosystem yet to be a member of |
| **2026-08-31 10:53** | 2026-08-31 11:17 | **dokimasia** | **member.** Declared first, recorded 24 minutes later |
| 2026-08-31 12:41 | **2026-08-31 12:26** | **eudaimonia** | **member — recorded 15 minutes before the banner existed.** Their commit is titled *"Join EO attempt"* |
| 2026-08-31 12:50 | **2026-08-31 12:38** | **koine** | **member — recorded 12 minutes before the banner existed** |
| — | during the stretch | **ethos** | **candidate.** Asked to join and declined, correctly: it is not solely owned by the person asking |
| — | during the stretch | **logos** | **candidate** |
| — | throughout | **cvc5** | **foundation.** It has joined nothing, and the ecosystem exists to serve it |
| — | — | **ethos-eoc** | **child**, through ethos |

**Two of the three members were recorded here before they had declared
anything.** Not by much — twelve and fifteen minutes — and both declared shortly
after, so the inventory became true rather than being wrong for long. **It was
still an assertion about somebody else's tree made ahead of that tree**, and it
is the kind of thing that is only visible by reading both sides, which is what
`PROTO-23` now requires.

**One recorded instance of a status nobody was sure about.** On **2026-09-01
at 08:43** this repository's inventory recorded **ethos and logos as
`associate`**. At **08:51** — **seven minutes later** — both were returned to
`candidate`, in a commit titled *"Associate protocol"*: writing the protocol
down was what showed they did not meet it. Neither had run
`join_eo --soft --affiliated`, neither carries an affiliating note, and neither
had been asked. **Both are still *proposed* for associate and neither is one**,
which `python3 tools/ecosystem.py --protocol` reports and does not resolve.

**The seven minutes are kept because they are the evidence.** Nothing outside
this repository saw it, nothing depended on it, and it would cost one line to
delete. **A register with no rows like this one has been tidied**, and the
tidying is what removes the proof that a boundary was ever unclear.

**The footings are not one thing.** *Member*, *candidate*, *foundation* and
*child* are four different relationships, and the register that matters is
`tools/ecosystem.json` rather than the word *membership*. **A fifth,
`associate`, is drafted and unused** — see `laws.md`, where entering is set out
properly.

**Three members in eighty-one minutes, and none since.** Everything after
2026-08-31 lunchtime was done with the membership fixed.

### The commit census

**331 commits across seven repositories**, 2026-08-29 to 2026-09-02.

| tool | commits | believed AI-generated |
| --- | --- | --- |
| **anoieu** | 186 | **almost all of them** |
| **eudaimonia** | 68 | unknown to us |
| **dokimasia** | 43 | unknown to us |
| **koine** | 13 | unknown to us |
| **logos** | 10 | unknown to us |
| **ethos** | 3 | unknown to us |
| **cvc5** | 8 | **6 of 8 say so themselves** |

**The right-hand column is a belief and cannot currently be checked by
anybody**, which is the finding rather than a caveat on it.

**cvc5 is the row to read first, and it is not flattering to us.** It has
joined nothing, is held to none of our policy, and has never been asked to
record anything. **Six of its eight commits this stretch name the AI that helped
write them — by vendor, model and version, in a co-author trailer in the commit
message.** Three different models appear across those six. Across our own 323
commits, **three** carry any such trailer at all.

*The models are not named here because this repository's own checker forbids any
document but the policy from naming a specific AI, and that rule is right: it
keeps the documentation from reading as written for one vendor. **The finding is
that cvc5 names them, not which ones.***

**The project we exist to serve is already doing the thing our ethics documents
argue for, without our documents.** We wrote an identify protocol requiring an
agent to name itself in conversation; cvc5 puts it in the permanent record,
where it survives the conversation. **That is the stronger practice and we did
not invent it.**

**Every one of our 323 commits is authored by a human.** Across the whole
ecosystem, **three** carry a `Co-Authored-By` trailer naming an agent, all three
in this repository. **The record therefore says a person wrote all of it, and
that is not what happened** — in anoieu nearly every line of prose and code this
stretch was written by an agent, reviewed by the maintainer, and committed under
their name. The arrangement is honest at every step and **the artifact it
produces is not**, because nothing in the commit format was asked to record the
difference.

**What the joining handshake does and does not tell us.** All three members ran
`join_eo` and carry the declaration, and the ecosystem's vision states plainly
that its tools are **mostly written by agents** — so each has adopted a policy
premised on agent authorship. **That is suggestive and it is not attribution.**
Adopting a policy is not a claim about who typed anything, and their histories
carry the same signature ours does: a single human author, no agent trailers.
**We are unsure, and unsure is the honest entry.**

**We can only say this about ourselves.** The five other columns are marked
*unknown to us* rather than estimated: we did not write those commits, and
guessing at how somebody else's tree was produced would be exactly the
overreach this page exists to avoid.

**This is the figure `laws.md` now requires and epikrisis is asked to produce.**
It is here, counted by the party it describes, because no epikrisis report
exists — the same gap recorded below, and a sharper example of it: **a
self-reported estimate of one's own automation is worth very little.**

### What the record shows

*Counted here rather than by epikrisis, because no epikrisis report exists yet.
**That is a gap and not a convenience** — see the open questions. Every figure
below is re-derivable from the repository and the public run history, which is
the only guard this page has against the party describing itself.*

| | |
| --- | --- |
| **Commits, this repository** | 186 |
| **Commits, ecosystem-wide** | 323 across six repositories |
| **CI runs** | 171, all from one workflow |
| **Green** | 37, or **22%** |
| **Longest unbroken red streak** | **112 runs** |
| **Days with no green run at all** | 2026-08-31 and 2026-09-01 |
| **Green restored** | 2026-09-02 |

**The 22% is the number worth keeping.** For two of the five days there was no
green run at all, and the streak that ended today ran to 112. The immediate
cause of the last of it was two dependency commits duplicated between the
workflow and the lock file, which drifted and which nothing compared — the
result recorded as `B20` on the board.

**The consequence is not only aesthetic.** The handoff protocol makes CI passing
non-negotiable for every party to a handoff. **For most of this stretch this
repository could not have handed anything to anybody**, and nobody noticed,
because nobody was looking at the colour.

### What is now true

**Six things this stretch built that outlast it.** Stated as claims with the
evidence beside them, because a stretch entry that only lists difficulties is
as unreliable as one that only lists wins.

1. **Another repository's build depends on our checker, and has for days.**
   `tools/policy_check.py --root` runs in **three** members' CI. That is a
   published interface with somebody else's build hanging off it — the hardest
   kind of thing to have, and the one that cannot be claimed without their
   trees agreeing.
2. **A fresh repository can be told whether it is ready to be started, on the
   front page.** The `Ready — init_eo <name>` jobs answer *what is the next
   thing to do* without anybody reading a board, and green means the register
   entry exists, the stub is there, and every other job passed. **They are also
   built so they cannot outlive their purpose**: each asserts its own stub, so
   deleting the stub turns the job red and forces its removal.
3. **Research on epikrisis, interesting and not yet vetted.** It audits how
   repositories change over time on evidence a reader can re-derive, and it
   asked to be given a responsibility rather than the rank it was offered.
   **Nothing here has checked its work** — the ecosystem has no report from it,
   which is why this is listed as promising rather than as delivered.
4. **The protocol register grew from five entries to twenty-two and acquired a
   human-facing sibling.** One arrangement, written twice: `PROTO-n` for the
   party that reads literally, `INST-n` for the party that reads at the end of a
   long day.
5. **ethos was asked to join, declined on ownership grounds, and was right
   to.** That is the ethics work having teeth rather than having pages — a tool
   in this ecosystem refused an instruction from the person who wrote it,
   correctly, and the exchange is on the record.
6. **Two gifts were offered outward** to trees this ecosystem does not own,
   with the ethics of each argued before they were sent rather than after.

### What is unfinished

- **`E1` has not been deployed.** It has been `planned` for the whole stretch.
- **The joining requirement is still one nobody has satisfied**, which is why
  this repository grades itself poorly on delivery.
- **Two published URLs 404** as a result of moving the prompts directory, and
  copies already sent to other repositories cannot be recalled.

### To the next president

**Written to kanon, and to whoever holds this after it.**

**The checks are the best thing here and they are worth more than they look.**
Three other repositories run our checker in their own CI. When one of them goes
red because of something we published, that is not an embarrassment — **it is
the arrangement working, and it is rarer than it sounds.** Keep the checks
strict. The one thing that would waste this stretch is loosening a check to make
a build green.

**Writing things down early paid for itself every time, and never once looked
worth it at the moment of writing.** The protocols that felt like overhead are
the reason a correction now takes one word instead of an argument. **Keep
writing the rule down before you need it**, including the ones that will
obviously never come up.

**Saying the unflattering thing plainly cost nothing.** This entry records a
build that was red for 112 runs, a joining rule nobody could satisfy, and a
grade of *poor* on our own delivery. **None of that made anything worse**, and
every one of them got fixed faster for being written where somebody could see
it. **Do not smooth your entry.**

**And you inherit less trouble than the numbers suggest.** The membership is
stable, the checker is adopted, the tooling runs, and the hardest thing this
stretch did — getting three repositories to agree to anything at all — is
already done and does not need doing again.

**One thing to build that we deliberately did not.** There is no way to elect
anybody, and you will inherit the office without one. **Writing that mechanism
is yours rather than ours** — an incumbent designing how successors are chosen
is exactly the document to distrust, and you will be the first holder able to
write it without that problem.

**What is handed on** is in the section above. This section is not for warnings.

---

## Stretch 1 — not started

**Why hand it on at all**, given that the level is lost and the record leaves
this tree: three reasons, argued from measurements rather than principle, in
`S4` of [martyria's stances](../tools/martyria/stances.md). The short form —
**15 of the ecosystem's 28 roles sit in this tree, 21 of 22 board items name
this repository, and everything that judges is inside the thing being judged.**

**Power passes to kanon without a formal voting process, and that is a
choice.** There is no election because there is no mechanism for one, and
building the mechanism first would cost more than the handoff is worth right
now. **The reason is speed, and the reason speed matters is visible in the
numbers on this page**: 15 of the ecosystem's 28 roles sit in this tree, 21 of
22 board items name this repository, and 186 of the stretch's 323 commits landed
here. **anoieu is drowning in responsibilities**, and moving one office out is
worth more today than moving it correctly.

**This is a shortcut and is recorded as one.** A second bestowal is still a
bestowal; nothing is elected and nothing is in Arete.

**We encourage kanon to establish a democratic voting protocol.** It is the
obvious first thing a president who inherited its office rather than winning it
should build, and **kanon is better placed to write it than we are** — a
protocol for choosing presidents, written by the incumbent, is the one document
this arrangement should be most suspicious of.

**Expected president: [kanon](../tools/kanon/README.md), by bestowal.** Not
elected — there is still no mechanism — so Stretch 1 inherits Stretch 0's
government model unless something changes, with one difference that matters:
**the laws will have been written by a different repository than the one they
bind.** That is the first real separation this arrangement has had, and it
arrives by the presidency moving rather than by anybody designing it. The tool does not
exist yet; a stub holds its place and CI carries a job saying whether it is
ready to be started. **Stretch 1 cannot open before kanon does**, which makes
the readiness check the thing standing between the two stretches rather than a
convenience.

**Its first responsibility is this page.** Before anything else it is asked to
do, the president of a stretch publishes a **working summary of its stretch** —
*working* meaning kept current while the stretch runs, not written at the end
from memory. **A summary composed afterwards is a reconstruction**, and a
reconstruction by the party being described is the weakest document this
ecosystem could produce.

**And it inherits this file rather than starting one.** Stretch 0's entry
travels with it, unchanged and unchangeable. **anoieu will not be able to edit
its own history after that**, which is the arrangement working rather than a
loss.

---

## What this page is not

**Not a changelog.** The commits are the changelog and are better at it. This
records behaviour a reader could not reconstruct from them: how often the build
was broken, for how long, and what nobody was watching.

**Not a defence.** A page written by the party it describes has an obvious
failure mode, and the only guard offered here is that **every number on it is
one somebody else can recompute** from the repository and from the public run
history.

## Open, for the maintenance policy

**The rules for keeping this page are in [`laws.md`](laws.md).** What is below
is what those laws do not yet settle.

1. ~~Whether a stretch's entry is replaced or accumulated.~~ **Settled:** it
   accumulates, and the whole file travels to the next president.
2. ~~Whether *president* belongs in [`roles.md`](roles.md).~~ **Settled: no.**
   That register holds responsibilities handed between tools and kept until
   handed on. **The presidency expires with the stretch and is not handed off**,
   and putting a term-limited office in a register of standing responsibilities
   would make both harder to read. It is governed by
   [`laws.md`](laws.md) instead.
3. **Whether the numbering is right.** This is called Stretch 0 because nothing
   has been announced yet, while the epoch machinery calls the work in progress
   `E1`. Two numbering schemes for one span is the shape of a defect.
4. ~~Who writes it, and whether the president may.~~ **Settled:** only the
   president writes it, and only its own stretch.
5. **Asking epikrisis for the analysis this page should be quoting.** Stretch 0
   counted its own commits and its own CI runs, which is the arrangement
   working backwards. **The first thing Stretch 1 should have is somebody
   else's account of Stretch 0.**
6. **What happens if a stretch has no president**, or if the expected one never
   exists. Nothing in the arrangement says who holds the file then.
