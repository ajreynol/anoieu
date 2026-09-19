"""The GitHub view must preserve data and link to the evidence it actually names."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu_analyzer.reporting import database


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        db = Path(directory) / "bugs.json"
        db.write_text(json.dumps({"bugs": [
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
            # A closure the view has to show, and the debt it must not hide.
            {"id": "landed", "tool": "anoieu", "code": "EO0031", "owner": "cvc5",
             "where": "landed.eo:1", "description": "ruled on and landed",
             "closed_verdict": "fixed and landed", "closed_on": "2026-09-19",
             "closed_commit": "0123456789abcdef0123456789abcdef01234567"},
            {"id": "pending", "tool": "anoieu", "code": "EO0031", "owner": "ethos",
             "where": "pending.eo:1", "description": "accepted, change not on main",
             "closed_verdict": "accepted and fixed", "closed_on": "2026-09-19",
             "awaiting_landing": {"project": "ethos", "branch": "topic",
                                  "commit": "89abcde"}},
        ]}), encoding="utf-8")
        before = db.read_bytes()
        database.render(str(db))
        view = (Path(directory) / "bugs.md").read_text(encoding="utf-8")
        cases = [
            ("rendering preserves the database byte for byte", db.read_bytes() == before),
            ("both producers appear with their recorded and open counts",
             "[Static analyzer](#static-analyzer) | 4 | 2 |" in view
             and "[Fuzzer](#fuzzer) | 2 | 2 |" in view),
            # The view used to render no closure at all, so every ruled-on
            # finding read as a live defect in somebody else's code.
            ("a ruled-on finding shows its verdict and links the closing commit",
             "fixed and landed ([`0123456`](https://github.com/cvc5/cvc5/commit/"
             "0123456789abcdef0123456789abcdef01234567))" in view),
            ("a finding nobody has ruled on reads as open",
             "| record without a measured commit | open |" in view),
            ("a closure whose change has not landed says so",
             "accepted and fixed<br>not landed: ethos topic" in view),
            ("static evidence links to the measured commit and encoded source path",
             "https://github.com/cvc5/cvc5/blob/abcdef1/proofs/eo/a%20b.eo#L7" in view),
            ("fuzzer evidence links to the committed reproducer",
             "(../tests/fuzz/crash-ethos-terminate-called-after-throwing-an-instance--fd1900/case.eo#L2)" in view),
            ("and a reproducer that is no longer committed is not linked",
             "tests/fuzz/withdrawn-and-removed/case.cpc:2" in view
             and "(../tests/fuzz/withdrawn-and-removed/case.cpc" not in view),
            ("descriptions cannot break tables or introduce HTML and links",
             "x &#124; y<br>\\[link\\](evil) &lt;script&gt;" in view),
            ("unknown provenance is not replaced with a link to main",
             "| old.eo:1 |" in view and "/blob/main/" not in view),
        ]
    failures = 0
    for label, passed in cases:
        print(("ok   " if passed else "FAIL ") + label)
        failures += not passed
    print(f"-- database view: {failures} failure(s)")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
