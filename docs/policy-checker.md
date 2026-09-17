# The policy checker contract

Use the latest anoieu implementation and select the mechanical policy contract:

```bash
python3 scripts/policy_check.py --policy-version 1 --root path/to/repository
```

The implementation receives fixes without requiring each consumer to maintain
an anoieu commit pin. The contract selects the requirements the consumer is
checked against. `--version` prints the full implementation commit; every check
run logs that commit, the selected contract, and the repository being checked.

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

[`tests/policy-v1.json`](../tests/policy-v1.json) records the blocking and
advisory checks. The adoption fixtures in [`tests/run.py`](../tests/run.py)
exercise compliant and noncompliant members, associates, discussion gates,
and child projects with both the default and explicit version 1. A new version
must have its own registry entry and fixtures while these continue to pass.
Bug fixes need a regression case demonstrating the implementation error; a new
requirement must not be introduced as a bug fix.

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

**A written document outside `docs/` is outside the layout.** The layout says every
written document lives in `docs/` and is named in the index; the index check
enumerates `docs/` and nothing else, so a committed Markdown file at the repository
root is invisible to it. Found in anoieu's own tree on 2026-09-17. Widening the
index check to the root is a new obligation on everybody who keeps one, which is
why it waits.

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
carry both forms as of 2026-09-17**, name the contract page as the authority for
what a contract fixes, and state the trade in their own words. That was the half
this interface was waiting on.

**Koine's joining guidance is the remaining half.** `eo_join` writes a pinned
workflow, so a repository joining today takes the pinned form by default. Whether
it should offer the contract form is koine's decision. `eo_bump` still serves
every dependency that needs an exact commit; it is not needed by a policy-checker
consumer on the contract form, and a lock should be removed only where nothing
else uses it.

**Members on the pinned form are not behind.** Read on 2026-09-17, aisthesis,
epikrisis, eschaton and tachyon each pin deliberately and say why, and dokimasia
pins with a bump script that refuses a commit anoieu's CI was not green at.
**That is the requirement working**, not a migration that has stalled.
