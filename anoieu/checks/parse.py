"""Manual pages for what the front end reports as it reads.

The parser and the loader emit their findings while reading rather than as a
pass over the model, so their codes are registered here for `explain` and for
the catalogue, with no function of their own.
"""

from __future__ import annotations

from . import page

page(
    "EO0001",
    "a lexical error",
    """
An unterminated string or quoted symbol, or a character the language has no
token for. anoieu recovers and keeps reading, so one of these does not hide the
rest of the file.
""",
)

page(
    "EO0002",
    "a form that is never closed, or a `)` that closes nothing",
    """
Reported at the `(` that has no `)`, rather than at the end of the file, which
is where a parser that only counts brackets notices.
""",
)

page(
    "EO0003",
    "a token standing outside any command",
    """
Every top-level form of a signature is a command, i.e. a list. A bare token at
the top level is usually a stray fragment of an edit -- or a template marker,
if the file is one of the compiler's `$MARKER$` templates rather than a
signature.
""",
)

page(
    "EO0010",
    "an include that does not resolve",
    """
An include path is resolved against the directory of the file that includes it,
not against the working directory of the run.
""",
)

page(
    "EO0020",
    "an attribute that is not in the language",
    """
Ethos prints `Unsupported attribute :foo` and carries on. The declaration keeps
its meaning *minus the annotation*, so a misspelled `:right-assoc-nil` leaves
an operator that is not variadic, every application of it means something else,
and the run still ends in `correct`. That is why this is an error rather than a
warning: nothing downstream will mention it again.
""",
)

page(
    "EO0021",
    "a field of declare-rule written out of order",
    """
`declare-rule` reads its fields positionally, in the order `:assumption`,
`:premises` | `:premise-list`, `:args`, `:requires`, `:conclusion` |
`:conclusion-explicit`. A field out of order stops the parser where it expected
the conclusion, so ethos answers `Expected conclusion in declare-rule` at the
end of the command -- several lines after the field that caused it.
""",
)

page("EO0022", "a malformed typed parameter", "A typed parameter is `(<symbol> <type> <attr>*)`.")

page(
    "EO0023",
    "a rule with no conclusion",
    "Every rule ends with `:conclusion` or `:conclusion-explicit`.",
)

page("EO0024", "a malformed program case", "A case of a program is a pair `(<pattern> <term>)`.")

page(
    "EO0025",
    "a literal category the language does not have",
    """
The categories are `<boolean>`, `<numeral>`, `<decimal>`, `<rational>`,
`<binary>`, `<hexadecimal>` and `<string>`.
""",
)

page(
    "EO0026",
    "a command a signature file may not hold",
    """
Signature files and proof files are read as Eunoia; only a file named by
`reference` is read as SMT-LIB. So `declare-fun`, `assert` and `check-sat` in a
signature are an error -- ethos answers `Expected Eunoia command` -- and the same
commands in a referenced `.smt2` file are ordinary.
""",
)

page(
    "ANO0001",
    "a check reported more than a run will print",
    """
Not a finding about a signature: a finding about this tool. A check that reports
dozens of things has usually broken rather than found dozens of defects — it
happened here when a change to how a directory is read merged 191 unrelated test
signatures into one symbol table, and three checks produced 253 findings that
were all artefacts of the merge.

So a run holds a flooding check back, keeps three of its findings as evidence,
and says how many it did not print. Raise `limits.per_check` in `anoieu.json` if
the findings are real, or pass `--no-limits` to see them once.
""",
)

page(
    "ANO0002",
    "a run reported more than it will print",
    """
The same guard, for the total rather than for one check. A run loud enough to
hit it is a run nobody reads, and is more often this tool's fault than the
signature's. Nothing is dropped silently: the count is always reported.
""",
)
