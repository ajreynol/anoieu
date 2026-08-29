# What we have established about `.eo` and `.eos`

Working notes, kept because the second goal of this project is to make both
languages better understood. Sources: `ethos/user_manual.md` (2,362 lines, the
`.eo` reference), `ethos/tools/eoc/semantics/README.md` (1,252 lines, the `.eos`
reference), `ethos/tools/eoc/README.md`, `ethos/docs/README.md`, and experiments
against `ethos` built from `ethosEoc3`.

---

## 1. `.eo` — the shape of the language

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

## 2. `.eos` — the shape of the language

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

## 3. What ethos does not check — verified

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

## 4. Where the languages are unsettled

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

## 5. Corpus

What exists to test against, all present locally:

| tree | content |
| --- | --- |
| `ethos/tests` | 204 files, small and adversarial — the closest thing to a language test suite |
| `cvc5/proofs/eo/cpc` | CPC: ~11,700 lines across `Cpc.eo`, 11 theories, 12 rule files, 11 program files; ~160 rule docstrings |
| `ethos/tools/eoc/semantics` | `smt.eos` (1,837 lines, 132 symbols, 9 sorts, 14 values, 5 literals, 67 programs) and `development-cpc.eos` (1,123 lines, 182 symbols) |
| `ethos/plugins/*/*.eos` | the native layers and the aggregate table — four more dialects of the same language |
| `logos/install/defs` | `Cpc.eos`, the official CPC semantics |
| `eudiamonia` | a template for other calculi — the second and third triples that will exist |
