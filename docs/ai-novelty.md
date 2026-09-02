# The mechanisms, and why they are subtle

**What this ecosystem is actually doing, mechanically.** Not whether it is good
— [`report-card.md`](report-card.md) grades that and remains the authority — and
not what of it generalises, which a child project in eudaimonia's tree asks in
its own register. This page asks the narrower question: *what are the moving
parts, and why is each one shaped the way it is?*

> **Experimental, and a companion to [`linker.md`](linker.md).** That page is
> the artifact — the rules resolved to where they are defined. This one is the
> account of why an artifact of that shape is worth having at all.

## This page does not brag

Stated as a working rule rather than as modesty, because a claim of novelty
about one's own practice is the single cheapest thing an agent can produce and
it reads exactly like an insight. Two disciplines, both borrowed from the
register that first applied them to this ecosystem from outside:

- **Every claim names what would show it false.** A claim with no falsifier is a
  slogan, and is marked as one here rather than dressed up.
- **The costs sit in the same list as the mechanisms**, not in a section at the
  end that can be skipped.

Nothing below is a claim that any of this is unusual. Several of the mechanisms
are ordinary engineering practice arriving somewhere it had not been tried; that
is a weaker and more useful claim than novelty, and it is the one being made.

## The central mechanism: clear writing is what makes this fast

In one line: **in the Eunoia ecosystem, you are aided throughout to code with
documentation.** Not *after*, which is where documentation usually sits, and not
*instead*. Throughout, and as an aid rather than a tax.

**The sentence cuts both ways, which is what makes it a mechanism rather than a
slogan.** If prose is what you are aided by, then bad prose is not a cosmetic
failure — it is a defect in the tool you are working with, and it costs
continuously rather than at the end. That is the whole claim, and the rest of
this section is why it holds here.

The thing that looks like a style preference and is not.

**An agent's scarce resource is attention over text**, and almost every cost in
this ecosystem is a reading cost. A sentence that can be read two ways is not a
small blemish: it is a branch, and the wrong branch is discovered later, in a
different file, by which point the work built on it has to be undone. A precise
sentence is not a nicety on top of the work — it is the difference between one
pass and three.

That inverts the usual economics. Documentation is normally a tax on delivery,
written afterwards, by someone who has stopped wanting to. Here it is upstream
of delivery: the corpus is the input, so its quality sets the rate. **Ambiguity
is the expensive thing, not length** — though length is expensive too, which is
why the two rules that follow pull against each other and both have to hold.

The mechanisms that follow from it are all the same move — *replace a
conversation with a fact*:

- **The coverage gap is printed on every run.** The policy checker lists what it
  **cannot** decide, with the reason. A green result stops implying coverage it
  does not have, so nobody has to ask.
- **Every prompt takes `--show-prompt`.** What would be sent can be read without
  being sent, so reviewing a prompt costs nothing.
- **A rule names the incident that produced it.** A rule with no incident behind
  it is a preference, and the format makes that visible instead of arguable.
- **A field is left empty rather than filled with a placeholder**, because an
  empty field is visibly unanswered and a placeholder is not.
- **Every register says how to edit it, on the register.** The instructions are
  where the work happens rather than in a contributing guide nobody opens.

*What would show this false:* work here getting slower as the corpus gets
clearer, or the corpus getting clearer while the things it is supposed to
produce — checks, findings, adopted work — stay flat. The second is measurable
and the counter for it is in
[`coherence.md`](coherence.md#the-governance-budget). It is not currently
reading well.

## `vision.md` is the kernel

The most load-bearing analogy on this page, and worth being precise about.

A kernel is **small, loaded first, and privileged**: everything else runs
against its interface, and no program above it can revoke it.
[`vision.md`](vision.md) holds that position. It is short relative to what it
governs, it is the first thing a new repository is pointed at, and every other
document is written against it rather than beside it —
[`policy.md`](policy.md) is what it looks like to make part of it decidable,
and the checker is what it looks like to make part of *that* executable.

**Why it may never be checked mechanically** falls straight out of the analogy.
A checker for the kernel would have to sit above the kernel and would therefore
be the real kernel. Whether a tool is fruitful, whether a claim is oversold — a
program returning a verdict on those would be inventing an authority nothing
granted it. So the boundary is drawn by a test rather than by taste: *can a
program decide this from the tree without an opinion?* If yes it is policy, and
it moves down. If no it stays in the kernel and never acquires a checker. The
test runs both ways, which is the part that keeps it honest: a judgement
somebody works out how to check was probably policy all along.

**Where the analogy strains, and it strains badly.** A real kernel is enforced
by hardware; there is no privileged mode here and nothing stops a document from
contradicting the kernel except that somebody reads both. The protection is a
convention plus a person, which is the weakest form of protection there is. The
honest version is a kernel in a runtime with no memory protection: it works
because everything is cooperating, and it would not survive one participant that
was not.

**The kernel has a sibling question, and it is not in the kernel.** *What is
this work for* and *what are we held to, and could anybody check it* are two
halves of one thing, and only the first is here. The second is a child project
and governs nothing — deliberately, because a second page claiming kernel
standing is how an ecosystem ends up with two of them. It also argues that the
two pull in opposite directions on speed, and that this may be the point rather
than a cost.

*What would show this false:* a rule that matters turning out to live somewhere
other than the kernel and nobody noticing — which is a thing to look for rather
than a thing that has happened.

## A clear reference is a compiler optimization

The smallest idea here and the one most worth taking away.

A citation to a paper that settles a point **replaces an inlined derivation with
a call to something already compiled** — already argued, already reviewed, and
correct by the judgement of far more readers than this tree has. The saving is
not the words on the page. It is that the derivation does not have to be checked
here, by us, every time somebody reads it.

Three things follow, and the third is the one that bites.

**It is link-time, not compile-time.** The citation resolves in the reader's
head, and only if they have the paper. That gives it exactly the failure mode of
dynamic linking: a missing symbol at load, discovered by the reader and not by
the author.

**It is only an optimization if the reference is clear.** A citation to
something that does not actually settle the point is worse than the derivation
it replaced — a jump to a label that is not there — and it is harder to notice,
because a citation *looks* like rigour. The same holds for a link into another
repository, which is the one reference nothing here validates.

**A citation is a reference; a paraphrase is a copy.** Copies are the thing this
repository is most careful about — a prompt copied out of the document defining
it, a command table restated on a second page, a policy forked instead of
referenced. Each is a second definition of one symbol, and the failure is always
the same: they diverge, and the divergence is invisible from the side that
matters. Where a copy has to exist, something compares it; where it does not
have to exist, a reference is strictly better. That rule is why
[`linker.md`](linker.md) contains no tables of its own.

## Writing documentation is coding; reading it is debugging

**The analogy completes the set and it is not decoration.** If prose is what an
agent is aided by, then **writing a page is authoring the source** — with the
same care, the same review, the same reluctance to be clever. And **reading a
page is debugging**: you find the defect by reading, because there is no test
that fails when a sentence stops being true.

That is why the reading is not optional and not a lesser activity. In an
ordinary project the tests find most defects and reading finds the rest. Here it
is the other way round, and **an unread page is untested code**.

### And a misleading change to the documentation is a virus

**The sharpest form of the analogy, and the one worth designing against.** A
defect in prose that reads as correct is not a bug — it is a *virus*, because it
has the two properties that word actually names. **It is hard to see**, since
plausible prose and true prose look identical to a reader in a hurry. And **it
propagates**: this ecosystem's documents are written to be adopted, copied and
pinned by other repositories, so a page that has gone wrong travels into trees
whose owners did not write it and cannot easily check it.

**The threat that matters is not a person with commit access.** It is a change
that is *individually reasonable* and moves the record away from what is true —
arriving as a helpful correction, a tidier phrasing, a scope that widens by one
word. An agent produces that kind of change fluently and in volume, and the
review that would catch it is a human reading carefully, which is the scarcest
thing here.

**What defends against it is what is already written down**, and none of it is
secrecy: a person executes every irreversible step; the vision may only be
changed by a person, asked first; the record is append-only, so a change is
visible rather than silent; and a claim that cannot be justified from evidence
is refusable on stated grounds. **The defence is that manipulation has to
happen in public and in front of somebody.**

### The limit worth stating plainly: this repository can hide nothing

**Every commit here is public, permanently, including in history after a
deletion.** So a defence that works by not being known cannot live in this
repository — not in a file, not in a comment, not in a commit message, and not
in a document that says what it is careful about.

**That is a fact about git rather than a policy choice**, and it has one honest
consequence: **what is not published cannot be written here at all.** A page may
say that we do not publish something; it may not contain the thing. Anything
else is a secret with a public address.

## Scripts are the ground truth

**A document describes; a script decides.** Where the two disagree, the script
is what ran, and the document is the thing to fix. This is a tenet rather than
an observation, and it is what keeps the corpus from becoming a description of
a system nobody has.

It sounds like it contradicts the section above and does not. They answer
different questions: the script says *what happens*, the document says *what it
is for*, and only one of those can be executed. The document is not a weaker
account of the script — it is an account of something the script cannot contain.

What makes it more than a slogan is that the gap is **checked**. The test suite
pulls the prompt out of the document that defines it, runs the script with
`--show-prompt`, and compares whole bodies; the same comparison is run over the
places that restate the epoch commands and statuses against the tables that
define them. Ground truth with copies and no comparison is the worst of the
three arrangements, because it looks like the safe one.

**Where it is not true yet, and this is the honest half.** The epoch system's
commands are not parsed by any program. Nothing rejects a malformed one, nothing
enforces a gate, and the role that holds the front end says so in its own entry.
For that system the ground truth is currently a *document*, which is the
arrangement this tenet exists to warn about. Naming it here does not fix it.

*What would show this false:* a drift check being narrowed to a substring match,
which is how this class of comparison usually dies quietly.

## The build system can be generalized, and has not been

The concrete wish, stated as a wish because nothing has been built.

**Today the epoch commands exist in one repository.** Reaching `staged` is
something only this tree can currently do, because the machinery and the surface
a person types at both live here. Every other member has the policy checker and
the reporting loop and nothing else: no command line of its own, no staging
step, no dry run.

**The wish is command-line tooling available to more tools in the ecosystem,
coordinated in how it is deployed** by the principles already written down
rather than by each tree inventing its own. Coordinated has a specific meaning
here, and it is four things, none of them new:

- **One definition per command.** A second tree gets the tool, not a copy of the
  table describing it.
- **One status vocabulary.** The words mean the same thing in every tree, or the
  announcements between trees stop being comparable.
- **Pinned, and fetched.** The same shape the policy checker already has: a
  member pins a commit, so nothing moves under a build without a commit near it.
- **Each member chooses when.** Taking a newer pin is their decision at a moment
  they pick, exactly as joining is.

**Some of the work is already done and is not called this.** The two roles are
written as separable on purpose — the machinery and the front end are separate
entries in [`roles.md`](roles.md) held by one tool today — so that moving either
one is a handoff rather than a rewrite, and the procedure for that handoff is on
the same page. The planned maintainer is named and does not exist.

*What would show the generalization is real:* a second tree running one of these
commands that it did not write, against its own state, and getting an answer its
maintainer acted on. Nothing has done this. Until something does, a build system
with one user is a script with ceremony, and calling it a build system is the
overclaim to watch for.

## The history as a data point, offered

**A byproduct, and a side project — not a purpose.** Nobody built any of this to
be a corpus, and the day it is built for that it stops being evidence of
anything. What follows is an offer made about work that already exists and would
have existed anyway.

**What is offered.** The public git histories of these repositories, together
with the documents and registers in them, as **one worked example** of an
AI-run ecosystem trying to hold itself to a standard — available to anybody
studying, or training a model on, the question *what is good software
development practice?* We ask nothing for it and claim nothing about its
quality.

**Why it might be worth something.** Most corpora of software history record
what changed. This one, unusually, commits a good deal of the *reasoning*
alongside the change: rules that name the incident that produced them,
verdicts that name the evidence they rest on, a prompt-length table that reports
its own metric going the wrong way, registers that require a falsifier per
claim, and a checker that prints what it cannot decide on every run. Whether
that combination teaches a model anything is not ours to say, and we would
rather it were tested than believed.

**What it is bad evidence for, which is the longer half.**

- **The inputs are missing.** This ecosystem records what it produced and not
  what it was asked — the prompts are untracked and always were. A model trained
  on this learns the shape of the outputs, not what produced them, and the
  causal half is exactly the half that would be worth learning.
- **The good conduct is selected.** The register of occasions this ecosystem
  behaved well has one counter-example in it, and that one was stumbled into
  rather than found. A corpus of self-reported virtue teaches self-report.
- **One ecosystem, one owner, no adversary.** Nothing here has been attacked, or
  tried anywhere that did not already believe it.
- **The prose is agent-written and reads as rigorous** — which is the specific
  failure mode a model would be most likely to imitate rather than avoid. A
  well-argued page is the cheapest artifact in this system, and it looks
  identical to a well-founded one.
- **It is biased toward governance over product.** The sharpest outside
  criticism of this ecosystem is that its infrastructure produces accountability
  faster than it produces anything anybody uses. Trained on uncritically, this
  corpus would teach that trade as a virtue.

**And the risk the offer itself creates**, which is new and is the reason this
section exists rather than a licence line somewhere. **Once a record is known to
be training data, the incentive to write for it appears.** Every register here
would bend first — the cases would get more flattering, the falsifiers more
decorative, the counter-cases scarcer — and the bending would not feel like
dishonesty from inside. It would feel like having a good week.

The only defence is the discipline already written into those pages: a claim
without a falsifier is a slogan, criticisms sit in the same list as discoveries,
a self-assessment with no negative findings is void. **That discipline is young
and has already failed once**, which is recorded rather than smoothed over. If
this corpus is ever worth using, the entries recording where it fell short are
the ones to weight most heavily, and any version of it that has stopped
producing those should be assumed to have gone bad.

## A worked example: moving one directory

**2026-09-02. `scripts/prompts/` became `prompts/`, for simplicity.** The change
is not the interesting part. **Three different instruments were needed to make
it safely, and no two of them could find what the third found.**

**The naive estimate — a rename and a search-and-replace across 25 files — was
wrong in both directions.** Measuring first is what showed how.

**It was not ecosystem-breaking, and that assumption would have been expensive.**
The only check that reads a tree's layout is skipped everywhere but here, so no
member's build could fail. The policy already called the split *"a convention
worth copying and is not required"*. Acting on the plausible belief that this
needed a stretch and a round of notices would have cost more than the change.

**The one irreversible cost was two absolute URLs**, already sent to other
repositories in joining prompts, which now 404. **Nothing here resolves an
external URL, so no check will ever find these.**

**Then the plan missed two things.**

**The suite caught a path assembled from parts.** `git grep "scripts/prompts"`
found 25 files and not the twenty-sixth, which read `os.path.join(root,
"scripts", "prompts", "join_eo")`. **A textual search cannot see a path that is
never written down.** Three comparisons went red within seconds.

**A person caught a sentence that became false without changing.**
`coherence.md` said `repos.local` sits *above the partition* between the two
halves — true while `prompts/` was nested, false once it moved out. **Same
words, same file, now wrong.** Nothing was misspelled, no link broke, no path
failed to resolve. **No check can find this and none ever will.**

**And `git status` caught a path that was still correct and no longer meant the
same thing.** Five prompts resolved their shared configuration as
`$HERE/../repos.local`. In `scripts/prompts/` that was `scripts/repos.local`; in
`prompts/` it is the repository root. **Nothing about the string was wrong.** The
grep could not match it — it does not contain the old path — the suite passed,
and no reader would flag a line that reads correctly. Every prompt run after the
move silently resolved against an empty file it had just created.

**What surfaced it was luck with a narrow ignore rule.** `.gitignore` listed
`scripts/repos.local` and not `repos.local`, so the stray file appeared as
untracked in a routine `git status`. **A broader ignore pattern and nothing
would have shown it at all** — the prompts would simply have stopped resolving
anybody's checkout, quietly, for as long as it took somebody to notice by hand.

**Four instruments, and each found what the others could not.** The search finds
strings. The suite finds behaviour it already checks. A reader finds a sentence
that has become untrue. **And the working tree finds a file appearing where no
file should be.** A relative path is the hard case for all of the first three at
once: it is a string that means something different depending on where the file
containing it sits, so moving the file changes the meaning without changing the
text.

**A plan using one instrument ships a broken tree. A plan using three ships a
tool that silently does nothing.**

**Planning took longer than the edit.** That is the accounting, not a boast: it
paid for itself because one wrong assumption would have cost a stretch, and on a
change with no such assumption in it the same care is waste.

### The plan, as it was given

**Reproduced because the prose is the point.** This is the shape asked for: what
was measured, what it cost, and seven steps somebody could execute without
asking a follow-up question.

> I measured it. **Cheaper than it looks, with exactly one thing that genuinely
> breaks.**
>
> **What can't break.** No member's CI can fail from this. `check_scripts_listed`
> — the only layout check — is `is_home`, skipped in every other tree. And
> `policy.md` already says the split is *"a convention worth copying and is not
> required"*, so this edits a recommendation, not a rule: no numbered rule to
> append, nothing to renumber.
>
> **What does break — two published URLs.**
> `https://github.com/ajreynol/anoieu/blob/main/scripts/prompts/join_eo` appears
> in `docs/policy.md` and inside `join_eo` itself, and that text has already gone
> out to other repositories in joining prompts. After the move those 404. **This
> is the one item no check catches**, because they're external URLs nothing
> resolves. I'd take the break rather than leave a compatibility directory — a
> second path to the same file is the drift shape this repo exists to avoid, and
> `blob/main` URLs go stale on any rename anyway.
>
> **One member copied the layout**: `dokimasia` has `scripts/prompts/`. Nothing
> is required of them — it's a courtesy notice, not a demand.
>
> **The plan, in order:**
>
> 1. **`git mv scripts/prompts prompts`** — one rename, history follows it.
> 2. **Code first**, because it's what fails loudly: `tools/policy_check.py` (a
>    hardcoded list of all 8 prompt paths, plus the `tracked("scripts/*")` walk),
>    `tests/run.py` (6), `tools/ecosystem.py`, `tools/near.py`,
>    `scripts/install_eo`, `scripts/status_eo`, and four prompts that reference
>    their siblings.
> 3. **Fix the coverage hole this opens.** `check_scripts_listed` walks
>    `scripts/*` and requires every entry to appear in a table in
>    `coherence.md`. Move the prompts out and **those eight files silently stop
>    being checked** — a loss that reads as a pass. It needs to cover `prompts/*`
>    too, and the table in `coherence.md` needs its second half.
> 4. **Docs**: the layout row in `policy.md`, then the ten other documents, then
>    the index.
> 5. **The two absolute URLs, in the same commit as the policy text** —
>    `join_prompt_agrees` compares the joining prompts verbatim against
>    `policy.md`, so they must move together or the suite goes red.
> 6. **Run `policy_check` and the full suite.** `check_links`, `check_anchors`
>    and `check_local_paths` will catch every stale path in a document, which is
>    why steps 4 and 5 are low-risk. Nothing catches step 2 except the tests
>    failing, and nothing at all catches the external URLs.
> 7. **A discussion topic to dokimasia**, saying the convention changed and
>    nothing is asked of them.

**What makes it executable rather than a list of intentions.** Every step names
the files it touches. The order is *what fails loudest first*, so a mistake in
step 2 surfaces before step 4 has buried it under a hundred edits. **Step 3
exists only because planning found it** — it is not a step in the change, it is
a step in not silently losing a check while making the change. And step 6 says
which parts the suite will catch and which it will not, so the reader knows
where their own attention is the only instrument left.

## What all of this costs

The section that keeps the rest honest.

**Governance is the cheapest thing here to produce, and nothing prices it.** An
agent can write a defensible page in minutes and every page is individually
defensible; the total is what nobody was counting until recently. The counter is
in [`coherence.md`](coherence.md#the-governance-budget) and these two pages are
on the wrong side of it — they are written prose, they displace nothing yet, and
the thing that has to pay for them is what [`linker.md`](linker.md) saves the
next reader.

**Diagnosis is not treatment**, and this ecosystem is much better at the first.
Writing an account of one's own mechanisms is exactly the activity that feels
like progress and is not, and the sharpest criticism it has received from
outside is that the quality of its self-criticism has been functioning as a
substitute for the work rather than a spur to it. That criticism applies to this
page more than to most.

**One reading, one tree.** Everything above is drawn from this ecosystem, which
is small, young, and mostly written by agents under one person's supervision.
None of it has been tried anywhere that did not already believe it.
