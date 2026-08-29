# anoieu — design notes

A brainstorm, not a plan. Everything here is a candidate; the ordering within
each section is rough value-to-cost. Claims about what ethos does and does not
check were verified against `ethos` built from `ethosEoc3` (see
[`language-notes.md`](language-notes.md) for the experiments).

---

## 1. Posture

Five commitments that decide most of the smaller questions.

**A linter that is wrong gets turned off.** Findings are graded, and the top
grade is reserved for things that are wrong under every reading:
`error` (no instantiation makes this work), `warning` (almost certainly a
mistake, but a reading exists), `hint` (style, convention, documentation).
Anything anoieu cannot decide it says nothing about. Silence on a hard case is
cheaper than a false positive on an easy one.

**Every finding has a witness.** "This rule can conclude a non-`Bool`" is a
claim, and the claim is worth more with the instantiation attached: *for
`F := (+ 1 1)`, the conclusion has type `Int`*. Witnesses are what let a user
confirm a finding in ten seconds, and what let anoieu's own test suite be a
corpus of `.eo` files rather than a corpus of assertions.

**No proof, no build, no solver** in the default path. `anoieu check Cpc.eo`
runs on a signature that has never been compiled, in an editor, in under a
second. Solver-backed checks exist (§4.6) but are opt-in.

**Report everything at once.** Ethos aborts on the first error, which is right
for a checker and wrong for the edit loop. anoieu recovers from syntax errors
and keeps going; a run over a 12,000-line signature should produce the whole
list.

**Adoptable on a signature that already exists.** CPC will light up on first
run. `--baseline` freezes today's findings so a team can adopt one check at a
time without a flag day.

---

## 2. What is already checked, and by whom

Duplicating an existing check is worse than useless — it trains people to ignore
the tool. The current division:

| checker | catches |
| --- | --- |
| `ethos` parser | grammar, arity of declared symbols, free parameters in a program case's RHS, evaluatable subterms in a pattern, forward-declared program type mismatch |
| `ethos` type checker | the type of any term it is *asked* for: a `define` with `:type`, a term a proof step builds, a rule application |
| `sem_compile.py` | `.eos` reference-level checks: every helper is written out, a case binds what it names, natives exist with the right arity, embedding types exist, block ordering, `--check` staleness |
| `model-smt` stage | every declared symbol has a semantics block |
| Lean / cvc5 | everything the compiler declined to check, one full regeneration later |

[`what-ethos-misses.md`](what-ethos-misses.md) sets out the same division by
mechanism -- why ethos does not report what it does not report -- with the
verified examples behind each.

The gaps `ethos/docs/README.md` names itself — the `:is-list-nil` diff,
exclusion closure, forward declarations never defined, a checkable unit smaller
than a whole configuration set — are all in anoieu's territory, and §4.4/§5.2
below are the response to them.

---

## 3. Two altitudes

A signature can be read at two heights, and different checks want different
ones.

- **Surface.** The file as written, with sugar intact: `(or x y z)`, `:list`
  parameters, binder syntax, overloaded names. This is where locations live, so
  every diagnostic is reported here.
- **Desugared.** What ethos actually builds: curried applications, nil
  terminators inserted, `eo::list_concat` where a `:list` parameter led, opaque
  applications for ambiguous constants. This is where typing and reachability
  are decidable without special cases.

anoieu should keep both and the map between them. A useful consequence: the
desugared altitude is exactly what `ethos-eoc`'s desugar stage already computes,
so the two can be compared on a corpus, which is the cheapest possible
conformance test of anoieu's own front end (§6, M2).

---

## 4. The check catalogue

Codes are sketched as `EO` (signature), `EOS` (semantics set), `TRI`
(cross-file), `DOC` (documentation). Every code gets a manual page — see §5.1,
because the manual pages are half the specification deliverable.

### 4.1 Tier 0 — syntax and structure

No name resolution, no types. Cheap, unglamorous, immediately useful in an
editor.

- Lexical and parse errors, **with recovery**, so a file reports all of them.
- Keyword-order errors in `declare-rule`. The fields are order-sensitive
  (`:assumption`, `:premises` | `:premise-list`, `:args`, `:requires`,
  `:conclusion`); writing `:args` before `:premises` gets you "Expected
  conclusion in declare-rule", which names neither the real problem nor its
  location.
- Misspelled attributes: `:right-assoc-nill`, `:premise`, `:implict`, `:opaqe`.
  A keyword that is not in the language should be an error rather than an
  ignored annotation.
- Duplicate declaration of a name (legal — it is overloading — but worth a hint
  when the two have the same type, which no application can ever tell apart).
- Reserved-name discipline: `eo::` is the builtin namespace, `$` marks a
  signature-internal helper, `@` a cvc5-internal symbol, `$eo_`/`$eoc_`/`$emb_`/
  `$sm_`/`$tsm_`/`$vsm_`/`$smtx_` are the compiler's. A user symbol landing in
  one of these is a collision waiting to happen; the compiler already refuses
  six families of them in `.eos`, and the signature side has no such check.
- Include graph: unresolved paths, cycles, a file included twice by two routes,
  an include whose symbols are never used.
- `declare-consts` for a literal category twice, or for a category the signature
  never uses.

### 4.2 Tier 1 — typing

The flagship tier. It needs a type checker for Eunoia — the real cost of this
project, and the thing that makes the rest possible.

- **Rule conclusions must be `Bool`.** The user's motivating example. A
  `declare-rule` whose conclusion has a non-`Bool` type is accepted by ethos and
  fails only at the first `step` that uses it. Three grades:
  - the conclusion is a term whose type is a ground non-`Bool` → `error`, the
    rule can never be applied;
  - the conclusion is an application of a program whose declared return type is
    not `Bool` → `error`;
  - the conclusion is a program application whose declared return is `Bool` but
    whose *cases* can return other types → `warning` with the witness case
    (this is the "may return a well-typed non-Bool term" case, and it is only
    visible if you look through the program, which nothing does today).
- **Program cases are type checked.** The manual says outright: "Terms in
  program bodies are not statically type checked." So for each case
  `((f p1 ... pn) r)`: each `pi` is of the type `:signature` declares for that
  place; `r`'s type is the declared return type; and where `:signature` uses
  `eo::quote`, the dependent binding is respected.
- **`define` bodies are type checked** even without `:type`. Ethos builds the
  term and never asks its type, so `(define P () (or a b))` where the desugaring
  inserts an `Int` nil into a `Bool` position is accepted, silently, forever.
- **Premise patterns are `Bool`**, and `:requires` pairs are typed.
- **Attribute contracts**, all stated in the manual, none enforced:
  - `:right-assoc-nil t` requires the operator to have type `(-> T1 T2 T2)` with
    `t : T2` (`:left-assoc-nil`, dually). Ethos accepts
    `(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)` without a word.
  - a non-ground nil terminator requires type `(-> T T T)`.
  - `:chainable c` requires `c` to be variadic; with a binary `c`, a chain of
    four arguments is a type error at the use site and a chain of one is an
    arity error, both reported far from the declaration that caused them.
  - `:pairwise`, `:arg-list`, `:binder` have analogous contracts.
  - opaque arguments must precede ordinary ones — the manual notes that
    otherwise *every* application is ill-typed, which is a declaration-time
    error waiting to be reported at declaration time.
- **Ambiguity**: an ambiguous constant or datatype constructor used without
  `as`; an application where more than one overload type checks (ethos silently
  takes the most recent and explicitly does not warn — anoieu can name every
  site where the choice was made for you).
- **Ill-typed by construction**: a term whose type is ground *and* evaluatable
  is ill-typed in Eunoia; that is a static property of the signature.
- **`eo::` misuse**: arity, and evaluation that can never succeed —
  `(eo::add 2 1/3)` (mixed categories), `(eo::extract s -1 3)` where the
  arguments are literals, `(eo::pow 2 -1)`, `(eo::to_str 200000)`. When both
  arguments are values, whether the operator evaluates is decidable, and a
  non-evaluating operator in a rule's conclusion means the rule cannot fire.
- **Programs applied to programs, builtins or oracles** are never invoked — the
  application is silently left unevaluated. Anything relying on that is a bug.

### 4.3 Tier 2 — behaviour of programs and rules

Still no solver; these are pattern-level analyses over the desugared form.

- **Unreachable case**: a case subsumed by an earlier one. Accepted silently
  today; almost always a mistake, since first-match-wins makes the later case
  dead.
- **Missing base case / stuck evaluation**: a program that matches `(and x xs)`
  and never `true` gets stuck at the end of every list. Report with a witness
  input. This is the single most common shape of side-condition bug.
- **The `:list` hazards**, which are Eunoia's most distinctive foot-gun and
  deserve their own family of checks:
  - forgetting `:list` — the manual's own "incorrect version": `(or l xs)` with
    an unmarked `xs` matches an `or` of *exactly two* children and silently
    fails on longer lists. Detectable as a pattern shape: a parameter in the
    tail position of an n-ary operator's pattern that is not marked `:list`;
  - marking two adjacent parameters `:list`, which desugars to
    `eo::list_concat` and makes the pattern illegal (ethos errors here, but the
    message is about an evaluatable subterm, not about the annotation);
  - a `:list` parameter used at a non-list position;
  - matching an n-ary operator without accounting for its nil.
- **Termination**: a recursive call that is not structurally smaller, and call
  cycles with no decreasing argument. Two payoffs — a genuine bug class, and a
  prediction of *which programs will need a hand-written `:lean` termination
  clause*, which today is discovered by regenerating a Lean package.
- **Rules that can never fire**: non-`Bool` conclusion (above); a premise
  pattern no well-typed term matches; a `:requires` pair whose sides are
  distinct values.
- **`:premise-list` operator must be variadic**, and `:assumption` rules must be
  applied with `step-pop` (a use-site check, for proof files).
- **Dead code**: programs no rule reaches, helper symbols nothing uses,
  parameters a declaration binds and never mentions.

### 4.4 Tier 3 — the triple

The reason the unit of analysis is three files. Most of these are today either
unchecked or checked two tools downstream.

- **Coverage, both directions.** A symbol with no semantics block is fatal at
  the model-smt stage; anoieu says it in a second, without a build. The converse
  — a block for a symbol the signature does not declare — nothing says at all.
- **Target existence and arity**: every symbol a `.eos` transform writes into
  exists in the SMT semantics with that arity, and every native exists in
  `natives.eos`.
- **Shape agreement between the two type rules.** Full agreement is a theorem
  and belongs to the VCs. *Sort-level* agreement is decidable and worth having:
  the signature says `concat : (-> (BitVec n) (BitVec m) (BitVec (eo::add n m)))`
  and the SMT semantics' `:typeof` case had better also produce a `BitVec`.
- **`:is-list-nil`, in both directions.** `ethos/docs/README.md` calls this the
  worst thing in the compiler, and its own direction #2 is exactly this check:
  the desugar stage forward-declares a nil predicate precisely when the nil is
  non-ground, the semantics defines one precisely when a human typed the
  attribute, and nothing compares the two. anoieu can compute the first from the
  signature alone — groundness of the nil term is a syntactic property — so it
  can do the diff *without running any stage*: missing (an undefined program
  reaches the backends, which under SMT is a free uninterpreted function) or
  dead (a definition nothing uses).
- **Exclusion closure**: `:exclude` names must exist (a typo excludes nothing,
  silently), and the set must be closed — excluding `lambda` and forgetting the
  rule written over it leaves a later stage naming something that was dropped.
- **Forward-declared programs that are never defined.**
- **Literal categories** in the signature ↔ `define-literal` in the SMT
  semantics, with agreeing type rules.
- **`.eos` role and form checks**: `define-sort`/`define-value`/`define-literal`
  are target-only, `define-method`/`define-rule` input-only, and nothing in the
  form says which — it is the role the file was named under. A set analyzed
  standalone can still be checked against both roles and report which one it
  can be.
- **`.eos` level and casting checks**, done from the file rather than by running
  `sem_compile.py`: the four levels (native / value / term / type) and the six
  refused name families. Same errors, better locations, no compile.
- **Termination clauses**: a `:lean` clause naming a program that no longer
  exists; a clause naming the native layer (refused by the stage); a program
  that needs one and has none (from §4.3's termination analysis).

### 4.5 Tier 4 — documentation

CPC's signature carries ~160 rule docstrings and ~80 program docstrings in a
consistent YAML-ish comment convention (`; rule:`, `; args:`, `; premises:`,
`; conclusion:`, `; return:`). Nothing parses them, so nothing keeps them true.

- Documented premise/argument names and counts match the declaration.
- Documented types match the declared types.
- `; return:` matches the `:signature` return type.
- Cross-references resolve: a docstring naming `$foo` or `ProofRule::SCOPE`
  where no such thing exists.
- Missing docstring on a public rule (a `hint`, opt-in).
- And the inverse of a checker: **generate the documentation** from the
  signature (§5.4). A doc generator is the reason to keep the docstrings honest,
  and the honesty check is the reason to trust the generated docs.

### 4.6 Tier 5 — opt-in, deeper

- **Discharge small obligations with cvc5.** `ethos/docs/README.md` direction #3
  proposes one VC per `:is-list-nil` block, since the intended meaning is
  written down: `($eo_is_list_nil f x)` ≡ `(eo::eq (eo::nil f (eo::typeof x)) x)`.
  Sort-agreement between the two type rules is another natural query. This is
  the boundary of anoieu's remit — not soundness of a *rule*, but coherence of
  the *description*.
- **Differential testing against ethos.** Generate well-typed terms for a
  signature; compare anoieu's predicted type and desugaring with what ethos
  builds. Finds bugs in anoieu, in ethos, and in the manual, and produces the
  conformance corpus that is half the specification deliverable.
- **Mutation coverage.** Mutate a rule; if the proof regression suite still
  passes, that rule is untested. Says something useful about a calculus's test
  coverage that nothing currently says.

---

## 5. User interfaces

### 5.1 The CLI, and the diagnostic format

```
anoieu check Cpc.eo                              # signature alone
anoieu check Cpc.eo --semantics Cpc.eos          # + the calculus semantics
anoieu check Cpc.eo --semantics Cpc.eos \
                    --smt-semantics smt.eos      # the whole triple
```

Diagnostics in the GCC/rustc shape, since every editor already parses it, with a
stable code per check:

```
Cpc.eo:412:3: error[EO0211]: rule `bv-eq-solve` can conclude a non-Bool term
   |
412|   :conclusion ($mk_bv_eq_solve x y)
   |               ^^^^^^^^^^^^^^^^^^^^ this has type (BitVec n) when x := #b0
   |
   = note: case 2 of `$mk_bv_eq_solve` (BitVectors.eo:87) returns a (BitVec n)
   = note: a step applying this rule fails with "Expected: Bool"
   = help: see `anoieu explain EO0211`
```

`--format=json|sarif|github` for CI; SARIF gets GitHub code-scanning annotations
for free. `--baseline`/`--update-baseline` for adoption on an existing calculus.
Inline suppression as a comment — `; anoieu: allow EO0211 <reason>` — which
also, deliberately, makes every suppression a searchable record of a place the
language surprised somebody.

`anoieu explain EO0211` prints the manual page for a code: what the rule is, why
it is a rule, a minimal example that triggers it, a minimal fix, and the passage
of the manual or the `.eos` README it comes from. **These pages are the
specification deliverable.** Writing the check and writing the page are the same
task.

### 5.2 `explain` — the checkable unit smaller than a file

`ethos/docs/README.md` direction #4 asks for a way to ask about one symbol
without compiling a set. That is a natural anoieu command, and it is the same
machinery as the checks:

```
anoieu explain --symbol str.++ Cpc.eo --semantics Cpc.eos
```

prints one page: the declaration and its attributes; what `(str.++ a b c)`
desugars to; the nil terminator and whether it is ground; the `.eos` block; what
that block compiles to; which rules and programs mention the symbol; and which
triple obligations it carries (`:is-list-nil` required? termination clause?).

`anoieu desugar <file>` and `anoieu desugar --term '(or x y z)' <file>` answer
the other half of the edit loop — *what did my sugar become* — which today is
answered by reading 660 lines of template or by running a stage.

### 5.3 Editor: LSP

The highest-value interface for the people writing these files daily, and the
reason error recovery is a requirement rather than a nicety.

- diagnostics as you type, whole-file;
- hover: the type of the subterm under the cursor, the desugared form of the
  application under the cursor, a symbol's attributes and nil;
- go-to-definition across the `include` graph, and across the triple — from a
  symbol in `.eo` to its `.eos` block and on to its SMT semantics;
- completion for `eo::` operators with their signatures and evaluation
  conditions, and for `.eos` attribute keywords by the role and kind of the
  entry being written;
- codelens on an n-ary application showing what it desugars to;
- document outline by theory / by section.

VS Code first; the protocol gets Emacs and Vim for free.

### 5.4 Reports

- **Triple coverage matrix.** Symbols down the side; declared / has semantics /
  target exists / `:is-list-nil` / termination clause / documented across the
  top. One page that says how far a calculus is from compiling.
- **Signature dashboard**: counts by theory, the rule table with each rule's
  computed conclusion type, the symbol→program→rule dependency graph, dead code.
- **Generated documentation** for a calculus, from the declarations and the
  docstrings (§4.5). "Doxygen for Eunoia" is a deliverable people would use
  even if it checked nothing.

### 5.5 Fixes

Where a finding has one obvious repair, offer it — as `--fix`, and as an LSP
code action:

- generate a skeleton `.eos` block for a symbol that has none, with the
  aggregates its kind requires;
- add a missing `:is-list-nil` attribute stub;
- add `:list` to the parameter the pattern-shape check flagged;
- reorder `.eos` blocks into dependency order (`sem_compile.py` reports the
  violation; nothing fixes it);
- normalize a rule's field order.

### 5.6 CI and the loop

`anoieu check --format=github` in cvc5's and ethos's CI; a pre-commit hook; and
a `--watch` mode that re-runs on save, which is the direct answer to the
feedback-loop complaint in `ethos/docs/README.md` §5.

---

## 6. Architecture

### The choice

**(A) Standalone front end.** anoieu parses `.eo`/`.eos` itself, models
desugaring, and implements its own type checker.
*For*: error recovery and multi-error reporting; LSP; analyses ethos's engine
cannot express (abstract types, "may return", reachability); runs where ethos is
not built; a second implementation is the best specification test there is.
*Against*: the type checker and desugaring are the hard parts of ethos, and a
divergence means anoieu is wrong about the language.

**(B) An ethos plugin.** The `Plugin` API already reports `bind`,
`defineProgram`, `markConstructorKind`, `define`, `includeFile`, and gets a
`finalize()` callback — enough to walk every program at the end and type check
each case with ethos's own type checker.
*For*: zero divergence, and the deep typing checks come almost free.
*Against*: C++; ethos aborts on the first error, so no multi-error reporting;
nothing to say about a file that does not parse; no editor story.

**(C) Hybrid — the recommendation.** Own front end (A) for everything, plus an
optional *oracle* mode that cross-checks against ethos where it is available:
the desugared form from the `desugar` stage, and types from a small plugin.
The oracle is not needed for a run; it is what the test suite uses, on every
push, over the whole corpus of `.eo` files in ethos, cvc5 and logos. Divergence
is a bug report against one of the two, and the accumulated agreements are the
conformance suite.

Implementation language: Python. The scale is small (CPC is ~12k lines total, a
non-issue), it matches the existing `tools/eoc/*.py` house style so the ethos
maintainers can read and extend it, `pygls` gives the LSP cheaply, and nothing
here is compute-bound. The parser and core IR should be written so a port is
possible if that changes.

### Shape

```
anoieu/
  syntax/     lexer, recovering parser, CST with spans   -- both languages
  resolve/    include graph, scopes, overload sets, the symbol table
  desugar/    the surface -> core map (n-ary, :list, binder, chainable,
              pairwise, arg-list, opaque, ambiguous)
  types/      the Eunoia type checker, conservative: every judgement is
              "yes", "no", or "cannot tell", and only "no" is reported
  eval/       an eo:: evaluator over values, for decidable-evaluation checks
  sem/        the .eos front end: roles, kinds, aggregates, levels, casting
  triple/     cross-file analyses
  checks/     one module per code, each with its manual page and its witnesses
  report/     diagnostics, formats, baselines, suppression
  ui/         cli, lsp, html reports
  corpus/     every .eo and .eos we can find, plus per-check witness pairs
```

Two things worth designing early because they are hard to retrofit: **spans on
everything** (a finding about a desugared term must point at the surface text
that produced it), and **a fact database** — if resolution and typing dump their
results as facts, then §4's checks are mostly queries over facts, ad-hoc
questions become `anoieu query` rather than a code change, and the reports in
§5.4 are views.

---

## 7. Roadmap

| | milestone | delivers |
| --- | --- | --- |
| **M0** ✅ | parser + CST + include graph, `check` with Tier-0 findings only | reads every `.eo` in ethos, cvc5, logos and eudaimonia without falling over; the corpus is established |
| **M1** ✅ | resolution, attribute contracts, dead code, docstring lint, `stats` | 30 checks, a witness apiece, and real findings on CPC and on `ethos/tests` -- see [`findings.md`](findings.md) |
| **M2** | desugaring + `explain`/`desugar` commands, validated against the desugar stage | the surface↔core map, and the conformance harness |
| **M3** | type checker → rule conclusions, program cases, `define` bodies, overload ambiguity | the flagship checks; the reason the tool exists |
| **M4** | `.eos` front end + triple checks, baselines, JSON/SARIF | the `is-list-nil` diff, exclusion closure, coverage matrix; CI-ready |
| **M5** | LSP, doc generation, opt-in solver obligations | the daily-driver interface |

What M1 taught, which was not in the plan: **the corpus is the design tool.**
Every check as first written had false positives on CPC, and every fix was a
statement about the language rather than about the code -- that a dependent
return type agrees with its argument at the constructor, that `eo::requires`
wraps a type without changing it, that a guarded recursive call is not a walk,
that a `define` alias and the term behind it are one term. The table at the end
of [`findings.md`](findings.md) is that record, and it is the part of M1 that
was specification work.

Running alongside all of it, not after it: `docs/eo-spec.md` and
`docs/eos-spec.md` grow one section per check implemented, and every check ships
with its witness pair in the corpus.

---

## 8. Open questions

For the record, and because several of them are places where the languages are
genuinely unsettled rather than merely undocumented — see
[`language-notes.md`](language-notes.md) §4.

1. Is an ill-typed `define` body an error in the language, or merely a term no
   one asked about? Ethos's answer today is the latter. anoieu's answer decides
   whether `EO01xx` is an `error` or a `warning`.
2. Are overlapping program cases intended? First-match-wins makes shadowing
   well-defined, so an unreachable case is a smell rather than an error — unless
   the language means to forbid it.
3. Is a nil terminator of the wrong type an error at declaration, or only at
   use? The manual says "must have type T2"; ethos accepts the declaration.
4. What exactly is a well-formed `.eos` *set*, independent of the role a run
   gives it? Today the role decides which forms are legal, and the role is a
   command-line option.
5. Should the `:is-list-nil` obligation stay in the model-semantics file, or
   move to a desugar-stage configuration (`ethos/docs/README.md` direction #1)?
   anoieu should be written so its check survives either answer.
6. How much of the SMT-LIB standard is fair game? A third reading of "SMT
   semantics" is conformance to the standard itself — a table of theory symbols
   and their types, against which a signature's declarations can be checked.
   Worth deciding whether that is in scope.
