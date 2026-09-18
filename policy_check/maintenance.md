# Maintaining the policy checker

Policy implementation and compatibility guidance, moved here on 2026-09-18.

### The policy checker interface

The supported interface is the latest anoieu implementation with a stable
mechanical contract: `scripts/policy_check.py --policy-version 1 --root PATH`.
Requirements, applicability and severity remain stable within that version;
checker bug fixes are allowed. New obligations require a new contract while
version 1 remains supported. The default stays 1. See the
[compatibility contract and shared CI workflow](README.md), including
the migration still needed in kanon's adoption instructions.

`--version` identifies the checker implementation commit, not the contract or
a governance document revision. Every run logs the implementation commit and
contract. Checks are encoded and tested here; they do not fetch or interpret
governance documents at runtime. The shared
[policy](https://github.com/ajreynol/kanon/blob/main/docs/policy.md) and
[vision](https://github.com/ajreynol/kanon/blob/main/docs/vision.md) have a separate
home. Vision is argued, never mechanically checked.

**A membership need not be advertised, and `associate` is the footing for it.**
The usual arrangement pairs a front-page declaration with a tree that backs it
and refuses either alone. A repository with reason not to announce it — not
published yet, one person's working tree, an arrangement it would oversell —
writes `**Footing:** ` and the name `associate` on its own `docs/maintenance.md`
instead, followed by what it holds itself to. That page is where this convention
already puts what a repository declines to advertise, so the claim moves there
rather than being dropped, and the checker skips the two declaration checks **by
name** rather than passing them quietly.

**An associate owes this ecosystem nothing.** The obligation on that page is
self-imposed, so the checks run and what they find is read against the marker
rather than against anything we are due — running them is reading its own claim
back to it. Whose fault a number is is **not decided here**: the shared register
knows each repository's footing and prints an associate's count as `tracked`
rather than `failing`. This checker says which tree it is looking at, words its
own summary the same way, and leaves the exit code alone — a checker that went
green on a marker in the tree it is checking would hand every repository a way
to pass by editing one line.

**One thing is still asked of an associate, and it is not a debt.** The front
page is the only thing a reader arriving at the repository has, since nothing
about the arrangement is advertised anywhere else — so it carries a
`How this repository is maintained` heading with something actually under it.
That is the floor the footing needs in order to mean anything, and it asks for
nothing the shared policy does not: its associate protocol already says that for
a tree adopting none of this, the ask is still that one heading. A tree below it
is reported like any other number found on an associate — as `tracked`, with
nobody at fault.

**Explaining the name is not part of the floor.** It is recommended for every
repository and required of none, and a footing is not a reason to read that
differently: an associate with no name section is told so as a minor finding,
exactly as a member is, and neither is failed for it.

A child project its parent's front page does not name records `unadvertised-child`
in its own README; that claim is about the parent and is checked against it.

**Link kanon at `main`, or not at all.** Kanon holds the governing documents,
so what they say today is what binds this repository: a link into that tree
goes to `main`. Never pin one to a commit — a pinned rule is a superseded copy
of somebody else's live page, and keeping one here would make anoieu an archive
of governance it does not hold. Where kanon has removed a page this record
names, the record names it and does not link it. Pinning anoieu's *own* removed
material is a different thing and is fine: this tree is ours to archive.

Do not relax a check merely to make CI green; what a new one owes is below,
under [adding a check](#adding-a-check-to-the-policy-checker). Keep downstream
compatibility explicit: declarations may link either the current shared policy
or its former anoieu location. Anoieu's owner and script-catalog checks read this page.

## Adding a check to the policy checker

The checker is the one program here that runs on other people's builds, so a
check is not a change to this repository — it is a change to theirs. It lands
permanently, it fires at moments nobody chose, and it is nearly never deleted.
**And it is a change to a published contract**: a new obligation, or an existing
one applied to more repositories, needs a new
[policy version](README.md), never a bug fix. Four conditions before one
goes in.

**It is decidable without an opinion.** Where answering it needs judgement it
belongs in the shared vision, which must never acquire a checker.

**It has been run against a tree this repository did not write.** Every false
positive so far was found by somebody else's repository and none by ours, which is
not luck: this is the one tree shaped like the checker's assumptions. Run a new
check against every checkout on the machine before it lands. A check that has only
ever seen this tree has not been tested.

**Its message names the fix.** A failure somebody has to interpret costs more than
the defect it found, and they are reading it in a red build on a schedule that is
not theirs.

**It stays true without curation.** The expensive kind is the check whose *data*
rots — a list of vendor names, a registry of tools, anything that has to be updated
as the world changes rather than as the tree does. There is one of those already,
`VENDORS`, and it is the check most likely to be wrong a year from now. Prefer a
check whose only input is the repository in front of it.

### Why this is a limit and not a ritual

The failure mode is a set of checks large enough that keeping it honest is the
work. Three things produce it, and each looks like diligence.

**A check that fires wrongly costs more than it can ever save** — somebody else's
afternoon, and the credibility of the whole set, because a maintainer who has been
sent one spurious failure reads the next one differently, including the true ones.

**Every check is a migration**, and *we do not pay it*. A repository that passes
today and fails tomorrow does work it did not ask for at a moment it did not
choose; the contract makes that survivable and does not make it free.

**Checks accumulate and are almost never removed.** So the question at the point of
adding one is not *is this true* but *will I defend this in a year, on somebody
else's repository, when it fails inconveniently*. Anything short of yes belongs in
the minor tier, which is what that tier is for.

**And there is a stopping rule.** A check earns its place by finding something. The
anchor check found three dead links on its first run. A check that has never fired
on anything is either perfect or pointless, and the second is the way to bet.

*This section is kanon's text, offered in their `D10` and taken.*
