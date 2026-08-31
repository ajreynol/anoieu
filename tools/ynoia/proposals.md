# Proposals

Ideas that might deserve a repository of their own, audited here, one section
each. Newest first.

Work that wants doing but not a repository of its own is
[`requests.md`](requests.md), which tracks where it would live instead. A
request that turns out to need its own tree is promoted here; a proposal that
turns out not to is sent there.

Every proposal opens with the same five lines, because what a person is being
asked is short and should not have to be extracted from an argument:

**Names:** the code names proposed, best first
**What:** one line
**Verdict:** needed | welcome | not yet | no
**If approved:** the first three steps
**Decided:** open, or who decided and when

**The verdict is about us, not about the tool.** A proposed tool is an
independent thing whose owner decides what it is and whether it ever joins this
ecosystem, and no audit here binds any of that. What this page decides is
whether **we** want to depend on it:

| verdict | means |
| --- | --- |
| **needed** | the ecosystem will take a dependency on it. We want it built and we intend to use it |
| **welcome** | worth building, and we are not depending on it. *Go and do it* — nothing here waits on you and nothing here breaks if it never appears |
| **not yet** | the thing it would fix is not a problem yet. Says what would change that |
| **no** | the argument does not hold |

The distinction that matters is between the first two, because they cost the
builder different things. *Needed* means somebody will be waiting, which is a
reason to build it and also an obligation nobody has agreed to. *Welcome* is a
smaller and often kinder answer: build it for your own reasons, on your own
schedule, and if it turns out well we will come to you.

**Nothing on this page approves anything.** A proposal is a claim on a name in a
shared namespace and on somebody's attention for years, and the policy reserves
that decision for a person. What this page produces is an argument with a
recommendation at the end, written so that agreeing or disagreeing with it takes
a minute rather than an afternoon.

This is the third thing ynoia does. The account asks whether the ecosystem's
arrangement earns its machinery; the register keeps the names; and this audits
the specific question *should this become a repository*, which is the same
question the account asks in general, applied to one case with a decision
attached.

## The standard

Four questions, in order. A proposal that fails an early one does not need the
later ones answered.

1. **Does it exist anywhere yet?** Code that has been written twice is evidence;
   code that has been written once is a design, and a design does not need a
   repository. The strongest signal available is two implementations that turned
   out identical, because that is a fact rather than a prediction.
2. **How many consumers, really?** Two is the number at which sharing looks
   obviously right and usually is not: the second consumer is the one that
   discovers what is actually shared, and a third is what shows whether the
   answer generalises or was a coincidence between two.
3. **What does a repository buy that `tools/` in an existing one does not?**
   Isolation, a release surface, an independent maintainer. Each is real and
   each is also a cost. The ecosystem already has a mechanism for sharing code —
   a member pins a commit and fetches — so the question is never *how would
   anyone get it* but *what breaks if it lives in somebody's tree*.
4. **Who maintains it when the enthusiasm is gone?** A repository is a standing
   obligation. If the answer is "whoever needs it next", the proposal is for a
   directory, not a repository.

**Two-consumers is not automatically a refusal**, and reading it that way is the
mistake this standard made on its first use. The count matters when the shared
*format* is still being discovered. It matters much less when the thing is
plainly needed by every future member, and it points the other way entirely when
the alternative is one repository hosting everyone else's shared machinery —
that makes its owner the de facto maintainer of everybody's, which is a larger
commitment than a separate repository, not a smaller one. Ask who ends up
holding it, not only how many use it.

The likeliest right answer is often **not yet, and here is what would change
that** — a threshold somebody can watch for rather than a refusal. It is not the
default answer, and a standard that reaches it every time is a standard that has
stopped being applied.

## P2 — the ecosystem's governance, out of the analyzer

**Names:** **`kanon`**, then `thesmos`, `epistates`, `oikonomia`
**What:** the policy every member is checked against, the checker that decides
it, the inventory of who is in, and the scripts that start, welcome, join and
install a tool — in a repository that is not also the tool that files findings
against you
**Verdict:** **needed** — the ecosystem already depends on this; the question is
whose tree it lives in
**If approved:** a person creates the empty repository → the policy, its checker,
the inventory and the `*_eo` scripts move there in one commit, with anoieu
becoming a consumer of them → every member's CI pin changes once, at a moment
somebody chose
**Decided:** **open.** Raised by the maintainer on 2026-08-31, who is inclined to
do it, and **deliberately not actionable until they raise it again**. Audited
here so that the argument exists before the decision does, which is the only
thing this page is for.

### The names

None is taken. A name is claimed when a person approves one, so nothing here
touches [`names.md`](names.md).

| name | Greek | the claim it makes | the objection to it |
| --- | --- | --- | --- |
| **kanon** | κανών, *the measuring rod* — the standard a thing is held against | the policy is exactly a rod: `policy_check.py` lays it alongside a tree and reports where the tree is short. It names the instrument rather than the authority, which is what this actually is | *canon* in English is about scripture and lists of approved works, and a governance repository is the one place that misreading does real harm |
| **thesmos** | θεσμός, *a thing laid down* — an institution before it is a law | it is the arrangement itself, written down: what a repository is, what a member owes, what a child project may do | heavier than the thing. A `thesmos` sounds founding and permanent, and this is a policy somebody amends on a Tuesday |
| **epistates** | ἐπιστάτης, the presiding member of the council, for one day | presides and does not rule: it runs the meeting, and the decisions stay with people. That is precisely the relationship the policy has to members | needs the footnote to land at all, which by the register's own test means it is not following the convention |
| **oikonomia** | οἰκονομία, *management of the house* | the unglamorous half is true: the inventory, the checkouts, who lives where | *economy* in English, and it says nothing about the rules, which are the part that matters |

**Recommended: `kanon`.** The register asks for a word for what the tool does to
its subject, and what this one does is *measure a tree against a stated
standard*. The objection is real and worth stating on the repository's own front
page: this is a rod, not a canon, and nothing in it is scripture.

### The proposal

anoieu is currently three things, and its own README says so: an analyzer, a
reporting system, and *the place the Eunoia ecosystem's shared policy is kept*.
The third has grown since that sentence was written. It is now
[`docs/policy.md`](../../docs/policy.md),
[`tools/policy_check.py`](../../tools/policy_check.py) — which runs in every
member's CI — [`tools/ecosystem.json`](../../tools/ecosystem.json),
[`tools/ecosystem.py`](../../tools/ecosystem.py),
[`scripts/init_eo`](../../scripts/init_eo),
[`scripts/join_eo`](../../scripts/join_eo),
[`scripts/check_join_eo`](../../scripts/check_join_eo),
[`scripts/welcome_eo`](../../scripts/welcome_eo),
[`scripts/global_audit`](../../scripts/global_audit),
[`scripts/install_eo`](../../scripts/install_eo) and
[`tools/checkouts.json`](../../tools/checkouts.json). That is a tool, and it is
not the analyzer.

The argument is not that the machinery is bad. It is that **one repository both
writes the rules a member is judged by and files the findings against them.** A
member that disputes a finding is disputing with the body that also defines what
compliance is, and the only thing separating those two roles today is that the
same people are careful. Separation is cheap now and expensive later.

### Against the standard

*Does it exist anywhere yet?* Yes — once, and **running in other repositories'
CI**, which is a third kind of evidence the standard does not have a line for.
Written twice means the shared shape has been discovered. Written once but
*consumed by four trees under a contract* means something stronger: the
dependency is already real, and the only open question is whose release surface
it rides on.

*How many consumers, really?* Four today — anoieu, eudaimonia, dokimasia, koine —
and every future member, by construction: joining *is* running this checker. The
count that matters here is not how many use it but how many pin **anoieu** to get
it, which is the same four, and each new member makes the move more expensive.

*What does a repository buy that `tools/` does not?* Three things, and the first
is the whole proposal. **The judge stops being the prosecutor.** Then: a release
surface that does not move when a check is added to the analyzer — today a member
pinning the policy pins a repository whose commits are mostly about `.eo`
parsing. And it lets anoieu's front page say one thing.

*Who maintains it when the enthusiasm is gone?* The honest risk is *anoieu under
another name*, which is what sank the first audit of `P1` and would sink this
one. Two things argue against it here. The artifact is documents plus one
checker with no dependencies, which is the lowest-maintenance shape anything in
this ecosystem has. And the work is mostly **refusal** — saying no to rules that
have not been run against a real tree — which is a job somebody can do in an
afternoon a month, or not at all, without the thing rotting.

### What the standard is missing, and this proposal needs

Every question above assumes a tool being *built*. This is a **transfer**, and a
transfer asks two more:

5. **What does the losing repository keep?** Here: the analyzer, the fuzzer, the
   findings ledger, and the reporting workflow. The line to argue is
   [`reporting-policy.md`](../../docs/reports/reporting-policy.md), which is a
   position shared with dokimasia about what may be published — governance by
   any reading, and also the document anoieu most needs to own, since it is the
   one constraining anoieu's own behaviour. **Recommendation: it stays**, and the
   governance repository holds what a repository *is*, not what a report may say.
6. **Is either half left unable to answer a question it used to answer alone?**
   One: *does this finding's project comply?* — today one tree holds both the
   finding and the checker. After a split, `global_audit` lives with the policy
   and the findings live with the analyzer, and the audit that reads across both
   needs two checkouts. `install_eo` already makes that a one-line problem, which
   is an argument for doing this **after** the install script settles, not
   before.

The standard should gain both questions whether or not this proposal is
approved. A page that audits *should this be a repository* and has no vocabulary
for *should this move* will keep producing confident answers to a question
nobody asked.

### If approved

1. **A person creates the repository, empty.** Nothing here can: repository
   creation carries credentials and a runner. No name is claimed until it is
   done.
2. **The move is one commit, not a migration.** The files above, their tests, and
   the parts of `tests/run.py` that check them. Anything left behind in anoieu
   that mentions the policy becomes a link.
3. **anoieu becomes a consumer, and is checked by a policy it no longer owns.**
   That is the forcing function the whole proposal rests on: the first rule that
   cannot survive being applied to its former author is the first rule that
   should not have been written.
4. **Every member's pin moves once.** The CI snippet in `policy.md` fetches a
   URL; it changes, and each member changes it at a moment they choose. This is
   the cost, it is real, and it grows with the member count — which is the
   argument for doing it while there are four.

### The risk worth writing down

A policy separated from the tree it was written for can drift into rules nobody
has run against a real repository — which is the failure the current arrangement
structurally cannot have, because the policy's author is also its first victim.
The mitigation is that the checker moves *with* the policy and anoieu stays a
consumer, so every rule is still run against at least one tree that did not write
it. If the governance repository ever ships a rule with no checkout behind it,
this proposal was wrong.

## P1 — central tooling for reporting

**Name:** **`koine`** — chosen, and now taken in [`names.md`](names.md)
**What:** the shared machinery of the reporting loop, fetched by every tool that
runs one, so the protocol has one implementation instead of one per member
**Verdict:** **needed** — we intend to depend on it
**If approved:** a person creates the empty repository → its owner decides what
it is → joining this ecosystem is their choice, and `init_eo` / `join_eo` are
offered, never required
**Decided:** **approved 2026-08-31** by the maintainer, as `koine`. Proposed by
dokimasia in its `D4`; audited at anoieu `441b562`, revised the same day — see
*What changed* below. The repository does not exist yet; approving it is not
creating it.

### The names

Five candidates, none taken. All are free in [`names.md`](names.md), and a name
is claimed when a person approves one — not when a document suggests it. Each
etymology below is written to be disagreed with, which is the test: if the
sentence explaining a name is a stretch, the scope is what is unclear.

| name | Greek | the claim it makes | the objection to it |
| --- | --- | --- | --- |
| **koine** | κοινή, *the common tongue* — the shared dialect that let people who spoke differently understand each other | the tool is a shared language between tools, which is exactly what a fixed reply format is | the strongest metaphor and the least literal. It says nothing about *reporting*, and a reader may take it as "the common one" |
| **angelia** | ἀγγελία, *the message* — not ἄγγελος, the one who carries it | it fixes the form of what passes between tools and never decides what is sent | close to *angel* in English, which is a distraction it never quite escapes |
| **homologia** | ὁμολογία, *saying the same thing* | two implementations agreeing is the whole purpose, and the drift check is literally this | describes the test rather than the tool; if the shared code grows past checking, the name stops fitting |
| **paradosis** | παράδοσις, *a handing over* | a finding handed to whoever owns it, which is the act the loop exists to perform | also means *tradition*, and a tool named for handing things down sounds like it decides what is handed |
| **typos** | τύπος, *the stamp that shapes* — hence a pattern | the tool is the mould the reply format is pressed from | reads as *type* in English, which is both too transparent for the convention and wrong about what it does |

**Chosen: `koine`.** The argument for it is that the thing actually being shared is
not code — it is the format two tools must both speak in order to be understood,
and the code follows from that. The argument against is the honest one in the
table: it is a name about *communication in general* attached to a tool about
reporting in particular.

**The name is ours to decide, and it is decided before the repository exists.**
It comes out of a shared register and a proposal argued here, so it is not a
thing to hand to whoever picks the work up — a name chosen at build time is a
name nobody else can plan around. What is *theirs* is everything after: the
scope, the interface, the pace, and whether the tool ever joins this ecosystem.

### The proposal

anoieu and dokimasia have both built the same loop: a script run in the project a
finding is about, a script run at home once it has replied, prompts defined in a
document, a drift check that the script's copy has not diverged from that
document, and a postmortem with one block per run. dokimasia built theirs in an
afternoon by reading ours.

What is shared is already identified rather than guessed at: the drift check,
around sixty lines and a copy in one direction; the reply-file finder and the
branch-state reporter, which are pure git and identical; and the reply format,
fixed by prose both sides already follow. What is not shared is equally clear —
the prompts, because the subjects differ, and what settles a row, which each tool
names for itself.

### Against the standard

*Does it exist?* Yes, twice, which is the strongest form of the evidence.

*How many consumers?* Two today, and **every future member**. This is a loop the
policy asks every tool in the ecosystem to run; a third consumer is not a
possibility to wait for but the next repository that joins.

*What does a repository buy?* The decisive answer, and the one the first audit
got backwards. The alternative is anoieu's `tools/`, which makes **anoieu the
maintainer of everybody's reporting machinery** — a standing obligation to every
member, taken on by the repository that has just finished writing down that it
will not sign maintenance contracts it cannot keep. A separate repository is the
*smaller* commitment for anoieu, not the larger one: it can have its own
maintainer, its own pace, and it can be retired without touching the analyzer.
It also stops anoieu's release surface from being two things wearing one name.

*Who maintains it?* Open, and the question a person should settle before
approving. If the honest answer is *anoieu, under another name*, then this is a
directory after all and the first audit was right. If it is somebody else, then
it is their tool, and the strongest form of this recommendation is the one that
leaves them free: we are saying we would use it, not that they owe it to us.

### If approved

1. **A person creates the repository on GitHub, by hand.** Empty. Nothing here
   does this and nothing here can: repository creation carries account
   credentials and a runner, so it is a security boundary rather than a
   convention. No name is claimed until it is done.
2. **Its owner decides what it is.** `init_eo` is offered as a starting point —
   it takes a name and writes a README saying what the tool is for, and complies
   with nothing else. The **scope is theirs**; the name is not, and `init_eo` is
   written to take it from the register rather than invite one.
3. **Joining this ecosystem is their choice, later or never.** `join_eo` exists
   when they want it. A tool we depend on is not thereby a member, and we can
   pin a commit of a repository that has never adopted a line of our policy.

Then the contents, if the owner agrees, in dokimasia's order and on dokimasia's
test — *share only
where two implementations turned out identical*, applied per piece: the
prompt-drift check first, because it is the piece guaranteed to rot (it exists to
catch divergence, and two copies of it will produce exactly that), then the
branch-state reporter, then the reply finder. Consumers pin it the way they pin
anoieu.

**Not in scope at the start:** a shared register format or shared issue
management. anoieu's is generated and dokimasia's is curated, dokimasia says two
of its slots are weak, and fixing a format now would fix it before either side
has evidence that theirs is right. Let the prose converge first.

### What the builder inherits

Not a specification — the scope is theirs — but the two implementations exist and
should not be rediscovered. In anoieu, at the commit this was audited:

- `tests/run.py`, `prompts_agree()` — pulls the fenced prompt out of the document
  that defines it, resolves the `-- or, ... --` alternatives, runs the script with
  `--show-prompt`, and diffs. This is the sixty lines both repositories now carry.
- `tests/run.py`, `join_prompt_agrees()` — the same idea in its simplest possible
  form, for a prompt with no substitutions. Worth reading first.
- `scripts/check_anoieu` and `scripts/process_anoieu` — the two halves of the
  loop, and where the reply format is actually emitted.
- `docs/reports/reporting-workflow.md` — the prose the scripts are checked
  against, and the document that already draws the line between what is shared
  and what is not.

In dokimasia: `scripts/check_dokimasia`, `scripts/process_dokimasia`, and their
`workflows.md`. Theirs was written by reading ours, so the *differences* are the
interesting part — they carry a fourth triage label, `answered`, for a row that
is a question and names no branch, which ours cannot express.

### Still open, and approved anyway

**Who maintains it.** The audit named this as the question to settle before
approving, and the approval came without it settled. That is a person's call to
have made and it is recorded here rather than smoothed over: if the answer turns
out to be *anoieu under another name*, this is a directory with extra ceremony
and the first audit was right. If it is somebody else, the recommendation stands
in its strongest form — we would use it, and they owe it to nobody.

**Its interface.** How a consumer fetches and calls the shared check is not
specified here, deliberately: it is the owner's to design, and a proposal that
arrived with an interface attached would be a specification wearing a
recommendation's clothes.

### What changed, and why

The first audit of this proposal recommended **not yet**, on the grounds that two
consumers cannot distinguish what is shared from what one of them wrote first,
and that the pin-and-fetch mechanism already reaches a member without a new
repository. Both remain true and neither is decisive, which the audit missed by
counting consumers instead of asking who ends up holding the thing. The
correction is recorded here rather than made silently, and the standard above has
been amended so it does not produce the same answer next time.
