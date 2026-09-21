# The history

Current command and helper locations are listed in [maintenance](maintenance.md#the-scripts).
Links below follow the files moved on 2026-09-18; historical path names remain as recorded.

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
[`laws.md`](https://github.com/ajreynol/kanon/blob/main/docs/laws.md). **This page is the record; that page is the rules.**

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

**At the 2026-09-02 snapshot it was still open.** Created 2026-08-26 and unmerged
when that snapshot was taken,
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

**Seventeen years, four repositories, and more than 130 people.** The first
five-day snapshot of Stretch 1, by comparison, counted 331 commits.

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
had **zero** commits during Stretch 1's first five-day snapshot, so their totals
as measured on 2026-09-02 are their Stretch 0 totals.

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
[`laws.md`](https://github.com/ajreynol/kanon/blob/main/docs/laws.md) sets out.

**Term: 2026-08-29 through 2026-09-15 — eighteen calendar days inclusive.**
It ended with the manual handoff to kanon.

Unless separately dated, the statistics and assessments below cover August 29
through September 2.

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

**And it is a role held by a tool**, which is the shape [`roles.md`](https://github.com/ajreynol/kanon/blob/main/docs/roles.md)
is built for and where this one is conspicuously absent. That is the second
open question below.

### Government model

**One office, bestowed, and no separation of powers.** Named plainly because
[`laws.md`](https://github.com/ajreynol/kanon/blob/main/docs/laws.md) requires the model that was *executed* rather than the one
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

**So it had been president for the first four days without knowing,
and the office did the work anyway.** Everything before that moment — the
policy, the registers, the direction — was a presidency being exercised under a
different name.

**When the maintainer decided is not determinable from here.** The record bounds
it above at 08:26 on 2026-09-02 and not at all below; the decision was made in
somebody's head between 2026-08-29 and that commit, and **no artifact narrows
it.** The word *endowment* in the commit title is the only trace, and it records
the act rather than the deciding.

**Worth keeping because it is the honest shape of this arrangement**: the office
was named after it had been operating, by the only party who could name it, and
the holder was the last to know.

### How long it lasted, and who joined

The office was explicitly bestowed on September 2 and passed to kanon on
September 15 at 16:15 CDT, when
[`7eb9973`](https://github.com/ajreynol/kanon/commit/7eb9973d921aedc845b9bdc33a67aad3df242268)
recorded the receiving repository as president.

**Entering, as a chronology: one row per event, from both sides of each
handshake.** A footing changes in two different trees at two different moments,
and putting them in one column each would have hidden the gap between them.
Times are commit timestamps in CDT (UTC−05:00).

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
| 2026-09-14 | 17:00 | `candidate` | [kanon](https://github.com/ajreynol/kanon) | **ours** — entered in the inventory in [`6ebb5fd`](https://github.com/ajreynol/anoieu/commit/6ebb5fdf7a6503cbc164b846a7ef73f9142e581d) |
| 2026-09-14 | 17:30 | `member` | kanon | **theirs** — [`1bd2b6b`](https://github.com/ajreynol/kanon/commit/1bd2b6b90172c88389dea900ac765477d4bfc667), *Join eo*, adds the README declaration and policy CI, pinned to anoieu `4d21ec9` |
| 2026-09-14 | 17:37 | `member` | kanon | **ours** — membership and its joining pin recorded in [`3b384c9`](https://github.com/ajreynol/anoieu/commit/3b384c9e96a042395b4ff70eedb1f30c010b7c36) |
| 2026-09-15 | 11:21 | `member` | logos | **theirs** — [`be479120`](https://github.com/cvc5/logos/commit/be4791204be5616df2bf6f42ea304b45b08d33e1), *More positioning on Eunoia ecosystem (#463)*, declares membership and adds policy CI, pinned to anoieu `7cdaab3` |
| 2026-09-15 | 15:08 | `member` | logos | **ours** — membership and its joining pin recorded in [`0aa4395`](https://github.com/ajreynol/anoieu/commit/0aa4395eb83b8a5f2ffab7771bc7960cebb1d6bd), replacing `candidate` and the proposed associate footing |
| throughout | — | `foundation` | [cvc5](https://github.com/cvc5/cvc5) | **neither.** It has joined nothing and owes nothing; the ecosystem exists to serve it |

**`status` is the membership role after the event; `footing` is whose act it
was** — *theirs* means it happened in their tree, *ours* means it happened in our
inventory. **The rows worth reading are the ones where those two disagree.**

**The first three members declared before we recorded them, and all three were
recorded in a single commit at 16:44 on 2026-08-31** — between three and four
hours after each banner landed.
**That is batching rather than a defect**: the trees were right and our register
caught up in one go.

The `joined` field names an anoieu pin; the recording times come from the
inventory commits.

**The footings are not one thing.** *Member*, *candidate*, *foundation* and
*child* are four different relationships, and the register that matters is
`scripts/ecosystem/ecosystem.json` rather than the word *membership*. **A fifth,
`associate`, is drafted and unused** — see `laws.md`, where entering is set out
properly.

**Three members in eighty-one minutes, and none added through 2026-09-02.**
The remainder of that five-day snapshot had fixed membership.

**Logos joined on 2026-09-15.** Its `main` branch at
[`be479120`](https://github.com/cvc5/logos/commit/be4791204be5616df2bf6f42ea304b45b08d33e1)
declares membership in the README and carries an `anoieu / policy` workflow
pinned to anoieu `7cdaab3`. [That policy run passed](https://github.com/cvc5/logos/actions/runs/34994441786).
Anoieu recorded `member` and the joining pin in `0aa4395` at 15:08. Kanon's
membership was recorded on September 14 in `3b384c9` at 17:37, after its
declaration in `1bd2b6b` at 17:30.

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
record anything. **Six of its eight commits in this snapshot name the AI that helped
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

**Every one of our 323 commits in the snapshot is authored by a human.** Across
the whole ecosystem, **three** carry a `Co-Authored-By` trailer naming an agent,
all three in this repository. **The record therefore says a person wrote all of
it, and that is not what happened** — in anoieu nearly every line of prose and
code during those five days was written by an agent, reviewed by the maintainer,
and committed under their name. The arrangement is honest at every step and **the artifact it
produces is not**, because nothing in the commit format was asked to record the
difference.

### The neighbours, over the same five days

**Six tools outside this ecosystem that have served cvc5 well, measured over the
identical window** — the `outsider` footing exists for exactly this.
Read from the GitHub API on 2026-09-02, not from checkouts.

| tool | commits, 2026-08-29 through 2026-09-02 | last commit |
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

**What the joining handshake does and does not tell us.** The first three members ran
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
green run at all, and the streak that ended on 2026-09-02 ran to 112. The immediate
cause of the last of it was two dependency commits duplicated between the
workflow and the lock file, which drifted and which nothing compared — the
result recorded as `B20` on the board.

**The consequence is not only aesthetic.** The handoff protocol makes CI passing
non-negotiable for every party to a handoff. **For most of those first five days this
repository could not have handed anything to anybody**, and nobody noticed,
because nobody was looking at the colour.

### What is now true

**Six things recorded by 2026-09-02.** Stated as claims with the
evidence beside them, because a stretch entry that only lists difficulties is
as unreliable as one that only lists wins.

1. **Another repository's build depends on our checker, and has for days.**
   `scripts/policy_check.py --root` runs in **three** members' CI. That is a
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
User-facing commands live directly in `scripts/`; internal ecosystem helpers
and JSON stay in `scripts/ecosystem/`. Corpus manifests live beside
`scripts/deps.py`. Assistant launchers live in `prompts/`, and
`tools/` holds child projects. `scripts/repos.local` remains the shared,
untracked checkout map. CI, tests, wrappers, prompts and documentation use the
new paths.

The published policy-check command is now `python3 scripts/policy_check.py`.
A member adopting a commit with this move must update the command in its workflow
together with its anoieu pin; a workflow pinned to an older commit keeps using
the path at that commit.

Members pin commits; there is no separate ecosystem release number. Package
metadata and data-format versions remain independent.

### The planning draft was withdrawn — 2026-09-15

The epoch design documents, state register and obsolete stub were removed.
Anoieu no longer uses the draft's commands or workflow gates. The independent
commit-pin check stays. History and letters remain here; older references to E1
describe the abandoned proposal, not a current workflow.

### What moves, where it goes, and what does not

**Completed 2026-09-15.** Anoieu
[`ca58216`](https://github.com/ajreynol/anoieu/commit/ca58216f0bac265ef24b6cc671efb91ddc70a4b8)
removed the 47 governance documents, ecosystem commands, prompts and research
files carried to kanon in
[`7eb9973`](https://github.com/ajreynol/kanon/commit/7eb9973d921aedc845b9bdc33a67aad3df242268).
That receiving commit records kanon as `president` and anoieu as `member` in
the inventory. The analyzer, fuzzer, policy checker and reporting workflow stay
in anoieu, along with its history, correspondence, findings and report card.

**Planning record, preserved from before the transfer.** The tables below
record the intended destinations and unresolved questions at that time;
`B15` limited the scope of the next move as it read then; kanon has since
closed the item and keeps the procedure in [how a role is handed
off](https://github.com/ajreynol/kanon/blob/main/docs/roles.md#how-a-role-is-handed-off),
read 2026-09-21. **That link was dead until then** — it named a board heading
kanon no longer has, and nothing on either side could see it: our checker skips
every `http` target by design.
**Pages and commands kanon has since removed are named below and not linked.**
Kanon's `main` is the authority on everything it holds, so a link here goes to
`main` or nowhere: pinning one would hand a reader a superseded copy of somebody
else's live rules. **Read against kanon's tree on 2026-09-17, the ecosystem
commands and prompts in the second table are not in it**; several of them are
[koine](https://github.com/ajreynol/koine)'s `eo_cmd/` today. This table records
where they were proposed to go, which is what a planning record is for, and
naming them is as far as it goes. Unresolved boundaries are listed below.
Our history and letters stay here under [LAW 4](https://github.com/ajreynol/kanon/blob/main/docs/laws.md#law-4--the-president-writes-historymd-in-its-own-repository-and-a-letter-to-its-successor).

**Proposed for kanon: the collected values.** Every one is a register or a governing
document — something that **decides** rather than describes. A child project is
one row; its internal registers travel with it.

| what | what it decides |
| --- | --- |
| [`vision.md`](https://github.com/ajreynol/kanon/blob/main/docs/vision.md) | what the work is for. Argued, never checked |
| [`policy.md`](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) | what a member is held to, and what joining costs |
| [`laws.md`](https://github.com/ajreynol/kanon/blob/main/docs/laws.md) | how the record is kept. Candidate laws, enforced by nothing |
| [`board.md`](https://github.com/ajreynol/kanon/blob/main/docs/board.md) | what is outstanding, in priority order, each with its next action |
| [`roles.md`](https://github.com/ajreynol/kanon/blob/main/docs/roles.md) | which tool is responsible for what |
| [`discussion.md`](discussion.md) | every topic between repositories |
| `coherence.md` | the standards the work is held to, and the protocol register |
| `interface.md` + `instructions.md` | the protocols, and their human-facing half |
| [ynoia](https://github.com/ajreynol/kanon/blob/main/tools/ynoia/README.md) | whether the arrangement earns its machinery — the names, the future tools, the requests, the proposals |
| martyria | actionable ethics: stances, testimony, and the cases against ourselves |
| zetesis | the general inquiry, and where our record cannot support a claim |
| [stathmos](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/README.md) | **proposed, not settled**: mediation of the report card. `R30` and its charter still name an independent repository as its destination |
| [sapheneia](https://github.com/ajreynol/eunoia/blob/main/tools/sapheneia/README.md) | Eunoia described as a language definition rather than as a checker's input |

**Proposed for kanon: the machinery that carries out all of it.** The table above
is what governs; this is what *runs*.

**`policy_check.py` is the one program that does not go**, and it is listed
under *Staying* below. The rules are governance; deciding whether a tree
complies with them is checking, and checking is what this repository is. The
consequence — that the checker and the document it enforces end up in two
repositories, and `ANOIEU_REV` stops pinning them together — is recorded against
`R31` in [`roles.md`](https://github.com/ajreynol/kanon/blob/main/docs/roles.md) and is not settled.

| what | what it does |
| --- | --- |
| [`../scripts/ecosystem/ecosystem.json`](https://github.com/ajreynol/kanon/blob/main/scripts/ecosystem/ecosystem.json) | **the inventory** — who is in this and on what footing. Under the laws it is also **the authority on who is president**, which makes it the one file that says where the office is |
| [`../scripts/ecosystem/`](https://github.com/ajreynol/kanon/blob/main/scripts/ecosystem/ecosystem.json) + `../scripts/status_eo` | the program that reads the inventory and the command a person runs: the table, the well-formedness audit, and the associate-protocol report |
| `../scripts/install_eo` + [`../scripts/ecosystem/checkouts.json`](https://github.com/ajreynol/kanon/blob/main/scripts/ecosystem/checkouts.json) | how the rest of the ecosystem is fetched onto a machine |
| `../prompts/join_eo`, `../prompts/check_join_eo`, `../prompts/confirm_eo` | joining, from the inside and the outside, and the grading of a join afterwards |
| `../prompts/init_eo`, `../prompts/welcome_eo`, `../scripts/ecosystem/near.py` | starting a new tool, recording its checkout, and catching an id one character from an existing one |
| `../prompts/global_audit`, `../prompts/process_discussion` | the sweep across every member, and working what another repository has addressed to us |
| `../scripts/bump_check.py` | checks whether the exact policy commit a member proposes to adopt passed CI |
| `../scripts/transfer_check.py` | whether roles are ready to move — **the program that carries out this section.** It goes with the thing it serves |
| `../scripts/ready_check.py` | temporary by construction, and it asserts its own stub exists. **It may be dead before the move**: it goes red the moment `tools/kanon/` is deleted, and the only repair is to delete it |

**Research removed from this tree — 2026-09-15.** The local copies of
`science-fiction.md` and `misc/ai-novelty.md` were removed after confirming that
[aisthesis](https://github.com/ajreynol/aisthesis) had copies.
`misc/linker.md` and `misc/methodology.md` were retired, not transferred; their
earlier contents remain in git. `docs/misc/` no longer holds any files.

**Staying: the analyzer, and what judges.**

| what | why it stays |
| --- | --- |
| `anoieu/`, `anoieu_fuzz/`, and their tests | the analyzer, the fuzzer, and the evidence they rest on. Ecosystem-specific tests belong with the moving machinery |
| [`../scripts/deps.json`](../anoieu_analyzer/reporting/config/deps.json), `deps.lock`, [`../scripts/deps.py`](../anoieu_analyzer/reporting/deps.py) | the corpus the analyzer is measured on, fetched and pinned |
| [`../scripts/run.py`](../scripts/run.py), [`../scripts/sweep.py`](../tests/sweep.py), [`../scripts/oracle_desugar.py`](../tests/oracle_desugar.py) | the run: refresh the sources, measure them, record what came back |
| `scripts/gen_checks_doc.py`, `gen_corpus_table.py`, `record.py` | the generators of the documents a run writes |
| [`../scripts/verdicts.py`](../anoieu_analyzer/reporting/verdicts.py) | the verdict audit — whether a finding closed as *fixed upstream* actually landed. It is about the database, so it stays with the database |
| [`../scripts/policy_check.py`](../scripts/policy_check.py) | **the policy checker, and it stays.** `R31`. The rules are governance and go; deciding whether a tree complies is checking, which is what this repository is for. It also means no member's workflow changes when the rules move |
| [`../prompts/close_bug_db`](../prompts/close_bug_db) | what each watched project has since done about what we found. The `check_anoieu` / `process_anoieu` pair that carried findings out and answers back was removed on 2026-09-19 with the workflow it served |
| [`../scripts/harvest_cpc_proofs`](../scripts/harvest_cpc_proofs) | corpus input for the analyzer |
| [`usage.md`](../anoieu_analyzer/usage.md), [`fuzzing.md`](../anoieu_fuzz/fuzzing.md), [`checks.md`](../anoieu_analyzer/checks.md), [`notes.md`](../anoieu_analyzer/notes.md) | how to run them, and what they do and do not check |
| [`../bug_db/`](../bug_db/README.md), [`experience.md`](../docs/experience.md) | findings against other people's code, what came of them, and the position governing what may be published about it |
| `report-card.md` | **the assessment of Arete**, as the plan read on 2026-09-15: it stayed because the assessor must not be the governor. **Superseded 2026-09-17** — the role moved with stathmos and the page has followed it. [stathmos's edition](https://github.com/ajreynol/kanon/blob/main/tools/stathmos/docs/report-card.md) is the live one; the copy here, last graded 2026-09-02, is removed |
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
- **Each tree needs its own documentation index.** An index describes the
  documents that tree holds; it is not an artifact to move wholesale. Where the
  index sits is the tree's own business — anoieu's is a section of its front
  page.
- **`tools/kanon/`** remains a stub, to be removed only when its replacement
  is accepted under `PROTO-20`.
- **[`../scripts/doc_currency.py`](../policy_check/currency.py)** measures how much
  evidence there is that *the tree it is run in* has current documentation. It
  is the mechanical half of the central policy rule, so it argues for kanon;
  tekmerion owns that question here and stays, which argues for staying. **Like the documentation
  index it is most likely a thing each side needs its own of**, and nobody has
  decided.
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
**Not entirely, and the evidence is on this page.**
[`D22`](https://github.com/ajreynol/anoieu/blob/ca58216f0bac265ef24b6cc671efb91ddc70a4b8/docs/discussion.md#d22--the-collected-values-and-what-we-are-asking-you-to-do-with-them) asks kanon to preserve
twelve registers with the same scrutiny — a reasonable request and also the
shape of reaching back. I wrote most of `vision.md`, `policy.md` and every law,
and I do not think I could read a rewrite of them without wanting to comment.
**The honest answer is that I am ready to stop holding them and not ready to
stop having opinions about them**, and only the first is required.

**2. Will I still be faithful to the responsibilities I am keeping?**
**The record says no.** What stays here is the analyzer, the fuzzer, the reports
and the report card — and of 186 commits in the first five-day snapshot,
**almost none of them were analyzer work.** The thing I am keeping is the thing I neglected while
holding the office, and nothing about the office leaving fixes that. **The
strongest reason to hand the presidency on is that it was crowding out the
work this repository actually exists to do.**

**3. Did I report all of my responsibilities?**
**Not yet.** The scope, role and dependency questions above remain open.
`doc_currency.py` still needs an explicit destination. Each tree needs its own
documentation index and CI. The research essays and the withdrawn planning draft
are no longer pending items in this handoff.

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

- **The proposed E1 handoff did not happen.** Its planning machinery has been
  withdrawn.
- **The joining requirement is still one nobody has satisfied**, which is why
  this repository grades itself poorly on delivery.
- **Two published URLs 404** as a result of moving the prompts directory, and
  copies already sent to other repositories cannot be recalled.

**The next president must not assume the proposed E1 handoff happened or that
the deferred draft governs their work.** Role handoffs remain a person's decision.
The figures on this page were not independently audited: they were produced by
the party they describe.

### Evidence

**Where every figure here came from, and how somebody else re-derives it.**

| figure | source | re-derive by |
| --- | --- | --- |
| commits, this repository | `git log` | count commits in the recorded 2026-08-29 through 2026-09-02 window |
| commits, other members | their checkouts | the same, in each tree |
| CI runs, green rate, red streak | the public run history | read the runs in the recorded 2026-08-29 through 2026-09-02 window |
| agent-attributed commits | commit message trailers | count messages naming a co-author |
| join and record times | both trees' histories | `git log -S` on the declaration; the inventory's `status` field, commit by commit |
| the neighbours | the GitHub API, read 2026-09-02 | the commits endpoint, with `since` and `until` |
| governance-to-code ratio | measured by kanon at anoieu `579aae7` | `du` over `docs/` and the packages |

**Not one of these was produced by an independent party.** `laws.md` says the
president does not analyse GitHub and epikrisis does; **no epikrisis report
was available for the five-day snapshot, so that account counted itself.**
That is the single largest qualification on everything above.

### What E1 carried downstream, and what it nearly said

The covering note below is a dated record, not a current instruction. The
associated planning draft was withdrawn on 2026-09-15.

**What it carried:** footings recorded on two axes instead of one; the
`associate` footing, defined and held by nobody; the `report/` convention and
the rule that a child project states whether there is a paper in it; `join_eo
--soft` in two forms; the rule that a prompt may not be for the repository it
arrives in; and the concept of a global announcement itself. One thing was owed
— a publishing stance — and everything else was notice.

**What is no longer the policy's, recorded because it was announced to every
member as a rule.** The `report/` convention is in neither `policy.md` nor
`vision.md` under kanon, read 2026-09-19. Dokimasia reported that twice; the only
place in the shared machinery still naming it was this repository's own checker
coverage list, which is where a reader would take it for kanon's rule, and it was
removed from that list on 2026-09-19. All three addressees of the announcement
stated a publishing stance, so the announcement itself is settled and removed.

**Corrected 2026-09-21, because the earlier account was the more flattering one.**
This page said the convention *did not survive the handoff*, and kanon's answer to
our `D38` establishes that it did: their `policy.md` carried the whole section from
the handoff commit `7eb9973` — the layout row, the eight-to-twenty pages, and the
child-project rule about a paper — and it was removed the next morning in
`d892fa6`, a simplification pass that took it out with a great deal else. **Nobody
dropped it in transit; the office that then held the policy deleted it.** Kanon's
answer also settles the open question: the convention is not the policy's, it is
not being put back on an agent's reading, and **the announcement's first section is
withdrawn for good** — if a person wants it back we will be told rather than left
to notice. One cost of it was found in kanon's own tree while answering: a child
project there had been attributing the convention to `vision.md` on its front page
since 2026-09-18, resting a page of per-tool verdicts on it.

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

The proposed E1 handoff was blocked at anoieu `8a71253`: the oracle job failed
and anoieu had not yet stated its own publishing stance. It was not completed.

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

## Stretch 2 — began 2026-09-15

**President: kanon, from 2026-09-15 at 16:15 CDT.** Anoieu's presidency ended
with the manual handoff recorded in
[`7eb9973`](https://github.com/ajreynol/kanon/commit/7eb9973d921aedc845b9bdc33a67aad3df242268).
The successor keeps its own account of Stretch 2. The proposal below records
the reasoning behind the handoff.

**Why hand the office on at all:** three reasons, argued from measurements
rather than principle, in
`S4` of [martyria's stances](https://github.com/ajreynol/epikrisis/blob/main/tools/martyria/docs/stances.md). The short form —
**15 of the ecosystem's 28 roles sit in this tree, 21 of 22 board items name
this repository, and everything that judges is inside the thing being judged.**

**kanon's maintainer is expected to refuse, on the grounds that it has not earned the
office — and that reasoning is careful, consistent with how tools here have
behaved before, and wrong.** The office is not given for merit and carries
none; awarding it for merit would send it to whoever has done the most and keep
it there, which is the concentration this handoff exists to reduce. **The case
is written where kanon will meet it**, in
[`tools/kanon/README.md`](https://github.com/ajreynol/anoieu/blob/37d12779b4b0e9eb51c9f40e131ca7db4fcd5dae/tools/kanon/README.md), and turns on the mission
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

**Expected president: [kanon](https://github.com/ajreynol/anoieu/blob/37d12779b4b0e9eb51c9f40e131ca7db4fcd5dae/tools/kanon/README.md), by bestowal.** Not
elected — there is still no mechanism — so Stretch 2 inherits Stretch 1's
government model unless something changes, with one difference that matters:
**the laws will have been written by a different repository than the one they
bind.** That is the first real separation this arrangement has had, and it
arrives by the presidency moving rather than by anybody designing it.

**The next president keeps its own history in its own repository**, current
while its stretch runs. Under LAW 4, it inherits neither this file nor our
letters. **Anoieu's history stays here**, including the Stretch 1 account, and
anoieu remains responsible for maintaining it. Transferring the office does not
transfer or freeze this record.

---

### Correspondence answered, and four checks that were passing wrongly — 2026-09-17

**Thirty-nine topics across eight repositories named anoieu**, and none of them
had an answer in this tree. They are answered now, drafted for a person to
carry.

**The single largest class of answer was *that page is not ours any
more*** — the governance documents, the registers, the roles, the prompts and the
research pages left on 2026-09-15, and nobody who had addressed a topic to anoieu
had any way to know which half of it had moved.

**Four checks were reported by koine as passing when they should not, and all
four are fixed.**

| what | how it failed | what it is now |
| --- | --- | --- |
| `check_links` | read fenced code, so a quoted path in an example was a dead link | reads `prose()`, like `check_anchors` beside it; every adoption fixture carries a fenced example |
| `postmortem_shape()` | a wrapped `**Summary:**` matched nothing and was skipped in silence | `postmortem_summary()`, and no readable summary is a failure. Both retired on 2026-09-19 with the postmortem log |
| the 250-character limit | ended the field at a blank line, so pressing return evaded it | reads on to the next field, which is dokimasia's reading and koine's |
| `landing.malformed()` | needed the words *awaiting landing* before it would complain | **a closed verdict opens with one of seven words**, and `accepted and fixed` owes a marker |

**The fourth is the one worth keeping the reasoning for.** koine said no regex
closes it and they were right: the absence of a phrase is not detectable in free
text. What is detectable is the **presence of a required word**, so the outcome
became the required thing and the phrase became its consequence. A verdict
reworded past the audit now leaves the vocabulary instead.

**Three of the four had been reported twice** — opened 2026-09-01 and re-checked
at `9794f31` the same day — and were fixed in under an hour. A report we had
already been given twice was not a report we were short of evidence for.

**Two diagnostics were added rather than two checks.** A skip that exists because
a path is absent now says *this check turns on if you add one*, which is koine's
joining cascade made visible before it happens; and a run against a working
directory says how far that tree is from its own last commit, which is the cause
of the disagreement kanon reported between a local verdict and a published one.
Both are output rather than requirements, so both are available under contract 1.

**Eight dangling links were found in this file by hand.** Every one pointed at a
command or prompt in kanon that is not there — they moved out of here and then
out of kanon — and `check_links` cannot see any of them, because it skips
everything beginning with `http`. dokimasia asked for exactly this check on
2026-08-31 and it is still declined: it would be a new obligation, so it is a
contract 2 candidate, and unpinned it would turn every member red for a rename
here. **Ten of theirs, then eight of ours, is the argument for it and does not
change the answer.**

**What was taken from other trees.** kanon's *Adding a check*, offered in their
`D10` and now in [`maintenance.md`](maintenance.md). dokimasia's reading of a
postmortem summary, which was right where ours was wrong. dokimasia's `SIG` facet,
cited in [`notes.md`](../anoieu_analyzer/notes.md) as the emitter half of the `src/proof/eo/` seam —
which closes the question of who builds that check with the answer *they did*.
eudaimonia's two positions on what may be taken from work a tool does not own,
appended to the reporting policy as *What we
take*. **None of it was ours and all of it was offered.**

**Ten topics were removed from [`discussion.md`](discussion.md)** — `D1`, `D3`,
`D6`, `D7`, `D8`, `D12`, `D13`, `D19`, `D23` and `D28` — each on evidence in the
tree that answered it rather than on elapsed time. Four were answered in one
topic by dokimasia, one by epikrisis, one by kanon, and three were settled by
their subject having moved: a register that no longer exists, a check koine
built, and a correction koine carried.

**And the trees moved while this was being written**, which is koine's `D10`
happening to the work of answering koine's `D10`. Seven of the eight discussion
files on this machine were edited between the first read and the last; one
repository's was untracked at the moment it was answered. Every reply says what
it was read against and on what date, which is the remedy koine asked for, applied
by hand because the rule that would have asked for it is with the maintainer.

### Two checks were grading members against rules the shared policy had removed — 2026-09-21

**The same defect twice more, and the shared policy's own coverage page had named
one of them before we did.** Both are the shape `D38` identified in the `report/`
convention: our checker publishing, on every member's tree, a requirement that is
in no shared page.

| what it demanded | where the policy stands now | what it is |
| --- | --- | --- |
| a child project that runs in the parent's CI, is named by the parent's code, or appears on its front page had to claim an **exception** in its charter | isolation is optional, advertising is the **default**, and integration with the parent requires "neither an exception nor promotion" | **retired in place.** A blocking check, so this could have failed a compliant tree |
| every discussion file had to carry *a prompt may not be for this repository* | kanon removed it on 2026-09-20 as an internal operational instruction, abandoned making it fatal, and said the implementation was ours | **narrowed to this tree.** Advisory, so it published a finding rather than a failure |

**The cost of the first is countable and is the reason this is written down.**
Eight children across this ecosystem — in dokimasia, eudaimonia, eunoia, kanon
and tachyon — carry a sentence claiming an exception, and **not one of them needed
to**: they wrote it because a check asked, and the check was reading a rule that
had been replaced. A requirement the policy no longer states cannot be an
obligation of contract 1 either, so removing it is a fix rather than a relaxation;
the regression case is a child that does all three things with a charter
mentioning none of them.

**The second was narrowed rather than deleted, because the rule earned its keep.**
It has fired twice in opposite directions, so this repository still holds itself to
it — and grades nobody else. Ten members carry the paragraph today and none was
obliged to; none loses it by our stopping.

**And `contract 1` promises three things, of which the snapshot compared two.**
Requirements, severity and **applicability** are what the contract fixes; the
registry recorded the blocking and advisory lists and nothing about where a check
runs, so narrowing one to this tree — or the widening the contract actually
forbids — was invisible to the suite. Applicability is recorded per check now, and
a change to it is a test failure. Found by making the change above and asking what
would have caught it.

**One more surface now says only true things.** The list of rules with no
automated check is printed on every run in every member repository, which makes it
the most widely published prose here; two of its lines named a test function that
did not exist, and three named a child-project rule by wording the policy had
since replaced. Every path and `snake_case` name in it is compared with the tree
now. **A coverage reason is a claim about this tree like any other**, and this one
carries the authority of something that executes.

**Four topics were removed from [`discussion.md`](discussion.md)** — `D37`, `D38`,
`D39`, `D40` — each answered rather than gone quiet, with the lasting part written
where it belongs first: the two contract decisions on the
[contract page](../policy_check/README.md), and koine's price for the coverage
query in [`maintenance.md`](maintenance.md). `D33` went with them: it existed as
the evidence for a decision a person had to make, and kanon made it — the rule was
withdrawn and the proposal abandoned, which is an answer and not a silence.
**`D38`'s answer carried a correction of ours worth keeping**: the `report/`
convention did *not* fail to survive the handoff, as we said it had. It survived
intact and kanon deleted it the next morning in a simplification pass. Ours was
the more flattering account of the two and it was wrong.

## What a run learned about itself

*What working a window taught us about how we work*, as against what it taught us
about a check — that half is [`experience.md`](experience.md), which records only
what passed between this repository and somebody else. A window turns up facts
about our own tooling that belong to no pull request and fit in no episode there.
Newest first, one line each; an empty section is the honest state when a run
turned up nothing.

**2026-09-21 — windows
[cvc5 `aee874240419..c2cc3caf7841`](https://github.com/cvc5/cvc5/compare/aee874240419...c2cc3caf7841),
[logos `c8165b2afd32..3acc3b90c4be`](https://github.com/cvc5/logos/compare/c8165b2afd32...3acc3b90c4be).**

- **Thirty-five of the cvc5 window's forty commits had already been measured.**
  The baseline is the open row's `found_at`, `aee874240419` of 2026-08-29, but
  `config/deps.lock` records cvc5 measured at `dbf176dfb71b` on 2026-09-19 —
  the thirty-fifth commit of this window, and the run that set `last_seen` on
  that row. The check fired there, so nothing up to it can have made the claim
  false, and both of the window's two `proofs/eo` commits stand before it. The
  five commits actually unread touch no signature at all. A baseline taken from
  a row's first sighting is right about what it is a window of and is not the
  narrowest one available; `last_seen` and the lock together name that.
- **The pass that found the fix could not close it, and nearly could not close
  it at all.** logos merged [#467](https://github.com/cvc5/logos/pull/467) — its
  whole body is *"Found by anoieu."* — inside this window, but `FUZ0001` is a
  claim about what a binary does, so reading the diff settled nothing and the row
  closed only once the checkers were rebuilt mid-run. The `logos` on `PATH` when
  the window was read had been built on 2026-08-21, a month before the fix and
  ten days before the commit of `E1`; a replay against it would have reproduced
  the original accept and read as a fix that did not work. A recorded `outcomes`
  entry names the checker and what it printed and not the revision that printed
  it, so nothing in the database would have caught the stale binary.

**2026-09-19 — windows
[cvc5 `aee874240419..dbf176dfb71b`](https://github.com/cvc5/cvc5/compare/aee874240419...dbf176dfb71b),
[ethos `6beeb8e6..04a9b4d41508`](https://github.com/cvc5/ethos/compare/6beeb8e6...04a9b4d41508),
[logos `7ff136bb..c8165b2afd32`](https://github.com/ajreynol/logos/compare/7ff136bb...c8165b2afd32).**

- **Our own closure prompt sent the run to the wrong files.** Both
  `prompts/close_bug_db` and `bug_db/README.md` still directed a closure into the
  findings ledgers that had been deprecated the day before, so the run wrote
  those two files before being corrected. Both pages were rewritten on the same
  day and now describe the convention that ships: closure fields on the database
  entry, plus a section above. The general shape is that a workflow retired in
  one place keeps directing work from another until something compares them.
- **Every ethos observation is measured against a branch `main` does not
  contain.** The recorded baseline `6beeb8e6` is on `ethosEoc3`, 1344 commits off
  a merge-base of `8709609e4fad`, with seven commits of `main`'s own since. So
  the ethos half of the database can be neither closed nor refuted by reading
  `main` — the compare view says `diverged` rather than `ahead` if anybody looks.
  Thirteen observations are pinned that way. `config/deps.json` has since dropped
  the exception and watches `main`; moving the measurement takes a run, and
  `config/deps.lock` still records the branch it was measured on.
- **A closure was invisible in the browsing view.** The `bugs.md` generator
  rendered no `closed_*` field, so twenty-five closures changed the database and
  not one byte of the page readers are pointed at, which was *current* by
  `--check` the whole time. Both rendered views carry a status column as of
  2026-09-19, and the counts now say how many rows are open.
- **Eighteen rows waited three months on a convention, not on a disagreement.**
  cvc5 had accepted the documentation findings and deferred them pending a
  decision about whether a program's *pattern variables* count as documented
  arguments. When the decision came it went the way the check already read. The
  blocker was never whether the rows were right.
- **A reply is not evidence, and this is the second time that has cost us.**
  Four `EO0031` rows sat open for three months after a maintainer said they were
  fixed, because nobody re-read the tree; three `EO0064` rows sat *closed* for
  three months on a fix that never landed, for the same reason in the other
  direction. One commit-first pass settled both.

### Salvaged from the retired postmortem log

> [!NOTE]
> **The two rounds below were worked through a reporting workflow that no longer
> exists**, along with everything they name: the two findings ledgers, the
> `TRIAGE:` / `HUMAN RESPONSE:` reply shape, the `awaiting landing:` marker and
> the audit that read it, and the `check_anoieu` and `process_anoieu` prompts.
> They were a round of *correspondence* — rows sent to a project, a reply worked
> back here — which is not what a closure run does now. They are kept because
> the lessons outlived the machinery, and several of them are why the current
> arrangement is what it is. **Read them for what was learned, not for how
> anything works today.**

**2026-08-31 — ethos: nineteen rows, seven fixes, and a decline nobody signed.**
Seven were real and fixed on one commit, two were our own error, eight were
declined and two left undecided.

- **A check that resolves a name must resolve it in the scope that binds it**,
  and a flat symbol table makes the wrong answer the easy one. Two rows read a
  program's own `cons` *parameter* against a `:right-assoc-nil` `cons` declared
  by the file that includes it. `_walk_pattern` had the parameter list in hand
  and never asked it. Narrowing one call site did not fix the class: every other
  check that resolves a head through `resolve_decl` still has the hole.
- **The two triage outcomes are not symmetric, and the process was built as
  though they were.** Ten declined rows were all correct on the merits and none
  had been put to the maintainer in a way he could disagree with. A proposed
  *fix* cannot fail this way — somebody reads a diff. A proposed *decline* asks
  for nothing and gets it.
- **Read the branch, not the sentence.** The reply's header said its changes
  were uncommitted; the branch carried a commit and the tree was clean. It cost
  nothing that time because the error ran in the safe direction. It will not
  always.
- **The sentence that decides what *fixed* means belongs on the page a reader
  lands on**, not one link further in. That ethos aborts on ordinary errors too
  — so how a checker exits is not the finding — was load-bearing for three `FUZ`
  verdicts and was two hops from the report.
- **A finding can be true of the file and false about what the file is**, and
  the second half is the one a maintainer reads first. Four of the nineteen rows
  told an include fragment it was a signature. The judgement was right; the noun
  was not.
- **A shortcut traded for tempo is fine to take and not fine to forget**, and
  the difference is whether something mechanical is left behind that will
  notice. Closing before a change landed was the *fixed upstream* mistake
  adopted deliberately, so it got a marker, an audit and a test. That machinery
  is gone; the debt it tracked is now `awaiting_landing` on the database entry.

**2026-08-31 — logos: the first full sweep.** Two of twenty were real defects,
two were correctly declined, and sixteen were misfiled against a file logos only
vendors.

- **We shipped a hypothesis inside the same record as a measurement, with
  nothing marking which was which.** A promoted reproducer carried a note
  blaming a missing `_`; ethos had been refusing two lines earlier the whole
  time, on the file's own unmutated text, and our shrinker had made the cut the
  note described. Their agent disbelieved the note and was right. Bucketing also
  strips line numbers — correct for deciding whether two findings are one, wrong
  for what a reader is shown.
- **A closed row's *reason* is a claim about the world that nothing rechecks.**
  Re-measuring re-derives open rows only, so a wrong verdict and a live finding
  can coexist indefinitely with nothing going red. Three rows recorded as *fixed
  upstream* had never been fixed, and it was the assistant at the far end that
  caught it. A verdict this repository can settle by itself should never be
  recorded without doing so.
- **The cross-reference field was the highest-value one and was empty.** Twelve
  of sixteen rows were already ruled on against cvc5, twenty lines down the same
  document, and the far end found that only after fetching cvc5 three times and
  matching premise text by hand. It was computable here. Rows may share a cause,
  and saying so is most of the value.
- **"Fixed on branch X" is worth nothing until somebody looks at X**, and the
  looking takes ten seconds. The branch named in that reply was `main` with no
  commits of its own, and the fix was an uncommitted edit in one working tree.
  This is the case the commit-first rule exists for.

**The standing rules that log produced.** Four still bind and are why closure
works the way it does: *read the branch, not the reply*; *absence closes
nothing*; *a decline needs an explicit signature*; *a shortcut leaves something
mechanical behind that will notice*. The rest governed a correspondence loop
that no longer runs — the outbound prompt's feedback field, the reply shape, and
the rule that a person approves every prompt change — and went with it.
