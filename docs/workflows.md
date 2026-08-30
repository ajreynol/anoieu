# Workflows

The tool is one command. Everything that makes it worth having is people: who
runs it, who decides a finding is real, who carries it to whoever can fix it,
and what comes back. This page is the arrangement for that, and the two prompts
that make the carrying repeatable.

It is written for people who know the calculus they are looking at. Nothing here
is a substitute for that.

## Who runs what

| the workflow | who | what it can change | what actually holds them to it |
| --- | --- | --- | --- |
| **check your own signatures** | anybody | nothing — it reads what you point it at, writes nothing, and needs no network | nothing, and nothing should |
| **verify a report** | anybody | nothing | `tools/run.py --pinned --check` restores recorded commits, so the answer does not depend on who asks |
| **regenerate the report** | a maintainer here | `docs/versions.md`, `corpus.md`, `open-findings.md`, `tools/deps.lock` | the refresh job never runs on a pull request and skips forks; running it by hand needs write access |
| **close a row** | a person, assisted | moves a row to *Closed*, writes `upstream.md` | the generator cannot delete a row, so a closure is always somebody's decision |
| **carry a finding to the project that owns it** | a person who can defend it | that project | deliberately nothing but judgement — see below |
| **turn anoieu on in another repository** | that project's maintainers | their build | their pin, their baseline, their severity policy |

Two of those are worth being precise about, because it is easy to claim more
control than exists.

**We do not control who runs the tool.** It is public, it is pure Python, and it
reads whatever you hand it. Someone can run it over cvc5 tomorrow and publish
whatever they like. What this repository controls is narrower and is the thing
worth controlling: **what is published here as a report** — measured from
commits we record, checked against a baseline we keep, and closed by a review
somebody signs. That is what *What we do not publish* in the top-level README is
about, and it binds us rather than anyone else.

**We do not control what happens to a finding once it is sent.** Sending it is
the last step we take.

## What is deliberately not automated

A finding is a claim about somebody else's code, and sending one spends their
attention, not ours. So: **nothing in this repository opens an issue, files a
pull request, comments on a thread, or writes to another project.** The most any
workflow below asks for is one command or one paste, decided by a person who has
read the thing.

This is not caution for its own sake. Our own log records a finding we reported
and were argued out of — the analysis was wrong, and a person had to explain why
([`upstream.md`](upstream.md), *cvc5-4: what we got wrong*). Automation would
have filed that faster, to more people, with more confidence. A pipeline that can
file a hundred findings unattended is a pipeline whose hundredth finding nobody
reads, including the ninety-nine that were right.

There is also a plainer reason. A finding delivered by a person who can answer
the follow-up question gets read. One delivered by a bot gets a bot's welcome.

## Two prompts

The recommended workflow, for an expert, is two pasted prompts and one line of
reply between them. Both are **fixed text**: the only thing that changes between
uses is an id. They are written for whatever assistant you already work with, in
whatever way you already run it — nothing below assumes one.

They are a pair. The first asks for a reply in a particular shape; the second
knows how to read it.

### 1. Take a finding to the project that owns it

Paste this to an assistant working in a checkout of the project the finding is
about — cvc5, ethos, logos, or whoever else — with `ID` replaced by the row's id.

```text
anoieu is a static analyzer for Eunoia signatures and semantic configuration.
It has reported a finding against this project. The report is at

  https://github.com/ajreynol/anoieu/blob/main/docs/open-findings.md

Find the row whose id is ID. It names a file, a line, and a check; that check
is described under its code in docs/checks.md in the same repository.

Working in this project, and only on what the row names:

1. Decide whether the finding is real by reading the code, not by trusting the
   row. Some of what anoieu reports is wrong.
2. If it is real, make the smallest change that fixes it, and say in one
   sentence what a reader of the calculus would now see differently.
3. If it is not real, say why -- concretely enough that the check could be
   narrowed so it stops reporting this.
4. If you cannot tell, say so. That is a useful answer, and the honest one for
   a signature whose intent you do not already know.

Do not fix other findings you notice on the way; each is reported and closed
separately. Do not summarize the analyzer's other results anywhere: a check
that reports nothing is not evidence that anything is right.

Then reply -- whichever of the four it was -- with a line of the form

  anoieu ID: fixed | declined | wrong -- <one sentence>

wherever the work is being discussed, and send that link to the anoieu
maintainers or open an issue at https://github.com/ajreynol/anoieu/issues.
anoieu does not watch this repository: a finding stays open until somebody
says otherwise.
```

### 2. Read a response back into anoieu

Paste this to an assistant working in a checkout of **this** repository, with the
response, or a link to it, in place of `RESPONSE`.

```text
A project we reported a finding to has responded. The response is:

  RESPONSE

Working in the anoieu repository:

1. Find the row in docs/open-findings.md by its id; if the response does not
   name one, find it by file and line.
2. Check the claim yourself, against the commit the report was measured at --
   `python3 tools/run.py --pinned` restores it. Do this even when the response
   agrees with us, and especially then.
3. Move the row to the Closed table with a verdict, and write what happened in
   docs/upstream.md. Move it; do not delete it. A deleted row is reported again
   on the next run, and the Closed table is what makes a verdict stick.
4. If the response says the analysis was wrong, the check is what needs
   changing, not the row: narrow it, add a witness under tests/witnesses/ that
   would have prevented the report, and record in docs/findings.md what the
   check had wrongly assumed. This case matters more than the other two.

Do not close a row because the finding is no longer reported -- it may only
have moved. Do not add rows by hand; that is the generator's job.
```

## The line that goes between them

```text
anoieu <id>: fixed | declined | wrong -- <one sentence>
```

One line, so it can be found later in a thread that has moved on. Three verdicts,
and the sentence matters more than the word:

- **fixed** — the change has landed or is in review. The row closes, and the
  interesting part is what a reader sees differently now.
- **declined** — real, and the project is choosing to live with it. The row
  closes with that verdict. A reason recorded here is worth more than the fix
  would have been, because it is a fact about the calculus that was not written
  down anywhere.
- **wrong** — the analysis is mistaken. The most valuable of the three: it closes
  a row here *and* opens work here, because a check that was wrong once will be
  wrong again for somebody with less patience.

Notice what the protocol does not have: a way to report that a file is clean. That
is deliberate, and the top-level README says why.
