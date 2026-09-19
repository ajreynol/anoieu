"""Render open findings from the shared bug database as Markdown.

    python3 -m anoieu_analyzer.reporting.database          # refresh both reports
    python3 -m anoieu_analyzer.reporting.database --check  # fail if either is stale
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


def open_bugs(db: str) -> list[dict]:
    """Use the same closure boundary as the closure prompt and verdict audit.

    Any recorded verdict removes the row from the open reports, including
    declined/intentional (won't fix) and fixes still awaiting landing. Keep
    those entries in the database so importing them again cannot reopen them.
    """
    with open(db, encoding="utf-8") as fh:
        return [b for b in json.load(fh)["bugs"] if "closed_verdict" not in b]


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
    bugs = open_bugs(db)
    repositories = {d.name: d.url.removesuffix(".git") for d in manifest()}
    groups = [
        ("Static analyzer", [b for b in bugs if b.get("tool") == "anoieu"]),
        ("Fuzzer", [b for b in bugs if b.get("tool") == "anoieu-fuzz"]),
    ]
    other = [b for b in bugs if b.get("tool") not in {"anoieu", "anoieu-fuzz"}]
    if other:
        groups.append(("Other producers", other))
    lines = [
        "# Open bugs", "",
        "Generated from [bugs.json](bugs.json) by `anoieu_analyzer.reporting.database`.",
        "Do not edit this view by hand. [Update instructions](README.md).", "",
        "Only open findings appear here. Entries carrying a `closed_verdict`,",
        "including declined and intentional (won't fix) findings, are omitted.",
        "The complete history and closure reasoning remain in [bugs.json](bugs.json).",
        "See [Closure](README.md#closure) for the verdicts and the separate audit",
        "of fixes awaiting landing. Open means nobody has ruled, not that a check",
        "was re-run. Dates record ingestion, not fresh reproduction. Static evidence",
        "links use the originally recorded source commit; fuzzer links open the",
        "committed reproducers.", "",
        "| Producer | Open findings |", "| --- | ---: |",
    ]
    for title, entries in groups:
        anchor = title.lower().replace(" ", "-")
        lines.append(f"| [{title}](#{anchor}) | {len(entries)} |")
    for title, entries in groups:
        lines.extend(["", f"## {title}", ""])
        if not entries:
            lines.append("No open findings.")
            continue
        lines.extend([
                      "| ID | Check | Owner | Finding | Status | Evidence | First ingested | Last ingested |",
                      "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for bug in entries:
            code = bug.get("code", "")
            guide = ("../anoieu_fuzz/fuzzing.md#the-codes" if code.startswith("FUZ")
                     else "../anoieu_analyzer/checks.md#" + quote(code.lower()))
            fields = [cell(bug.get("id", bug.get("bug", ""))),
                      f"[{cell(code)}]({guide})" if code else "—",
                      cell(bug.get("owner", "")), cell(bug.get("description", "")),
                      "open",
                      evidence(bug, repositories), cell(bug.get("first_seen", "")),
                      cell(bug.get("last_seen", ""))]
            lines.append("| " + " | ".join(fields) + " |")
    return "\n".join(lines) + "\n"


def static_markdown(db: str) -> str:
    """The static subset uses the same open findings as the combined report."""
    bugs = [b for b in open_bugs(db) if not b.get("code", "").startswith("FUZ")]
    cols = ("bug", "owner", "code", "where", "description", "status",
            "first seen", "last seen")
    lines = [
        "# Open static analysis findings", "",
        "Generated from [bugs.json](bugs.json) by `anoieu_analyzer.reporting.database`.",
        "Do not edit this view by hand. [Update instructions](README.md).", "",
        "Only static findings without a `closed_verdict` appear here. Closed findings,",
        "including declined and intentional (won't fix) findings, remain in",
        "[bugs.json](bugs.json) with their verdicts, evidence and ingestion dates.",
        "[bugs.md](bugs.md) includes open findings from both the analyzer and fuzzer.",
        "Open means nobody has ruled; ingestion dates do not imply a fresh reproduction.",
        "See [Closure](README.md#closure) for the verdicts and the separate audit",
        "of fixes awaiting landing.", "",
        f"## Open static findings ({len(bugs)})", "",
    ]
    if not bugs:
        return "\n".join(lines + ["No open findings."]) + "\n"
    lines.extend(["| " + " | ".join(cols) + " |",
                  "| " + " | ".join("---" for _ in cols) + " |"])
    for b in bugs:
        fields = [b.get("bug", ""), b.get("owner", ""), b.get("code", ""),
                  b.get("where", ""), b.get("description", ""), "open",
                  b.get("first_seen", ""), b.get("last_seen", "")]
        lines.append("| " + " | ".join(cell(value) for value in fields) + " |")
    return "\n".join(lines) + "\n"


def reports(db: str, static_page: str | None = None) -> dict[str, str]:
    directory = os.path.dirname(db)
    return {os.path.join(directory, "bugs.md"): markdown(db),
            static_page or os.path.join(directory, "static-analysis.md"): static_markdown(db)}


def render(db: str, static_page: str | None = None) -> None:
    """Refresh both reports without running producers or changing the database."""
    for page, text in reports(db, static_page).items():
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check without rewriting")
    args = parser.parse_args(argv)
    stale = False
    for page, text in reports(DB).items():
        label = os.path.relpath(page, ROOT)
        if args.check:
            current = ""
            if os.path.isfile(page):
                with open(page, encoding="utf-8") as fh:
                    current = fh.read()
            if current != text:
                print(f"{label} is stale; run python3 -m anoieu_analyzer.reporting.database")
                stale = True
            else:
                print(f"{label} is current")
        else:
            with open(page, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"wrote {label}")
    return int(stale)


if __name__ == "__main__":
    raise SystemExit(main())
