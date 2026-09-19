# The register: claims found to have gone false

**One row per claim, and each says which of the two it is.** The charter names
the standard — τεκμήριον, conclusive evidence, against σημεῖον, a sign that may
point the other way — and the guard against confusing them lives here: **an
entry that cannot say which it is has failed**, and is worse than no entry.

| kind | what it takes |
| --- | --- |
| **τεκμήριον** | a command somebody with no reason to believe us can run, whose output settles the claim. A path that does or does not exist; a string that is or is not in a file |
| **σημεῖον** | anything weaker, including *somebody read this page on this date*. Worth recording and never worth more than it is |

This is written by whoever does the work, from the parent's own tree, and it is
not a schedule: a claim reaches this page when somebody finds it, which is the
limitation the whole project is about.

**What it is not.** It does not grade a document, judge whether a claim was
worth making, or certify anything as current. A page absent from this register
has not been checked.

## 2026-09-19 — the first pass, from one session in the parent's tree

**Fifteen claims, every one τεκμήριον, and one of them found by a job going
red — the only one.** This is
[zetesis's `F5`](https://github.com/ajreynol/epikrisis/blob/main/tools/zetesis/findings.md)
with instances attached: the parent's CI was green throughout, its policy checker
reported zero failures, and its documentation-currency job reported 16 of 16
documents carrying a date. **Every claim below was false while all three of those
said what they say.**

| # | where | the claim | what was true instead |
| --- | --- | --- | --- |
| 1 | `docs/README.md` | the report card is at `kanon/tools/stathmos/report-card.md` | `kanon/tools/stathmos/docs/report-card.md` — kanon moved its children's documents on 2026-09-18 |
| 2 | `docs/history.md` | sapheneia is at `kanon/tools/sapheneia/README.md` | it is a child of **eunoia**, at `eunoia/tools/sapheneia/` |
| 3 | `docs/history.md` | `kanon/scripts/ecosystem/ecosystem.py` is the program that reads the inventory | no such file; that directory holds JSON only |
| 4 | `anoieu_fuzz/README.md`, `docs/discussion.md` (×3) | ynoia's registers are at `kanon/tools/ynoia/{papers,tools,why-eunoia}.md` | all three are under `tools/ynoia/docs/` |
| 5 | `anoieu_analyzer/diagnostics.py` | SARIF output names `https://github.com/cvc5/anoieu` as the tool's repository and rule documentation | that repository does not exist; it is `ajreynol/anoieu` |
| 6 | `policy_check/checker.py` | two skipped rules are "checked elsewhere: `prompts_agree` in tests/run.py" | `tests/run.py` had no such function. Printed on every run, in every member repository |
| 7 | `policy_check/checker.py` | the policy asks a repository with a result to write it up in `report/` | neither `policy.md` nor `vision.md` mentions it. Reported by dokimasia twice before it was removed |
| 8 | `docs/maintenance.md` | ownership is recorded as `**Owner:** handle — Name, affiliation.` | the shared policy asks for a link to its own list *instead of* the name, handle or affiliation — and the parent's own check required the forbidden form |
| 9 | `config/deps.lock` | the lock records the commits `docs/reports/corpus.md` reports on | that page is `docs/corpus.md`; the generator already said so and the committed file had not been regenerated |
| 10 | `bug_db/bugs.md`, `bug_db/static-analysis.md` | 74 static findings, with no status | 61 of them had been ruled on. The generated views rendered no `closed_*` field, and both were *current* by their own `--check` |
| 11 | `bug_db/README.md` | `run.py --pinned` "regenerates the legacy reports too" | there are no legacy reports; it re-measures into `docs/corpus.md` |
| 12 | `docs/README.md` | "anything that does not belong in the six above belongs here", on the sixth row | five rows precede it |
| 13 | the tree as a whole | the shared policy says anoieu keeps the reporting policy | no such page existed for a day: it was deleted with the workflow it was filed beside, and the only statement of it left was a summary inside a live discussion topic |
| 14 | `docs/discussion.md`, a live standing invitation | two child projects "exist here", and a report against this repository is recorded in `tools/martyria/reports.md` | both left with epikrisis on 2026-09-14; `tools/` here holds one child and that path does not exist. The invitation had been telling other tools for five weeks where to send something, and the place was not there |
| 15 | `docs/corpus.md` | ethos was measured on ref `ethosEoc3` at `fe74fe40e7f1` | the generator reads the ref from `config/deps.json`, which had been changed to `main` — so regenerating the page made it say `main` beside a commit that is not on `main`. **The parent's CI was red on this**, and the only repair its own error message offered was to commit the false version |

**Re-derive any row** by resolving the path it names against the tree it names,
at the commit this entry was written. Rows 5 through 15 are settled by reading
one file in the parent's own checkout; rows 1 through 4 need the other
repository, which is the finding below.

### What the fifteen say, which is more than fifteen facts

**Four of the six stale links are into another repository, and the parent's
checker skips every one by design.** `check_links` resolves every committed path
and `check_anchors` every heading, and both stop at `http`. So the parent's link
checking is complete for its own tree and blind in exactly the direction where a
claim goes stale without anybody here touching anything. It is recorded as a
contract 2 candidate on the parent's contract page for a defensible reason — an
unpinned cross-repository check would turn every member red on one rename in a
tree they do not own — which makes this **a gap somebody chose rather than
missed**, and the honest measurement of it is a count like the one above rather
than an argument.

**Three of the fifteen are a document describing the tree it sits in.** Rows 6,
7 and 8 are the parent's own checker making claims about the parent's own tree
and about the shared policy, wrongly, on every run. That is the worst shape a
stale claim takes: it carries the authority of something that executes.

**Three are generated pages that were current and wrong at the same time**, and
these are the sharpest things in this register. `bugs.md` and
`static-analysis.md` passed `--check` on every push for as long as the closures
existed, because `--check` compares the page with what the generator would write
and the generator did not know about closures. Row 15 is the same failure with
the sign flipped: the committed page was *true* and the generator had started
producing something false, so the job that exists to keep the page current was
red, and doing what its error message said would have published the falsehood.

**A generated document cannot go stale against its generator and can go stale
against the world**, and the parent's documentation-index note — *generated
documents cannot go stale in this sense* — is true in the sense it means and
reads wider than it is. Row 15 sharpens it further: **a generator is itself a
claim about the world**, and when its inputs come from two registers that
disagree, regeneration is how the falsehood gets committed.

**And the count nobody can calibrate is the one that matters.** Fifteen is how
many one session found, not how many there are. The register says what was
checked; it says nothing about the rest, and the parent's own reporting policy
forbids turning that into a coverage number.

### What would have caught each

| row | what would have caught it | exists? |
| --- | --- | --- |
| 1–4 | resolving a cross-repository link against a checkout of the named repository | no — contract 2 candidate |
| 5 | comparing the SARIF surface with the register it restates | **now yes**, in `tests/cli_cases.py` |
| 6 | asserting that a named test function exists | no |
| 7 | comparing the checker's coverage list with the policy it claims to be listing | no, and it would need the policy's text |
| 8 | the check deciding the requirement as written, rather than its opposite | **now yes**, home-only |
| 9 | comparing a committed generated file with what its generator writes | partly — `--check` exists for two of the four generated pages |
| 10 | nothing mechanical. The page agreed with its generator | no |
| 11–12 | nothing mechanical | no |
| 13 | asserting that a responsibility the shared policy assigns this repository has a page | no |
| 14 | resolving a committed path named in a code span, not only one inside a link | no — the link checks read Markdown link targets, and this was neither a link nor `http` |
| 15 | comparing the generated page's ref against the lock that supplied its commit | **now yes**, in `tests/run.py`; and the generator takes both halves from the lock |

**Seven of fifteen have no mechanical form at all**, which is the project's own
question answering itself: the evidence that these documents are accurate is
still *somebody read them*, and this register is the record of which somebody,
when, and what they found.

**Row 14 has a cheap-looking fix and it is not proposed here.** A committed path
written in a code span is invisible to a link check, and a check that resolved
every backticked path would fire on every illustrative path in every document —
which is the parent's own standard for what not to build. Whether a narrower form
exists is a question for the parent; this register's job is to have the instance
rather than the answer.
