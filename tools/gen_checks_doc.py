#!/usr/bin/env python3
"""Write docs/checks.md from the registry.

The manual page of a check is written beside the check, so that the two cannot
drift; this renders them into one document, which is the catalogue a reader
comes to first.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu.checks import REGISTRY, load_checks  # noqa: E402

HEADER = """# The checks

One page per check, rendered from the registry by `tools/gen_checks_doc.py`;
each page is written beside the check it explains, so the two cannot drift.
`anoieu explain <CODE>` prints the same text.

A check is `on` unless it says otherwise: the ones that are off by default are
those whose findings are a matter of taste on a signature that is already
written, and `--pedantic` turns them on.

"""


def main() -> int:
    load_checks()
    out = [HEADER]
    codes = sorted(REGISTRY)
    out.append("| code | says | default |\n| --- | --- | --- |")
    for code in codes:
        chk = REGISTRY[code]
        out.append(f"| [{code}](#{code.lower()}) | {chk.title} | {'on' if chk.default_on else 'off'} |")
    out.append("")
    for code in codes:
        chk = REGISTRY[code]
        out.append(f"## {code}\n")
        out.append(f"**{chk.title}**")
        if not chk.default_on:
            out.append("\n*Off by default; run with `--pedantic` or `--only " + code + "`.*")
        out.append("\n" + (chk.page or "(no manual page yet)") + "\n")
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "checks.md")
    with open(path, "w") as f:
        f.write("\n".join(out).rstrip() + "\n")
    print(f"-- wrote {os.path.relpath(path)} ({len(codes)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
