#!/usr/bin/env python3
"""End-to-end cases for the parts of the tool a CI job depends on.

The witness suite says what each check reports. This says what a *run* does with
those findings: that a comment silences one, that a baseline holds one, that a
configuration file is read, and that the machine-readable formats parse. Every
case is the command a repository would actually run.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        [sys.executable, "-m", "anoieu", *argv],
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

    rc, o, _ = run("check", bad, "--format", "sarif")
    try:
        doc = json.loads(o)
        res = doc["runs"][0]["results"]
        ok = doc["version"] == "2.1.0" and res[0]["ruleId"] == "EO0041"
    except Exception as e:  # noqa: BLE001
        ok, res = False, str(e)
    case("sarif parses and names the rule", ok, "" if ok else str(res))

    rc, o, _ = run("check", bad, "--format", "github")
    case("github annotations are emitted", o.startswith("::error file="), o.splitlines()[:1])

    rc, _, err = run("check", bad, "--only", "NOPE0001")
    case("an unknown code is refused", rc == 2 and "no check called" in err, f"exit {rc}")

    rc, _, err = run("check", os.path.join(d, "absent.eo"))
    case("a missing file is refused", rc == 2 and "no such file" in err, f"exit {rc}")

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
