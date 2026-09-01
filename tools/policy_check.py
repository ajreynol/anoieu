#!/usr/bin/env python3
"""Check this repository against `docs/policy.md`, and say what it cannot check.

Policy is a set of claims about a *tree* — where files go, what the README ends
with, what a child project may import — so a program can decide them without
asking anybody's opinion. That is the whole reason policy is checked here and
the vision is not: see "Policy is checked; vision is argued" in
`docs/vision.md`. **Nothing in this file may ever check `vision.md`.** Whether
a tool is fruitful yet, whether a claim is oversold, whether a child project has
earned its keep — those are judgements nobody has the authority to settle, and a
green tick against one would manufacture an authority that does not exist.

Each check names the rule or convention it implements, so a failure is traceable
to a sentence somebody wrote. The run also prints every policy rule that has
**no** automated check, because a checker that only lists its own passes reads
as coverage it does not have.

    python3 tools/policy_check.py             # check; exit 1 on any failure
    python3 tools/policy_check.py --root PATH # check somebody else's checkout
    python3 tools/policy_check.py --coverage  # what is checked, and what is not
    python3 tools/policy_check.py --version   # which commit of the policy this is
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: The repository under test. `--root` points it at somebody else's checkout;
#: `HOME` stays this one, because a few checks are about anoieu's own files.
ROOT = HOME
POLICY_URL = "ajreynol/anoieu"

# Rules with no automated check, and the honest reason. Printed on every run.
UNCHECKED = [
    ("rule 1, a human starts one", "intent; no artifact records who asked"),
    ("rule 6, additive never authoritative", "a claim about tone, not about the tree"),
    ("rule 7, nothing leaves the island by machine", "absence of an action cannot be observed here"),
    ("rule 8, it cites what it inherited", "whether a citation supports its claim is reading"),
    ("rule 9, it ends with a verdict", "'has gone quiet' is a judgement about elapsed time"),
    ("the maintenance note carries no technical detail", "what counts as technical is editorial"),
    ("`tools/` is the harness, not the product", "no mechanical test separates the two"),
    ("`tests/` holds the evidence, not only the tests", "readability in a minute is not measurable"),
    ("a workflow is defined in prose", "checked elsewhere: `prompts_agree` in tests/run.py"),
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
]

# Written by a run. `closed-findings.md` is deliberately absent: it is written by
# the review step and *read* by the generator, so it is a hand-maintained file.
GENERATED = ["reports/open-findings.md", "reports/corpus.md", "checks.md"]
INDEX_EXEMPT = {"README.md"}
COMPETING_ENTRY = ["INTRODUCTION.md", "OVERVIEW.md", "ABOUT.md", "GUIDE.md", "START.md"]

KINDS = {"request", "proposal", "question", "notice", "answer"}
STATES = {"open", "answered", "declined", "withdrawn", "settled"}
FIELDS = ["To", "Kind", "Status", "Opened", "Settles when"]

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


def version() -> str:
    """The commit of *this checker*, so a build log records what it was checked
    against. A member pins a commit; the run should say which one it got."""
    out = subprocess.run(["git", "-C", HOME, "rev-parse", "--short", "HEAD"],
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


def maintenance_note(text: str) -> str:
    """The body of the README's maintenance note, or "" if there is none.

    Shared by the two readers below, because a footing that makes a claim about
    somebody's tree should be decided by reading that tree, and both of them read
    the same section of it.
    """
    secs = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
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
    of the tree — see *The associate protocol* in `docs/policy.md`, which says
    what is still undecided and what would settle it.

    Read for a **report** and never for a verdict. Nothing in `CHECKS` calls it,
    nothing fails on it, and the repositories it is asked about are held to none
    of this. `tools/ecosystem.py --protocol` is what runs it, so that a person
    deciding the protocol can see who would satisfy which version of it today.
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

    Split out from the check below because a second reader wants the same
    answer from text it did not read off this disk: `tools/ecosystem.py --check
    --online` asks it of a README fetched from a remote, to decide whether the
    inventory's record of who has joined is still true. One implementation, so
    the two cannot come to different answers about the same file.
    """
    if not text:
        return ["no README.md, so nothing declares membership"]
    note = maintenance_note(text)
    if not note:
        return ["README.md has no maintenance note to declare membership in"]
    bad = []
    low = note.lower()
    if "eunoia ecosystem" not in low:
        bad.append("the maintenance note does not say it is part of the Eunoia ecosystem")
    if POLICY_URL not in note or "policy.md" not in note:
        bad.append(f"the maintenance note does not link to {POLICY_URL}'s docs/policy.md")
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

    The note an `associate` in `tools/ecosystem.json` carries: it names the
    ecosystem it works with, and it says it is not held to the policy. Read from
    a fetched README by `tools/ecosystem.py --check --online`, exactly as
    `declaration_in` is for a member -- so both footings that assert something
    about somebody else's tree are decided by reading that tree.

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


def check_declaration() -> list[str]:
    """*Joining the Eunoia ecosystem* — the claim the rest of this run backs.

    A declaration nothing backs is what this whole check exists to prevent, and a
    compliant tree that says nothing has not joined anything. So both, or neither.
    """
    return declaration_in(read("README.md"))


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
    """
    readme = read("README.md")
    if readme and not any("name" in s.lower() for s in sections(readme)):
        return ["README.md has no section explaining the repository's name"]
    return []


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
        if base in INDEX_EXEMPT:
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
    for rel in ("tools/deps.json", "tools/deps.lock"):
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
        if breaks and "rule 10" not in low:
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
    for rel in tracked("*.md") + ["scripts/prompts/check_anoieu", "scripts/prompts/process_anoieu",
                                    "scripts/prompts/join_eo", "scripts/prompts/check_join_eo",
                                    "scripts/prompts/process_discussion", "scripts/prompts/init_eo",
                                    "scripts/prompts/global_audit", "scripts/prompts/welcome_eo"]:
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
    """
    bad = []
    for rel in tracked("*.md"):
        for m in re.finditer(r"(?<![\w/])(/home/[\w.-]+|/Users/[\w.-]+)/",
                             prose(read(rel))):
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
    """Every command in `scripts/` appears in the table that lists them.

    The cheapest kind of check: its input is the tree, so it cannot rot, and the
    thing it prevents is the one that actually happened repeatedly -- a script
    added and documented in a sentence somewhere, until the sentences were the
    documentation.
    """
    table = read("docs/coherence.md")
    if not table:
        return []
    bad = []
    for rel in tracked("scripts/*"):
        name = os.path.basename(rel)
        if name.endswith(".local") or f"`{name}" in table:
            continue
        bad.append(f"scripts/{name} is not in the table in docs/coherence.md")
    return bad


def check_response_gate() -> list[str]:
    """*Responding to somebody else's discussion file* — the protocol's safety rule.

    A build failure rather than a minor finding: it is the only thing in the file
    that stops an agent acting on correspondence nobody asked it to act on, and a
    safety rule that degrades to a warning is one that is eventually ignored.
    """
    text = read("docs/discussion.md")
    if not text:
        return ["docs/discussion.md does not exist, so it carries no response gate"]
    first_topic = re.search(r"^##\s+D\d+\s", text, re.M)
    head = text[: first_topic.start()] if first_topic else text
    if "&gt;" not in head and not re.search(r"^>", head, re.M):
        return ["docs/discussion.md has no banner block above its first topic"]
    low = head.lower()
    bad = [f"the banner does not state {what}"
           for what, forms in BANNER if not any(f in low for f in forms)]
    return bad


def check_discussion() -> list[str]:
    """*The discussion file* — reported as minor, never as a build failure."""
    text = read("docs/discussion.md")
    if not text:
        return ["docs/discussion.md does not exist: no standing channel to the ecosystem"]
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
        block = "\n".join(lines[i + 1:i + 9])
        got = dict(re.findall(r"^\*\*([A-Za-z ]+):\*\*\s*(.*)$", block, re.M))
        for f in FIELDS:
            if f not in got or not got[f].strip():
                bad.append(f"{tid} has no **{f}:**")
        if got.get("To", "").strip().lower() in {"", "upstream", "the ecosystem", "everyone"}:
            bad.append(f"{tid} does not name the tool it addresses unequivocally")
        kind = got.get("Kind", "").strip()
        if kind and kind not in KINDS:
            bad.append(f"{tid} has Kind {kind!r}, not one of {'/'.join(sorted(KINDS))}")
        state = got.get("Status", "").strip()
        if state and state not in STATES:
            bad.append(f"{tid} has Status {state!r}, not one of {'/'.join(sorted(STATES))}")
    if not seen:
        bad.append("docs/discussion.md carries no topics")
    return bad


def has(*rel):
    """Applicability: the check runs only where the thing it is about exists."""
    def applies():
        for r in rel:
            if os.path.exists(os.path.join(ROOT, r)):
                return None
        return "nothing at " + " or ".join(rel)
    return applies


def is_home():
    return None if os.path.abspath(ROOT) == HOME else "specific to anoieu's own files"


# (title, check, applies). A check that does not apply is skipped and named:
# passing must never read as more coverage than it was. The set is deliberately
# small and is expected to grow.
CHECKS = [
    ("the README declares membership of the ecosystem", check_declaration, None),
    ("the front page is the only entry point", check_front_page, None),
    ("the README ends with the maintenance note", check_maintenance_note, None),
    ("every document is named in the documentation index", check_docs_index, has("docs")),
    ("every generated document says it is generated", check_generated_labelled, is_home),
    ("dependencies are fetched and pinned, never vendored", check_dependencies, has("deps", "tools/deps.json")),
    ("working space is untracked", check_working_space, has(".gitignore")),
    ("child projects carry a charter, and name what they break", check_children, has("tools")),
    ("the discussion file carries the response gate, at the top", check_response_gate, None),
    ("every link in a document or an outbound prompt resolves", check_links, None),
    ("no document names a specific AI", check_no_vendor, None),
    ("no document cites another document's rule by number", check_citations, None),
    ("every link to a heading finds one", check_anchors, None),
    ("no document names one machine's filesystem", check_local_paths, None),
    ("the membership declaration opens the maintenance note", check_declaration_first, None),
    ("every script is listed where the scripts are listed", check_scripts_listed, is_home),
]


# Reported, never fatal. A malformed field block is a lapse in somebody's
# correspondence rather than a defect in their tree, and failing a build over
# the shape of a sentence addressed to a colleague is the wrong instrument.
MINOR = [
    ("the discussion file is present and well-formed", check_discussion, None),
    ("the README explains the repository's name", check_name_explained, None),
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
    print("   docs/vision.md, in full — judgement, and nobody has the authority")


def main() -> int:
    global ROOT
    if "--root" in sys.argv:
        ROOT = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    if "--version" in sys.argv:
        print(f"{POLICY_URL} {version()}")
        return 0
    if "--coverage" in sys.argv:
        coverage()
        return 0
    if os.path.abspath(ROOT) != HOME:
        print(f"-- {POLICY_URL} {version()} checking {ROOT}")
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
        if applies and applies():
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
    print(f"-- policy: {failures} failure(s), {skipped} skipped")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
