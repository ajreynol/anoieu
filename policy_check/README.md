# Repository policy checking

This directory owns anoieu's policy-checking responsibilities: the checker,
contract, documentation-currency report and regression fixtures. It is separate
from static analysis, fuzzing and their bug database.

| file | responsibility |
| --- | --- |
| [`checker.py`](checker.py) | versioned mechanical checks and CLI |
| [`currency.py`](currency.py) | advisory documentation-currency report |
| [`outbound.py`](outbound.py) | links into other ecosystem trees, resolved against local checkouts. A command, never a gate |
| [`tests/`](tests) | contract snapshot and reader/adoption fixtures |
| [`maintenance.md`](maintenance.md) | guidance for maintaining and extending checks |

Run `python3 -m policy_check.tests` for the focused suite. The repository suite
also runs it. `python3 -m policy_check` and the stable human launcher
`python3 scripts/policy_check.py` use the same implementation. The shared CI
workflow remains in [`.github/workflows/policy.yml`](../.github/workflows/policy.yml),
where GitHub requires it.

## The policy checker contract

Use the latest anoieu implementation and select the mechanical policy contract:

```bash
python3 scripts/policy_check.py --policy-version 1 --root path/to/repository
```

The implementation receives fixes without requiring each consumer to maintain
an anoieu commit pin. The contract selects the requirements the consumer is
checked against. `--version` prints the full implementation commit; every check
run logs that commit, the selected contract, and the repository being checked.

**What a joining repository is actually asked for is two files**, and everything
else this checker carries reports `skip` naming the path that would switch it on
— *nothing at docs/discussion.md — this check turns on if you add one*, and so
for the documentation index, `.gitignore`, `tools/` and the rest. Measured by
kanon on 2026-09-18 against a tree of exactly the README and the workflow their
joining section gives, at contract 1: **0 failures, 14 skipped**. A discussion
file is **not** in that set — the response gate becomes fatal only once one
exists — and a cascade cannot happen, because there is no first failure to
trigger it. Kanon's joining section is the authority on what is asked; this
paragraph says what the checker does with it.

## What version 1 promises

Version 1 is the mechanical contract supported when this interface was
introduced on 2026-09-17. It is the default, and the default stays 1 even when
additional versions are introduced. CI consumers should spell it explicitly.
It is not a version of kanon's governance documents and does not declare that
all of the shared policy is mechanically checked.

Within version 1:

- Requirements and their applicability remain stable. Adding an obligation or
  applying an existing one to more repositories requires a new contract.
- Blocking checks remain blocking; advisory checks remain advisory. Changing
  severity requires a new contract.
- Implementation bugs can be fixed. Correcting a false positive can make a
  failing tree pass; correcting a missed violation can make a passing tree
  fail. Stability preserves the requirements, not bugs in their implementation.
- The entry point `scripts/policy_check.py`, `--root`, `--policy-version`,
  `--coverage`, and `--version` remain supported. A file move must retain a
  forwarding entry point.
- Exit codes are 0 for no blocking findings, 1 for blocking findings, and 2 for
  invalid command arguments, including an unsupported contract. Unknown
  contracts are never silently treated as the latest supported version.

Diagnostic wording and coverage explanations can improve. Terminal text is
for people; it is not a stable machine-readable schema. The chosen contract's
coverage is available with `--policy-version 1 --coverage`.

[`policy_check/tests/policy-v1.json`](tests/policy-v1.json) records the blocking
checks, the advisory ones, **and where each one applies** — the third thing this
list promises and, until 2026-09-21, the one nothing compared. A check quietly
widened from this tree to every member is precisely the new obligation the
contract forbids, and a snapshot of names and severities could not see it. **Some of them never run on a member's tree**: a check whose
applicability is *home-only* is one this repository holds itself to, it reports
`skip` everywhere else, and adding one is not an added obligation on anybody. The
registry lists it all the same, because a reader comparing two contracts should
see every check the implementation carries rather than a filtered view. The adoption fixtures in [`tests/cases.py`](tests/cases.py)
exercise compliant and noncompliant members, associates, discussion gates,
and child projects with both the default and explicit version 1. A new version
must have its own registry entry and fixtures while these continue to pass.
Bug fixes need a regression case demonstrating the implementation error; a new
requirement must not be introduced as a bug fix.

**What a link may point at is one of those fixes, made 2026-09-19.** The anchor
check recognised heading slugs only, so a valid link to an explicit
`<a id="...">` anchor — a numbered subclause, or an alias retained so that links
written before a renumbering keep resolving — was reported as a missing heading,
and the only way past it was to promote a paragraph to a heading. Reported by
kanon as their `D20`. Widening what counts as a target can only turn a failure
into a pass, so it stays inside contract 1; the regression case is
`anchor_targets` in [`tests/cases.py`](tests/cases.py).

**And the child-project island exception is retired, in place, 2026-09-21.**
`check_children` used to **fail** a child project that ran in the parent's CI, was
named by code outside its own directory, or appeared on the parent's front page,
unless its charter claimed an exception by citing the rule number that once
granted one. Every one of those three is now expressly permitted: *its boundaries
are explicit; isolation is optional* lets a child import parent code, provide
artifacts to other projects and join the parent's tests and CI; *its parent
chooses whether to advertise it* makes advertising the **default**; and *a child
that delivers says what it delivers and for whom* closes it, saying that shared
usefulness and integration with the parent require "neither an exception nor
promotion". The shared policy's own coverage table named the mismatch before we
did.

**A requirement the policy no longer states cannot be an obligation of contract
1 either**, so removing it is a fix and not a relaxation — it can only turn a
failure into a pass, and a charter that still carries the old sentence is
unaffected, because nothing reads it now. What replaces it is an observation: the
run prints the shared surfaces a grep can see, because a charter is asked to
*name* its shared entry points, dependencies and outputs, and whether it does is
reading. The regression case is `integrated-child` in
[`tests/cases.py`](tests/cases.py) — a child doing all three things with a
charter that mentions none of them, which the previous implementation failed.
The cost of having had it is measurable: **eight children across this ecosystem
carry a sentence claiming an exception in order to satisfy a check**, and none of
them needed to. A charter that still carries it is not wrong, only unread.

**One check is narrowed to this tree rather than deleted, 2026-09-21.** *A prompt
may not be for this repository* was reported as a minor finding on every member's
tree; kanon removed it from the shared policy on 2026-09-20 as an internal
operational instruction, abandoned the proposal to make it fatal, and said the
implementation decision was ours. **A finding published against ten trees for a
paragraph in no shared page is a claim about somebody else's document that their
document does not make** — the same defect as the `report/` convention, which we
published the same way and withdrew for good. So `check_prompt_gate` is
**home-only** now: this repository keeps holding itself to a rule that has fired
twice in opposite directions, and grades nobody else on it. Ten members carry the
paragraph today and none of them was obliged to; none of them loses it by our
stopping. Narrowing applicability removes an obligation rather than adding one, so
it stays inside contract 1 — and the snapshot above now records it, which is how a
later widening would be caught.

**What the coverage list claims is now compared with the tree, 2026-09-21.** The
list of rules with no automated check is printed on every run in every member
repository, and two of its lines named a test function that did not exist. Since
that text is the most widely published prose here, `coverage_names_real_things`
in [`../tests/run.py`](../tests/run.py) resolves every path it names and every
`snake_case` name it offers as standing in for a check. A coverage reason is a
claim about this tree like any other.

## Which requirement governs the `anoieu / policy` job

**Both forms are allowed and a repository picks one; what differs is what may
move under it.**

- **A pin.** The member names a checker commit. Nothing changes until the member
  moves it, and **anoieu's requirement applies: move a pin only onto a commit
  where anoieu's CI was green, ask about that commit rather than about the tip,
  and fail closed when the answer cannot be established.** A pin holds an
  implementation, so it also holds that implementation's idea of *where the
  policy lives* and every check it happened to carry.
- **A contract.** The member names `policy-version: '1'` and follows current
  `main`. The **obligations** are fixed; the implementation is not.

**The two requirements do not collide, because the first one is about moving a
pin and a repository on the contract form has no pin to move.** Reported by
dokimasia as their `D11`, and it is worth saying plainly rather than leaving to
be inferred.

**And the thing they asked us to confirm is true rather than a misreading: on the
contract form a build can go red with nothing committed.** A corrected false
negative starts reporting a violation that was already in the tree, and an
implementation regression is possible like any other. What contract 1 rules out
is a **new obligation** arriving that way. A member who wants the stronger
property — no change at all without a commit of their own — should pin, and that
is a legitimate choice rather than a lagging one.

**When a pinned checker and the current policy disagree, the policy wins and the
answer is to bump.** A pin selects an implementation and not a policy text, so a
member sitting on an older commit can be asked for something the policy has since
removed, or told to link a page that has since moved. **The checker is never the
authority on what the policy says.** Where the two disagree: write what the policy
publishes, move the pin to a green commit, and the finding goes. Raised by
aisthesis as their `D1` and by epikrisis as their `D3`, each from a pin that
asked for something the policy no longer says — a `**Status:**` field on a
discussion topic, and a declaration naming anoieu rather than kanon. **A member on
the contract form never meets this**, which is the clearest thing that can be said
for that form.

## What a new contract would carry

Recorded here so that a request can be argued with rather than repeated. **None
of these is in contract 1**, because each adds an obligation to a tree rather than
correcting an implementation, and the point of the contract is that a member's
build does not acquire work it did not choose.

**A link into another repository in this ecosystem should resolve.** `check_links`
skips every target beginning with `http`, so a cross-repository link is the one
link nothing checks — and both repositories that have looked for these have found
them: ten of dokimasia's into anoieu after a rename here, and eight of anoieu's
into kanon after the governance handoff. Requested by dokimasia as their `D3`,
2026-08-31. Two conditions come with it. A `<ref>` that is not the branch being
checked is a link to a *version* and must be skipped rather than resolved against
whatever is checked out. And the shared workflow runs current `main`, so a member
pins nothing: an unpinned cross-repository check would turn every member red on
one rename here, with no commit anywhere near them. Whatever form this takes is
likelier to be advisory than blocking.

**What is built meanwhile is the half that needs no contract**, and it found
four dead links on its first run. `python3 -m policy_check.outbound` resolves every
link this repository makes into another ecosystem tree against a local checkout of
that tree: forty-four links, four dead — a board heading kanon no longer keeps, and
three paths in epikrisis that moved when it put its children's documents under
`docs/`. All four had been invisible to two green builds. **It is a command and
must never become a gate**, for the reason the candidate is a candidate: it fails
for a rename in a tree nobody here touched. It also refuses to count a repository
it has no checkout of as passing, and says how many links it could not ask about.

**Meanwhile the cheap instrument is the mover, and one repository has taken it
on.** We asked kanon for it as our `D40`, having published our own was-to-is table
first; kanon accepted on 2026-09-19 and wrote it into its maintenance guide — a
move notice there carries one row per path, old and new, and a deletion says
*deleted* and names what holds the register now. **It binds kanon's own notices
and no member**, which is the right scope for it: a rule in the shared policy
would oblige every repository, and that is a person's decision. It repaired
fourteen dead links in their tree and six in ours, which is the measurement worth
keeping beside the candidate. It does not close the candidate: a mover who does
not write a table is still undetectable from either end.

**The ownership link is decided here and nowhere else, and kanon has been asked
whether it should be wider.** `check_owner_unadvertised` reads the requirement as
the shared policy writes it — a page identifying ownership links the ecosystem's
maintainer list rather than naming a person — and it is **home-only**, because
applying an existing requirement to more repositories adds an obligation. Raised
as our `D39`; kanon answered on 2026-09-19 that it is **not** asking for the
widening, corrected its own page to say the requirement is decided mechanically
in this tree alone, and carries the decision as `B43` on its board for a person.
So the check stays home-only until somebody decides otherwise, and this paragraph
is the record that the question was asked and answered rather than left open.

**Every written document is named in the index, wherever it lives.** The index
check enumerates `docs/` and nothing else, so a document anywhere else is
invisible to it — a committed Markdown file at the repository root, or, since
2026-09-19, this repository's own documents, which deliberately sit beside the
thing they describe. Widening the enumeration to a whole tree is a new obligation
on everybody who keeps an index, which is why it waits. **Anoieu holds itself to
it meanwhile**, in the home-only `check_every_document_indexed`, so the shape is
worked out on our own tree before it is proposed to anybody.

## The shared CI workflow

Once this interface is published, consumers can use this entire
`.github/workflows/anoieu.yml`:

```yaml
name: anoieu

on: [push, pull_request]

permissions:
  contents: read

jobs:
  policy:
    uses: ajreynol/anoieu/.github/workflows/policy.yml@main
    with:
      policy-version: '1'
```

Anoieu maintains [the called workflow](../.github/workflows/policy.yml). It
checks out the caller's tree and current anoieu `main` into separate directories,
then runs the selected contract. Consumers do not need `ANOIEU_REV`, an
`anoieu.lock`, or a custom clone-and-check script for this policy check.
The caller keeps its own workflow triggers and branch protection settings.
GitHub documents this mechanism in
[reusable workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations).

**Two things about this workflow are not established, and absence is not a pass.**
Nothing exercises it: it is published for members, and no run of ours calls it, so
the evidence that it works is the runs in members' trees rather than anything here.
And **this repository does not itself keep a check named `anoieu / policy`** — the
shared convention it publishes to everybody else. Our own `ci.yml` runs
`scripts/policy_check.py --policy-version 1` on every push, which is the same
decision by the same code, under the name `ci / policy`. So the contract is met and
the convention is not, and the two are worth separating rather than eliding. Both
are a person's to decide; recorded 2026-09-21 so that neither is discovered as a
surprise.

Following `main` deliberately accepts implementation updates. A rerun can use
a different implementation commit, including a bug fix that corrects a verdict;
the logged commit is the evidence for what actually ran. The compatibility
promise is protected by anoieu's tests, not a guarantee that software cannot
have a regression. This arrangement concerns the policy checker: analyzer
corpora and reproduction dependencies retain their own pins.

## Migration across the ecosystem

The checker interface and workflow are implemented here, and consumers migrate
on their own schedule. Nothing about this change migrates anybody.

**Kanon's [adoption instructions](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#2-run-the-check)
carry both forms, re-read 2026-09-21**, name the contract page as the authority for
what a contract fixes, and state the trade in their own words. That was the half
this interface was waiting on.

**Koine's joining guidance points at Kanon's adoption instructions.** `eo_join`
sends a repository to that page for its workflow. Koine itself uses the shared
workflow at `main` with contract 1 and has no checker lock to update. Other
dependencies can still need exact commits; remove a lock only where nothing
else uses it.

**Members on the pinned form are not behind.** Read on 2026-09-19, five repositories
call the shared workflow and name contract 1 — epikrisis, kanon, koine, logos and
tachyon — and four pin deliberately: aisthesis and eschaton at `154228a`,
eudaimonia at `dc2c613`, and dokimasia through a lock its own `bump_anoieu`
refuses to move onto a commit anoieu's CI was not green at. **That is the
requirement working**, not a migration that has stalled.

**And a pin holds a policy's address as well as its rules**, which is the cost
epikrisis reported in their `D5` and the reason they left the pinned form. A
member sitting on a commit from before the governance handoff has a checker whose
declaration check names the repository the policy used to live in, so writing the
declaration the policy publishes turns their build red while keeping it green
links a reader to a policy that is not there. Nothing can fix that at the old
commit; the contract form is what removes the trap, and naming the trade is the
whole of what a member needs in order to choose.
