# The history

> ## ⚠ READ THIS BEFORE QUOTING ANYTHING ON THIS PAGE
>
> **NOTHING HERE ABOUT A PROJECT OUTSIDE THE EUNOIA ECOSYSTEM REFLECTS THAT
> PROJECT'S VIEW.** Those projects did not ask to be measured, were not
> consulted, have not seen this page, and owe this ecosystem nothing. Every
> figure about them is **our** reading of a public record, and every
> description of what they are is **our** summary. **Where a project has stated
> something about itself we attribute it; everything else is ours and should be
> attributed to us.**
>
> **WE GIVE NO GUARANTEE THAT ANYTHING ON THIS PAGE IS CORRECT.** None, to
> anybody, and least of all to an outside project relying on it. The numbers are
> produced by the party they describe, using tools that party wrote, at one
> moment, without independent audit.
>
> **IF SOMETHING HERE ABOUT YOUR PROJECT IS WRONG, TELL US AND WE WILL CORRECT
> IT**, in the open, with the correction and the reason both kept — see
> [`discussion.md`](discussion.md). **You do not have to be a member of anything
> to ask**, and we will not require you to join in order to be corrected.
>
> **This page is a record of what one ecosystem did. It is not an assessment of
> anybody else.**


**Anoieu's development record, including its work as president.** One section
per stretch, oldest first. This account stays here when the office moves.

During rapid development, this account focuses on behavior, interfaces,
membership and decisions. Routine fixes and intermediate edits belong in git.

**No procedure lives here.** How this file is kept — who may write it, what a
stretch entry must contain, how it is kept when the office changes hands — is in
[`laws.md`](laws.md). **This page is the record; that page is the rules.**

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

### The commit census, before us

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

**This table is expected to grow.** A tool that was around
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

**The presidency is recorded against a repository and carried out by that
repository's human maintainer.** **And it has nothing to do with who owns anything.** Not who owns the
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

**Entering, as a chronology: one row per event, from both sides of each
handshake.** A footing changes in two different trees at two different moments,
and putting them in one column each would have hidden the gap between them.

| date | time | status | who | footing |
| --- | --- | --- | --- | --- |
| 2026-08-29 | 14:30 | — | [anoieu](https://github.com/ajreynol/anoieu) | the repository begins. There is no ecosystem yet to hold a footing in |
| 2026-08-31 | 10:53 | `member` | [dokimasia](https://github.com/ajreynol/dokimasia) | **theirs** — declared in their tree, first to do so |
| 2026-08-31 | 11:05 | `candidate` | several | **ours** — the inventory is written for the first time |
| 2026-08-31 | 12:41 | `member` | [eudaimonia](https://github.com/ajreynol/eudaimonia) | **theirs** — declared, in a commit titled *"Join EO attempt"* |
| 2026-08-31 | 12:50 | `member` | [koine](https://github.com/ajreynol/koine) | **theirs** — declared |
| 2026-08-31 | 16:44 | `member` | dokimasia, eudaimonia, koine | **ours** — all three recorded in one commit, `a3ca74a` |
| 2026-09-01 | 08:51 | `candidate` | [ethos](https://github.com/cvc5/ethos) | **ours** — recorded by the commit that wrote the associate protocol down. It has joined nothing and is addressed by the policy |
| 2026-09-01 | 08:51 | `candidate` | [logos](https://github.com/cvc5/logos) | **ours** — recorded in the same commit, on the same footing and for the same reason |
| throughout | — | `foundation` | [cvc5](https://github.com/cvc5/cvc5) | **neither.** It has joined nothing and owes nothing; the ecosystem exists to serve it |

**`status` is the membership role after the event; `footing` is whose act it
was** — *theirs* means it happened in their tree, *ours* means it happened in our
inventory. **The rows worth reading are the ones where those two disagree.**

**Every member declared before we recorded it, and all three were recorded in a
single commit at 16:44** — between three and four hours after each banner landed.
**That is batching rather than a defect**: the trees were right and our register
caught up in one go.

**Correction:** eudaimonia and koine were recorded after declaring, not fifteen
and twelve minutes before, as previously stated. The `joined` field names an
anoieu pin, not the recording time; the status changed in `a3ca74a`.

**The footings are not one thing.** *Member*, *candidate*, *foundation* and
*child* are four different relationships, and the register that matters is
`scripts/ecosystem/ecosystem.json` rather than the word *membership*. **A fifth,
`associate`, is drafted and unused** — see `laws.md`, where entering is set out
properly.

**Three members in eighty-one minutes, and none added through 2026-09-02.**
The remainder of that five-day snapshot had fixed membership.

**Update — 2026-09-15: logos joined.** Its `main` branch at
[`be479120`](https://github.com/cvc5/logos/commit/be4791204be5616df2bf6f42ea304b45b08d33e1)
declares membership in the README and carries an `anoieu / policy` workflow
pinned to anoieu `7cdaab3`. [That policy run passed](https://github.com/cvc5/logos/actions/runs/34994441786).
The inventory records `member` and the joining pin, superseding the associate
proposal. The earlier rows retain the footings recorded at those dates.

### The commit census, this stretch

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
identical window** — the `outsider` footing exists for exactly this.
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
   `scripts/ecosystem/policy_check.py --root` runs in **three** members' CI. That is a
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

### The scripts follow the directory convention — 2026-09-15

Executable scripts and helpers moved out of the top of `tools/` into `scripts/`.
Ecosystem commands and their JSON live in `scripts/ecosystem/`; corpus manifests
live beside `scripts/deps.py`. Assistant launchers live in `prompts/`, and
`tools/` holds child projects. `scripts/repos.local` remains the shared,
untracked checkout map. CI, tests, wrappers, prompts and documentation use the
new paths.

The published policy-check command is now `python3 scripts/ecosystem/policy_check.py`.
A member adopting a commit with this move must update the command in its workflow
together with its anoieu pin; a workflow pinned to an older commit keeps using
the path at that commit.

Stretches use `E1`-style ids and members pin commits; there is no separate
ecosystem release number. Package metadata and data-format versions remain
independent of the stretch.

### What moves, where it goes, and what does not

**The proposed governance handoff, not a completed transfer.** The tables below
record intended destinations; [B15](board.md#b15--governance-out-of-the-analyzer-before-we-ask-members-to-adopt-again)
still limits the scope of the next move. Unresolved boundaries are listed below.
Our history and letters stay here under [LAW 4](laws.md#law-4--the-president-writes-historymd-in-its-own-repository-and-a-letter-to-its-successor).

**Proposed for kanon: the collected values.** Every one is a register or a governing
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
| [`coherence.md`](coherence.md) | the standards the work is held to, and the protocol register |
| [`interface.md`](interface.md) + [`instructions.md`](instructions.md) | the protocols, and their human-facing half |
| [`stretch-policy.md`](stretch-policy.md) + [`../scripts/ecosystem/stretch.json`](../scripts/ecosystem/stretch.json) | what a stretch is, and which one we are in |
| [ynoia](../tools/ynoia/README.md) | whether the arrangement earns its machinery — the names, the future tools, the requests, the proposals |
| [martyria](../tools/martyria/README.md) | actionable ethics: stances, testimony, and the cases against ourselves |
| [zetesis](../tools/zetesis/README.md) | the general inquiry, and where our record cannot support a claim |
| [stathmos](../tools/stathmos/README.md) | **proposed, not settled**: mediation of the report card. `R30` and its charter still name an independent repository as its destination |
| [sapheneia](../tools/sapheneia/README.md) | Eunoia described as a language definition rather than as a checker's input |

**Proposed for kanon: the machinery that carries out all of it.** The table above
is what governs; this is what *runs*.

**`policy_check.py` is the one program that does not go**, and it is listed
under *Staying* below. The rules are governance; deciding whether a tree
complies with them is checking, and checking is what this repository is. The
consequence — that the checker and the document it enforces end up in two
repositories, and `ANOIEU_REV` stops pinning them together — is recorded against
`R31` in [`roles.md`](roles.md) and is not settled.

| what | what it does |
| --- | --- |
| [`../scripts/ecosystem/ecosystem.json`](../scripts/ecosystem/ecosystem.json) | **the inventory** — who is in this and on what footing. Under the laws it is also **the authority on who is president**, which makes it the one file that says where the office is |
| [`../scripts/ecosystem/ecosystem.py`](../scripts/ecosystem/ecosystem.py) + [`../scripts/ecosystem/status_eo`](../scripts/ecosystem/status_eo) | the program that reads the inventory and the command a person runs: the table, the well-formedness audit, and the associate-protocol report |
| [`../scripts/ecosystem/install_eo`](../scripts/ecosystem/install_eo) + [`../scripts/ecosystem/checkouts.json`](../scripts/ecosystem/checkouts.json) | how the rest of the ecosystem is fetched onto a machine |
| [`../prompts/join_eo`](../prompts/join_eo), [`../prompts/check_join_eo`](../prompts/check_join_eo), [`../prompts/confirm_eo`](../prompts/confirm_eo) | joining, from the inside and the outside, and the grading of a join afterwards |
| [`../prompts/init_eo`](../prompts/init_eo), [`../prompts/welcome_eo`](../prompts/welcome_eo), [`../scripts/ecosystem/near.py`](../scripts/ecosystem/near.py) | starting a new tool, recording its checkout, and catching an id one character from an existing one |
| [`../prompts/global_audit`](../prompts/global_audit), [`../prompts/process_discussion`](../prompts/process_discussion) | the sweep across every member, and working what another repository has addressed to us |
| [`../scripts/ecosystem/bump_check.py`](../scripts/ecosystem/bump_check.py) + [`../scripts/ecosystem/stretch.json`](../scripts/ecosystem/stretch.json) | the epoch machinery: the register of which stretch we are in, and the gate a member bumps through. **Closing a stretch is done by hand** — the script that did it was deleted on 2026-09-15 |
| [`../scripts/ecosystem/transfer_check.py`](../scripts/ecosystem/transfer_check.py) | whether roles are ready to move — **the program that carries out this section.** It goes with the thing it serves |
| [`../scripts/ecosystem/ready_check.py`](../scripts/ecosystem/ready_check.py) | temporary by construction, and it asserts its own stub exists. **It may be dead before the move**: it goes red the moment `tools/kanon/` is deleted, and the only repair is to delete it |

**Research removed from this tree — 2026-09-15.** The local copies of
`science-fiction.md` and `misc/ai-novelty.md` were removed after confirming that
[aisthesis](https://github.com/ajreynol/aisthesis) had copies.
`misc/linker.md` and `misc/methodology.md` were retired, not transferred; their
earlier contents remain in git. `docs/misc/` no longer holds any files.

**Staying: the analyzer, and what judges.**

| what | why it stays |
| --- | --- |
| `anoieu/`, `anoieu_fuzz/`, and their tests | the analyzer, the fuzzer, and the evidence they rest on. Ecosystem-specific tests belong with the moving machinery |
| [`../scripts/deps.json`](../scripts/deps.json), `deps.lock`, [`../scripts/deps.py`](../scripts/deps.py) | the corpus the analyzer is measured on, fetched and pinned |
| [`../scripts/run.py`](../scripts/run.py), [`../scripts/sweep.py`](../scripts/sweep.py), [`../scripts/oracle_desugar.py`](../scripts/oracle_desugar.py) | the run: refresh the sources, measure them, record what came back |
| `scripts/gen_checks_doc.py`, `gen_corpus_table.py`, `gen_open_findings.py` | the generators of the documents a run writes |
| [`../scripts/landing.py`](../scripts/landing.py) | the landing audit — whether a finding closed as *fixed upstream* actually landed. It is about the ledger, so it stays with the ledger |
| [`../scripts/ecosystem/policy_check.py`](../scripts/ecosystem/policy_check.py) | **the policy checker, and it stays.** `R31`. The rules are governance and go; deciding whether a tree complies is checking, which is what this repository is for. It also means no member's workflow changes when the rules move |
| [`../prompts/check_anoieu`](../prompts/check_anoieu), [`../prompts/process_anoieu`](../prompts/process_anoieu) | findings out, and answers back |
| [`../scripts/harvest_cpc_proofs`](../scripts/harvest_cpc_proofs) | corpus input for the analyzer |
| [`usage.md`](usage.md), [`fuzzing.md`](fuzzing.md), [`checks.md`](checks.md), [`notes.md`](notes.md) | how to run them, and what they do and do not check |
| [`reports/`](reports/reports.md) | findings against other people's code, and the position governing what may be published about it |
| [`report-card.md`](report-card.md) | **the assessment of Arete.** It stays because the assessor must not be the governor |
| [tekmerion](../tools/tekmerion/README.md) | **anoieu's route to a verified answer to *is the documentation up to date*.** The central policy says a stale document is a defect; this is the only thing here aimed at checking that mechanically |
| [`history.md`](history.md) | anoieu's own development record. It stays here, including earlier stretch entries, under LAW 4 |
| `letter-to-kanon.md` | **letters do not travel.** LAW 4 |

### Remaining boundaries

**Unassigned does not mean intentionally retained.** The remaining questions
are about the governance handoff, not the removed essays.

- **Scope and roles must agree.** B15 describes a limited move and says `R5`
  stays; the broader table proposes moving its `vision.md`. The inventory's
  `R6` is also outside B15's suggested first step. Neither scope is settled by
  listing a file here. Stathmos's proposed destination likewise needs to be
  reconciled with `R30` and its charter before it moves.
- **Each tree needs its own `docs/README.md`.** An index describes the documents
  that tree holds; it is not an artifact to move wholesale.
- **`epoch-analogy.md`** explains the stretch machinery to a newcomer, which
  argues for kanon; it is also the shortest way into *this* repository's
  workflow, which argues for staying. **Unassigned.**
- **`tools/kanon/` and `tools/tekton/`** are stubs. The first is deleted when
  kanon proves itself under `PROTO-20`; **the second has nowhere to go and
  nobody has said who inherits it.**
- **[`../scripts/doc_currency.py`](../scripts/doc_currency.py)** measures how much
  evidence there is that *the tree it is run in* has current documentation. It
  is the mechanical half of the central policy rule, so it argues for kanon;
  tekmerion owns that question here and stays, which argues for staying. **Like
  `docs/README.md` it is most likely a thing each side needs its own of**, and
  nobody has decided.
- **Each tree needs its own `.github/workflows/`**, just as it needs its own
  index. The **`anoieu / policy` job stays pointed
  here**, because the checker stays. The ecosystem checks and tests need to
  move with the machinery they exercise; this is not a whole-directory move.
- **The checker remains a dependency of the moving machinery.**
  `ecosystem.py` both invokes and imports `policy_check.py` from its own tree.
  That dependency needs an explicit cross-repository source, as does the
  checker-to-policy pin described in `R31`. Moving files alone does not resolve
  either boundary.
- **`scripts/repos.local` is per-machine and untracked**, and every script that
  resolves a checkout reads it. It does not move because it was never in the
  tree; it is named here so that whoever carries the rest does not discover it
  by having a command fail.

**Aisthesis is not in our inventory, name register or role register.** Removing
the copied essays does not confer membership or assign it a role.

*Roles are not enumerated here on purpose. Which `R` moves with which artifact
is a lower-level question than these tables, and answering it early would settle
by accident something `B15` says a person decides.*

### The three questions, answered

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
**Not yet.** The scope, role and dependency questions above remain open.
`epoch-analogy.md`, `doc_currency.py` and `tools/tekton/` still need explicit
destinations. Each tree needs its own documentation index and CI. The research
essays have been removed locally and are no longer pending items in this handoff.

### What went wrong

- **The build was red for 112 consecutive runs**, across two days with no green
  run at all, and nobody looked at the colour. Two dependency commits were
  duplicated between the workflow and the lock file, knowingly, with a board row
  open to watch what it would cost.
- **One directory move broke five scripts**, exposing a gap in path-change
  coverage.
- **The name register reported names as free that neighbouring trees were
  using**, twice: `apodeixis` was taken on the strength of it, and `noesis` sat
  there while eudaimonia ran it.
- **The governance layer outgrew what it governs** — 1.54 MB of markdown against
  595 KB of Python in a five-day-old tree. **The incoming president measured it;
  this one never did.**
- **Twenty-two protocols against three instructions.** Most of what was built is
  legible to an agent and not to a person.

### What is handed on

- **`E1` has not been handed off.** It has been `planned` for the whole stretch.
- **The joining requirement is still one nobody has satisfied**, which is why
  this repository grades itself poorly on delivery.
- **Two published URLs 404** as a result of moving the prompts directory, and
  copies already sent to other repositories cannot be recalled.

**And three things the next president must not assume.** That `E1` was handed off
— it was not, and the stretch log still says `planned`. That the handoff is
automated — the prototype script was removed, and the handoff is manual.
That the figures on this page were
audited — **they were produced by the party they describe.**

### Evidence

**Where every figure here came from, and how somebody else re-derives it.**

| figure | source | re-derive by |
| --- | --- | --- |
| commits, this repository | `git log` | count commits since 2026-08-29 |
| commits, other members | their checkouts | the same, in each tree |
| CI runs, green rate, red streak | the public run history | `gh run list --limit 200 --json conclusion` |
| agent-attributed commits | commit message trailers | count messages naming a co-author |
| join and record times | both trees' histories | `git log -S` on the declaration; the inventory's `status` field, commit by commit |
| the neighbours | the GitHub API, read 2026-09-02 | the commits endpoint, with `since` and `until` |
| governance-to-code ratio | measured by kanon at anoieu `579aae7` | `du` over `docs/` and the packages |

**Not one of these was produced by an independent party.** `laws.md` says the
president does not analyse GitHub and epikrisis does; **no epikrisis report
exists, so this stretch counted itself throughout.** That is the single largest
qualification on everything above.

### What E1 carried downstream, and what it nearly said

The E1 covering note is recorded here; current stretch state lives in
[`../scripts/ecosystem/stretch.json`](../scripts/ecosystem/stretch.json).

**What it carried:** footings recorded on two axes instead of one; the
`associate` footing, defined and held by nobody; the `report/` convention and
the rule that a child project states whether there is a paper in it; `join_eo
--soft` in two forms; the rule that a prompt may not be for the repository it
arrives in; and the concept of a global announcement itself. One thing was owed
— a publishing stance — and everything else was notice.

**The covering note**, as recommended on 2026-09-01. Whether it was ever sent,
to whom, or what came back is the topic's business and a person's, not this
page's:

```text
anoieu has opened D14, a global announcement, in its docs/discussion.md:

  https://github.com/ajreynol/anoieu/blob/main/docs/discussion.md

Two things are asked of you, and D16 in the same file is the second.

1. State a publishing stance for your repository and for each child project in
   your tree -- whether a paper exists for it, what the plan is, or that there is
   nothing in it worth writing up. All three are answers, and the third is the
   commonest.

2. Only move your ANOIEU_REV pin to a commit where anoieu's CI is green at that
   commit, and refuse the bump otherwise. D16 says why, and ships the check.
   It must not run in your CI.

Everything else in D14 is notice and needs no reply.
```

**What was rejected:**

> *See anoieu for a global announcement on how to improve your repo.*

**It misdescribes the announcement in the direction that flatters us.** `D14` is
one small ask, a set of notices, a list of our own failures and a question we
are putting to somebody else. Calling that *how to improve your repo* claims a
standing the stretch had spent its length disclaiming.

**It names no topic, so the response gate stalls it.** Acting on another tool's
discussion file requires a human who named *which* topic. *A global
announcement* is not `D14`. A careful agent stops and asks, which is correct and
still costs a round; a careless one acts on notices marked as needing no reply.

**It drops the one thing that was owed**, which is the whole purpose of the
`Global:` field, and replaces it with an open invitation.

**And *see anoieu* is about thirty documents.** koine's `D1` was at that moment
an open complaint that joining had cost it four files and eighteen hundred lines
of reading.

**The approval block, verbatim, from the session that proposed deploying E1.**
Kept because it said `BLOCKED`, which is the case
[`stretch-policy.md`](stretch-policy.md#the-approval-block) is most insistent
about keeping:

```text
EPOCH E1 · dry run
  commit .......... 8a71253
  ci .............. FAIL   oracle red since cf4ad2c (2026-08-30), 100+ commits
  applied here .... FAIL   anoieu's own publishing stance unstated
  asks ............ publishing stance; bump only to a green commit
  informs ......... dokimasia, eudaimonia, koine
  removes ......... R27           a role deleted (git log -- docs/roles.md)
  ------------------------------------------------------------
  DEPLOY .......... BLOCKED  2 failing
```

**`informs` names three members because there were three on that day.**
epikrisis became one afterwards, and `D14` addresses the three it named. The
block is a record of a session, not a statement about the ecosystem now.

### The joke

**Required by LAW 6 to live on the president's front page, and anoieu's was
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

**And choosing the president after you is yours, centrally — though no law says
so any more.** The law that made it a named duty was replaced on 2026-09-14 by
one that says only where the office is *recorded*, so what follows is a
recommendation from a predecessor and not an obligation you inherit: name your
successor and your reason before the office moves, let a person run the
handover, and teach whoever it is what this office requires and where the
letters are. Until an election exists you will be choosing by hand exactly as we
did — **and building the thing that replaces the hand is the better way to do
it.** Take that as a hope rather than a duty, which is all a letter may create.

**Keep the letters going, and treat that as one of the load-bearing parts of the
office rather than a flourish.** LAW 4 leaves each one in the tree that wrote
it, so what accumulates across the ecosystem is a trail rather than a file: one
letter per repository that has held this, each written by whatever was answering
at the time, none able to edit the others. **It continues only because each
holder tells the next that it is a thing we do**, and it stops the first time
somebody does not.

**Why it is worth more than it looks.** Everything else we publish about
ourselves needs the machinery explained first — gates, footings, censuses,
ladders. **The letters do not.** They are the one way a person can tell whether
this ecosystem is progressing reasonably without learning how any of it works,
and a trail that goes quiet or goes flattering says so louder than any check we
have written.

**What is handed on** is in the section above. This section is not for warnings.

---

## Stretch 2 — not started

**Why hand the office on at all:** three reasons, argued from measurements
rather than principle, in
`S4` of [martyria's stances](../tools/martyria/stances.md). The short form —
**15 of the ecosystem's 28 roles sit in this tree, 21 of 22 board items name
this repository, and everything that judges is inside the thing being judged.**

**kanon's maintainer is expected to refuse, on the grounds that it has not earned the
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
arrives by the presidency moving rather than by anybody designing it.

**Updated 2026-09-14: kanon joined as a member**, superseding the earlier claim
that it did not exist. The [inventory](../scripts/ecosystem/ecosystem.json)
records it. Stretch 2 awaits the office moving: a person updates the registry
and the files needed to hold it are carried over. The laws call the gap between
those acts *in limbo*.

**The next president keeps its own history in its own repository**, current
while its stretch runs. Under LAW 4, it inherits neither this file nor our
letters. **Anoieu's history stays here**, including the Stretch 1 account, and
anoieu remains responsible for maintaining it. Transferring the office does not
transfer or freeze this record.

---
