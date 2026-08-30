# The log: what was reported, and what came back

Every anoieu finding that has reached another repository and been ruled on.
[`README.md`](README.md) holds the other half — the open findings, which are
hypotheses nobody has judged yet. A row moves from there to here the moment it
gets a verdict, in either direction.

A finding that turns out to be wrong is the most useful thing on this page, so
those are written up at length: what we claimed, why it was wrong, and what the
analyzer does differently now.

## Where it stands

| verdict | count | which |
| --- | --- | --- |
| **fixed upstream** | 2 | `cvc5-1`, `cvc5-2` |
| **declined — our error** | 1 | `cvc5-4` |
| **overstated — claim corrected** | 1 | `cvc5-1`'s impact |
| **deferred** | 1 | `cvc5-3`, pending a documented convention |
| **not yet** | 1 | `cvc5-5`, pending a pinned release |

Changes the analyzer made as a result:

- **ordered profiles**, so reachability is asked in a world someone runs
  (`cvc5-4`);
- **profile-scoped findings**, so a local answer is never a repository-wide
  claim (`cvc5-4`);
- **three levels of impact kept apart** for a declaration that disagrees with
  its cases (`cvc5-1`);
- a regression case in `tests/cli_cases.py` for the arrangement that produced
  the wrong finding.

---

## cvc5 — the CPC signature

Reported against cvc5 commit `622a50a3`, assessed by the cvc5 maintainers, whose
response is reproduced in that repository as `anoieu-response.md`.

| item | what we said | decision |
| --- | --- | --- |
| **cvc5-1** | `$is_seq_const_rec` and `$is_seq_const` declare `Int` and return `Bool` | **accepted, fixed** — both signatures now return `Bool` |
| **cvc5-2** | four arithmetic skolem declarations duplicated in `expert/theories/ArithExt.eo` | **accepted, fixed** — the second block removed |
| **cvc5-3** | 18 documentation arity and field findings | **deferred** — documentation rather than calculus, and the convention for documenting a program's pattern variables has to be decided first |
| **cvc5-4** | `$is_app` is reached by nothing | **declined — our analysis was wrong.** See below |
| **cvc5-5** | run anoieu in CI, report-only then blocking | **not yet** — reasonable once the entry-point handling is fixed and a released version can be pinned |

Both accepted changes were verified on a temporary copy before landing: ethos
accepted the base and the base-plus-expert signature, and the `EO0031` and
`EO0064` diagnostics went away.

### cvc5-4: what we got wrong

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

### cvc5-1: what we overstated

The finding was right and the fix landed, but our *impact* claim did not
reproduce. We wrote that a use of `$is_seq_const` where a `Bool` is expected is
a type error; cvc5 found that a direct typed use checks as `correct`, because
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
[`findings.md`](findings.md) is corrected.

---

## What cvc5 asked for next

Recorded here because it is the clearest statement anyone has given us of what
would make the analyzer worth running. Tracked as items in
[`README.md`](README.md).

| request | state |
| --- | --- |
| ordered analysis profiles, and profile-scoped findings | **done** — above |
| reproducers that exercise the claimed failure, kept with the diagnostic | open |
| impact-aware severity: exhaustive cases, stuck applications, a reproduced rejection | open |
| reachability roots, traces (`lambda-elim -> $is_app`), and a way to mark public helpers | open |
| a check comparing each rule against cvc5's `ProofRule` declaration, its children and arguments, and `eo_printer.cpp` | open — would catch interface drift that makes an emitted proof uncheckable |
| documentation checks that compare names and roles, not counts, and distinguish call arguments from pattern variables | open — and it is why cvc5-3 is deferred |
| diagnostics naming the repository that owns the file | open |
| versioned releases, stable diagnostic meanings, path-independent baselines, a policy for narrowing a check without invalidating suppressions | partly — baselines are path-independent already; releases and the narrowing policy are not written down |

---

## ethos

Nothing filed yet. Four items stand in the register: the `<` declared
`:right-assoc` in `tests/match-simple.eo`, two test signatures using literals
whose category they never declare, a dead case in `naive-nary.eo`, and three
diagnostics worth improving.

## logos

Nothing filed yet. One triple finding stands: `Cpc.eos:546` has an entry for
`str.indexof_re_split`, which CPC does not declare. cvc5's response notes
correctly that this belongs to the repository that owns the semantics, not to
cvc5 — which is also the argument for the ownership field they asked for.
