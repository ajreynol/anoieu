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

    python3 tools/policy_check.py            # check; exit 1 on any failure
    python3 tools/policy_check.py --coverage # only print what is and is not checked
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
    ("do not add a file per assistant", "a convention about what not to create"),
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
#: and is a lookup everywhere else, so it is only allowed at home.
NUMBERED = {"rule": "policy.md", "tenet": "vision.md",
            "position": "reporting-policy.md"}


def check_citations() -> list[str]:
    """*When you cite a rule from another document, say what it says*."""
    bad = []
    for rel in tracked("*.md"):
        base = os.path.basename(rel)
        text = prose(read(rel))
        for word, home in NUMBERED.items():
            if base == home:
                continue
            for m in re.finditer(rf"\b{word}s?\s(\d{{1,2}})\b", text, re.I):
                bad.append(f"{rel} cites {word} {m.group(1)} by number; say what it says")
    return bad


def check_declaration() -> list[str]:
    """*Joining the Eunoia ecosystem* — the claim the rest of this run backs.

    A declaration nothing backs is what this whole check exists to prevent, and a
    compliant tree that says nothing has not joined anything. So both, or neither.
    """
    text = read("README.md")
    if not text:
        return ["no README.md, so nothing declares membership"]
    secs = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    note = ""
    for i, m in enumerate(secs):
        if "maintain" in m.group(1).lower():
            note = text[m.end(): secs[i + 1].start() if i + 1 < len(secs) else len(text)]
    if not note:
        return ["README.md has no maintenance note to declare membership in"]
    bad = []
    if "eunoia ecosystem" not in note.lower():
        bad.append("the maintenance note does not say it is part of the Eunoia ecosystem")
    if POLICY_URL not in note or "policy.md" not in note:
        bad.append(f"the maintenance note does not link to {POLICY_URL}'s docs/policy.md")
    return bad


def check_front_page() -> list[str]:
    """*There is one entry point* and *Every repository explains its own name*."""
    bad = []
    readme = read("README.md")
    if not readme:
        return ["no README.md at the repository root"]
    for name in COMPETING_ENTRY:
        if os.path.exists(os.path.join(ROOT, name)):
            bad.append(f"{name} competes with README.md for the entry point")
    if not any("name" in s.lower() for s in sections(readme)):
        bad.append("README.md has no section explaining the repository's name")
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
    out = []
    tools = os.path.join(ROOT, "tools")
    for name in sorted(os.listdir(tools)):
        d = os.path.join(tools, name)
        if os.path.isdir(d) and not name.startswith((".", "__")) \
           and os.path.exists(os.path.join(d, "README.md")):
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
    for rel in tracked("*.md") + ["scripts/check_anoieu", "scripts/process_anoieu",
                                    "scripts/join_eo", "scripts/check_join_eo"]:
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            continue
        here = os.path.dirname(full)
        text = read(rel)
        # markdown links resolve from the file; bare `docs/...` mentions are
        # repo-relative by convention, in prose and in the prompts alike.
        targets = [(m.group(1), here) for m in re.finditer(r"\]\(([^)\s]+)\)", text)]
        targets += [(t, ROOT) for t in
                    re.findall(r"(?<![\w/`(])(docs/[\w./-]+\.(?:md|html))", text)]
        for t, base in targets:
            t = t.split("#")[0]
            if not t or t.startswith(("http", "mailto:")):
                continue
            if t.startswith("docs/"):
                base = ROOT
            if not os.path.exists(os.path.normpath(os.path.join(base, t))):
                bad.append(f"{rel} links to {t}, which does not exist")
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
    ("the front page is the only entry point, and explains the name", check_front_page, None),
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
]


# Reported, never fatal. A malformed field block is a lapse in somebody's
# correspondence rather than a defect in their tree, and failing a build over
# the shape of a sentence addressed to a colleague is the wrong instrument.
MINOR = [
    ("the discussion file is present and well-formed", check_discussion, None),
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
    if "--coverage" in sys.argv:
        coverage()
        return 0
    if os.path.abspath(ROOT) != HOME:
        print(f"-- checking {ROOT} against {POLICY_URL}'s docs/policy.md")
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
