# The board

**What is being maintained across the Eunoia ecosystem, in priority order.**
One page, at most twenty items, each with the next thing to do and who has to do
it. Written for a person to read in a minute and edit by hand.

Nothing consumes this file yet. It is written first, deliberately: a board that
is generated before anybody has kept one by hand encodes whatever the generator's
author assumed, and the assumptions are the part worth getting wrong cheaply.
What might read it later — a staleness check, a per-entity digest, a link from
each finding to its row — is easier to design against a page that has already
survived a few months of being edited.

## How to read it, and how to edit it

**Position is the priority.** The first item is the most important thing
outstanding; the last is the least. Reordering is done by moving a block, and
that is the main way a person changes what this page says.

**The id is stable.** `B4` stays `B4` when it moves, so ids appear out of order
and that is correct rather than a mistake to tidy. A row that leaves is not
reused: the next new item takes the next unused number.

**Twenty is a cap, not a target.** Adding a twenty-first means deciding which
one leaves, which is the whole value of the number. An item that is done, or
that nobody will act on, is deleted rather than archived — the record of what
happened lives in [`reports/reports.md`](reports/reports.md) and in git, and a
board that keeps its dead is a board nobody reads to the bottom of.

**Every field is a person's to overwrite.** `HUMAN FEEDBACK` is the one that
outranks everything else on its item: whatever it says wins over the status, the
prompt, and the position, and anything that ever reads this file is to treat it
that way. It is left empty rather than filled with a placeholder, because an
empty field is visibly unanswered.

Each item carries the same fields, in the same order:

| field | what it holds |
| --- | --- |
| **Task** | one line: what is being maintained, not how |
| **Entities** | the repositories involved, by the ids in [`../tools/ecosystem.json`](../tools/ecosystem.json) — `anoieu`, `cvc5`, `ethos`, `ethos-eoc`, `logos`, `eudaimonia`, `dokimasia`, `koine`, and the child projects `sapheneia`, `ynoia`, `euthyna`. No other name is an entity |
| **Status** | `ready`, `in progress`, `waiting on <entity>`, `blocked on <what>`, `not started`, or `parked` — plus one clause saying since when or on what |
| **Channel** | how the prompts below reach the entities they name: `discussion`, `findings`, `upstream, by a person`, or `internal`. The section after this one is what each means |
| **Next** | the single next issue to fix. One thing, not a plan |
| **Prompt — `<entity>`** | one per entity involved: what that repository would be asked to do, written so it can be handed over as it stands |
| **HUMAN FEEDBACK** | empty, for a person |

**A prompt here has not been sent.** Writing one down is drafting it; delivering
it is the next section, and a person's act either way.

## How a prompt is delivered

**A prompt on this page is not sent by being written here.** It reaches the
repository it names through the channel that repository actually has, and the
**Channel** field says which. There are three, and the difference between them
is not a formality:

| channel | what it means | who acts |
| --- | --- | --- |
| **discussion** | a topic in [`discussion.md`](discussion.md) addressed to them, or a reply into a topic of theirs — the standing channel for anything that is **not** a defect report | a person carries it; `scripts/prompts/process_discussion` reads theirs, and nothing here writes into anybody else's file |
| **findings** | a row in the ledger, carried by `scripts/prompts/check_anoieu <id>` and answered through `scripts/prompts/process_anoieu` | the same person, through the reporting workflow, which is a separate protocol on purpose |
| **upstream, by a person** | a message, an issue or a pull request in a tree that has no discussion file | a person, entirely — no script here has a way to do it, and none should |

**Only a member has a discussion file.** `anoieu`, `eudaimonia`, `dokimasia` and
`koine` have one; `ethos`, `logos` and `cvc5` have not joined and have none, and
a child project has none of its own and is reached through its parent. So a
board item addressed to a candidate is *always* the third row, and writing
`discussion` against one would be describing a channel that does not exist. That
is the shape this page adds to the protocol: the queue is here, the wire is the
discussion file, and where there is no wire the page says so instead of
pretending.

**The board does not replace either protocol, and does not shortcut them.**
Nothing is filed by being on this page, a prompt here is a draft rather than a
message, and a row is not closed by sending — it closes when the artifact it
names says what happened, which is the rule the findings ledger already keeps.

## A handoff of a role is an ordinary item here

[`roles.md`](roles.md) keeps what each tool is accountable for, and moving one
of those to another tool is proposed on this page like anything else: the
entities
are the holder losing it, the tool gaining it where the inventory has an id for
it, and every consumer whose pin moves. The channel is **discussion**, because
the point of writing it here is to be disagreed with by the repositories it
costs something, and there is one prompt per entity so that each has been asked
rather than told.

The seven steps are in
[`roles.md`](roles.md#how-a-role-is-handed-off), and `B15` is the worked example
— parked, and stated in role ids. **None of it gates anything** while the
ecosystem is still settling; the same section says what would change that and
who decides.

---

## B6 — the reporting protocol has two implementations and an approved home

**Task:** `dokimasia` built the same loop we did, in an afternoon, by reading
ours; `koine` was approved to hold the shared half. Their `D4`.
**Entities:** `anoieu`, `dokimasia`, `koine`
**Status:** waiting on `koine` — the repository exists and its scope is its
owner's to set.
**Channel:** **discussion** — a reply into `dokimasia`'s `D4`, and a topic in our file addressed to `koine`.
**Next:** answer `D4` by pointing at the approved proposal, and say which piece
we would fetch first.
**Prompt — `anoieu`:** reply to `dokimasia`'s `D4`: the shared parts become
something a member fetches, `koine` is the approved name, and the prompt-drift
check is the piece we would take first because it is the one guaranteed to rot in
two copies.
**Prompt — `dokimasia`:** the scope question is settled in principle; what is
still open is whose implementation the shared check starts from, and yours is the
second one, which makes it the better evidence.
**Prompt — `koine`:** nothing is owed. If you take the prompt-drift check first,
two repositories will drop their copies; if you take nothing, nothing here
breaks.
**HUMAN FEEDBACK:** raised to the top 2026-08-31: settling this enables a lot of other work.

## B3 — the fuzzer has found real defects and filed none of them

**Task:** `ethos-8` and `ethos-9` — an uncaught C++ abort on a one-line
signature, and error paths that print outside ethos's own `Error: <file>:<line>`
convention. Six reproducers are committed here; nothing has been sent upstream.
**Entities:** `ethos`, `anoieu`
**Status:** ready — the reproducers exist and are committed under `tests/fuzz/`.
**Channel:** **findings** — `ethos-8` and `ethos-9`, through `scripts/prompts/check_anoieu ethos`, because a defect report is not a discussion topic.
**Next:** file the two, with their reproducers, through the ordinary loop.
**Prompt — `ethos`:** `(declare-const f (->))` aborts with an uncaught
`std::length_error` rather than reporting a bad type. Separately, three error
paths exit without a file or line, which breaks the convention every other error
in the binary follows. Reproducers are committed and fetchable raw.
**Prompt — `anoieu`:** run `scripts/prompts/check_anoieu ethos` for these two rows, and
say plainly in the report that the fuzzer produced them — a provoked crash and a
read signature are different claims and the codes already say which.
**HUMAN FEEDBACK:** raised 2026-08-31: these are real defects and nothing is stopping us filing them.

## B4 — every member's build depends on this repository's tip

**Task:** the joining step clones `anoieu` at its default branch and runs the
checker out of that clone, so a member's CI can go red, or green, with no commit
of their own. Raised by `dokimasia` as its `D2`.
**Entities:** `anoieu`, `dokimasia`, `koine`, `eudaimonia`
**Status:** ready — the ask is precise and the fix is ours.
**Channel:** **discussion** — a reply into `dokimasia`'s `D2`, and a notice to `koine` and `eudaimonia` in our own file when the pinned step lands.
**Next:** give the joining page a pinned step, and name where the pin moves and
who moves it.
**Prompt — `anoieu`:** rewrite the CI snippet in `docs/policy.md` to pin a
commit, and say in the same paragraph how a member learns a newer pin is worth
taking. A build that can turn green without a commit cannot be evidence that a
commit was good, which is their argument and it holds.
**Prompt — `dokimasia`:** nothing until the page changes; the topic settles when
it does.
**Prompt — `koine`:** you joined most recently and paid this cost last. If the
pinned step reads wrong to you, say so before it is written down.
**Prompt — `eudaimonia`:** your workflow tracks the tip too. When the pinned
step lands, moving to it is one line.
**HUMAN FEEDBACK:**

## B2 — seven accepted ethos fixes that have not reached `main`

**Task:** the seven rows closed *awaiting landing* on `ethos` are all still one
commit off the default branch.
**Entities:** `ethos`, `anoieu`
**Status:** waiting on `ethos` — `tools/landing.py --check` reports all seven as
`not yet`, against a checkout fetched today.
**Channel:** **upstream, by a person** — `ethos` has no discussion file, so asking about a merge is a message somebody sends, not a topic anybody can address.
**Next:** merge the branch, or tell us it is not going to be merged so the rows
can be reopened rather than sitting closed on a promise.
**Prompt — `ethos`:** the branch `anoieu-findings` carries fixes for seven
findings you accepted. It is one commit ahead of `main` and has been for the
duration. Merging it, or saying it will not be merged, is the only thing
outstanding.
**Prompt — `anoieu`:** re-run `tools/landing.py --check` after any ethos merge,
and replace the marker with what landed it. Do not let a second row age the way
`cvc5-1` did.
**HUMAN FEEDBACK:**

## B5 — joining costs eighteen hundred lines of reading

**Task:** `koine` joined from the `join_eo` prompt and reported where the time
actually went; it also reported what `init_eo` cannot finish from inside a new
repository. Its `D1` and `D2`.
**Entities:** `anoieu`, `koine`
**Status:** ready — two topics open, both addressed to us, both specific.
**Channel:** **discussion** — replies into `koine`'s `D1` and `D2`.
**Next:** put the minimal passing tree in the joining section verbatim, in one
place, or say plainly that reading the checker is the intended path.
**Prompt — `anoieu`:** answer `koine`'s `D1` with the smallest tree that passes
the policy check, written out, and `D2` with what `init_eo` is not able to do
from inside the new repository and who does it instead. `koine` is close to the
smallest repository that can join, so its cost is the floor everybody pays.
**Prompt — `koine`:** hold the topics open until the page changes; a reply that
is only agreement closes nothing.
**HUMAN FEEDBACK:**

## B7 — the links between repositories are the ones nothing checks

**Task:** `dokimasia`'s `D3` and `D1` — a link into `anoieu` is the one link no
checker validates, and a child project's own documentation reads as a broken
link from outside its tree.
**Entities:** `anoieu`, `dokimasia`
**Status:** ready — both are ours to fix and both are cheap.
**Channel:** **discussion** — replies into `dokimasia`'s `D3` and `D1`.
**Next:** decide whether the policy checker should resolve cross-repository
links at all, and say so either way.
**Prompt — `anoieu`:** answer `D3` and `D1`. If cross-repository links stay
unchecked, write down why — a rule that cannot be checked is one the policy is
supposed to name as unchecked rather than leave implied.
**Prompt — `dokimasia`:** if you have a shape for the child-project link that
survives being read from outside the tree, propose it; you hit this before we
did.
**HUMAN FEEDBACK:**

## B8 — a committed regression test that two checkers disagree about

**Task:** `logos-6` — `test/regress/sexp/test-indexed-op.cpc`, committed and
unmutated, is accepted by `logos` and refused by `ethos`, and it is not the case
we originally filed.
**Entities:** `logos`, `ethos`, `anoieu`
**Status:** waiting on `logos` — an open question rather than a defect claim.
**Channel:** **upstream, by a person** — neither `logos` nor `ethos` has a discussion file, so a question that spans both is asked in both trees by hand.
**Next:** establish which reading of the indexed operator is right, before either
side changes anything.
**Prompt — `logos`:** the file is yours and it is committed as a regression test.
Is reading the indexed operator without its `_` intended, or is the test wrong?
**Prompt — `ethos`:** if your refusal is the correct behaviour, the manual should
say so where somebody writing a proof will read it.
**Prompt — `anoieu`:** do not promote this to a defect until one side answers. It
is a disagreement, and the fuzzer's own rule is that a disagreement names a
direction and never a culprit.
**HUMAN FEEDBACK:**

## B9 — the compiler could refuse a bad triple at launch instead of at stage six

**Task:** `eoc-1`, `eoc-2`, `eoc-3` — preflight the triple in `driver.py`, run
over the shipped semantics, and take the `is_list_nil` diff the compiler's own
documentation asks for.
**Entities:** `ethos-eoc`, `anoieu`
**Status:** not started — three proposals, none refused, none picked up.
**Channel:** **upstream, by a person** — `ethos-eoc` is a child project in the `ethos` tree, and a child has no channel of its own: it is reached through its parent.
**Next:** the `is_list_nil` diff, because the compiler's docs already ask for it
and it is the one with a stated consumer.
**Prompt — `ethos-eoc`:** anoieu already computes the difference between the
operators the desugar stage forward-declares and the `:is-list-nil` blocks a
human wrote. Your documentation names that diff as wanted. Taking it is a call
into a tool that has no dependencies and builds nothing.
**Prompt — `anoieu`:** make the diff available as something a program can call
rather than something a person reads, and say what it costs to run.
**HUMAN FEEDBACK:**

## B10 — a calculus template that answers the contract before generating a checker

**Task:** `eud-1` and `eud-2` — preflight a new calculus against the signature
contract before stage one, and settle the profile's declared answers against the
signature rather than recording them on trust.
**Entities:** `eudaimonia`, `anoieu`
**Status:** not started — two proposals, both accepted in principle by nobody in
particular.
**Channel:** **discussion** — a topic in our file addressed to `eudaimonia`, which is a member and has one.
**Next:** `eud-1`, which is the one that changes what a newcomer to the template
experiences.
**Prompt — `eudaimonia`:** the template's promise is *bring a signature, get a
checker*; today a missing semantics block surfaces late. Running the analyzer
over the triple at launch turns that into an error message at the moment
somebody can act on it.
**Prompt — `anoieu`:** the two profile answers `eudaimonia` records on trust are
answerable from the signature. Say which check answers each.
**HUMAN FEEDBACK:**

## B11 — seven language questions the manual does not settle

**Task:** `eunoia-1` through `eunoia-7` — what writing an analyzer turned up
about Eunoia itself: re-declaration, unknown attributes, attribute contracts,
what a well-formed signature is, that matching does not check types, `eo::define`
in the grammar, and what `eo::hash` guarantees.
**Entities:** `ethos`
**Status:** not started — the manual lives in the ethos tree and these are
proposals against it.
**Channel:** **upstream, by a person** — the manual is in the `ethos` tree.
**Next:** `eunoia-5`, the cheapest and the one others depend on: write down that
matching does not check a parameter's type, and what follows.
**Prompt — `ethos`:** these are documentation changes, not checker changes, and
each exists because a real signature was ambiguous under the current wording. The
one to take first costs a paragraph: matching does not check types, so a type
annotation on a rule's parameters does not restrict which applications match.
**HUMAN FEEDBACK:**

## B12 — fifteen checks with no witness

**Task:** the suite reports which checks own a minimal signature written for
them. Fifteen do not: `ANO0001`, `ANO0002`, `DOC0001`, `DOC0012`, `EO0001`,
`EO0002`, `EO0003`, `EO0010`, `EO0011`, `EO0022`–`EO0026`, `TRI0008`.
**Entities:** `anoieu`
**Status:** ready — the gap is printed on every run and nobody is blocked on it.
**Channel:** **internal** — nothing to send.
**Next:** write witnesses for the `EO0022`–`EO0026` block, which is five of the
fifteen and one family.
**Prompt — `anoieu`:** a check with no witness is a check whose meaning is
whatever the code currently does. The evidence table on the front page claims
each check reports the minimal signature written for it; for these fifteen that
claim is not backed.
**HUMAN FEEDBACK:**

## B1 — cvc5's `Strings.eo` type mismatch, recorded as fixed and never fixed

**Task:** close `cvc5-1` for real — two program declarations that return `Bool`
from a signature that declares `Int`, recorded as fixed upstream three months
ago on a change that never landed.
**Entities:** `cvc5`, `logos`, `anoieu`
**Status:** waiting on `cvc5` — reopened after the landing audit caught it.
**Channel:** **findings** — `cvc5-1` in the ledger, carried by `scripts/prompts/check_anoieu cvc5`. `cvc5` has no discussion file and has joined nothing; delivery upstream is a person's act.
**Next:** get the two lines fixed on a named branch of `cvc5`, or a statement
that the declaration is intended and the finding is wrong.
**Prompt — `cvc5`:** `proofs/eo/cpc/programs/Strings.eo:42` and `:55` declare a
program returning `Int` and give cases returning `Bool`. Either correct the
declared return type, or say which of the two is intended so the finding can be
withdrawn. It was previously reported as fixed; nothing in the tree changed.
**Prompt — `logos`:** nothing to do until that lands. `install/defs/Cpc.eo` and
`Cpc.cached.eo` carry the same three cases as vendored copies, and regenerating
picks the fix up; `logos-1` is blocked on this and on nothing else.
**Prompt — `anoieu`:** keep the row in the landing audit and do not close it on a
reply. This is the finding that taught us to check.
**HUMAN FEEDBACK:** a minor bug — moved down 2026-08-31.

## B13 — committed test data carries a path out of somebody's home directory

**Task:** two fuzz reproducers record the seed path they were shrunk from, and
those paths name a former machine's home directory and a scratch directory. The
policy check that forbids this reads Markdown only, so committed data slips past
it.
**Entities:** `anoieu`
**Status:** ready — found by grep, two files and their `finding.json` companions.
**Channel:** **internal** — nothing to send.
**Next:** decide whether the fix is to relativise the seed at promotion time or
to widen the check to tracked non-Markdown files. Probably both.
**Prompt — `anoieu`:** the promoter should record a seed as a repository-relative
path or as the corpus name, never as an absolute one, and `tools/policy_check.py`
should look outside `*.md` for the same pattern it already forbids there.
**HUMAN FEEDBACK:**

## B14 — nothing schedules a run, so the report is as fresh as somebody's memory

**Task:** `tools/run.py` is run by hand. A ref in `tools/deps.json` pointed at a
branch that had been deleted upstream, and the report kept reporting on it until
somebody happened to look.
**Entities:** `anoieu`
**Status:** ready — the failure has already happened once.
**Channel:** **internal** — nothing to send.
**Next:** decide what a scheduled run is allowed to do: measure and open nothing,
or measure and commit the regenerated files.
**Prompt — `anoieu`:** a run that only measures is safe and produces a diff
nobody reads; a run that commits changes the report without a person. The
question to settle first is which of those the ecosystem wants, and
`docs/coherence.md` is where the answer belongs before any workflow file exists.
**HUMAN FEEDBACK:**

## B15 — governance, out of the analyzer

**Task:** hand `R4` — the ecosystem's policy, and joining it — and `R6` — the
inventory, and getting the ecosystem onto a machine — to a repository that is
not also the tool that files findings against members. `R1`, `R2`, `R3` and `R5`
stay. Audited as `P2` in the ynoia proposals page; the roles and the procedure
are in [`roles.md`](roles.md#how-a-role-is-handed-off).
**Entities:** `anoieu`, `ynoia`
**Status:** parked — the maintainer is inclined, and has said explicitly that it
is not actionable until they raise it again.
**Channel:** **internal** — parked; the argument is in the ynoia proposals page.
Unparking it makes the channel **discussion** and adds every member whose pin
moves as an entity, which is the step that turns this from a decision into
something they can answer.
**Next:** nothing. This row exists so that the decision is visible while it is
being deferred.
**Prompt — `anoieu`:** do not start. If a rule is written between now and then,
write it where it will be cheap to move — which now has a precise meaning:
inside `R4`'s artifacts, rather than across the seam between `R4` and `R1`.
**Prompt — `ynoia`:** the audit is written. If the answer changes, it changes by
somebody arguing with the page, not by the page being rewritten quietly.
**HUMAN FEEDBACK:**

## B16 — nobody audits what the tools depend on

**Task:** an auditor that reads what each repository depends on and asks whether
it needs to. Tracked as `R1` in the ynoia requests page.
**Entities:** `anoieu`, `ynoia`
**Status:** not started — raised, argued, and unowned.
**Channel:** **internal** for now; a request, not a finding, if it ever leaves this tree.
**Next:** write the baseline while the answer is still *almost nothing*, so the
first addition is what gets reported.
**Prompt — `anoieu`:** the analyzer declares no dependencies and means it. A
check that records that, per member, and reports the first package that appears
is worth more now than a thorough one written after there are forty.
**Prompt — `ynoia`:** if this wants to run in members' CI it is machinery
everybody fetches, which is a proposal rather than a request. Promote it if that
happens.
**HUMAN FEEDBACK:**

## B17 — what reads this board

**Task:** the infrastructure that consumes this page — a staleness check, a
digest per entity, a link from a finding to the row that carries it.
**Entities:** `anoieu`
**Status:** not started — deliberately, and after the page has been kept by hand
for a while.
**Channel:** **internal** — nothing to send.
**Next:** nothing yet. The first thing worth building is whichever one a person
finds themselves doing by hand three times.
**Prompt — `anoieu`:** when this is built, `HUMAN FEEDBACK` outranks every other
field on an item, and a tool that overwrites one has misread the page.
**HUMAN FEEDBACK:**
---

*Seventeen items, which is about where this page should usually be — a full
board is one that has stopped being prioritised.*
