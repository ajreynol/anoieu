# The checks

One page per check, rendered from the registry by `tools/gen_checks_doc.py`;
each page is written beside the check it explains, so the two cannot drift.
`anoieu explain <CODE>` prints the same text.

A check is `on` unless it says otherwise: the ones that are off by default are
those whose findings are a matter of taste on a signature that is already
written, and `--pedantic` turns them on.


| code | says | default |
| --- | --- | --- |
| [DOC0001](#doc0001) | a rule or program with no docstring | off |
| [DOC0010](#doc0010) | a docstring names something other than what it documents | on |
| [DOC0011](#doc0011) | a docstring documents a different number of premises or arguments | on |
| [DOC0012](#doc0012) | a docstring documents a field the declaration does not have | on |
| [EO0001](#eo0001) | a lexical error | on |
| [EO0002](#eo0002) | a form that is never closed, or a `)` that closes nothing | on |
| [EO0003](#eo0003) | a token standing outside any command | on |
| [EO0010](#eo0010) | an include that does not resolve | on |
| [EO0011](#eo0011) | the include graph has a cycle | on |
| [EO0020](#eo0020) | an attribute that is not in the language | on |
| [EO0021](#eo0021) | a field of declare-rule written out of order | on |
| [EO0022](#eo0022) | a malformed typed parameter | on |
| [EO0023](#eo0023) | a rule with no conclusion | on |
| [EO0024](#eo0024) | a malformed program case | on |
| [EO0025](#eo0025) | a literal category the language does not have | on |
| [EO0026](#eo0026) | a command a signature file may not hold | on |
| [EO0030](#eo0030) | a declared name collides with the compiler's namespace | on |
| [EO0031](#eo0031) | an overload no application can tell apart | on |
| [EO0040](#eo0040) | an associative operator's type does not have the shape the attribute requires | on |
| [EO0041](#eo0041) | a nil terminator does not have the operator's tail type | on |
| [EO0042](#eo0042) | the operator an attribute names is not variadic, or does not exist | on |
| [EO0046](#eo0046) | an opaque argument stands after an ordinary one | on |
| [EO0051](#eo0051) | a program case does not match the program's signature | on |
| [EO0052](#eo0052) | a program case can never be reached | on |
| [EO0053](#eo0053) | a program walks a list and has no case for its end | on |
| [EO0054](#eo0054) | a pattern matches a fixed number of elements of an n-ary operator | on |
| [EO0055](#eo0055) | a pattern desugars to something that cannot be matched on | on |
| [EO0056](#eo0056) | a parameter nothing uses | off |
| [EO0057](#eo0057) | a program is declared and never defined | on |
| [EO0060](#eo0060) | a program nothing reaches | off |
| [EO0062](#eo0062) | a rule concludes a term that is not a Bool | on |
| [EO0063](#eo0063) | a rule takes a premise that is not a Bool | on |
| [EO0064](#eo0064) | a program case returns a type the program does not declare | on |
| [EO0065](#eo0065) | a symbol is applied to more arguments than it takes | on |
| [EO0066](#eo0066) | a program is applied to the wrong number of arguments | on |
| [EO0067](#eo0067) | a requirement that can never hold | on |
| [EO0069](#eo0069) | a premise list gathered by an operator that is not variadic | on |
| [EO0070](#eo0070) | a program case that calls itself with the arguments it just matched | on |
| [EO0071](#eo0071) | a literal whose category the signature never gave a type | on |
| [EO0072](#eo0072) | a builtin operator is applied to the wrong number of arguments | on |
| [EO0073](#eo0073) | an evaluation the language says cannot happen | on |
| [EO0074](#eo0074) | a list operator applied to something that is not an n-ary operator | on |
| [EO0076](#eo0076) | a `:list` annotation that does nothing | off |

## DOC0001

**a rule or program with no docstring**

*Off by default; run with `--pedantic` or `--only DOC0001`.*

Off by default. A signature that documents most of its rules is saying that the
undocumented ones are an oversight.

## DOC0010

**a docstring names something other than what it documents**

The `; rule: X` or `; program: X` line above a declaration names what it
documents. When the two disagree, one of them was renamed and the other was not,
and the docstring is now attached to the wrong thing.

## DOC0011

**a docstring documents a different number of premises or arguments**

`; premises:` and `; args:` list one `- name: description` item per premise and
per argument. A count that disagrees with the declaration means a premise or an
argument was added or removed on one side only.

A rule written with `:premise-list` takes any number of premises, so its
docstring is not counted.

## DOC0012

**a docstring documents a field the declaration does not have**

A docstring that documents an assumption, premises or a requirement the rule
does not have describes a rule that was changed underneath it.

## EO0001

**a lexical error**

An unterminated string or quoted symbol, or a character the language has no
token for. anoieu recovers and keeps reading, so one of these does not hide the
rest of the file.

## EO0002

**a form that is never closed, or a `)` that closes nothing**

Reported at the `(` that has no `)`, rather than at the end of the file, which
is where a parser that only counts brackets notices.

## EO0003

**a token standing outside any command**

Every top-level form of a signature is a command, i.e. a list. A bare token at
the top level is usually a stray fragment of an edit -- or a template marker,
if the file is one of the compiler's `$MARKER$` templates rather than a
signature.

## EO0010

**an include that does not resolve**

An include path is resolved against the directory of the file that includes it,
not against the working directory of the run.

## EO0011

**the include graph has a cycle**

Ethos includes a file once, so a cycle terminates rather than looping -- but it
means the order symbols are declared in depends on which file a run started
from, and a signature that only works from one entry point is a signature with a
latent error.

## EO0020

**an attribute that is not in the language**

Ethos prints `Unsupported attribute :foo` and carries on. The declaration keeps
its meaning *minus the annotation*, so a misspelled `:right-assoc-nil` leaves
an operator that is not variadic, every application of it means something else,
and the run still ends in `correct`. That is why this is an error rather than a
warning: nothing downstream will mention it again.

## EO0021

**a field of declare-rule written out of order**

`declare-rule` reads its fields positionally, in the order `:assumption`,
`:premises` | `:premise-list`, `:args`, `:requires`, `:conclusion` |
`:conclusion-explicit`. A field out of order stops the parser where it expected
the conclusion, so ethos answers `Expected conclusion in declare-rule` at the
end of the command -- several lines after the field that caused it.

## EO0022

**a malformed typed parameter**

A typed parameter is `(<symbol> <type> <attr>*)`.

## EO0023

**a rule with no conclusion**

Every rule ends with `:conclusion` or `:conclusion-explicit`.

## EO0024

**a malformed program case**

A case of a program is a pair `(<pattern> <term>)`.

## EO0025

**a literal category the language does not have**

The categories are `<boolean>`, `<numeral>`, `<decimal>`, `<rational>`,
`<binary>`, `<hexadecimal>` and `<string>`.

## EO0026

**a command a signature file may not hold**

Signature files and proof files are read as Eunoia; only a file named by
`reference` is read as SMT-LIB. So `declare-fun`, `assert` and `check-sat` in a
signature are an error -- ethos answers `Expected Eunoia command` -- and the same
commands in a referenced `.smt2` file are ordinary.

## EO0030

**a declared name collides with the compiler's namespace**

`ethos-eoc` generates names under fixed prefixes: `$eo_` for the Eunoia deep
embedding, `$sm_`/`$tsm_`/`$vsm_` for the SMT term, type and value families,
`$smtx_` for the programs written over them, `$native_` for the native layer,
`$eoc_` for what a configuration block compiles to. A signature that declares
one of those is fine under ethos and collides under the compiler, where the
generated file holds two declarations of one name.

## EO0031

**an overload no application can tell apart**

Overloading is resolved by the type of the application: ethos takes the most
recently declared symbol of that name whose application type checks. Two
declarations of one name with the *same* type are therefore indistinguishable,
and ethos says nothing, by design, so that a signature may order declarations by
precedence.

The consequence is worse than a dead declaration. The two are *distinct
symbols*, so a term built between them is not equal to a term built after them,
and the two print the same:

    Error: Unexpected conclusion for rule refl:
        Proves: (_ (= d) d)
      Expected: (_ (= d) d)

A duplicated `declare-const` -- the copy-paste kind -- is therefore a proof
failure waiting for the first term that is built before the second copy, with a
diagnostic that shows nothing.

## EO0040

**an associative operator's type does not have the shape the attribute requires**

A constant marked `:right-assoc` (or a `-nil` variant) must have a type of the
form `(-> T1 T2 T2)`, and one marked `:left-assoc` a type of the form
`(-> T1 T2 T1)`: the fold has to be able to put its own result back into the
argument it came from. Ethos does not check this. A declaration that breaks it
type checks, and the first application of it fails somewhere else.

## EO0041

**a nil terminator does not have the operator's tail type**

`:right-assoc-nil t` inserts `t` at the tail of every application of the
operator, so `t` must have the operator's second argument type (for
`:left-assoc-nil`, its first). Ethos checks nothing at the declaration:

    (declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)   ; accepted

and `(define P () (or a b))` is then accepted too, because a `define` body with
no `:type` is never type checked. The error surfaces the first time anything
asks for the type of a term built with the operator.

This check reports only when both types can be read off the declarations: a
literal whose category has a `declare-consts`, a declared constant, or an
application of one.

## EO0042

**the operator an attribute names is not variadic, or does not exist**

`:chainable c`, `:pairwise c`, `:arg-list c` and `:binder c` each hand `c` a
number of arguments that depends on the application, so `c` has to accept any
number of them -- it must itself be marked `:right-assoc`, `:left-assoc`, one of
the `-nil` variants, or `:chainable`.

With a binary `c`, ethos accepts the declaration and the consequence appears at
a use site: a chain of three arguments works, one of four fails with
`Non-function ... as head of APPLY`, and a chain of one fails with
`Incorrect arity`.

## EO0046

**an opaque argument stands after an ordinary one**

The manual: "Opaque arguments should always be expected before other arguments.
Otherwise all applications of the given function will be ill-typed." That is a
property of the declaration, so it can be said at the declaration rather than at
every application of it.

## EO0051

**a program case does not match the program's signature**

A program declares its arity with `:signature`, and every case has to match it.
A case of the wrong arity can never fire.

## EO0052

**a program case can never be reached**

A program is an *ordered* list of rewrite rules, first match wins, and matching
does not check types -- `TypeChecker::match` binds a parameter to whatever term
stands in its place. So an earlier case shadows a later one whenever its pattern
is the more general of the two: a case whose arguments are all parameters
matches every application, and `(($p (or x xs) l) ...)` matches everything
`(($p (or a xs) l) ...)` does.

Patterns are compared after desugaring, since that is what matching sees: a
`:list` parameter in a tail position stands for a list of any length, and one
that is not stands for a list of exactly the length written.

## EO0053

**a program walks a list and has no case for its end**

A program that matches `(f x xs)` with `xs` marked `:list` and then calls itself
on `xs` is walking an f-list, and needs a case for the nil that ends it --
`(($p false) ...)` for an `or`-list, `(($p true) ...)` for an `and`-list -- or a
parameter that catches it. Without one the last step does not evaluate, and what
a proof reports is that a step failed to check, not that a case was missing.

The recursive call is what identifies a walk. A program that merely *matches* an
application of an n-ary operator -- to say what its unit is, say -- is not
walking anything and is not reported.

## EO0054

**a pattern matches a fixed number of elements of an n-ary operator**

For an operator with a nil terminator, `(or l xs)` is sugar for
`(or l (or xs false))`: it matches an `or` of *exactly two* elements. Marking
`xs` with `:list` in the enclosing parameter list is what makes it match the
tail. The manual gives this as its own worked "incorrect version": the program
works on two-element lists and silently fails to evaluate on longer ones, which
in a proof surfaces as a checking failure with no indication of the cause.

A pattern that really does mean "exactly two elements" is legal and common, so
this is a hint: it says what the pattern matches, and leaves the question of
whether that was the intention to the reader.

## EO0055

**a pattern desugars to something that cannot be matched on**

A pattern is matched, not evaluated, so it may not hold a term the evaluator
would rewrite. The sugar is what usually puts one there: a `:list` parameter
anywhere but the tail of an n-ary application is folded in with
`eo::list_concat`, and an operator with a type-dependent nil inserts an
`eo::nil` where the pattern ends.

anoieu desugars the pattern and looks at the result, which is the same rule
ethos applies -- it answers `Cannot match on evaluatable subterm`, naming the
built term rather than the annotation that produced it. `anoieu desugar --term`
prints the same form.

## EO0056

**a parameter nothing uses**

*Off by default; run with `--pedantic` or `--only EO0056`.*

The parameter list of a rule or a program is a pool of names its patterns and
bodies draw on. One that no case mentions is dead, and is usually the trace of a
case that was edited away or a name that was misspelled where it was used.

## EO0057

**a program is declared and never defined**

`program` with no body is a forward declaration, to be defined later. One that
never is reaches the backends as a name with no meaning: under SMT-LIB a free
uninterpreted function the solver may read as it likes, under Lean a name that
was never written. Ethos itself simply never evaluates it.

## EO0060

**a program nothing reaches**

*Off by default; run with `--pedantic` or `--only EO0060`.*

A program no rule, program or definition names is dead: it is compiled, trimmed
and published for nothing, and if it was meant to be used, the rule that meant
to use it does not.

## EO0062

**a rule concludes a term that is not a Bool**

A proof step wraps what its rule proves in `(eo::pf F)`, which requires `F` to be
a `Bool`. Ethos never checks the conclusion when the rule is *declared*: the
program a rule desugars to is given return type `Bool` outright, and the
conclusion term is not compared with it. So

    (declare-rule bad ((x Int)) :args (x) :conclusion (+ x 1))

is accepted, and the first step that applies it fails with

    Expression of unexpected type: (_ (+ a) 1)  Type: Int  Expected: Bool

The rule can never be applied successfully, and nothing says so until someone
writes the proof that finds out.

## EO0063

**a rule takes a premise that is not a Bool**

A premise pattern is matched against what a premise proof proves, which is
always a `Bool`. A pattern of another type matches nothing, so the rule cannot
be applied.

## EO0064

**a program case returns a type the program does not declare**

"Terms in program bodies are not statically type checked" -- the user manual
says so, and `typeCheckProgramPair` checks only that the right-hand side binds
nothing new and that no pattern holds an evaluatable subterm. So a case that
returns the wrong type is accepted, and it fails only when a proof reaches that
case:

    (program $mk ((x Int) (F Bool)) :signature (Bool) Bool
      ( (($mk (not F)) F)
        (($mk F)       (+ 1 1)) ))    ; Int where Bool was declared

A proof that takes the first case checks `correct`. One that takes the second
fails, in a step that names neither the program nor the case.

Compared by type constructor, so a dependent return type -- `(BitVec n)` against
`(BitVec (eo::add n m))` -- agrees.

## EO0065

**a symbol is applied to more arguments than it takes**

An application of a symbol to more arguments than its type has is ill-typed, and
inside a program body or a rule nothing asks, so it sits there:

    (program $p ((F Bool)) :signature (Bool) Bool
      ( (($p F) (not F F)) ))          ; `not` is unary -- accepted, "correct"

Variadic symbols are exempt, since that is what their attribute is for, and a
symbol applied to *fewer* arguments than it takes is an ordinary partial
application.

## EO0066

**a program is applied to the wrong number of arguments**

A program declares its arity with `:signature`, and an application of another
arity never evaluates. Ethos notices at parse time and prints

    Wrong number of arguments when applying program $q, 3 arguments expected, got 2

without a file or a line, and the run still ends in `correct` with exit 0. This
says the same thing, where it happened.

## EO0067

**a requirement that can never hold**

`:requires ((a b))` is satisfied when the two sides evaluate to the same term.
Where both sides are values written out and they are different values, no
substitution can make them equal, so the rule can never be applied -- and
nothing says so until someone tries.

The same holds for an `eo::requires` written into a conclusion by hand, which
is what the attribute is sugar for.

## EO0069

**a premise list gathered by an operator that is not variadic**

`:premise-list F op` collects the formulas its premises prove and builds one
term from them with `op`, so `op` has to accept any number of arguments: the
manual asks for one marked `:right-assoc`, `:left-assoc`, a `-nil` variant, or
`:chainable`. With a binary operator, a rule applied to three premises builds an
application that does not type check, and one applied to none has nothing to
build.

## EO0070

**a program case that calls itself with the arguments it just matched**

A case whose whole right-hand side is the program applied to exactly what its
pattern matched does not compute anything: evaluating it evaluates it again,
with the same arguments, for as long as the checker is willing to keep going.
This is the shape a case takes when an argument was meant to shrink and does
not -- a tail that was written as the list, an index that was meant to be
decremented.

## EO0071

**a literal whose category the signature never gave a type**

`declare-consts` is what associates a syntactic category with a type: without
`(declare-consts <numeral> Int)` a numeral in a term has no type, and the term
holding it is ill-typed the moment anything asks. Signature files do no
normalisation, so a hexadecimal literal needs `<hexadecimal>` even where
`<binary>` is declared -- the normalisation of one into the other applies to
proof and reference files only.

`<boolean>` is exempt: `true` and `false` are builtin, and so is a literal that
stands only under a computational operator: ethos distinguishes a numeral value
independently of its type, so `(eo::add 1 1)` evaluates in a signature that
declares no numerals at all. What is reported is a literal standing where its
type is asked for.

## EO0072

**a builtin operator is applied to the wrong number of arguments**

Every `eo::` operator has the arity the user manual gives it, and an application
of another arity is a term that never evaluates -- ethos leaves it as it stands
rather than refusing it, so a rule written around one simply fails to fire, and
a program returns an application of itself.

The list operators are the easy ones to get wrong, because each takes the
operator it is about as its first argument: `eo::list_concat` takes three
arguments, not two, and `eo::nil` takes the operator and, where the nil depends
on it, a type.

## EO0073

**an evaluation the language says cannot happen**

The computational operators evaluate on values of one category -- "no mixed
arithmetic", as the manual puts it -- and on arguments in range. Where both
arguments are literals, whether the application evaluates is decided at the
point it is written:

    (eo::add 2 1/3)     stays as it is: a numeral and a rational
    (eo::zdiv 7 0)      stays as it is: division by zero
    (eo::pow 2 -1)      stays as it is: the exponent is negative

A term that does not evaluate is not an error to ethos; it is simply a term, and
the rule or program built around it does not do what it was written to do.

## EO0074

**a list operator applied to something that is not an n-ary operator**

Every list operator is *about* an operator, which it takes as its first
argument: `(eo::list_concat or x y)` concatenates two `or`-lists. The manual is
explicit that these evaluate only where that argument is an associative operator
with a nil terminator, so applying one to a symbol that was never marked
variadic gives a term that stays as it is -- and a program returning it looks,
to whatever called it, like a program that failed.

## EO0076

**a `:list` annotation that does nothing**

*Off by default; run with `--pedantic` or `--only EO0076`.*

`:list` says how a parameter behaves as a child of an n-ary application. A
parameter that never stands in one is annotated for nothing -- which is either a
leftover, or a misunderstanding of what the annotation does, and the second is
worth knowing about because the same misunderstanding is what leaves it *off*
where it was needed.
