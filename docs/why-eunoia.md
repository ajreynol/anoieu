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
most worth testing.

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

# The case for doing it in Lean

Stated as strongly as we can put it, because these are the arguments that would
actually move the decision.

## A. The type system gives most of the check catalogue for nothing

Program bodies untyped, matching untyped, `define` bodies never typed, a
program's declared return type unverified, arity unchecked inside a body: every
one of those is a check in this repository, and every one is a non-question in a
typed functional language. We wrote three thousand lines to recover a fraction
of what Lean would have given by construction. That is not an argument about
taste; it is a measured cost, and we paid it.

## B. The `.eos` layer is the tell

The fragment cannot express its own meaning, so a *second* bespoke language
exists to say what its symbols mean — with four levels of vocabulary that are
never written down in a term, its own compiler, its own reference checks, and
(by its own documentation) at least one seam that nothing checks. In a Lean
arrangement the semantics would be ordinary definitions, the four levels would
be types, and the compiler would be unnecessary. When a design needs a second
language to explain the first, that is evidence about the first.

## C. Termination is the language's job, and here it is nobody's

A Eunoia program may not terminate and nothing checks it; the Lean backend needs
hand-written measures supplied as literal Lean text inside `.eos` files, and a
missing one surfaces when Lean runs, a full regeneration later. Lean checks
termination as a matter of course.

## D. The narrowness argument cuts both ways

What makes CPC proofs tractable is not that Lean *can* express more; it is that
the emitter does not. An emitter targeting a fixed deep embedding in Lean is
exactly as constrained as one targeting CPC — the freedom to write arbitrary
Lean is hypothetical unless somebody uses it, and a convention plus a linter (in
Lean, where writing the linter is easier) would enforce the same fragment. The
honest version of reason 2 is therefore narrower than it sounds: what we want is
a *fixed* language for proofs, not necessarily a *separate* one.

## E. So does the interchange argument

Proof terms over a fixed embedding are data too: serialisable, diffable,
checkable by anything that implements the embedding. And the portability we
claim is worth what its consumers make it worth — today CPC has one producer,
and its consumers are ethos and a checker generated from the same source.

## F. Two implementations is a choice, not a consequence

A checker, a compiler, a generated checker, and a semantics relating them, all
kept in step by hand at the seams. None of that exists in the native
arrangement. The `is_list_nil` predicate — hand-written per operator, required
exactly when the desugar stage forward-declares one, compared with nothing — is
what this cost looks like in practice.

## G. "A fragment we understand well" is doing a lot of work

We understand it well *now*, partly because this project spent a week finding
out what it means: that matching does not check types, that `eo::define` binds in
parallel, that a `:list` annotation is inert under a plain associative operator.
None of those were written down. Lean's semantics are also documented, also
stable, and maintained by a much larger community with much more at stake.

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
and, separately, whether `.eos` in its current form is the right way to say what
a symbol means, or whether that half specifically belongs in Lean while the
signature stays as the SMT-facing interface.

That last one seems, to us, the most likely place a real improvement is hiding.

---

# Where anoieu sits in this

Squarely on one side, and it should be said plainly: this tool is an argument for
the narrow-fragment position, and also an admission that the position is not
free. A fragment small enough to analyze exhaustively is only better than a
language that checks itself *if the analysis actually exists*. Every check in
`docs/checks.md` is something a type system would have given for nothing.

---

# Open questions

1. **Direction of generation.** Signature → Lean, or Lean → signature? logos is
   already a generated deep embedding; the question is which end is the source.
2. **Could the `.smt2` → Lean translation be eliminated or verified?** If it
   could, argument 1's sharpest point — the reference seam — loses much of its
   force, and the native arrangement gets a lot more attractive.
3. **Should `.eos` be Lean?** Keep the signature as the SMT-facing artifact,
   write the semantics as Lean definitions, generate what the SMT backend needs
   from those. Would that keep argument 1 and dissolve objection B?
4. **Where is the line between a rule and a side condition?** Every computation
   moved into a program is work not proved, and work whose meaning must be
   modelled somewhere.
5. **How much does the fast checker actually buy?** Nobody here has measured
   ethos against the generated Lean checker on the same proofs. Until somebody
   does, reason 4 is folklore.
6. **What is a well-formed signature?** Unanswered in the language itself, and
   the answer decides whether the weak checking is a bug or a deliberate trade.
7. **Would a second producer change the calculus?** CPC is shaped by cvc5. A
   second one would show how much of it is *the* calculus and how much is one
   solver's habits.
8. **Is the ceiling real?** What reasoning has cvc5 wanted to emit and been
   unable to express as rules?

# What would change our minds

- **A measurement** showing the generated Lean checker is fast enough on
  solver-scale proofs. Reason 4 goes, and with it much of the case for a
  separate C++ checker.
- **A verified or eliminated `.smt2` frontend for the Lean side.** The strongest
  concrete argument in column one is the reference seam; close it and the
  balance shifts.
- **A Lean-side calculus definition** from which the fast checker is generated as
  well as the soundness development, without losing readability for the people
  who maintain the signature. Reason 6 inverts.
- **Evidence that signature authors trip over the fragment's subtleties more
  often than Lean users trip over Lean's.** Objections A and G would outweigh
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
