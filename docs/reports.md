# The reports

Everything anoieu has to say about somebody else's code, in three registers:
what it is **asking** of each project, **how** each finding was confirmed, and
what **came back**. All three are written and argued by hand.

The machine-generated half is elsewhere and deliberately so:
[`open-findings.md`](open-findings.md) is every finding the checks currently
report, and [`corpus.md`](corpus.md) is what was measured to produce it.

## The register: what anoieu is asking, and of whom

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

**Two sources feed this, and the code says which.** `EO`, `DOC` and `TRI` are
what the checks read out of a signature. **`FUZ` is what the [anoieu
fuzzer](fuzzing.md) provoked out of a checker** — a crash, a diagnostic outside
its own convention, or two checkers answering one file differently. A fuzzer
finding is an (A) like any other and is held to the same standard, with one
difference in how it is evidenced: it is confirmed by running a binary against
a committed reproducer under `tests/fuzz/`, rather than by re-running a check.
The mechanical ledger in [`open-findings.md`](open-findings.md) carries both,
and files a disagreement against *both* checkers, because deciding which of the
two is wrong is exactly the judgement a row here has made and a row there has
not.

So this is the page to open when you want to know what anoieu is asking of
anyone. [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) says how each defect was confirmed;
[`reporting-policy.md`](reporting-policy.md#running-it-in-ci) says how the adoption works; [`reporting-policy.md`](reporting-policy.md#the-workflow)
suggests how to work one of these with an assistant, and what we do with the
reply. None of those asks anything; this does.

- ✅ **live** — written, tested, and run over the corpus
- ◐ **partial** — the useful half exists and the limit is stated
- ○ **sketched** — designed in [`notes.md`](notes.md#the-design), not written

#### If you own one of these tools

Read your section. It is short, it says what anoieu found in your files and what
it would like you to do, and every claim in it was reproduced against ethos
before it was written down.

| you own | your section | read first |
| --- | --- | --- |
| cvc5's CPC signature | [cvc5](#cvc5--the-calculus-everything-downstream-is-built-from) | the log first: one finding fixed, one declined, and one we recorded as fixed that never was ([`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back)) |
| ethos, the proof checker | [ethos](#ethos--the-proof-checker-and-its-own-signatures) | ethos-1: a test signature declares an operator that cannot fold |
| ethos-eoc, the compiler | [ethos-eoc](#ethos-eoc--the-eunoia-compiler) | eoc-3: the `is_list_nil` diff your own docs ask for |
| logos | [logos](#logos--the-lean-development) | logos-2: a semantics entry for an operator CPC does not declare |
| eudaimonia | [eudaimonia](#eudaimonia--the-template-for-other-calculi) | eud-1: preflight a calculus against the signature contract |
| Eunoia itself | [Eunoia](#eunoia-itself--the-language-and-its-manual) | eunoia-1: an identical re-declaration makes two symbols that print the same |

#### Two faces, two documents

| | where | what it holds |
| --- | --- | --- |
| **Open findings** | this page, below | what anoieu believes and nobody has ruled on: hypotheses, each reproduced, each still able to be wrong |
| **The log** | [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) | what was reported and what came back: accepted, declined, deferred — and what the analyzer changed when a finding was wrong |

One finding has landed in cvc5, one was declined because our analysis was
wrong, one was overstated, and one we recorded as fixed turned out never to have
been changed at all. The log is the more honest half of the pair, and the one to
read first if you are deciding how much weight to give the other.

#### How a row moves

The **state** column is the whole tracker; there is no second one elsewhere. A
row that gets a verdict leaves this table and is written up in the log.

| state | means |
| --- | --- |
| `open` | a defect, reproduced, not yet fixed |
| `proposed` | a change or an adoption we recommend and nobody has ruled on |
| `open question` | we do not think we know the right answer |
| `blocked on X` | waiting on another row |
| `needs M4` | waiting on a milestone here, not on you |
| `filed <link>` | raised upstream; the link is the issue or pull request |
| `fixed` / `adopted` / `declined` | ruled on: the row moves to [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) with the reasoning |

A row that is **declined** is a good outcome and stays visible: the check that
produced it then gets a suppression comment in your file or a `disable` in your
configuration, so the same argument is not had twice.

---

### Open findings

**Hypotheses, not verdicts.** Everything below is something anoieu believes and
nobody who owns the file has ruled on yet. Each was reproduced before it was
written down — see [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) — and each can still turn out to
be wrong, as `cvc5-4` did. A row leaves this table the moment it is ruled on, in
either direction, and lands in the log: **[`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back)**.

| # | tool | kind | what | state |
| --- | --- | --- | --- | --- |
| [cvc5-1](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | A | `programs/Strings.eo:42` and `:55` declare `Int` and return `Bool` | reopened — recorded as fixed, never changed |
| [cvc5-6](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | B | compare each rule against its `ProofRule` declaration, its children and arguments, and `eo_printer.cpp` reshaping | requested by cvc5; may belong to [dokimasia](https://github.com/ajreynol/dokimasia) instead, see [`notes.md`](notes.md#8-a-neighbouring-tool) |
| [cvc5-7](#cvc5--the-calculus-everything-downstream-is-built-from) | cvc5 | B | keep a reproducer with every claim about first use, and derive severity from whether a call can stay stuck | requested by cvc5 |
| [ethos-1](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | `tests/match-simple.eo:11` declares `<` `:right-assoc` with a `Bool` return | open |
| [ethos-2](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | an unknown attribute warns and is dropped, silently changing what a term means; make it an error, or at least carry the location | proposed |
| [ethos-3](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | a misordered `declare-rule` field reports as `Expected conclusion`, several lines from the cause | proposed |
| [ethos-4](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | a program applied to the wrong arity prints without a file or line, and the run still exits `correct` | proposed |
| [ethos-5](#ethos--the-proof-checker-and-its-own-signatures) | ethos | B | run over `tests/*.eo`, `DOC*` disabled | proposed |
| [ethos-8](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | **`FUZ0002`** — `(declare-const f (->))` aborts with an uncaught `std::length_error` | open |
| [ethos-9](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | **`FUZ0003`** — three error paths abort outside the `Error: <file>:<line>` convention, with no location | open |
| [ethos-6](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | two test signatures use literals whose category they never declare, so `+` gets an untyped nil | open |
| [ethos-7](#ethos--the-proof-checker-and-its-own-signatures) | ethos | A | `tests/naive-nary.eo:182` — a case of `isPermutation` that can never be reached | open |
| [eoc-1](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | preflight: have `driver.py` run anoieu over the triple before stage 1, so a missing semantics block is refused at launch rather than at stage 6 | proposed |
| [eoc-2](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | run over `semantics/*.eos` and the signatures the tests compile | proposed |
| [eoc-3](#ethos-eoc--the-eunoia-compiler) | ethos-eoc | B | lean on anoieu for its own direction #2 — the diff between the operators the desugar stage forward-declares and the `:is-list-nil` blocks a human wrote | proposed |
| [logos-1](#logos--the-lean-development) | logos | A | the flattened copies carry cvc5-1; regenerating picks it up once cvc5 fixes it | blocked on cvc5-1 |
| [logos-2](#logos--the-lean-development) | logos | A | `Cpc.eos:542` has an entry for `str.indexof_re_split`, which CPC does not declare | confirmed, fix not landed |
| [logos-3](#logos--the-lean-development) | logos | B | run the triple over `Cpc.eos` and the signature it is of | proposed |
| [logos-6](#logos--the-lean-development) | logos | A | `test/regress/sexp/test-indexed-op.cpc`, committed and unmutated, is accepted by logos and refused by ethos — and it is not the thing we filed | open question |
| [eud-1](#eudaimonia--the-template-for-other-calculi) | eudaimonia | B | answer the signature contract from the signature and semantics, before a checker is generated, rather than from the compiler's output afterwards | proposed |
| [eud-2](#eudaimonia--the-template-for-other-calculi) | eudaimonia | B | settle the calculus profile's two *declared* answers against the signature instead of recording them on trust | proposed |
| [eunoia-1](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | refuse a re-declaration whose type is identical to an earlier one | proposed |
| [eunoia-2](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | an unknown attribute should be an error, not a dropped annotation | proposed |
| [eunoia-3](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | enforce the attribute contracts the manual states as "must", at the declaration | proposed |
| [eunoia-4](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | decide what a well-formed signature is: type program bodies, or say that a program's return type is a claim nothing checks | open question |
| [eunoia-5](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | write down that matching does not check types, and what follows from it | proposed |
| [eunoia-6](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | settle `eo::define` in the grammar: several bindings, bound in parallel | proposed |
| [eunoia-7](#eunoia-itself--the-language-and-its-manual) | Eunoia | C | say what `eo::hash` guarantees, or mark it as the one thing a model cannot follow | open question |

**Settled, and not repeated here:** `cvc5-2` is fixed upstream, `cvc5-3` is
deferred, `cvc5-4` was declined because our analysis was wrong, and `cvc5-5`
waits on a pinned release. All four, with the reasoning and with what the
analyzer does differently as a result, are in
[`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back).
**`cvc5-1` is not settled and is back in the table above:** it was closed on a
triage that said both signatures now return `Bool`, and they never did.

### The claim

Ethos is a proof checker, and a good one *because* it is lazy: it computes a
type when something asks, checks the program case a proof reaches, and says
nothing about the rest. The consequence is that a *signature* — as opposed to a
proof — is nobody's job. A `define` body with no `:type` is never typed, a
program case is checked when a proof gets there, and a proof rule that can only
ever fail is a legal declaration until someone writes the step that finds out.

anoieu is the eager reader of the same files. It asks about every declaration,
with no proof in hand, no build, and no solver, in under a second. Of the 49
witness files in its suite — each holding one deliberate mistake — **ethos
accepts 43 and answers `correct`**. That number is the whole argument.

The second thing it is for is slower and possibly worth more: every check is a
statement about what Eunoia means, so the check catalogue, its witnesses, and
the differential harness against ethos amount to an executable account of a
language whose `.eos` half is specified today by one README and the compiler
that reads it. See [`notes.md`](notes.md#what-we-have-established-about-eo-and-eos).

### Status at a glance

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
| full type checking | which rules *may* conclude a non-`Bool` through a program's cases | ○ — [M3](notes.md#7-roadmap) |
| the triple | does the signature agree with its `.eos` semantics, and those with SMT-LIB | ○ — [M4](notes.md#7-roadmap) |
| solver-backed obligations | is this `:is-list-nil` predicate actually the operator's nil | ○ — [Tier 5](notes.md#46-tier-5--opt-in-deeper) |
| editor integration | the same findings while typing, with hover types and cross-triple jumps | ○ — [M5](notes.md#7-roadmap) |

---

### cvc5 — the calculus everything downstream is built from

**Today.** Three real defects, found on the first audit and confirmed against
ethos, plus documentation drift. Full write-up in [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed);
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

#### Actions

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

### ethos — the proof checker, and its own signatures

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

#### Actions

**ethos-1 (A)** — `tests/match-simple.eo:11`:
`(declare-const < (-> Int Int Bool) :right-assoc)`. A right-associative operator
folds its result back into its second argument, so its type must be
`(-> T1 T2 T2)`; every application of three or more arguments here is ill-typed.
Drop the attribute. Reported by `EO0040`.

*Answered: accepted, the attribute is removed on `anoieu-findings`@`292201c2`.
The finding is closed on that; whether it reaches `main` is a question for the
landing audit rather than for this one.*

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

*Answered, and reduced. The four `eo-definitions.eo` rows are declined and the
decline holds: that file is an include fragment whose includer declares
`<numeral>`, so the word "signature" in the message is ours to fix, not ethos's
— see the log. What remains asked is only the two `right-assoc-variants.eo`
rows, and the maintainer has deliberately left those undecided: what a
declaration-shape regression ought to declare is a question about that test.*

**ethos-7 (A)** — `tests/naive-nary.eo:182`. `isPermutation`'s first case
matches any pair of identical arguments, so its second case, which matches a
pair of identical `or`-terms, can never be reached. Reported by `EO0052`.

*Answered: accepted, the case is deleted on `anoieu-findings`@`292201c2`.
The finding is closed on that; whether it reaches `main` is a question for the
landing audit rather than for this one.*

**ethos-8 (A)** — `(declare-const f (->))` — a `->` type with no arguments —
aborts ethos with `terminate called after throwing an instance of
'std::length_error': cannot create std::vector larger than max_size()`. An
uncaught C++ exception rather than a diagnostic, so nothing downstream can tell
it from any other abnormal exit. Reproducer:
`tests/fuzz/crash-ethos-terminate-called-after-throwing-an-instance--fd1900/`.
Found by the fuzzer, `FUZ0002`.

*Answered: accepted. `(->)` is refused in the parser before a term is built, so
the message carries a position, on `anoieu-findings`@`292201c2` with a
regression. The finding is closed on that. ethos noted that `(_)` is
still a bare `Check failure` — not reported by any row, and not asked for.*

**ethos-9 (A)** — three error paths abort with a message that does not go
through the `Error: <file>:<line>.<col>:` convention the rest of ethos's
diagnostics use, so they carry no location and no `Error:` prefix:

- `(declare-consts <numeral> Int)` followed by `(declare-consts <numeral> Bool)`
  — "cannot set type rule for kind NUMERAL to Bool, since its type was already
  set to Int";
- `(assume-push p true)` at the top level of a `.eo`, which reports that
  "including" the file did not preserve assumption scope, of a file that was
  given on the command line rather than included;
- `(include "no-such-file.eo")` — "Couldn't open file:".

Each is a real refusal and should be one; the ask is that it say so in the
form everything else says it, because an editor, a CI annotation and this
repository's own oracle all read that output by its shape. Reproducers for the
first two are under `tests/fuzz/`. Found by the fuzzer, `FUZ0003`.

*Answered: accepted for the two that had reproducers, both routed through the
lexer's `parseError` on `anoieu-findings`@`292201c2` with regressions. The third,
`(include "no-such-file.eo")`, was not in the report and is not ruled on.
The findings are closed on that, and the landing is audited separately.*

**ethos-5 (B)** — run over the test signatures. `anoieu check tests` reads 202
files under 191 entry points and reports **seven errors, three warnings and
one hint** in total — ethos-1, ethos-6, ethos-7, the `symm` docstring drift,
and one pattern that matches exactly two elements. It was three hints until two
of them turned out to be ours: see the `Nary.eo` rows in the log. That is a job
that could be blocking on the day it is turned on. Its tests are not written to
the docstring convention, so:

```json
{ "entry_points": ["tests"], "disable": ["DOC0010", "DOC0011", "DOC0012"] }
```

A directory names every `.eo` under it, so `"entry_points": ["tests"]` is the
whole configuration.

### ethos-eoc — the Eunoia compiler

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

#### Actions

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

### logos — the Lean development

**Today.** Little that is specific, and less than there was. `install/defs/Cpc.cached.eo`
is a copy of cvc5's `Cpc.eo` rather than something logos wrote, and cvc5's
`Cpc.eo` is the ground truth — so auditing the copy files cvc5's findings under
logos's name, seventeen times as it turned out. It is no longer read at all
(`NOT_AUDITED` in `tools/gen_corpus_table.py`), and whether the copy has drifted
from the original is a sync check — planned, in cvc5's CI — rather than
anything a static analyzer should be reporting. What is left for logos is what
logos owns: `Cpc.eos`, the semantics, and what the fuzzer turned up about the
parser — of which one finding was confirmed and fixed, one was declined with a
reason that holds, and one we withdrew as our own error.

**What it gets next, and it is the largest single item on the roadmap.** logos
owns `Cpc.eos`, the official semantics of CPC, so the triple checks are what
anoieu can say here that nothing else does: which symbols have no semantics
block, which blocks name symbols nothing declares, whether the two type rules
agree at the sort level, which operators owe an `:is-list-nil`, and which
programs will need a hand-written `:lean` termination clause.

#### Actions

**logos-1 (A)** — `install/defs/Cpc.eo` and `Cpc.cached.eo` carry cvc5-1.
Nothing to change in logos itself: regenerating picks the fix up once there is
one. There is not one yet — we recorded cvc5-1 as fixed upstream and it never
was, which logos caught while answering the rows against the copy, so the next
signature bump will carry the same three cases across unchanged.

**logos-2 (A)** — `Cpc.eos:542` has `(define-symbol str.indexof_re_split (s r q))`
and CPC declares no such operator: it declares `str.indexof_re`. The name is real
on the *target* side, and another entry transforms into it at line 584, which is
legitimate; the input-side entry is what no compilation reaches. Found by the
first run over the whole triple, and cvc5's response notes correctly that it
belongs to whoever owns the semantics rather than to cvc5. Reported by `TRI0002`.

**Confirmed by logos, and the fix has not landed.** They deleted the entry and
established it was dead rather than merely unused —
`install/install-cpc.sh --cached --check` reports the generated Lean byte-identical
with the line gone. But the deletion is an uncommitted working-tree edit, and the
branch it was said to be on, `anoieu-findings`, is `main` (`d4a03a59`) with no
commits of its own; the row stays open until it is somewhere a second person can
read it.
**And it will come back.** `scripts/bump-eoc-version.py` copies this file wholesale
from ethos's `tools/eoc/semantics/development-cpc.eos`, which still carries the same
line at `:542` in the ethos we pin (`3cf1c03fdfd0`) — so the next internal bump
restores it unless the deletion lands there first. That makes the same finding an
ethos one, in a file `deps.json` already checks out and no corpus currently reads
as a triple.

**logos-4 and logos-5 are ruled on** and are in
[the log](reports.md#logos--the-parser-and-the-semantics): the `declare-fun` case
declined for a reason that holds, the `assume`-after-`step` case declined and
documented, and the indexed-operator case withdrawn as ours.

**logos-6 (A, open question)** — `test/regress/sexp/test-indexed-op.cpc`,
committed and unmutated, writes `((_ extract 1 0) a)`. logos says `correct`; the
ethos on this machine refuses it at that line — *"Incorrect arity for extract,
which expects 2 arguments but 1 were provided"*, reading `(_ extract 1 0)` as a
curried `((extract 1) 0)`. That is the same shape as the `declare-fun` row: a
committed regression test of one checker that the other will not take.
**It is an open question and not a finding**, for two reasons. It is unconfirmed
against the reference: `deps.json` checks out ethos's `tests`, `tools/eoc` and
`plugins` and no source, so the pinned ethos cannot be built here, and every `FUZ`
row already carries that caveat. And logos raised it themselves, saying it may be
an artefact of which ethos they have. It needs one run against whichever ethos we
call the reference; if it stands, it is promoted through `anoieu-fuzz promote`
like any other, by a person.
It matters more than its size because it is what the withdrawn row was standing
in front of — see the log.

**logos-3 (B)** — run the triple in CI. logos already vendors ethos and consumes
cvc5's signature, so it is the natural place for the job — see the open question
below.

### eudaimonia — the template for other calculi

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

#### Actions

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

### Eunoia itself — the language and its manual

Eunoia is defined by [`user_manual.md`](https://github.com/cvc5/ethos/blob/main/user_manual.md)
in the ethos tree, and by ethos, which is where the definition is settled when
the two differ. anoieu is an accidental second reading of both: writing a
checker for a language you did not design surfaces every place the definition
under-determines behaviour, because the checker has to pick, and every pick is a
question somebody has to answer. This section is those questions.

#### Where the manual says "must" and nothing checks

| the manual requires | ethos does | what we saw |
| --- | --- | --- |
| a `:right-assoc` operator has type `(-> T1 T2 T2)` | accepts any type | `<` in `tests/match-simple.eo`, ill-typed for every chain of three ([ethos-1](#ethos--the-proof-checker-and-its-own-signatures)) |
| a nil terminator has the operator's tail type | accepts any term | `:right-assoc-nil 0` on a `Bool` operator type checks until something asks for the type of a term built with it |
| a chainable operator's combiner is variadic | accepts a binary one | works at two and three arguments, fails at one and at four |
| opaque arguments come before ordinary ones, "otherwise all applications will be ill-typed" | accepts either order | every application of the symbol is ill-typed, reported at each use site |

A "must" that nothing enforces is a "should" in practice, and each of these is a
local property of one declaration — the check is a few lines wherever it goes.
That is [eunoia-3](#eunoia-itself--the-language-and-its-manual).

#### Where the definition is silent, and we had to find out

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

#### What we would argue for

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

#### What the tool would like from a future manual

Three things, all of which anoieu now has to carry instead: a normative
statement per attribute, saying which of its conditions are requirements; a
statement of *when* each requirement is checked, since the answer today ranges
from "at the declaration" to "when a proof reaches that case"; and the list of
what a pattern may not hold, which is currently discoverable only from an error
message. The check catalogue in [`checks.md`](checks.md) is close to being that
appendix, and it would be a better one if the manual and the checker agreed on
which of its entries are errors.

---

### How they fit together

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
in [`reporting-policy.md`](reporting-policy.md#running-it-in-ci).

### What this is not

- **Not soundness.** Whether a proof rule is *valid* is what the verification
  conditions `ethos-eoc` emits are for. anoieu's question is the one below that:
  whether a signature and its semantics say something coherent at all.
- **Not a second checker.** Where a judgement needs the type checker or the
  evaluator, ethos is the authority, and anoieu says nothing rather than
  guessing. Every check that fired falsely on CPC was narrowed until it stopped;
  that record is the reason to believe the ones that remain.
- **Not a style tool.** The checks that are matters of taste on a signature that
  is already written are off by default.
- **Not a clean bill of health.** We publish defects and never assurances. A
  check that reports nothing is recorded as *that check reported nothing*, never
  as a statement that a signature, a semantics or a triple is correct,
  consistent or complete. The checks are partial by construction and narrowed on
  purpose, so a quiet run is evidence about the checks and not about the
  artifact — and a false sense of security, once handed to another analysis
  effort, is far harder to withdraw than a wrong finding.

### Open questions we are tracking

| question | why it matters | state |
| --- | --- | --- |
| Where does the triple job run? CPC's signature is in cvc5, its semantics in logos, and the compiler that reads both is in ethos. | The most valuable check will run in a repository that is not where its findings get fixed. | open; shapes what the `.eos` loader takes as input |
| Does cvc5 want its docstring convention enforced? | 18 findings today, and a doc generator would make them matter. | open |
| Should ethos absorb the declaration-time checks? | They are twenty lines there and would need no external tool. | open, and a good outcome either way |
| Should `driver.py` call anoieu, or should CI? | A preflight helps the person; a CI job protects the branch. They are not exclusive. | open (eoc-1) |
| How stable are check numbers? | Baselines and per-repository policy refer to them by code. | codes are permanent once released; a narrowed check keeps its number |
| Generated signatures in a corpus. | `Cpc.cached.eo` repeats what CPC says, so checking both reports everything twice. | resolved by convention: check sources, not artifacts |
| Should a check enumerate the class the fuzzer sampled? | Both `FUZ0003` fixes were one shape — a user-reachable `EO_FATAL()` in a file with no lexer — which is greppable in the ethos sources without a fuzzer. | open; ethos's suggestion, and the strongest of the four |
| Should the generator apply every builtin head to zero arguments? | `(->)` was `FUZ0002` and `(_)` is behind it with a bare `Check failure`; one mutation would sweep the family instead of one bucket at a time. | open; ethos's suggestion |
| Should a nil terminator's type be checked against the operator's tail? | `EO0040` checks the *shape* of a `:right-assoc` type and nothing checks the terminator, whose type is asked for the moment the operator is applied. The computational-operator exemption is right for literals generally and wrong in terminator position. | open; ethos's suggestion, and it would have caught the `str.++` mismatch nobody reported |
| Should a docstring's *field names* be checked, not just its counts? | `DOC0011` and `DOC0012` both assume the fields are right and count what is under them; it took both firing at once to say that `tests/Uf-rules.eo` wrote `; args:` where `; premises:` belonged, and neither can see the reverse mistake. | open; ethos's suggestion |

### The documents

| file | what it is |
| --- | --- |
| [`usage.md`](usage.md) | the interface: inputs, commands, options, exit codes |
| [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) | what has been reported to another repository, and what happened to it |
| [`reporting-policy.md`](reporting-policy.md#running-it-in-ci) | running this in ethos, ethos-eoc, logos and cvc5 |
| [`checks.md`](checks.md) | every check and its manual page, generated from the registry |
| [`closed-findings.md`](closed-findings.md) | every finding ruled on, with its verdict; `tools/landing.py` audits the ones closed before their fix landed |
| [`corpus.md`](corpus.md) | what the checks report on every signature we can find, generated and checked in CI |
| [`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) | what the first runs found, and every false positive that had to be shed first |
| [`notes.md`](notes.md#what-ethos-misses-and-why) | why ethos does not report these itself, by mechanism |
| [`notes.md`](notes.md#what-we-have-established-about-eo-and-eos) | what we have established about `.eo` and `.eos`, and where they are unsettled |
| [`notes.md`](notes.md#the-design) | the roadmap, the check catalogue, the architecture |
| [`report/cpc-audit.html`](report/cpc-audit.html) | the CPC audit, written for a reader outside the project |


## The workings: how each finding was confirmed

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

### The corpus

| tree | files read | crashes | findings |
| --- | --- | --- | --- |
| CPC (`Cpc.eo` and its include graph) | 35 | 0 | 35 (3 errors, 18 warnings, 14 hints) |
| CPC expert (`expert/CpcExpert.eo`) | 21 | 0 | 6 warnings |
| `ethos/tests`, `logos/install/defs`, `eudaimonia/examples` | 193 | 0 | 42 |
| the whole of `logos` and `eudaimonia`, generated files and templates included | ~500 | 0 | — |

Reading the compiler's own `$MARKER$` templates reports what it should: a
template is not a signature until the markers are filled, and anoieu says so
rather than falling over.

### What ethos says about the same files

Every check owns a witness under `tests/witnesses`, and `tests/run.py --oracle`
runs ethos on each one:

**Of the 49 witnesses that hold the mistake, ethos accepts 43 and answers
`correct`.** It refuses six: a `declare-rule` field out of order, an opaque
argument after an ordinary one, a program case of the wrong arity, a pattern
with two `:list` parameters, and a builtin applied to the wrong number of
arguments. For those five anoieu's contribution is the message and the location
rather than the detection -- ethos reports the pattern one, for instance, as
`Cannot match on evaluatable subterm`, which names neither the annotation nor
the parameter.

The forty-three are the case for the tool.
[`notes.md`](notes.md#what-ethos-misses-and-why) says why each of them gets past
ethos.

### Real bugs in CPC

Three, so far. Each was confirmed by constructing the smallest signature that
reproduces it and running ethos on it.

#### `$is_seq_const` and `$is_seq_const_rec` declare the wrong return type

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

**Corrected, after cvc5 assessed it.** The finding was right -- and it is still
there. We recorded it as fixed, "both signatures now return `Bool`", and both
still declare `Int`: at `622a50a3`, the commit it was reported against, and at
`aee874240419`, the commit this report is measured against. See
[`reports.md`](reports.md#cvc5-1-what-we-recorded-as-fixed).
What *was* wrong was our claim about when it bites, and that correction is worth
more than the finding.

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

#### Four skolem declarations are duplicated verbatim in the expert signature

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

#### `<` is declared `:right-assoc` with a `Bool` return -- `ethos/tests/match-simple.eo:11`

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

#### Three more, in ethos's own test signatures

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

#### The first run over a whole triple

cvc5's `Cpc.eo`, logos's `Cpc.eos`, ethos's `smt.eos` and the embedding they are
written against, checked together:

```bash
python3 -m anoieu check <cvc5>/proofs/eo/cpc/Cpc.eo \
  --semantics <logos>/install/defs/Cpc.eos \
  --smt-semantics <ethos>/tools/eoc/semantics/smt.eos \
  --embedding <ethos>/plugins/model_smt/model_smt.eo
```

One finding: `Cpc.eos:542` has `(define-symbol str.indexof_re_split (s r q))`,
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

#### Two rules that match the same applications

`rules/Rewrites.eo:90` and `:94`:

```lisp
(declare-rule arith-eq-elim-real ((t1 Real) (s1 Real))
  :args (t1 s1) :conclusion (= (= t1 s1) (and (>= t1 s1) (<= t1 s1))))
(declare-rule arith-eq-elim-int ((t1 Int) (s1 Int))
  :args (t1 s1) :conclusion (= (= t1 s1) (and (>= t1 s1) (<= t1 s1))))
```

Identical premises, arguments, requirements and conclusion; the parameters are
declared at different types. That distinction has no effect on which
applications match, because matching does not check a parameter's type -- so the
two rules accept exactly the same steps, are both compiled, both get a
verification condition and a Lean lemma, and a proof may cite either for either
sort. Reported by `EO0083`.

Whether that is a defect is for whoever maintains the generated rewrite rules;
what is certain is that the type annotation is not doing the work it looks like
it is doing, which is [eunoia-5](reports.md#eunoia-itself--the-language-and-its-manual)
again.

#### An inventory, not a defect: the rules a calculus admits

`EO0077` reports every rule marked `:sorry`. Both hits in the corpus are
intentional — CPC's `trust` rule, which carries every inference cvc5 has not
formalised and says so in its own docstring, and `ethos/tests/sorry.eo`, which
tests the feature. The check stays as a hint: it answers "which rules is this
proof's verdict resting on" without grep, and a calculus where the answer grows
is a calculus worth asking about.

#### One that is only a bug from the wrong entry point

`$evaluate_list` is forward-declared in `programs/Utils.eo:70` and defined in
`Cpc.eo:347`, so a run whose entry point is `expert/CpcExpert.eo` alone has it
declared and never defined. In practice cvc5's regression runner writes
`(include ".../Cpc.eo")` before `(include ".../expert/CpcExpert.eo")`
(`test/regress/cli/run_regression.py:372`), so the pair is always loaded
together and the gap never opens. Reported by **EO0057**, which now says "under
this entry point" for exactly this reason.

### Findings worth reading

#### `<` declared `:right-assoc` with a `Bool` return — `ethos/tests/match-simple.eo:11`

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

#### Documentation that no longer describes its rule — CPC, 18 findings

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

#### A program nothing reaches — CPC

`$is_app` (`programs/Utils.eo:123`) is declared, documented and never named by a
rule, a program, a definition or a declaration. Reported as a hint under
`--pedantic`.

#### Patterns that match exactly two elements — 14 in CPC, 31 across the corpus

Reported as hints, because a pattern that means "exactly two" is legal and
common. The interesting ones are where a single program does both:
`$str_arith_entail_is_approx` (`programs/Strings.eo:1745`) matches `(+ n1 n2)`
with the tail marked `:list` and `(* n1 n3)` with it unmarked, in adjacent
cases, so the same program walks a sum of any length and a product of exactly
two factors.

### What the corpus taught the checks

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
| two rules with the same premises and conclusion are the same rule | nineteen CPC rules share that shape and differ only in what they *require* of it | the identity of a rule includes its requirements, its assumption, its premise-list operator and whether its conclusion is explicit |
| a parameter shadowing a declared symbol is a hazard | it is idiomatic: a program parameterised by an operator names its parameter `cons`, `nil` or `f`, and ethos's own tests do it 150 times | the check was written, measured, and deleted |
| a name in the `$eo_` namespace collides with the compiler | `ethos/tests/eo-definitions.eo` defines the whole of `eo::` that way, deliberately | `$eo_` is reported only under `--pedantic`; the generated prefixes always |
| `declare-fun` is not a Eunoia command | true of a signature, false of a file named by `reference` | the loader tracks the role a file was read under |

That table is the M1 half of the specification work: each row is a question
about what a Eunoia signature means, which had to be answered before the check
could be written.


## The log: what was reported, and what came back

Every anoieu finding that has reached another repository and been ruled on.
[`open-findings.md`](open-findings.md) holds the other half — the findings that are
hypotheses nobody has judged yet. A row moves from there to here the moment it
gets a verdict, in either direction.

A finding that turns out to be wrong is the most useful thing on this page, so
those are written up at length: what we claimed, why it was wrong, and what the
analyzer does differently now.

### Where it stands

| verdict | count | which |
| --- | --- | --- |
| **fixed upstream** | 1 | `cvc5-2` |
| **declined — our error** | 1 | `cvc5-4` |
| **overstated — claim corrected** | 1 | `cvc5-1`'s impact |
| **recorded as fixed, and never was** | 1 | `cvc5-1`, reopened |
| **deferred** | 1 | `cvc5-3`, pending a documented convention |
| **not yet** | 1 | `cvc5-5`, pending a pinned release |
| **not audited** | 17 | every row against `logos/install/defs/Cpc.cached.eo` |
| **declined, and the reason holds** | 2 | `logos-4`'s `declare-fun` case, `logos-5` |
| **withdrawn — our error** | 1 | `logos-4`'s indexed-operator case |
| **accepted, closed, awaiting landing** | 7 | ethos-1, ethos-7, ethos-8, ethos-9 and the `symm` docstring — seven rows on `anoieu-findings`@`292201c2`, tracked by `tools/landing.py` |
| **accepted, and nothing committed** | 1 | `logos-2`, still open — the one case the new closing rule does *not* cover |
| **declined, not yet confirmed** | 8 | the three ethos `EO0084` rows, `conclusion-spec.eo`, the four `eo-definitions.eo` rows |
| **our error, not yet withdrawn** | 2 | the two ethos `Nary.eo` rows |
| **undecided by the maintainer** | 2 | ethos-6's two `right-assoc-variants.eo` rows |

Changes the analyzer made as a result:

- **ordered profiles**, so reachability is asked in a world someone runs
  (`cvc5-4`);
- **profile-scoped findings**, so a local answer is never a repository-wide
  claim (`cvc5-4`);
- **three levels of impact kept apart** for a declaration that disagrees with
  its cases (`cvc5-1`);
- a regression case in `tests/cli_cases.py` for the arrangement that produced
  the wrong finding;
- **the fuzzer's shrinker no longer edits a seed run as it stands**, after a
  promoted reproducer turned out to differ from the committed file it came from
  by a cut the reference had never looked at (`logos-4`);
- **files a project did not author are not audited** (`NOT_AUDITED` in
  `tools/gen_corpus_table.py`), after seventeen rows were filed against logos
  for a copy of somebody else's signature;
- **a pattern's head is read in the scope that binds it** (`EO0054`), after two
  rows against ethos resolved a program's own parameter against a
  `:right-assoc-nil` declaration made by the file that includes it (`ethos`, the
  `Nary.eo` rows);
- **a merge is no longer what closes a row** — a maintainer's acceptance and a
  commit on a named branch are, with the landing tracked separately by
  [`tools/landing.py`](../tools/landing.py) so that the shortcut is booked rather
  than forgotten (`ethos`, seven rows).

---

### cvc5 — the CPC signature

Reported against cvc5 commit `622a50a3`, assessed by the cvc5 maintainers, whose
response is reproduced in that repository as `anoieu-response.md`.

| item | what we said | decision |
| --- | --- | --- |
| **cvc5-1** | `$is_seq_const_rec` and `$is_seq_const` declare `Int` and return `Bool` | **accepted** — and *not* fixed. We recorded "both signatures now return `Bool`"; they did not then and do not now. Reopened, see below |
| **cvc5-2** | four arithmetic skolem declarations duplicated in `expert/theories/ArithExt.eo` | **accepted, fixed** — the second block removed |
| **cvc5-3** | 18 documentation arity and field findings | **deferred** — documentation rather than calculus, and the convention for documenting a program's pattern variables has to be decided first |
| **cvc5-4** | `$is_app` is reached by nothing | **declined — our analysis was wrong.** See below |
| **cvc5-5** | run anoieu in CI, report-only then blocking | **not yet** — reasonable once the entry-point handling is fixed and a released version can be pinned |

Both accepted changes were verified on a temporary copy *before* landing:
ethos accepted the base and the base-plus-expert signature, and the `EO0031` and
`EO0064` diagnostics went away. **That is a check on the change we proposed, not
on the tree afterwards, and neither was ever re-checked against cvc5.** For
`cvc5-1` that is how it came to be recorded as fixed when nothing had changed.
`cvc5-2` has not been re-checked here either, and the four `EO0031` rows it is
about are still open in [`open-findings.md`](open-findings.md) — nobody has
ruled on what that means, and this entry is not the place to decide it.

#### cvc5-4: what we got wrong

`$is_app` is used by the expert signature's `lambda-elim` rule:

```lisp
:requires ((($get_arg_list t) x) (($is_app f t) true))
```

We reported it as dead because we analysed `Cpc.eo` and `expert/CpcExpert.eo` as
two independent worlds. That is not a configuration anyone runs: cvc5 checks an
expert proof by including `Cpc.eo` and *then* `expert/CpcExpert.eo`, in that
order, into one symbol table — `test/regress/cli/run_regression.py`. In that
world the rule and the program are in the same signature and the finding does
not exist.

**What changed.** An analysis target is now an ordered **profile** rather than a
set of entry points:

```json
{
  "profiles": [
    {"name": "safe",   "includes": ["cpc/Cpc.eo"]},
    {"name": "expert", "includes": ["cpc/Cpc.eo", "cpc/expert/CpcExpert.eo"]}
  ]
}
```

Files named in a profile are read in order into one signature, the way the
consumer reads them. Several files given on the command line are one ordered
profile rather than several separate ones. Reachability findings carry the
profile they were found in, and a finding is only reported where it holds in
**every profile that read the file the subject stands in** — so a program used
only by the expert signature is no longer dead, and a program unreached in a
profile that does not exist is no longer a claim.

Run over cvc5's two real profiles, the dead-code check now reports `$is_app`
nowhere. `tests/cli_cases.py` carries the arrangement as a regression: a base
file, a second file whose rule uses its helper without including it, and the
three answers — dead alone, alive as a profile, and dropped when two profiles
disagree.

#### cvc5-1: what we overstated

The finding was right, but our *impact* claim did not reproduce. We wrote that a
use of `$is_seq_const` where a `Bool` is expected is a type error; cvc5 found that a direct typed use checks as `correct`, because
both programs are total over their argument and ethos evaluates the application
before consulting the declared return type. The declared `Int` surfaces only
when an application stays stuck.

Our reproduction used a program whose application could not evaluate, and we
generalised from it. The distinction we now owe every report of this shape, in
cvc5's words:

- a declaration that disagrees with its cases;
- an application that may remain stuck and expose the declared return type;
- a concrete proof or term that current ethos rejects.

`EO0064`'s manual page says which of the three it is, and
[`reports.md`](reports.md#the-workings-how-each-finding-was-confirmed) is corrected.

#### cvc5-1: what we recorded as fixed

**The three rows are reopened.** We closed them with the verdict *fixed
upstream — both signatures now return Bool*. They do not. `$is_seq_const_rec`
and `$is_seq_const` declare `:signature ((Seq T)) Int` at `622a50a3`, the commit
the finding was reported against, and at `aee874240419`, the commit
[`corpus.md`](corpus.md) records this report as measured against — and over the
last three hundred commits of cvc5 `main` neither program has ever declared
anything else. They entered `programs/Strings.eo` in `6441210` already declaring
`Int`. The checks report all three cases today; the only reason they were not in
the open table is that a closed id is one the generator skips.

**Nobody upstream told us it was fixed and nothing here checked.** The verdict
was written from an assessment of the change we proposed, and the entry above
records that both accepted changes were verified *on a temporary copy before
landing*. That is a check that the fix would work, not that it happened, and the
gap between the two is where this sat.

**It was caught by a third party reading our own ledger.** logos, answering the
rows we filed against its flattened copy of the same signature, went to cvc5
`main` to check whether the copy would pick up a fix at the next bump, found the
line unchanged, and told us the closed verdicts were wrong — three times, once per
row, each naming the id. That is the whole argument for publishing the ledger
with the ids in it.

What follows for the tool, rather than for this row:

- **`--pinned` never re-derived these.** It re-runs every check over the
  recorded commits and reports what they say, and all three are still reported;
  what it cannot do is notice that a *closed* id is still being reported,
  because closing is defined as removing the finding from the generator's
  consideration. A closed row and a live finding can therefore coexist
  indefinitely with nothing red. Worth a check on the report itself: an id in
  `closed-findings.md` that the checks still report at the pinned commits is either
  a wrong verdict or a verdict that has expired, and both want a person.
- **A verdict of *fixed upstream* is a claim about somebody else's tree**, and it
  is the one kind of verdict this repository can settle by itself, from `deps/`.
  It should not have been recorded without that.

---

### What cvc5 asked for next

Recorded here because it is the clearest statement anyone has given us of what
would make the analyzer worth running. Tracked as items in
[`reports.md`](reports.md#the-register-what-anoieu-is-asking-and-of-whom).

| request | state |
| --- | --- |
| ordered analysis profiles, and profile-scoped findings | **done** — above |
| reproducers that exercise the claimed failure, kept with the diagnostic | open |
| impact-aware severity: exhaustive cases, stuck applications, a reproduced rejection | open |
| reachability roots, traces (`lambda-elim -> $is_app`), and a way to mark public helpers | open |
| a check comparing each rule against cvc5's `ProofRule` declaration, its children and arguments, and `eo_printer.cpp` | open — would catch interface drift that makes an emitted proof uncheckable |
| documentation checks that compare names and roles, not counts, and distinguish call arguments from pattern variables | open — and it is why cvc5-3 is deferred |
| diagnostics naming the repository that owns the file | open |
| versioned releases, stable diagnostic meanings, path-independent baselines, a policy for narrowing a check without invalidating suppressions | **less than we claimed.** A baseline entry's id moves with the path root, so changing an entry point invalidates every entry while the findings are identical — which is what happened to `tests/corpus/cpc-baseline.json` when CPC's entry point moved. Tracked as C6 in [`notes.md`](notes.md#7a-maintenance-coherence--todo); releases and the narrowing policy are still not written down |

---

### ethos — the checker and its test signatures

Nineteen rows were put to ethos and answered one at a time, on branch
`anoieu-findings`; the reply is reproduced in that repository as
`anoieu-response.md`, and every block carries both a `TRIAGE:` and a
`HUMAN RESPONSE:`. Seven were accepted and fixed, ten were declined as
deliberate, and two the maintainer left undecided.

| item | what we said | decision |
| --- | --- | --- |
| **ethos-1** | `<` is `:right-assoc` with a `Bool` return in `tests/match-simple.eo:11` | **accepted, fixed** — attribute removed. **Closed**, awaiting landing |
| **ethos-7** | `isPermutation`'s case at `naive-nary.eo:182` is shadowed by the one above it | **accepted, fixed** — line deleted. **Closed**, awaiting landing |
| the `symm` docstring | `tests/Uf-rules.eo:25` heads a premise `; args:` | **accepted, fixed** — one line, `; args:` to `; premises:`, settling both rows. **Closed**, awaiting landing |
| **ethos-8** | `(declare-const f (->))` aborts with an uncaught `std::length_error` | **accepted, fixed** — refused in the parser, with a position. **Closed**, awaiting landing |
| **ethos-9** | two error paths abort outside the `Error: <file>:<line>.<col>:` convention | **accepted, fixed** — both routed through the lexer's `parseError`. **Closed**, awaiting landing |
| the three `EO0084` rows | `identity` and `id` conclude one of their own premises | **declined** — deliberate no-op rules. Open; see below |
| `conclusion-spec.eo:8` | the pattern matches an `or` of exactly two elements | **declined** — a split clause has exactly two disjuncts. Open; see below |
| the two `Nary.eo` rows | the pattern matches a `cons` of exactly two elements | **our error.** The head is a program parameter. Check narrowed; open pending confirmation |
| the four `eo-definitions.eo` rows | literals whose category the signature never declares | **declined** — the file is an include fragment, and the word *signature* is what is wrong. Open; see below |
| **ethos-6**, `right-assoc-variants.eo` | `+`'s nil terminator `0`, and `""`, have no declared category | **undecided** — the trial edit was made and reverted. Open |

**Seven rows closed and twelve did not**, for reasons that are worth keeping
apart.

**The seven accepted fixes are real, and we checked them rather than took
them.** They are one commit, `292201c2`, cut from `main`@`8709609e`. For the
four signature rows we ran the checks over the fixed files and over the
originals: each fix clears its row, and each original still reports it. For the
three `FUZ` rows `anoieu_fuzz verify` moves every reproducer from `abnormal` to
`reject`, and the `Error: <file>:<line>.<col>:` text each now prints is
introduced by that commit and absent from `main` — so each stopped reproducing
*for the reason on its row*, which is the distinction the follow-up is supposed
to make and the one a bare "no longer reproduces" would have missed.

They were left open for a day, on the rule that a branch had to be merged before
a row could close. **That rule is gone**, and these seven are the first rows
closed under what replaced it: a maintainer's acceptance plus a commit on a named
branch, with the merge treated as a separate question. Holding a finding open
until somebody else's pull request is approved measures their review queue, not
the finding, and while the checks are still moving that is a bad trade. What the
change costs is stated where it is taken on, in
[what closes a row](reporting-policy.md#what-closes-a-row-and-what-does-not):
each of the seven verdicts ends with `awaiting landing: ethos anoieu-findings
292201c2`, and `python3 tools/landing.py --check` is the pass that asks whether
that commit has reached `main` yet. Today it answers *not yet* for all seven,
which is the correct answer and a recorded one rather than an assumed one.

Worth recording because it cuts the other way from the last round: the reply's
own header states that *nothing is committed* and that the changes sit unstaged
in the working tree. They do not — the branch carries `292201c2` and the tree is
clean. The reply was written while that was true and was overtaken by the
correction it describes. It cost nothing here because we read the branch instead
of the sentence, which is exactly why the follow-up is told to.

**The ten declines are open because of a change to how we work**, not because of
anything ethos said. The maintainer's decisions are recorded and none of them is
in doubt; what is in doubt is the process that produced them. Asked afterwards,
he said he had not pushed back on the *won't fix* answers — an agent proposes
"not a defect", the human does not object, and silence becomes a verdict. So no
declined row is closed on this round's evidence, and the rule the reply is being
read against has changed underneath it: see the postmortem, and the proposal to
make prompt one ask for an explicit confirmation before it records a decline.

#### The two `Nary.eo` rows: our error, and a worse one than it looked

Both rows say `(cons x nil)` matches a `cons` of exactly two elements.
`tests/Nary.eo:88` and `:154` declare `cons` and `nil` as *parameters* of the
enclosing program — `(cons (-> L L L)) (nil L)` — so no n-ary sugar applies to
the pattern at all, and read as a list `(cons x nil)` is the one-element list
the case exists to match. ethos said so, and it is right.

The interesting part is where the check got its `:right-assoc-nil` from, because
it is not in `Nary.eo`. Checking `Nary.eo` on its own reports neither row. The
rows come from `tests/examples-nary.eo`, which is `(include "Nary.eo")` on line
1 and `(declare-const cons (-> S S S) :right-assoc-nil nil)` on line 7 — so the
check reached into a program in an included file and resolved its parameter
against a global declared in the *including* file, **after the include**, that
the parameter shadows and that did not exist when the program was parsed.

The wrong assumption is that a name means one thing per signature.
`resolve_decl` reads `Signature.by_name`, one flat table with no notion of a
local scope, and `_walk_pattern` had the enclosing parameter list in hand the
whole time and never consulted it — the desugarer beside it does, but only to
ask whether a parameter is `:list`. `EO0054` now returns as soon as the head of
a pattern is a name the parameter list binds, with
`tests/witnesses/EO0054-shadowed-good.eo` as the witness. `ethos test
signatures` drops from three `EO0054` to one; the survivor is
`conclusion-spec.eo:8`, where `or` really is declared `:right-assoc-nil` and is
nobody's parameter, and no other project's count moves.

Two things this does not fix, both recorded rather than done. The narrowing is
per-check, and any other check that resolves a head through the flat table has
the same hole. And a symbol declared after the `include` that reaches it is
visible to us at a point ethos would not have it — a scoping question the loader
answers by flattening, which is fine for most checks and wrong for this class.

#### The four `eo-definitions.eo` rows: the finding is true and the sentence is not

`EO0071` says "`0` is a `<numeral>` literal, and **this signature** has no
`declare-consts <numeral>`". Both halves of that are true of
`tests/eo-definitions.eo` read on its own, and the file is never read on its
own: it declares no sorts, includes nothing, and uses `$eo_nil`, which the
manual says cannot be given a static definition. ethos refuses it standalone at
line 148, long before any numeral. Its includer,
`tests/eo-definitions-test.eo`, declares `<numeral>` on line 3 and checks
`correct`.

We check it standalone because a corpus directory is *one profile per file* —
every `.eo` under `tests/` is an entry point, whether or not it is one. So the
check is not wrong about the file; the report is wrong about what the file is,
and it says so in the one word a maintainer reads first. The check's own
judgement was good throughout: its computational-operator exemption behaved
exactly as its page describes on all seven `EO0071` rows, reporting only the
four places a type is actually asked for.

Not fixed here, because the honest fix is not a narrowing. Suppressing or
rewording these needs to know that *something else in the corpus includes this
file*, and that is a reverse edge no check can see: `ctx.include_edges` runs
forward from the entry point, and profiles are independent by construction.
Building a corpus-level include index is a change to the report generator and to
what a profile means, and it is not one to make while writing up the rows it
would have suppressed. The id survives a reword — a fingerprint is the code, the
path and the text of the line, never the message — so nothing is lost by
deciding this separately.

#### `right-assoc-variants.eo`: undecided, and correctly so

The two rows there are the only ones the maintainer declined to rule on, and the
reasoning is worth keeping. The finding is true and has a demonstrable
consequence — adding `(declare-consts <numeral> Int)` is the single difference
between `(eo::typeof (+ x y))` answering "Parsed type has an unevalated term"
and answering `Int` — but the consequence is only reachable from a file that
does not exist. Nothing includes `right-assoc-variants.eo`, it applies no
operator, and it checks `correct` either way; it exists to exercise the shapes
of `:right-assoc-nil` declarations, and a terminator whose category has no type
may be one of the shapes it is for. The trial edit was made and reverted, and is
not on `292201c2`.

That is the right answer to a row we could not have decided from here, and it is
the one case where *cannot tell* survived contact with somebody who knows the
file. ethos also noticed, and did not act on, that `str.++`'s nil terminator in
that file would not carry the tail type if the operator could be applied — which
the missing declaration currently hides, so adding it would expose a mismatch
rather than fix one. Recorded, not filed: no row reports it.

### logos — the parser and the semantics

Nineteen rows were put to logos and answered one at a time, on branch
`anoieu-findings`; the reply is reproduced in that repository as
`anoieu-response.md`. Sixteen of them were rows we had already closed as *not
audited*, and the answer to each is the one that closure had assumed —
`install/defs/Cpc.cached.eo` is generated, byte-exact against the cvc5 signature
the Lean packages were compiled from, and a correction there would falsify the
pin rather than fix anything. Nothing moved for those sixteen. Three rows were
substantive.

| item | what we said | decision |
| --- | --- | --- |
| **logos-2** | `Cpc.eos:542` declares a semantics entry for `str.indexof_re_split`, which CPC does not declare | **accepted** — entry deleted, generated Lean byte-identical without it. **Left open**: the change has not landed |
| **logos-4**, `declare-fun` | `test/regress/sexp/test-define.cpc`, committed and unmutated, is accepted by logos and refused by ethos | **declined**, and the reason holds. Closed |
| **logos-4**, `(( extract 1 0) a)` | logos reads the indexed operator without its `_` and accepts a proof ethos refuses | **withdrawn — our error.** The reproducer was an artefact of our shrinker. Closed |
| **logos-5** | an `assume` after the first `step`: ethos accepts, logos refuses | **declined and documented** — a deliberate restriction of logos's input format, now stated in `docs/parser.md`. Closed |

#### logos-2: accepted, and the row stays open

The entry was a symbol of the *target* vocabulary — declared in ethos's
`smt.eos`, and legitimately written by the transform a few lines below it — that
had been given an input-side entry it had no business having, so it contributed a
transform case nothing could reach. logos deleted it and established that it was
dead rather than merely unused: `install/install-cpc.sh --cached --check` reports
the generated Lean byte-identical with the line gone.

**The row is still open, and the reason is the branch.** `anoieu-findings` is
`main`, `d4a03a59`, with no commits of its own; the deletion, and the parser work
below, are uncommitted edits in one working tree. Our own report is measured
against `updateCompiler` at `47f29bfa`, a different branch, where the line stands
and `TRI0002` still reports it. A reply is a triage and the branch is the
authority, and here the branch is empty — so the row keeps its finding and gains
a note saying where the work is.

logos also told us the finding will return: `scripts/bump-eoc-version.py` copies
`Cpc.eos` wholesale from ethos's `tools/eoc/semantics/development-cpc.eos`, which
carries the same line at `:542` in the ethos we pin. That is checked out here
already and no corpus reads it as a triple.

#### logos-4, `declare-fun`: declined, and the reason holds

`declare-fun` in a proof file is deliberate and documented. logos ignores
`include` and `reference` — it has the signature built in and never reads the
input problem — so a proof has to carry its own declarations, where ethos puts
the command behind its reference-file table because that is where it expects them
to come from. The symbol gets exactly the type SMT-LIB gives it, which is the
type ethos would give it from a reference file, so nothing is misread. And the
divergence cannot arise on real cvc5 output: the `eo` variant of cvc5's printer
emits `(declare-const f (-> U U U))`, never `declare-fun`. The reproducer still
reproduces, by design, and the row is closed as declined rather than as fixed.

logos observed that the severity reads high for what it is — the reproducer is
one of their own regression tests, unmutated, and the finding is that their input
format is a documented superset in one command. The severity is not a claim about
fault: `FUZ0001` is the direction, not the attribution, and
[`reporting-policy.md`](reporting-policy.md#a-finding-from-the-fuzzer) says so.
What the observation is really about is that a `FUZ` row carries no field for
"whose fault", which is the same ownership gap cvc5 asked for.

#### logos-4, the indexed operator: what we got wrong

**The reproducer was an artefact of our own shrinker, and the note on it named a
cause that had nothing to do with why ethos refused the file.**

The case was `test/regress/sexp/test-indexed-op.cpc`, taken from logos's own
regression suite and run *as it stands* — which is a thing this fuzzer does
first, deliberately, and which is where its best finding so far came from. It
disagreed: logos said `correct`, ethos refused. So far so good.

Then the shrinker ran. `shrink` keeps an edit when the finding is still the same
finding, and "the same" is the bucket — the two checkers' coarse verdicts and a
normalisation of the refusing one's message. The bucket says nothing about
*where* the refusal happened. Ethos was refusing at **line 3**, on the file's own
unmutated `((_ extract 1 0) a)`. So the shrinker was free to cut anything on line
4, and it cut the `_` out of `(((_ extract 1 0) a))`, leaving `((( extract 1 0)
a))`, and the bucket held — not because the cut mattered but because nothing on
line 4 had ever been reached.

That reduction is exactly reproducible from the committed code:

```python
>>> from anoieu_fuzz.triage import _spans, _cut
>>> cmd = "(step @p1 :rule refl :args (((_ extract 1 0) a)))"
>>> _cut(cmd, *next(s for s in _spans(cmd)[1] if cmd[slice(*s)] == "_"))
'(step @p1 :rule refl :args ((( extract 1 0) a)))'
```

What was then promoted was a file nobody had written, under a note — *"( extract
1 0) without the `_`: logos reads it as the indexed operator, ethos does not"* —
that described the cut rather than the refusal. Every later reader inherited it,
including this repository's own register and `fuzzing.md`, and including logos,
who fixed their parser against it.

**What is true underneath.** Three separate things, and the row conflated them:

1. The parser *was* more permissive than the grammar: a parenthesised head that
   is not marked `_` was read as a curried application. Reduced on its own,
   `(( extract 1 0) a)` gets a **parse** error from ethos — *"Expected qualified
   identifier or indexed symbol as head of apply"* — not the type error the row
   recorded. logos narrowed `parseTermCore`, added guards in `test/Parser.lean`
   and `test/CpcParser.lean`, and against a build carrying that change the
   reproducer no longer reproduces: `anoieu_fuzz verify` reports it as `was
   accept, is reject`. That fix is real and stands on its own, whatever happens
   to this row.
2. **The disagreement ethos was actually reporting is untouched by that fix, and
   is still there.** `((_ extract 1 0) a)` — the SMT-LIB spelling, in a committed
   regression test — is accepted by logos and refused by the ethos on this
   machine. It is now `logos-6` in the register, as an open question rather than
   a row, because it is unconfirmed against the reference build and logos
   themselves flagged it as possibly an artefact of their ethos.
3. The row's severity and direction were right and its subject was wrong, which
   is the worst combination: a true headline over a reproducer that does not
   support it.

**What changed here.** The reproducer is removed from `tests/fuzz/` and the row
is closed as withdrawn. `shrink` now refuses to touch a case whose source is a
seed run as it stands, with the reasoning in its docstring and a case in
`tests/fuzz_cases.py` that fails if the guard goes away. The argument is not that
shrinking is bad — for a case the fuzzer generated it is most of what makes the
corpus readable — but that for a file somebody else committed the finding *is*
the file, and an edit restates it as a claim about a file nobody has.

**What did not change, and is the harder question.** A coarser bucket than the
thing being claimed is what let this through, and that is not specific to seeds:
any shrink can keep an edit the verdict never depended on. A shrinker that asked
the reference *where* it refused, and required that to stay put, would have
caught it. That is a real change to `judge` and to what an `Outcome` carries, and
it is not one to make while writing up the row it would have prevented.

#### logos-5: declined, and documented

The refusal is deliberate. logos reads a proof as an assumption set together with
the steps that refute it, and that shape is what its correctness theorem is
stated over, so accepting a mid-proof `assume` would change what a proof *is*
there rather than fix a parser. What was missing is that `docs/parser.md` claimed
syntactic parity with ethos without recording the restriction; it now records it,
with regression guards. The reproducer will keep reproducing and the row is
closed as declined rather than as fixed — which is what logos asked for, and the
distinction `FUZ0005` exists to make: refusing what the reference accepts costs a
user a proof and guarantees nothing false.

The documenting sentence is in the same uncommitted working tree as everything
else on that branch. That does not hold the row open, because what closes it is
the decision not to change the behaviour, and that decision does not need a
commit to be somebody's.

#### And a correction to our ledger, from logos

Answering the rows against the copy, logos went and looked at what the copy is a
copy *of*, and found that three rows we had closed as *fixed upstream* were not
fixed. That is [cvc5-1](#cvc5-1-what-we-recorded-as-fixed), above, and it is the
most valuable thing in the reply.
