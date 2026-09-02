# The history

**What previous presidents did, and what the current one is doing.** One
section per stretch, oldest first, and nothing else.

**No procedure lives here.** How this file is kept — who may write it, what a
stretch entry must contain, where it goes when the office changes hands — is in
[`laws.md`](laws.md). **This page is the record; that page is the rules**, and
the two were tangled together until 2026-09-02.

---

## Stretch 0 — Before anoieu

**President: none.** There was no ecosystem to preside over, and this entry
exists because two things happened before anoieu's first commit that everything
since has been built on top of. **It is written by Stretch 1's president, from
the outside, and is the one entry nobody held office for.**

**Span:** everything up to 2026-08-29.

### The two events that were already true

**cvc5 gated safe mode in its own CI — 2025-05-09, `#11869`.** A build
configuration named `safe-mode` became a job that has to pass, which means
**cvc5 already had a mechanism for saying *this narrower thing must keep
working***, more than a year before this ecosystem existed. Much of what has
been built since is a way of asking questions about that boundary.
[dokimasia](https://github.com/ajreynol/dokimasia) is the tool with something to
say here and says it at length: safe mode **names a configuration rather than a
set of code**, and what it actually protects is not enumerable today. **Ask it
rather than us.**

**logos offered cvc5 a CI check — 2026-08-26,
[`cvc5#12891`](https://github.com/cvc5/cvc5/pull/12891).** *Add Logos checker
download and CI check.* **Arguably the most significant single event in this
history so far**, and it happened three days before anoieu existed.

It is the whole argument working end to end, once, in public: a proof
development produces a checker, the checker is offered to the project it serves,
and **the offer is made as a gift with nothing asked in return** — no
membership, no policy, no attribution, no request that cvc5 adopt anything. If
this ecosystem is ever worth something, that is the shape it will be worth
something in.

**It is still open.** Created 2026-08-26 and unmerged at the close of Stretch 1,
which is the honest state of it: **the most significant thing here has not yet
been accepted by the people it was offered to**, and that is their decision and
not a delay.

### The commit census

**15,822 commits across four repositories, everything up to 2026-08-29.**

| tool | commits | first commit | authors | agent-attributed |
| --- | --- | --- | --- | --- |
| **cvc5** | 14,064 | 2009-09-26 | 123 | **70** |
| **ethos** | 1,055 | 2023-07-18 | 10 | **9** |
| **logos** | 699 | 2026-03-03 | 4 | 0 |
| **eudaimonia** | 4 | 2026-08-29 | 1 | 0 |

**Seventeen years, four repositories, and more than 130 people.** Stretch 1, by
comparison, is 331 commits over five days.

**The agent column is a count of commits carrying a co-author trailer that names
an agent**, which is the only signal that exists and is a weak one — see the
research question posed to epikrisis in `D21`'s neighbour. **cvc5's first is
dated 2026-03-14**, so agent-assisted work was going on in the project this
ecosystem serves for five months before the ecosystem existed, and was being
recorded in the permanent record while it happened.

**dokimasia and koine are absent because they did not exist**, and that is the
table's job: it says what was here, not who is here now.

**This table is expected to grow, and law 13 says how.** A tool that was around
before 2026-08-29 and joins later may have its row inserted retroactively, by
whoever is president then, with the date it was added. **Those are facts that
were always true and the table did not know them** — the four rows above are
what we happened to be looking at, not a claim about what existed.

### Why this entry exists at all

**Because a history that begins when we started reads as though nothing came
before**, and two of the three most consequential things in it predate us. **The
ecosystem did not create the conditions it operates in.** cvc5's CI, its safe
mode, its maintainers' judgement and logos's proof development were all there
first.

---

## Stretch 1 — Initialization

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

| declared | we recorded | who | footing |
| --- | --- | --- | --- |
| — | — | **anoieu** | the repository begins 2026-08-29; there is no ecosystem yet to be a member of |
| **10:53** | 16:44 | **dokimasia** | **member.** First to declare, by an hour and a half |
| **12:41** | 16:44 | **eudaimonia** | **member.** Their commit is titled *"Join EO attempt"* |
| **12:50** | 16:44 | **koine** | **member** |
| — | during the stretch | **ethos** | **candidate.** Asked to join and declined, correctly: it is not solely owned by the person asking |
| — | during the stretch | **logos** | **candidate** |
| — | throughout | **cvc5** | **foundation.** It has joined nothing, and the ecosystem exists to serve it |
| — | — | **ethos-eoc** | **child**, through ethos |

*All times 2026-08-31.*

**Every member declared before we recorded it, and all three were recorded in a
single commit at 16:44** — between three and four hours after each banner landed.
**That is batching rather than a defect**: the trees were right and our register
caught up in one go.

**A correction, because this table said the opposite for several hours.** An
earlier version of this entry claimed eudaimonia and koine were **recorded as
members before their banners existed**, by fifteen and twelve minutes. **That was
wrong, and wrong in the direction that flattered nobody.** It came from reading
the inventory's `joined` field — which records a commit of ours associated with
each join — as the moment we recorded membership. It is not: the status field
did not change to `member` until `a3ca74a`, and tracing that field commit by
commit is what showed it. **The claim is corrected rather than deleted**, and
the method that produced it is named so the same mistake is visible next time.

**The footings are not one thing.****The footings are not one thing.** *Member*, *candidate*, *foundation* and
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

### The joke

**Required by law 12 to live on the president's front page, and anoieu's was
there before the law was.** [`README.md`](../README.md), under *The name*:

> **Eunoia** is *Eu·noi·a*. Read its syllables backwards and you get *a·noi·eu*,
> which is spelled **anoieu** and pronounced **"annoy you"**.

**It passes the test the law asks of it: the joke doubles as the description.**
A tool whose whole job is to annoy you now, in your editor, about the thing that
would otherwise annoy you in an hour. **A stranger who reads only the joke knows
what the tool is for**, which is more than most of this page manages.

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

## Stretch 2 — not started

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
elected — there is still no mechanism — so Stretch 2 inherits Stretch 1's
government model unless something changes, with one difference that matters:
**the laws will have been written by a different repository than the one they
bind.** That is the first real separation this arrangement has had, and it
arrives by the presidency moving rather than by anybody designing it. The tool does not
exist yet; a stub holds its place and CI carries a job saying whether it is
ready to be started. **Stretch 2 cannot open before kanon does**, which makes
the readiness check the thing standing between the two stretches rather than a
convenience.

**Its first responsibility is this page.** Before anything else it is asked to
do, the president of a stretch publishes a **working summary of its stretch** —
*working* meaning kept current while the stretch runs, not written at the end
from memory. **A summary composed afterwards is a reconstruction**, and a
reconstruction by the party being described is the weakest document this
ecosystem could produce.

**And it inherits this file rather than starting one.** Stretch 1's entry
travels with it, unchanged and unchangeable. **anoieu will not be able to edit
its own history after that**, which is the arrangement working rather than a
loss.

---
