#!/usr/bin/env python3
"""The id of a finding, computed the way the checks compute it.

Two producers write the findings record -- `scripts/anoieu_analyzer`, which
is the checks, and an agent driven by `prompts/anoieu_analyzer_agent`. They are
compared **per id**, so an agent that invents its own ids is not comparable with
the program at all, however good its reading of the file was.

So this is the one piece of arithmetic both producers share:

    python3 -m anoieu.reporting.finding_id EO0031 proofs/eo/cpc/Cpc.eo 17
    python3 -m anoieu.reporting.finding_id EO0031 proofs/eo/cpc/Cpc.eo --line '(declare-const x Int)'

Given a path that exists, it reads the line itself; given `--line` it takes the
text as handed. The path is **relative to the owner's tree**, not to this one.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import ROOT


from anoieu.fingerprint import id_of  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("code", help="the check code, e.g. EO0031")
    ap.add_argument("where", help="the path inside the owner's tree")
    ap.add_argument("line", nargs="?", type=int, help="the line number")
    ap.add_argument("--line", dest="text", help="the text of the line, if the file is not here")
    ap.add_argument("--root", default="", help="where the owner's tree is, to read the line from")
    args = ap.parse_args()

    text = args.text
    if text is None:
        if args.line is None:
            print("give a line number, or --line with the text of the line", file=sys.stderr)
            return 2
        path = os.path.join(args.root, args.where) if args.root else args.where
        if not os.path.isfile(path):
            print(f"{path}: no such file; pass --root, or --line with the text",
                  file=sys.stderr)
            return 2
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        if not 1 <= args.line <= len(lines):
            print(f"{path}: has no line {args.line}", file=sys.stderr)
            return 2
        text = lines[args.line - 1]

    print(id_of(args.code, args.where, text.strip()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
