#!/usr/bin/env python3
"""Check this repository against `tools/policy.md`, and say what it cannot check.

Policy is a set of claims about a *tree* — where files go, what the README ends
with, what a child project may import — so a program can decide them without
asking anybody's opinion. That is the whole reason policy is checked here and
the vision is not: see "Policy is checked; vision is argued" in
`tools/vision.md`. **Nothing in this file may ever check `vision.md`.** Whether
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
]

# Written by a run. `closed-findings.md` is deliberately absent: it is written by
# the review step and *read* by the generator, so it is a hand-maintained file.
GENERATED = ["open-findings.md", "corpus.md", "checks.md"]
INDEX_EXEMPT = {"README.md"}
COMPETING_ENTRY = ["INTRODUCTION.md", "OVERVIEW.md", "ABOUT.md", "GUIDE.md", "START.md"]


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


def sections(text: str) -> list[str]:
    return re.findall(r"^##\s+(.+?)\s*$", text, re.M)


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
    for path in tracked("docs/*.md"):
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
         "--", ":!tools/" + name, ":!docs/coherence.md", ":!tools/policy.md",
         ":!tools/vision.md"],
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


CHECKS = [
    ("the front page is the only entry point, and explains the name", check_front_page),
    ("the README ends with the maintenance note", check_maintenance_note),
    ("every document is named in the documentation index", check_docs_index),
    ("every generated document says it is generated", check_generated_labelled),
    ("dependencies are fetched and pinned, never vendored", check_dependencies),
    ("working space is untracked", check_working_space),
    ("child projects carry a charter, and name what they break", check_children),
]


def coverage() -> None:
    print("-- checked")
    for title, _ in CHECKS:
        print(f"   {title}")
    print("-- not checked, and why")
    for rule, why in UNCHECKED:
        print(f"   {rule} — {why}")
    print("-- never to be checked")
    print("   tools/vision.md, in full — judgement, and nobody has the authority")


def main() -> int:
    if "--coverage" in sys.argv:
        coverage()
        return 0
    failures = 0
    for title, fn in CHECKS:
        bad = fn()
        if bad:
            failures += len(bad)
            print(f"FAIL {title}")
            for b in bad:
                print(f"     {b}")
        else:
            print(f"ok   {title}")
    print()
    coverage()
    print()
    print(f"-- policy: {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
