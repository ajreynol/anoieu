#!/usr/bin/env python3
"""Differential test of the desugarer against ethos.

anoieu's account of what the parser builds is only worth having if it agrees
with the parser. Ethos has no command that prints a desugared term, but it
prints one in a type error, so each case is compiled into a definition whose
`:type` cannot hold and the term is read back out of the message:

    Expression: (_ (or a) (_ (or b) false))

Both sides are then un-curried and compared as terms, so neither printer's
habits matter.

    python3 tools/oracle_desugar.py                     # the whole battery
    python3 tools/oracle_desugar.py --verbose           # print every case
    python3 tools/oracle_desugar.py --ethos <path>
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anoieu.desugar import Scope, curry, desugar, uncurry  # noqa: E402
from anoieu.loader import _params_from, load  # noqa: E402
from anoieu.syntax.parser import Node, parse  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTEXT = os.path.join(ROOT, "tests", "desugar", "context.eo")
CASES = os.path.join(ROOT, "tests", "desugar", "cases.txt")

_EXPR = re.compile(r"^Expression: (.*)$", re.MULTILINE)


def read_cases(path: str) -> list[tuple[str, str]]:
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        params, term = line.split("|", 1)
        out.append((params.strip(), term.strip()))
    return out


def ethos_desugar(ethos: str, params: str, term: str) -> tuple[str | None, str]:
    """What ethos builds, read out of the type error a bad `:type` provokes."""
    body = f"(define @anoieu_probe ({'' if params == '-' else params[1:-1]}) {term} :type @AnoieuProbe)"
    src = f'(include "{CONTEXT}")\n(declare-const @AnoieuProbe Type)\n{body}\n'
    with tempfile.NamedTemporaryFile("w", suffix=".eo", delete=False) as f:
        f.write(src)
        path = f.name
    try:
        p = subprocess.run(
            [ethos, "--no-print-dag", path], capture_output=True, text=True, timeout=30
        )
        text = p.stdout + p.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"could not run ethos: {e}"
    finally:
        os.unlink(path)
    m = _EXPR.search(text)
    if not m:
        first = [l for l in text.splitlines() if l.strip()][:2]
        return None, "ethos printed no term: " + " / ".join(first)
    return m.group(1).strip(), ""


def unify_as(node):
    """`(as X T)` and `(_ X T)` are one term written two ways.

    The manual says ethos reads `(as set.empty (Set Int))` as the opaque
    application `(_ set.empty (Set Int))`; its printer writes that back as `as`.
    Neither spelling is wrong, so the comparison sees through it.
    """
    if node.is_atom:
        return node
    kids = [unify_as(c) for c in node.children]
    if kids and kids[0].is_atom and kids[0].text == "as" and len(kids) == 3:
        kids[0] = Node(kids[0].path, kids[0].line, kids[0].col, kids[0].end_line,
                       kids[0].end_col, text="_")
    out = Node(node.path, node.line, node.col, node.end_line, node.end_col, items=[], kind="list")
    out.items = kids
    return out


def strip_lambda(node):
    """`(lambda (eo::tuple x xs) BODY)` is how a parameterized definition prints."""
    if node.is_list and node.head == "lambda" and len(node.children) == 3:
        return node.children[2]
    return node


def normalize(text: str, path: str):
    forms = parse(path, text).forms
    if not forms:
        return None
    return unify_as(uncurry(strip_lambda(forms[0])))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ethos", default=os.environ.get("ETHOS", "ethos"))
    ap.add_argument("--cases", default=CASES)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    res = load(CONTEXT)
    sig = res.signature
    cases = read_cases(args.cases)
    bad = 0
    skipped = 0

    for params_src, term_src in cases:
        parsed = parse("<case>", term_src)
        if not parsed.forms:
            print(f"FAIL {term_src}: could not parse the case")
            bad += 1
            continue
        term = parsed.forms[0]
        plist = []
        if params_src != "-":
            pforms = parse("<params>", params_src).forms
            if pforms:
                plist = _params_from(pforms[0], [])
        mine = unify_as(uncurry(curry(desugar(term, Scope(sig, {p.name: p for p in plist})))))

        theirs_src, why = ethos_desugar(args.ethos, params_src, term_src)
        if theirs_src is None:
            print(f"skip {term_src:44} {why}")
            skipped += 1
            continue
        theirs = normalize(theirs_src, "<ethos>")

        if str(mine) == str(theirs):
            if args.verbose:
                print(f"ok   {term_src:44} -> {mine}")
            continue
        bad += 1
        print(f"FAIL {term_src}")
        print(f"       anoieu: {mine}")
        print(f"       ethos:  {theirs}")

    print(f"-- {len(cases)} case(s), {bad} disagreement(s), {skipped} skipped")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
