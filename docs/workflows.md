# A suggested AI workflow for using anoieu

How to work a single finding with an assistant, from the report to whoever can
fix it and back. The arrangement is not specific to anoieu — the conventions it
rests on are set out separately, in [`triage.md`](triage.md), so that another
analyzer that reports findings against somebody else's files can adopt them by
substituting its own. What is anoieu-specific here is confined to the two
prompts — the tool's name, the report's URL, and a handful of paths and
commands — and to the right-hand column of the table on that page.

**Guidelines, not machinery.** Nothing in this repository files anything
anywhere: a finding travels because a person carries it, and comes back because
a person sends it. What follows is what we suggest that person do, and the two
prompts worth keeping around — one for the project that owns the finding, one
for the follow-up here.

It assumes an expert — somebody who knows the file being looked at. Nothing here
is a substitute for that.

## Who runs what

Running the checks needs no permission from anybody: the tool reads what you
point it at, writes nothing, and needs no network. Verifying a published report
is equally open — `tools/run.py --pinned --check` restores the recorded commits,
so the answer does not depend on who is asking.

Two things are ours: **regenerating the report**, which is a maintainer here
moving what it is measured against, and **closing a row**, which is a judgement
somebody signs. The generator cannot delete a row, so it can never be the thing
that closes one.

We do not control who runs the tool — it is public and reads whatever it is
handed. What we control is what is published *here* as a report, which is the
thing the promises in the top-level README are about.

## A reply is somebody's triage, not the status

This is the part that is easy to get wrong, and the reason the prompts below are
worded the way they are.

An assistant working in cvc5 or ethos or logos can read a finding and propose a
change. It cannot settle anything. **The person on that project decides what to
say to us, and what they say describes their triage** — where their reading
landed, often under time pressure, on our word, sometimes without having written
the file in question.

So the authority on what happened is not the reply. It is **the branch**:
whether the change is merged, what review does to it, and what the commits that
follow it look like. A fix can be accepted and then quietly reverted; a decline
can be reversed by the next person to read the file; and the case we care about
most — our analysis being wrong — usually only becomes clear in review, when
somebody who knows what the file was for objects to the fix rather than to the
finding.

Which gives the rule for our side: **a reply opens a question here, it does not
close one.** Record the branch against the row, leave the row open, and go back
to the branch later to find out what actually happened — which is the whole job
of the second prompt. A row closed on a triage is a row closed on a guess, and
the log then reads as more settled than it is.

## Prompt one: in the project that owns the finding

Fixed text. The only things that change between uses are the id and the branch.
It is written for whatever assistant you already work with, run however you
already run it. Paste it in a checkout of the project the finding is about.

It deliberately says nothing about what kind of thing the finding is about. A
row may be about a signature, a semantics set, a configuration, an inconsistency
between two of them, or something anoieu learns to check next year, and a prompt
that named one of those would quietly narrow what the reader looks for.

```text
anoieu is a static analyzer for the Eunoia languages. It has reported a finding
against this project. The report is at

  https://github.com/ajreynol/anoieu/blob/main/docs/open-findings.md

Find the row whose id is ID. It names a file, a line, and a check, and that
check is described under its code in docs/checks.md in the same repository.
Treat the row as a claim about that file and nothing more: it does not tell you
what kind of problem to expect, and you should not assume one.

Working on branch BRANCH, and only on what the row names:

1. Decide whether the finding is real by reading the file, not by trusting the
   row. Some of what anoieu reports is wrong.
2. If it is real, make the smallest change that fixes it, and say in one
   sentence what a reader of that file would see differently as a result.
3. If it is not real, or if you cannot tell, change nothing and say why. "I
   cannot tell" is the honest answer when you do not already know what the file
   was meant to say, and it is more useful than a guess.

Do not fix other findings you notice on the way; each is reported separately.
Do not summarize the analyzer's other results anywhere: a check that reports
nothing is not evidence that anything is right.

Then draft a reply for a maintainer of this project to review and send. It is
your triage and not a resolution -- you are proposing a change that has not
been reviewed, and what actually happened will be settled by this branch: by
whether it is merged, and by the commits that follow it. Draft it as

  ## ID -- <check> -- <path>:<line>

  TRIAGE: triaged as fixed | not a defect | cannot tell, on branch BRANCH,
  pending review. <What you changed, or why you changed nothing.>

  HUMAN RESPONSE:

and leave the sending to them.

Leave HUMAN RESPONSE: empty. It is the maintainer's, and the two labels exist
to keep what you concluded apart from what a person decided. If they ask you to
write it instead, do -- but then quote the field back to them exactly, the text
itself and not a description of it, say plainly that you are writing in their
place and it will be read under their name, and change it as many times as they
ask until they say it says what they mean. Writing that field and summarising
it back is the one thing this shape exists to prevent.
```

## Prompt two: the follow-up, here

The reply from prompt one names a branch. That branch is the thing worth
reading, and reading it is a job in this repository rather than in theirs — so
the second prompt is for an assistant working in a checkout of **anoieu**, and
the only thing that changes between uses is a link.

The link can be to the branch, the pull request, or wherever the triage was
written down. It is a pointer to where the answer will be, not the answer.

What arrives is part assistant and part human — prompt one ends by handing its
draft to a maintainer, who reviews it, edits it and sends it — and telling those
apart is the one thing the prompt below spends words on. The rest of the job is
small on purpose: read the reply, work out what actually
happened, clean up **only the rows it is about**, and say what was done. There
is no write-up file and no second sign-off — the staged diff is the review, and
an agent that has moved three rows and narrowed a check has already shown its
work. What it may change, and the two cases where it should stop and ask, are in
[`triage.md`](triage.md) rather than in the prompt.

```text
A project we reported a finding to has responded:

  LINK

Read it as two things. What follows TRIAGE: is an assistant's reading, made
quickly and on our word. What follows HUMAN RESPONSE: is a maintainer's
decision. Where the two differ the decision is what counts, and a reply
carrying only a triage is a proposal rather than a result.

Working in the anoieu repository:

1. Find the row or rows in docs/open-findings.md that the reply is about.
2. Establish what actually happened: re-check at the version the report was
   measured against with `python3 tools/run.py --pinned`, and follow the branch
   to its end -- merged, reworked, reverted, or still open. That outcome counts,
   not what the triage predicted.
3. Clean up the table as docs/triage.md says, for those rows and no others.
4. If our analysis was wrong, the check is what needs changing rather than the
   row: narrow it, add a witness under tests/witnesses/ that would have caught
   the mistake, and record in docs/findings.md what it had wrongly assumed.
5. Write what happened in docs/upstream.md.

Leave everything staged, and say what you decided and why -- the action you
took, not a summary of what you read. Come back to me only if you disagree with
how the reply classified the resolution, or you cannot tell whether the finding
is resolved; leave the row open and say what you would need to know.
```

### Keeping the two in step

The first prompt's output is the second prompt's input, so they are one contract
seen from two sides. If the reply's shape changes in one it has to change in the
other, and in [`triage.md`](triage.md), which is where the shape is actually
defined — all three or none.

The failure is quiet, which is why it is worth saying: an agent asked to read a
format nobody produces any more will not stop, it will improvise. It will find
something in the trail that looks close enough, act on it, and report having
done so. Nothing errors, and the first sign of trouble is a row closed on a
misreading. Changing one prompt and not the other is the cheapest way to break
this workflow.

Neither prompt gives anybody a way to say that a file is clean — not the project
replying to us, and not the agent recording what came of it. The top-level README
explains why we do not accept that as a result, including from somebody offering
it in good faith.

## Medium term: issues, on our own repository

A table in a file is a poor place to hold a conversation. It has no threads, no
notifications, and no way for somebody who has not cloned the repository to
reply — so today a finding is discussed wherever the person carrying it happens
to be, and the ledger entry is written afterwards from whatever survived. The
intended fix is to give a finding a GitHub issue, and let the reply be a comment
on it.

Three constraints on that, worth writing down before anything is built:

**The issues live here, never on the project the finding is about.** An issue
filed in somebody else's tracker puts our claim in their queue, under our name,
where they have to dispose of it — and a wrong one is expensive for them to get
rid of. On our own tracker the same text is an invitation: they can ignore it,
argue with it, or link it from their own issue if they think it deserves one.
The asymmetry is the point, and it is the same reason nothing here files
anything anywhere today.

**A person posts, always.** The step from a file to a notification in somebody's
inbox is outward-facing and effectively irreversible, and it is not one an agent
should take on its own judgement — nor one it should hold the credential for.
What we would build is a script a maintainer runs over rows they have picked,
which opens an issue here for each and records its number against the row. One
command, deliberately, by the person whose name is on it. Reading the resulting
thread stays an agent's job; writing to it does not.

**Not yet.** Machinery that speaks on someone's behalf has to be right the first
time, and we are not at the point where the report changes often enough to need
it. The conventions above are built to survive the change rather than to be
replaced by it: a row is already the body of an issue, its id is already the key
an issue would be recorded against, and a reply is already shaped like the
comment that would answer one — `TRIAGE:` from an assistant, `HUMAN RESPONSE:`
from a person, in a thread instead of an email. Until then, the file is the
record.
