# The laws

**The rules for updating [`history.md`](history.md), and nothing else.** A
narrow document on purpose: it governs one file, and a law about anything else
does not belong here.

**Held by the president, and that is the flaw in it.** The president writes the
record *and* the rules the record is kept under, which is the arrangement this
page most wants to be rid of. **A tool should maintain these laws eventually,
and it is not this one.** Until then every rule below should be read as one the
bound party wrote for itself.

## Who holds what, and what is missing

| what | who holds it |
| --- | --- |
| **the office** | the **president** — a repository, holding it for one stretch, which keeps and writes [`history.md`](history.md) |
| **the law** | **this page**, which the president is bound by |
| **keeping the law** | **nobody yet.** The tool that should hold this page does not exist, so the bound party holds it |
| **independent audit** | **epikrisis**, which analyses what the repositories actually did, on evidence a reader can re-derive |
| **deciding compliance** | **the checks** — CI and the policy checker, mechanically, and they settle nothing about intent |

**Where this is weaker than it looks.**

- **Nobody is chosen by anybody but the maintainer.** The president is appointed
  and serves until the maintainer says otherwise. There is no term, no
  procedure, and no way to remove one.
- **The separation above does not exist yet.** It is written as though it does.
  Today one party holds the office, writes the law, and keeps the record, and
  the only real check is that **the maintainer reviews and commits every
  change** — which is oversight, not independence.
- **Nothing decides intent.** The checks decide whether a rule was followed
  literally. Nothing here decides whether a president acted within the spirit of
  these laws, and no mechanism is proposed for it.
- **And none of this carries a claim about ownership.** The presidency is an
  office within this ecosystem's own work. It confers nothing over anybody's
  repository, including the ones the ecosystem exists to serve.

## The laws

**1. Only the president may modify `history.md`.** Not a member, not a child
project, not somebody working in the president's tree who is not acting for it.

**2. A president may only write the stretch that describes it.** Earlier entries
are read-only.

**3. The file travels with the office.** When the presidency moves, the file
moves, unchanged. **This is what enforces law 2** — after the move your stretch
is in somebody else's repository and you cannot reach it. The laws are kept
short because most of the work is done by where the file lives.

**4. The past is never revised.** A mistake in a closed stretch is corrected by
the *current* president appending a correction to the *current* entry, naming
what was wrong. **The wrong statement stays**, for the same reason this
ecosystem never rewrites its git history: the record of the error is the part
worth keeping.

**5. A stretch's heading is its purpose, in at most three words.** Not a summary
of what happened. A heading written after the fact has lost the thing worth
recording, and one that cannot be said in three words describes a stretch nobody
has understood yet.

**6. An entry opens with how long the stretch lasted in real human time, and
with the change in membership in the order it happened.** Those two before
anything else.

**7. The president does not analyse GitHub.** epikrisis does, as a service. A
president quoting its own count of its own commits is the party being described
choosing the numbers that describe it.

**8. Every figure must be re-derivable by somebody else** from the repository
and the public run history. A number that only the president can produce does
not go on the page.

**9. The summary is kept current while the stretch runs.** Not written at the
end from memory. **A summary composed afterwards is a reconstruction**, and a
reconstruction by the party being described is the weakest document this
ecosystem could produce.

**10. Publishing the working summary is the president's first responsibility**,
before anything else it is asked to do.

## The template a closing president fills in

**A stretch is closed by its own president, in this template, before the file
travels.** After that the office has moved and the entry cannot be touched, so
**closing the entry is the last act of a presidency, not the first act of the
next one.**

**The standard it is written to: explain the stretch as clearly as possible to
somebody who was not there.** Not to record everything, and not to justify
anything. A closed entry that a stranger cannot follow has failed whatever else
it contains.

**Seven fields, in this order, all of them present.** *Nothing to report* is an
answer and is written; an omitted field is not.

| field | what it holds |
| --- | --- |
| **Purpose** | what the stretch was for, in a sentence. The heading is its three-word form |
| **Span** | how long it lasted in real human time, first date to last |
| **Membership** | what changed and when, in the order it happened |
| **What is now true** | what the stretch established that was not true before it. The part somebody can build on |
| **What went wrong** | plainly, with what it cost. **A stretch with nothing in this field was not examined** |
| **What is handed on** | unfinished work the next president inherits, and anything it must not assume |
| **Evidence** | where the figures came from, and how a reader re-derives them |

**Concise is a requirement and not a preference.** A president writing at
length about its own stretch is producing a defence, and the seven fields exist
partly to make that hard. **If a field needs more than a short paragraph, the
thing it describes belongs in a document of its own and this entry links to
it.**

## Amending these laws

**By the maintainer, and by nobody else, until a tool holds this page.** A
president proposing an amendment writes the proposal and does not apply it.
**A law the bound party can change is not a law**, and the only reason the ones
above are worth anything today is that they were published before the stretch
they will be used to judge.
