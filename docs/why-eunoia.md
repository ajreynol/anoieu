# Why a proof calculus, and not just Lean

> **Internal note.**
>
> Tracked, so that it has a history and can be argued with in review — but
> deliberately not linked from `docs/README.md` or any other index, because it
> is a working argument rather than a published position, and nothing in the
> tool depends on it. Its purpose is to have the case written down well enough
> to argue with — with the ethos, cvc5 and logos people, and with ourselves — so
> that the reasons for the arrangement are examined rather than inherited. Both
> columns are meant to be read: where the argument against is stronger, it says
> so. Link it from an index only if it becomes something to publish.

## The question, put fairly

An SMT solver has found an answer and is asked to justify it. Two arrangements:

**Native.** The solver emits a Lean proof — terms, or a script — and Lean checks
it. One language, one kernel, one toolchain, and the theorem you get at the end
is a Lean theorem.

**A calculus.** The solver emits a proof in a fixed proof calculus (CPC), written
against a signature in a small language (Eunoia). A checker for that calculus
checks it. The calculus is *also* compiled — by `ethos-eoc` — into a Lean
development (logos) that says its rules are sound against a semantics of
SMT-LIB, and into a verification condition per rule.

The second is more machinery. This is the argument that the machinery earns its
place, and the argument against.

---

# The case for the calculus

## 1. Eunoia is SMT-LIB, and that is the level the work actually happens at

A solver developer's day is spent manipulating SMT terms: `(or x y)`,
`(str.++ s t)`, `(bvadd x y)`, a rewrite that turns one into another. Eunoia is
that vocabulary, in that concrete syntax, with the type rules written the way an
SMT-LIB theory declaration is written:

```lisp
(declare-const or (-> Bool Bool Bool) :right-assoc-nil false)
(declare-rule contra ((F Bool)) :premises (F (not F)) :conclusion false)
```

Nothing here is encoded as anything. The rule is *about* `or`, not about a
constructor of an inductive type that stands for `or` under an embedding the
reader has to keep in their head. The distance between what a solver developer
thinks and what they write is close to zero, and that distance is paid on every
one of CPC's 593 rules, by the people least interested in paying it.

In a native arrangement the first thing you must do is choose an embedding of
SMT terms into Lean — deep or shallow, with or without sorts as types, with what
treatment of variadic operators and of numerals — and from then on every rule is
a statement about the embedding. The embedding is a design artifact that has to
be argued, maintained and understood by everyone who writes a rule, and it is
*additional* to the calculus itself. Eunoia's answer to "what is the embedding"
is: there isn't one, the terms are the terms.

Four things follow.

**The proof and the problem are in one language.** This is the sharpest form of
the argument, and it is concrete. Ethos supports `(reference "problem.smt2")`:
it parses the actual benchmark, collects its `assert` formulas, and then refuses
any `assume` in the proof that is not one of them. The proof is checked against
*the file the solver was given*, syntactically, with an optional normalisation
routine written in the same language when the two spellings differ.

A Lean pipeline cannot do that without a translator from SMT-LIB into its
embedding — and that translator is trusted, unverified, and precisely where the
statement you prove can drift from the problem you were handed. A perfect Lean
proof of a subtly mistranslated formula is worth nothing, and nothing in the
Lean development can tell you it happened. The calculus arrangement moves that
seam into a place where a checker can look at it.

**The emitter is small, and can lie less.** cvc5's proof production maps internal
inference steps onto rules over the same terms it was already manipulating. The
closer the target language is to the internal representation, the less
translation code there is between the reasoning and its record, and the less
room for the record to describe something other than what happened.

**The signature is a specification of cvc5's SMT-LIB, in the community's own
vocabulary.** CPC's header says outright where cvc5 departs from the standard:
mixed Int/Real arithmetic, variadic operators with nil terminators instead of
associative chains, strings as sequences. That is a document SMT people can read
and disagree with, in the notation of the standard it is deviating from. The
equivalent knowledge in a native arrangement lives in the embedding and in the
emitter, where the SMT-LIB community cannot read it.

**Ownership sits where the expertise is.** The authoritative artifact — the
calculus — is maintained by the people who maintain the solver, in a language
they already read. Nobody has to learn a proof assistant to change a rule.
(Against, honestly: the `.eos` semantics *does* demand both kinds of expertise
at once, which is the seam where this benefit stops.)

## 2. A narrow fragment is a thing you can understand; a wide one is not

Eunoia is deliberately small: declarations with a handful of attributes,
programs that are ordered rewrite rules matched first-to-last, computations over
literals, and proof rules that are patterns with side conditions. No
elaboration, no implicit-argument synthesis, no typeclass search, no macros, no
tactics, no metaprogramming — and nothing a proof can invoke that is not one of
those.

What that buys is not elegance. It is that **the ways a thing can be wrong are
enumerable**, and this repository is the evidence: 43 checks cover a large part
of what a signature can get wrong, the whole analyzer is about three thousand
lines, and its account of the language's desugaring is validated against the
real parser case by case. Nobody writes that for "arbitrary Lean", because for
arbitrary Lean the list does not close.

The same narrowness is what lets one proof be checked by more than one thing.
What a proof *means* is fixed by a signature rather than by one program's
behaviour.

## 3. The proof is data, not a program

A CPC proof is a list of steps: a name, a rule, premises, arguments. It streams,
it diffs, it is generated and consumed by machines, and it imports nothing. A
Lean proof is a program in a language whose elaborator, standard library and
syntax move; a proof that elaborates today may not in a year, for reasons that
have nothing to do with the mathematics.

The counter: a calculus moves too — CPC gains rules. The difference we would
argue for is that the calculus is *versioned data* rather than code, and its
checker is generated from it, so a change is a diff in a signature rather than a
migration.

## 4. Machine-generated proofs are enormous, and the fragment makes checking them cheap

SMT proofs are not written by people. They come out of a solver in the hundreds
of thousands of steps, with structure no human chose. Checking them wants
bottom-up evaluation, matching without unification, and no search — which is
what the fragment provides and what a proof assistant, whose elaborator exists
to be clever on human-written input, does not specialise in.

We have no measurements of our own here, and would want some before leaning on
this hard. It is the historical reason the arrangement exists, and the claim
most worth testing — and Pathos, below, is an attempt to make it moot by
building a checker that is fast *and* verified.

## 5. Computation is expressible without being proved

A rule can fire only if a program says two polynomials normalise to the same
thing, or the bit-blasted forms match. The program is written in the fragment,
so its evaluation is total in practice, inspectable, and cheap.

Natively you either prove the same work step by step — which is what makes
proofs enormous — or discharge it by reflection with a verified normalizer,
which is expensive to build, or by an unverified decision procedure, which
enlarges what you trust. The calculus makes the third option *inspectable*: what
a side condition computes is written in a language a tool can read. This one
reads it.

## 6. You do not have to choose: the Lean side is generated

`ethos-eoc` compiles one signature into a fast checker *and* a Lean development
in which each rule's soundness is a lemma against a semantics of SMT-LIB, *and*
an SMT verification condition per rule. "Check it fast" and "justify it in a
proof assistant" are not alternatives — the second is derived from the same
description as the first, and regenerated when the calculus changes.

Writing proofs natively gives you a Lean theorem per proof. This arrangement
gives you a Lean theorem about the *rules*, once, and then every proof that uses
them for free.

## 7. Analyzability is a property you can design for

Because the fragment is small, tools like this one are possible; because they
are possible, the fragment's own weak checking is fixable. That loop is only
available at this end of the spectrum.

---

# The case for doing it in Lean — but *which* tool?

"Do it in Lean" is not one proposal. The ecosystem is five artifacts, and each
could move independently; separating them is most of the argument, because the
reasons above defend some of them and say nothing about the others.

| artifact | today | "in Lean" would mean | separable? |
| --- | --- | --- | --- |
| the **signature** (`.eo`) | SMT-LIB-shaped text, maintained by solver developers | the calculus defined as Lean inductives and rule schemas | yes |
| the **semantics** (`.eos`) | a second bespoke language, its own compiler | Lean definitions over a fixed SMT-LIB model | yes |
| the **compiler** (`ethos-eoc`) | C++ plugins + a Python driver splicing text into `$MARKER$` templates | a Lean metaprogram elaborating definitions | mostly, after the semantics |
| the **checker** (`ethos`) | C++, fast, unverified | ship the generated Lean checker instead | yes |
| the **proof format** (CPC files) | s-expression steps over SMT terms | Lean terms over a fixed embedding | yes |

## T1. The semantics (`.eos`) as Lean definitions — the strongest candidate

Today the meaning of a symbol is written in a language that exists only to say
it: two configuration sets, four levels of vocabulary that are never written
down in a term, a compiler (`sem_compile.py`) that renders them into a
signature written in a deep embedding, an aggregate table declaring which
generated program each case is spliced into, directives passed between stages as
head comments in generated files, and one obligation — `is_list_nil` — that is
hand-written per operator and compared with nothing.

In Lean, the SMT-LIB model is already a development (logos's `SmtEval`,
`SmtModel`), and a calculus's semantics would be a function from its term
language into that model. The four levels become types. The aggregate table
becomes pattern matching. `sem_compile.py` disappears. The `is_list_nil`
obligation becomes something with a type — a field, or a lemma — rather than a
predicate nothing checks.

**What it costs.** The fast checker's model-smt stage consumes the deep
embedding, and the SMT-LIB and SyGuS backends consume it too, so this needs
either extraction from Lean into those, or an admission that verification
conditions come from the Lean side by another route. And writing a calculus's
semantics would demand Lean fluency where it currently demands `.eos` fluency —
which is not obviously the harder of the two, but is a different population.

**It does not touch argument 1.** The signature stays `.eo`, SMT-shaped, owned
by solver developers. This is the one proposal where the case above offers no
defence, which is why we think it is the strongest.

## T2. The compiler (`ethos-eoc`) as a Lean metaprogram

The compiler's architecture is text: eleven templates with holes, blocks emitted
in an order constrained by what names what, and a side channel of `$eoc-`
comments that a Python regex reads back out. A metaprogram that elaborated
definitions instead would have none of those problems, and its output would be
type-checked as it was produced rather than when Lean next runs.

It would still need to read `.eo` — logos already parses the proof format, so a
signature parser is not far-fetched — and the SMT-LIB and SyGuS backends still
emit text either way. Mostly a follow-on to T1: the compiler's main job is
compiling the semantics, so moving the semantics moves most of the compiler.

## T3. Retire `ethos` and ship the generated checker

One implementation instead of two, soundness by construction, and no seams
between a C++ checker and a Lean one to keep in step.

**What it costs, and one cost we had not counted.** Performance, which nobody
has measured. The `.smt2` reference check, which would have to move too — and
which is argument 1's sharpest point. And an asset we only noticed by reading
eudaimonia: it builds ethos *alongside* the compiler and cross-checks its
regression proofs against the generated checker. Two independent implementations
disagreeing is a bug report; one implementation is a bug report nobody files.
Retiring ethos deletes that.

## T4. The signature (`.eo`) itself

The maximal proposal, and the one arguments 1 and 2 actually answer. It would
give this analyzer's whole catalogue for free, and it would move the artifact
solver developers maintain out of the notation they think in, put the reference
seam back behind an unverified translator, and re-target cvc5's emitter.

Worth being precise about, because the SMT-abstraction argument gets used to
defend the *whole* status quo when what it defends is T4 and T5. It says nothing
about T1, T2 or T3.

## T5. The proof format

Separable from everything above: one could keep `.eo` and `.eos` and still have
cvc5 emit Lean over a fixed embedding, or keep CPC proofs and move the entire
toolchain. This is the question the document opened with, and it is the *last*
of the five to be settled, not the first.

## A note on this analyzer

Under T1, T2, T3 and T5, anoieu is unaffected: it reads signatures. Under T4,
most of it stops being necessary. That is a useful way to sort the proposals —
and a reason to distrust our enthusiasm about exactly one of them.

---

# The general objections

These are about the fragment rather than about any one tool, and are numbered
`O` so as not to collide with the arrangements lettered below.

## O1. The type system gives most of the check catalogue for nothing

Program bodies untyped, matching untyped, `define` bodies never typed, a
program's declared return type unverified, arity unchecked inside a body: every
one of those is a check in this repository, and every one is a non-question in a
typed functional language. We wrote three thousand lines to recover a fraction
of what Lean would have given by construction. That is not an argument about
taste; it is a measured cost, and we paid it.

## O2. The `.eos` layer is the tell

The fragment cannot express its own meaning, so a *second* bespoke language
exists to say what its symbols mean — with four levels of vocabulary that are
never written down in a term, its own compiler, its own reference checks, and
(by its own documentation) at least one seam that nothing checks. In a Lean
arrangement the semantics would be ordinary definitions, the four levels would
be types, and the compiler would be unnecessary. When a design needs a second
language to explain the first, that is evidence about the first.

## O3. Termination is the language's job, and here it is nobody's

A Eunoia program may not terminate and nothing checks it; the Lean backend needs
hand-written measures supplied as literal Lean text inside `.eos` files, and a
missing one surfaces when Lean runs, a full regeneration later. Lean checks
termination as a matter of course.

## O4. The narrowness argument cuts both ways

What makes CPC proofs tractable is not that Lean *can* express more; it is that
the emitter does not. An emitter targeting a fixed deep embedding in Lean is
exactly as constrained as one targeting CPC — the freedom to write arbitrary
Lean is hypothetical unless somebody uses it, and a convention plus a linter (in
Lean, where writing the linter is easier) would enforce the same fragment. The
honest version of reason 2 is therefore narrower than it sounds: what we want is
a *fixed* language for proofs, not necessarily a *separate* one.

## O5. So does the interchange argument

Proof terms over a fixed embedding are data too: serialisable, diffable,
checkable by anything that implements the embedding. And the portability we
claim is worth what its consumers make it worth — today CPC has one producer,
and its consumers are ethos and a checker generated from the same source.

## O6. Two implementations is a choice, not a consequence

A checker, a compiler, a generated checker, and a semantics relating them, all
kept in step by hand at the seams. None of that exists in the native
arrangement. The `is_list_nil` predicate — hand-written per operator, required
exactly when the desugar stage forward-declares one, compared with nothing — is
what this cost looks like in practice.

## O7. "A fragment we understand well" is doing a lot of work

We understand it well *now*, partly because this project spent a week finding
out what it means: that matching does not check types, that `eo::define` binds in
parallel, that a `:list` annotation is inert under a plain associative operator.
None of those were written down. Lean's semantics are also documented, also
stable, and maintained by a much larger community with much more at stake.

---

# Six ways to arrange the ecosystem

Each is a coherent whole, not a wish. "Compatible with argument 1" means the
artifact a solver developer writes stays SMT-shaped.

| | authoritative | generated | production checkers | semantics lives in | biggest cost | arg. 1? |
| --- | --- | --- | --- | --- | --- | --- |
| **A** as it stands | `.eo` + `.eos` | Lean development, VCs | ethos | `.eos` | two languages, unchecked seams | yes |
| **B** semantics in Lean | `.eo` | Lean development, VCs, the SMT model for ethos | ethos | Lean | extraction back to the SMT/SyGuS backends | yes |
| **C** compile from Lean | Lean | `.eo`, the fast checker | ethos | Lean | the artifact leaves the solver developers' notation | partly |
| **D** one checker | `.eo` + `.eos` | Lean checker | the generated Lean checker | `.eos` | performance; loses the reference check and the cross-check | yes |
| **E** kernel + elaborator | a tiny core calculus | expansions of the big rules | a small kernel | wherever the kernel's is | proof size; every derived rule needs an expansion | yes |
| **F** no calculus | Lean | — | Lean | Lean | an unverified `.smt2` frontend; no SMT-level artifact | no |

**A, as it stands.** The virtue is that every piece exists and works. The costs
are the ones this document lists: two bespoke languages, a compiler made of text
templates, and obligations passed between tools that nothing compares.

**B, semantics in Lean.** T1 alone. The signature stays where solver developers
can read it; the part that needs types gets them. The open engineering question
is whether the SMT-LIB and SyGuS verification conditions can be extracted from
the Lean semantics as cleanly as they are currently generated from `.eos`.

**C, compile from Lean.** Invert the direction of generation: define the
calculus in Lean and emit the `.eo` signature for ethos. Keeps a fast checker
and an SMT-level artifact — but the *maintained* one is Lean, and the SMT-shaped
one is a build product, which is the opposite of where the expertise sits.
Argument 1 is only partly satisfied: solver developers can read the generated
signature but do not edit it.

**D, one checker.** Retire ethos from production and ship what logos proves. The
cleanest story about trust, blocked on a measurement nobody has taken, and it
gives up the two-implementation cross-check that eudaimonia currently relies on.
Pathos is the project that would unblock it — not by taking the measurement but
by removing the trade-off it measures.

**E, kernel and elaborator.** The LFSC-shaped alternative: a minimal core with a
handful of rules, and CPC's rules as macro expansions checked against it, with
an untrusted elaborator doing the expansion. The trusted base becomes very
small, and the Lean development only has to be about the kernel. What it costs
is exactly what CPC's side conditions were designed to avoid: a computation that
a program decides in one step becomes a derivation, and proofs grow accordingly.
Worth stating as a considered option rather than an unconsidered one — the
ecosystem moved away from it, and the reasons should be written down.

**F, no calculus.** The native arrangement, done with discipline: a fixed deep
embedding, an emitter restricted to it, and a Lean-side linter enforcing the
fragment. Everything in the case above about narrowness survives — what does not
survive is the SMT-level artifact and the reference seam, which now depend on a
translator from `.smt2` into the embedding.

**B and D compose**, and their composition is the arrangement we would bet on if
the measurement in T3 came out well: the signature stays the SMT-facing
interface and the proof format, and the entire verification stack — semantics,
soundness, checker — is Lean. Ethos survives as the fast unverified checker used
in the edit loop and as the independent cross-check, which is what it is best at
and what nothing else provides.

---

# Two projects that do not exist yet, and change the picture

**Pathos** and **hermeneia** are code names. Neither has a repository or a line
of code: both are future work, named here
because the costs and open questions above are stated relative to what exists
today, and each of these would move a different one. Writing down what they
*would* change is also the cheapest way to notice which of today's arguments are
about the arrangement and which are merely about its current state.

## Pathos — an efficient verified proof checker

*A code name, for work not yet started; there is no repository and no code.*
It continues the line the ecosystem names itself along — ethos and logos are two
of Aristotle's three modes of persuasion, and pathos is the third.

The ecosystem currently offers a choice between two half-answers: ethos is fast
and unverified, and the generated Lean checker is verified and unmeasured. A
checker that is both would not be a compromise between them; it would remove the
question.

**What it settles.** Reason 4 — machine-generated proofs are enormous, and the
fragment is what makes checking them cheap — is the load-bearing argument for
keeping a separate C++ checker in production, and open question 5 admits that
nobody has measured it. Pathos is an attempt to *dissolve* that trade-off rather
than to measure it. If it lands:

- arrangement **D** becomes viable, since its only stated blocker is the
  measurement;
- T3's cost list shrinks to the reference check and the cross-check, both of
  which are addressable on their own;
- the trusted base becomes the Lean kernel, the parser and the statement, rather
  than a C++ program about which nothing is proved.

**What it does not settle.** A verified checker still checks *a calculus*, so the
signature and its semantics remain its inputs, and argument 1, the reference
seam and the `.eos` question are all untouched. Pathos is orthogonal to
arrangements **B** and **C** — which is worth saying, because "we are building a
verified checker" is easily heard as "the rest is settled", and it is not.

**Where the difficulty sits.** Efficiency in a verified setting comes from the
data structures whose invariants are the hard part of the proof: hash consing,
term sharing, mutable state, and the tricks that make matching cheap. That is
the reason "efficient" and "verified" have historically been alternatives, and
it is where the work would go.

**And a consequence for this argument.** A verified checker is an expensive
artifact, and expensive artifacts want a stable interface to be built against.
That is a point *for* the calculus as a fixed input — reason 3, restated with
something concrete at stake.

## Hermeneia — from the embedded semantics to Lean's own logic

*Also a code name, and also work not yet started.* ἑρμηνεία is interpretation —
the carrying of meaning from one account into another, and the title of
Aristotle's *De Interpretatione* — which is exactly what the project does:
carry what a proof establishes about an encoding into a statement in Lean's own
terms.

Logos proves things about a deep embedding. Its guarantee today reads

```lean
theorem correct___logos_state_is_refutation (assums : List Term) (cmds : CCmdList)
    (h : logos_state_is_refutation (logos_run assums cmds) = true) :
    eo_satisfiability (logos_assumption_term assums) false
```

— the conjunction of a list of *embedded* `Term`s is unsatisfiable under the
*embedded* SMT-LIB semantics. That is true, checkable, and about the encoding. A
Lean user who wants to conclude something about Lean's own `Int`, `BitVec` or
`String` has to bridge the gap themselves, and there is no bridge.

The second project is that bridge: a correspondence between the SMT-LIB
semantics Logos carries and Lean's native logic, symbol by symbol and sort by
sort, so that what a proof establishes can be *restated* as an ordinary Lean
proposition.

**What it changes, and it is more than it looks.**

*The ecosystem acquires a second audience.* Today every consumer of a CPC proof
is a checker. With a correspondence, a consumer can be a **proof**: a Lean
development calls a solver, gets a refutation, and ends up with a theorem in its
own terms. That is the strongest available answer to objection O5 — the
interchange argument is worth what its consumers make it worth — because it adds
a kind of consumer the arrangement does not have at all.

*It answers open question 2 from the other end.* The sharpest argument for the
calculus is the reference seam: a Lean pipeline needs a trusted, unverified
translator from `.smt2` into its embedding, and that is where a statement can
drift from the problem. A correspondence does not verify that translator; it
makes it unnecessary in one direction. The problem stays in SMT-LIB, where ethos
can check the proof against the actual file, and the *verdict* is what travels
into Lean.

*It changes what the generated Lean development is for.* Reason 6 says the Lean
side is generated rather than chosen. Today what is generated is a soundness
argument that a person reads and trusts. With a correspondence it becomes a
component that a person *uses*, which is a different order of usefulness for the
same generation machinery.

**Why the compiler is the natural place to set it up.** A correspondence is a
per-symbol obligation — `Int` to `Int`, `bvadd` to a bit-vector operation,
`str.++` to an append — stated against the same semantics that already produces
one artifact per symbol. That is exactly `ethos-eoc`'s shape: it compiles a
symbol's meaning into a constructor, a type rule, an evaluator case and a
verification condition, and a correspondence lemma is one more thing in that
list. If it works, the compiler earns its keep by generating something no
hand-written development would keep in step — which is a real answer to
objection O2, and a reason to be slower about T2 than that objection suggests.

Read the other way, it is also the strongest argument yet for arrangement **B**:
a correspondence between two *Lean* definitions is a far easier thing to state,
prove and maintain than one between a Lean definition and a term rendered out of
`.eos` text by a compiler written in C++ and Python.

**Where the difficulty sits.** Choosing what corresponds to what, and what to do
where the two disagree. SMT-LIB's operations are total; Lean's native ones are
total in a different way or not at all — division by zero, an out-of-range
`str.substr`, a bit-vector of width zero. CPC already carries the evidence that
this is the hard part: it declares `div_total`, `mod_total`, `/_total` and the
`@div_by_zero` family precisely because the standard's totality has to be said
somewhere. A correspondence has to say where each of those lands in Lean, and
the answer is a design decision, not a lemma.

## What both mean for the argument above

Two of the cost columns are dated rather than wrong. Arrangement **D** is
blocked on a measurement that Pathos would replace with an artifact, and reason
4's folklore status matters much less if the trade-off it rests on is dissolved
instead of settled.

They also pull in different directions, which is worth being explicit about:
Pathos improves the *checker* without touching the semantics question, while
hermeneia makes the semantics question more consequential — and is easier
the more of the semantics lives in Lean. A team with effort for one of them is
choosing between "make the current arrangement's weakest artifact strong" and
"make the current arrangement's strongest artifact reach further".

What they share is that both are expensive things built *against* the signature
and the proof format. Each one that gets built raises the cost of moving them,
which is an argument for settling questions 1 and 3 — where the calculus is
defined, and whether `.eos` should be Lean — before rather than after.

---

# What eudaimonia says about all this

[eudaimonia](https://github.com/cvc5/eudaimonia) is the arrangement with the
calculus taken out: bring a signature and a semantics, get a Lake project with a
checker, its proofs, its regression suite and its documentation. It is the
falsification test for the claim `ethos-eoc` makes about itself — *a second
calculus is a second pair of files, not a change to the tool* — and its status
is the most informative thing in this document, because it says which half of
that claim is currently earned.

**What is done** (per its `TODO.md`, which is more current than its README's
status paragraph): fetching and building the compiler, driving it over a
signature and installing what it publishes, preserving hand-written per-rule
proofs across a regeneration, a `--check` mode that installs into a throwaway
copy and diffs, signature caching, a signature-independent parser library
vendored into each generated project and wired to the correctness statement, a
calculus profile, and ethos built alongside as a reference checker whose verdicts
are cross-checked against the generated one.

**What is not**: the correctness development itself. The core checker proof
(~3,000 lines in Logos), the side conditions (~257), the soundness theorem
(~1,063), the per-rule proofs (591 files), and the shared rule-support lemmas
are all generated as *stubs describing what belongs in them*. So the mechanical
pipeline generalizes and the proofs do not — yet.

**Three things it buys the argument.**

*It makes the signature a reusable input format.* The artifact that gets reused
across calculi is the SMT-level description, not the Lean. That is the
structural case for keeping the `.eo` layer, and it is stronger than any
aesthetic argument about notation: something already depends on it in a way that
a second calculus exercises.

*It gives the format a second consumer* — partially. Not a second producer, but a
second thing that reads a signature and does something non-trivial with it,
which is the weaker half of the interchange claim in reason 3.

*It preserves two implementations on purpose.* Its section 4d builds ethos next
to the compiler and cross-checks the regression proofs, and records the one
asymmetry (ethos has no SMT-LIB semantics, so there are questions it cannot
answer). This is the concrete asset arrangement D would delete.

**And two things it reveals about the cost.**

*The signature contract is checked late, and against the artifact.* Its README
specifies what a calculus must provide: a binary `and`, `and` translated to
`SmtTerm.and` by the semantics, and the Bool literals — plus, *only for calculi
whose rules gather `:list` premises with `and`*, that `and` be declared
`:right-assoc-nil true`. That last one is explicitly not a core requirement, and
a calculus without such rules needs no nil at all; `examples/hello` is one. (An
earlier draft of this document quoted it as universal. It is not, and the
correction is the point: a requirement stated in prose is a requirement that
drifts.)

`install/install-<calc>.sh` does check all of it — against **what the compiler
emitted**, because "the name an operator compiles to need not be its spelling,
and the attribute is only visible in what it generates". So the gap is not that
nothing checks it; it is that the check runs after a checker has been generated,
reads the output rather than the input, and can therefore only report what a
signature *became*. Answering the same questions from the signature and its
semantics — before anything is generated, in terms the author wrote — is
[eud-1](README.md#eudaimonia--the-template-for-other-calculi).

*Its calculus profile has answers that are declared rather than verified.* Seven
questions; five checked against what the compiler emitted, two recorded on
trust — and its own note that `value-ordering` is declared "and that is a
finding", because `SmtValueOrder.lean` is identical between `Cpc` and `CpcMini`,
so the compiler emits the same ordering whatever the signature says. A related
measurement: `examples/hello` declares three constants and one rule, and 370 of
its 2,395 generated lines — 15% — are datatype and literal machinery it cannot
use. Both are the same underlying fact: pieces of the "template" are fixed where
the claim says they are derived.

**What it points at.** Its own blocker for generalizing the proofs is to
*"stabilize the SMT-LIB model as a fixed base that signatures extend"* and to
*"extract the invariant core"* — separating what is calculus-independent from
what a signature contributes. That is the same seam arrangement **B** addresses,
approached from the other end. Two independent efforts arriving at one boundary
is the best evidence in this document that the boundary is real and currently in
the wrong place.

---

# What both columns agree on

Reading them together, the disagreement is narrower than "calculus or Lean".

Nobody in either column wants a solver to emit unconstrained tactic scripts, and
nobody wants rule soundness to go unjustified. Both columns want a fixed
language for proofs and a proof assistant somewhere in the arrangement. What
they disagree about is **which artifact is authoritative and which is
generated**:

- The calculus column says the SMT-level signature is authoritative — because it
  is what solver developers write and read, because it is what the reference
  check compares a proof against, and because the Lean development can be
  generated from it.
- The Lean column says the Lean development should be authoritative — because
  then the type system does the checking anoieu now does by analysis, the
  semantics needs no second language, and termination is not a hand-written
  attribute.

Which suggests the productive question is not *whether* to have a calculus, but
**where its definition should live and which direction the generation runs** —
arrangement **C** against arrangements **A**, **B** and **D** — and, separately,
whether `.eos` in its current form is the right way to say what a symbol means,
or whether that half specifically belongs in Lean while the signature stays as
the SMT-facing interface, which is arrangement **B**.

That last one seems, to us, the most likely place a real improvement is hiding,
and eudaimonia's roadmap arrives at the same seam from the other side.

---

# Where anoieu sits in this

Squarely on one side, and it should be said plainly: this tool is an argument for
the narrow-fragment position, and also an admission that the position is not
free. A fragment small enough to analyze exhaustively is only better than a
language that checks itself *if the analysis actually exists*. Every check in
`docs/checks.md` is something a type system would have given for nothing.

---

# Open questions

1. **Direction of generation.** Signature → Lean (**A**, **B**, **D**) or
   Lean → signature (**C**)? logos is already a generated deep embedding; the
   question is which end is the source.
2. **Could the `.smt2` → Lean translation be eliminated or verified?** If it
   could, argument 1's sharpest point — the reference seam — loses much of its
   force, and the native arrangement gets a lot more attractive.
3. **Should `.eos` be Lean?** Keep the signature as the SMT-facing artifact,
   write the semantics as Lean definitions, generate what the SMT backend needs
   from those. Would that keep argument 1 and dissolve objection O2? It is arrangement **B**.
4. **Where is the line between a rule and a side condition?** Every computation
   moved into a program is work not proved, and work whose meaning must be
   modelled somewhere.
5. **How much does the fast checker actually buy?** Nobody here has measured
   ethos against the generated Lean checker on the same proofs. Until somebody
   does, reason 4 is folklore and arrangement **D** cannot be argued either way —
   and if Pathos succeeds the question becomes "did the third checker work"
   rather than "which of the two do we keep".
6. **Was the kernel-and-elaborator arrangement (E) rejected, or just left
   behind?** The ecosystem came from LFSC; the reasons for moving away from a
   tiny kernel with expandable rules are worth writing down while people still
   remember them.
7. **Where is the line between the invariant core and what a signature
   contributes?** eudaimonia's blocker and arrangement **B**'s design question
   are the same question, and whoever answers it answers both.
8. **What is a well-formed signature?** Unanswered in the language itself, and
   the answer decides whether the weak checking is a bug or a deliberate trade.
9. **Would a second producer change the calculus?** CPC is shaped by cvc5. A
   second one would show how much of it is *the* calculus and how much is one
   solver's habits.
10. **Is the ceiling real?** What reasoning has cvc5 wanted to emit and been
    unable to express as rules?

# What would change our minds

- **A measurement** showing the generated Lean checker is fast enough on
  solver-scale proofs, or **a verified checker that is fast by construction**
  (Pathos). Reason 4 goes, and with it much of the case for a separate C++
  checker.
- **Hermeneia: a correspondence between the embedded semantics and Lean's own
  logic.** The
  arrangement would then have a consumer that is a proof rather than a checker,
  which is a kind of consumer it has never had, and objection O5 would need
  rewriting.
- **A verified or eliminated `.smt2` frontend for the Lean side.** The strongest
  concrete argument in column one is the reference seam; close it and the
  balance shifts.
- **A Lean-side calculus definition** from which the fast checker is generated as
  well as the soundness development, without losing readability for the people
  who maintain the signature. Reason 6 inverts.
- **Evidence that signature authors trip over the fragment's subtleties more
  often than Lean users trip over Lean's.** Objections O1 and O7 would outweigh
  the case.
- **A calculus growing without bound** to keep up with the solver. The ceiling
  becomes the deciding cost.

# An experiment that would settle more than an argument

Take ten CPC rules of different shapes — one with a premise list, one with a
side condition doing real computation, one over bit-vectors with dependent
widths, one binder rule. Write them twice: as they are, and as a Lean deep
embedding with the same soundness statement. Then compare, on the same terms:
lines written, what each catches before it runs, what each catches only at use,
who on the team could maintain it, and how long checking takes for a real proof
using them.

Most of the disagreements above are empirical, and none of them has been
measured.
