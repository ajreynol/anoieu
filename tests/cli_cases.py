#!/usr/bin/env python3
"""End-to-end cases for the parts of the tool a CI job depends on.

The witness suite says what each check reports. This says what a *run* does with
those findings: that a comment silences one, that a baseline holds one, that a
configuration file is read, and that the machine-readable formats parse. Every
case is the command a repository would actually run.
"""

from __future__ import annotations

import collections
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from policy_check.checker import CHECKER_REPO  # noqa: E402

NIL_BAD = """(declare-const Int Type)
(declare-consts <numeral> Int)
(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
"""

# The shape of cvc5's expert signature: a base file declaring a helper, and a
# second file whose rule uses it *without including it*. The consumer loads both,
# in order, into one symbol table.
BASE = """(declare-const Int Type)
(declare-parameterized-const = ((T Type :implicit)) (-> T T Bool))
(program $helper ((x Int)) :signature (Int) Int ( (($helper x) x) ))
"""

EXPERT = """(declare-const b Int)
(declare-rule uses-helper ((x Int))
  :args (x)
  :requires ((($helper x) x))
  :conclusion (= x x)
)
"""

NIL_SUPPRESSED = """(declare-const Int Type)
(declare-consts <numeral> Int)
; anoieu: allow EO0041  the Int nil is what this test is about
(declare-const or (-> Bool Bool Bool) :right-assoc-nil 0)
(declare-const and (-> Bool Bool Bool) :right-assoc-nil 0)
"""


def run(*argv: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, "-m", "anoieu_analyzer", *argv],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return p.returncode, p.stdout, p.stderr


def write(directory: str, name: str, text: str) -> str:
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write(text)
    return path


def codes(out: str) -> list[str]:
    return [f["code"] for f in json.loads(out)]


def cases(d: str) -> list[tuple[str, bool, str]]:
    """Each case: what it is, whether it held, and what happened."""
    out: list[tuple[str, bool, str]] = []

    def case(name: str, ok: bool, detail: str = "") -> None:
        out.append((name, ok, detail))

    bad = write(d, "nil.eo", NIL_BAD)
    sup = write(d, "sup.eo", NIL_SUPPRESSED)

    rc, o, _ = run("check", bad, "--format", "json")
    case("an error exits 1", rc == 1, f"exit {rc}")
    case("the finding is reported", codes(o) == ["EO0041"], str(codes(o)))

    rc, o, _ = run("check", sup, "--format", "json")
    case("a comment silences its line", codes(o) == ["EO0041"], str(codes(o)))
    rc, o, _ = run("check", sup, "--no-suppress", "--format", "json")
    case("--no-suppress restores it", codes(o) == ["EO0041", "EO0041"], str(codes(o)))

    base = os.path.join(d, "baseline.json")
    rc, o, _ = run("check", bad, "--baseline", base, "--update-baseline")
    held = json.load(open(base))["findings"] if os.path.isfile(base) else []
    case("--update-baseline writes the findings", len(held) == 1, f"{len(held)} entries")
    rc, o, _ = run("check", bad, "--baseline", base, "--format", "json")
    case("a baselined finding is held back", codes(o) == [], str(codes(o)))
    rc, _, _ = run("check", bad, "--baseline", base)
    case("and the run passes", rc == 0, f"exit {rc}")

    moved = write(d, "nil.eo", "\n\n" + NIL_BAD)  # the finding moves down two lines
    rc, o, _ = run("check", moved, "--baseline", base, "--format", "json")
    case("a baseline survives lines moving", codes(o) == [], str(codes(o)))
    write(d, "nil.eo", NIL_BAD)

    # the configuration cases live in their own directory: discovery walks up from
    # the entry point, so a config beside the other cases would govern them too
    sub = os.path.join(d, "cfg")
    os.makedirs(sub, exist_ok=True)
    write(sub, "nil.eo", NIL_BAD)
    cfg = os.path.join(sub, "anoieu.json")
    with open(cfg, "w") as f:
        json.dump({"entry_points": ["nil.eo"], "severity": {"EO0041": "hint"}}, f)
    rc, o, _ = run("check", "--config", cfg, "--format", "json")
    got = json.loads(o)
    case("a config supplies the entry points", len(got) == 1, f"{len(got)} findings")
    case(
        "and can lower a severity",
        bool(got) and got[0]["severity"] == "hint",
        got[0]["severity"] if got else "-",
    )
    rc, _, _ = run("check", "--config", cfg)
    case("which changes the exit code", rc == 0, f"exit {rc}")

    with open(cfg, "w") as f:
        json.dump({"entry_points": ["nil.eo"], "disable": ["EO0041"]}, f)
    rc, o, _ = run("check", "--config", cfg, "--format", "json")
    case("a config can disable a check", codes(o) == [], str(codes(o)))

    rc, o, _ = run("check", os.path.join(sub, "nil.eo"), "--format", "json")
    case("a config is found from the entry point", codes(o) == [], str(codes(o)))

    # cvc5-4: `$is_app` was reported dead because the base and expert signatures
    # were analysed as separate worlds. They are not: the consumer includes them
    # in order into one symbol table.
    prof = os.path.join(d, "prof")
    os.makedirs(prof, exist_ok=True)
    base = write(prof, "base.eo", BASE)
    expert = write(prof, "expert.eo", EXPERT)
    rc, o, _ = run("check", base, "--pedantic", "--only", "EO0060", "--format", "json")
    case("a helper unused by its own file reads as dead", codes(o) == ["EO0060"], str(codes(o)))
    rc, o, _ = run("check", base, expert, "--pedantic", "--only", "EO0060", "--format", "json")
    case(
        "several files are one ordered profile, so the user is seen",
        codes(o) == [],
        str(codes(o)),
    )
    pcfg = os.path.join(prof, "anoieu.json")
    with open(pcfg, "w") as f:
        json.dump(
            {
                "profiles": [
                    {"name": "safe", "includes": ["base.eo"]},
                    {"name": "expert", "includes": ["base.eo", "expert.eo"]},
                ]
            },
            f,
        )
    rc, o, _ = run("check", "--config", pcfg, "--pedantic", "--only", "EO0060",
                   "--format", "json")
    case(
        "a reachability claim must hold in every profile that reads the file",
        codes(o) == [],
        str(codes(o)),
    )

    # a directory holds signatures that have nothing to do with each other, so
    # each is its own profile; merging them into one made every repeated
    # declaration across unrelated test files look like a duplicate
    many = os.path.join(d, "many")
    os.makedirs(many, exist_ok=True)
    write(many, "one.eo", NIL_BAD)
    write(many, "two.eo", NIL_BAD)
    rc, o, _ = run("check", many, "--format", "json")
    case("a directory is one profile per file", codes(o) == ["EO0041", "EO0041"], str(codes(o)))

    # a flood is the analyzer's bug, not the signature's: held back, and said
    flood = write(d, "flood.eo", "(declare-const Int Type)\n(declare-consts <numeral> Int)\n"
                  + "".join(f"(declare-const or{i} (-> Bool Bool Bool) :right-assoc-nil 0)\n"
                            for i in range(30)))
    rc, o, _ = run("check", flood, "--format", "json")
    got = collections.Counter(codes(o))
    case("a flooding check is held back", got["EO0041"] == 3 and got["ANO0001"] == 1, str(dict(got)))
    case("and holding it back fails the run", rc == 1, f"exit {rc}")
    rc, o, _ = run("check", flood, "--no-limits", "--format", "json")
    got = collections.Counter(codes(o))
    case("--no-limits reports all of them", got["EO0041"] == 30 and not got["ANO0001"],
         str(dict(got)))

    rc, o, _ = run("check", bad, "--format", "sarif")
    try:
        doc = json.loads(o)
        res = doc["runs"][0]["results"]
        ok = doc["version"] == "2.1.0" and res[0]["ruleId"] == "EO0041"
    except Exception as e:  # noqa: BLE001
        ok, res = False, str(e)
    case("sarif parses and names the rule", ok, "" if ok else str(res))

    # The SARIF URLs are a surface that restates two registers: the repository
    # this tool is published from, and the anchors in the generated check
    # catalogue. Neither comparison existed, and the repository half was wrong
    # -- every SARIF run GitHub ingested pointed at a repository that does not
    # exist. The ground truths are elsewhere on purpose: `CHECKER_REPO`, which
    # the declaration check already depends on, says which repository this is,
    # and `anoieu_analyzer/checks.md` carries the anchors. A test that read the
    # constant it
    # is checking would pass on any value.
    try:
        doc = json.loads(o)
        driver = doc["runs"][0]["tool"]["driver"]
        urls = [driver["informationUri"]] + [r["helpUri"] for r in driver["rules"]]
        expected = "https://github.com/" + CHECKER_REPO
        catalogue = open(os.path.join(ROOT, "anoieu_analyzer", "checks.md")).read()
        anchors = {h.lower() for h in re.findall(r"^## (\S+)", catalogue, re.M)}
        wrong = [u for u in urls if not u.startswith(expected)]
        missing = [r["helpUri"] for r in driver["rules"]
                   if r["helpUri"].rsplit("#", 1)[-1] not in anchors]
    except Exception as e:  # noqa: BLE001
        wrong, missing = [str(e)], []
    case("sarif points at the repository this tool is published from", not wrong, str(wrong))
    case("and every helpUri anchor is one anoieu_analyzer/checks.md carries", not missing, str(missing))

    rc, o, _ = run("check", bad, "--format", "github")
    case("github annotations are emitted", o.startswith("::error file="), o.splitlines()[:1])

    rc, _, err = run("check", bad, "--only", "NOPE0001")
    case("an unknown code is refused", rc == 2 and "no check called" in err, f"exit {rc}")

    rc, _, err = run("check", os.path.join(d, "absent.eo"))
    case("a missing file is refused", rc == 2 and "no such file" in err, f"exit {rc}")

    entry = os.path.join(d, "entry-points")
    os.makedirs(entry)
    fragment = write(entry, "fragment.eo", "(define zero () 0)\n")
    write(entry, "consumer.eo", '(declare-const Int Type)\n'
          '(declare-consts <numeral> Int)\n(include "fragment.eo")\n')
    rc, o, _ = run("check", entry, "--only", "EO0071", "--format", "json")
    case("directory checks a fragment in its consumer's literal context", rc == 0 and not codes(o), o)
    rc, o, _ = run("check", fragment, "--only", "EO0071", "--format", "json")
    case("explicitly naming a fragment still checks it standalone", codes(o) == ["EO0071"], o)
    write(entry, "other.eo", '(include "fragment.eo")\n')
    rc, o, _ = run("check", entry, "--only", "EO0071", "--format", "json")
    case("a second consumer without the declaration is still checked", codes(o) == ["EO0071"], o)
    write(entry, "cycle-a.eo", '(include "cycle-b.eo")\n')
    write(entry, "cycle-b.eo", '(include "cycle-a.eo")\n')
    rc, o, _ = run("check", entry, "--only", "EO0011", "--format", "json")
    case("a directory with a rootless include cycle retains its diagnostic", "EO0011" in codes(o), o)
    from anoieu_analyzer.profiles import profiles
    from anoieu_analyzer.reporting.gen_corpus_table import signatures
    case("CLI and reporting select the same profiles", profiles([entry]) == signatures([entry]))

    from anoieu_analyzer.loader import load
    from anoieu_analyzer.syntax.parser import parse
    from anoieu_analyzer.typing import infer
    cycle = write(d, "alias-cycle.eo", '(define a () b)\n(define b () a)\n')
    sig = load(cycle).signature
    term = parse("probe", "(a true)").forms[0]
    case("type inference terminates on an alias cycle", infer(term, {}, sig) is None)

    return out


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
    print(f"-- {len(results)} case(s), {bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
