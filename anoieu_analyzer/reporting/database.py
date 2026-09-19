"""Render the shared bug database as Markdown for GitHub browsing.

    python3 -m anoieu_analyzer.reporting.database          # refresh the view
    python3 -m anoieu_analyzer.reporting.database --check  # fail if the view is stale
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
from urllib.parse import quote

from . import ROOT
from .deps import manifest

DB = os.path.join(ROOT, "bug_db", "bugs.json")


def cell(value: object) -> str:
    """Render evidence as text, without letting it change the Markdown table."""
    text = html.escape(str(value), quote=False).replace("\\", "\\\\")
    for char in "`*_[]":
        text = text.replace(char, "\\" + char)
    return text.replace("|", "&#124;").replace("\r", "").replace("\n", "<br>")


def status(bug: dict, repositories: dict[str, str]) -> str:
    """What has been decided about a finding, and what backs the decision.

    **A view that shows only the claim overstates what is outstanding.** This
    page is what `README.md` points a reader at, and until 2026-09-19 it rendered
    no closure at all: 68 of 82 findings had been ruled on and every row read
    like a live defect in somebody else's code. The verdict is the column that
    makes the count honest.

    The verdict itself is the whole of the status -- `bug_db/README.md` defines
    the seven words -- and what is added here is the evidence: the pull request
    or commit it closed on, and, for `accepted and fixed`, that the change has
    not reached the project's default branch yet. That last one is the debt
    `awaiting_landing` records and `verdicts.py` audits; a row that hid it would
    read as finished.
    """
    verdict = bug.get("closed_verdict", "")
    if not verdict:
        return "open"
    text = cell(verdict)
    pr = bug.get("closed_pr", "")
    commit = bug.get("closed_commit", "")
    repo = repositories.get(bug.get("owner", ""), "")
    if pr.startswith("https://"):
        text += f" ([pull request]({pr}))"
    elif repo and re.fullmatch(r"[0-9a-f]{7,40}", commit):
        text += f" ([`{commit[:7]}`]({repo}/commit/{commit}))"
    elif commit:
        text += f" (`{cell(commit[:7])}`)"
    landing = bug.get("awaiting_landing") or {}
    if landing:
        where = " ".join(str(landing.get(k, "")) for k in ("project", "branch") if landing.get(k))
        text += f"<br>not landed: {cell(where)}" if where else "<br>not landed"
    return text


def evidence(bug: dict, repositories: dict[str, str]) -> str:
    location = bug.get("where", "")
    path, sep, line = location.rpartition(":")
    if not sep or not line.isdigit():
        path, line = location, ""
    anchor = f"#L{line}" if line else ""
    if bug.get("tool") == "anoieu-fuzz" and path.startswith("tests/fuzz/"):
        # Only repository-relative, committed reproducer locations are links. A
        # withdrawn finding keeps its recorded location and loses its
        # reproducer, and a link to a file nobody can open is worse than none.
        if ".." not in path.split("/") and os.path.exists(os.path.join(ROOT, path)):
            return f"[{cell(location)}](../{quote(path)}{anchor})"
    repo = repositories.get(bug.get("owner", ""), "")
    commit = bug.get("found_at", "")
    if repo and path and re.fullmatch(r"[0-9a-f]{7,40}", commit):
        url = f"{repo}/blob/{commit}/{quote(path)}{anchor}"
        return f"[{cell(location)}]({url})"
    return cell(location) or "—"


def markdown(db: str) -> str:
    with open(db, encoding="utf-8") as fh:
        bugs = json.load(fh)["bugs"]
    repositories = {d.name: d.url.removesuffix(".git") for d in manifest()}
    groups = [
        ("Static analyzer", [b for b in bugs if b.get("tool") == "anoieu"]),
        ("Fuzzer", [b for b in bugs if b.get("tool") == "anoieu-fuzz"]),
    ]
    other = [b for b in bugs if b.get("tool") not in {"anoieu", "anoieu-fuzz"}]
    if other:
        groups.append(("Other producers", other))
    lines = [
        "# Bug database", "",
        "Generated from [bugs.json](bugs.json) by `anoieu_analyzer.reporting.database`.",
        "Do not edit this view by hand. [Update instructions](README.md).", "",
        "This is the history of recorded findings, including the ones that have been",
        "ruled on. **Status** is the verdict written onto the entry, or `open` where",
        "there is none; the seven verdicts and what each requires are defined under",
        "[Closure](README.md#closure). A verdict is a judgement recorded against a",
        "named commit, so `open` means nobody has ruled, never that a check was",
        "re-run. Dates record ingestion, not fresh reproduction. Static evidence",
        "links use the originally recorded source commit; fuzzer links open the",
        "committed reproducers. The reasoning behind a verdict is `closed_why` in",
        "the [database itself](bugs.json), and what a change meant is",
        "[experience.md](../docs/experience.md).", "",
        "| Producer | Recorded findings | Open |", "| --- | ---: | ---: |",
    ]
    for title, entries in groups:
        anchor = title.lower().replace(" ", "-")
        open_count = sum(1 for b in entries if not b.get("closed_verdict"))
        lines.append(f"| [{title}](#{anchor}) | {len(entries)} | {open_count} |")
    for title, entries in groups:
        lines.extend(["", f"## {title}", "",
                      "| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |",
                      "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for bug in entries:
            code = bug.get("code", "")
            guide = ("../docs/fuzzing.md#the-codes" if code.startswith("FUZ")
                     else "../docs/checks.md#" + quote(code.lower()))
            fields = [cell(bug.get("id", bug.get("bug", ""))),
                      f"[{cell(code)}]({guide})" if code else "—",
                      cell(bug.get("owner", "")), cell(bug.get("description", "")),
                      status(bug, repositories),
                      evidence(bug, repositories), cell(bug.get("first_seen", "")),
                      cell(bug.get("last_seen", ""))]
            lines.append("| " + " | ".join(fields) + " |")
    return "\n".join(lines) + "\n"


def render(db: str) -> None:
    """Write the browsing view beside the database that was actually updated."""
    page = os.path.join(os.path.dirname(db), "bugs.md")
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(markdown(db))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check without rewriting")
    args = parser.parse_args()
    if args.check:
        page = os.path.join(os.path.dirname(DB), "bugs.md")
        current = open(page, encoding="utf-8").read() if os.path.isfile(page) else ""
        if current != markdown(DB):
            print("bug_db/bugs.md is stale; run python3 -m anoieu_analyzer.reporting.database")
            return 1
        print("bug_db/bugs.md is current")
    else:
        render(DB)
        print("wrote bug_db/bugs.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
