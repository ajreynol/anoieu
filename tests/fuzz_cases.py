#!/usr/bin/env python3
"""End-to-end cases for anoieu-fuzz, the fuzzer.

A fuzzer is a program whose output is other people's bugs, which makes it the
one component here that cannot be tested against what it finds: a suite that
asserted "ethos crashes on this" would go green or red for reasons that are
nothing to do with this repository, and would need ethos built to run at all.

So this tests the *harness* rather than the findings, against checkers written
here -- two dozen lines of Python apiece, with the interface a real checker
has. Each one is a checker whose answers are known, which is what lets a case
say "these two disagree and anoieu-fuzz noticed" and mean it.

    python3 tests/fuzz_cases.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from anoieu_fuzz.checkers import classify, from_config, load_config  # noqa: E402
from anoieu_fuzz.codes import CODES, KIND_TO_CODE  # noqa: E402
from anoieu_fuzz.gen import (  # noqa: E402
    Case,
    unwrap,
    absolutize,
    generate,
    reformat,
    split_commands,
)
from anoieu_fuzz.triage import Corpus, Finding, judge, shrink  # noqa: E402
from anoieu_fuzz import report as reporting  # noqa: E402

# A checker that accepts anything whose parentheses balance. It stands for the
# permissive side of a disagreement.
LENIENT = """import sys
text = open(sys.argv[-1]).read()
if text.count("(") != text.count(")"):
    sys.stderr.write("Error: unbalanced\\n"); sys.exit(1)
print("correct")
"""

# ... and one that also refuses a command it does not implement, the way a
# checker with a smaller parser does.
STRICT = """import sys
text = open(sys.argv[-1]).read()
if text.count("(") != text.count(")"):
    sys.stderr.write("Error: unbalanced\\n"); sys.exit(1)
if "declare-fun" in text:
    sys.stderr.write("Error: declare-fun is not a command\\n")
    print("incorrect"); sys.exit(1)
print("correct")
"""

# A checker that dies the way a checker dies: no diagnostic, just a status.
FRAGILE = """import sys
text = open(sys.argv[-1]).read()
if "boom" in text:
    sys.exit(3)
print("correct")
"""

SLOW = """import time
time.sleep(30)
print("correct")
"""

# What ethos and logos actually print, so that `classify` is tested against the
# strings it was written for rather than against a description of them.
ETHOS_OK = ("correct\n", "", 0)
ETHOS_ERR = (
    "",
    "Fatal failure within void ethos::Lexer::parseError(const std::string&, bool) at "
    "/x/src/lexer.cpp:88\nError: /tmp/case.cpc:2.0: Expected KEYWORD, got `` (EOF).\n",
    -6,
)
ETHOS_INTERNAL = (
    "",
    "Fatal failure within void ethos::TypeChecker::setLiteralTypeRule(...) at /x/t.cpp:53\n"
    "TypeChecker::setTypeRule: cannot set type rule for kind NUMERAL to S2\n",
    -6,
)
ETHOS_CRASH = ("", "terminate called after throwing an instance of 'std::length_error'\n", -6)
LOGOS_BAD = (
    "incorrect\n",
    "Error: every proof command executed without getting stuck, but the final state "
    "after step @p2 is not a closed proof of false.\n",
    1,
)
LOGOS_PARSE = ("", "Error parsing proof: offset 21: expected ')'\n", 1)
LOGOS_PARTIAL = ("incomplete\n", "Error: assumption 0 has no SMT-LIB translation\n", 2)


def write(directory: str, name: str, text: str) -> str:
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write(text)
    return path


def config(directory: str, name: str, **checkers: str) -> str:
    """An anoieu-fuzz.json naming each fake checker, as a real one would be named."""
    entry = {}
    for checker, body in checkers.items():
        script = write(directory, f"{checker}.py", body)
        argv = [sys.executable, script, "{file}"]
        entry[checker] = {"modes": {"proof": argv, "signature": argv}}
    path = os.path.join(directory, f"{name}.json")
    with open(path, "w") as f:
        json.dump({"checkers": entry, "signature": ""}, f)
    return path


def run(*argv: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, "-m", "anoieu_fuzz", *argv], capture_output=True, text=True, cwd=ROOT
    )
    return p.returncode, p.stdout, p.stderr


def cases(d: str) -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []

    def case(name: str, ok: bool, detail: str = "") -> None:
        out.append((name, ok, detail))

    # -- reading a file back into commands

    text = '(a b)\n; (not a command)\n(c "a ) string" |a ) symbol|)\n(d (e))\n'
    got = split_commands(text)
    case("a file splits into its top-level commands", len(got) == 3, f"{len(got)}: {got}")
    case(
        "a paren inside a string or a |symbol| is not a paren",
        got[1] == '(c "a ) string" |a ) symbol|)',
        got[1] if len(got) > 1 else "-",
    )
    case(
        "an unterminated form is kept rather than dropped",
        split_commands("(a (b") == ["(a (b"],
        str(split_commands("(a (b")),
    )
    case(
        "a seed's relative include is made absolute",
        absolutize(['(include "../x.eo")'], "/s/d") == ['(include "/s/x.eo")'],
        str(absolutize(['(include "../x.eo")'], "/s/d")),
    )

    # -- what a checker said, as a verdict

    verdicts = {
        "ethos accepting": (ETHOS_OK, "correct", "accept"),
        "ethos refusing by abort": (ETHOS_ERR, "rejected", "reject"),
        "ethos aborting off its own convention": (ETHOS_INTERNAL, "unexplained", "abnormal"),
        "an uncaught C++ exception": (ETHOS_CRASH, "crash", "abnormal"),
        "logos refusing a proof": (LOGOS_BAD, "incorrect", "reject"),
        "logos refusing to parse": (LOGOS_PARSE, "rejected", "reject"),
        "logos accepting but unmodelled": (LOGOS_PARTIAL, "incomplete", "accept"),
    }
    for what, ((o, e, rc), status, coarse) in verdicts.items():
        got = classify("c", rc, o, e, 0.0)
        case(
            f"{what} is {status}",
            (got.status, got.coarse) == (status, coarse),
            f"{got.status}/{got.coarse}",
        )
    case(
        "a signal is not on its own a crash",
        classify("c", -6, *ETHOS_ERR[:2][::-1][::-1], 0.0).coarse == "reject",
        "",
    )
    case(
        "two runs of one defect reduce to one detail",
        classify("c", -6, "", "Error: /a/b.cpc:12.3: no symbol `x`\n", 0.0).detail
        == classify("c", -6, "", "Error: /q/z.cpc:99.1: no symbol `y`\n", 0.0).detail,
        classify("c", -6, "", "Error: /a/b.cpc:12.3: no symbol `x`\n", 0.0).detail,
    )

    # -- the oracle

    from anoieu_fuzz.checkers import Outcome  # noqa: PLC0415

    empty = Case(["(a)"])
    agree = [Outcome("x", "correct", "accept"), Outcome("y", "correct", "accept")]
    case("agreement is not a finding", judge(empty, agree) is None, "")
    both_no = [Outcome("x", "rejected", "reject", "one thing"),
               Outcome("y", "incorrect", "reject", "another thing")]
    case(
        "two refusals for different reasons are still agreement",
        judge(empty, both_no) is None,
        "",
    )
    split = [Outcome("x", "correct", "accept"), Outcome("y", "incorrect", "reject", "no")]
    got = judge(empty, split, reference="y")
    case("accepting what the reference refused is the serious direction",
         got is not None and got.code == "FUZ0001",
         got.code if got else "none")
    got_other = judge(empty, split, reference="x")
    case("and refusing what it accepted is the mild one",
         got_other is not None and got_other.code == "FUZ0005",
         got_other.code if got_other else "none")
    case("which is a warning rather than an error",
         CODES["FUZ0005"].severity.value == "warning" and
         CODES["FUZ0001"].severity.value == "error", "")
    unattributed = judge(empty, split, reference="nobody")
    case("a disagreement the reference sat out is read the serious way",
         unattributed is not None and unattributed.code == "FUZ0001",
         unattributed.code if unattributed else "none")
    case("both directions keep the `disagreement` bucket prefix, so the ids "
         "already in the ledger survive the split",
         got.bucket.startswith("disagreement") and got_other.bucket.startswith("disagreement"),
         f"{got.bucket[:26]} / {got_other.bucket[:26]}")
    flipped = judge(empty, [Outcome("x", "rejected", "reject", "no"),
                            Outcome("y", "correct", "accept")], reference="y")
    case("and the two directions are still different buckets",
         flipped is not None and flipped.bucket != got.bucket,
         f"{flipped.bucket[:34]} / {got.bucket[:34]}" if flipped else "none")
    got = judge(empty, [Outcome("x", "crash", "abnormal", "boom")])
    case("a crash is a finding on its own", got is not None and got.kind == "crash",
         got.kind if got else "none")
    got = judge(empty, [Outcome("x", "timeout", "abnormal", ">10s")])
    case("so is a timeout", got is not None and got.kind == "timeout",
         got.kind if got else "none")
    case("a checker that did not run says nothing",
         judge(empty, [Outcome("x", "skipped", "skipped")]) is None, "")

    # through `classify`, because that is where a detail is made portable, and
    # bucketing is only stable because it was. The strings are ethos's, from a
    # run: what differs between two instances is the build path and the symbol.
    def fatal(where: str, what: str) -> "Finding":
        return judge(empty, [classify("x", -6, "", f"Fatal failure within f(x) at {where}\n{what}\n", 0)])

    a = fatal("/home/a/src/type_checker.cpp:53", "cannot set type rule for NUMERAL to S2")
    b = fatal("/elsewhere/build/type_checker.cpp:53", "cannot set type rule for NUMERAL to S9")
    case("two instances of one defect share a bucket", a.bucket == b.bucket,
         f"{a.bucket} / {b.bucket}")
    c = judge(empty, [classify("x", -6, "", "Fatal failure within g(y) at /a/state.cpp:9\nno\n", 0)])
    case("a different defect does not", a.bucket != c.bucket, c.bucket)

    # -- shrinking

    big = Case([f"(cmd{i})" for i in range(20)] + ["(keep (a (b c)) d)"])

    def probe(case_: Case) -> Finding | None:
        text = " ".join(case_.commands)
        if "(keep" in text and "(cmd7)" in text:
            return Finding("crash", "B", "", case_, [])
        return None

    small, spent = shrink(big, probe, "B")
    case(
        "shrinking keeps only the commands that matter",
        sorted(small.commands) == ["(cmd7)", "(keep)"],
        f"{small.commands} in {spent} runs",
    )
    case("and cuts inside the command it kept", "(keep)" in small.commands,
         str(small.commands))

    # A seed run as it stands is the file somebody committed, and the finding is
    # that *that file* disagrees. The bucket does not say where a checker
    # refused, so an edit the verdict does not depend on holds it and survives --
    # which is how a promoted reproducer came to carry a cut the reference had
    # never looked at. See shrink()'s docstring and docs/reports/reports.md.
    seeded = Case(["(keep (a (b c)) d)", "(cmd7)"], source="seed:committed.cpc")
    untouched, spent_seed = shrink(seeded, probe, "B")
    case("a seed run as it stands is not shrunk",
         untouched.commands == seeded.commands and spent_seed == 0,
         f"{untouched.commands} in {spent_seed} runs")
    mutated = Case(["(keep (a (b c)) d)", "(cmd7)", "(cmd8)"],
                   source="mutated:seed:committed.cpc")
    cut, _ = shrink(mutated, probe, "B")
    case("but a mutation of one still is",
         sorted(cut.commands) == ["(cmd7)", "(keep)"], str(cut.commands))

    # -- the corpus

    root = os.path.join(d, "findings")
    corpus = Corpus(root)
    f1 = Finding("crash", "b1", "s", Case(["(a)"], suffix=".eo"), [])
    case("a new bucket is written", corpus.add(f1) is True, "")
    case("the case is on disk", os.path.isfile(os.path.join(root, "b1", "case.eo")), "")
    case("the same bucket again is counted, not rewritten", corpus.add(f1) is False, "")
    case("and counted", corpus.counts["b1"] == 2, str(corpus.counts))

    # -- generation

    one = generate("s1", "proof")
    again = generate("s1", "proof")
    case("a seed determines a case", one.text() == again.text(), "")
    case("a different seed does not", generate("s2", "proof").text() != one.text(), "")
    for mode in ("proof", "signature"):
        bad = [
            i
            for i in range(40)
            if not _balanced("\n".join(generate(f"b{i}", mode).commands))
        ]
        case(f"{mode} cases are balanced s-expressions", not bad, f"{len(bad)} were not")
    case(
        "a proof case with no signature carries its own declarations",
        any("declare-const" in c for c in generate("p", "proof").commands),
        "",
    )
    twin = reformat("r", Case(['(echo "a ; b")', "(declare-const x Int)"]))
    case(
        "reformatting never edits inside a string",
        '(echo "a ; b")' in twin.commands,
        str(twin.commands),
    )

    # -- end to end, against checkers whose answers are known

    cfg = config(d, "pair", lenient=LENIENT, strict=STRICT)
    case(
        "a config that names checkers replaces the defaults",
        sorted(c.name for c in from_config(load_config(cfg))) == ["lenient", "strict"],
        str(sorted(c.name for c in from_config(load_config(cfg)))),
    )
    out_dir = os.path.join(d, "out")
    seed = write(d, "seed.cpc", "(declare-fun f (U) U)\n(declare-const a U)\n")
    rc, o, e = run(
        "run", "--config", cfg, "--out", out_dir, "-n", "4", "--mode", "proof",
        "--seed-corpus", seed, "--mutate", "1.0",
    )
    case("a disagreement is found and exits 1", rc == 1, f"exit {rc}: {e[-200:]}")
    case(
        "the seed is checked as it stands, before anything is mutated",
        "(seed:" in o or "seed.cpc" in o,
        o[-300:],
    )
    case("and is reported as one", "disagreement" in o, o[-300:])
    found = os.path.isfile(os.path.join(out_dir, "findings.jsonl"))
    case("and written to the corpus", found, str(os.listdir(out_dir)) if found else "-")

    cfg2 = config(d, "fragile", fragile=FRAGILE)
    out2 = os.path.join(d, "out2")
    seed2 = write(d, "boom.cpc", "(boom)\n(declare-const a U)\n")
    rc, o, _ = run(
        "run", "--config", cfg2, "--out", out2, "-n", "3", "--seed-corpus", seed2,
        "--mutate", "1.0", "--checker", "fragile",
    )
    case("a checker that dies quietly is a crash", rc == 1 and "crash" in o, o[-200:])

    cfg3 = config(d, "slow", slow=SLOW)
    out3 = os.path.join(d, "out3")
    seed3 = write(d, "slow.cpc", "(slow)\n")
    rc, o, _ = run(
        "run", "--config", cfg3, "--out", out3, "-n", "1", "--seed-corpus", seed3,
        "--timeout", "1", "--checker", "slow", "--no-shrink",
    )
    case("a checker that never answers is a timeout", "timeout" in o, o[-200:])

    cfg4 = config(d, "one", lenient=LENIENT)
    rc, o, _ = run("run", "--config", cfg4, "--out", os.path.join(d, "out4"),
                   "-n", "3", "--checker", "lenient")
    case("a run that finds nothing exits 0", rc == 0, f"exit {rc}: {o[-200:]}")

    rc, o, _ = run("replay", "--config", cfg, seed)  # cfg names only the fakes
    case("replay reports what each checker said", rc == 1 and "lenient" in o and "strict" in o,
         o[-200:])
    rc, o, _ = run("one", "--seed", "x7", "--mode", "signature")
    case("`one` prints a case and nothing else", rc == 0 and o.startswith("; anoieu-fuzz"),
         o[:60])
    rc, o, _ = run("checkers")
    case("`checkers` says what is configured", rc == 0 and "ethos" in o and "logos" in o,
         o[:80])

    # -- what a real proof looks like, and what makes two findings one

    wrapped = "(\n(declare-const x Bool)\n(assume @p0 x)\n(step @p1 :rule refl)\n)"
    case(
        "a proof cvc5 wrapped in one outer form unwraps into its commands",
        len(unwrap(split_commands(wrapped))) == 3,
        str(unwrap(split_commands(wrapped))),
    )
    case(
        "and an ordinary command is left alone",
        unwrap(["(declare-const x Int)"]) == ["(declare-const x Int)"],
        str(unwrap(["(declare-const x Int)"])),
    )
    case(
        "as is a wrapper around something that is not a command list",
        unwrap(["(-> Bool Bool)"]) == ["(-> Bool Bool)"],
        str(unwrap(["(-> Bool Bool)"])),
    )

    def detail(msg: str) -> str:
        return classify("c", 1, "incorrect\n", msg + "\n", 0.0).detail

    case(
        "a checker that quotes the offending term back is still one finding",
        detail("Error: assumption after the first step: (assume @p1 @t6)")
        == detail("Error: assumption after the first step: (assume @p0 (not (= x 4)))"),
        detail("Error: assumption after the first step: (assume @p1 @t6)"),
    )
    case(
        "but two token classes are two findings",
        detail("Error: /a.cpc:2.0: Expected command, got `` (EOF).")
        != detail("Error: /a.cpc:2.0: Expected command, got `x` (SYMBOL)."),
        detail("Error: /a.cpc:2.0: Expected command, got `` (EOF)."),
    )

    # -- the reporting half: codes, the committed corpus, and the ledger

    case(
        "every kind of finding has a code",
        set(KIND_TO_CODE) == {"overaccept", "underaccept", "crash", "unexplained", "timeout"},
        str(sorted(KIND_TO_CODE)),
    )
    case(
        "and the two directions of a disagreement are not equally severe",
        CODES[KIND_TO_CODE["overaccept"]].severity.rank
        < CODES[KIND_TO_CODE["underaccept"]].severity.rank,
        f'{CODES["FUZ0001"].severity.value} vs {CODES["FUZ0005"].severity.value}',
    )
    case(
        "and every code has a page",
        all(CODES[c].page and CODES[c].title for c in KIND_TO_CODE.values()),
        str([c for c in KIND_TO_CODE.values() if not CODES[c].page]),
    )

    promoted = reporting.load()
    case("the committed corpus is readable", isinstance(promoted, list), "")
    broken = [r["bucket"] for r in promoted if not (r["case"] and os.path.isfile(r["case"]))]
    case("every promoted finding has its reproducer", not broken, str(broken))
    unknown = [r["bucket"] for r in promoted if r.get("kind") not in KIND_TO_CODE]
    case("and a kind that maps to a code", not unknown, str(unknown))
    ownerless = [r["bucket"] for r in promoted if reporting.owner_of(r) == "—"]
    case("and an owner", not ownerless, str(ownerless))

    # The generator in tools/ needs deps/ to run the checks, and CI's fast job
    # has none; this half of what it checks needs nothing but this repository.
    # Both files, because a promoted finding that has been ruled on has its row
    # in the closed half and is accounted for there.
    text = ""
    for name in ("open-findings.md", "closed-findings.md"):
        path = os.path.join(ROOT, "docs", "reports", name)
        text += open(path).read() if os.path.isfile(path) else ""
    unlisted = [k for k in reporting.rows() if f"`{k}`" not in text]
    case(
        "every promoted finding has a row in the ledger",
        not unlisted,
        f"{len(unlisted)} unlisted; run tools/gen_open_findings.py",
    )

    if promoted:
        diag = reporting.diagnostic(promoted[0])
        case(
            "a promoted finding is an ordinary diagnostic",
            diag.code.startswith("FUZ") and diag.span.line >= 1 and bool(diag.notes),
            f"{diag.code} at line {diag.span.line}",
        )
        case(
            "whose span skips the header comment the generator wrote",
            not open(diag.span.path).read().splitlines()[diag.span.line - 1].startswith(";"),
            "",
        )
        try:
            parsed = json.loads(reporting.render(promoted, "json"))
            ok = isinstance(parsed, list) and parsed[0]["code"].startswith("FUZ")
        except Exception as exc:  # noqa: BLE001
            ok, parsed = False, str(exc)
        case("and renders through anoieu's own formats", ok, str(parsed)[:120])

    src = os.path.join(d, "bucket")
    os.makedirs(src, exist_ok=True)
    write(src, "case.eo", "; header\n(declare-const f (->))\n")
    with open(os.path.join(src, "finding.json"), "w") as f:
        json.dump({"kind": "crash", "bucket": "b-test", "summary": "x",
                   "outcomes": [{"checker": "ethos", "status": "crash",
                                 "coarse": "abnormal", "detail": "boom"}]}, f)
    corpus_dir = os.path.join(d, "corpus")
    where = reporting.promote(src, corpus_dir)
    case("promote copies the reproducer", os.path.isfile(os.path.join(where, "case.eo")), where)
    try:
        reporting.promote(src, corpus_dir)
        again = "it did not"
    except FileExistsError:
        again = ""
    case("and refuses to overwrite one", not again, again)
    got = reporting.load(corpus_dir)
    case("a promoted crash is owned by the checker that crashed",
         got and reporting.owner_of(got[0]) == "ethos",
         reporting.owner_of(got[0]) if got else "-")

    # verify, against checkers whose answers are known: one agreeing with what
    # was recorded, one that has changed its mind since
    vdir = os.path.join(d, "vcorpus", "b-verify")
    os.makedirs(vdir, exist_ok=True)
    write(vdir, "case.cpc", "; header\n(declare-fun f (U) U)\n")
    with open(os.path.join(vdir, "finding.json"), "w") as f:
        json.dump({"kind": "overaccept", "bucket": "b-verify", "mode": "proof",
                   "summary": "lenient accepted what strict refused",
                   "outcomes": [
                       {"checker": "lenient", "status": "correct", "coarse": "accept"},
                       {"checker": "strict", "status": "incorrect", "coarse": "reject"}]}, f)
    # `disagreement` is not a kind any more, so this record would not resolve to
    # a code; the corpus cases above are what keep the promoted ones honest.
    rc, o, _ = run("verify", "--config", cfg, "--corpus", os.path.join(d, "vcorpus"))
    case("verify replays a promoted reproducer",
         rc == 0 and o.count(" ok ") == 2 and "2 verdict(s) compared" in o, o[-220:])

    with open(os.path.join(vdir, "finding.json")) as f:
        record = json.load(f)
    record["outcomes"][1]["coarse"] = "accept"  # as if strict had once agreed
    with open(os.path.join(vdir, "finding.json"), "w") as f:
        json.dump(record, f)
    rc, o, _ = run("verify", "--config", cfg, "--corpus", os.path.join(d, "vcorpus"))
    case("and fails when a verdict has moved", rc == 1 and "CHANGED" in o, o[-220:])

    rc, o, _ = run("verify", "--config", cfg4, "--checker", "nobody",
                   "--corpus", os.path.join(d, "vcorpus"))
    case("a run that compared nothing says so", "compared nothing" in o or
         "nothing was compared" in o, o[-200:])

    rc, o, _ = run("explain", "FUZ0001")
    case("explain prints the page", rc == 0 and "FUZ0001" in o, o[:60])
    rc, _, e = run("explain", "FUZ9999")
    case("and refuses an unknown code", rc == 2, f"exit {rc}")
    rc, o, _ = run("list-codes")
    case("list-codes prints every code", rc == 0 and o.count("FUZ") == len(CODES), o[:80])

    return out


def _balanced(text: str) -> bool:
    """Whether every parenthesis in a generated case is matched.

    Generated text is meant to be *wrong*, but it is meant to be wrong in
    Eunoia rather than wrong in s-expressions: an unbalanced file tests a lexer
    and nothing past it, and the mutator is where that is supposed to come from.
    """
    depth = 0
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == ";":
            while i < n and text[i] != "\n":
                i += 1
        elif c == '"':
            i += 1
            while i < n and text[i] != '"':
                i += 1
        elif c == "|":
            i += 1
            while i < n and text[i] != "|":
                i += 1
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        results = cases(d)
    bad = 0
    for name, ok, detail in results:
        if ok:
            print(f"ok   {name}")
        else:
            bad += 1
            print(f"FAIL {name}: {detail}")
    print(f"-- anoieu-fuzz: {len(results)} case(s), {bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
