# Working on anoieu

**Start at [`docs/coherence.md`](docs/coherence.md).** It is the maintenance
entry point: what this repository is responsible for, which documents may not be
changed without asking a person, and what the open technical work is.

Three things that are true before you read anything else:

- **Leave work staged, not committed.** A person reviews the diff and commits.
- **Some documents need permission.** `tools/vision.md` and `tools/policy.md`
  first, then `docs/reporting-philosophy.md` and the prompts in
  `docs/reporting-policy.md`. The ladder is in `docs/coherence.md`.
- **Weakening a claim needs nobody; strengthening one needs a person.**

Run `python3 tests/run.py` and `python3 tools/policy_check.py` before handing back.

`policy_check.py` enforces `tools/policy.md`. Nothing enforces `tools/vision.md`,
and nothing may: it is argued, not checked.
