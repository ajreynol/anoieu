"""Render open findings from the shared bug database as Markdown.

    python3 -m anoieu_analyzer.reporting.database          # refresh the reports
    python3 -m anoieu_analyzer.reporting.database --check  # fail if any is stale

Besides the two open reports, this refreshes the tally block in
`docs/experience.md`, which counts what each watched project has done with the
observations recorded against it.
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


#: The markers `docs/experience.md` carries around its generated tally.
TALLY_BEGIN = "<!-- tally:begin (generated by anoieu_analyzer.reporting.database) -->"
TALLY_END = "<!-- tally:end -->"

#: The tally's columns after `bugs found`: each verdict that says a closed
#: observation was a bug, in the order `bug_db/README.md` lists them, under the
#: heading a reader of the log wants.
TALLY_VERDICTS = (
    ("fixed and landed", "landed upstream"),
    ("accepted and fixed", "fixed, awaiting landing"),
    ("declined", "declined"),
    ("intentional", "intentional"),
    ("not audited", "not audited"),
)
#: Verdicts that say the observation was not a separate bug after all, so they
#: are counted beside the table rather than as bugs found.
TALLY_UNCOUNTED = ("withdrawn", "re-coded")


def credited(bug: dict, projects: list[str]) -> str:
    """The one project a closed observation counts against.

    A single owner is that project. A disagreement between two, written `a+b`,
    counts against the one whose change or ruling closed it: `closed_by` when
    the closure recorded it, and otherwise the project its landing debt, its
    pull request or its reasoning names. The two sides of a disagreement are
    never both charged with it, and never neither.
    """
    owner = bug.get("owner", "")
    sides = owner.split("+")
    if len(sides) == 1:
        return owner or "unowned"
    named = [bug.get("closed_by", ""),
             (bug.get("awaiting_landing") or {}).get("project", "")]
    named += [m.group(1) for m in re.finditer(r"github\.com/[^/\s]+/([^/\s]+)/",
                                               bug.get("closed_pr", "") + " " +
                                               bug.get("closed_commit", ""))]
    lead = re.match(r"\s*([A-Za-z0-9_-]+):", bug.get("closed_why", ""))
    named.append(lead.group(1) if lead else "")
    for name in named:
        if name in sides:
            return name
    raise ValueError(f"{bug.get('id')} is a closed {owner} disagreement that names neither "
                     f"side as the one that closed it; give it \"closed_by\"")


def tally_markdown(db: str) -> str:
    """How many bugs each watched project has had found and closed, and how.

    Only closed observations count: an open one has not been ruled on, and the
    open reports already list it. Counted from the database rather than written
    by hand, because a count in prose is the first thing a closure forgets to
    update.
    """
    with open(db, encoding="utf-8") as fh:
        bugs = [b for b in json.load(fh)["bugs"] if b.get("closed_verdict")]
    order = [d.name for d in manifest()]
    uncounted = {v: sum(1 for b in bugs if b["closed_verdict"] == v) for v in TALLY_UNCOUNTED}
    counted = [(credited(b, order), b["closed_verdict"])
               for b in bugs if b["closed_verdict"] not in TALLY_UNCOUNTED]
    projects = sorted({p for p, _ in counted},
                      key=lambda p: (order.index(p) if p in order else len(order), p))
    cols = ["project", "bugs found", *(h for _, h in TALLY_VERDICTS)]
    lines = [TALLY_BEGIN, "",
             "| " + " | ".join(cols) + " |",
             "| --- |" + " ---: |" * (len(cols) - 1)]
    total = [0] * (len(cols) - 1)
    for project in projects:
        verdict = [v for p, v in counted if p == project]
        row = [len(verdict), *(verdict.count(v) for v, _ in TALLY_VERDICTS)]
        total = [a + b for a, b in zip(total, row)]
        lines.append(f"| {cell(project)} | " + " | ".join(map(str, row)) + " |")
    lines.append("| **total** | " + " | ".join(f"**{n}**" for n in total) + " |")
    lines.extend([
        "",
        "Closed observations only, counted from [`bug_db/bugs.json`](../bug_db/bugs.json); "
        "do not edit by hand. A disagreement between two checkers counts against the one "
        "whose change or ruling closed it. *Bugs found* leaves out "
        f"{uncounted['withdrawn']} withdrawn observation(s), which were our error, and "
        f"{uncounted['re-coded']} re-coded one(s), which another entry carries.",
        "", TALLY_END])
    return "\n".join(lines)


def experience_page(db: str) -> str | None:
    """`docs/experience.md` beside the database, when the database is ours.

    Only a database at `<root>/bug_db/bugs.json` has a log to update, so a test
    rendering a scratch database never touches the real page.
    """
    directory = os.path.dirname(os.path.abspath(db))
    if os.path.basename(directory) != "bug_db":
        return None
    page = os.path.join(os.path.dirname(directory), "docs", "experience.md")
    return page if os.path.isfile(page) else None


def spliced(page: str, block: str) -> str:
    """`page` with the text between its tally markers replaced by `block`."""
    with open(page, encoding="utf-8") as fh:
        text = fh.read()
    start, end = text.find(TALLY_BEGIN), text.find(TALLY_END)
    if start < 0 or end < start:
        raise ValueError(f"{os.path.relpath(page, ROOT)} has no tally markers "
                         f"({TALLY_BEGIN} ... {TALLY_END})")
    return text[:start] + block + text[end + len(TALLY_END):]


def reports(db: str, static_page: str | None = None) -> dict[str, str]:
    directory = os.path.dirname(db)
    out = {os.path.join(directory, "bugs.md"): markdown(db),
           static_page or os.path.join(directory, "static-analysis.md"): static_markdown(db)}
    page = experience_page(db)
    if page:
        out[page] = spliced(page, tally_markdown(db))
    return out


def render(db: str, static_page: str | None = None) -> None:
    """Refresh the reports and the tally without running producers or changing the database."""
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
