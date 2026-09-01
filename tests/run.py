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
import contextlib
import difflib
import io
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


def inventory_well_formed() -> int:
    """`tools/ecosystem.json` read as a document about itself.

    The offline half of `tools/ecosystem.py --check`, run here so that editing
    the inventory fails at the moment somebody edits it rather than in CI. The
    other half asks each remote whether what we record is still true, and needs
    a network, so it stays a CI step and is not run from the suite.
    """
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
    import ecosystem  # noqa: PLC0415

    inv = {k: v for k, v in json.load(open(ecosystem.INVENTORY)).items()
           if not k.startswith("_")}
    bad = ecosystem.well_formed(inv)
    for b in bad:
        print(f"FAIL {b}")

    # And the table still prints, for a row that resolves to a checkout. `--check`
    # was added as a second function named `check`, which shadowed the one the
    # table calls; nothing here noticed, because nothing ran the tool the way a
    # person runs it. **One resolvable checkout is the whole point**: with none,
    # every row takes the `no checkout` branch and the shadowed call is never
    # reached, which is how the first version of this test passed against the
    # bug it was written for. This repository is the checkout, so the mapping is
    # true and the run costs one policy check.
    root = os.path.dirname(HERE)
    mapping = os.path.join(HERE, "repos.local.test")
    with open(mapping, "w") as f:
        f.write(f"anoieu {root}\n")
    env = dict(os.environ, ANOIEU_REPOS=os.path.join(HERE, "no-such-dir"),
               ANOIEU_REPOS_FILE=mapping)
    out = subprocess.run([sys.executable, os.path.join(root, "tools", "ecosystem.py")],
                         capture_output=True, text=True, env=env, timeout=120)
    os.remove(mapping)
    if out.returncode != 0 or not re.search(r"^anoieu\s+member\s", out.stdout, re.M):
        print(f"FAIL tools/ecosystem.py with no arguments exited {out.returncode}: "
              f"{(out.stderr or out.stdout).strip().splitlines()[-1:]}")
        bad = bad + ["the default mode"]
    print(f"-- the inventory is well formed, and the table prints: "
          f"{len(bad)} failure(s), {len(inv)} entries")
    return len(bad)


def install_commands() -> int:
    """`scripts/install_eo` installs with `git clone`, and with nothing else.

    It is the one command in this repository that changes a machine outside it,
    so what it may execute is checked rather than promised. Three questions, all
    answerable without a network and without cloning anything: what the dry run
    prints, what a real run would hand to `execute`, and whether anything else
    could be run at all. A command added to this script fails here, which is the
    point -- an install that quietly grew a `curl` would otherwise be reviewed
    once, by whoever wrote it.
    """
    import importlib.machinery  # noqa: PLC0415
    import importlib.util  # noqa: PLC0415
    import io  # noqa: PLC0415
    from contextlib import redirect_stdout  # noqa: PLC0415

    path = os.path.join(os.path.dirname(HERE), "scripts", "install_eo")
    loader = importlib.machinery.SourceFileLoader("install_eo", path)
    spec = importlib.util.spec_from_loader("install_eo", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    failures = 0
    source = open(path).read()

    #: What a line of the dump may start with. `mkdir` and `cd` are printed for
    #: a person pasting it; the script itself makes the directory with
    #: os.makedirs and passes cwd=, so neither is ever executed here.
    allowed = ("mkdir -p ", "cd ", "git clone ")

    fake = os.path.join(HERE, "no-such-root-for-a-test")
    out = io.StringIO()
    with redirect_stdout(out):
        mod.dump(fake, mod.plan())
    live = [l for l in out.getvalue().splitlines() if l.strip() and not l.startswith("#")]
    stray = [l for l in live if not l.startswith(allowed)]
    if stray:
        print(f"FAIL install_eo prints {len(stray)} line(s) that are not "
              f"mkdir, cd or git clone: {stray[:3]}")
        failures += 1
    else:
        print(f"ok   install_eo prints only mkdir, cd and git clone ({len(live)} lines)")

    bad = [" ".join(r.command()) for r in mod.plan()
           if tuple(r.command()[:2]) != mod.INSTALL]
    if bad:
        print(f"FAIL install_eo would run something other than git clone: {bad}")
        failures += 1
    else:
        print("ok   and every command it would run is a git clone")

    refused = 0
    for cmd in (["rm", "-rf", "/"], ["git", "push"], ["curl", "http://example"],
                ["git", "clone; rm -rf /"]):
        try:
            mod.execute(cmd, HERE)
            print(f"FAIL install_eo executed {cmd}")
        except SystemExit:
            refused += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL install_eo raised {type(e).__name__} rather than refusing {cmd}")
    if refused == 4:
        print("ok   and refuses anything else at run time, rather than trusting the caller")
    else:
        failures += 1

    try:
        mod.git(HERE, "push")
        print("FAIL install_eo would run `git push` against a checkout")
        failures += 1
    except SystemExit:
        print("ok   and asks a checkout only for reads")

    for smell in ("shell=True", "os.system", "os.popen", "check_output"):
        if smell in source:
            print(f"FAIL install_eo contains {smell}")
            failures += 1
    starts = source.count("subprocess.run")
    if starts != 2:
        print(f"FAIL install_eo starts a process in {starts} places; "
              "the audit knows about two, in execute and git")
        failures += 1
    else:
        print("ok   and starts a process in exactly two places, both checked above")

    print(f"-- the install script: {failures} failure(s)")
    return failures


def postmortem_shape() -> int:
    """The log's own conventions, since a convention nothing checks is a wish.

    One `Tool:`/`Summary:`/`Resolution:` block per run, none on the sections
    beneath it, and a summary short enough to stay a summary. The shape is
    written out in docs/reports/postmortem.md itself; this is the half a reader cannot
    enforce by reading.
    """
    LIMIT, SENTENCES = 250, 2
    path = os.path.join(os.path.dirname(HERE), "docs", "reports", "postmortem.md")
    text = re.sub(r"```.*?```", "", open(path).read(), flags=re.S)  # not the template

    # a run section is a level-2 heading that starts with a date
    runs = re.split(r"^## (?=\d{4}-\d{2}-\d{2} )", text, flags=re.M)[1:]
    failures = 0
    if not runs:
        print("FAIL docs/reports/postmortem.md has no run sections")
        return 1

    for run in runs:
        title = run.splitlines()[0].strip()
        head, _, rest = run.partition("\n### ")
        for field in ("Tool:", "Summary:", "Resolution:"):
            n = len(re.findall(rf"^\*\*{field}\*\*", head, re.M))
            if n != 1:
                print(f"FAIL postmortem {title!r}: {n} {field} lines above the "
                      f"sections, expected 1")
                failures += 1
        stray = re.findall(r"^\*\*(Tool|Summary|Resolution):\*\*", rest, re.M)
        if stray:
            print(f"FAIL postmortem {title!r}: {sorted(set(stray))} on a section; "
                  "those fields belong to the run, not to a finding")
            failures += 1

        m = re.search(r"^\*\*Summary:\*\* (.+?)(?=\n\*\*|\n\n|\Z)", head, re.S | re.M)
        if not m:
            continue
        summary = " ".join(m.group(1).split())
        if len(summary) > LIMIT:
            print(f"FAIL postmortem {title!r}: summary is {len(summary)} "
                  f"characters, at most {LIMIT}")
            failures += 1
        n = len(re.findall(r"[.!?](?:\s|$)", summary))
        if n > SENTENCES:
            print(f"FAIL postmortem {title!r}: summary is {n} sentences, "
                  f"at most {SENTENCES}")
            failures += 1

    print(f"-- the postmortem log: {len(runs)} run(s), {failures} failure(s)")
    return failures


def prompts_agree() -> int:
    """The two scripts say what `docs/reports/reporting-workflow.md` says they say.

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
    doc = open(os.path.join(root, "docs", "reports", "reporting-workflow.md")).read()

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
    SWEEP, POSTM = "-- or, for the sweep form --", "-- or, with --no-postm --"

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
         ["bash", "scripts/prompts/check_anoieu", "--show-prompt", "ID"],
         resolve(one, SWEEP, alt=False),
         lambda s: s.replace("anoieu-ID", "BRANCH")),
        ("check_anoieu, the sweep",
         ["bash", "scripts/prompts/check_anoieu", "--show-prompt"],
         resolve(one, SWEEP, alt=True).replace("PROJECT", "anoieu"),
         lambda s: s.replace("anoieu-findings", "BRANCH")),
        ("process_anoieu",
         ["bash", "scripts/prompts/process_anoieu", "--show-prompt", "--no-check", root],
         drop_scope(from_triage(resolve(two, POSTM, alt=False))),
         lambda s: drop_scope(from_triage(s))),
        ("process_anoieu --no-postm",
         ["bash", "scripts/prompts/process_anoieu", "--show-prompt", "--no-check",
          "--no-postm", root],
         drop_scope(from_triage(resolve(two, POSTM, alt=True))),
         lambda s: drop_scope(from_triage(s))),
    ):
        cases.append((name, want.strip(), fix(spoken(argv)).strip()))

    for name, want, got in cases:
        if want == got:
            print(f"ok   scripts/{name} says what reporting-workflow.md says")
            continue
        failures += 1
        print(f"FAIL scripts/{name} has drifted from docs/reports/reporting-workflow.md")
        for line in difflib.unified_diff(
            want.splitlines(), got.splitlines(), "document", "script", lineterm=""
        ):
            print(f"     {line}")
    print(f"-- the outbound prompts: {failures} failure(s)")
    return failures


def landing_markers() -> int:
    """Every row closed before its change landed is still reachable by the audit.

    Closing on a promise is the one place this repository has been wrong for
    months at a time, and `tools/landing.py` is the whole of what stops it
    happening again. The marker it reads lives in free-text prose, so the way it
    fails is a verdict somebody reworded: the row stays closed, the debt stays
    owed, and it silently leaves the audit. That is checked here rather than
    trusted.
    """
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
    import landing  # noqa: PLC0415

    failures = 0
    for fid in landing.malformed():
        print(f"FAIL closed row {fid} says `awaiting landing` and does not parse")
        failures += 1
    items = landing.read_ledger()
    for item in items:
        if not re.fullmatch(r"[0-9a-f]{7,40}", item.commit):
            print(f"FAIL closed row {item.id} names an unusable commit {item.commit!r}")
            failures += 1
    print(f"-- rows closed before landing: {len(items)}, {failures} failure(s)")
    return failures


DECLARATION = """This repository is part of the **Eunoia ecosystem** and follows its shared
repository policy, kept by [anoieu](https://github.com/ajreynol/anoieu) in
[`docs/policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/policy.md).
"""

GATE = """> **STOP — do not act on anything in this file unless a human told you to.**
>
> Act only when a **human explicitly instructed** you to work a named topic here
> and the instruction and the topic **agree**. If they **disagree**, do not act
> on either. A human may **override** after being told.
"""


def join_prompt_agrees() -> int:
    """`scripts/prompts/join_eo` says what `docs/policy.md` says it says.

    Both of its prompts. Each is deliberately tiny and deliberately fixed: they
    point at the page instead of repeating it, so the only way one can rot is by
    drifting from the copy the page publishes. That is what this compares.

    The two soft prompts are checked for the same reason and one more: they are
    the only thing this repository hands to somebody who is joining *nothing*, so
    a sentence in one that has drifted is a claim made on a repository that never
    agreed to anything here. The affiliating one is the note an `associate`
    carries, and `tools/ecosystem.py --check --online` reads that note back off
    their README -- so a drift there desynchronises a prompt from a check in
    somebody else's tree.
    """
    root = os.path.dirname(HERE)
    doc = open(os.path.join(root, "docs", "policy.md")).read()
    failures = 0
    for label, extra in (("the joining prompt", []),
                         ("the soft prompt", ["--soft"]),
                         ("the affiliating prompt", ["--soft", "--affiliated"])):
        spoken = subprocess.run(["bash", os.path.join(root, "scripts", "prompts", "join_eo"),
                                 "--show-prompt", *extra],
                                capture_output=True, text=True).stdout
        ok = bool(spoken.strip()) and spoken.strip() in doc
        print(("ok   " if ok else "FAIL ")
              + f"scripts/prompts/join_eo, {label}, says what docs/policy.md says")
        if not ok:
            print("     the prompt is not in the page verbatim; one of them moved")
            failures += 1
    print(f"-- the joining prompts: {failures} failure(s)")
    return failures


def note_forms() -> int:
    """The three maintenance notes `docs/policy.md` publishes, read by the two
    readers that decide a footing.

    A member's declaration and the two things a prospective associate might be
    asked for are all a paragraph in somebody else's README, and
    `tools/ecosystem.py` tells them apart from a remote. Getting that wrong is
    not a failed build: it is this repository recording a footing that is not
    true, about a repository that never agreed to anything.

    `note_in` is the drafted associate protocol and is the loosest of the three,
    so the case that matters is the bare note -- accepted by it, and refused by
    both of the others.

    The templates are pulled from the page rather than typed here, so editing one
    of them fails this test rather than silently changing what a footing means.
    """
    root = os.path.dirname(HERE)
    sys.path.insert(0, os.path.join(root, "tools"))
    import policy_check  # noqa: PLC0415

    doc = open(os.path.join(root, "docs", "policy.md")).read()

    def template(after: str) -> str:
        chunk = doc[doc.index(after):]
        return re.search(r"```markdown\n(.*?)\n```", chunk, re.S).group(1)

    joined = template("### 1. Declare it, at the top of your maintenance note")
    independent = template("### The soft form: the note without the membership")
    affiliating = template("**There is a second form, for a repository that is happy")

    bare = ("# A tool\n\n## How this repository is maintained\n\nWritten by one "
            "person in their own time, reviewed by nobody, and nothing here has "
            "been checked by a second reader.\n")

    # (label, text, is a member's declaration?, the affiliating note?, any note?)
    cases = [
        ("the membership declaration", joined, True, False, True),
        ("the independent soft note", independent, False, False, True),
        ("the affiliating soft note", affiliating, False, True, True),
        ("a bare maintenance note", bare, False, False, True),
        ("no maintenance note at all", "# A tool\n\nWhat it does.\n", False, False, False),
    ]
    failures = 0
    for label, text, want_member, want_assoc, want_note in cases:
        is_member = not policy_check.declaration_in(text)
        is_assoc = not policy_check.affiliation_in(text)
        has_note = not policy_check.note_in(text)
        for got, want, reader in ((is_member, want_member, "declaration_in"),
                                  (is_assoc, want_assoc, "affiliation_in"),
                                  (has_note, want_note, "note_in")):
            ok = got == want
            failures += 0 if ok else 1
            print(("ok   " if ok else "FAIL ")
                  + f"{reader} {'accepts' if want else 'refuses'} {label}")
    print(f"-- the maintenance notes a footing rests on: {failures} failure(s)")
    return failures


def protocol_report() -> int:
    """`tools/ecosystem.py --protocol` reports the right column for each tree.

    The readers are witnessed above; this is the wiring around them, which is the
    half that had never produced a `yes` when it was written. It runs offline
    against three synthetic READMEs, because the real one reads somebody else's
    repository and a test that needed the network would be a test nobody runs.

    It also pins the property the report exists for: **it never fails.** A tool
    in this table is held to none of this repository's policy and the protocol it
    is being read against is not decided, so a non-zero exit would be this
    repository grading somebody against a rule that does not exist.
    """
    root = os.path.dirname(HERE)
    sys.path.insert(0, os.path.join(root, "tools"))
    import ecosystem  # noqa: PLC0415

    doc = open(os.path.join(root, "docs", "policy.md")).read()

    def template(after: str) -> str:
        chunk = doc[doc.index(after):]
        return re.search(r"```markdown\n(.*?)\n```", chunk, re.S).group(1)

    trees = {
        "nothing": "# A tool\n\nWhat it does.\n",
        "affiliated": template("**There is a second form, for a repository that is happy"),
        "joined": template("### 1. Declare it, at the top of your maintenance note"),
    }
    inv = {n: {"status": "candidate", "proposed": "associate", "repo": n,
               "url": f"https://github.com/x/{n}", "vetted": "2026-09-01",
               "what": "-", "why": "-"} for n in trees}
    # `ignored` must not appear: it is neither an associate nor proposed as one.
    inv["ignored"] = {"status": "candidate", "repo": "ignored",
                      "url": "https://github.com/x/ignored", "what": "-"}

    want = {"nothing": ("no", "no", "no"), "affiliated": ("yes", "yes", "no"),
            "joined": ("yes", "no", "yes")}

    real, buf = ecosystem.readme_for, io.StringIO()
    ecosystem.readme_for = lambda name, e: (trees.get(name, ""), "checkout")
    try:
        with contextlib.redirect_stdout(buf):
            code = ecosystem.protocol(inv)
    finally:
        ecosystem.readme_for = real
    out = buf.getvalue()

    failures = 0
    for name, cols in want.items():
        row = next((l for l in out.splitlines() if l.startswith(name)), "")
        got = tuple(row.split()[3:6])
        ok = got == cols
        failures += 0 if ok else 1
        print(("ok   " if ok else "FAIL ")
              + f"--protocol reads {name} as note={cols[0]} "
                f"affiliating={cols[1]} declares={cols[2]}"
              + ("" if ok else f" -- got {got}"))
    for label, ok in (("it never fails", code == 0),
                      ("a tool that is neither is left out", "ignored" not in out)):
        failures += 0 if ok else 1
        print(("ok   " if ok else "FAIL ") + f"--protocol: {label}")
    print(f"-- the associate protocol report: {failures} failure(s)")
    return failures


def epoch_gate() -> int:
    """`tools/bump_check.py` refuses everything that is not a finished green run.

    This is the gate a downstream member puts in front of adopting a stretch, so
    the expensive direction is **letting something through**: a member that
    refuses wrongly tries again tomorrow, and one that adopts wrongly has pinned
    itself to a commit our own CI rejected. Every case below that is not an
    unambiguous pass is therefore asserted to refuse.

    Offline in full. The real thing reads a remote, and a test that needed the
    network is a test nobody runs.
    """
    root = os.path.dirname(HERE)
    sys.path.insert(0, os.path.join(root, "tools"))
    import bump_check  # noqa: PLC0415

    def run(name, status="completed", conclusion="success"):
        return {"name": name, "status": status, "conclusion": conclusion}

    cases = [
        ("a finished green run", [run("policy")], 0),
        ("green with a skipped job", [run("policy"), run("x", conclusion="skipped")], 0),
        ("a neutral job", [run("policy"), run("x", conclusion="neutral")], 0),
        ("one failing job", [run("policy"), run("x", conclusion="failure")], 1),
        ("a cancelled job", [run("policy", conclusion="cancelled")], 1),
        ("a job still running", [run("policy"), run("x", status="in_progress")], 2),
        ("a queued job", [run("policy", status="queued")], 2),
        ("no runs at all", [], 2),
    ]
    failures = 0
    for label, runs, want in cases:
        got, why = bump_check.verdict(runs)
        ok = got == want
        failures += 0 if ok else 1
        verb = {0: "adopts", 1: "refuses", 2: "refuses as unverified"}[want]
        print(("ok   " if ok else "FAIL ") + f"bump_check {verb} {label}"
              + ("" if ok else f" -- got {got}: {why}"))

    import tempfile  # noqa: PLC0415

    tmp = tempfile.mkdtemp(prefix="anoieu-epoch-")
    wf = os.path.join(tmp, ".github", "workflows")
    os.makedirs(wf)
    open(os.path.join(wf, "anoieu.yml"), "w").write(
        "jobs:\n  policy:\n    steps:\n      - env:\n          ANOIEU_REV: 441b562\n")
    rev, why = bump_check.pinned_rev(tmp)
    for label, ok in (("reads a member's pinned commit", rev == "441b562" and not why),
                      ("says so when a member pins nothing",
                       bump_check.pinned_rev(HERE)[0] == ""
                       and bool(bump_check.pinned_rev(HERE)[1]))):
        failures += 0 if ok else 1
        print(("ok   " if ok else "FAIL ") + f"bump_check {label}")

    # the version markers the internal tools read
    open(os.path.join(wf, "anoieu.yml"), "a").write("          EUNOIA_EPOCH: E7\n")
    marks = [
        ("reads a recorded epoch marker", bump_check.epoch_marker(tmp) == "E7"),
        ("reports no marker as absent, never as a failure",
         bump_check.epoch_marker(HERE) == ""),
        ("reads the current stretch from the log",
         re.fullmatch(r"E\d+", bump_check.current_stretch(root) or "") is not None),
    ]
    for label, ok in marks:
        failures += 0 if ok else 1
        print(("ok   " if ok else "FAIL ") + f"bump_check {label}")

    print(f"-- the epoch gate: {failures} failure(s)")
    return failures


def epoch_surfaces_agree() -> int:
    """Every place that restates the epoch commands or statuses says the same
    thing as the register it copies.

    `epoch help` prints the command set; the syntax-error example prints it
    again; the help block prints the status vocabulary a third time. Each is a
    **copy**, and this repository's own position is that a declared ground truth
    with copies and no comparison is the worst of the three ways it goes wrong,
    because it looks safe. So the comparison exists, and it is this.

    Ground truth is the command table in `docs/interface.md` and the status table
    in `docs/stretch-policy.md`. Where a copy disagrees, the table is right.
    """
    root = os.path.dirname(HERE)
    iface = open(os.path.join(root, "docs", "interface.md")).read()
    policy = open(os.path.join(root, "docs", "stretch-policy.md")).read()

    truth_cmds = set(re.findall(r"^\| `((?:epoch|make) [a-z]+(?: [a-z]+)?)` \|",
                                iface, re.M))
    block = re.search(r"```text\n(epoch \u2014 .*?)\n```", iface, re.S)
    truth_stat = set(re.findall(
        r"^\| `(brainstorm|planned|staged|deployed|installed)` \|", policy, re.M))

    failures = 0

    def case(label, got, want):
        nonlocal failures
        ok = got == want
        failures += 0 if ok else 1
        print(("ok   " if ok else "FAIL ") + label
              + ("" if ok else f"\n     copy has {sorted(got)}\n     table has {sorted(want)}"))

    if not block:
        print("FAIL the `epoch help` output block is not in docs/interface.md")
        print("-- the epoch surfaces: 1 failure(s)")
        return 1
    helptext = block.group(1)

    def part(head):
        m = re.search(rf"^{head}(.*?)(?:\n\n|\Z)", helptext, re.S | re.M)
        return m.group(1) if m else ""

    case("`epoch help` lists exactly the commands the table defines",
         set(re.findall(r"^  ((?:epoch|make) [a-z]+(?: [a-z]+)?)\s{2,}\S",
                        part("commands:"), re.M)),
         truth_cmds)
    case("the syntax-error example accepts exactly those commands",
         {c.strip() for c in re.search(r"accepted: (.+)", iface).group(1).split("|")},
         truth_cmds)
    case("`epoch help` names exactly the statuses the policy defines",
         # the whole `status:` block, not just its first line -- a status named
         # on a continuation line is still a copy and still has to agree
         set(re.findall(r"[a-z]+", part("status:")))
         & {"brainstorm", "planned", "staged", "deployed", "installed"},
         truth_stat)

    print(f"-- the epoch surfaces: {failures} failure(s)")
    return failures


def adoption_interface() -> int:
    """`policy_check.py --root` is what another repository runs in its own CI.

    It is a published interface with somebody else's build hanging off it, so it
    is tested here rather than trusted: a repository that declares membership and
    keeps the shape passes, and one that keeps the shape but declares nothing
    fails. Both halves, because a declaration nothing backs and a compliant tree
    that says nothing are the two ways this can be got wrong.
    """
    import shutil  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    checker = os.path.join(os.path.dirname(HERE), "tools", "policy_check.py")
    failures = 0
    tmp = tempfile.mkdtemp(prefix="anoieu-adopt-")
    try:
        for declares, want in ((True, 0), (False, 1)):
            root = os.path.join(tmp, "yes" if declares else "no")
            os.makedirs(os.path.join(root, "docs"))
            subprocess.run(["git", "-C", root, "init", "-q"], check=True)
            open(os.path.join(root, "README.md"), "w").write(
                "# faketool\n\nA thing.\n\n## The name\n\nfaketool, because it is fake.\n"
                "\n## How this repository is maintained\n\n"
                + (DECLARATION if declares else "") + "\nBy a person.\n")
            open(os.path.join(root, "docs", "discussion.md"), "w").write(
                "# Discussion\n\n" + GATE + "\n## D1 — hello\n\n"
                "**To:** anoieu\n**Kind:** notice\n**Status:** open\n"
                "**Opened:** 2026-08-31\n**Settles when:** somebody says so\n\nWe exist.\n")
            open(os.path.join(root, "docs", "README.md"), "w").write(
                "# The documentation\n\n| document | its job |\n| --- | --- |\n"
                "| [`discussion.md`](discussion.md) | the channel |\n")
            open(os.path.join(root, ".gitignore"), "w").write("scratch/\n*.local.md\n")
            # A child project with its own docs/, linking into it the way a
            # child project does. This once failed: the link checker forced
            # every `docs/...` target to resolve from the repository root, so a
            # correct relative link inside tools/<child>/ was reported dead --
            # a check firing on something that was not a problem, which is ours.
            os.makedirs(os.path.join(root, "tools", "kalon", "docs"))
            open(os.path.join(root, "tools", "kalon", "docs", "design.md"), "w").write(
                "# design\n")
            open(os.path.join(root, "tools", "kalon", "README.md"), "w").write(
                "# kalon\n\n*\u03ba\u03b1\u03bb\u03cc\u03bd, the fitting thing.*\n\n"
                "A child project. It does not ship anything.\n\n"
                "See [the design](docs/design.md).\n")
            subprocess.run(["git", "-C", root, "add", "-A"], check=True,
                           capture_output=True)
            subprocess.run(["git", "-C", root, "-c", "user.email=t@t", "-c",
                            "user.name=t", "commit", "-qm", "x"], check=True,
                           capture_output=True)
            got = subprocess.run([sys.executable, checker, "--root", root],
                                 capture_output=True, text=True)
            ok = got.returncode == want
            failures += 0 if ok else 1
            print(("ok   " if ok else "FAIL ")
                  + ("a repository that declares membership and keeps the shape passes"
                     if declares else
                     "a repository that keeps the shape but declares nothing fails"))
            if not ok:
                print(f"     exit {got.returncode}, wanted {want}")
                print("     " + got.stdout.strip().replace("\n", "\n     "))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"-- the adoption interface: {failures} failure(s)")
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
    failures += join_prompt_agrees()
    failures += note_forms()
    failures += protocol_report()
    failures += epoch_gate()
    failures += epoch_surfaces_agree()
    failures += adoption_interface()
    failures += postmortem_shape()
    failures += install_commands()
    failures += inventory_well_formed()
    failures += landing_markers()

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
