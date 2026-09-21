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

**Seventeen claims, every one τεκμήριον, and one of them found by a job going
red — the only one.** This is
[zetesis's `F5`](https://github.com/ajreynol/epikrisis/blob/main/tools/zetesis/docs/findings.md)
with instances attached: the parent's CI was green throughout, its policy checker
reported zero failures, and its documentation-currency job reported 16 of 16
documents carrying a date. **Every claim below was false while all three of those
said what they say.**

| # | where | the claim | what was true instead |
| --- | --- | --- | --- |
| 1 | the documentation index | the report card is at `kanon/tools/stathmos/report-card.md` | `kanon/tools/stathmos/docs/report-card.md` — kanon moved its children's documents on 2026-09-18 |
| 2 | `docs/history.md` | sapheneia is at `kanon/tools/sapheneia/README.md` | it is a child of **eunoia**, at `eunoia/tools/sapheneia/` |
| 3 | `docs/history.md` | `kanon/scripts/ecosystem/ecosystem.py` is the program that reads the inventory | no such file; that directory holds JSON only |
| 4 | `anoieu_fuzz/README.md`, `docs/discussion.md` (×3) | ynoia's registers are at `kanon/tools/ynoia/{papers,tools,why-eunoia}.md` | all three are under `tools/ynoia/docs/` |
| 5 | `anoieu_analyzer/diagnostics.py` | SARIF output names `https://github.com/cvc5/anoieu` as the tool's repository and rule documentation | that repository does not exist; it is `ajreynol/anoieu` |
| 6 | `policy_check/checker.py` | two skipped rules are "checked elsewhere: `prompts_agree` in tests/run.py" | `tests/run.py` had no such function. Printed on every run, in every member repository |
| 7 | `policy_check/checker.py` | the policy asks a repository with a result to write it up in `report/` | neither `policy.md` nor `vision.md` mentions it. Reported by dokimasia twice before it was removed |
| 8 | `docs/maintenance.md` | ownership is recorded as `**Owner:** handle — Name, affiliation.` | the shared policy asks for a link to its own list *instead of* the name, handle or affiliation — and the parent's own check required the forbidden form |
| 9 | `config/deps.lock` | the lock records the commits `docs/reports/corpus.md` reports on | that page is `bug_db/corpus.md`; the generator already said so and the committed file had not been regenerated |
| 10 | `bug_db/bugs.md`, `bug_db/static-analysis.md` | 74 static findings, with no status | 61 of them had been ruled on. The generated views rendered no `closed_*` field, and both were *current* by their own `--check` |
| 11 | `bug_db/README.md` | `run.py --pinned` "regenerates the legacy reports too" | there are no legacy reports; it re-measures into `bug_db/corpus.md` |
| 12 | the documentation index | "anything that does not belong in the six above belongs here", on the sixth row | five rows precede it. The index has since moved to the front page and the sentence went with the row |
| 13 | the tree as a whole | the shared policy says anoieu keeps the reporting policy | no such page existed for a day: it was deleted with the workflow it was filed beside, and the only statement of it left was a summary inside a live discussion topic |
| 14 | `docs/discussion.md`, a live standing invitation | two child projects "exist here", and a report against this repository is recorded in `tools/martyria/reports.md` | both left with epikrisis on 2026-09-14; `tools/` here holds one child and that path does not exist. The invitation had been telling other tools for five weeks where to send something, and the place was not there |
| 15 | `bug_db/corpus.md` | ethos was measured on ref `ethosEoc3` at `fe74fe40e7f1` | the generator reads the ref from `config/deps.json`, which had been changed to `main` — so regenerating the page made it say `main` beside a commit that is not on `main`. **The parent's CI was red on this**, and the only repair its own error message offered was to commit the false version |
| 16 | `config/deps.json` | logos is at `https://github.com/ajreynol/logos.git` | the project is `cvc5/logos` — cvc5's own commits link `cvc5/logos/pull/…`, and the ecosystem register records that url. The manifest named a personal mirror as the project we publish findings about |
| 17 | `verdicts.py --check` output | seven ethos closures are still owed a landing | the change had landed on ethos `main` as [#241](https://github.com/cvc5/ethos/pull/241), squash-merged under a new commit id. The audit asked whether the *branch* commit was an ancestor of `main`, which it will never be, so it reported the debt as outstanding for a change that was already in |

**Re-derive any row** by resolving the path it names against the tree it names,
at the commit this entry was written. Rows 5 through 15 are settled by reading
one file in the parent's own checkout; rows 1 through 4, 16 and 17 need the other
repository, which is the finding below.

### What the seventeen say, which is more than seventeen facts

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

**Three of the seventeen are a document describing the tree it sits in.** Rows 6,
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

**And the count nobody can calibrate is the one that matters.** Seventeen is how
many one session found, not how many there are. The register says what was
checked; it says nothing about the rest, and the parent's own reporting policy
forbids turning that into a coverage number.

### What would have caught each

| row | what would have caught it | exists? |
| --- | --- | --- |
| 1–4 | resolving a cross-repository link against a checkout of the named repository | **now yes, as a command**: `python3 -m policy_check.outbound`, added 2026-09-21, which found four more of these on its first run. Still no — as a *check*: it is a contract 2 candidate, and a gate that fails for somebody else's rename is the thing being avoided |
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
| 16 | comparing a manifest url against the ecosystem register's url for the same project | no — the register is another repository's file, which is the row 1–4 problem again |
| 17 | asking by patch identity rather than by ancestry | **now yes**, in `verdicts.py`, which also names the commit that carries the change |

**Seven of seventeen have no mechanical form at all**, which is the project's own
question answering itself: the evidence that these documents are accurate is
still *somebody read them*, and this register is the record of which somebody,
when, and what they found.

**Row 14 has a cheap-looking fix and it is not proposed here.** A committed path
written in a code span is invisible to a link check, and a check that resolved
every backticked path would fire on every illustrative path in every document —
which is the parent's own standard for what not to build. Whether a narrower form
exists is a question for the parent; this register's job is to have the instance
rather than the answer.

## 2026-09-21 — the second pass, and the sharpest entries yet are in executing code

**Eleven claims, every one τεκμήριον, and three of them were printed on every
member repository's build.** The first pass found that the worst shape a stale
claim takes is *a document describing the tree it sits in*; this pass sharpens it.
**The worst shape is a claim about somebody else's document, made by a program, in
their build.** Rows 20 to 22 are that, and one of them had been named on the
shared policy's own coverage page before anybody here looked.

| # | where | the claim | what was true instead |
| --- | --- | --- | --- |
| 18 | `policy_check/checker.py`, `check_children` | a child project that runs in the parent's CI, is named by parent code, or appears on its front page must claim an exception in its charter, or the build **fails** | all three are expressly permitted: isolation is optional, advertising is the default, and integration with the parent requires "neither an exception nor promotion". The shared policy's own coverage table had named the mismatch |
| 19 | the same check, in effect | — | **eight children** in five repositories carry a sentence claiming that exception. Every one wrote it to satisfy this check; none of them needed to |
| 20 | `policy_check/checker.py`, the coverage list | three child-project rules, described by wording the shared policy had replaced — *nothing leaves the island by machine*, *additive never authoritative*, *it cites what it inherited* | the rules read *cross-repository feedback goes through the parent*, *an independent account does not confer authority*, and *it explains why the parent is its home*. Printed on every run in every member repository |
| 21 | `policy_check/checker.py`, `check_prompt_gate` | every discussion file should carry *a prompt may not be for this repository*, reported as a minor finding on ten members' trees | the shared policy removed it on 2026-09-20 and abandoned making it fatal, saying the implementation decision was the parent's |
| 22 | `policy_check/tests/policy-v1.json` | the snapshot holds what contract 1 fixes | it held the requirements and the severities and **not the applicability**, which the contract fixes equally — so a check widened from the parent's tree to every member, the one thing the contract forbids, was invisible to the suite |
| 23 | `anoieu_fuzz/README.md` | the fuzzer was folded into the parent because of "the island rules it had to break in order to be useful" | there are no island rules; a child may share all three of the things it broke. A retired rule cited in the present tense as the reason for a past decision |
| 24 | `docs/history.md` | the `report/` convention *did not survive the handoff* to kanon | it survived intact in the handoff commit and was deleted the next morning in a simplification pass. Established by kanon, in their own tree, at the parent's asking |
| 25 | `docs/maintenance.md` | *our request in `discussion.md`* describes the coverage gap | the request had been answered and the topic removed. A live pointer into a file whose contents move by design |
| 26 | `docs/history.md` | kanon keeps what is unresolved about role handoffs at `board.md#a-handoff-of-a-role-is-an-ordinary-item-here` | no such heading; the procedure is `roles.md#how-a-role-is-handed-off`. **The path resolved and the section did not**, which is the half a careless repair leaves behind |
| 27 | `docs/history.md` | martyria's stances are at `epikrisis/tools/martyria/stances.md` | `tools/martyria/docs/stances.md` — epikrisis put its children's documents under `docs/` |
| 28–29 | `tools/tekmerion/README.md`, `docs/register.md` | zetesis's findings are at `epikrisis/tools/zetesis/findings.md` | `tools/zetesis/docs/findings.md`, same move. **Two of these were this project's own pages**, citing the finding this project rests on |

**Re-derive rows 18 and 21** by checking out the parent at `2e32912` and running
its own checker against any repository in this ecosystem holding a child project;
rows 20, 22, 23 and 25 by reading one file in the parent's tree at that commit.
Row 19 is a count over five trees and is the one row here that needs them.
Row 24 is settled by reading kanon's `7eb9973` and `d892fa6`. Rows 26 to 29 are
settled by `python3 -m policy_check.outbound`, which is the command the parent
wrote in order to find them and did not have when the pass began.

### What the second pass says that the first did not

**A check is a claim, and it is the one kind that recruits.** Row 19 is what makes
this pass worse than the first. A stale sentence in a document is read and
disbelieved; a stale sentence in a *check* is obeyed. Eight children wrote a
statement about a rule that no longer existed because a program asked them to, and
every one of those statements is now a small stale claim in somebody else's tree,
put there by this one. **The parent's checker is the only document here that can
propagate its own errors into repositories that never read it.**

**And a contract can promise something no test compares.** Row 22 is the quietest
entry in this register and possibly the most useful: the parent published a
stability promise in three parts, wrote a snapshot test, and the snapshot covered
two of them. Nothing was wrong in the tree — the gap was between a promise and its
instrument, and no reading of either alone would find it. It took asking *what
would have caught this* about a change already made.

### What would have caught each

| row | what would have caught it | exists? |
| --- | --- | --- |
| 18, 20, 21 | comparing the checker's rule descriptions with the policy text they claim to describe | **no**, and it needs the other repository's prose — the rows 1–4 problem in its hardest form. Nothing compares a *paraphrase* to its source |
| 19 | nothing. The cost of a wrong check is in other people's trees and no run here can see it | no |
| 22 | recording applicability in the contract snapshot, so a narrowing or widening is a test failure | **now yes**, in `policy_check/tests/cases.py` |
| 23, 24, 25 | nothing mechanical. All three are prose that was true when written | no |
| — | asserting that every path and function name in the checker's coverage list exists | **now yes**, in `tests/run.py`. This is row 6's missing form, built for row 6 and it would not have caught any row above: the coverage list's *names* were real, and its *descriptions* were stale |

**The last line is the honest one.** Row 6 asked for a check that a named test
function exists, that check now exists, and it catches nothing in this pass.
**What went wrong here was never a name; it was a paraphrase of somebody else's
rule, drifting while the name stayed valid.** A checker that quotes a policy it
does not hold has no mechanical defence against the policy changing, and saying so
is more use than a check that would have looked like one.

**Eleven of twenty-nine now have no mechanical form**, up from seven of seventeen,
and the ratio moving the wrong way is the result rather than a disappointment: the
first pass found what a link checker misses, and this one found what no checker in
this tree can reach.

**Rows 26 to 29 are the encouraging half, and they are encouraging for an
uncomfortable reason.** They were found because the parent stopped treating the
cross-repository gap as somebody else's to close and wrote the command — and the
command immediately found four more instances, two of them on this project's own
pages, one of them a citation of the finding this whole project rests on. **A
register that cites a moved file is the failure it exists to record**, and the
only reason it is here rather than unnoticed is that somebody built the instrument
rather than waiting for the contract.
