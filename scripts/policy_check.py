#!/usr/bin/env python3
"""Check this repository against the shared repository policy, and say what it cannot check.

Policy is a set of claims about a *tree* — where files go, what the README ends
with, what a child project may import — so a program can decide them without
asking anybody's opinion. That is the whole reason policy is checked here and
the vision is not: see "Policy is checked; vision is argued" in
the vision held with governance. **Nothing here may ever check vision.** Whether
a tool is fruitful yet, whether a claim is oversold, whether a child project has
earned its keep — those are judgements nobody has the authority to settle, and a
green tick against one would manufacture an authority that does not exist.

Each check names the rule or convention it implements, so a failure is traceable
to a sentence somebody wrote. The run also prints every policy rule that has
**no** automated check, because a checker that only lists its own passes reads
as coverage it does not have.

**A membership need not be advertised, and the footing for that is `associate`.**
The usual arrangement pairs a front-page declaration with a tree that backs it,
and refuses either alone. A repository that is held to the policy and has reason
not to announce it — it is not published, it is one person's working tree, it
would oversell what is in it — carries no declaration and records the footing on
its own maintenance page instead, saying there what it holds itself to.

**An associate owes this ecosystem nothing, and the obligation it records is its
own.** So the checks still run, and what they are measured against is the
repository's own marker rather than anything we are owed: running them is
reading its claim back to it. Whether a number found that way is anybody's fault
is not decided here — the shared register decides that, from the footing it
records, and prints an associate's count as *tracked* rather than *failing*.
This run says which tree it is looking at and leaves the reading to it.

`associate_in` reads the marker; the two declaration checks skip by name rather
than passing quietly, because an associate is defined by not carrying the thing
they look for.

    python3 scripts/policy_check.py             # check; exit 1 on any failure
    python3 scripts/policy_check.py --root PATH # check somebody else's checkout
    python3 scripts/policy_check.py --coverage  # what is checked, and what is not
    python3 scripts/policy_check.py --version   # which commit of the checker this is
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: The repository under test. `--root` points it at somebody else's checkout;
#: `REPO_ROOT` stays this one, because a few checks are about anoieu's own files.
ROOT = REPO_ROOT
CHECKER_REPO = "ajreynol/anoieu"
POLICY_REPO = "ajreynol/kanon"
# Accept pre-handoff declarations without making members rewrite their README.
POLICY_REPOS = (POLICY_REPO, CHECKER_REPO)

# Rules with no automated check, and the honest reason. Printed on every run.
UNCHECKED = [
    ("rule 1, a human starts one", "intent; no artifact records who asked"),
    ("rule 6, additive never authoritative", "a claim about tone, not about the tree"),
    ("rule 7, nothing leaves the island by machine", "absence of an action cannot be observed here"),
    ("rule 8, it cites what it inherited", "whether a citation supports its claim is reading"),
    ("rule 9, it ends with a verdict", "'has gone quiet' is a judgement about elapsed time"),
    ("the maintenance note carries no technical detail", "what counts as technical is editorial"),
    ("commands and helpers live in `scripts/`, assistant launchers in `prompts/`",
     "no mechanical test distinguishes a command from an assistant launcher"),
    ("`tests/` holds the evidence, not only the tests", "readability in a minute is not measurable"),
    ("a workflow is defined in prose", "checked elsewhere: `prompts_agree` in tests/run.py"),
    ("a surface that restates a register is compared to it",
     "the comparison lives with the surface: `prompts_agree` in tests/run.py "
     "covers the findings prompts; governance templates belong with governance. "
     "Whether a new surface has a comparison is not decidable from here"),
    ("coding style", "encouraged and never blocking, so nothing here checks it -- by design"),
    ("a topic is never about somebody else's discussion file",
     "what a topic is *about* is semantic; a heuristic here would misfire on legitimate notices"),
    ("do not add a file per assistant", "a convention about what not to create"),
    ("a repository with a result writes it up in `report/`",
     "whether work is worth a paper is a judgement, and the vision may never acquire a checker"),
    ("the soft form of the maintenance note",
     "about a repository held to none of this, so no check here runs against one; "
     "`affiliation_in` reads it for the inventory and never grades anybody"),
    ("a member shares the approach the vision argues for",
     "the judgement half of a footing; vision may never acquire a checker"),
    ("an id is allocated above the highest ever used, including removed topics",
     "the highest ever used is in Git history once a finished topic is removed, "
     "and this reads a tree rather than a history -- CI clones are routinely "
     "shallow. A duplicate *within the file* is caught; a number reused after a "
     "removal is not"),
    ("why an associate does not declare",
     "a repository's own reason for not advertising — not published yet, one "
     "person's working tree, an arrangement it does not want to oversell. The "
     "marker is checked for being readable; the choice behind it is nobody's to "
     "grade, and an associate owes this ecosystem nothing either way"),
]

# Written by a run. `closed-findings.md` is deliberately absent: it is written by
# the review step and *read* by the generator, so it is a hand-maintained file.
GENERATED = ["reports/open-findings.md", "reports/corpus.md", "checks.md"]
#: Extensions read as bytes rather than text; the path check skips them.
#: An absolute path out of somebody's home directory.
HOME_PATH = r"(?<![\w/])(/home/[\w.-]+|/Users/[\w.-]+)/"
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".pyc", ".zip", ".gz"}
INDEX_EXEMPT = {"README.md"}
#: A letter from one president to the next is the other thing in `docs/` that is
#: deliberately unindexed. The laws hold that it is an account and not
#: documentation -- nothing checks it, and it is in no index -- so indexing it
#: would be this checker overruling the page it is written to enforce. Matched
#: by name rather than listed, because the next one is addressed to somebody
#: whose name nobody here knows yet.
INDEX_EXEMPT_RE = r"^letter-to-[\w.-]+\.md$"
COMPETING_ENTRY = ["INTRODUCTION.md", "OVERVIEW.md", "ABOUT.md", "GUIDE.md", "START.md"]

KINDS = {"request", "proposal", "question", "notice", "answer"}
#: The field block, and there is no `Status:` in it. **Presence in the file is
#: the status**: a discussion is live while it is there, and a finished one is
#: removed outright -- replies and all -- once its lasting decision has been
#: written into the document it governs. Git history keeps the conversation, so
#: an archive kept here would be a second copy that nobody maintains.
FIELDS = ["To", "Kind", "Opened", "Settles when"]
#: Carried only to say it is gone. A topic still holding a `Status:` predates
#: the change, and the value it holds is the thing most likely to be wrong --
#: `open` on a topic that ended, or `settled` on one nobody removed.
RETIRED_FIELDS = ("Status",)

# The response gate, clause by clause. Each entry is one clause of the banner
# every discussion.md must carry, and the alternatives a repository may spell it
# with. Wording may vary; a missing clause may not.
BANNER = [
    ("the refusal to act unbidden", ["do not act", "must not act", "never act"]),
    ("the human instruction", ["human"]),
    ("that it be explicit", ["explicit"]),
    ("the disagreement rule", ["disagree"]),
    ("the human override", ["override"]),
]


#: The misaddressing rule, clause by clause -- *A prompt may not be for this
#: repository*. Reported and never fatal while it is new: a guardrail that turns
#: somebody's build red before they have read the reason for it is one they
#: delete. It joins BANNER when every member has adopted or declined it.
PROMPT_GATE = [
    ("that a prompt may have come to the wrong repository",
     ["meant for this repository", "meant for me", "misaddress"]),
    ("that saying so is an acceptable answer",
     ["acceptable answer", "not meant for me"]),
    # Not "does it say stop" -- the response gate above it already says that, so
    # such a clause would be satisfied by text that is not this rule at all. The
    # clause worth carrying is the half that keeps the rule cheap.
    ("that it stops only where the right addressee can be named",
     ["stop only if you can name", "cannot, it is for you",
      "name the repository it was meant for"]),
]


def version() -> str:
    """The commit of *this checker*, so a build log records what it was checked
    against. A member pins a commit; the run should say which one it got."""
    out = subprocess.run(["git", "-C", REPO_ROOT, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() or "unknown"


def tracked(pattern: str) -> list[str]:
    out = subprocess.run(["git", "-C", ROOT, "ls-files", pattern],
                         capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l]


def read(rel: str) -> str:
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def prose(text: str) -> str:
    """The text with fenced code stripped: a sample is not a sentence, and the
    prose conventions below have no business linting somebody's example."""
    return re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)


def sections(text: str) -> list[str]:
    return re.findall(r"^##\s+(.+?)\s*$", text, re.M)


#: Vendors and models. *No document names a specific AI* — this list is the
#: check, so adding a name here is how the rule keeps up with the market.
VENDORS = ["claude", "codex", "chatgpt", "openai", "anthropic", "copilot",
           "gemini", "llama", "mistral", "deepseek", "grok"]


def check_no_vendor() -> list[str]:
    """*No document names a specific AI*, with this policy page as the exception."""
    bad = []
    for rel in tracked("*.md"):
        if os.path.basename(rel) == "policy.md":
            continue
        low = prose(read(rel)).lower()
        for v in VENDORS:
            if re.search(rf"(?<![\w-]){v}(?![\w-])", low):
                bad.append(f"{rel} names {v}; say 'an assistant' or 'an agent'")
    return bad


#: Where each numbering is defined. A number is legible inside its own document
#: and is a lookup everywhere else, so it is only allowed at home. *Home* is a
#: set rather than one file because a document that has grown may be split
#: across two -- `report-card.md` is `vision.md`'s grading half, governed by it
#: and citing its tenets the way any section of it would. Splitting a page is
#: not the same as citing one, and a check that could not tell them apart would
#: charge a filename change as a defect.
NUMBERED = {"rule": ("policy.md",),
            "tenet": ("vision.md", "report-card.md"),
            "position": ("reporting-policy.md",)}


def check_citations() -> list[str]:
    """*When you cite a rule from another document, say what it says*."""
    bad = []
    for rel in tracked("*.md"):
        base = os.path.basename(rel)
        text = prose(read(rel))
        for word, home in NUMBERED.items():
            if base in home:
                continue
            for m in re.finditer(rf"\b{word}s?\s(\d{{1,2}})\b", text, re.I):
                bad.append(f"{rel} cites {word} {m.group(1)} by number; say what it says")
    return bad


#: How an affiliating note may spell its refusal of the policy. Wording varies;
#: the clause may not.
NOT_HELD = ["does not adopt", "adopts no", "not held to", "does not follow",
            "not bound by", "does not adhere"]

#: The membership claim, and the whole of what is required to have made it.
#:
#: **`part of` is the word that decides it, not the link.** The affiliating soft
#: note names this ecosystem too -- *it works with the Eunoia ecosystem and is
#: not held to its policy* -- so a check that accepted any mention of the name
#: would read that note as a declaration. What separates them is the claim: one
#: says it is *part of* this, the other says it *works with* it.
#:
#: This used to also require a link to the policy, and two members that had
#: plainly joined failed on it while making the claim in as many words. A
#: declaration decides *declares / does not declare*, and a repository that says
#: it is part of this has declared. The link is worth having and is now reported
#: as a minor finding rather than failing anybody's build.
MEMBER_CLAIM = r"\b(?:part|member)\s+of\s+(?:the\s+)?\**\s*eunoia ecosystem"

#: How a footing line may spell the obligation it takes on -- the mirror of
#: `NOT_HELD`, and tested after it, because *not held to* contains *held to*.
HELD_CLAIM = ["held to", "follows", "adopts", "adheres to", "bound by"]

#: The local page a repository uses to record what it declines to put on its
#: front page. The owner is already recorded here and kept off every other page,
#: so a membership that is deliberately not advertised is recorded in the same
#: place, in the same shape, and read the same way.
FOOTING_PAGE = "docs/maintenance.md"

#: The footing marker, as `check_owner_unadvertised` reads `**Owner:**` from the
#: same page: a name, then the reason it is being recorded. The reason is not
#: decoration -- a bare word would let a tree opt out of the declaration check by
#: asserting a footing and saying nothing about what it has taken on.
#:
#: **The reason is optional to the pattern and required by the reader**, which is
#: deliberate: a marker written without one has to be *matched* in order to be
#: *refused*. A pattern that demanded the reason would read a bare footing line
#: as no marker at all, and the tree would fail the declaration check with a
#: message about its README while the mistake sat in another file.
#:
#: The pattern matches the marker; **the reason is the paragraph it opens**, read
#: to the next blank line by `footing_in`. Every document here wraps at eighty
#: columns, so a reason that had to fit on one line would be a convention nobody
#: could follow while writing ordinary prose -- and the failure would be silent,
#: since the half of the sentence that wrapped is the half that says anything.
FOOTING_LINE = r"^\*\*Footing:\*\*\s*`([\w-]+)`[ \t]*(?:[—-][ \t]*)?"

#: The footings this checker knows how to act on. **The authority for what
#: footings exist is the shared policy, not this file**; these are a reader's
#: copy of the two names that change what a run does here.
#:
#: `associate` was the name the policy settled on for a repository with no
#: front-page declaration. This checker proposed `unadvertised-member` for the
#: same thing and was answered: the notion was taken and the name was not, which
#: is the right way round. The old name is not accepted as a synonym -- a tree
#: using it is using a footing nothing defines, and should hear so.
ASSOCIATE = "associate"
UNADVERTISED_CHILD = "unadvertised-child"

#: The footing names a marker may carry. Anything else is a typo or a footing
#: this checker has not been taught, and both are worth saying rather than
#: passing over -- but only the two above change what is checked.
FOOTINGS = {ASSOCIATE, UNADVERTISED_CHILD, "member", "president",
            "candidate", "foundation", "child", "outsider"}

#: How an unadvertised child's marker may spell what makes it unadvertised. The
#: fact being recorded is about the *parent's* front page, so the line has to say
#: something about it: a child is on its parent's footing and owes nothing of its
#: own, so there is no obligation clause to ask for and the absence of one is not
#: a lapse. What is left to state is the thing a reader cannot otherwise check.
NOT_ADVERTISED = ["not advertised", "unadvertised", "front page does not",
                  "not named on the front page", "does not name it"]


def maintenance_note(text: str) -> str:
    """The body of the README's maintenance note, or "" if there is none.

    Shared by the two readers below, because a footing that makes a claim about
    somebody's tree should be decided by reading that tree, and both of them read
    the same section of it.
    """
    # `[ \t]*` rather than `\s*`: the latter swallows the newline after the
    # heading, so a maintenance note that is the last line of a README ends up
    # with `m.end()` at the end of the text and reads as *no heading at all*.
    # That was invisible while `note_in` was only ever reported; it is a
    # failure message somebody has to act on now.
    secs = list(re.finditer(r"^##[ \t]+(.+?)[ \t]*$", text, re.M))
    note = ""
    for i, m in enumerate(secs):
        if "maintain" in m.group(1).lower():
            note = text[m.end(): secs[i + 1].start() if i + 1 < len(secs) else len(text)]
    return note


def note_in(text: str) -> list[str]:
    """What is missing from a bare maintenance note: the *whole* of the
    associate protocol as currently drafted, and it is drafted rather than
    decided.

    A heading saying how the repository is run, and something under it. No
    declaration, no link to us, no workflow, no pin, and nothing about the shape
    of the tree. The shared policy describes which parts of the associate
    protocol remain undecided.

    Read for a **report** and never for a verdict. Nothing in `CHECKS` calls it,
    nothing fails on it, and the repositories it is asked about are held to none
    of this. Ecosystem inventory tooling can use it to report who would satisfy
    a proposed protocol.
    """
    if not text:
        return ["no README.md, so nothing says how the repository is maintained"]
    note = maintenance_note(text)
    if not note:
        return ["README.md has no `How this repository is maintained` heading"]
    if len(prose(note).split()) < 12:
        return ["the maintenance note is a heading with nothing under it"]
    return []


def declaration_in(text: str) -> list[str]:
    """What is missing from a README's declaration of membership, if anything.

    Split out from the check below so inventory tooling can ask the same
    question of a fetched README. Both readers use one implementation.
    """
    if not text:
        return ["no README.md, so nothing declares membership"]
    note = maintenance_note(text)
    if not note:
        return ["README.md has no maintenance note to declare membership in"]
    bad = []
    low = note.lower()
    if not re.search(MEMBER_CLAIM, low):
        bad.append("the maintenance note does not say it is part of the Eunoia ecosystem")
    # A note that declares membership and also refuses the policy says nothing,
    # and *a repository that later joins rewrites the section rather than adding
    # to it* is the rule that makes it so. Refusing the contradiction here is what
    # keeps an affiliating note -- which may well link this page in order to say
    # what it is not held to -- from being read as a declaration.
    if not bad and any(f in low for f in NOT_HELD):
        bad.append("the maintenance note declares membership and also says it is "
                   "not held to the policy; a note carrying both says nothing")
    return bad


def affiliation_in(text: str) -> list[str]:
    """What is missing from an **affiliating** maintenance note, if anything.

    The note names the ecosystem it works with and says it is not held to the
    policy. Inventory tooling can use this reader on a fetched README, just as it
    uses `declaration_in` for a member.

    **This is not the `associate` footing, whatever the shared policy's older
    paragraphs still say.** `associate` was once the word for a tool we had read
    and did not hold; it now means a repository with no front-page declaration
    that records on its own maintenance page what it holds *itself* to, which is
    very nearly the opposite. `associate_in` reads that. This reader keeps the
    note it always read — a repository that adopts none of this — and the two
    must not be confused, because one is held to the policy and one is held to
    nothing.

    **This is never a check in `CHECKS`.** It is about a repository that has
    joined nothing, and running it here would be this tree grading somebody who
    is not held to it.
    """
    if not text:
        return ["no README.md, so nothing says how the repository is maintained"]
    note = maintenance_note(text)
    if not note:
        return ["README.md has no maintenance note"]
    low = note.lower()
    bad = []
    if "eunoia ecosystem" not in low:
        bad.append("the maintenance note does not name the Eunoia ecosystem")
    if not any(f in low for f in NOT_HELD):
        bad.append("the maintenance note does not say it is not held to the policy, "
                   "which is what keeps it from reading as a declaration")
    return bad


def footing_in(text: str) -> tuple[str, str]:
    """The footing a maintenance page records, and the reason it gives.

    `("", "")` when the page records none, which is the ordinary case: a member
    declares on its front page and needs no marker, and a repository that has
    joined nothing has nothing to record.
    """
    m = re.search(FOOTING_LINE, text, re.M)
    if not m:
        return ("", "")
    paragraph = re.split(r"\n[ \t]*\n", text[m.end():], maxsplit=1)[0]
    return (m.group(1), " ".join(paragraph.split()))


def associate_in(text: str) -> list[str]:
    """What is missing from an **associate's** footing marker.

    A repository can be held to the policy and have good reason not to say so on
    its front page: it is not published yet, or it is one person's working tree,
    or advertising an arrangement would oversell what is in it. The declaration
    and the compliance are separable, and *both, or neither* only ever spoke to
    the pair being advertised together.

    **So the claim moves rather than disappearing.** It goes on the local
    maintenance page, which is where this convention already puts what a
    repository declines to advertise. What the marker records is an obligation
    the repository imposes on **itself** -- an associate owes this ecosystem
    nothing -- so the line has to say what that obligation is. A marker naming a
    footing and no obligation leaves a reader, and this checker, with nothing to
    hold it to and nothing to measure it against.

    **That is also why the marker is read this strictly while nothing is owed.**
    Strictness here is not an obligation being enforced; it is the difference
    between a claim somebody can check and a word. What the checks then find is
    measured against this line and not against anything we are due.

    Takes the text of `docs/maintenance.md`, so inventory tooling can ask the
    question of a fetched page, as `declaration_in` and `affiliation_in` are
    asked of a fetched README.
    """
    if not text:
        return [f"no {FOOTING_PAGE}, so nothing records a footing"]
    name, reason = footing_in(text)
    if not name:
        return [f"{FOOTING_PAGE} records no **Footing:** line"]
    if name != ASSOCIATE:
        return [f"{FOOTING_PAGE} records the footing `{name}`, not `{ASSOCIATE}`"]
    bad = []
    low = reason.lower()
    # Order matters: *not held to* contains *held to*, and a refusal of the
    # policy under this footing is the one contradiction worth naming before the
    # absence of a claim. A tree that is held to none of this is not an
    # associate; it keeps the independent soft note and `affiliation_in` reads it.
    if any(f in low for f in NOT_HELD):
        bad.append("the footing line takes the footing and also refuses the "
                   "policy; a marker carrying both says nothing")
    elif not any(h in low for h in HELD_CLAIM):
        bad.append("the footing line does not say the repository holds itself to "
                   "anything, so it records a word rather than a footing")
    if "polic" not in low:
        bad.append("the footing line does not name the policy it holds itself to")
    return bad


def unadvertised_child_in(text: str) -> list[str]:
    """What is missing from an **unadvertised child project's** footing marker.

    A child project is reached through its parent and stands on its parent's
    footing, owing nothing of its own — so *unadvertised* means something
    different here than it does for a repository. It is not a membership kept
    off a front page; it is a project the parent has chosen not to put on its
    front page at all. Read-only work, a line of enquiry that may not go
    anywhere, something the parent does not want counted among what it ships.

    **So the marker records a fact about the parent, and the parent's README is
    what settles it.** The line says the project is not advertised; the check
    that reads it goes and looks. Nothing is asked about obligations, because a
    child has none to state.

    Takes the text of `tools/<name>/README.md`, which for a child project is a
    local page and not a front page — the same reason the membership marker
    lives on the local maintenance page rather than the README.
    """
    if not text:
        return ["no README.md, so nothing records a footing"]
    name, reason = footing_in(text)
    if not name:
        return ["the README records no **Footing:** line"]
    if name != UNADVERTISED_CHILD:
        return [f"the README records the footing `{name}`, not `{UNADVERTISED_CHILD}`"]
    if not any(f in reason.lower() for f in NOT_ADVERTISED):
        return ["the footing line does not say the project is unadvertised, so it "
                "records a word rather than a fact somebody can check"]
    return []


def records_associate() -> bool:
    """Whether the tree under test records the `associate` footing."""
    return not associate_in(read(FOOTING_PAGE))


def is_associate() -> bool:
    """An associate without qualification: the marker, and no declaration.

    A tree carrying **both** is neither of the two things it is claiming, and
    `check_footing_consistent` says so. Nothing else here treats it as an
    associate, because doing that would quietly settle a contradiction in
    favour of whichever half this file happened to read first -- and would let
    the softer reading of the number win by accident.
    """
    return bool(records_associate() and declaration_in(read("README.md")))


def check_declaration() -> list[str]:
    """*Joining the Eunoia ecosystem* — the claim the rest of this run backs.

    A declaration nothing backs is what this whole check exists to prevent, and a
    compliant tree that says nothing has not joined anything. So both, or neither.

    An associate is the one tree this does not run against, because carrying no
    front-page declaration is what the footing *is*. It is skipped by name rather
    than passed: see `is_advertised`.
    """
    return declaration_in(read("README.md"))


def check_footing_marker() -> list[str]:
    """*A footing marker names a footing, and says what it takes on.*

    Runs against any tree that records one. A marker is a claim the rest of this
    run is read against, exactly as a declaration is, so a malformed one is
    reported and not shrugged off -- it stands in for the front-page declaration,
    and it is the only place a reader can check what the tree holds itself to.

    **Reporting it is not charging anybody with anything.** An associate owes us
    nothing, and what a run of this finds on one is a measurement; the shared
    register is what decides whose fault a number is, and it prints an
    associate's as *tracked*. What is refused here is a marker that cannot be
    read, which is a different thing from a tree that falls short of it.
    """
    text = read(FOOTING_PAGE)
    name, _reason = footing_in(text)
    if not name:
        return []
    if name not in FOOTINGS:
        return [f"{FOOTING_PAGE} records the footing `{name}`, which is not one "
                "the shared policy defines"]
    return associate_in(text) if name == ASSOCIATE else []


def check_footing_consistent() -> list[str]:
    """*An associate carries no front-page declaration.*

    The footing is defined by the absence: a repository that declares membership
    on its front page is a member, and one that does not may record this footing
    instead. A tree doing both leaves a reader with two answers and no way to
    choose, and the two are not the same claim -- a member is held to this by
    the declaration, an associate by its own marker and nothing else. Say one:
    delete the marker, or delete the declaration.
    """
    if not records_associate():
        return []
    if declaration_in(read("README.md")):
        return []
    return [f"{FOOTING_PAGE} records `{ASSOCIATE}` and README.md declares "
            "membership; a declared membership is a member's, not an associate's"]


def check_associate_floor() -> list[str]:
    """*An associate still says how it is maintained.*

    An associate owes this ecosystem nothing, and this is not a debt being
    collected. It is the floor the **footing** needs in order to mean anything:
    the marker says a tree holds itself to the policy while declaring nothing in
    public, so the front page is the only thing a reader arriving at the
    repository has, and a maintenance note is what makes it usable.

    **This asks for nothing the shared policy does not already ask.** Its
    associate protocol says that for a tree adopting none of this the ask is
    still one heading -- `How this repository is maintained`, with something
    under it. `note_in` is that reading and was written for it; all this does is
    give it a verdict.

    **Explaining the name is not part of the floor.** It is recommended for
    every repository and required of none, and an associate is not an exception:
    see `check_name_explained`, which reports it as a minor finding here as it
    does everywhere else.
    """
    return list(note_in(read("README.md")))


def check_child_unadvertised() -> list[str]:
    """*An unadvertised child project is not named on the front page.*

    The marker's content is a fact about the parent, so the parent is where it
    is checked. A child that records the footing and is then named on the front
    page is advertised, whatever its README says — and the front page is the one
    a reader believes, because it is the one they see first.

    A child that records no footing is the ordinary case and is not asked to.
    """
    bad = []
    front = read("README.md")
    for name in child_projects():
        text = read(f"tools/{name}/README.md")
        footing, _reason = footing_in(text)
        if not footing:
            continue
        if footing not in FOOTINGS:
            bad.append(f"tools/{name}: records the footing `{footing}`, which is "
                       "not one the shared policy defines")
            continue
        if footing != UNADVERTISED_CHILD:
            continue
        bad += [f"tools/{name}: {b}" for b in unadvertised_child_in(text)]
        if re.search(rf"\b{re.escape(name)}\b", front):
            bad.append(f"tools/{name}: records `{UNADVERTISED_CHILD}` and the "
                       "front page names it; it is advertised after all")
    return bad


def check_front_page() -> list[str]:
    """*There is one entry point.*"""
    bad = []
    readme = read("README.md")
    if not readme:
        return ["no README.md at the repository root"]
    for name in COMPETING_ENTRY:
        if os.path.exists(os.path.join(ROOT, name)):
            bad.append(f"{name} competes with README.md for the entry point")
    return bad


def check_name_explained() -> list[str]:
    """*Every repository explains its own name* -- recommended, never enforced.

    A repository that arrived with its name already fixed, or whose name has no
    story worth a paragraph, is not doing anything wrong, and failing somebody's
    build over the absence of an etymology would be the wrong instrument for what
    is at bottom a suggestion about being readable.

    **Recommended for everyone, and required of nobody -- an associate
    included.** This check briefly made an exception of one, on the argument
    that an associate's front page is its whole public surface. The argument was
    not enough: the rule says *recommended*, it says it about every repository,
    and a footing is not a reason to read one word of it differently. A check
    that hardens for the tree least able to answer back is the wrong instrument
    twice over.
    """
    readme = read("README.md")
    if readme and not any("name" in sec.lower() for sec in sections(readme)):
        return ["README.md has no section explaining the repository's name"]
    return []


def check_owner_unadvertised() -> list[str]:
    """The local maintenance page records ownership without front-page credit.

    Home-only: another repository chooses its own attribution. A shared
    governance document may carry its own ownership record independently.
    """
    source = "docs/maintenance.md"
    m = re.search(r"^\*\*Owner:\*\*\s*`[^`]+`\s*[—-]\s*([^.\n]+?)\.", read(source), re.M)
    if not m:
        return [f"{source} does not record an owner, so accountability rests on nobody"]
    name = m.group(1).strip()
    bad = []
    for rel in tracked("*"):
        if rel in {source, "docs/policy.md"} or os.path.splitext(rel)[1] in BINARY:
            continue
        if name.lower() in read(rel).lower():
            bad.append(f"{rel} names the owner; keep anoieu's attribution in {source}")
    return bad


def check_maintenance_note() -> list[str]:
    """*The maintenance note* — the last section of the README, always."""
    secs = sections(read("README.md"))
    if not secs:
        return ["README.md has no sections"]
    if "maintain" not in secs[-1].lower():
        return [f"README.md ends with {secs[-1]!r}, not the maintenance note"]
    return []


def check_docs_index() -> list[str]:
    """*`docs/` has an index* — and every document it carries is named in it."""
    index = read("docs/README.md")
    if not index:
        return ["docs/README.md, the documentation index, does not exist"]
    bad = []
    for path in tracked("docs"):
        if not path.endswith(".md"):
            continue
        base = os.path.basename(path)
        if base in INDEX_EXEMPT or re.match(INDEX_EXEMPT_RE, base):
            continue
        if base not in index:
            bad.append(f"{path} is not named in docs/README.md")
    return bad


def check_generated_labelled() -> list[str]:
    """*Written and generated documents are separated and labelled*."""
    bad = []
    for base in GENERATED:
        text = read(f"docs/{base}")
        if not text:
            bad.append(f"docs/{base} is missing")
        elif not re.search(r"generated|rendered (from|by)|written by|rewritten", text[:2000], re.I):
            bad.append(f"docs/{base} does not say it is generated")
    return bad


def check_dependencies() -> list[str]:
    """*Dependencies are fetched and pinned, never vendored*."""
    bad = []
    if tracked("deps/*"):
        bad.append("deps/ has tracked files: dependencies are vendored, not fetched")
    for rel in ("scripts/deps.json", "scripts/deps.lock"):
        if not os.path.exists(os.path.join(ROOT, rel)):
            bad.append(f"{rel} is missing: nothing pins what was read")
    return bad


def check_working_space() -> list[str]:
    """*Working space is untracked, and says so*."""
    ignore = read(".gitignore")
    bad = []
    for pat in ("scratch/", "*.local.md"):
        if pat not in ignore:
            bad.append(f".gitignore does not carry {pat}")
    if tracked("scratch/*"):
        bad.append("scratch/ has tracked files")
    return bad


def child_projects() -> list[str]:
    """Directories under `tools/` that say they are child projects.

    A README is not enough on its own: plenty of repositories keep an ordinary
    tool under `tools/` with a README describing it, and holding those to the
    charter rules is a check firing on something that is not a problem. Like
    membership, this is declared rather than inferred -- a child project says so
    in its own first paragraph, and one that does not is not one.
    """
    out = []
    tools = os.path.join(ROOT, "tools")
    if not os.path.isdir(tools):
        return out
    for name in sorted(os.listdir(tools)):
        d = os.path.join(tools, name)
        if not os.path.isdir(d) or name.startswith((".", "__")):
            continue
        readme = read(os.path.join("tools", name, "README.md"))
        if re.search(r"\b(child|research) project\b", readme, re.I):
            out.append(name)
    return out


def island_breaks(name: str) -> list[str]:
    """Rule 2 and rule 3, as far as a grep can see them."""
    breaks = []
    hits = subprocess.run(
        ["git", "-C", ROOT, "grep", "-l", "-E", rf"\b(tools\.)?{re.escape(name)}\b",
         "--", ":!tools/" + name, ":!docs/coherence.md", ":!docs/policy.md",
         ":!docs/vision.md"],
        capture_output=True, text=True).stdout.split()
    code = [h for h in hits if h.endswith((".py", ".yml", ".toml"))]
    if any(h.startswith(".github/") for h in hits):
        breaks.append("rule 2: it runs in CI")
    if [h for h in code if not h.startswith(".github/")]:
        breaks.append(f"rule 2: named by code outside its own directory ({', '.join(sorted(code)[:3])})")
    if "README.md" in hits or "docs/README.md" in hits:
        breaks.append("rule 3: it is advertised on the front page or in the documentation index")
    return breaks


def check_children() -> list[str]:
    """Rules 4, 5 and 10 for every child project under `tools/`."""
    bad = []
    for name in child_projects():
        readme = read(f"tools/{name}/README.md")
        low = readme.lower()
        if "does not" not in low and "out of scope" not in low and "is not" not in low:
            bad.append(f"tools/{name}: rule 5, the charter never says what it will not do")
        if not re.search(r"[Ͱ-Ͽ]|etymolog|greek", readme, re.I):
            bad.append(f"tools/{name}: rule 4, the README does not explain the name")
        breaks = island_breaks(name)
        # Either the number or the thing the number says. The number alone was
        # the original marker and it put two of our own checks in conflict: a
        # non-island child had to write "rule 10", and no document outside
        # `policy.md` may cite a rule by number. Both rules are right and the
        # marker was wrong -- a reader of a charter should be told what the
        # exception *is*, not given a lookup. The number still passes, so no
        # tree that already used it breaks.
        if breaks and "rule 10" not in low and "not an island" not in low:
            bad.append(f"tools/{name}: not an island and no rule 10 statement — "
                       + "; ".join(breaks))
        elif breaks:
            print(f"     tools/{name}: rule 10 exception recorded, {len(breaks)} break(s)")
            for b in breaks:
                print(f"       - {b}")
    return bad


def check_links() -> list[str]:
    """*docs/ has an index* and the rest of the layout, made checkable.

    A relative link that does not resolve is a defect in the tree, and it is the
    characteristic cost of moving a document: the prose still reads correctly and
    every path in it is wrong. This also covers the paths the outbound prompts in
    `scripts/` name, because a prompt that sends somebody to a document that
    moved is worse than one that sends them nowhere.
    """
    bad = []
    for rel in tracked("*.md") + ["prompts/check_anoieu", "prompts/process_anoieu",
                                    "prompts/join_eo", "prompts/check_join_eo",
                                    "prompts/process_discussion", "prompts/init_eo",
                                    "prompts/global_audit", "prompts/welcome_eo"]:
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            continue
        here = os.path.dirname(full)
        text = read(rel)
        # A markdown link resolves from the file that carries it, always -- a
        # child project with its own docs/ writes `](docs/x.md)` and means its
        # own. A bare `docs/...` in prose or in a prompt is conventionally
        # repo-relative, but the same sentence inside a subdirectory may mean
        # the local one, so either reading counts: a path that resolves under
        # one of them is not a broken link.
        targets = [(m.group(1), [here]) for m in re.finditer(r"\]\(([^)\s]+)\)", text)]
        targets += [(t, [ROOT, here]) for t in
                    re.findall(r"(?<![\w/`(])(docs/[\w./-]+\.(?:md|html))", text)]
        for t, bases in targets:
            t = t.split("#")[0]
            if not t or t.startswith(("http", "mailto:")):
                continue
            if not any(os.path.exists(os.path.normpath(os.path.join(b, t)))
                       for b in bases):
                bad.append(f"{rel} links to {t}, which does not exist")
    return bad


def slug(heading: str) -> str:
    """A heading as GitHub anchors it: lowercased, punctuation dropped, spaces
    hyphenated. Approximate by design -- it is used to *accept*, never to
    rewrite, so an anchor this gets wrong is reported and looked at."""
    h = re.sub(r"`|\*|_", "", heading.strip().lower())
    h = re.sub(r"[^\w\s-]", "", h)
    # each space becomes a hyphen, runs are not collapsed: "a - b" anchors as
    # "a---b" once the dash is dropped, which is what GitHub does.
    return re.sub(r"\s", "-", h)


def check_anchors() -> list[str]:
    """A link to a heading that does not exist, in a document in this tree.

    The half of a moved document that a plain link check misses: the file still
    resolves and the section it names is gone. This is the damage a reorganised
    documentation tree does silently, and it costs nothing to keep true.
    """
    bad = []
    for rel in tracked("*.md"):
        here = os.path.dirname(os.path.join(ROOT, rel))
        text = prose(read(rel))
        for m in re.finditer(r"\]\(([^)\s]*\.md)#([^)\s]+)\)", text):
            target, anchor = m.group(1), m.group(2)
            full = os.path.normpath(os.path.join(here, target))
            if not os.path.isfile(full):
                continue                      # the link check owns that failure
            with open(full, encoding="utf-8") as fh:
                heads = {slug(h) for h in re.findall(r"^#{1,6}\s+(.+?)\s*$",
                                                     prose(fh.read()), re.M)}
            if anchor.lower() not in heads:
                bad.append(f"{rel} links to {target}#{anchor}, and that heading "
                           "is not in it")
    return bad


def check_local_paths() -> list[str]:
    """An absolute path out of somebody's home directory, committed in a document.

    Always a leak and never useful to a reader: it names a machine that is not
    theirs. Decidable, and the list of things it looks for does not grow.

    Documents *and* committed data. It read `*.md` only until two promoted fuzz
    reproducers were found recording the absolute seed path they were shrunk
    from -- one naming a former machine's home directory and one a scratch
    directory under it. A rule that holds for prose and not for the data beside
    it is a rule with a hole in it, and this is the shape the hole takes: the
    leak arrives through a generator rather than through somebody typing.
    """
    bad = []
    for rel in tracked("*.md"):
        for m in re.finditer(HOME_PATH, prose(read(rel))):
            bad.append(f"{rel} carries the absolute path {m.group(1)}/…, "
                       "which names one machine")
            break
    return bad


def check_local_paths_data() -> list[str]:
    """The same rule, over committed **data** -- reported, never fatal.

    Two promoted fuzz reproducers here recorded the absolute seed path they were
    shrunk from, which is how a home directory reaches a tree that forbids one in
    prose: through a generator rather than through somebody typing. So the rule
    is worth applying to data, and the surface is new.

    **Minor on purpose, and this one is not about being new.** Run against the
    members, it passes two and fails a third on files it has every right to have
    committed before anybody wrote this down. Promoting it to fatal now would
    turn somebody's build red on the day they bump for an unrelated reason, and
    the announcement carrying this stretch says in terms that nothing goes red on
    anybody. It becomes fatal when the trees it applies to are clear of it, which
    is a decision for a person and not a date.
    """
    bad = []
    for rel in tracked("*"):
        if rel.endswith(".md") or rel.startswith("deps/"):
            continue
        if os.path.splitext(rel)[1] in BINARY:
            continue
        for m in re.finditer(HOME_PATH, read(rel)):
            bad.append(f"{rel} carries the absolute path {m.group(1)}/…, "
                       "which names one machine")
            break
    return bad


def check_declaration_first() -> list[str]:
    """*Declare it, at the top of your maintenance note.*

    Position is the whole of what this adds: a declaration buried under three
    paragraphs is not what a reader arriving at the note first sees.
    """
    text = read("README.md")
    secs = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    for i, m in enumerate(secs):
        if "maintain" not in m.group(1).lower():
            continue
        end = secs[i + 1].start() if i + 1 < len(secs) else len(text)
        note = text[m.end():end].strip()
        if "eunoia ecosystem" not in note.lower():
            return []                      # check_declaration owns that failure
        first = note.split("\n\n")[0].lower()
        if "eunoia ecosystem" not in first:
            return ["the membership declaration is not the first paragraph of "
                    "the maintenance note"]
    return []


def check_scripts_listed() -> list[str]:
    """Every command or helper in scripts/ and prompts/ is locally catalogued."""
    source = "docs/maintenance.md"
    table = read(source)
    if not table:
        return [f"{source}, the local script catalogue, does not exist"]
    bad = []
    for rel in tracked("scripts/*") + tracked("prompts/*"):
        name = os.path.basename(rel)
        if name.endswith(".local") or f"`{name}" in table:
            continue
        bad.append(f"{rel} is not in the table in {source}")
    return bad


def check_response_gate() -> list[str]:
    """*Responding to somebody else's discussion file* — the protocol's safety rule.

    A build failure rather than a minor finding: it is the only thing in the file
    that stops an agent acting on correspondence nobody asked it to act on, and a
    safety rule that degrades to a warning is one that is eventually ignored.

    **It is a rule about the file and never about having one.** A repository that
    keeps no `docs/discussion.md` is skipped rather than failed, by the
    applicability gate in `CHECKS`. The fatal tier obliges a repository to gate
    the channel it opened; it has never been this checker's business to oblige
    anybody to open one, and for a while it did that by accident — a missing file
    reported here as a build failure, in the same run that reported it as a minor
    finding, next to a vacuous pass. See *The discussion file* in the policy.
    """
    text = read("docs/discussion.md")
    if not text:
        return []                      # no channel to gate; `CHECKS` skips it
    first_topic = re.search(r"^##\s+D\d+\s", text, re.M)
    head = text[: first_topic.start()] if first_topic else text
    if "&gt;" not in head and not re.search(r"^>", head, re.M):
        return ["docs/discussion.md has no banner block above its first topic"]
    low = head.lower()
    bad = [f"the banner does not state {what}"
           for what, forms in BANNER if not any(f in low for f in forms)]
    return bad


def check_declaration_links() -> list[str]:
    """*Declare it, at the top of your maintenance note* — the link half.

    Reported, never fatal. The declaration is the claim; the link is how a
    reader who has just been told this repository follows a shared policy finds
    out what the policy asks. That is worth saying and is not worth turning
    somebody's build red over — and it had been doing exactly that to two
    repositories that had joined and said so plainly.
    """
    note = maintenance_note(read("README.md"))
    if not note or not re.search(MEMBER_CLAIM, note.lower()):
        return []                      # not a declaration; nothing to link from
    if any(repo in note for repo in POLICY_REPOS) and "policy.md" in note:
        return []
    return [f"the declaration does not link to {POLICY_REPO}'s docs/policy.md, so "
            "a reader is told this repository follows a policy and not where to "
            "read it"]


def check_discussion() -> list[str]:
    """*The discussion file* — reported as minor, never as a build failure.

    It grades the shape of a channel that exists. Whether one exists at all is
    not graded here or anywhere, and the applicability gate in `MINOR` is what
    keeps it that way: a repository with no file to grade is skipped and named,
    rather than told in passing that it is missing something.
    """
    text = read("docs/discussion.md")
    if not text:
        return []                      # nothing to grade; `MINOR` skips it
    bad, seen, fenced = [], set(), False
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^##\s+(D\d+)\s+—\s+(.+?)\s*$", line)
        if not m:
            if re.match(r"^##\s+(?!#)", line) and i > 6:
                bad.append(f"{line.strip()!r} is not `## D<n> — <topic>`")
            continue
        tid, _ = m.groups()
        if tid in seen:
            bad.append(f"{tid} is used twice; ids are allocated once and never reused")
        seen.add(tid)
        # The whole contiguous field block, however long it is -- not a fixed
        # window. It used to read eight lines, which was one more than the five
        # required fields needed and exactly as many as a topic carrying both
        # `Pinned:` and `Global:` produces. A seventh field, or any field value
        # wrapping onto a second line, pushed a required one out of the window
        # and this reported it missing when it was there.
        block = []
        for line in lines[i + 1:]:
            if line.startswith("## "):
                break
            if not line.strip():
                if block:
                    break
                continue              # the blank between heading and fields
            if not re.match(r"^\*\*[A-Za-z ]+:\*\*", line) and not block:
                break                 # no field block at all
            block.append(line)
        got = dict(re.findall(r"^\*\*([A-Za-z ]+):\*\*\s*(.*)$", "\n".join(block), re.M))
        for f in FIELDS:
            if f not in got or not got[f].strip():
                bad.append(f"{tid} has no **{f}:**")
        if got.get("To", "").strip().lower() in {"", "upstream", "the ecosystem", "everyone"}:
            bad.append(f"{tid} does not name the tool it addresses unequivocally")
        kind = got.get("Kind", "").strip()
        if kind and kind not in KINDS:
            bad.append(f"{tid} has Kind {kind!r}, not one of {'/'.join(sorted(KINDS))}")
        for f in RETIRED_FIELDS:
            if f in got:
                bad.append(f"{tid} carries **{f}:**, which the format no longer "
                           "has; a discussion is live while it is in the file, "
                           "and a finished one is removed")
    if not seen:
        bad.append("docs/discussion.md carries no topics")
    return bad


def check_prompt_gate() -> list[str]:
    """*A prompt may not be for this repository* -- carried beside the response
    gate, and reported rather than enforced while it is new.

    Beside the gate and never folded into it: the response gate is the one rule
    here enforced as a build failure, and diluting it is a worse trade than
    repeating a sentence next to it.
    """
    low = prose(read("docs/discussion.md")).lower()
    if not low:
        return []                      # no channel to carry it; `MINOR` skips it
    return [f"docs/discussion.md does not carry {what}"
            for what, forms in PROMPT_GATE if not any(f in low for f in forms)]


def has(*rel):
    """Applicability: the check runs only where the thing it is about exists."""
    def applies():
        for r in rel:
            if os.path.exists(os.path.join(ROOT, r)):
                return None
        return "nothing at " + " or ".join(rel)
    return applies


def is_home():
    return None if os.path.abspath(ROOT) == REPO_ROOT else "specific to anoieu's own files"


def not_associate():
    """Applicability: the floor below is about an associate's front page only.

    Named on every other run rather than silently skipped, because a member
    reading its own log should be able to see that this check exists and why it
    did not apply to them.
    """
    return None if is_associate() else "this tree carries no `associate` marker"


def is_advertised():
    """Skip reason for the declaration checks when the tree records `associate`.

    A skip rather than a pass, because the run must not read as having found a
    declaration it never looked for. The line it prints names the marker and the
    page it is on, so a reader of the log can go and check the claim -- which is
    the only thing standing in for the front page here.
    """
    if not is_associate():
        return None
    return (f"{FOOTING_PAGE} records the footing `{ASSOCIATE}`: no front-page "
            "declaration, and what it holds itself to is written there")


# (title, check, applies). A check that does not apply is skipped and named:
# passing must never read as more coverage than it was. The set is deliberately
# small and is expected to grow.
CHECKS = [
    ("the README declares membership of the ecosystem", check_declaration, is_advertised),
    ("the front page is the only entry point", check_front_page, None),
    ("the README ends with the maintenance note", check_maintenance_note, None),
    ("every document is named in the documentation index", check_docs_index, has("docs")),
    ("every generated document says it is generated", check_generated_labelled, is_home),
    ("dependencies are fetched and pinned, never vendored", check_dependencies, has("deps", "scripts/deps.json")),
    ("working space is untracked", check_working_space, has(".gitignore")),
    ("child projects carry a charter, and name what they break", check_children, has("tools")),
    ("the discussion file carries the response gate, at the top",
     check_response_gate, has("docs/discussion.md")),
    ("every link in a document or an outbound prompt resolves", check_links, None),
    ("no document names a specific AI", check_no_vendor, None),
    ("no document cites another document's rule by number", check_citations, None),
    ("every link to a heading finds one", check_anchors, None),
    ("no document names one machine's filesystem", check_local_paths, None),
    ("the membership declaration opens the maintenance note",
     check_declaration_first, is_advertised),
    ("every script is listed where the scripts are listed", check_scripts_listed, is_home),
    ("local ownership is recorded without advertising", check_owner_unadvertised, is_home),
    ("a recorded footing names one the policy defines, and what it takes on",
     check_footing_marker, has(FOOTING_PAGE)),
    ("an associate carries no front-page declaration",
     check_footing_consistent, has(FOOTING_PAGE)),
    ("an associate's front page says how it is maintained",
     check_associate_floor, not_associate),
    ("an unadvertised child project is not named on the front page",
     check_child_unadvertised, has("tools")),
]


# Reported, never fatal. A malformed field block is a lapse in somebody's
# correspondence rather than a defect in their tree, and failing a build over
# the shape of a sentence addressed to a colleague is the wrong instrument.
MINOR = [
    ("the membership declaration links to the policy", check_declaration_links, is_advertised),
    ("the discussion file is well-formed", check_discussion, has("docs/discussion.md")),
    ("the README explains the repository's name", check_name_explained, None),
    ("committed data carries no path out of a home directory", check_local_paths_data, None),
    ("the discussion file says a prompt may be misaddressed",
     check_prompt_gate, has("docs/discussion.md")),
]


def coverage() -> None:
    print("-- checked")
    for title, _, _a in CHECKS:
        print(f"   {title}")
    for title, _, _a in MINOR:
        print(f"   {title} (minor: reported, never fatal)")
    print("-- not checked, and why")
    for rule, why in UNCHECKED:
        print(f"   {rule} — {why}")
    print("-- never to be checked")
    print("   the shared vision, in full — judgement, and nobody has the authority")


def main() -> int:
    global ROOT
    if "--root" in sys.argv:
        ROOT = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    if "--version" in sys.argv:
        print(f"{CHECKER_REPO} {version()}")
        return 0
    if "--coverage" in sys.argv:
        coverage()
        return 0
    if os.path.abspath(ROOT) != REPO_ROOT:
        print(f"-- {CHECKER_REPO} {version()} checking {ROOT}")
    # Said before the checks rather than after them, so that nobody reads a
    # screen of failures for a tree that owes this ecosystem nothing and draws
    # the conclusion the footing exists to refuse.
    associate = is_associate()
    if associate:
        print(f"-- this tree records the footing `{ASSOCIATE}` on {FOOTING_PAGE}: "
              "it owes this ecosystem nothing, and what follows is read against "
              "what it says there")
    failures = skipped = 0
    for title, fn, applies in CHECKS:
        why = applies() if applies else None
        if why:
            skipped += 1
            print(f"skip {title} — {why}")
            continue
        bad = fn()
        if bad:
            failures += len(bad)
            print(f"FAIL {title}")
            for b in bad:
                print(f"     {b}")
        else:
            print(f"ok   {title}")
    for title, fn, applies in MINOR:
        # Named, not swallowed. A minor check that quietly prints nothing when it
        # does not apply is indistinguishable from one that is not in the list,
        # which is the same overclaim the `skip` line exists to prevent above.
        why = applies() if applies else None
        if why:
            skipped += 1
            print(f"skip {title} — {why}")
            continue
        bad = fn()
        if bad:
            print(f"minor {title}")
            for b in bad:
                print(f"     {b}")
        else:
            print(f"ok   {title}")
    print()
    coverage()
    print()
    # **The count is reported either way and the exit code does not move.** What
    # an associate's number *means* is the shared register's call, not this
    # checker's -- it knows the footing each repository is on and prints an
    # associate's count as `tracked`. A checker that decided that for itself,
    # from a marker in the tree it is checking, would hand every repository a
    # way to turn its own build green by editing one line.
    if associate:
        print(f"-- policy: {failures} tracked, {skipped} skipped — measured "
              f"against what {FOOTING_PAGE} says this tree holds itself to. "
              "Nobody is owed this, and nobody is at fault for the number")
    else:
        print(f"-- policy: {failures} failure(s), {skipped} skipped")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
