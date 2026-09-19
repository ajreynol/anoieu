"""Anoieu's closure adapter against the real pinned Koine programs."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from anoieu_analyzer.reporting import ROOT, koine, verdicts


def main() -> int:
    failures = 0

    def case(label, passed, detail=""):
        nonlocal failures
        print(("ok   " if passed else "FAIL ") + label)
        if not passed:
            failures += 1
            print(detail)

    tool = koine.find(clone=False, programs=("koine_close_db", "koine_window", "koine_check_db"))
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "owner"
        # Exercise real subprocess callbacks in an isolated owner repository.
        for relative in ("prompts/close_bug_db", "anoieu_analyzer/reporting/__init__.py",
                         "anoieu_analyzer/reporting/koine.py", "anoieu_analyzer/reporting/verdicts.py"):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(ROOT) / relative, target)
        config = root / "anoieu_analyzer/reporting/config"
        config.mkdir()
        projects = {n: {"url": f"https://github.com/example/{n}.git", "ref": "release"}
                    for n in ("a", "b", "quiet")}
        (config / "deps.json").write_text(json.dumps(projects))
        (config / "deps.lock").write_text(json.dumps({n: {"commit": "lock-rev"} for n in projects}))
        (root / "bug_db").mkdir()
        db = root / "bug_db/bugs.json"
        rows = [{"id": "shared", "owner": "a+b", "code": "TRI0001", "found_at": "abc1234"},
                {"id": "fuzz", "owner": "a", "code": "FUZ0001"},
                {"id": "closed", "owner": "quiet", "closed_verdict": "declined"}]
        db.write_text(json.dumps({"bugs": rows}))
        before = db.read_bytes()
        env = dict(os.environ, KOINE=tool)

        def run(*args):
            return subprocess.run([sys.executable, str(root / "prompts/close_bug_db"), *args],
                                  cwd=directory, env=env, capture_output=True, text=True)

        result = run("--dry-run")
        case("Koine gets manifest refs, shared ownership and recorded baselines",
             result.returncode == 0 and "a: 2 open observations" in result.stdout
             and "b: 1 open observations" in result.stdout
             and "quiet: nothing open" in result.stdout
             and "/compare/abc1234...release" in result.stdout
             and "1 row(s) record no revision" in result.stdout, result.stderr)
        result = run("a", "--show-prompt", "--date", "2026-10-01")
        case("the shared prompt retains Anoieu's evidence, verdicts and checks",
             result.returncode == 0 and "holds 2 open observations" in result.stdout
             and "## b --" not in result.stdout and "2026-10-01" in result.stdout
             and all(f"`{v}`" in result.stdout for v in verdicts.OUTCOMES)
             and all(s in result.stdout for s in ("candidate for replay", "re-read both sides",
                 "`When`, `Kind`, `Ours`, `Theirs` and `Outcome`", "koine_check_db",
                 "--also awaiting_landing", "reporting.database --check", "Commit nothing")), result.stderr)
        case("previews preserve the owner database", db.read_bytes() == before)
        rows[0]["found_at"] = ""
        db.write_text(json.dumps({"bugs": rows}))
        case("missing observations' revisions fall back to the lock",
             "/compare/lock-rev...release" in run("b", "--dry-run").stdout)
        rows[0]["found_at"] = "abc1234"
        rows[1]["found_at"] = "def5678"
        db.write_text(json.dumps({"bugs": rows}))
        result = run("a", "--dry-run")
        case("ambiguous remote baselines refuse; explicit overrides and scoped runs work",
             result.returncode == 2 and "no oldest revision" in result.stderr
             and run("a", "--since", "a=override", "--dry-run").returncode == 0
             and run("b", "--dry-run").returncode == 0, result.stderr)
        case("unknown local project names refuse", run("--use-local", "unknown", "--dry-run").returncode == 2)
        legacy = Path(directory) / "legacy/bug_db_manager"
        legacy.mkdir(parents=True)
        (legacy / "koine_append_db").touch()
        env["KOINE"] = str(legacy.parent)
        result = run("b", "--dry-run")
        case("append-only Koine cannot supply closure, and previews never clone",
             result.returncode != 0 and "koine_close_db" in result.stderr
             and not (root / "deps").exists(), result.stderr)
        env["KOINE"] = tool

        (root / "docs").mkdir()
        (root / "docs/experience.md").write_text("episode format\n")
        binary = Path(directory) / "codex"
        binary.write_text(f"#!{sys.executable}\nimport os, sys\nprint(os.getcwd())\n"
                          "print(sys.argv[1])\nprint(sys.argv[2])\nsys.exit(17)\n")
        binary.chmod(0o755)
        env["PATH"] = directory + os.pathsep + os.environ["PATH"]
        result = run("b", "--codex", "--print")
        case("the shared launcher receives the assistant mode, owner root and failure status",
             result.returncode == 17 and result.stdout.startswith(f"{root}\nexec\n")
             and "## b -- 1 open observations" in result.stdout, result.stderr)

        history = Path(directory) / "history with spaces"
        history.mkdir()

        def git(*args):
            return subprocess.check_output(["git", "-C", str(history), *args], text=True).strip()

        git("init", "-q")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", "baseline", "--allow-empty")
        base = git("rev-parse", "HEAD")
        rows[0]["found_at"] = base
        rows[1]["found_at"] = ""
        db.write_text(json.dumps({"bugs": rows}))
        result = run("b", "--use-local", f"b={history}", "--show-prompt")
        case("empty local windows start no assistant", result.returncode == 0
             and not result.stdout and "no commit after the baseline" in result.stderr, result.stderr)
        git("-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", "next", "--allow-empty")
        rows[1]["found_at"] = git("rev-parse", "HEAD")
        db.write_text(json.dumps({"bugs": rows}))
        result = run("--use-local", f"a={history}", "--dry-run")
        case("one explicit local project leaves others remote and selects the oldest revision",
             result.returncode == 0 and f"baseline: {base}" in result.stdout
             and "oldest of 2 recorded revisions" in result.stdout
             and f"/compare/{base}...release" in result.stdout, result.stderr)
        # repos.local uses whitespace-separated paths, so use a plain alias.
        alias = Path(directory) / "history"
        alias.symlink_to(history, target_is_directory=True)
        (config / "repos.local").write_text(f"b {alias}\n")
        case("bare local names still resolve through repos.local",
             run("b", "--use-local", "b", "--dry-run").returncode == 0)
        git("-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", "branch-only", "--allow-empty")
        rows[1]["found_at"] = git("rev-parse", "HEAD")
        git("checkout", "-q", "--detach", base)
        git("-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", "other branch", "--allow-empty")
        rows[0]["found_at"] = git("rev-parse", "HEAD")
        db.write_text(json.dumps({"bugs": rows}))
        result = run("a", "--use-local", f"a={history}", "--dry-run")
        case("incomparable local revisions refuse instead of guessing a baseline",
             result.returncode == 2 and "no oldest revision" in result.stderr, result.stderr)
    print(f"-- closure adapter: {failures} failure(s)")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
