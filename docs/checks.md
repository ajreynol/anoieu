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
| [EO0055](#eo0055) | a `:list` parameter stands where the pattern cannot match | on |
| [EO0056](#eo0056) | a parameter nothing uses | off |
| [EO0057](#eo0057) | a program is declared and never defined | on |
| [EO0060](#eo0060) | a program nothing reaches | off |

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
declarations of one name with the *same* type are therefore indistinguishable --
the earlier one can never be selected -- and ethos says nothing, by design, so
that a signature may order declarations by precedence.

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
stands in its place. So a case whose arguments are all distinct parameters
matches every application, and every case written after it is dead.

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

**a `:list` parameter stands where the pattern cannot match**

See EO0054. A `:list` parameter anywhere but the tail position of an n-ary
application desugars to `eo::list_concat`, and a pattern may not hold an
evaluatable subterm, so the case can never be read.

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
