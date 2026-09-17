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

The checker interface and workflow are implemented here. Existing consumers
have not been migrated by this change, and must wait for this implementation
to be available on `main` before using the workflow above.

Kanon's current [adoption instructions](https://github.com/ajreynol/kanon/blob/main/docs/policy.md#2-run-the-check)
still require commit pins and disclaim compatibility. Those instructions need
to adopt this contract, replace the per-consumer bumping requirement for the
policy checker, and distinguish the contract from a governance revision.
Kanon holds that ecosystem decision; anoieu supplies the tested interface.

Koine's joining guidance should then point at this workflow. `eo_bump` still
serves dependencies that require exact commit pins; it is no longer needed
for policy-checker consumers that migrate to this interface. Remove a
consumer's lock and bump configuration only if nothing else uses them.
