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


def evidence(bug: dict, repositories: dict[str, str]) -> str:
    location = bug.get("where", "")
    path, sep, line = location.rpartition(":")
    if not sep or not line.isdigit():
        path, line = location, ""
    anchor = f"#L{line}" if line else ""
    if bug.get("tool") == "anoieu-fuzz" and path.startswith("tests/fuzz/"):
        # Only repository-relative, committed reproducer locations are links.
        if ".." not in path.split("/"):
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
        "This is the history of recorded findings, including resolved ones; it does",
        "not assign open/closed status. Dates record ingestion, not fresh reproduction.",
        "Static evidence links use the originally recorded source commit. Fuzzer links",
        "open the committed reproducers. Verdicts remain in the",
        "[findings ledgers](../docs/reports/open-findings.md).", "",
        "| Producer | Recorded findings |", "| --- | ---: |",
    ]
    for title, entries in groups:
        anchor = title.lower().replace(" ", "-")
        lines.append(f"| [{title}](#{anchor}) | {len(entries)} |")
    for title, entries in groups:
        lines.extend(["", f"## {title}", "",
                      "| ID | Check | Owner | Finding | Evidence | First ingested | Last ingested |",
                      "| --- | --- | --- | --- | --- | --- | --- |"])
        for bug in entries:
            code = bug.get("code", "")
            guide = ("../docs/fuzzing.md#the-codes" if code.startswith("FUZ")
                     else "../docs/checks.md#" + quote(code.lower()))
            fields = [cell(bug.get("id", bug.get("bug", ""))),
                      f"[{cell(code)}]({guide})" if code else "—",
                      cell(bug.get("owner", "")), cell(bug.get("description", "")),
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
