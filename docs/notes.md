# Notes

The miscellany: why the tool can find what it finds, what we had to establish
about the languages in order to write it, and what is built, rejected or still
open. Working notes rather than a specification — the nearest thing to a
specification is the check catalogue in [`checks.md`](checks.md), where every
page is written beside the code it describes.

Anything that does not belong in the other five documents belongs here.

## What ethos misses, and why

This is the argument for the tool, written by *mechanism* rather than by check.
Six things about how ethos works account for nearly everything anoieu can find,
and knowing which is which is how you tell where the next check will come from.

Every claim here was run against `ethos` built from `ethosEoc3` at commit
`2118635d`; source references are to that tree. The witnesses under
`tests/witnesses` hold each example, and `tests/run.py --oracle` re-runs ethos
over all of them:

```bash
ETHOS=<ethos>/build/src/ethos python3 tests/run.py --oracle
```

**Of the 49 witnesses that hold the mistake, ethos accepts 43 and answers
`correct`.**

---

### 1. Ethos is demand-driven: it types a term only when something asks

Ethos is a proof checker, and its speed comes from computing a type on demand.
A signature is not a thing it validates; it is the vocabulary a proof is checked
against. Three consequences.

#### A `define` body is never type checked without `:type`

```lisp
(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
(declare-const a Bool) (declare-const b Bool)
(define P () (or a b))              ; accepted: "correct"
(define P () (or a b) :type Bool)   ; the same body: type error on the nil
```

The term is built and stored. Nothing asks its type, so nothing notices it has
none. `:type` is optional, so most bodies in a signature are never typed at all.

#### Program bodies are not type checked, at all

The user manual says so (`user_manual.md:1727`):

> Terms in program bodies are not statically type checked. Evaluating a program
> may introduce non-well-typed terms if the program body is malformed.

`ExprParser::typeCheckProgramPair` (`src/expr_parser.cpp:1256`) is the whole of
what a case is checked for: that the right-hand side binds nothing the left-hand
side did not, and that no pattern holds an evaluatable subterm. No types
anywhere. So this stands in a signature indefinitely:

```lisp
(program $mk ((x Int) (F Bool)) :signature (Bool) Bool
  ( (($mk (not F)) F)
    (($mk F)       (+ 1 1)) ))     ; Int where Bool was declared
```

A proof that exercises the first case checks `correct`. A proof that exercises
the second fails with `Expected: Bool`. Nothing in between says the signature was
already wrong.

#### A rule's conclusion is typed at the first `step`, not at the declaration

`declare-rule` desugars to a program over premises and arguments, and its return
type is *set* to `Bool` (`src/cmd_parser.cpp:491`, in the `DECLARE_RULE` case at
line 382) rather than checked against the conclusion:

```lisp
(declare-rule bad-conc ((x Int)) :args (x) :conclusion (+ x 1))   ; accepted
(step @p0 (+ a 1) :rule bad-conc :args (a))
;; Error: Expression of unexpected type: (_ (+ a) 1)  Type: Int  Expected: Bool
```

**The class is latent errors.** Ethos's verdict on a signature depends on which
proof you happen to run; anoieu's does not. The deepest version of it is a rule
whose conclusion is `($mk F)` where `$mk` is *declared* to return `Bool` and has
cases that return other types: ethos can only ever see the branch a given proof
took, and deciding "this rule may conclude a well-typed non-`Bool` term" means
looking through the program at every case. That needs the type checker, and is
M3.

---

### 2. Ethos checks terms; it never checks a declaration's contract

An attribute is parse-time metadata. Nothing compares it with the type it is
written on, so a broken contract fails later, elsewhere, in a term the reader
never wrote.

| written | what the manual requires | when it fails | check |
| --- | --- | --- | --- |
| `(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)` | the nil has the operator's tail type | at the first `or` term whose type is asked for | EO0041 |
| `(declare-const < (-> Int Int Bool) :right-assoc)` | type `(-> T1 T2 T2)` | at the first application of three or more arguments | EO0040 |
| `(declare-const >= (-> Int Int Bool) :chainable and)`, `and` binary | the combiner is variadic | at four arguments (`Non-function ... as head of APPLY`) and at one (`Incorrect arity`) | EO0042 |
| an opaque argument after an ordinary one | opaque arguments come first | at *every* application, all of which are ill-typed | EO0046 |

The second is in the ethos tree today, at `tests/match-simple.eo:11`. It has
never fired because that test only ever applies `<` to two arguments.

Each of these is decidable from the declaration alone, with no type checker,
which is why they are in M1.

---

### 3. Ethos ignores what it does not understand

A misspelled attribute is not an error. `ExprParser` looks the keyword up, does
not find it, warns, and stores a dummy (`src/expr_parser.cpp:1014`):

```text
$ ethos t.eo
Unsupported attribute :right-assoc-nill
t.eo:1.62: Unhandled attribute NONE
correct
```

Exit code 0. The declaration keeps its meaning *minus the annotation*: `or` is
no longer variadic, so every application of it now builds a different term, and
nothing downstream mentions it again. That is why EO0020 is an error rather than
a warning.

---

### 4. Matching is untyped and first-match-wins, so nothing is ever "dead"

`TypeChecker::match` binds a parameter to whatever stands in its place, and says
so in its own comment (`src/type_checker.cpp:494`):

```cpp
// note that we do not ensure the types match here
```

So a case whose arguments are all parameters matches every application whatever
their declared types, and every case written after it is unreachable. Ethos has
no reason to notice: it simply never gets there (EO0052).

The same blindness covers a family of questions about a signature *as a whole*,
which a checker that evaluates one term at a time never asks:

- a program declared with no body and never defined, which reaches the SMT
  backend as a free uninterpreted function and Lean as a name that was never
  written (EO0057);
- a program nothing reaches -- `$is_app` in CPC's `programs/Utils.eo` is
  declared, documented, and named by nothing (EO0060);
- a parameter no case mentions (EO0056);
- a program that walks an n-ary list and has no case for the nil that ends it:
  the last step of the recursion does not evaluate, and what a proof reports is
  that a step failed to check (EO0053);
- a pattern that matches an n-ary operator of exactly two elements because a
  tail parameter is not marked `:list` -- the manual's own worked "incorrect
  version", where the program works on short lists and silently fails on long
  ones (EO0054).

---

### 5. Ethos stops at the first error, and reports where it noticed

Two differences even for what ethos does catch.

**One diagnostic per run.** A parse error is a `Fatal failure` and the process
aborts, so a file with three mistakes takes three runs. anoieu recovers and
reports the file.

**The location is the symptom, not the cause.** Write `:args` before `:premises`
in a `declare-rule` and ethos answers `Expected conclusion in declare-rule`,
pointing at the end of the command and naming a field that is not the problem;
the fields are read positionally, so the parser stops where it expected the
conclusion. anoieu points at the misordered keyword and states the order
(EO0021). Likewise two `:list` parameters in one pattern: ethos says `Cannot
match on evaluatable subterm`, naming neither the annotation nor the parameter,
because by then the pattern has already been desugared into an
`eo::list_concat` (EO0055).

---

### 6. Ethos reads one file role, and never reads comments

- **Documentation.** CPC documents 166 of its 593 rules in a structured comment
  convention that nothing parses, so nothing keeps it true. Real drift: `symm`
  documents its premise under `; args:`; `string_decompose` takes two premises
  and documents one; `quant_var_reordering` documents a premise it does not
  have. Ethos cannot have an opinion here -- they are comments (DOC0010-0012).
- **The pipeline past ethos.** A signature declaring `$sm_foo` or `$eoc_bar` is
  fine under ethos and collides with what `ethos-eoc` generates (EO0030).
- **The triple.** Ethos knows nothing of `.eos`. Every cross-file question is
  invisible to it by construction: a declared symbol with no semantics block, a
  block for a symbol nothing declares, a transform whose target does not exist
  in the SMT semantics, an `:is-list-nil` that is required and missing (or
  present and dead), an `:exclude` list that is not closed under what it
  excludes. That is M4, and `ethos/docs/README.md` asks for most of it by name.

---

### Where the line honestly falls

Ethos is the ground truth for typing and evaluation, and it refuses six of the
forty-nine witnesses: a `declare-rule` field out of order, an opaque argument
after an ordinary one, a program case of the wrong arity, a pattern with two
`:list` parameters, and a builtin operator applied to the wrong number of
arguments. For those, anoieu contributes the message, the location, and
the fact that it reports them *alongside* everything else rather than instead of
everything else.

The discipline runs the other way too. M1 is deliberately type-free, so it stays
silent wherever a judgement would need the type checker. Every check had false
positives on CPC in its first form, and each fix narrowed it: a dependent return
type agrees with its argument at the *constructor*, `eo::requires` wraps a type
without changing it, a guarded recursive call is not a walk, a `define` alias and
the term behind it are one term. Those narrowings are recorded in
[`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed), because each is a statement about what the language
means.

### The classes, and where each stands

| class | the mechanism it exploits | status |
| --- | --- | --- |
| attribute contracts | §2, declarations unvalidated | live: EO0040, EO0041, EO0042, EO0046 |
| dead, unreachable, stuck | §4, untyped first-match | live: EO0052, EO0053, EO0056, EO0057, EO0060 |
| silently ignored input | §3 | live: EO0020 |
| the builtin layer — arity, impossible evaluations, untyped literals, list operators over non-n-ary symbols | §1, nothing asks for the value | live: EO0071–EO0074 |
| documentation drift | §6 | live: DOC0010, DOC0011, DOC0012 |
| better location, whole-file reports | §5 | live, in every check |
| compiler-namespace collisions | §6 | live: EO0030 |
| a rule that may conclude a non-`Bool`; program case return types; `define` bodies | §1, demand-driven typing | M3, needs the type checker |
| the triple: coverage, transform targets, `:is-list-nil`, exclusion closure | §6, one file role | M4 |


## What we have established about `.eo` and `.eos`

Working notes, kept because the second goal of this project is to make both
languages better understood. Sources: `ethos/user_manual.md` (2,362 lines, the
`.eo` reference), `ethos/tools/eoc/semantics/README.md` (1,252 lines, the `.eos`
reference), `ethos/tools/eoc/README.md`, `ethos/docs/README.md`, and experiments
against `ethos` built from `ethosEoc3`.

---

### 1. `.eo` — the shape of the language

Eunoia is a logical framework in SMT-LIB 3.0 clothing. Terms, types and kinds
share one grammar; all functions are unary and all applications curried
(`(f a b)` is `(_ (_ f a) b)`); `Type`, `->`, `_`, `Bool`, `true`, `false` are
the only builtin constants, and every theory is a signature rather than a
builtin.

Five things carry most of the language's weight, and every one of them is a
place a signature can go wrong quietly.

**Declarations.** `declare-const`, `declare-parameterized-const` (named,
possibly `:implicit`, possibly `:opaque` arguments, dependent return types),
`declare-consts` (a literal category has a type, possibly computed from
`eo::self`), `declare-datatype(s)`, `define` (a *macro*, expanded at parse
time, with an optional `:type` that is the only thing that makes it type
checked).

**Sugar on applications.** `:right-assoc`, `:left-assoc`, the `-nil` variants,
`:right-assoc-non-singleton-nil`, `:chainable`, `:pairwise`, `:arg-list`,
`:binder`, and the `:list` annotation on parameters that says a parameter is a
*tail* rather than an element. The desugaring is precisely specified in the
manual and is where the language's characteristic bugs live: `(or l xs)` with an
unmarked `xs` matches an `or` of exactly two children, and two adjacent `:list`
parameters desugar to an `eo::list_concat` that is then illegal as a pattern.

**Computation.** ~50 `eo::` operators over the literal categories (numeral,
decimal, rational, binary, hexadecimal, string) plus 18 list operators over
`f`-lists, all with the same discipline: they evaluate on values of the right
category and are *left unevaluated* otherwise. No mixed arithmetic. `eo::eq` and
`eo::is_eq` are syntactic. `eo::hash` is deliberately underconstrained, which is
why the Lean backend refuses to model it.

**Programs.** An ordered list of rewrite rules, first match wins, with a
declared `:signature` and optional `eo::quote` for dependent argument binding.
Crucially: *program bodies are not statically type checked* — the manual says
so — and cases are checked only for free parameters and for evaluatable
subterms in patterns.

**Proof rules.** `declare-rule` desugars to a program over premises and
arguments returning the proven formula; `assume` to a `declare-const` of
`(Proof f)`; `step` to a `define` with `:type (Proof f)`. Proof checking *is*
type checking, in a type system with `Proof` and `Quote` types the user cannot
name. Ethos additionally requires every well-typed term's type to be either
non-ground or fully reduced.

### 2. `.eos` — the shape of the language

Newer, smaller, and specified by one README plus the compiler that reads it. A
**set** is one file of s-expressions, and there are nine forms and no others:
`section`, `define-macro`, `program`, `define-symbol`, `define-sort`,
`define-value`, `define-literal`, `define-method`, `define-rule` (plus
`declare-native` and `define-native-method` in the native-layer sets, and
`declare-aggregate-method` in the aggregate table). Anything else is refused —
a set says what a theory *does*, never what the embedding *is*.

Four ideas are doing the work:

**Roles.** A set is a *target* (`smt.eos` — what an SMT-LIB symbol means to a
model) or an *input* (`Cpc.eos` — what a calculus symbol becomes in the
embedding). Which forms are legal depends on the role, and the role is given by
the command-line option that names the file, not by anything in it.

**Aggregates.** Each symbol contributes one *case* to each of a set of big
programs — `$smtx_typeof`, `$smtx_model_eval`, `$eo_to_smt`, and so on — and
which aggregates exist is itself configuration
(`plugins/model_smt/model_smt.eos`), read by the stage out of the head of the
generated file. This is the extensible axis, and it works: adding an attribute a
symbol may carry is three edits and no rebuild.

**Levels.** A term is written at one of four levels — native, value, term, type
— and *which one is never written down*: it is read off the type of the place
the term stands in. A bare `f` compiles to `$native_f`, `$smtx_model_eval_f`,
`$sm_f` or `$tsm_f` accordingly. Elegant, and the single hardest thing about
writing a block.

**Macros and layer prefixes.** `smt.` names the SMT-LIB layer, `eo.` the input
as the desugar stage embeds it; both are ordinary `define-macro`s in an
`embedding.eo`, expanded before anything else sees them, legal in patterns as
well as in terms.

### 3. What ethos does not check — verified

Each of these was run against `ethos` (`ethosEoc3`). They are the empirical core
of the case for this tool.

**A rule may conclude a non-`Bool` term.** The declaration is accepted; the
first `step` using it fails.

```lisp
(declare-rule bad-conc ((x Int)) :args (x) :conclusion (+ x 1))   ; accepted
(step @p0 (+ a 1) :rule bad-conc :args (a))
;; Error: Expression of unexpected type: (_ (+ a) 1)  Type: Int  Expected: Bool
```

**A program case may have the wrong return type, and lie dormant.** The case
below is only reached by a proof that takes the second branch:

```lisp
(program $mk ((x Int) (F Bool)) :signature (Bool) Bool
  ( (($mk (not F)) F)
    (($mk F)       (+ 1 1)) ))     ; Int where Bool was declared -- accepted
```

A proof exercising the first case checks `correct`; one exercising the second
fails with `Expected: Bool`. Nothing between the two says the signature was
already wrong.

**A `define` body is never type checked without `:type`.**

```lisp
(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
(declare-const a Bool) (declare-const b Bool)
(define P () (or a b))              ; accepted: "correct"
(define P () (or a b) :type Bool)   ; the same body: type error on the nil
```

**A nil terminator of the wrong type is accepted at declaration.** The `0`
above is an `Int` nil for a `Bool` operator; the manual requires it to have the
operator's tail type. Nothing complains until a term is built *and* its type is
asked for.

**A `:chainable` operator with a non-variadic combiner is accepted.**
`(declare-const >= (-> Int Int Bool) :chainable and)` with a binary `and`
declares fine, works for two- and three-argument chains, and fails for four
(`Non-function ... as head of APPLY`) and for one (`Incorrect arity for and`).

**Unreachable program cases are accepted silently.** A general pattern before a
specific one makes the specific one dead; nothing says so.

The pattern behind all six: **ethos is lazy on purpose.** It checks what a proof
asks it to check, which is what makes it a fast proof checker, and it means the
well-formedness of a *signature* — as opposed to the validity of a *proof* — is
currently nobody's job.

### 4. Where the languages are unsettled

Not documentation gaps: places where there is a real question and the current
answer is whatever the implementation does.

- **What does "well-formed signature" mean?** Ethos has no such notion. If
  every `define` body and every program case had to type check, several
  signatures in the wild would need changes; if they do not, then a signature is
  well-formed exactly when the proofs people happen to write against it check.
- **Are overlapping program cases legal?** First-match-wins makes shadowing
  well-defined, so unreachability is a smell, not a violation — unless the
  language intends coverage/disjointness, which nothing states.
- **What is the status of the attribute contracts?** The manual says a nil
  terminator "must" have type `T2` and a chainable combiner "should" be
  variadic. Ethos enforces neither. Both readings are defensible; only one can
  be the specification.
- **What is a well-formed `.eos` set independent of its role?** Today the role
  decides which forms are legal and the role is a command-line option, so the
  same file is well-formed or not depending on how it is named.
- **What is the exact contract of `:is-list-nil`?** Its meaning is written down
  — `($eo_is_list_nil f x)` ≡ `(eo::eq (eo::nil f (eo::typeof x)) x)` — but it is
  hand-written per operator, required when the nil is non-ground, and compared
  with nothing. `ethos/docs/README.md` §10 is a full account of why.
- **`eo::typeof` in desugared output is an approximation** (monomorphised per
  partial application) and nothing in the output marks which parts are exact.
- **How much of SMT-LIB is assumed?** `smt.eos` is one reading of the standard,
  written for one target. Whether a signature's `+` is *SMT-LIB's* `+` is a
  question no tool asks, and CPC's own header lists the places cvc5 deliberately
  differs (mixed arithmetic, variadic operators with nil, strings as sequences).

### 5. Corpus

What exists to test against, all present locally:

| tree | content |
| --- | --- |
| `ethos/tests` | 204 files, small and adversarial — the closest thing to a language test suite |
| `cvc5/proofs/eo/cpc` | CPC: ~11,700 lines across `Cpc.eo`, 11 theories, 12 rule files, 11 program files; ~160 rule docstrings |
| `ethos/tools/eoc/semantics` | `smt.eos` (1,837 lines, 132 symbols, 9 sorts, 14 values, 5 literals, 67 programs) and `development-cpc.eos` (1,123 lines, 182 symbols) |
| `ethos/plugins/*/*.eos` | the native layers and the aggregate table — four more dialects of the same language |
| `logos/install/defs` | `Cpc.eos`, the official CPC semantics |
| `eudiamonia` | a template for other calculi — the second and third triples that will exist |


## The design

A brainstorm, not a plan. Everything here is a candidate; the ordering within
each section is rough value-to-cost. Claims about what ethos does and does not
check were verified against `ethos` built from `ethosEoc3` (see
[`notes.md`](notes.md#what-we-have-established-about-eo-and-eos) for the experiments).

---

### 1. Posture

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

**Defects out, assurances never.** The tool reports what is wrong and says
nothing about what is right. A check that finds nothing means only that it found
nothing: the analysis is partial by design, every check has been narrowed until
it stopped over-reporting, and whole classes of error are outside it. Publishing
a clean result as a property of the artifact would hand the next reader — or the
next analysis tool built on this one — a confidence we cannot support, and that
is harder to take back than a false positive. It also shapes the output format:
there is no score, no coverage percentage, and no summary that reads as a
verdict.

**Findings are addressed to someone else.** Almost nothing this tool reports is
about this tool: a finding is about a file in cvc5, ethos, logos or the language
itself, and it will be read by the person who wrote that file, who did not ask
for it. Three design consequences follow, and they are why the first four
commitments are worth their cost: a finding must carry its own reproduction,
because the reader has no reason to trust us; the record of what a check gets
*wrong* has to be public, because that is what makes what it gets right
believable; and every ask has to live in one place with a state on it, or it
becomes an argument repeated monthly. That place is
[`reports.md`](reports.md#the-register-what-anoieu-is-asking-and-of-whom) -- the register of what anoieu is asking of whom.

---

### 2. What is already checked, and by whom

Duplicating an existing check is worse than useless — it trains people to ignore
the tool. The current division:

| checker | catches |
| --- | --- |
| `ethos` parser | grammar, arity of declared symbols, free parameters in a program case's RHS, evaluatable subterms in a pattern, forward-declared program type mismatch |
| `ethos` type checker | the type of any term it is *asked* for: a `define` with `:type`, a term a proof step builds, a rule application |
| `sem_compile.py` | `.eos` reference-level checks: every helper is written out, a case binds what it names, natives exist with the right arity, embedding types exist, block ordering, `--check` staleness |
| `model-smt` stage | every declared symbol has a semantics block |
| Lean / cvc5 | everything the compiler declined to check, one full regeneration later |

[`notes.md`](notes.md#what-ethos-misses-and-why) sets out the same division by
mechanism -- why ethos does not report what it does not report -- with the
verified examples behind each.

The gaps `ethos/docs/README.md` names itself — the `:is-list-nil` diff,
exclusion closure, forward declarations never defined, a checkable unit smaller
than a whole configuration set — are all in anoieu's territory, and §4.4/§5.2
below are the response to them.

---

### 3. Two altitudes

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

### 4. The check catalogue

Codes are sketched as `EO` (signature), `EOS` (semantics set), `TRI`
(cross-file), `DOC` (documentation). Every code gets a manual page — see §5.1,
because the manual pages are half the specification deliverable.

#### 4.1 Tier 0 — syntax and structure

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

#### 4.2 Tier 1 — typing

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

#### 4.3 Tier 2 — behaviour of programs and rules

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

#### 4.4 Tier 3 — the triple

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

#### 4.5 Tier 4 — documentation

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

#### 4.6 Tier 5 — opt-in, deeper

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

### 5. User interfaces

#### 5.1 The CLI, and the diagnostic format

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

#### 5.2 `explain` — the checkable unit smaller than a file

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

#### 5.3 Editor: LSP

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

#### 5.4 Reports

- **Triple coverage matrix.** Symbols down the side; declared / has semantics /
  target exists / `:is-list-nil` / termination clause / documented across the
  top. One page that says how far a calculus is from compiling.
- **Signature dashboard**: counts by theory, the rule table with each rule's
  computed conclusion type, the symbol→program→rule dependency graph, dead code.
- **Generated documentation** for a calculus, from the declarations and the
  docstrings (§4.5). "Doxygen for Eunoia" is a deliverable people would use
  even if it checked nothing.

#### 5.5 Fixes

Where a finding has one obvious repair, offer it — as `--fix`, and as an LSP
code action:

- generate a skeleton `.eos` block for a symbol that has none, with the
  aggregates its kind requires;
- add a missing `:is-list-nil` attribute stub;
- add `:list` to the parameter the pattern-shape check flagged;
- reorder `.eos` blocks into dependency order (`sem_compile.py` reports the
  violation; nothing fixes it);
- normalize a rule's field order.

#### 5.6 CI and the loop

`anoieu check --format=github` in cvc5's and ethos's CI; a pre-commit hook; and
a `--watch` mode that re-runs on save, which is the direct answer to the
feedback-loop complaint in `ethos/docs/README.md` §5.

---

### 6. Architecture

#### The choice

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

#### Shape

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

### 7. Roadmap

| | milestone | delivers |
| --- | --- | --- |
| **M0** ✅ | parser + CST + include graph, `check` with Tier-0 findings only | reads every `.eo` in ethos, cvc5, logos and eudaimonia without falling over; the corpus is established |
| **M1** ✅ | resolution, attribute contracts, dead code, docstring lint, `stats` | 30 checks, a witness apiece, and real findings on CPC and on `ethos/tests` -- see [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) |
| **M2** ✅ | desugaring + `desugar`/`symbol` commands, validated against ethos | the surface↔core map, and the conformance harness: 34 cases, one per policy, agreeing with ethos term for term |
| **M3** ◐ | type checker → rule conclusions, program cases, `define` bodies, overload ambiguity | the flagship checks; the reason the tool exists. The *shallow* half is written -- the type of a term where its head settles it, with a callee's type parameters bound from the arguments (`anoieu/typing.py`) -- which is what found the CPC return-type bug. What it still cannot do: type a term whose head is a parameter, follow `eo::` evaluation, or check a `define` body against a use site |
| **M4** ✅ | `.eos` front end + triple checks, baselines, JSON/SARIF | the CI plumbing (see [`reporting-workflow.md`](reporting-workflow.md#running-it-in-ci)) and the `.eos` reader, which is vocabulary-agnostic by design because the language is moving: five checks over the triple, including the `is-list-nil` diff and exclusion closure the compiler's own documentation asks for. The first run over the real CPC triple -- cvc5's signature, logos's semantics, ethos's SMT semantics -- reported one dead entry and nothing else |
| **M5** | LSP, doc generation, opt-in solver obligations | the daily-driver interface |

What M1 taught, which was not in the plan: **the corpus is the design tool.**
Every check as first written had false positives on CPC, and every fix was a
statement about the language rather than about the code -- that a dependent
return type agrees with its argument at the constructor, that `eo::requires`
wraps a type without changing it, that a guarded recursive call is not a walk,
that a `define` alias and the term behind it are one term. The table at the end
of [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) is that record, and it is the part of M1 that
was specification work.

Running alongside all of it, not after it: `docs/eo-spec.md` and
`docs/eos-spec.md` grow one section per check implemented, and every check ships
with its witness pair in the corpus.

---

### 7a. Maintenance coherence — moved

What must remain true of the record after any edit, whoever made it, and which
of those a machine can check, is now [`coherence.md`](coherence.md#the-open-technical-work)
— together with what this repository is responsible for and which documents may
not be changed without asking. It is the entry point for maintenance work.

---

### 8. A neighbouring tool

[**dokimasia**](https://github.com/ajreynol/dokimasia) analyses cvc5's
proof-production code — the C++ — and asks a completeness question about it:
not *is this proof step valid* but *is there a path through the solver that
reaches an inference no proof step covers*, particularly under
`--safe-mode=safe`, where cvc5 promises that anything it solves it can prove. It
reads eight stages of the pipeline, from configuration through elaboration to
the Eunoia serialiser, and says it models itself on this tool.

**They do share a position**, if not a line of code: what may be published about
somebody else's work, what a finding is worth, and why nothing crosses a
repository boundary on its own. That is written down once, here, in
[`reporting-policy.md`](reporting-policy.md), and referenced from there.

**Technically the two barely overlap, and it is worth being clear why.** anoieu reads
`.eo` and `.eos` files and asks whether a *signature and its semantics* are
coherent; dokimasia reads C++ and asks whether the *solver* can justify what it
decides. Different inputs, different question, no shared code, and neither
depends on the other.

They meet at exactly one seam: `src/proof/eo/`, where cvc5 turns an internal
proof into Eunoia. A rule that cvc5 emits but CPC does not declare, or declares
with different arguments, is invisible to both halves in isolation and visible
from either side of that seam — which is what
[`cvc5-6`](reports.md#cvc5--the-calculus-everything-downstream-is-built-from)
asks for. That check may well belong there rather than here: dokimasia already
reads the emitter, and we only read the signature. Worth settling before either
of us builds it twice.

### 9. Open questions

For the record, and because several of them are places where the languages are
genuinely unsettled rather than merely undocumented — see
[`notes.md`](notes.md#what-we-have-established-about-eo-and-eos) §4.

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
