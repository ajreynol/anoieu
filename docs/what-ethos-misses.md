# What ethos misses, and why

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

**Of the 32 witnesses that hold the mistake, ethos accepts 27 and answers
`correct`.**

---

## 1. Ethos is demand-driven: it types a term only when something asks

Ethos is a proof checker, and its speed comes from computing a type on demand.
A signature is not a thing it validates; it is the vocabulary a proof is checked
against. Three consequences.

### A `define` body is never type checked without `:type`

```lisp
(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
(declare-const a Bool) (declare-const b Bool)
(define P () (or a b))              ; accepted: "correct"
(define P () (or a b) :type Bool)   ; the same body: type error on the nil
```

The term is built and stored. Nothing asks its type, so nothing notices it has
none. `:type` is optional, so most bodies in a signature are never typed at all.

### Program bodies are not type checked, at all

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

### A rule's conclusion is typed at the first `step`, not at the declaration

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

## 2. Ethos checks terms; it never checks a declaration's contract

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

## 3. Ethos ignores what it does not understand

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

## 4. Matching is untyped and first-match-wins, so nothing is ever "dead"

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

## 5. Ethos stops at the first error, and reports where it noticed

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

## 6. Ethos reads one file role, and never reads comments

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

## Where the line honestly falls

Ethos is the ground truth for typing and evaluation, and it refuses five of the
thirty-two witnesses: a `declare-rule` field out of order, an opaque argument
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
[`findings.md`](findings.md), because each is a statement about what the language
means.

## The classes, and where each stands

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
