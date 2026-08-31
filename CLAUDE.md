# Working on anoieu

**Start at [`docs/coherence.md`](docs/coherence.md).** It is the maintenance
entry point: what this repository is responsible for, which documents may not be
changed without asking a person, and what the open technical work is.

Three things that are true before you read anything else:

- **Leave work staged, not committed.** A person reviews the diff and commits.
- **Some documents need permission.** `docs/vision.md` and `docs/policy.md`
  first, then `docs/reporting-policy.md` and the prompts in
  `docs/reporting-workflow.md`. The ladder is in `docs/coherence.md`.
- **Weakening a claim needs nobody; strengthening one needs a person.**

Run `python3 tests/run.py` and `python3 tools/policy_check.py` before handing back.

`policy_check.py` enforces `docs/policy.md`. Nothing enforces `docs/vision.md`,
and nothing may: it is argued, not checked.
