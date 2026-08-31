#!/usr/bin/env python3
"""The witness suite.

Every check owns a pair of files: one the check must report, and (where the
distinction is interesting) one it must stay quiet about. The `; expect:` line
at the top of a witness says which codes the file is for, so the suite is
readable as a specification of what each check means -- which is the point of
writing witnesses rather than assertions.

    python3 tests/run.py            # run every witness
    python3 tests/run.py --oracle   # also ask ethos what it says about each

It also runs `cli_cases.py` -- what a *run* does with the findings -- and
`fuzz_cases.py`, the harness of the fuzzer, whose checkers are written in the
suite so that neither ethos nor logos has to be on the machine.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anoieu.checks import REGISTRY, Context, load_checks, run_all  # noqa: E402
from anoieu.cli import _embedding_vocabulary  # noqa: E402
from anoieu.loader import load  # noqa: E402
from anoieu.semantics import load_set  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WITNESSES = os.path.join(HERE, "witnesses")


ORACLE = os.path.join(HERE, "oracle.json")


def ethos_verdict(binary: str, path: str) -> dict:
    """What ethos says about one witness, reduced to what is stable across
    machines: whether it accepted the file, and the first line of any complaint
    with absolute paths stripped out."""
    try:
        p = subprocess.run([binary, path], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"verdict": "not run", "detail": str(e)[:80]}
    text = (p.stdout + p.stderr).strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if p.returncode == 0 and "correct" in text:
        note = lines[0] if len(lines) > 1 else ""
        return {"verdict": "accepted", "detail": _portable(note)}
    err = next((l for l in lines if l.startswith("Error:")), lines[0] if lines else "")
    return {"verdict": "refused", "detail": _portable(err)}


def _portable(line: str) -> str:
    """Drop anything that is about this machine rather than about the file."""
    line = re.sub(r"(/[^\s:]+)+/(?=[\w.-]+\.eo)", "", line)
    return line[:120]


def expected(path: str) -> set[str]:
    with open(path) as f:
        for line in f:
            if line.startswith("; expect:"):
                return {c.strip() for c in line.split(":", 1)[1].split() if c.strip()}
    return set()


def run_one(path: str, want: set[str]) -> set[str]:
    """A witness is a signature, and — for the checks over a triple — whichever
    of its companions exist: `X.eos` is its semantics, `X.smt.eos` the SMT
    semantics it is written against, `X.embed.eo` the deep embedding."""
    load_checks()
    res = load(path)
    stem = path[: -len(".eo")]
    companion = lambda suffix: stem + suffix if os.path.isfile(stem + suffix) else None
    sem = companion(".eos")
    smt = companion(".smt.eos")
    embed = companion(".embed.eo")
    ctx = Context(
        signature=res.signature,
        files=res.files,
        sources=res.sources,
        root=os.path.dirname(path),
        pedantic=True,
        include_edges=res.include_edges,
        semantics=load_set(sem) if sem else None,
        smt_semantics=load_set(smt) if smt else None,
        embedding_names=_embedding_vocabulary(embed) if embed else set(),
    )
    got = {d.code for d in list(res.diagnostics) + run_all(ctx)}
    # the checks that are off by default are only asked about when a witness
    # says it is for one of them
    off = {code for code, chk in REGISTRY.items() if not chk.default_on}
    return {c for c in got if c not in off or c in want}


def witness_coverage() -> None:
    """Which checks own a witness, and which do not.

    Printed rather than enforced: a check without one is a gap to fill, not a
    regression, and a suite that fails on it would be red for as long as the gap
    exists — which is how a number stops being read. Saying it every run is what
    keeps it from drifting quietly.
    """
    from anoieu.checks import REGISTRY  # noqa: PLC0415

    load_checks()
    covered: set[str] = set()
    for name in os.listdir(WITNESSES):
        if name.endswith(".eo"):
            covered |= expected(os.path.join(WITNESSES, name))
    missing = sorted(set(REGISTRY) - covered)
    print(f"-- {len(REGISTRY) - len(missing)} of {len(REGISTRY)} checks own a witness")
    if missing:
        print(f"   without one: {' '.join(missing)}")


def manifest_agrees() -> int:
    """The sources the report is generated from are named in three places —
    `tools/deps.json`, the targets in `tools/gen_corpus_table.py`, and the lock
    a run writes. A name that appears in one and not the others makes a corpus
    silently unmeasured, which reads exactly like a corpus with no findings. So
    check it here, where no network is needed."""
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
    import deps  # noqa: PLC0415
    import gen_corpus_table as corpus  # noqa: PLC0415

    failures = 0
    named = {d.name for d in deps.manifest()}
    for label, repo, rels, triple in corpus.TARGETS:
        wanted = {repo} | ({r for r, _ in triple.values()} if triple else set())
        missing = wanted - named
        if missing:
            print(f"FAIL {label}: no such project in deps.json: {sorted(missing)}")
            failures += 1
    for d in deps.manifest():
        if not d.paths:
            print(f"FAIL {d.name}: no paths, so a clone of it would be empty")
            failures += 1
        if any(os.path.splitext(p)[1] for p in d.paths):
            # cone-mode sparse-checkout takes directories; a file is rejected at
            # clone time, which is a long way from here to find out.
            print(f"FAIL {d.name}: sparse-checkout takes directories, not {d.paths}")
            failures += 1
    locked = deps.read_lock()
    for name in named:
        if name not in locked:
            print(f"FAIL {name}: no commit in deps.lock; run tools/run.py")
            failures += 1
    print(f"-- the manifest, the targets and the lock agree: {failures} failure(s)")
    return failures


def prompts_agree() -> int:
    """The two scripts say what `docs/reporting-policy.md` says they say.

    The document is what every project was promised; the scripts under
    `scripts/` are a convenience that holds a copy so nobody has to paste one.
    A copy that has drifted is worse than no copy, because the drift is
    invisible from the side that matters -- somebody in ethos or logos reading
    a prompt they were sent.

    Only the body is compared. The scope line and the branch are what the
    scripts fill in, and are the reason they exist.
    """
    import re  # noqa: PLC0415
    import subprocess as sp  # noqa: PLC0415

    root = os.path.dirname(HERE)
    doc = open(os.path.join(root, "docs", "reporting-policy.md")).read()

    # The whole of each prompt, both forms. A script holds the document's text
    # around one or two substituted spans, and the document writes both sides of
    # each with a "-- or, ... --" marker between them. Resolving the marker lets
    # the comparison cover every line, rather than anchoring part way down and
    # leaving the rest unchecked -- which is how a stale paragraph once survived
    # a rewrite of the text above it.
    def body(start: str, end: str) -> str:
        chunk = doc[doc.index(start) : doc.index(end)]
        return re.search(r"```text\n(.*?)\n```", chunk, re.S).group(1)

    def resolve(text: str, marker: str, alt: bool) -> str:
        """Keep one side of an alternatives block and drop the marker.

        The block is the run of lines before the marker back to the last blank
        line, the marker, and the run after it up to the next blank line.
        """
        lines = text.split("\n")
        i = next(k for k, l in enumerate(lines) if l.strip() == marker)
        a = max((k for k in range(i) if not lines[k].strip()), default=-1) + 1
        b = next((k for k in range(i + 1, len(lines)) if not lines[k].strip()),
                 len(lines))
        keep = lines[i + 1 : b] if alt else lines[a:i]
        return "\n".join(lines[:a] + keep + lines[b:])

    def spoken(argv: list[str]) -> str:
        got = sp.run(argv, cwd=root, capture_output=True, text=True)
        if got.returncode != 0:
            return f"!! {argv[0]}: {(got.stderr or got.stdout).strip()[:160]}"
        return got.stdout

    failures = 0
    cases: list[tuple[str, str, str]] = []

    one = body("### Prompt one", "### Prompt two")
    two = body("### Prompt two", "### Prompt three")
    SWEEP, POSTM = "-- or, for the sweep form --", "-- or, with --postm --"

    # prompt two's opening differs by design -- the document says "paste a link",
    # the script has already resolved a checkout -- so compare from TRIAGE down,
    # and separately its own scope sentence is a variable the script fills in.
    def from_triage(text: str) -> str:
        return text[text.index("TRIAGE: is an assistant") :].strip()

    def drop_scope(text: str) -> str:
        """The one sentence each side words for the run it is doing."""
        out = []
        for para in text.split("\n\n"):
            if para.lstrip().startswith("Working in the anoieu repository"):
                continue
            if para.startswith("Process ") or para.startswith("Address "):
                continue
            out.append(para)
        return "\n\n".join(out).strip()

    for name, argv, want, fix in (
        ("check_anoieu, one id",
         ["bash", "scripts/check_anoieu", "--show-prompt", "ID"],
         resolve(one, SWEEP, alt=False),
         lambda s: s.replace("anoieu-ID", "BRANCH")),
        ("check_anoieu, the sweep",
         ["bash", "scripts/check_anoieu", "--show-prompt"],
         resolve(one, SWEEP, alt=True).replace("PROJECT", "anoieu"),
         lambda s: s.replace("anoieu-findings", "BRANCH")),
        ("process_anoieu",
         ["bash", "scripts/process_anoieu", "--show-prompt", "--no-check", root],
         drop_scope(from_triage(resolve(two, POSTM, alt=False))),
         lambda s: drop_scope(from_triage(s))),
        ("process_anoieu --postm",
         ["bash", "scripts/process_anoieu", "--show-prompt", "--no-check",
          "--postm", root],
         drop_scope(from_triage(resolve(two, POSTM, alt=True))),
         lambda s: drop_scope(from_triage(s))),
    ):
        cases.append((name, want.strip(), fix(spoken(argv)).strip()))

    for name, want, got in cases:
        if want == got:
            print(f"ok   scripts/{name} says what reporting-policy.md says")
            continue
        failures += 1
        print(f"FAIL scripts/{name} has drifted from docs/reporting-policy.md")
        for line in difflib.unified_diff(
            want.splitlines(), got.splitlines(), "document", "script", lineterm=""
        ):
            print(f"     {line}")
    print(f"-- the outbound prompts: {failures} failure(s)")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle", action="store_true",
                    help="also ask ethos about each witness, and run the desugaring battery")
    ap.add_argument("--ethos", default=os.environ.get("ETHOS", "ethos"))
    ap.add_argument(
        "--record",
        action="store_true",
        help="write tests/oracle.json from this run instead of checking against it",
    )
    args = ap.parse_args()

    failures = 0
    recorded = json.load(open(ORACLE)) if os.path.isfile(ORACLE) else {}
    seen: dict[str, dict] = {}
    for name in sorted(os.listdir(WITNESSES)):
        if not name.endswith(".eo") or name.endswith(".embed.eo"):
            continue  # an embedding is a companion of a witness, not one itself
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
            got = ethos_verdict(args.ethos, path)
            seen[name] = got
            want_v = recorded.get(name)
            mark = ""
            if want_v and want_v != got:
                mark = f"  CHANGED (was {want_v['verdict']}: {want_v['detail'][:50]})"
                failures += 1
            elif not want_v and recorded:
                mark = "  (not recorded)"
            print(f"     ethos: {got['verdict']}"
                  + (f" -- {got['detail'][:70]}" if got["detail"] else "") + mark)
    if args.oracle:
        if args.record:
            with open(ORACLE, "w") as f:
                json.dump(seen, f, indent=1, sort_keys=True)
            print(f"-- recorded what ethos said about {len(seen)} witness(es)")
            failures = 0
        elif not recorded:
            print("-- no tests/oracle.json; run with --record to create it")
        else:
            missing = sorted(set(recorded) - set(seen))
            for name in missing:
                print(f"FAIL {name}: recorded, but no such witness now")
            failures += len(missing)
            print(f"-- ethos said what tests/oracle.json records, "
                  f"for {len(seen)} witness(es)")

    print(f"-- witnesses: {failures} failure(s)")

    print()
    witness_coverage()

    print()
    failures += manifest_agrees()

    print()
    failures += prompts_agree()

    sys.stdout.flush()
    print()
    import cli_cases  # noqa: PLC0415

    failures += cli_cases.main()

    sys.stdout.flush()
    print()
    import fuzz_cases  # noqa: PLC0415

    failures += fuzz_cases.main()

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
