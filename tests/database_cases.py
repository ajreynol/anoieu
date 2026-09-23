"""Open reports exclude closures while preserving their database history."""
from __future__ import annotations

import json
import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu_analyzer.reporting import database, verdicts


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        db = Path(directory) / "bugs.json"
        closed = [
            {"id": f"closed-{tool}-{i}", "bug": f"closed-{tool}-{i}",
             "tool": tool, "code": "FUZ0002" if tool == "anoieu-fuzz" else "EO0031",
             "description": f"settled {tool} finding {i}", "closed_verdict": verdict,
             **({"awaiting_landing": {"project": "ethos", "branch": "topic",
                                      "commit": "89abcde"}}
                if verdict == "accepted and fixed" else {})}
            for tool in ("anoieu", "anoieu-fuzz", "another-producer")
            for i, verdict in enumerate(verdicts.OUTCOMES)
        ]
        bugs = [
            {"id": "static", "tool": "anoieu", "code": "EO0031", "owner": "cvc5",
             "where": "proofs/eo/a b.eo:7", "found_at": "abcdef1",
             "description": "x | y\n[link](evil) <script>",
             "first_seen": "2026-09-16", "last_seen": "2026-09-18"},
            {"id": "fuzz", "tool": "anoieu-fuzz", "code": "FUZ0002",
             "where": "tests/fuzz/crash-ethos-terminate-called-after-throwing-an-instance--fd1900/case.eo:2", "description": "crash"},
            {"id": "gone", "tool": "anoieu-fuzz", "code": "FUZ0001",
             "where": "tests/fuzz/withdrawn-and-removed/case.cpc:2",
             "description": "reproducer removed when the finding was withdrawn"},
            {"id": "old", "tool": "anoieu", "code": "EO0031", "owner": "cvc5",
             "where": "old.eo:1", "description": "record without a measured commit"},
        ] + closed
        db.write_text(json.dumps({"bugs": bugs}), encoding="utf-8")
        before = db.read_bytes()
        database.render(str(db))
        view = (Path(directory) / "bugs.md").read_text(encoding="utf-8")
        static = (Path(directory) / "static-analysis.md").read_text(encoding="utf-8")
        cases = [
            ("rendering preserves the database byte for byte", db.read_bytes() == before),
            ("both producers count only open findings",
             "[Static analyzer](#static-analyzer) | 2 |" in view
             and "[Fuzzer](#fuzzer) | 2 |" in view),
            ("every verdict, including won't fix, is excluded for every producer",
             all(b["id"] not in view and b["bug"] not in static for b in closed)
             and "Other producers" not in view),
            ("the static report counts only open static findings",
             "## Open static findings (2)" in static
             and "record without a measured commit" in static and "FUZ0002" not in static),
            ("a finding nobody has ruled on reads as open",
             "| record without a measured commit | open |" in view),
            ("hidden closures still retain their landing debt for the audit",
             len(verdicts.outstanding(str(db))) == 3),
            ("static evidence links to the measured commit and encoded source path",
             "https://github.com/cvc5/cvc5/blob/abcdef1/proofs/eo/a%20b.eo#L7" in view),
            ("fuzzer evidence links to the committed reproducer",
             "(../tests/fuzz/crash-ethos-terminate-called-after-throwing-an-instance--fd1900/case.eo#L2)" in view),
            ("and a reproducer that is no longer committed is not linked",
             "tests/fuzz/withdrawn-and-removed/case.cpc:2" in view
             and "(../tests/fuzz/withdrawn-and-removed/case.cpc" not in view),
            ("descriptions cannot break tables or introduce HTML and links",
             all("x &#124; y<br>\\[link\\](evil) &lt;script&gt;" in page
                 for page in (view, static))),
            ("unknown provenance is not replaced with a link to main",
             "| old.eo:1 |" in view and "/blob/main/" not in view),
        ]
        with patch.object(database, "DB", str(db)), contextlib.redirect_stdout(io.StringIO()):
            cases.append(("fresh reports pass the CI check", database.main(["--check"]) == 0))
            for name in ("bugs.md", "static-analysis.md"):
                page = Path(directory) / name
                page.write_text("stale report\n", encoding="utf-8")
                cases.append((f"CI detects a stale {name} without rewriting it",
                              database.main(["--check"]) == 1
                              and page.read_text(encoding="utf-8") == "stale report\n"))
                page.unlink()
                cases.append((f"CI detects a missing {name} without creating it",
                              database.main(["--check"]) == 1 and not page.exists()))
                database.main([])

            # A closure must immediately stale the existing reports, then the
            # documented command must remove it from both without a producer.
            bugs[0]["closed_verdict"] = "declined"
            bugs[1]["closed_verdict"] = "intentional"
            db.write_text(json.dumps({"bugs": bugs}), encoding="utf-8")
            after_closure = db.read_bytes()
            cases.append(("a closure makes the reports stale", database.main(["--check"]) == 1))
            database.main([])
            view = (Path(directory) / "bugs.md").read_text(encoding="utf-8")
            static = (Path(directory) / "static-analysis.md").read_text(encoding="utf-8")
            cases.append(("the closure command removes static and fuzzer rows and preserves history",
                          "| static |" not in view and "| fuzz |" not in view
                          and "proofs/eo/a b.eo" not in static
                          and "[Static analyzer](#static-analyzer) | 1 |" in view
                          and "[Fuzzer](#fuzzer) | 1 |" in view
                          and database.main(["--check"]) == 0 and db.read_bytes() == after_closure))

        for label, entries in (("all findings closed", closed), ("empty database", [])):
            db.write_text(json.dumps({"bugs": entries}), encoding="utf-8")
            database.render(str(db))
            view = (Path(directory) / "bugs.md").read_text(encoding="utf-8")
            static = (Path(directory) / "static-analysis.md").read_text(encoding="utf-8")
            cases.append((f"{label} renders explicit empty reports",
                          view.count("No open findings.") == 2
                          and "[Static analyzer](#static-analyzer) | 0 |" in view
                          and "[Fuzzer](#fuzzer) | 0 |" in view
                          and "No open findings." in static))

    # The experience log's tally is spliced in only beside a database laid out
    # as ours is, and counts per owner with withdrawn rows left out.
    with tempfile.TemporaryDirectory() as directory:
        (Path(directory) / "bug_db").mkdir()
        (Path(directory) / "docs").mkdir()
        db = Path(directory) / "bug_db" / "bugs.json"
        page = Path(directory) / "docs" / "experience.md"
        db.write_text(json.dumps({"bugs": [
            {"id": "a", "owner": "cvc5"},
            {"id": "b", "owner": "cvc5", "closed_verdict": "fixed and landed"},
            {"id": "c", "owner": "ethos", "closed_verdict": "withdrawn"},
            {"id": "d", "owner": "ethos+logos"},
            {"id": "e", "owner": "ethos+logos", "closed_verdict": "fixed and landed",
             "closed_by": "ethos"},
            {"id": "f", "owner": "ethos+logos", "closed_verdict": "declined",
             "closed_why": "logos: deliberate"},
        ]}), encoding="utf-8")
        page.write_text(f"# Log\n\n{database.TALLY_BEGIN}\nstale\n{database.TALLY_END}\n\n## E1\n",
                        encoding="utf-8")
        database.render(str(db))
        text = page.read_text(encoding="utf-8")
        cases.extend([
            ("the tally counts closed bugs only, per project",
             "| cvc5 | 1 | 1 |" in text and "stale" not in text),
            ("a closed disagreement counts against the side that closed it",
             "| ethos | 1 | 1 |" in text and "| logos | 1 | 0 | 0 | 1 |" in text
             and "+" not in text.split(database.TALLY_BEGIN)[1]),
            ("a withdrawn observation is not a bug found", "1 withdrawn" in text),
            ("the rest of the log is left alone", text.startswith("# Log\n") and text.endswith("## E1\n")),
        ])
        bugs = json.loads(db.read_text(encoding="utf-8"))["bugs"]
        bugs.append({"id": "g", "owner": "ethos+logos", "closed_verdict": "declined"})
        db.write_text(json.dumps({"bugs": bugs}), encoding="utf-8")
        try:
            database.render(str(db))
            refused = False
        except ValueError:
            refused = True
        cases.append(("a closed disagreement naming neither side is refused, not guessed", refused))
    failures = 0
    for label, passed in cases:
        print(("ok   " if passed else "FAIL ") + label)
        failures += not passed
    print(f"-- database view: {failures} failure(s)")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
