# Postmortem log

A living log of what handling findings has taught anoieu about **its own
workflow**. One section per **iteration** — one run of the loop, one reply
worked — with the findings that changed how this repository works listed under
it: a check narrowed, the harness fixed, the report reshaped, a prompt
rewritten. Newest first.

**This is not where a finding is written up.** That is
[`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back), which
carries the reasoning, the commits and the evidence at whatever length they
need. An entry here is at most three paragraphs and points there. The two files
answer different questions: *what happened to this finding* is the log in
`reports.md`; *what this finding taught us about working findings* is here.

## The procedure

**Whose job.** The anoieu maintainer processing a reply — step 7 of prompt two in
[`reporting-policy.md`](reporting-policy.md#prompt-two-the-follow-up), which is
what [`scripts/process_anoieu`](../scripts/process_anoieu) runs. Not the project
that owns the finding: they send feedback, we decide what it changed here.

**When.** An entry is earned when processing a bug report **changed how anoieu
works**. A row confirmed and closed on its merits, with nothing here altered,
does not get one. If nothing changed, say so in the session rather than writing
an entry that says nothing happened.

    scripts/process_anoieu <project> [ID]           # the agent decides
    scripts/process_anoieu --postm <project> [ID]   # an entry is required

`--postm` makes it mandatory for that run — for a round you already know is worth
recording, or when you want the reasoning captured whatever the agent concludes.
Without it the agent applies the test above and says which way it went.

**The shape of an entry.** One heading per **iteration of anoieu** — one run of
the loop, one reply worked — not one per bug. A run usually settles several
findings; they are listed under the same heading, each with its own fields.

```text
## <date> — <project>: <what this round was>

<One or two sentences: what was asked, what came back, what moved.>

### <finding id, or a phrase for a group of them>

**Tool:** which project, and ours too when a tool of ours was at fault.
**Summary:** what was reported, in one sentence.
**Resolution:** what was decided, and what changed here.

<What happened — only enough to make the resolution make sense.>

**Learned:** <the general fact, stated so it applies to the next finding rather
than to this one.>
```

Keep only text that makes clear **what happened** and **what the workflow
learned**. Everything else — the commits, the reproduction, the argument — goes
in [`reports.md`](reports.md#the-log-what-was-reported-and-what-came-back) and is
linked from the entry. A finding that was settled on its merits with nothing
changed here does not need its own section; say so in the round's opening
sentences.

## Standing rules this log has produced

Stated in full in
[`reporting-policy.md`](reporting-policy.md#feedback-both-ways); listed here with
the entry that produced each, because a rule with no incident behind it is a
preference.

| rule | from |
| --- | --- |
| the outbound prompt asks for `FEEDBACK TO ANOIEU`, and the reply has a field for what was noticed but not acted on | the whole first round: everything we learned arrived as prose in a reply with nowhere to put it |
| every round leaves the prompts clearer, more actionable and shorter | the first revision grew both and had to be cut back twice |
| a prompt is procedural; technical detail is a link | 2026-08-31, `3e271ee47343e758` — a sentence inlined in the prompt had been untrue for as long as it had existed |
| a person approves every change to a prompt template | standing; a template that rewrote itself from its own experience drifts with nobody agreeing to the direction |
| the guardrails are never traded for brevity | standing: *fix nothing else*, *do not summarise other results*, *touch no issue tracker*, *leave everything staged* |

## Where the workflow stands

Updated each round. This is the part to read if you want to know whether the loop
is paying for itself.

**What is working.** Re-measuring is exact and is one command each way —
`tools/run.py --pinned` for the checks, `anoieu_fuzz verify` for the reproducers
— so *does this still hold* is a question with an answer rather than a judgement.
Moving a row is a two-line edit. The two labels, `TRIAGE:` and `HUMAN RESPONSE:`,
survived contact with a real reply and did the work they exist for. Naming the
escape hatch in advance — *the serious direction may still end with the reference
being stricter than the language requires* — is what let the far end decline a
row confidently instead of hedging.

**What is hard, and it is all judgement.** Closing a row on the strength of a
persuasive paragraph: two of three substantive replies were correct on the merits
and one of them still could not be closed. Deciding scope, when a reply corrects
something belonging to a third project. And a finding that stops reproducing
looking like a fix when it is a bad reproducer.

**Outstanding.** Five suggestions from the far end, none yet built, each a change
to what a finding *is* rather than a tidy-up. In their words, in
`anoieu-dev-response.md` in the logos repository.

| what | why it matters | cost of not doing it |
| --- | --- | --- |
| warn when a closed row's finding is still reported at the pinned commits | a verdict is a claim about the world and nothing rechecks it | three rows sat closed on a fix that never landed |
| put the cross-corpus correspondence in the `notes` column mechanically | the twin is already computed here | sixteen rows and forty minutes of somebody matching text by hand |
| record the argv, checker version and signature revision with each promoted finding | the record is not self-contained enough to replay | the far end had to guess the invocation, and the guess turned out to matter |
| mark a `note` as a reading rather than a measurement | a hypothesis ships beside a measurement, indistinguishable | one confident, wrong note nearly produced a confident, wrong triage |
| keep the raw detail beside the portable one | bucketing erases what the reader needs | `<path>:N.N` hid which line the reference actually refused |

**Prompt size, by round.** The rule is that these come down; the number is how it
is kept honest.

| round | prompt one | prompt two | what was removed to pay for additions |
| --- | ---: | ---: | --- |
| 1 (2026-08-31) | 60 → 54 | 39 → 63 | prompt one lost the inlined explanation of what each code means and how each is confirmed, which moved to the header of [`open-findings.md`](open-findings.md) where it can be maintained. Prompt two grew, and that is the honest number: it gained the postmortem step and its `--postm` alternative, the branch check, the closed-row scope rule, and the caveat on a reproducer that stops reproducing. It is the one number in this table going the wrong way. Next round's candidate for removal is step 4, which is procedure that could be a link |

---

---

## 2026-08-31 — logos: the first full sweep

Twenty open rows were put to logos and answered one at a time; nineteen came
back. Sixteen were one fact about a generated file, restated sixteen times.
Three were substantive: one fixed but not landed, two declined with reasons that
hold. One row we withdrew as our own error, and one verdict of ours — against a
third project — turned out never to have been true. Two of the four sections
below are about tools of ours rather than about logos.

The two clean declines are not written up here: `adc98aa79b4861bb`
(`declare-fun` in a proof file) and `4de9bb965fa0c04b` (an `assume` after the
first `step`) were both confirmed, both declined for reasons that hold, and
neither changed anything in this repository. They are in
[`reports.md`](reports.md#logos--the-parser-and-the-semantics).

### `3e271ee47343e758`

**Tool:** logos, and our own fuzzer.
**Summary:** A `FUZ0001` disagreement — logos accepted a proof ethos refused —
reported against a reproducer we had damaged ourselves.
**Resolution:** logos fixed a real parser bug; we withdrew the row, deleted the
reproducer, and stopped the shrinker editing seeds.

The case was one of logos's own regression tests, `test-indexed-op.cpc`, run as
a seed *as it stands*. logos accepted it, ethos refused it, and it was promoted
under a note blaming the missing `_` in `(( extract 1 0) a)`. logos narrowed a
parser that read any parenthesised head as a curried application, and the case
stopped reproducing — but their agent disbelieved our note and said so. It was
right: ethos had been refusing at **line 3** throughout, on the file's own
unmutated SMT-LIB spelling. Our shrinker had cut the `_` from line 4 and the
bucket held, because a bucket says nothing about *where* a refusal happened.
`shrink` now refuses to touch a seed run as it stands, with a guard in
`tests/fuzz_cases.py`. Detail in
[`reports.md`](reports.md#logos-4-the-indexed-operator-what-we-got-wrong).

**Learned:** we shipped a *hypothesis* — the note — inside the same record as a
*measurement* — the outcomes — with nothing marking which was which, and the
next reader nearly took it as given. And bucketing strips line numbers, which is
right for deciding whether two findings are one and wrong for what a reader is
shown: the stripped `N.N` is exactly what hid which line failed.

### `1d977d28576d3693`, `878038145dca690c`, `6cc91770c5491971`

**Tool:** cvc5.
**Summary:** Three `EO0064` rows closed as *fixed upstream* had never been fixed.
**Resolution:** Reopened, with the register and the log corrected.

Nothing of ours found this. The assistant at the far end, checking whether the
copy it maintains would pick up a fix at the next bump, read what the copy is a
copy *of* and told us our own Closed table was wrong. It was worse than stale:
both programs declare `Int` at the commit the finding was reported against and
at the pinned tip, and they entered `programs/Strings.eo` already declaring
`Int`. The verdict was written from an assessment of the change we *proposed*,
never from the tree afterwards. Detail in
[`reports.md`](reports.md#cvc5-1-what-we-recorded-as-fixed).

**Learned:** the generator adds and never removes, which works — the hole is one
level in. A closed row correctly stays closed, but its *reason* is a claim about
the world that nothing rechecks, and `--pinned` re-derives open rows only. So a
wrong verdict and a live finding can coexist indefinitely with nothing red.
*Fixed upstream* is the one verdict this repository can settle by itself, from
`deps/`, and should never be recorded without doing so.

### Sixteen rows against `install/defs/Cpc.cached.eo`

**Tool:** logos (the file), cvc5 (the content).
**Summary:** Sixteen rows filed against the project that vendored a generated
signature rather than the one that wrote it.
**Resolution:** Already closed here as *not audited*; the prompt and the report's
header were fixed instead.

The rows cost nothing here and a great deal at the far end: it read the file's
header, fetched cvc5 three times, matched premise text line by line, and only
then found that twelve of the sixteen were **already ruled on, against cvc5,
twenty lines further down the same document** — then wrote sixteen
near-identical blocks, correctly, because the prompt said each row gets its own.

**Learned:** the `notes` column is the highest-value field in the report and was
empty on all twenty rows, when *same source line as `c9887e6df81fcdb6` (cvc5,
closed: intentional)* was already computable here. The prompt also asserted the
rows were unrelated; sixteen of twenty shared one cause. It now says rows may
share a cause and to say so. The mechanical cross-reference is still not built.

### `eac7ccd4d5fb0953`

**Tool:** logos.
**Summary:** `TRI0002` — the semantics declares an entry for a symbol CPC does
not declare.
**Resolution:** Confirmed and fixed at the far end; **row left open**, because
nothing landed.

The entry was a target-vocabulary symbol given an input-side entry by mistake,
and they proved it dead rather than merely unused by showing the generated Lean
byte-identical without it. The branch named in the reply was `main` with no
commits of its own, and the deletion was an uncommitted edit in one working
tree.

**Learned:** *"fixed on branch X"* is worth nothing until somebody looks at X,
and the looking takes ten seconds. Prompt two now says to compare the branch to
its base and read what is on it, and that a branch level with main, or a change
left uncommitted, is not a fix. This is the case the workflow's central claim —
the branch is the authority, not the reply — exists for.
