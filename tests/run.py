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

from anoieu_analyzer.checks import REGISTRY, Context, load_checks, run_all  # noqa: E402
from anoieu_analyzer.cli import _embedding_vocabulary  # noqa: E402
from anoieu_analyzer.loader import load  # noqa: E402
from anoieu_analyzer.semantics import load_set  # noqa: E402

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
    """Drop anything that is about this machine rather than about the file.

    Two shapes of path turn up and only the first was being removed. A witness
    is named with the directory it was run from, which differs per checkout;
    and an internal failure in ethos names the source file ethos was *built*
    from, which differs per machine. Missing the second is how one recorded
    verdict came to hold part of somebody's home directory, cut off mid-path by
    the length limit below, and could never match anywhere else again.
    """
    line = re.sub(r"(/[^\s:]+)+/(?=[\w.-]+\.eo)", "", line)   # the witness's directory
    line = re.sub(r"\s*(?:\bat\s+)?/\S*/\S*", "", line)      # a path on the machine
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
    from anoieu_analyzer.checks import REGISTRY  # noqa: PLC0415

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
    `anoieu_analyzer/reporting/config/deps.json`, the targets in `anoieu_analyzer/reporting/gen_corpus_table.py`, and the lock
    a run writes. A name that appears in one and not the others makes a corpus
    silently unmeasured, which reads exactly like a corpus with no findings. So
    check it here, where no network is needed."""
    from anoieu_analyzer.reporting import deps  # noqa: PLC0415
    from anoieu_analyzer.reporting import gen_corpus_table as corpus  # noqa: PLC0415

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
            print(f"FAIL {name}: no commit in deps.lock; run scripts/run.py")
            failures += 1

    # And the fourth thing, which nothing compared until now: the checkouts on
    # disk. The lock says which commit the report is a report of; deps/ is what
    # somebody reading this repository actually has in front of them. When they
    # disagree, every claim derived from those trees is about a different tree
    # than the record names -- silently, because both look fine on their own.
    # Found by hand on 2026-09-02, three of four disagreeing.
    #
    # Skipped rather than failed when deps/ is absent: the suite runs in a job
    # that clones nothing, and a check that goes red for a directory it was
    # never given would be reporting on the job rather than on the tree.
    root = os.path.dirname(HERE)
    checked = skipped = 0
    for name, commit in sorted(locked.items()):
        head = os.path.join(root, "deps", name)
        if not os.path.isdir(os.path.join(head, ".git")):
            skipped += 1
            continue
        got = subprocess.run(["git", "-C", head, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        checked += 1
        if got and not (got.startswith(commit) or commit.startswith(got)):
            print(f"FAIL {name}: deps/ is at {got[:8]}, the lock records "
                  f"{commit[:8]} -- the report names a tree that is not here")
            print("     run `python3 scripts/run.py --pinned` to restore the "
                  "recorded commits, or `scripts/run.py` to record these")
            failures += 1
    if skipped:
        print(f"     {skipped} checkout(s) not on disk, so not compared")

    # And the fifth: the ref `bug_db/corpus.md` reports beside each commit.
    #
    # **A generated page can be current against its generator and false about
    # the world**, and this is the shape that took. The table's ref came from
    # `deps.json`, which says what is *watched now*, while its commit came from
    # the lock, which says what was *measured*. The two agreed until the ethos
    # exception was dropped on 2026-09-19 -- after which the page asserted that
    # a commit on `ethosEoc3` was ethos's `main`, and the corpus job went red on
    # the committed tree with the only fix on offer being to write the false
    # version. The lock is the register for both halves; this compares the page
    # against it.
    corpus_page = os.path.join(root, "docs", "corpus.md")
    if os.path.isfile(corpus_page):
        with open(corpus_page, encoding="utf-8") as fh:
            rows = dict(re.findall(r"^\| \*\*(\w[\w-]*)\*\* \| `([^`]+)` \|",
                                   fh.read(), re.M))
        for name, entry in sorted(deps.read_lock_entries().items()):
            want, got = entry.get("ref", ""), rows.get(name)
            if got is None:
                print(f"FAIL bug_db/corpus.md has no row for {name}, which the "
                      "lock records a commit for")
                failures += 1
            elif want and got != want:
                print(f"FAIL bug_db/corpus.md says {name} was measured on "
                      f"{got!r}; the lock records the commit as {want!r}")
                print("     the ref reported has to describe the commit "
                      "reported -- see `sync` in anoieu_analyzer/reporting/deps.py")
                failures += 1

    print(f"-- the manifest, the targets, the lock and the checkouts agree: "
          f"{failures} failure(s), {checked} compared")
    return failures


def verdict_audit() -> int:
    """Every closure in the database is readable, and its debt is still tracked.

    Closing before a change lands is the one place this repository has been
    wrong for months at a time, and
    `anoieu_analyzer/reporting/verdicts.py` is the whole of what stops it
    happening again. The way that fails is a verdict somebody reworded: the
    finding stays closed, the debt stays owed, and it silently leaves the audit.
    That is checked here rather than trusted.
    """
    from anoieu_analyzer.reporting import verdicts  # noqa: PLC0415

    failures = 0
    for fid in verdicts.unreadable():
        print(f"FAIL closed entry {fid} has a verdict the vocabulary does not know")
        failures += 1
    for fid in verdicts.malformed():
        print(f"FAIL closed entry {fid} has an awaiting_landing that names no place to look")
        failures += 1
    for fid in verdicts.undeclared():
        print(f"FAIL closed entry {fid} is `accepted and fixed` and does not say "
              "where the change is")
        failures += 1
    for fid in verdicts.overdeclared():
        print(f"FAIL closed entry {fid} carries a landing and is not closed on a promise")
        failures += 1
    owed = verdicts.outstanding()
    failures += verdict_vocabulary(verdicts)
    print(f"-- closures recorded before landing: {len(owed)}, {failures} failure(s)")
    return failures


def verdict_vocabulary(verdicts) -> int:
    """`verdicts.OUTCOMES` and the document that defines it say the same words.

    A surface that restates a register declares its ground truth and is compared
    to it; here the register is *Closure* in `bug_db/README.md` and the copy is
    the dict that runs. Without this the two drift, and a verdict the document
    permits stops being one the audit accepts -- which reads as a defect in
    somebody's database.

    The three synthetic entries are the reason the vocabulary exists at all: the
    reworded verdict that no pattern catches, and a promise with nothing to
    watch.
    """
    import json  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    failures = 0
    doc = os.path.join(os.path.dirname(HERE), "bug_db", "README.md")
    text = open(doc).read()
    body = text.split("**A verdict is one of seven words")[1].split("\n### ")[0]
    named = set(re.findall(r"^\| `([a-z -]+)` \|", body, re.M))
    if named != set(verdicts.OUTCOMES):
        print(f"FAIL the verdict vocabulary differs: document {sorted(named)}, "
              f"anoieu_analyzer/reporting/verdicts.py {sorted(verdicts.OUTCOMES)}")
        failures += 1

    BUGS = [
        {"id": "1" * 16, "closed_verdict": "accepted and fixed",
         "closed_why": "it will land shortly"},
        {"id": "2" * 16, "closed_verdict": "fixed eventually",
         "closed_why": "reworded out of the vocabulary"},
        {"id": "3" * 16, "closed_verdict": "declined", "closed_why": "no",
         "awaiting_landing": {"project": "ethos", "branch": "b", "commit": "1234567"}},
        {"id": "4" * 16, "closed_verdict": "accepted and fixed", "closed_why": "x",
         "awaiting_landing": {"project": "ethos", "branch": "", "commit": "1234567"}},
    ]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"bugs": BUGS}, fh)
        fake = fh.name
    try:
        cases = (
            ("a promise with nothing to watch is caught",
             verdicts.undeclared(fake), ["1" * 16]),
            ("a verdict outside the vocabulary is caught",
             verdicts.unreadable(fake), ["2" * 16]),
            ("a landing on an entry that is not a promise is caught",
             verdicts.overdeclared(fake), ["3" * 16]),
            ("a landing that names no branch is caught",
             verdicts.malformed(fake), ["4" * 16]),
        )
        for what, got, want in cases:
            ok = got == want
            failures += 0 if ok else 1
            print(("ok   " if ok else "FAIL ") + what)
            if not ok:
                print(f"     got {got}, wanted {want}")
    finally:
        os.unlink(fake)
    return failures


def targets_agree() -> int:
    """The two workflows describe the same standard targets.

    The old path reads the `TARGETS` literal in `anoieu_analyzer/reporting/gen_corpus_table.py`;
    `scripts/anoieu_analyzer` and the agent prompt read
    `anoieu_analyzer/reporting/config/targets.json`. Both are kept while the new workflow proves itself,
    and two descriptions of one thing that nothing compares is the drift this
    ecosystem keeps finding -- in a prompt, in a generated page, and here
    it would be in what a report is a report of.
    """
    from anoieu_analyzer.reporting import targets as config  # noqa: PLC0415
    from anoieu_analyzer.reporting.gen_corpus_table import TARGETS  # noqa: PLC0415

    spec = config.load()
    listed = config.as_tuples(spec)
    failures = 0
    if listed != list(TARGETS):
        only_json = [t for t in listed if t not in TARGETS]
        only_py = [t for t in TARGETS if t not in listed]
        for t in only_json:
            print(f"FAIL anoieu_analyzer/reporting/config/targets.json has a target TARGETS does not: {t[0]!r}")
        for t in only_py:
            print(f"FAIL TARGETS has a target anoieu_analyzer/reporting/config/targets.json does not: {t[0]!r}")
        if not only_json and not only_py:
            print("FAIL anoieu_analyzer/reporting/config/targets.json and TARGETS agree on the targets "
                  "and not on their order")
        failures = max(1, len(only_json) + len(only_py))
    ids = [t["id"] for t in spec]
    for dup in {i for i in ids if ids.count(i) > 1}:
        print(f"FAIL anoieu_analyzer/reporting/config/targets.json uses the target id {dup!r} twice")
        failures += 1
    print(f"-- standard targets: {len(spec)}, {failures} failure(s)")
    return failures


def prompts_agree() -> int:
    """The closure prompt's entry shape and `docs/experience.md`'s template agree.

    **Two descriptions of one thing, and the prompt is a copy.** The page is the
    register: it sets out the fields an episode carries, in order, under *How
    this page is maintained*, and a reader of the log is entitled to expect every
    entry to look alike. `prompts/close_bug_db` restates that list to the
    assistant that writes them, so the two drift the moment either moves -- which
    is how the prompt came to be directing closures into two ledgers that had
    already been deleted.

    Every bolded label in the template block counts, whether it sits in the
    entry's table (`**When**`) or heads a paragraph (`**What happened.**`), and
    trailing punctuation and whitespace are normalised on both sides: each page
    wraps at eighty columns, and a label split across a line break is the same
    label.

    This is the comparison `policy_check/checker.py` names when it skips *a
    workflow is defined in prose* and *a surface that restates a register is
    compared to it*.
    """
    def flat(text: str) -> str:
        return re.sub(r"\s+", " ", text)

    def clean(label: str) -> str:
        return flat(label).strip().rstrip(".:").strip()

    root = os.path.dirname(HERE)
    page = os.path.join(root, "docs", "experience.md")
    prompt = os.path.join(root, "prompts", "close_bug_db")
    with open(page, encoding="utf-8") as fh:
        text = fh.read()
    _, sep, tail = text.partition("## How this page is maintained")
    if not sep:
        print("FAIL docs/experience.md has no 'How this page is maintained' "
              "section, so the entry template is not where prompts/close_bug_db "
              "says it is")
        return 1
    block = re.search(r"```text\n(.*?)```", tail, re.S)
    if not block:
        print("FAIL docs/experience.md's maintenance section carries no template block")
        return 1
    # A field label heads its line or sits alone in a table cell. Emphasis in
    # the middle of a sentence is prose, not a field, and counting it as one is
    # how this check first asked the prompt to name "This field is why the page
    # exists".
    template, seen = [], set()
    for label in re.findall(r"^(?:\|\s*)?\*\*([^*]+?)\*\*", block.group(1), re.M):
        name = clean(label)
        if name and name not in seen:
            seen.add(name)
            template.append(name)
    with open(prompt, encoding="utf-8") as fh:
        listed = [clean(x) for x in re.findall(r"`([^`\n]+?)`", flat(fh.read()))]

    failures = 0
    #: Where each template field is first named in the prompt, so that a missing
    #: field and a reordered one are told apart.
    at = {f: listed.index(f) for f in template if f in listed}
    for field in template:
        if field not in at:
            print(f"FAIL prompts/close_bug_db does not name the `{field}` field "
                  "that docs/experience.md's template requires")
            failures += 1
    named = [f for f in template if f in at]
    if len(named) == len(template) and sorted(named, key=at.get) != named:
        print("FAIL prompts/close_bug_db names the entry fields in a different "
              f"order from the template: {sorted(named, key=at.get)} against {named}")
        failures += 1
    print(f"-- the entry template and its prompt: {len(template)} field(s), "
          f"{failures} failure(s)")
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
    from policy_check.tests import cases as policy_cases
    failures += policy_cases.main()
    failures += verdict_audit()
    failures += targets_agree()
    failures += prompts_agree()

    sys.stdout.flush()
    print()
    import cli_cases  # noqa: PLC0415

    failures += cli_cases.main()

    sys.stdout.flush()
    print()
    import fuzz_cases  # noqa: PLC0415

    failures += fuzz_cases.main()

    import database_cases  # noqa: PLC0415

    failures += database_cases.main()

    import closure_cases  # noqa: PLC0415

    failures += closure_cases.main()

    if args.oracle:
        print()
        sys.stdout.flush()
        import subprocess as sp  # noqa: PLC0415

        oracle = os.path.join(os.path.dirname(HERE), "tests", "oracle_desugar.py")
        p = sp.run([sys.executable, oracle, "--ethos", args.ethos], text=True)
        failures += 1 if p.returncode else 0

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
