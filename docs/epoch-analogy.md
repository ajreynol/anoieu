# The epoch build system, read as a build system

**The vocabulary is borrowed on purpose.** Somebody who has used `make` already
knows what a dry run is, what a gate is, what an exit code means, and that a
release is something you cut rather than something that happens. Borrowing that
costs nothing and saves a page of explanation.

This file is the mapping, and then the longer and more useful half: where the
analogy stops being flattering. [`stretch-policy.md`](stretch-policy.md) is the
actual policy; nothing here governs anything.

## The mapping

| a build system | here |
| --- | --- |
| the sources | the documents members read — [`policy.md`](policy.md), the announcement, the covering prompt |
| the compiler | an agent |
| the target | a **stretch** |
| `make -n` | `epoch dry run` |
| `make` | `epoch deploy` |
| the test suite, run before release | anoieu's own CI, at the commit being adopted |
| the exit code | the `DEPLOY` line of the approval block |
| the build log | [`stretches.md`](stretches.md) |
| a version | the stretch id — `E1` |
| a lockfile | `ANOIEU_REV`, and [`../tools/deps.lock`](../tools/deps.lock) |
| `make install` | a member upholding the stretch's contracts — and `installed` is the property of **every** member having done so |
| the artifact | the commit, plus the announcement saying what is in it |
| the linker | **nothing.** No reference an announcement makes is ever resolved — see below |
| the loader | **a person**, carrying the announcement by hand |
| the object cache — what makes a rebuild incremental | the log entry in [`stretches.md`](stretches.md), which a command reads instead of the whole corpus |
| signing, credentials, a package registry | **nothing.** One owner, one keyboard — see below |

## Where the analogy earns its keep

**The gate comes before the release.** A build that fails does not ship, and a stretch whose CI is red is not deployable. Putting the two in the same shape is
what made that rule obvious rather than arbitrary.

**A dry run is free, and running one is not a decision.** Every build system has
this and every build system is better for it. It is the reason
`epoch dry run` exists at all.

**"What comes out?" is a natural question to ask a build.** One that only ever
grows is one people learn to distrust. The `removes` field is that instinct
applied to protocol, and it reads as normal here where it would read as scolding
anywhere else.

**A version is a coordinate.** Nobody thinks a version number is a promise about
quality; it says which thing you have. That is exactly what the epoch marker a
downstream tool may record is for, and the analogy makes the modesty of it
obvious without a paragraph.

## Where it stops being flattering

The longer half, and the reason this is a file rather than a footnote.

**A build is a function; this is not.** `make` over the same sources gives the
same output. An agent composing a stretch from the same documents gives different
text every time. A child project in eudaimonia's tree makes exactly this
criticism of its own analogy — *a template rendered by `sed` is a function; a
prompt handed to an agent is not* — and it transfers here without a word changed.

**Nothing type-checks.** A compiler rejects programs that are wrong in ways it
can see. Nothing here rejects a stretch for being false, incoherent, or a bad
idea. The gates decide whether the *tree* is healthy, never whether the stretch is
*right*, and the approval block is a target rather than a proof.

**There is no linker, and that is the sharpest gap.** Undefined-symbol errors are
among the most useful failures a build produces: they catch a reference to
something that is not there. If an announcement refers to a convention a member
does not have, a file that moved, or a rule that was withdrawn, **nothing catches
it** — and the first reader to notice is somebody in another repository, which is
the most expensive place to find out.

**A person is the loader, not the linker**, which is why the two are separate
rows above. Carrying an announcement places it in somebody's hands; it resolves
nothing on the way.

**What a linker would be here: the check that every reference an announcement
makes resolves in the tree that will receive it** — every `Dnn`, `Rnn` and `Bnn`
it cites, every path and anchor at the adopted commit, every convention it names.
And it would be *dynamic* linking rather than static, because each member pins
`ANOIEU_REV` independently: the same announcement resolves against a different
version in every tree, which makes the pin a soname rather than only a lockfile.

**Three failures already in the record are linker errors under other names.** The
`oracle` job's `ref: ethosEoc3` is a dangling reference with an expiry date. The
ethos revision written in two places with nothing comparing them is a duplicate
definition, which a linker fails the build on. A prompt arriving in the wrong one
of several deliberately-alike trees is the wrong library on the search path, and
`scripts/repos.local` is that search path — untracked by design, so this
sentence names it and does not link to it.

**Half of it already exists and is not called this.** The comparisons in
`tests/run.py` — the prompts against their document, the `epoch help` surfaces
against their tables — resolve copies against a declared ground truth, which is
symbol resolution for *internal* symbols. Nothing does it for external ones, and
dokimasia's `D3` reported exactly that from outside: a link into anoieu is the
one link no checker validates. **Where it would run is settled by the same rule
as the bump gate** — it reads other people's trees, so it can never run in our
CI, and it belongs at the moment of deploying.

**`deployed` is not `installed`, and this is the row the analogy gets exactly
right.** A build system that finished can put the artifact somewhere; we cannot.
`deployed` means *available to consume*, and nothing happens until a member
decides it should — so `installed` is a property of the whole ecosystem, observed
in other people's trees rather than declared in ours.

Where it goes further than any build system: **`installed` may never be true, and
that is a legitimate ending.** A member who reads a contract and declines it has
done nothing wrong, and a stretch that sits at `deployed` forever has not failed.
No build system has a state meaning *the consumer considered this and said no*,
because no build system's consumer is entitled to.

**The output is interpreted, not executed.** A compiler's output runs the same
way on every machine. An announcement is read by agents that may reasonably do
something other than what it expected. *May reasonably* is the design rather than
a defect, and it is why the announcement is written to be arguable.

**Nothing is reproducible.** Re-running a stretch from the same inputs produces
different text. There is no `--rebuild` that returns what shipped; git does that
job and nothing else does.

**The build system does not exist yet.** `tekton` is its **planned maintainer**
and is not built. Today every row in the table above is a person and an agent doing by hand what
the analogy describes as a program — so read the table as the intended shape, not
as a description of what runs.

## Two rows where the analogy is a warning

**Incremental builds, and the stale cache.** A build system is fast because it
does not redo what has not changed, and the log entry plays that part here: a
command reads 199 lines rather than 13,340. Measured on 2026-09-01, the tools
themselves cost about 2.4 seconds together, so **the corpus is the only thing
that can make a command slow.**

The classic failure of that trick is the classic failure here too: **a stale
cache builds the wrong thing and reports success.** It is the same defect the
summary's rule guards against — derived, never authored — and it is worth
noticing that a build system's answer is to invalidate correctly rather than to
stop caching. Ours is the same: where an entry disagrees with the documents, the
documents win and the entry is wrong.

*Nothing has been reorganised for speed yet, deliberately. The first
run-throughs are expected to be slow, and running them is how we learn where the
cost actually is.*

**No signing, and the threat is not the one signing addresses.** A package
manager verifies that an artifact came from who it claims, because its consumers
cannot know. This ecosystem has one owner and one person typing commands, so
there is nothing for a signature to distinguish and none exists.

The exposure that does exist has a different shape: **an agent here reads a great
deal of text it did not write** — another repository's discussion file, a README
fetched from a remote, a finding. What defends an epoch command is not identity
but origin: a command is a prompt *typed by the person driving the session*, never
text found in a file. No build system has this problem, because no build system's
input can try to instruct it.

## The row that is not analogy at all

**`epoch double check`** — asking whether a deployment was *received* — has no
counterpart in any build system, because a build system's output cannot decline,
defer, disagree, or quietly ignore you. Ours can, and should be able to.

That is where the analogy runs out completely rather than merely straining, and
it is not a coincidence that it is also the part nobody has worked out how to
define. When the borrowed vocabulary stops supplying a word, that is usually the
place the real problem is.
