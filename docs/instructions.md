# The instructions

**The human-facing half of the protocol register.** A protocol says what an
agent does; an instruction says what **you** do. They are siblings and they
come in pairs where a thing has two sides — one page an agent is expected to
follow literally, one page a person is expected to be able to read at the end
of a long day.

Written for **the human**. The word is plain on purpose. This ecosystem is one
in which agents write most of the prose, run most of the checks and are awake at
every hour, so the useful distinction is almost never *which kind of person*
somebody is — it is **whether the party being addressed is a person at all**,
and *human* is the word that carries that and nothing else.

*Some pages say "a person" and mean the same thing. That is fine and nobody
should sweep through changing it: the two words are interchangeable here, and
`human` is simply the one to reach for when the contrast with an agent is the
point.*

*This page briefly used **runner** instead, on the reasoning that it named the
one who runs the tools. It was the wrong word for this repository in
particular: `runner` already means a machine executing a CI job, and half the
documentation here is about CI. A term that makes a reader pause to decide which
sense is meant has already cost more than a more ordinary word would have.*

## What separates an instruction from a protocol

| | a protocol | an instruction |
| --- | --- | --- |
| addressed to | an agent | the human |
| lives in | [`interface.md`](interface.md) and elsewhere | this page |
| numbered | `PROTO-n` | `INST-n` |
| may assume | the tree, the filenames, the ids | **nothing but the terminal** |
| failure mode | ambiguity — the agent does the wrong literal thing | altitude — it is correct and unreadable |

**The last row is the one that costs.** An instruction that cannot be followed
without first knowing which file to open has failed, however accurate it is:
that is the test [`PROTO-1`](interface.md#proto-1--the-response-clarification-protocol)
already applies to answers, applied here to standing advice. Paths may appear
in an instruction; **needing one may not.**

**Ids are permanent, and a withdrawn instruction stays listed** with the reason
and the date, for the same reason the other registers here do it: a number that
silently disappears gets reused, and then two things share it.

## The register

| id | in one line | its protocol |
| --- | --- | --- |
| [`INST-1`](#inst-1--your-working-window) | set the hours you intend to work, in advance, and let the ecosystem hold you to them | [`PROTO-18`](interface.md#proto-18--the-sleep-protocol) |

---

## `INST-1` — your working window

**What you do:** decide the hours you intend to be available, write them down
once, and leave them alone. Ten hours a day is the most the ecosystem will
record; less is better and nothing here will argue with you about it. You may
also declare **breaks** — hours inside the working day that are yours — and
they are treated exactly like the hours outside it.

**When:** now, once, and then only in daylight. **Changing the window is a
daytime decision.** The point of writing it down in advance is that the urge to
keep going arrives later than the judgement about whether to, and the person
awake at one in the morning is not the one who should be ruling on whether one
in the morning is a working hour.

**Why it exists:** it is easier to not start than to stop, and an ecosystem of
tools that are always awake and never tired is an unusually good machine for
making that harder. A schedule you set in advance is the one thing in the
arrangement that is on the other side.

**What happens when the hours end:** the ecosystem drops to `sleep`, a status
below every other one, where nothing is in play. **Any agent may put us there
and none of them needs to ask.** That sounds like a great deal of power and is
not: dropping has always been free here, and this is one step further down the
same staircase.

**What happens when they start again:** the next time you turn up inside your
window, the ecosystem wakes on its own — it says good morning, **asks whether
you want to change your hours**, and tells you what this tool is currently
trying to do. The question about your hours is asked *then* and at no other
time, which is deliberate: it is the one moment you are being asked in daylight,
with the night behind you, rather than at the hour when the answer would be
convenient. **Outside your window, asking to wake is simply refused** — not
argued with, not weighed, just refused, because a rule you can talk an agent out
of at two in the morning is not a rule.

**Waking starts you at the bottom.** Whatever the stretch had reached when the
day ended, you come back at `brainstorm` and climb again. That is the ordinary
price of dropping rather than a penalty, and it is the one practical reason to
pick a window that fits your work instead of one you keep running past.

**What the agent does about it:** outside your window, once in a session, it
tells you to take a break — and then does the work you asked for anyway. It
will not withhold anything, it will not repeat itself, and it will not offer an
opinion about your evening. If the window looks like it was widened tonight, it
says so once. **It cannot stop you and is not trying to**; what it can do is
make moving the line leave a mark.

**If you are doing research, say so and it stays quiet for the session.** The
exemption is yours to claim and not the agent's to infer, because an agent
allowed to decide that tonight's work is the exception would decide that every
night, sincerely, and the rule would be gone inside a week.

### How to set it

The schedule lives with [martyria](../tools/martyria/README.md), the project
that maintains this mechanism, and it is a small file with a start time, an end
time and any breaks. To see where you stand right now:

```text
python3 tools/martyria/sleep.py
```

It prints the window, the time, and — if you are outside it — one sentence.
`epoch sleep` and `epoch wake` are the same thing said to the build system.
**It is never run in CI**, for the same reason the bump gate is not: it says
something different every hour, and a build that depends on the hour fails for
reasons that have nothing to do with the code.
