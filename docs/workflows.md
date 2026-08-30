# Working a finding

Guidelines, not machinery. Nothing in this repository files anything anywhere:
a finding travels because a person carries it, and comes back because a person
sends it. What follows is what we suggest that person do, and one prompt worth
keeping around.

It assumes an expert — somebody who knows the calculus being looked at. Nothing
here is a substitute for that.

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

This is the part that is easy to get wrong, and the reason the prompt below is
worded the way it is.

An assistant working in cvc5 or ethos or logos can read a finding and propose a
change. It cannot settle anything. **The person on that project decides what to
say to us, and what they say describes their triage** — where their reading
landed, often under time pressure, on our word, sometimes without having written
the signature in question.

So the authority on what happened is not the reply. It is **the branch**:
whether the change is merged, what review does to it, and what the commits that
follow it look like. A fix can be accepted and then quietly reverted; a decline
can be reversed by the next person to read the file; and the case we care about
most — our analysis being wrong — usually only becomes clear in review, when
somebody who knows the calculus objects to the fix rather than to the finding.

Which gives the rule for our side: **a reply opens a question here, it does not
close one.** Record the branch against the row, leave the row open, and go back
to the branch later to find out what actually happened. A row closed on a triage
is a row closed on a guess, and the log then reads as more settled than it is.

## The prompt

Fixed text. The only things that change between uses are the id and the branch.
It is written for whatever assistant you already work with, run however you
already run it. Paste it in a checkout of the project the finding is about.

```text
anoieu is a static analyzer for Eunoia signatures and semantic configuration.
It has reported a finding against this project. The report is at

  https://github.com/ajreynol/anoieu/blob/main/docs/open-findings.md

Find the row whose id is ID. It names a file, a line, and a check, and that
check is described under its code in docs/checks.md in the same repository.

Working on branch BRANCH, and only on what the row names:

1. Decide whether the finding is real by reading the code, not by trusting the
   row. Some of what anoieu reports is wrong.
2. If it is real, make the smallest change that fixes it, and say in one
   sentence what a reader of the calculus would now see differently.
3. If it is not real, or if you cannot tell, change nothing and say why. "I
   cannot tell" is the honest answer for a signature whose intent you do not
   already know, and saying it is more useful than a guess.

Do not fix other findings you notice on the way; each is reported separately.
Do not summarize the analyzer's other results anywhere: a check that reports
nothing is not evidence that anything is right.

Then draft a reply for a maintainer of this project to review and send. It is
your triage and not a resolution -- you are proposing a change that has not
been reviewed, and what actually happened will be settled by this branch: by
whether it is merged, and by the commits that follow it. Draft it as

  anoieu ID: triaged as <fixed | not a defect | cannot tell> on branch BRANCH,
  pending review -- <one sentence>

and leave the sending to them.
```

## When a reply comes back

Nothing automatic happens, and nothing should. What we suggest:

- **Check it yourself** before believing it, at the commit the report was
  measured against — `python3 tools/run.py --pinned` restores it. Do this when
  the reply agrees with us as much as when it does not.
- **Leave the row open**, and note the branch in it. The reply is a pointer to
  where the answer will be, not the answer.
- **Go back to the branch later.** Merged and untouched is a closure. Reverted,
  reworked, or never merged is a different finding than the one we filed, and
  worth reading before saying anything else.
- **When the branch shows the analysis was wrong**, that is the valuable case,
  and the check is what needs changing rather than the row: narrow it, add a
  witness under `tests/witnesses/` that would have prevented the report, and
  record in [`findings.md`](findings.md) what the check had wrongly assumed.
- **Write what happened in [`upstream.md`](upstream.md)** either way, and move
  the row to *Closed* only once the branch, rather than the reply, says so.

One thing the reply deliberately cannot say is that a file is clean. The
top-level README explains why we do not accept that as a result, including from
somebody offering it in good faith.
