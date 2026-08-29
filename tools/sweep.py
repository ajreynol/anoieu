#!/usr/bin/env python3
"""Run every check over a corpus of signatures, and say what came back.

Robustness first: a front end that reads the wild corpus without falling over is
what M0 is for. The counts are the second thing this says, and they are the
input to tuning a check's severity.

    python3 tools/sweep.py <dir-or-file>...
"""

from __future__ import annotations

import collections
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu.checks import Context, load_checks, run_all  # noqa: E402
from anoieu.loader import load  # noqa: E402


def files(paths: list[str]) -> list[str]:
    out: list[str] = []
    for p in paths:
        if os.path.isfile(p):
            out.append(p)
            continue
        for root, _dirs, names in os.walk(p):
            for n in sorted(names):
                if n.endswith(".eo"):
                    out.append(os.path.join(root, n))
    return out


def main() -> int:
    load_checks()
    counts: collections.Counter = collections.Counter()
    crashed: list[tuple[str, str]] = []
    read = 0
    for path in files(sys.argv[1:]):
        try:
            res = load(path)
            ctx = Context(
                signature=res.signature,
                files=res.files,
                sources=res.sources,
                root=os.path.dirname(path),
                pedantic=False,
                include_edges=res.include_edges,
            )
            diags = list(res.diagnostics) + run_all(ctx)
            read += 1
            for d in diags:
                counts[d.code] += 1
        except Exception:
            crashed.append((path, traceback.format_exc().strip().splitlines()[-1]))
    print(f"-- read {read} file(s), {len(crashed)} crash(es)")
    for code, n in sorted(counts.items()):
        print(f"   {code}  {n}")
    for path, err in crashed[:10]:
        print(f"   crash: {path}: {err}")
    return 1 if crashed else 0


if __name__ == "__main__":
    sys.exit(main())
