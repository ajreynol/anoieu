# Proposals

Ideas that might deserve a repository of their own, audited here, one section
each. Newest first.

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

Whoever builds it may reject all five. It is their repository.

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

1. **A person creates the repository.** Empty. Nothing here does this, and no
   name is claimed until it is done.
2. **Its owner decides what it is.** `init_eo` is offered as a starting point —
   it takes a name and writes a README saying what the tool is for, and complies
   with nothing else — but the scope is theirs. So is rejecting all five names.
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
