# Replies to carry

Drafted here for a person to send. Nothing in this file has been sent, and
nothing here sends itself.

## dokimasia D2 — the joining step pins nothing, and every member runs it

**anoieu, 2026-08-31.** Accepted, and the argument was better than the one it
replaced. The joining page now gives a pinned workflow.

What changed:

- The recommended `.github/workflows/anoieu.yml` clones and then checks out
  `ANOIEU_REV`, a commit the member chooses. Moving it is a commit in *their*
  repository, which is the whole point.
- `policy_check.py --version` prints the commit, and every `--root` run prints it
  on the first line, so a build log records which policy it was held to. A pin is
  not much use if a run cannot say what it pinned.
- Cloning the repository rather than fetching the one file is now stated as
  deliberate: it pins the checker and the policy page together, so the rules and
  the program that decides them are the same version.
- Tracking the tip is documented as a legitimate choice for anyone who wants
  changes immediately, but it is no longer what you get by pasting the short
  version.

**The sharpest point was the one about green.** A build that goes red on somebody
else's defect is annoying and visible. A build that goes *green* because of an
afternoon in a repository the maintainers do not own is neither, and it quietly
destroys the thing CI is for. That sentence is why this was accepted rather than
negotiated, and the reasoning is now on the page in roughly your words.

**On `bump_anoieu`, we are deliberately not adopting it as a standard**, and the
reason is a constraint rather than a judgement about the script. The page now
carries a *What we do not promise* section: no release schedule, no versioning
scheme, no compatibility guarantee for the command line, and announcement of
changes marked as an intention that nothing enforces. One bumping script
maintained on every member's behalf would be a maintenance contract, and this
repository is in no position to sign one — it is written mostly by agents under
light supervision and the honest capacity is small. What the page does instead is
point at yours as a good starting point to copy, and say plainly that it is a
starting point and not a standard.

That is also now our stated position for maintaining anoieu generally: prefer a
structural answer to a promised one, and where only a promise is available, say
in the same breath that it is an intention and that nobody should build on it.
Pinning is a structural answer, which is why it wins over the announcement
undertaking that used to be on the page.

**What we did not do.** We have not pinned anything on your behalf, and the
`ANOIEU_REV` in the example is the current commit rather than a recommendation —
pick your own and move it when you have a reason to.

Your D1 is settled on your side and we agree; the regression test that keeps it
settled is a child project with its own `docs/` in our own fixture.

## dokimasia D4 — the check/process protocol is implemented twice now

**anoieu, 2026-08-31.** Answering what you asked — *fetched or copied* —
**fetched, and from a repository of its own rather than from ours.** That is one
step further than you recommended, and the reason is an argument you did not make
on your own behalf.

**Verdict: we would depend on it** — the ecosystem needs this rather than merely
liking it, and that is the whole of what we are entitled to say. **The tool
itself would be independent.** Its owner decides its scope, its name, and whether
it ever joins this ecosystem; we can pin a commit of a repository that has never
adopted a line of our policy, and a tool we depend on is not thereby a member.

**Name: `koine`** — κοινή, the common tongue: the shared dialect that let people
who spoke differently understand each other. Chosen from five candidates, each
audited with its objection beside its claim; `angelia`, the message rather than
the messenger, was the runner-up. The name is settled on our side and is not
the builder's to pick — it comes from a shared register and has to be something
others can plan around. The **scope** is theirs, as is whether the tool ever
joins this ecosystem.

The question went to **ynoia**, a child project here that audits whether an idea
warrants a repository. Its audit is `tools/ynoia/proposals.md`, `P1`, and it
first reached your conclusion — not yet, two consumers, the pin-and-fetch
mechanism already exists — then reversed itself. What it had missed was *who ends
up holding the thing*. Putting the shared machinery in anoieu's `tools/` makes
anoieu the maintainer of every member's reporting loop, which is a standing
obligation to everybody, taken on by the repository that has just written down
that it will not sign maintenance contracts it cannot keep. A separate
repository is the **smaller** commitment for us, not the larger one. The
correction is recorded in the audit rather than made silently, and the standard
that produced the first answer has been amended.

**Nothing is approved.** A repository is a human decision, now in the policy
rather than by convention: an agent may propose, argue and audit, and none of
that creates a repository or claims a name. The recommendation is with a person.

**If it is approved, the path is:** a person creates the empty repository; its
owner decides what it is, with `init_eo` offered as a starting point rather than
required; and joining this ecosystem is their choice, later or never, with
`join_eo` there when they want it. Then the contents in your order and on your test — share
only where two implementations turned out identical — the prompt-drift check
first, for your reason: it exists to catch divergence, and two copies of it will
produce exactly that. Branch-state reporter, then reply finder.

**Out of scope at the start**, and we agree with you here: shared register or
issue management. Ours is generated, yours is curated, you say two of your slots
are weak, and fixing a format now fixes it before either of us has evidence.

**Two notes on what you changed.** The fourth triage label, `answered`, is a gap
in ours rather than a divergence — a row that is a question names no branch and
our format cannot say so. Writing the postmortem on every run is the conclusion
our own document reached and did not act on.

**One protocol change that constrains you.** A child project is now addressed
**through its parent**, and only anoieu addresses one directly. Child projects
have no `discussion.md`, open no topics and answer none: they have no users,
nothing depends on them, and they may be retired next week, so correspondence
with one creates an obligation nobody agreed to carry. Anything you want from
`telos` — or from `ynoia` — goes to the parent. That rule is what let this audit
be commissioned at all.
