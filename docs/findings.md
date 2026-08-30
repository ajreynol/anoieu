# What the first run found

The M1 checks, run over every signature we could find. This is the record of
what the tool says today and how each finding was confirmed, and it doubles as
the argument for the design: nearly everything reported here is something ethos
accepts without a word.

Reproduce with:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo
python3 tools/sweep.py <ethos>/tests <logos>/install/defs <eudaimonia>/examples
ETHOS=<ethos>/build/src/ethos python3 tests/run.py --oracle
```

## The corpus

| tree | files read | crashes | findings |
| --- | --- | --- | --- |
| CPC (`Cpc.eo` and its include graph) | 35 | 0 | 35 (3 errors, 18 warnings, 14 hints) |
| CPC expert (`expert/CpcExpert.eo`) | 21 | 0 | 6 warnings |
| `ethos/tests`, `logos/install/defs`, `eudaimonia/examples` | 193 | 0 | 42 |
| the whole of `logos` and `eudaimonia`, generated files and templates included | ~500 | 0 | — |

Reading the compiler's own `$MARKER$` templates reports what it should: a
template is not a signature until the markers are filled, and anoieu says so
rather than falling over.

## What ethos says about the same files

Every check owns a witness under `tests/witnesses`, and `tests/run.py --oracle`
runs ethos on each one:

**Of the 37 witnesses that hold the mistake, ethos accepts 32 and answers
`correct`.** It refuses five: a `declare-rule` field out of order, an opaque
argument after an ordinary one, a program case of the wrong arity, a pattern
with two `:list` parameters, and a builtin applied to the wrong number of
arguments. For those five anoieu's contribution is the message and the location
rather than the detection -- ethos reports the pattern one, for instance, as
`Cannot match on evaluatable subterm`, which names neither the annotation nor
the parameter.

The thirty-two are the case for the tool.
[`what-ethos-misses.md`](what-ethos-misses.md) says why each of them gets past
ethos.

## Real bugs in CPC

Three, so far. Each was confirmed by constructing the smallest signature that
reproduces it and running ethos on it.

### `$is_seq_const` and `$is_seq_const_rec` declare the wrong return type

`programs/Strings.eo:42` and `:55`:

```lisp
(program $is_seq_const_rec ((T Type) (e T) (ss (Seq T) :list))
  :signature ((Seq T)) Int          ; <- Int
  (
  (($is_seq_const_rec (seq.++ (seq.unit e) ss))   ($is_seq_const_rec ss))
  (($is_seq_const_rec (as seq.empty (Seq T)))     true)      ; <- Bool
  (($is_seq_const_rec ss)                         false)     ; <- Bool
  )
)
```

Every case returns a Boolean, the docstring says *"return: true if s is a
sequence constant"*, and the signature says `Int`. Program bodies are not type
checked, so ethos accepts it.

**Corrected, after cvc5 assessed it.** The finding was right and both signatures
now return `Bool` -- but our claim about *when* it bites was too strong, and the
correction is worth more than the finding.

We wrote that a use where a `Bool` is expected is a type error, from this
reproduction:

```text
$ ethos t.eo          ; (and ($is_const x) true)
Error: Type checking failed: Checking application of and
  Term: ($is_const x)   Has type: Int   Expected type: Bool
```

That program's application *cannot evaluate* -- its argument is a parameter --
so the declared return type is what a caller sees. `$is_seq_const` is total over
its argument, and ethos evaluates the application before consulting the declared
type, so cvc5 found that a direct typed use checks as `correct`. The declared
`Int` surfaces only where an application stays stuck.

So this was an internal inconsistency and a hazard for static tools and future
consumers, not a demonstrated failure of a current proof. Three claims we now
keep apart, in cvc5's words: a declaration that disagrees with its cases; an
application that may remain stuck and expose the declared return type; and a
concrete term that current ethos rejects. It also reaches the downstream pipeline unchanged -- the same
three findings appear in `logos/install/defs/Cpc.eo` and `Cpc.cached.eo`, the
flattened copies the Lean development is built from.

Reported by **EO0064**.

### Four skolem declarations are duplicated verbatim in the expert signature

`expert/theories/ArithExt.eo`, lines 17-20 and again at 26-29, comment included:

```lisp
; skolems for virtual term substitution
(declare-const @arith_vts_delta Real)
(declare-const @arith_vts_delta_free Real)
(declare-parameterized-const @arith_vts_infinity ((T Type)) T)
(declare-parameterized-const @arith_vts_infinity_free ((T Type)) T)
```

Ethos treats a repeated declaration as an overload, and two declarations of one
name with one type are two *distinct symbols that print identically*. Nothing is
wrong today, because the second copy shadows the first before any term is built
from it -- but the failure mode it sets up is the worst one available:

```text
$ ethos c1.eo         ; a term built before the second copy, compared with one after
Error: Unexpected conclusion for rule refl:
    Proves: (_ (= d) d)
  Expected: (_ (= d) d)
```

A proof failure whose two sides are the same text. Anything later that builds a
term with one of these symbols between the two blocks -- a nil terminator, a
`define`, a rule -- turns the duplication into that.

Reported by **EO0031**.

### `<` is declared `:right-assoc` with a `Bool` return -- `ethos/tests/match-simple.eo:11`

```lisp
(declare-const < (-> Int Int Bool) :right-assoc)
```

A right-associative operator folds its result back into its second argument, so
its type must be `(-> T1 T2 T2)`. This one returns `Bool` where it takes an
`Int`, so every application of three or more arguments is ill-typed:

```text
Error: Type checking failed: (_ (< 1) (_ (< 2) 3))
       Checking application of (< 1): unexpected type of child #1
```

The test only ever applies `<` to two arguments, so the attribute has been inert
since it was written.

Reported by **EO0040**.

### Three more, in ethos's own test signatures

Found by the checks over the builtin layer, added after the first audit.

**A nil terminator with no type.** `ethos/tests/right-assoc-variants.eo:48`
declares `+` with `:right-assoc-nil 0`, and the file -- which includes nothing --
never says what a numeral is. The signature passes ethos alone, because nothing
asks; the first use of `+` shows what it built:

```text
Error: Expression of unexpected type:
Expression: (eo::define ((_v0 (+ q))) (_ _v0 (_ _v0 0)))
      Type: (arith_typeunion_nary Int2 (arith_typeunion_nary Int2 eo::?))
  Expected: Int2
```

`eo::?` is the untyped nil. Line 62 is the same for `""`, and
`tests/eo-definitions.eo` -- the manual's own derived-operator signature -- has
four numerals in typed positions with no `<numeral>` declared. Reported by
`EO0071`.

**A case that can never be reached.** `ethos/tests/naive-nary.eo:182`:

```lisp
(program isPermutation ((l1 Bool) (l2 Bool) (ls Bool) (ls2 Bool))
    :signature (Bool Bool) Bool
    (
        ((isPermutation l1 l1) true)
        ((isPermutation (or l1 l2) (or l1 l2)) true)     ; <- dead
        ...
```

The first case matches any pair of *identical* arguments -- one parameter twice,
so matching binds it once and checks the second occurrence agrees -- which is
exactly what the second case matches. Reported by `EO0052`, whose subsumption
test is what sees it.

### The first run over a whole triple

cvc5's `Cpc.eo`, logos's `Cpc.eos`, ethos's `smt.eos` and the embedding they are
written against, checked together:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo \
  --semantics <logos>/install/defs/Cpc.eos \
  --smt-semantics <ethos>/tools/eoc/semantics/smt.eos \
  --embedding <ethos>/plugins/model_smt/model_smt.eo
```

One finding: `Cpc.eos:546` has `(define-symbol str.indexof_re_split (s r q))`,
and CPC declares no such operator — it declares `str.indexof_re`. The name is
real on the *target* side (`smt.eos:1639` defines it) and another entry
transforms into it at line 584, which is legitimate; what is dead is the
input-side entry, which no compilation reaches.

The other four checks — coverage, the `:is-list-nil` diff, exclusion closure and
transformation targets — reported nothing on this run. That is a fact about
those four checks and not about the triple: each is partial, each has been
narrowed until it stopped over-reporting, and nothing here licenses a conclusion
that the signature, the semantics and the target agree. See *What we do not
publish* in the top-level README.

### An inventory, not a defect: the rules a calculus admits

`EO0077` reports every rule marked `:sorry`. Both hits in the corpus are
intentional — CPC's `trust` rule, which carries every inference cvc5 has not
formalised and says so in its own docstring, and `ethos/tests/sorry.eo`, which
tests the feature. The check stays as a hint: it answers "which rules is this
proof's verdict resting on" without grep, and a calculus where the answer grows
is a calculus worth asking about.

### One that is only a bug from the wrong entry point

`$evaluate_list` is forward-declared in `programs/Utils.eo:70` and defined in
`Cpc.eo:347`, so a run whose entry point is `expert/CpcExpert.eo` alone has it
declared and never defined. In practice cvc5's regression runner writes
`(include ".../Cpc.eo")` before `(include ".../expert/CpcExpert.eo")`
(`test/regress/cli/run_regression.py:372`), so the pair is always loaded
together and the gap never opens. Reported by **EO0057**, which now says "under
this entry point" for exactly this reason.

## Findings worth reading

### `<` declared `:right-assoc` with a `Bool` return — `ethos/tests/match-simple.eo:11`

```lisp
(declare-const < (-> Int Int Bool) :right-assoc)
```

A right-associative operator folds its own result back into its second argument,
so its type has to be `(-> T1 T2 T2)`. This one returns `Bool` where it takes an
`Int`, so *every* application of three or more arguments is ill-typed.
Confirmed:

```text
$ ethos t.eo
Error: Type checking failed: (_ (< 1) (_ (< 2) 3))
       Checking application of (< 1): unexpected type of child #1
```

The declaration has stood since the test was written, because the test only ever
applies `<` to two arguments and the attribute is inert until someone does not.

### Documentation that no longer describes its rule — CPC, 18 findings

CPC documents each rule and program in a comment block, and nothing checks them.

- `symm` (`rules/Uf.eo:31`) documents `F` under `; args:`; the rule declares it
  as a premise and takes no arguments.
- `string_decompose` (`rules/Strings.eo:191`) takes two premises and documents
  one.
- `quant_var_reordering` documents a premise for a rule that has none.
- `$re_ac_merge`, `$derivative` and three other programs document their pattern
  parameters as if they were arguments, so the counts disagree with
  `:signature`.

None of these is a bug in the calculus. All of them are wrong in the file, and a
generated documentation page would print them.

### A program nothing reaches — CPC

`$is_app` (`programs/Utils.eo:123`) is declared, documented and never named by a
rule, a program, a definition or a declaration. Reported as a hint under
`--pedantic`.

### Patterns that match exactly two elements — 14 in CPC, 31 across the corpus

Reported as hints, because a pattern that means "exactly two" is legal and
common. The interesting ones are where a single program does both:
`$str_arith_entail_is_approx` (`programs/Strings.eo:1745`) matches `(+ n1 n2)`
with the tail marked `:list` and `(* n1 n3)` with it unmarked, in adjacent
cases, so the same program walks a sum of any length and a product of exactly
two factors.

## What the corpus taught the checks

Every one of these was a false positive on the first run, and the fix is
recorded because it is a statement about the language:

| first attempt | what the corpus said | what the check does now |
| --- | --- | --- |
| a right-associative operator's return type must *equal* its second argument type | `concat : (-> (BitVec n) (BitVec m) (BitVec (eo::add n m)))` is fine: the type is dependent and agrees where it matters | compare type *constructors*, and say nothing when either side is a type parameter |
| ... and `(-> T T (eo::requires ($is_arith_type T) true T))` is not an arrow at all | `eo::requires` wraps a type without changing it | strip `eo::requires` before comparing |
| a program matching an n-ary application needs a case for the operator's nil | `$get_zero` matches `(or b1 b2)` to say what `or`'s unit *is*, and walks nothing | require a recursive call on the tail, and no guard on it |
| ... and `$re_nullable` has no case for `@re.empty` | `@re.empty` is a `define` for `(str.to_re "")`, which it does have a case for | expand `define` aliases before comparing terms |
| ... and `$str_fixed_len_re` recurses on a union tail with no base case | the call stands under `(eo::ite (eo::eq r1 re.none) ...)`, which never reaches the nil | a call guarded by a test on the tail is not a walk |
| ... and `$str_re_consume_inter` has no case for `re.all` | its first case matches `(re.inter c1)`, a list of exactly one element, which ends the recursion a step early | a fixed-length case of the same operator ends the walk |
| a nil that is not covered is a finding | most nils in CPC are non-ground -- `($seq_empty (Seq T))`, `(eo::to_bin m 0)` -- and each instance spells its base case differently (`""` for strings) | say nothing when the nil is non-ground |
| a symbol's return type is what its declaration says | `ite : (-> Bool A A A)` returns `A`, which says nothing until the arguments say what `A` is | bind a callee's type parameters from the arguments, and answer `None` if any stays unbound |
| a type is what it is written as | `String` is a `define` for `(Seq Char)`, `@List` for `eo::List` | expand aliases before comparing two types |
| any two different type heads disagree | `T`, `U`, `S` are type variables, and a head that is not a declared type constructor cannot be compared at all | compare only heads that resolve to a declared type constructor |
| a literal needs a declared category wherever it stands | `(eo::add 1 1)` evaluates in a signature that declares no numerals: ethos distinguishes a numeral *value* independently of its type | report only literals standing where a type is asked for, which meant modelling which positions those are |
| a term that cannot evaluate is a finding wherever it stands | `(eo::is_ok X)` *asks* whether X evaluates, and ethos's own operator tests are full of `(eo::is_ok (eo::pow 2 -1))` | say nothing beneath an `eo::is_ok` |
| an `eo::` name is a computational operator | `eo::List::cons` and `eo::List::nil` are constructors of the builtin list, and patterns match them constantly | test membership of the operator table, never the `eo::` prefix — a mistake made twice, in two checks, before the table was reused |
| a parameter shadowing a declared symbol is a hazard | it is idiomatic: a program parameterised by an operator names its parameter `cons`, `nil` or `f`, and ethos's own tests do it 150 times | the check was written, measured, and deleted |
| a name in the `$eo_` namespace collides with the compiler | `ethos/tests/eo-definitions.eo` defines the whole of `eo::` that way, deliberately | `$eo_` is reported only under `--pedantic`; the generated prefixes always |
| `declare-fun` is not a Eunoia command | true of a signature, false of a file named by `reference` | the loader tracks the role a file was read under |

That table is the M1 half of the specification work: each row is a question
about what a Eunoia signature means, which had to be answered before the check
could be written.
