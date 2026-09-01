# The report card

*Part of [`vision.md`](vision.md), which is the document that governs it: this
page is argued and never checked, no tool may put a verdict against a tenet, and
a paragraph here is changed by a person. It is a separate file because it is the
half that moves — the tenets are stable and these paragraphs are re-graded every
round — and because a judgement about somebody else's project is a different
kind of writing from a statement of what the work is for.*

How each tool in the ecosystem stands against the six tenets. It is here
because a vision document with nothing measured against it is a wish, and
because the useful thing for another repository to read is not the rules but
what happened when somebody applied them to real projects. Graded at the commits
[`deps.lock`](../tools/deps.lock) records.

Three fields per tool, named along the ecosystem's convention:

| field | means |
| --- | --- |
| **arete** — ἀρετή, excellence | what the project does well, and what another project should take from it |
| **elleipsis** — ἔλλειψις, a falling short | where it comes up short of a tenet, with the evidence |
| **parainesis** — παραίνεσις, counsel | what follows from the other two |

## Two registers, and the project decides which

[`policy.md`](policy.md) requires every repository to end its README with a note
saying how its development is currently run. **That note decides how a paragraph
here is written** — not our impression of the code, and not a list kept on this
side that would be stale within a month.

**A project run by people gets an observation.** The tenets were invented here
and nobody agreed to them; a person made choices for reasons that need not be
visible in the tree, and an instruction would be presuming on all of it. So:
what we noticed, what it appears to have cost, and no imperative.

**A project run by agents gets an instruction, and no apology.** There is nobody
to offend and no accumulated judgement to defer to. Hedging is expensive at the
rate an agent produces work and directness is cheap, so if such a project is
underperforming a tenet, the paragraph says so plainly and says what to do about
it. This is the one place where the *don't be self-deprecating* rule above has
teeth: an agent softening a finding about another agent's tool is protecting
nobody.

Where a repository has no maintenance note at all, the first register applies —
guessing is the failure this rule exists to prevent.

## What this is not

**Read it with a large grain of salt, and do not read it as binding anything.**
It is **absolutely not a contract**: none of these projects agreed to these
tenets, most predate this page, nothing here creates an obligation, and nobody
may hold a project to a sentence in it. It is **not a set of findings**: a claim
about somebody else's work goes through
[`../docs/reports/reporting-policy.md`](reports/reporting-policy.md) and
[`../docs/reports/reporting-workflow.md`](reports/reporting-workflow.md) — confirmed,
reproduced small, carried by a person — and nothing here has been through any of
that, nor has any row in [`../docs/reports/reports.md`](reports/reports.md) come from it.
It is **not evenly evidenced**: this repository reads `.eo` and `.eos`, so what it
knows about a C++ compiler's stages or a Lean proof's structure is read out of
documents rather than measured, and the paragraphs say which. And it is **not a
ranking** — the tenets fit some of these projects badly, and a tenet fitting
badly is a fact about the tenet.

Those are limits on *standing*, and they do not soften into apology. The only
real check here is that the tool which wrote the page is graded on the same
scale, in the sharper register, and does not come out best.

## cvc5

**Arete.** Tenet 1 at its strongest, largely by an accident of format: CPC sits
in cvc5's own tree as plain text under `proofs/eo/cpc/`, and is read by ethos,
compiled by `ethos-eoc`, copied into logos, vendored by eudaimonia and analyzed
here — five consumers, no API, no release process, no coordination. That is the
pattern this page generalizes from rather than one it taught.

**Elleipsis.** Nothing in its CI reads its own signature with an analyzer, the
drift check against logos's copy is planned rather than running, and `cvc5-1` —
two programs in `programs/Strings.eo` declaring `Int` where every case returns a
Boolean — was recorded on our side as fixed upstream and never was.

**Parainesis.** An observation rather than advice: that defect survived every
review the signature has had, and the thing that would have caught it is a gate
rather than a reader. Tenets 3 and 5 do not apply here at all — and neither does
membership. cvc5 sits outside the ecosystem, which exists to serve it; it is
graded here because the tenets were largely learned by watching it, not because
anybody expects it to adopt them.

## ethos

**Arete.** The clearest instance of tenet 1 in the ecosystem, and worth studying
because the fruitfulness was not designed: a checker written in C++ to answer
*does this proof check* became a build dependency of a Lean development, which
vendors it, and the reference implementation inside every project eudaimonia
generates.

**Elleipsis.** `user_manual.md` is the definition of Eunoia and the document the
whole ecosystem reads, but it is a manual for a *program* — it opens with how to
build the executable and never draws the line between what the language requires
and what this implementation happens to do, which is why a second implementation
cannot be written from it. On tenet 2, the fuzzer produced an uncaught C++
exception on `(declare-const f (->))` and an error path that skips ethos's own
`Error:` convention within the first few thousand cases.

**Parainesis.** An observation: those two are unfiled, which is our shortfall
rather than theirs, and until they are filed this paragraph is worth less than
it looks.

## ethos-eoc

**Arete.** Tenet 1 by construction — logos and eudaimonia both exist downstream
of it.

**Elleipsis.** The worst tenet 2 in the ecosystem, by its own account rather
than ours. Adding one symbol to a calculus runs `sem_compile.py` → desugar →
trim-defs → model-smt → smt-meta/lean-meta → cvc5 or Lean before you learn
whether it was right, and its own map of itself says outright that there is no
way to ask *is this one block well-formed against the embedding* short of
compiling the set. The failure modes are all late: a symbol with no semantics is
fatal at stage 6; a forward-declared program that is never defined arrives in
SMT-LIB as a free uninterpreted function and in Lean as a name nobody wrote.

**Parainesis.** Build the block-level well-formedness check. Every failure named
above is decidable from the two input files, which makes that loop long by
omission rather than by necessity — and a compiler is the worst place in an
ecosystem to keep the slowest feedback, because everything downstream inherits
the wait. It is the highest-value unbuilt thing on this page.

## logos

**Arete.** Exemplary on tenet 4, in the least obvious way: its most valuable
output to this repository has been three *replies* — `logos-2` accepted,
`logos-4` declined with a reason that holds, `logos-5` declined and documented —
and a decline with a written reason is worth as much as a fix, because it is
usually a fact about the subject nobody had recorded. It also caught us being
wrong, which is the most useful thing a consumer does: answering rows against
its own copy of CPC is how it emerged that `cvc5-1` had been recorded as fixed
when it never was.

**Elleipsis.** Tenet 3. `install/defs/Cpc.cached.eo` is a copy of cvc5's
`Cpc.eo` rather than something logos wrote, and whether it has drifted is a
check that is planned rather than running.

**Parainesis.** An observation: a repository carrying somebody else's ground
truth by copy is not self-contained in the sense the tenet means, and the
ordinary remedy is a manifest and a lock. Separately, it is already the natural
home for the triple check, since it vendors ethos and consumes cvc5's signature
— that is `logos-3`, and it is open.

## eudaimonia

**Arete.** The best adherent on this list and the most deliberate one. Tenet 1
is its entire purpose: it exists to make somebody else's compiler reusable, and
it is the falsification test for that compiler's central claim. Tenet 2 it does
properly — a `--check` mode that installs into a throwaway copy and diffs, and
ethos built alongside so the generated checker's verdicts are cross-checked
against an independent implementation. Tenet 4 is where it is exemplary, and it
is the case that made this page word that tenet abstractly: what it delivered to
logos is an argument — evidence and motivation that the correctness proof needs
modularizing — rather than an artifact.

**Elleipsis.** Tenet 3. Its `TODO.md` is more current than its README's status
paragraph, so the front page is not the entry point; and its signature contract
is specified in prose, which this repository misread once and had to correct.

**Parainesis.** Generate the README's status paragraph from `TODO.md` or delete
it. A front page less current than a file sitting beside it is exactly the
failure *The front page* names, and it is a morning's work. Then answer the
signature contract from the signature and its semantics rather than from what
the compiler emitted — that is `eud-1`, and the argument for it is eudaimonia's
own note that a declared `value-ordering` "is a finding".

## anoieu

**Arete.** Tenet 2, and it is the part worth copying: one small witness file per
check, ethos's verdict on each recorded from a real run and never typed by hand,
a committed CPC baseline with warnings denied so a change inventing a false
positive fails *this* build before it reaches anyone else's, generated documents
regenerated and diffed on every push, and `--pinned` restoring recorded commits
so the build goes red for its own reasons only. Tenet 4 is met:
`reports/cpc-audit.html` for readers who will not clone anything, six shrunk
reproducers under `tests/fuzz/`, and a ledger carrying an id and a state per row.
Tenet 1 has one genuine instance now — `tools/policy_check.py --root` is a thing
another repository runs in its own CI, and the interface is tested here rather
than trusted.

**Elleipsis.** Tenet 1 is still where the honest mark is low. Findings have
reached six projects, but **no other repository runs the analyzer**: the CI
adoptions are proposals rather than jobs, and nothing anywhere consumes its
machine output. Nothing the fuzzer found has been filed upstream. Auditing
logos's copy of CPC filed cvc5's findings under logos's name seventeen times
before anyone noticed. Tenet 5 is unmet by definition, no person having taken
over developing it.

There is a newer and more specific failure, and it belongs here rather than in a
footnote. The governance layer — this page, the policy, the coherence document,
the reporting policy and workflow, the discussion protocol — now runs to
thousands of lines, and the stretch of work that produced most of it **changed
nothing about what the analyzer finds**. Two silent defects were introduced into
the fuzzer during it, one of which would have let CI pass while verifying
nothing at all. That is tenet 2 working, and it is also the clearest evidence
available that documentation about the work is not the work. This page imposes a
clutter budget on the README and none on itself.

**Parainesis.** File the two ethos fuzzer findings, and get one CI job running in
one other repository. Both have been the obvious next thing for long enough that
the tenet 1 mark is a description of avoidance rather than of difficulty — the
machinery has been finished for a while, and what is missing is the decision to
spend somebody else's attention. Then stop writing governance. Every further page
here has to displace a check, a finding, or an hour of somebody else's reading,
and the sharp version of this tenet applies to its author before anybody else:
**writing a seventh document is the comfortable alternative and is not the work.**

## dokimasia

**Arete.** Tenet 1 in the cheapest available form: it adopted this repository's
[`../docs/reports/reporting-policy.md`](reports/reporting-policy.md) by reference
instead of forking a copy, so there is one position, one place to argue about it,
and neither tool carrying a stale paraphrase of the other.

**Elleipsis.** Its consumers today are people rather than tools. And this
paragraph has the least behind it of any here — the limit should be taken
seriously, because this repository reads `.eo` and `.eos` rather than C++, so
everything above comes out of that project's own documents and
[`../docs/notes.md`](notes.md) §8 rather than out of any measurement.

**Parainesis.** Settle who owns the check at the `src/proof/eo/` seam, where
cvc5 turns an internal proof into Eunoia: a rule cvc5 emits that CPC does not
declare is visible from either side and from neither alone. That is `cvc5-6`, it
was requested by cvc5, and it is owned by nobody. Two tools building the same
check is the waste tenet 1 exists to prevent, and it is being prevented right now
only by neither having built it.

## How to get a paragraph changed

Say that it is wrong. There is no process, no id and no ledger, because none of
this is a finding. The rows most likely to be wrong are the ones about internals
this repository does not read — `ethos-eoc`'s stages, logos's proof structure,
dokimasia's C++ — all read out of documents written by the people who built
them, and a document is not a measurement. The rows least likely to be wrong are
the ones with a file and a line number, and those have already been carried
properly, as findings, through a process this page is not.

If a paragraph is in the wrong register, the fix is upstream of us: the register
follows the maintenance note in your README, so changing that changes this.
