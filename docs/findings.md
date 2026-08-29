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
| CPC (`Cpc.eo` and its include graph) | 35 | 0 | 32 (18 warnings, 14 hints) |
| `ethos/tests`, `logos/install/defs`, `eudaimonia/examples` | 193 | 0 | 42 |
| the whole of `logos` and `eudaimonia`, generated files and templates included | ~500 | 0 | — |

Reading the compiler's own `$MARKER$` templates reports what it should: a
template is not a signature until the markers are filled, and anoieu says so
rather than falling over.

## What ethos says about the same files

Every check owns a witness under `tests/witnesses`, and `tests/run.py --oracle`
runs ethos on each one:

**Of the 18 witnesses that hold the mistake, ethos accepts 14 and answers
`correct`.** It refuses four: a `declare-rule` field out of order, an opaque
argument after an ordinary one, a program case of the wrong arity, and a pattern
with two `:list` parameters. For those four anoieu's contribution is the message
and the location rather than the detection -- ethos reports the pattern one, for
instance, as `Cannot match on evaluatable subterm`, which names neither the
annotation nor the parameter.

The fourteen are the case for the tool.

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
| a name in the `$eo_` namespace collides with the compiler | `ethos/tests/eo-definitions.eo` defines the whole of `eo::` that way, deliberately | `$eo_` is reported only under `--pedantic`; the generated prefixes always |
| `declare-fun` is not a Eunoia command | true of a signature, false of a file named by `reference` | the loader tracks the role a file was read under |

That table is the M1 half of the specification work: each row is a question
about what a Eunoia signature means, which had to be answered before the check
could be written.
