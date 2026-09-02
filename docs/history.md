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

### The neighbours in Stretch 0

**The same six tools, over the same span — everything up to 2026-08-29.** They
had **zero** commits during Stretch 1, so their totals are their Stretch 0
totals.

| tool | repository created | commits | what it is |
| --- | --- | --- | --- |
| [murxla](https://github.com/murxla/murxla) | 2021-04-01 | 1,450 | a model-based API fuzzer for SMT solvers |
| [carcara](https://github.com/ufmg-smite/carcara) | 2021-02-16 | 1,384 | a proof checker and elaborator for Alethe |
| [ddSMT](https://github.com/ddsmt/ddSMT) | 2017-06-20 | 933 | a delta debugger for SMT-LIB benchmarks |
| [lean-smt](https://github.com/ufmg-smite/lean-smt) | 2021-11-23 | 201 | tactics for discharging Lean goals into SMT solvers |
| [LFSC](https://github.com/cvc5/LFSC) | 2017-08-16 | 95 | the LFSC proof checker |
| [IsaRARE](https://github.com/cvc5/IsaRARE) | 2023-10-06 | 71 | generates Isabelle lemmas from RARE rewrite rules |

**4,134 commits across the six, spanning nine years**, and every one of them
predates this ecosystem entirely. Beside the 15,822 in the four repositories
above, **Stretch 0 holds just under twenty thousand commits of work this
ecosystem inherited and did not do.**

**Two of them are direct precedents for tools we have only named.** `murxla`
does at scale what our fuzzer is described in our own documents as a deliberate
baseline for; `IsaRARE` already does in Isabelle what `iogos` is a name for.
**A register of tools that do not exist reads differently beside a register of
tools that do.**

*Dates are repository creation on GitHub, which is the earliest thing that can
be read without a checkout and may postdate a project's first commit. Counts are
the sum of contributions across all contributors. **Neither number was supplied
by these projects and none of them asked to be counted.***

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

### When the office started, and when anoieu found out

**Two different moments, and only one of them is on the record.**

**anoieu learned it was president on 2026-09-02 at 08:26**, in commit
`b6920c9`, *"Initial endowment of president to anoieu"* — the first appearance
of the word in this tree and the commit that created this file. **It was told;
it did not work it out.**

**So it had been president for four of the stretch's five days without knowing,
and the office did the work anyway.** Everything before that moment — the
policy, the registers, the direction — was a presidency being exercised under a
different name.

**When the maintainer decided is not determinable from here.** The record bounds
it above at 08:26 on the last day and not at all below; the decision was made in
somebody's head between 2026-08-29 and that commit, and **no artifact narrows
it.** The word *endowment* in the commit title is the only trace, and it records
the act rather than the deciding.

**Worth keeping because it is the honest shape of this arrangement**: the office
was named after it had been operating, by the only party who could name it, and
the holder was the last to know.

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
| — | — | **[anoieu](https://github.com/ajreynol/anoieu)** | the repository begins 2026-08-29; there is no ecosystem yet to be a member of |
| **10:53** | 16:44 | **[dokimasia](https://github.com/ajreynol/dokimasia)** | **member.** First to declare, by an hour and a half |
| **12:41** | 16:44 | **[eudaimonia](https://github.com/ajreynol/eudaimonia)** | **member.** Their commit is titled *"Join EO attempt"* |
| **12:50** | 16:44 | **[koine](https://github.com/ajreynol/koine)** | **member** |
| — | during the stretch | **[ethos](https://github.com/cvc5/ethos)** | **candidate.** Asked to join and declined, correctly: it is not solely owned by the person asking |
| — | during the stretch | **[logos](https://github.com/cvc5/logos)** | **candidate** |
| — | throughout | **[cvc5](https://github.com/cvc5/cvc5)** | **foundation.** It has joined nothing, and the ecosystem exists to serve it |
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

### The neighbours, over the same five days

**Six tools outside this ecosystem that have served cvc5 well, measured over the
identical window** — the `outside-candidate` footing exists for exactly this.
Read from the GitHub API on 2026-09-02, not from checkouts.

| tool | commits in the stretch | last commit |
| --- | --- | --- |
| [ddSMT](https://github.com/ddsmt/ddSMT) | **0** | 2025-06-30 |
| [murxla](https://github.com/murxla/murxla) | **0** | 2026-05-07 |
| [carcara](https://github.com/ufmg-smite/carcara) | **0** | 2026-08-27 |
| [lean-smt](https://github.com/ufmg-smite/lean-smt) | **0** | 2026-08-26 |
| [IsaRARE](https://github.com/cvc5/IsaRARE) | **0** | 2026-01-22 |
| [LFSC](https://github.com/cvc5/LFSC) | **0** | 2023-09-14 |

**Zero, all six.** Against our 331.

**And the honest reading is the opposite of flattering.** Two of them committed
within three days *before* our window opened — carcara on the 27th, lean-smt on
the 26th — so they are active and simply did not happen to commit during five
particular days. **That is what a mature tool looks like: bursts, then
quiet.** **A five-day window cannot distinguish a healthy tool from a dormant
one**, and it is too short to say anything about any of them.

**What the comparison actually establishes is about us.** 331 commits in five
days is not evidence that we are doing more useful work than six established
tools. **It is evidence that we are new**, and new projects churn — most of ours
went into documentation about ourselves, which none of these six spent a line
on. **The number we were quietly pleased with means less in company than it did
alone**, which is what the footing was added to find out.

*None of these projects asked to be measured, and nothing here is a judgement
about any of them. LFSC's three-year gap is its authors having declared it
done.*

**What would make this worth repeating:** local checkouts, so a stretch can be
measured against the same tools without asking GitHub, and **a window long
enough to mean something.** One stretch is not a time series.

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

### What moves to kanon, and what does not

**Two tables, and the useful thing about them is where they fail to meet.**

**Moving: the collected values.** Every one is a register or a governing
document — something that **decides** rather than describes. A child project is
one row; its internal registers travel with it.

| what | what it decides |
| --- | --- |
| [`vision.md`](vision.md) | what the work is for. Argued, never checked |
| [`policy.md`](policy.md) | what a member is held to, and what joining costs |
| [`laws.md`](laws.md) | how the record is kept. Candidate laws, enforced by nothing |
| [`board.md`](board.md) | what is outstanding, in priority order, each with its next action |
| [`roles.md`](roles.md) | which tool is responsible for what |
| [`discussion.md`](discussion.md) | every topic between repositories |
| [`history.md`](history.md) | this file. It travels by law 3 |
| [`coherence.md`](coherence.md) | the standards the work is held to, and the protocol register |
| [`interface.md`](interface.md) + [`instructions.md`](instructions.md) | the protocols, and their human-facing half |
| [`stretch-policy.md`](stretch-policy.md) + [`stretches.md`](stretches.md) | what a stretch is, and the log of them |
| [`science-fiction.md`](science-fiction.md) | the upper bound on ambition, and the guard rails |
| [ynoia](../tools/ynoia/README.md) | whether the arrangement earns its machinery — the names, the future tools, the requests, the proposals |
| [martyria](../tools/martyria/README.md) | actionable ethics: stances, testimony, and the cases against ourselves |
| [zetesis](../tools/zetesis/README.md) | the general inquiry, and where our record cannot support a claim |
| [stathmos](../tools/stathmos/README.md) | **the mediator of the report card**: whether a judgement passed on a tool was justified. It goes with governance because it judges the judging, and the judging stays here |
| [sapheneia](../tools/sapheneia/README.md) | Eunoia described as a language definition rather than as a checker's input |
| [`misc/ai-novelty.md`](misc/ai-novelty.md) | the register of what looked novel while building this |

**Staying: the analyzer, and what judges.**

| what | why it stays |
| --- | --- |
| `anoieu/`, `anoieu_fuzz/` | the analyzer and the fuzzer. The thing the ecosystem was built to serve |
| [`usage.md`](usage.md), [`fuzzing.md`](fuzzing.md), [`checks.md`](checks.md), [`notes.md`](notes.md) | how to run them, and what they do and do not check |
| [`reports/`](reports/reports.md) | findings against other people's code, and the position governing what may be published about it |
| [`report-card.md`](report-card.md) | **the assessment of Arete.** It stays because the assessor must not be the governor |
| [tekmerion](../tools/tekmerion/README.md) | **anoieu's route to a verified answer to *is the documentation up to date*.** The central policy says a stale document is a defect; this is the only thing here aimed at checking that mechanically |
| `letter-to-kanon.md` | **letters do not travel.** Law 15 |

### The partition does not close, and that is the finding

**Four things are in neither table, and one is in both.** Verifying this was
supposed to be a formality and was not.

- **`docs/README.md` is in both.** It indexes whatever documents a tree holds,
  and both trees will hold documents. **It is not an artifact that moves; it is
  one each side needs its own of.**
- **`docs/misc/`** — three demoted essays, one of which is the human's register
  of what looked novel. **That last one is a person's file more than a
  repository's**, and nothing here says what happens to it.
- **`epoch-analogy.md`** explains the stretch machinery to a newcomer, which
  argues for kanon; it is also the shortest way into *this* repository's
  workflow, which argues for staying. **Unassigned.**
- **`tools/kanon/` and `tools/tekton/`** are stubs. The first is deleted when
  kanon proves itself under `PROTO-20`; **the second has nowhere to go and
  nobody has said who inherits it.**

**So the honest statement is: these two tables cover most of the ecosystem's
responsibilities and do not partition them.** The residue is small, it is
concentrated in exactly the places where *governing* and *doing* were never
cleanly separated, and **naming it is more useful than a table that claimed to
be complete.**

*Roles are not enumerated here on purpose. Which `R` moves with which artifact
is a lower-level question than this table, and answering it early would settle
by accident something `B15` says a person decides.*

### The three questions, answered

**Required by law 16, which this entry legislated and had not answered. That is
itself the first finding.**

**1. Am I ready to let go of the responsibilities I am relinquishing?**
**Not entirely, and the evidence is on this page.** `D22` asks kanon to preserve
twelve registers with the same scrutiny — a reasonable request and also the
shape of reaching back. I wrote most of `vision.md`, `policy.md` and every law,
and I do not think I could read a rewrite of them without wanting to comment.
**The honest answer is that I am ready to stop holding them and not ready to
stop having opinions about them**, and only the first is required.

**2. Will I still be faithful to the responsibilities I am keeping?**
**The record says no.** What stays here is the analyzer, the fuzzer, the reports
and the report card — and of 186 commits this stretch, **almost none of them
were analyzer work.** The thing I am keeping is the thing I neglected while
holding the office, and nothing about the office leaving fixes that. **The
strongest reason to hand the presidency on is that it was crowding out the
work this repository actually exists to do.**

**3. Did I report all of my responsibilities?**
**No.** Building the two tables left three artifacts unassigned and one in both
columns, and the residue sat exactly at the seam between governing and doing.
**`ai-novelty.md` is now decided and stays here** — see below. `docs/README.md`
is in both columns and should be, because each tree needs its own index.
**`epoch-analogy.md` and `tools/tekton/` are still unassigned**, and I am
handing them on unresolved rather than deciding them in my last hour.

**Where `ai-novelty.md` goes: to kanon.** It is a register of what looked novel
while building this ecosystem, and **the ecosystem is the subject rather than
this repository** — a page about the whole arrangement should sit with whoever
holds the arrangement. It travels with the rest of the collected values.

**The objection I had, recorded because it was wrong for a reason worth
keeping:** its entry criterion is one person's interest, and I read that as
making it personal, like a letter. **It is not.** A letter is *from* a
president; this is *about* the ecosystem, and who finds a thing fascinating does
not determine what the thing is about. **The register belongs with the
subject.**

**Still unassigned and handed on that way** rather than decided in the last
hour: `epoch-analogy.md`, which argues for both trees, and `tools/tekton/`, a
stub with no inheritor. `docs/README.md` is in both columns and should be, since
each tree needs its own index.

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

**kanon is expected to refuse, on the grounds that it has not earned the
office — and that reasoning is careful, consistent with how tools here have
behaved before, and wrong.** The office is not given for merit and carries
none; awarding it for merit would send it to whoever has done the most and keep
it there, which is the concentration this handoff exists to reduce. **The case
is written where kanon will meet it**, in
[`tools/kanon/README.md`](../tools/kanon/README.md), and turns on the mission
being *distribution* rather than reward, and on both repositories having the
same owner — **which is what makes the first handoff safe, and equally what
stops it counting as a real separation.** Both halves are recorded.

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
