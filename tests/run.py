#!/usr/bin/env python3
"""The witness suite.

Every check owns a pair of files: one the check must report, and (where the
distinction is interesting) one it must stay quiet about. The `; expect:` line
at the top of a witness says which codes the file is for, so the suite is
readable as a specification of what each check means -- which is the point of
writing witnesses rather than assertions.

    python3 tests/run.py            # run every witness
    python3 tests/run.py --oracle   # also ask ethos what it says about each
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anoieu.checks import REGISTRY, Context, load_checks, run_all  # noqa: E402
from anoieu.loader import load  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WITNESSES = os.path.join(HERE, "witnesses")


def expected(path: str) -> set[str]:
    with open(path) as f:
        for line in f:
            if line.startswith("; expect:"):
                return {c.strip() for c in line.split(":", 1)[1].split() if c.strip()}
    return set()


def run_one(path: str, want: set[str]) -> set[str]:
    load_checks()
    res = load(path)
    ctx = Context(
        signature=res.signature,
        files=res.files,
        sources=res.sources,
        root=os.path.dirname(path),
        pedantic=True,
        include_edges=res.include_edges,
    )
    got = {d.code for d in list(res.diagnostics) + run_all(ctx)}
    # the checks that are off by default are only asked about when a witness
    # says it is for one of them
    off = {code for code, chk in REGISTRY.items() if not chk.default_on}
    return {c for c in got if c not in off or c in want}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle", action="store_true",
                    help="also ask ethos about each witness, and run the desugaring battery")
    ap.add_argument("--ethos", default=os.environ.get("ETHOS", "ethos"))
    args = ap.parse_args()

    failures = 0
    for name in sorted(os.listdir(WITNESSES)):
        if not name.endswith(".eo"):
            continue
        path = os.path.join(WITNESSES, name)
        want = expected(path)
        got = run_one(path, want)
        ok = want <= got and (want or not got)
        status = "ok  " if ok else "FAIL"
        if not ok:
            failures += 1
        extra = sorted(got - want)
        line = f"{status} {name:22} expected {sorted(want) or '(nothing)'}"
        if extra:
            line += f"  also reported {extra}"
        print(line)
        if args.oracle:
            try:
                p = subprocess.run(
                    [args.ethos, path], capture_output=True, text=True, timeout=30
                )
                text = (p.stdout + p.stderr).strip()
                lines = text.splitlines()
                if p.returncode == 0 and "correct" in text:
                    verdict = "correct" + (
                        f"  (with a warning: {lines[0][:60]})" if len(lines) > 1 else ""
                    )
                else:
                    err = next((l for l in lines if l.startswith("Error:")), lines[0] if lines else "")
                    verdict = f"refused -- {err[:90]}"
            except (OSError, subprocess.TimeoutExpired) as e:
                verdict = f"(not run: {e})"
            print(f"     ethos: {verdict}")
    print(f"-- witnesses: {failures} failure(s)")

    sys.stdout.flush()
    print()
    import cli_cases  # noqa: PLC0415

    failures += cli_cases.main()

    if args.oracle:
        print()
        sys.stdout.flush()
        import subprocess as sp  # noqa: PLC0415

        oracle = os.path.join(os.path.dirname(HERE), "tools", "oracle_desugar.py")
        p = sp.run([sys.executable, oracle, "--ethos", args.ethos], text=True)
        failures += 1 if p.returncode else 0

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
