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
