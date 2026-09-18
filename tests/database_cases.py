"""The GitHub view must preserve data and link to the evidence it actually names."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu.reporting import database


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        db = Path(directory) / "bugs.json"
        db.write_text(json.dumps({"bugs": [
            {"id": "static", "tool": "anoieu", "code": "EO0031", "owner": "cvc5",
             "where": "proofs/eo/a b.eo:7", "found_at": "abcdef1",
             "description": "x | y\n[link](evil) <script>",
             "first_seen": "2026-09-16", "last_seen": "2026-09-18"},
            {"id": "fuzz", "tool": "anoieu-fuzz", "code": "FUZ0002",
             "where": "tests/fuzz/example/case.eo:2", "description": "crash"},
            {"id": "old", "tool": "anoieu", "code": "EO0031", "owner": "cvc5",
             "where": "old.eo:1", "description": "record without a measured commit"},
        ]}), encoding="utf-8")
        before = db.read_bytes()
        database.render(str(db))
        view = (Path(directory) / "bugs.md").read_text(encoding="utf-8")
        cases = [
            ("rendering preserves the database byte for byte", db.read_bytes() == before),
            ("both producers appear with their recorded counts",
             "[Static analyzer](#static-analyzer) | 2" in view
             and "[Fuzzer](#fuzzer) | 1" in view),
            ("static evidence links to the measured commit and encoded source path",
             "https://github.com/cvc5/cvc5/blob/abcdef1/proofs/eo/a%20b.eo#L7" in view),
            ("fuzzer evidence links to the committed reproducer",
             "(../tests/fuzz/example/case.eo#L2)" in view),
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
