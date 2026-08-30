# What anoieu is for

Two things live here.

**A sketch**, of the value this tool is meant to deliver, tool by tool, and a
record of how much of it exists. Every capability carries a status, and a
milestone that lands moves its row rather than adding a paragraph somewhere else.

**The actionable list.** Whenever a run produces something someone else should
act on, it is written down here:

- **(A) a concrete fix** in one of these tools — a defect anoieu found, named
  down to the file and line, with the change that resolves it;
- **(B) an adoption** — a recommendation that a tool run anoieu in its CI, with
  the configuration it would use and the rung of the ladder it should start on;
- **(C) a change to Eunoia itself** — to the language or to the manual that
  defines it, argued from something writing the analyzer turned up.

So this is the page to open when you want to know what anoieu is asking of
anyone. [`findings.md`](findings.md) says how each defect was confirmed;
[`ci.md`](ci.md) says how the adoption works. Neither asks anything; this does.

- ✅ **live** — written, tested, and run over the corpus
- ◐ **partial** — the useful half exists and the limit is stated
- ○ **sketched** — designed in [`design.md`](design.md), not written

### If you own one of these tools

Read your section. It is short, it says what anoieu found in your files and what
it would like you to do, and every claim in it was reproduced against ethos
before it was written down.

| you own | your section | read first |
| --- | --- | --- |
| cvc5's CPC signature | [cvc5](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5-1: two programs declare `Int` and return `Bool` |
| ethos, the proof checker | [ethos](#ethos--the-proof-checker-and-its-own-signatures) | ethos-1: a test signature declares an operator that cannot fold |
| ethos-eoc, the compiler | [ethos-eoc](#ethos-eoc--the-eunoia-compiler) | eoc-3: the `is_list_nil` diff your own docs ask for |
| logos | [logos](#logos--the-lean-development) | logos-1: the flattened copies carry cvc5-1 |
| eudaimonia | [eudaimonia](#eudaimonia--the-template-for-other-calculi) | eud-1: preflight a calculus against the signature contract |
| Eunoia itself | [Eunoia](#eunoia-itself--the-language-and-its-manual) | eunoia-1: an identical re-declaration makes two symbols that print the same |

### How a row moves

The **state** column is the whole tracker; there is no second one elsewhere.

| state | means |
| --- | --- |
| `open` | a defect, reproduced, not yet fixed |
| `proposed` | a change or an adoption we recommend and nobody has ruled on |
| `open question` | we do not think we know the right answer |
| `blocked on X` | waiting on another row |
| `needs M4` | waiting on a milestone here, not on you |
| `filed <link>` | raised upstream; the link is the issue or pull request |
| `fixed` / `adopted` / `declined` | ended, and kept in the table with the reason |

A row that is **declined** is a good outcome and stays visible: the check that
produced it then gets a suppression comment in your file or a `disable` in your
configuration, so the same argument is not had twice.

---

## Action items

| # | tool | kind | what | state |
| --- | --- | --- | --- | --- |
| [cvc5-1](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | A | `$is_seq_const_rec` and `$is_seq_const` declare `Int` and return `Bool` — `:signature ((Seq T)) Bool` on both | open |
| [cvc5-2](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | A | four skolem declarations duplicated verbatim in `expert/theories/ArithExt.eo` — delete lines 26–29 | open |
| [cvc5-3](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | A | 18 docstrings no longer describe their rule | open |
| [cvc5-4](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | A | `$is_app` in `programs/Utils.eo` is reached by nothing | open |
| [cvc5-5](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | B | run report-only on `Cpc.eo` and `CpcExpert.eo`, then baseline and block | proposed |
| [ethos-1](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | `tests/match-simple.eo:11` declares `<` `:right-assoc` with a `Bool` return | open |
| [ethos-2](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | an unknown attribute warns and is dropped, silently changing what a term means; make it an error, or at least carry the location | proposed |
| [ethos-3](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | a misordered `declare-rule` field reports as `Expected conclusion`, several lines from the cause | proposed |
| [ethos-4](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | a program applied to the wrong arity prints without a file or line, and the run still exits `correct` | proposed |
| [ethos-5](#ethos--the-proof-checker-and-its-own-signatures) | ethos | B | run over `tests/*.eo`, `DOC*` disabled | proposed |
| [ethos-6](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | two test signatures use literals whose category they never declare, so `+` gets an untyped nil | open |
| [ethos-7](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | `tests/naive-nary.eo:182` — a case of `isPermutation` that can never be reached | open |
| [eoc-1](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | preflight: have `driver.py` run anoieu over the triple before stage 1, so a missing semantics block is refused at launch rather than at stage 6 | proposed, needs M4 |
| [eoc-2](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | run over `semantics/*.eos` and the signatures the tests compile | proposed, needs M4 |
| [eoc-3](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | lean on anoieu for its own direction #2 — the diff between the operators the desugar stage forward-declares and the `:is-list-nil` blocks a human wrote, which nothing compares today | proposed, needs M4 |
| [logos-1](#logos--the-lean-development) | logos | A | the flattened copies carry cvc5-1; regenerate once it is fixed upstream | blocked on cvc5-1 |
| [logos-2](#logos--the-lean-development) | logos | B | run the triple over `Cpc.eos` and the signature it is of | proposed, needs M4 |
| [eud-1](#eudaimonia--the-template-for-other-calculi) | eudaimonia | B | answer the signature contract from the signature and semantics, before a checker is generated, rather than from the compiler's output afterwards | proposed, needs M4 |
| [eud-2](#eudaimonia--the-template-for-other-calculi) | eudaimonia | B | settle the calculus profile's two *declared* answers against the signature instead of recording them on trust | proposed, needs M4 |
| [eunoia-1](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | refuse a re-declaration whose type is identical to an earlier one | proposed |
| [eunoia-2](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | an unknown attribute should be an error, not a dropped annotation | proposed |
| [eunoia-3](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | enforce the attribute contracts the manual states as "must", at the declaration | proposed |
| [eunoia-4](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | decide what a well-formed signature is: type program bodies, or say that a program's return type is a claim nothing checks | open question |
| [eunoia-5](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | write down that matching does not check types, and what follows from it | proposed |
| [eunoia-6](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | settle `eo::define` in the grammar: several bindings, bound in parallel | proposed |
| [eunoia-7](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | say what `eo::hash` guarantees, or mark it as the one thing a model cannot follow | open question |

Nothing in this table is filed anywhere yet; it is what we would file.

## The claim

Ethos is a proof checker, and a good one *because* it is lazy: it computes a
type when something asks, checks the program case a proof reaches, and says
nothing about the rest. The consequence is that a *signature* — as opposed to a
proof — is nobody's job. A `define` body with no `:type` is never typed, a
program case is checked when a proof gets there, and a proof rule that can only
ever fail is a legal declaration until someone writes the step that finds out.

anoieu is the eager reader of the same files. It asks about every declaration,
with no proof in hand, no build, and no solver, in under a second. Of the 37
witness files in its suite — each holding one deliberate mistake — **ethos
accepts 32 and answers `correct`**. That number is the whole argument.

The second thing it is for is slower and possibly worth more: every check is a
statement about what Eunoia means, so the check catalogue, its witnesses, and
the differential harness against ethos amount to an executable account of a
language whose `.eos` half is specified today by one README and the compiler
that reads it. See [`language-notes.md`](language-notes.md).

## Status at a glance

| capability | answers | status |
| --- | --- | --- |
| parsing, includes, structure | is this a well-formed signature at all, and where exactly is it not | ✅ |
| attribute contracts | does `:right-assoc-nil`, `:chainable`, `:arg-list`, `:opaque` mean what this declaration can support | ✅ |
| the `:list` and n-ary hazards | does this pattern match the tail, or exactly two elements; can it be matched at all | ✅ |
| dead and unreachable code | which case can never fire, which program nothing reaches, which forward declaration was never defined | ✅ |
| shallow typing | is a rule's conclusion a `Bool`, does a program case return what it declares, is a symbol over-applied | ◐ — where the head settles it; a term whose head is a parameter, or that needs `eo::` evaluation, is not answered |
| desugaring | what does the parser build from what I wrote | ✅ — 34 cases agreeing with ethos term for term |
| the builtin layer | is an `eo::` operator applied to the right number of arguments, is this evaluation one the manual says cannot happen, does this literal have a type, is this list operator about an n-ary operator | ✅ |
| documentation | does the docstring still describe the rule | ✅ |
| CI plumbing | baselines, suppression comments, config files, SARIF, many entry points | ✅ |
| full type checking | which rules *may* conclude a non-`Bool` through a program's cases | ○ — [M3](design.md#7-roadmap) |
| the triple | does the signature agree with its `.eos` semantics, and those with SMT-LIB | ○ — [M4](design.md#7-roadmap) |
| solver-backed obligations | is this `:is-list-nil` predicate actually the operator's nil | ○ — [Tier 5](design.md#46-tier-5--opt-in-deeper) |
| editor integration | the same findings while typing, with hover types and cross-triple jumps | ○ — [M5](design.md#7-roadmap) |

---

## cvc5 — the calculus everything downstream is built from

**Today.** Three real defects, found on the first audit and confirmed against
ethos, plus documentation drift. Full write-up in [`findings.md`](findings.md);
the shareable version is [`report/cpc-audit.html`](report/cpc-audit.html).

**Why it matters here more than anywhere.** CPC is the input to the Lean
development, to the VC generator, and to every proof cvc5 emits. A defect in it
propagates: the same findings appear in `logos/install/defs/Cpc.eo`, because
that file is CPC flattened.

**What it gets next.** The triple checks, which is where the rest of the value
is for a calculus this size: every symbol having a semantics, every transform
naming something that exists, and the `:is-list-nil` obligations computed from
the signature rather than discovered when a stage fails.

**The honest limit.** Once the current findings are fixed, CPC will mostly be
clean, and anoieu's value there becomes regression protection: it fires on the
pull request that introduces the next one, which is worth having and is worth
less than the first run.

### Actions

**cvc5-1 (A)** — `proofs/eo/cpc/programs/Strings.eo:42` and `:55`. Both programs
declare `:signature ((Seq T)) Int` and every case returns a Boolean; their
docstrings say *"return: true if …"*. Change both return types to `Bool`.
Harmless today because every call sits inside an `eo::requires`, which compares
by evaluation; a call anywhere a `Bool` is expected is a type error naming
neither the program nor its declaration. Reported by `EO0064`.

**cvc5-2 (A)** — `proofs/eo/cpc/expert/theories/ArithExt.eo`. The four skolem
declarations at lines 17–20 are repeated verbatim at 26–29, comment included.
Ethos reads the repeat as an overload, so these are two distinct symbols that
print identically; a term built between the blocks would fail to match one built
after them, with `Proves:` and `Expected:` showing the same text. Delete the
second block. Reported by `EO0031`.

**cvc5-3 (A)** — 18 docstrings that no longer describe their declaration:
`symm` documents its premise under `; args:`, `string_decompose` takes two
premises and documents one, `quant_var_reordering` documents a premise it does
not have, and five programs document their pattern parameters as if they were
arguments. Reported by `DOC0011` and `DOC0012`; the list is one
`anoieu check --only DOC0011 --only DOC0012` away.

**cvc5-4 (A)** — `proofs/eo/cpc/programs/Utils.eo:123`. `$is_app` is declared,
documented, and named by no rule, program, definition or declaration. Delete it
or use it. Reported by `EO0060` under `--pedantic`.

**cvc5-5 (B)** — start report-only, so the four above are triaged without build
pressure, then baseline and block:

```json
{
  "entry_points": ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
  "baseline": "proofs/eo/anoieu-baseline.json",
  "severity": {"EO0054": "hint"}
}
```

Check the sources, not the generated artifacts. A whole-of-CPC run reads 51
files in well under a second.

## ethos — the proof checker, and its own signatures

*The ethos repository holds two tools: `ethos`, the C++ proof checker, and
`ethos-eoc`, the compiler built from `plugins/`. This section is the checker;
the next one is the compiler.*

**Today.** The `<` declared `:right-assoc` with a `Bool` return in
`tests/match-simple.eo` — inert since the file was written, because that test
only ever applies it to two arguments. More generally: ethos's test signatures
are small, numerous, and each exercised by exactly one proof, which is the
condition latent errors need. Plus better messages for four things ethos does
catch, and all of them at once instead of the first.

**The other half.** The specification work belongs to ethos as much as to us.
Each check ships with a manual page explaining what the language requires and
what ethos does with a file that breaks it; each has a witness; the desugarer is
validated case by case against the real parser. Where the two disagree, exactly
one is wrong, and the record of every narrowing so far reads as a list of facts
about Eunoia that were not written down anywhere.

**A possibility worth naming.** A check that proves uncontroversial is a check
ethos could adopt natively — the attribute contracts are declaration-time
properties it could enforce in twenty lines, and it would then need no external
tool for them. That would be a good outcome, not a loss.

### Actions

**ethos-1 (A)** — `tests/match-simple.eo:11`:
`(declare-const < (-> Int Int Bool) :right-assoc)`. A right-associative operator
folds its result back into its second argument, so its type must be
`(-> T1 T2 T2)`; every application of three or more arguments here is ill-typed.
Drop the attribute. Reported by `EO0040`.

**ethos-2 (A)** — an attribute ethos does not know prints
`Unsupported attribute :right-assoc-nill`, is dropped, and the run exits
`correct`. The declaration then means something else — the operator is no longer
variadic and every application of it builds a different term. Either refuse it,
or carry file and line on the warning so it can be found. Reported by `EO0020`.

**ethos-3 (A)** — the fields of `declare-rule` are read positionally, so writing
`:args` before `:premises` answers `Expected conclusion in declare-rule` at the
end of the command, naming a field that is not the problem. Reported by
`EO0021`, which points at the misordered keyword.

**ethos-4 (A)** — a program applied to the wrong number of arguments prints
`Wrong number of arguments when applying program $q, 3 arguments expected, got 2`
with no file and no line, and the run still exits `correct`. Reported by
`EO0066`, with the location.

**ethos-6 (A)** — two test signatures use literals whose category they never
declare, so those terms have no type. `right-assoc-variants.eo:48` gives `+` the
nil terminator `0` with no `(declare-consts <numeral> …)` anywhere in its
closure: the file passes ethos alone, and the first use of `+` produces
`(arith_typeunion_nary Int2 (arith_typeunion_nary Int2 eo::?))` — the `eo::?` is
the untyped nil. `:62` is the same for `""`, and `eo-definitions.eo` has four.
Reported by `EO0071`.

**ethos-7 (A)** — `tests/naive-nary.eo:182`. `isPermutation`'s first case
matches any pair of identical arguments, so its second case, which matches a
pair of identical `or`-terms, can never be reached. Reported by `EO0052`.

**ethos-5 (B)** — run over the test signatures. `anoieu check tests` reads 202
files under 191 entry points and reports **seven errors, three warnings and
three hints** in total — ethos-1, ethos-6, ethos-7, the `symm` docstring drift,
and three patterns that match exactly two elements. That is a job that could be
blocking on the day it is turned on. Its tests are not written to the docstring
convention, so:

```json
{ "entry_points": ["tests"], "disable": ["DOC0010", "DOC0011", "DOC0012"] }
```

A directory names every `.eo` under it, so `"entry_points": ["tests"]` is the
whole configuration.

## ethos-eoc — the Eunoia compiler

*Not the checker.* `ethos-eoc` is the second binary built from the ethos
repository — the core sources plus the `desugar`, `trim-defs`, `model-smt`,
`smt-meta` and `lean-meta` plugins, driven by `tools/eoc/driver.py`. It takes a
calculus and compiles it: into the Lean development logos is built from, into an
SMT-LIB verification condition per proof rule, and into a SyGuS query per rule.
Where the checker consumes a signature *and a proof*, the compiler consumes a
signature *and its semantics* — which is to say it consumes exactly the triple
anoieu is built to check.

**This is probably where anoieu pays off most, for three reasons.**

**Its failure modes are the late kind.** The compiler's own map of itself
(`docs/README.md` in the ethos tree) is a list of things nobody checks until
several tools downstream: a symbol with no semantics is fatal at stage 6, an
exclusion list that is not closed leaves a later stage naming something that was
dropped, a forward-declared program that is never defined reaches SMT-LIB as a
free uninterpreted function and Lean as a name that was never written, and a
missing termination clause surfaces when Lean runs. Each of those is decidable
from the two input files.

**Its feedback loop is the longest in the ecosystem.** Adding one symbol to a
calculus costs `sem_compile.py` → desugar → trim-defs → model-smt →
smt-meta/lean-meta → cvc5 or Lean before you learn whether it was right. That
document says outright there is "no way to ask *is this one block well-formed
against the embedding*" short of compiling the set. anoieu is that question,
answered in a second, before any stage runs.

**Its worst pain point is a check.** `is_list_nil` gets four pages of that
document and the verdict "the worst thing in the compiler". The desugar stage
forward-declares a nil predicate exactly when an operator's nil is non-ground;
the semantics defines one exactly when a human typed `:is-list-nil`; **nothing
compares the two**, and the failure mode for forgetting is silence. Whether a
nil is ground is syntactic, so anoieu can compute both sides from the input
files and diff them without running a stage. That is the compiler's own
direction #2, and its direction #5 — verify every `:exclude` name exists and
close the list under what it excludes — is the same shape.

Two more from the same list fall out: direction #4 asks for "a checkable unit
smaller than a set", which `anoieu symbol` already is for the signature side and
would extend to a block of an `.eos`; and the termination clauses a Lean run
needs can be predicted from the recursion analysis rather than discovered by
regenerating a package.

### Actions

**eoc-1 (B)** — a preflight in `driver.py`: run `anoieu check` over the
signature and the two `.eos` sets before stage 1, and refuse at launch what
would otherwise fail at stage 6 in a language the user was not writing in. This
is the integration that shortens the loop, and it is a few lines in the driver.

**eoc-2 (B)** — run over `tools/eoc/semantics/*.eos` and the signatures the
tests compile, in the same CI job that already runs `regress.py` and
`sem_compile.py --check`. Those two answer "did the output move" and "are the
generated files current"; anoieu answers the third question, "is the input
coherent", which nothing asks today.

**eoc-3 (A)** — implement the `is_list_nil` diff and the exclusion closure as
anoieu checks (M4), at which point the compiler can decide whether to keep its
own half of the arrangement or lean on the analyzer for it.

All three need the `.eos` front end, which is the next milestone.

## logos — the Lean development

**Today.** Little that is specific: the signatures it installs are flattened
copies of CPC, so it inherits CPC's findings and adds none of its own.

**What it gets next, and it is the largest single item on the roadmap.** logos
owns `Cpc.eos`, the official semantics of CPC, so the triple checks are what
anoieu can say here that nothing else does: which symbols have no semantics
block, which blocks name symbols nothing declares, whether the two type rules
agree at the sort level, which operators owe an `:is-list-nil`, and which
programs will need a hand-written `:lean` termination clause.

### Actions

**logos-1 (A)** — `install/defs/Cpc.eo` and `Cpc.cached.eo` carry cvc5-1.
Regenerate once it is fixed upstream; nothing to do in logos itself.

**logos-2 (B)** — run the triple, once it exists. logos already vendors ethos
and consumes cvc5's signature, so it is the natural place for the job — see the
open question below.

## eudaimonia — the template for other calculi

**Today.** Nothing beyond what any signature gets.

**What it is for.** eudaimonia's promise is that you bring a calculus and get a
checker. Its README specifies a *signature contract*: a binary `and` translated
to `SmtTerm.and` by the semantics, the Bool literals, and — only where rules
gather `:list` premises with `and` — a nil terminator on `and`. Its installer
checks all of it, against what the compiler emitted, because an operator's
compiled name need not be its spelling. The remaining gap is one of *timing and
subject*: the check reads the artifact after a checker has been generated, where
the same questions could be answered from the signature and semantics
beforehand, in the terms their author wrote.

### Actions

**eud-1 (B)** — a preflight: answer the contract's questions from the signature
and its semantics before generating anything, so that a calculus that cannot
meet the framework is refused in its author's own terms rather than in the
compiler's output. The installer's check stays as the backstop it is; this one
moves the first answer earlier. Needs the triple front end and nothing else.

**eud-2 (B)** — the calculus profile asks seven questions about a calculus and
answers five of them from what the compiler emitted; `binders` and
`value-ordering` are recorded on trust, because nothing in the *output*
distinguishes the answers. Both are properties of the signature and its
semantics, which is what anoieu reads: it can answer them from the input rather
than from the artifact, which is also the right place to answer them from.
eudaimonia's own note that `value-ordering` being declared "is a finding" is the
argument for doing it.

## Eunoia itself — the language and its manual

Eunoia is defined by [`user_manual.md`](https://github.com/cvc5/ethos/blob/main/user_manual.md)
in the ethos tree, and by ethos, which is where the definition is settled when
the two differ. anoieu is an accidental second reading of both: writing a
checker for a language you did not design surfaces every place the definition
under-determines behaviour, because the checker has to pick, and every pick is a
question somebody has to answer. This section is those questions.

### Where the manual says "must" and nothing checks

| the manual requires | ethos does | what we saw |
| --- | --- | --- |
| a `:right-assoc` operator has type `(-> T1 T2 T2)` | accepts any type | `<` in `tests/match-simple.eo`, ill-typed for every chain of three ([ethos-1](#ethos--the-proof-checker-and-its-own-signatures)) |
| a nil terminator has the operator's tail type | accepts any term | `:right-assoc-nil 0` on a `Bool` operator type checks until something asks for the type of a term built with it |
| a chainable operator's combiner is variadic | accepts a binary one | works at two and three arguments, fails at one and at four |
| opaque arguments come before ordinary ones, "otherwise all applications will be ill-typed" | accepts either order | every application of the symbol is ill-typed, reported at each use site |

A "must" that nothing enforces is a "should" in practice, and each of these is a
local property of one declaration — the check is a few lines wherever it goes.
That is [eunoia-3](#action-items).

### Where the definition is silent, and we had to find out

Each of these was established by experiment during this project. None is in the
manual; all four are things a person writing a signature has to know.

- **Matching does not check types.** `TypeChecker::match` says so in a comment —
  *"note that we do not ensure the types match here"* — so a parameter's declared
  type constrains nothing in a pattern, and a case whose arguments are all
  parameters matches every application and shadows every case after it.
- **A `define` body is never type checked without `:type`.** The body is built
  and stored; nothing asks its type. Most bodies in a signature carry no `:type`.
- **`eo::define` binds in parallel.** `(eo::define ((v a) (w b)) ...)` is fine;
  `(eo::define ((v a) (w (or v b))) ...)` answers `Could not find symbol v`. It
  is `let`, not `let*`, and neither the manual's grammar nor the `.eos` one says
  which — both show a single binding.
- **A repeated declaration with an identical type makes two symbols that print
  the same.** Overloading is by type, so the earlier one can never be selected;
  a term built before the second declaration then fails to match one built
  after it, and the report shows `Proves:` and `Expected:` as the same text.

To which add one the manual does state, whose consequence deserves stating too:
**program bodies are not type checked**, so a program's `:signature` return type
is a claim nothing verifies — which is how two CPC programs came to declare
`Int` and return `Bool` ([cvc5-1](#cvc5--the-calculus-everything-downstream-is-built-from)).

### What we would argue for

**eunoia-1 (C) — refuse a re-declaration whose type is identical.** Overloading
exists to give one name several *types*; two declarations of one name with one
type are indistinguishable to the resolver, so the earlier is dead and the pair
is a trap. The cost is a comparison at declaration time. The payoff is removing
the worst diagnostic in the ecosystem — a proof failure whose two sides print
identically — and it would have caught [cvc5-2](#cvc5--the-calculus-everything-downstream-is-built-from)
at the moment it was written.

**eunoia-2 (C) — an unknown attribute should be an error.** Today
`:right-assoc-nill` prints `Unsupported attribute`, is dropped, and the run exits
`correct` — with the operator no longer variadic and every application of it
building a different term. If tolerating unknown annotations matters, reserve a
prefix for them and refuse everything else.

**eunoia-3 (C) — enforce the four contracts above at the declaration.** Each
moves a failure from a use site in another file to the line that caused it.

**eunoia-4 (C) — decide what a well-formed signature is.** Either program case
bodies are type checked, and a signature that does not type check is not a
signature; or the manual says plainly that a program's declared return type is
documentation. The first is the honest reading of what `:signature` looks like it
means, and it would reject at least one signature in the wild today. The second
is free, and it should then be *written down*, because everything downstream —
the compiler, the Lean backend, the person reading the file — takes that
declaration at face value. anoieu currently takes the middle path: it reports
where the mismatch is decidable and says nothing where it is not.

**eunoia-5 (C) — write down that matching is untyped.** Making it typed would
silently change what existing programs match, so the cheap and probably correct
answer is a paragraph in the manual, plus the consequence: a case of all
parameters is a catch-all whatever its declared types say, and cases are tried in
order.

**eunoia-6 (C) — settle `eo::define` in the grammar.** Several bindings, bound
in parallel, is what ethos implements; the grammar shows one binding and says
nothing about scope.

**eunoia-7 (C) — say what `eo::hash` guarantees.** The manual says it returns "a
numeral unique to" a value, which is enough for a signature to reason through
and not enough for a model to follow: the Lean backend refuses to print the
program that would call it, so a calculus using hash is one no generated checker
can be built for. Either constrain it enough to model, or mark it as the one
operator that puts a rule beyond verification — which is a property a rule's
author would want to know about at the time.

**And one that is a discussion, not a proposal.** `:list` is declared on a
parameter but means something only where that parameter stands under an n-ary
head — so the same parameter can be a tail in one pattern and an element in
another, and a program in CPC does exactly that in adjacent cases. It is the
language's most common foot-gun, and the manual's own worked "incorrect version".
Whether the annotation belongs at the use site instead is a breaking question
worth asking once, rather than a change worth making quietly.

### What the tool would like from a future manual

Three things, all of which anoieu now has to carry instead: a normative
statement per attribute, saying which of its conditions are requirements; a
statement of *when* each requirement is checked, since the answer today ranges
from "at the declaration" to "when a proof reaches that case"; and the list of
what a pattern may not hold, which is currently discoverable only from an error
message. The check catalogue in [`checks.md`](checks.md) is close to being that
appendix, and it would be a better one if the manual and the checker agreed on
which of its entries are errors.

---

## How they fit together

**One tool, thin integrations.** anoieu stays one repository, released as one
versioned package. Each consuming repository owns exactly three things — its
entry points, its baseline, its severity policy — in one `anoieu.json` its own
reviewers can read. The CI job is then one line.

**The risk sits here, not there.** anoieu's own CI checks out cvc5 and ethos at
pinned refs and runs the analyzer against a baseline committed in this
repository. A change that invents a false positive fails *this* build before it
can fail anyone else's. That inversion is what earns the right to ask other
repositories to run this on every push.

**Pin a version.** A new check reaches a repository only when someone there
bumps the pin. Widening a check is a minor release, narrowing one is a patch,
renumbering is major.

**Four rungs, stop at any of them.** Report-only annotations → baseline and fail
on new errors → fail on new warnings → burn the baseline down and delete it.

**Order: ethos, cvc5 report-only, cvc5 blocking, ethos-eoc, logos.** Ethos is
the smallest surface and the right audience for language findings. cvc5 goes
report-only first so its findings get triaged without build pressure. The
compiler and logos arrive together with the triple, which is what makes them
worth wiring up.

The mechanics — workflow files, per-repository configuration, the ladder — are
in [`ci.md`](ci.md).

## What this is not

- **Not soundness.** Whether a proof rule is *valid* is what the verification
  conditions `ethos-eoc` emits are for. anoieu's question is the one below that:
  whether a signature and its semantics say something coherent at all.
- **Not a second checker.** Where a judgement needs the type checker or the
  evaluator, ethos is the authority, and anoieu says nothing rather than
  guessing. Every check that fired falsely on CPC was narrowed until it stopped;
  that record is the reason to believe the ones that remain.
- **Not a style tool.** The checks that are matters of taste on a signature that
  is already written are off by default.

## Open questions we are tracking

| question | why it matters | state |
| --- | --- | --- |
| Where does the triple job run? CPC's signature is in cvc5, its semantics in logos, and the compiler that reads both is in ethos. | The most valuable check will run in a repository that is not where its findings get fixed. | open; shapes what the `.eos` loader takes as input |
| Does cvc5 want its docstring convention enforced? | 18 findings today, and a doc generator would make them matter. | open |
| Should ethos absorb the declaration-time checks? | They are twenty lines there and would need no external tool. | open, and a good outcome either way |
| Should `driver.py` call anoieu, or should CI? | A preflight helps the person; a CI job protects the branch. They are not exclusive. | open (eoc-1) |
| How stable are check numbers? | Baselines and per-repository policy refer to them by code. | codes are permanent once released; a narrowed check keeps its number |
| Generated signatures in a corpus. | `Cpc.cached.eo` repeats what CPC says, so checking both reports everything twice. | resolved by convention: check sources, not artifacts |

## The documents

| file | what it is |
| --- | --- |
| [`usage.md`](usage.md) | the interface: inputs, commands, options, exit codes |
| [`ci.md`](ci.md) | running this in ethos, ethos-eoc, logos and cvc5 |
| [`checks.md`](checks.md) | every check and its manual page, generated from the registry |
| [`findings.md`](findings.md) | what the first runs found, and every false positive that had to be shed first |
| [`what-ethos-misses.md`](what-ethos-misses.md) | why ethos does not report these itself, by mechanism |
| [`language-notes.md`](language-notes.md) | what we have established about `.eo` and `.eos`, and where they are unsettled |
| [`design.md`](design.md) | the roadmap, the check catalogue, the architecture |
| [`report/cpc-audit.html`](report/cpc-audit.html) | the CPC audit, written for a reader outside the project |
