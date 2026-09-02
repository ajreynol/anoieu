# The instructions

**The short page.** What you do, in your own words, at the end of a long day.

Its sibling is [`interface.md`](interface.md), which says the same things to an
agent — at length, with every edge closed. You do not need that page.

Written for **the human**. The word is plain because the distinction that
matters here is not what sort of person you are — it is whether the party being
addressed is a person at all.

## The list

| | what you do |
| --- | --- |
| [`INST-1`](#inst-1--your-working-window) | set your working hours, once, and let us hold you to them |
| [`INST-2`](#inst-2--ask-who-you-are-talking-to) | type *identify* whenever you want to know which tool the agent thinks it is working for |

Ids stay put. A withdrawn one stays listed, so nobody reuses the number.

---

## `INST-1` — your working window

**Write down the hours you mean to work.** Up to ten a day, and you can name
breaks inside them.

**Do it in daylight.** The urge to keep going turns up later than the judgement
about whether to.

Outside your hours, four things:

- we go to `sleep`, and any tool can put us there;
- once a session, you get told to take a break;
- **you still get your answer** — nothing is withheld or slowed down;
- asking to come back early is refused rather than argued about.

Next time you turn up inside your hours, you get a greeting, a question about
whether you want to change them, and a note on where things stand. **That
question is asked then and at no other time.**

Coming back also starts you at the bottom — whatever was in progress, you climb
again from `brainstorm`. Worth knowing when you pick the hours.

**Doing research? Say so, and it stays quiet for the session.** It is yours to
say; no tool decides that for you.

### Setting it

```text
python3 tools/martyria/sleep.py
```

That prints your window and where you stand in it. The schedule is the small
file beside it — a start, an end, any breaks, and optionally your timezone.
`epoch sleep` and `epoch wake` say the same thing to the build system.

**Two things it cannot do.** It cannot stop you. And it does not know how much
you have worked — only what time it is.

---

## `INST-2` — every answer says who it is from

**Every response you get opens with one line**: the tool the agent believes it
is working for, and what that tool is for.

    <tool> — <what it is for>, powered by <which AI, by name>.

**It names the AI, specifically** — which model and which version, not "an
assistant". You are entitled to know what is answering you: these differ in what
they are good at and in how they fail, and you cannot weigh an answer without
knowing that. *The documents here never name one, deliberately, so that anybody's
agent can do this work; the spoken line always does.*

**You do not have to ask for it, and it should never stop.** If it stops, the
protocol has been dropped, which is worth more of your attention than whatever
was in the answer.

**Ask for the long version any time.** You get the same line plus which
checkout it is working in and the mission quoted from that tool's own files.

**If it is ever wrong, say so.** The agent is reporting a belief, not proving
anything, and you are the only one in a position to correct it. The repositories
here look alike, and an agent in the wrong one is not visibly confused — it is
confidently helpful in the wrong place.
