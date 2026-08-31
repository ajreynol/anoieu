"""The committed reproducer corpus, and the findings it stands for.

A run writes what it finds to a scratch directory that is not checked in
(`fuzz-findings/`, gitignored). Nothing there is a *finding* in this project's
sense yet: it has not been read, it may be an artefact of the harness, and the
binary it was found against may be somebody's working tree.

**Promotion is the step that makes it one.** `anoieu-fuzz promote` copies a
reproducer into `tests/fuzz/`, where it is committed, and from there it is
exactly like a finding from the checks: it has a code, an owner, a fingerprint,
a row in [`docs/open-findings.md`](../docs/open-findings.md), and it leaves the
open table only when somebody rules on it.

The asymmetry with the checks is worth stating, because it is the reason this
file exists rather than the fuzzer simply writing rows. A check's finding is
re-derived by running the check: the evidence *is* the code in this repository.
A fuzzer's finding cannot be, because re-deriving it means running somebody
else's binary, which CI here does not have. So the evidence is the committed
reproducer plus the recorded verdicts -- the same arrangement, and for the same
reason, as `tests/oracle.json`: written by a real run, never by hand, and
checkable by anyone who has the binary.
"""

from __future__ import annotations

import json
import os
import shutil

from anoieu.diagnostics import Diagnostic, Severity, Span, SourceMap
from anoieu.fingerprint import fingerprint

from .codes import CODES, code_for

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Where a promoted reproducer lives. Beside `tests/witnesses/`, which is the
#: same idea for the checks: one directory, one case, readable in a minute.
CORPUS = os.path.join(ROOT, "tests", "fuzz")


def load(corpus: str = "") -> list[dict]:
    """Every promoted finding, newest arrangement first read off disk."""
    corpus = corpus or CORPUS
    out = []
    if not os.path.isdir(corpus):
        return out
    for name in sorted(os.listdir(corpus)):
        path = os.path.join(corpus, name, "finding.json")
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            record = json.load(f)
        record["bucket"] = record.get("bucket", name)
        record["dir"] = os.path.join(corpus, name)
        record["case"] = _case_path(record["dir"])
        out.append(record)
    return out


def _case_path(directory: str) -> str:
    for name in sorted(os.listdir(directory)):
        if name.startswith("case."):
            return os.path.join(directory, name)
    return ""


def _first_command(text: str) -> tuple[int, str]:
    """The line a diagnostic should point at: the first that is not a comment.

    A reproducer opens with the header comment the generator wrote, and
    pointing at that would make every finding's fingerprint depend on the seed
    it happened to be generated from.
    """
    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip() and not line.lstrip().startswith(";"):
            return i, line
    return 1, text.splitlines()[0] if text.splitlines() else ""


def diagnostic(record: dict, sources: SourceMap | None = None) -> Diagnostic:
    """One promoted finding, as the same object a check yields.

    Everything downstream -- the text renderer, `--format sarif`, the
    fingerprint, the row in the ledger -- then works on it without knowing it
    came from a fuzzer rather than from a pass over a signature.
    """
    case = record.get("case") or ""
    text = ""
    if case and os.path.isfile(case):
        with open(case, errors="replace") as f:
            text = f.read()
    line, line_text = _first_command(text)
    if sources is not None and case:
        sources.add(case, text)

    spec = code_for(record["kind"])
    outcomes = record.get("outcomes", [])
    notes = [f"{o['checker']}: {o['status']}" + (f" -- {o['detail']}" if o.get("detail") else "")
             for o in outcomes]
    notes.append(
        f"found by the anoieu fuzzer in {record.get('mode', '?')} mode"
        + (f", from {record['source']}" if record.get("source") else "")
    )
    if record.get("note"):
        notes.append(record["note"])
    rel = os.path.relpath(case, ROOT) if case else record.get("bucket", "?")
    return Diagnostic(
        code=spec.code,
        severity=spec.severity,
        message=record.get("summary", spec.title),
        span=Span(case or rel, line, 1, line, max(2, len(line_text) + 1)),
        label="this file",
        notes=notes,
        help=f"confirm it with `python3 -m anoieu_fuzz replay {rel}`, "
        f"and read `python3 -m anoieu_fuzz explain {spec.code}`",
    )


def owner_of(record: dict) -> str:
    """Whose defect this is, as far as a fuzzer can say.

    A crash belongs to the checker that crashed. A disagreement belongs to
    nobody yet -- that is the whole content of the finding -- so it is filed
    against both until somebody rules on it, and the review step that moves the
    row is where it acquires one owner.
    """
    if record.get("owner"):
        return record["owner"]
    names = [o["checker"].split(" ")[0] for o in record.get("outcomes", [])
             if o.get("coarse") != "skipped"]
    seen: list[str] = []
    for n in names:
        if n not in seen:
            seen.append(n)
    if record.get("kind") in ("crash", "unexplained", "timeout"):
        bad = [o["checker"].split(" ")[0] for o in record.get("outcomes", [])
               if o.get("coarse") == "abnormal"]
        return bad[0] if bad else (seen[0] if seen else "—")
    return "+".join(seen) if seen else "—"


def rows(corpus: str = "") -> dict[str, dict]:
    """Every promoted finding as a row for `docs/open-findings.md`.

    The shape is `tools/gen_open_findings.py`'s, keyed by the same fingerprint,
    so the generator merges these with what the checks report and neither side
    knows about the other.
    """
    out: dict[str, dict] = {}
    for record in load(corpus):
        sources = SourceMap()
        diag = diagnostic(record, sources)
        key = fingerprint(diag, sources, ROOT)
        where = os.path.relpath(diag.span.path, ROOT)
        out[key] = {
            "owner": owner_of(record),
            "code": diag.code,
            "where": f"{where}:{diag.span.line}",
            "what": diag.message.replace("|", "\\|"),
        }
    return out


def promote(source: str, corpus: str = "", owner: str = "", note: str = "") -> str:
    """Copy one reproducer out of a run's output and into the committed corpus.

    Deliberately a command somebody types. A run can produce a bucket that is
    an artefact of this harness -- a mutated `include` pointing nowhere was the
    first one -- and a fuzzer that filed its own output would be publishing
    faster than anybody could read it, which is the one thing
    `docs/philosophy.md` asks us not to do.
    """
    corpus = corpus or CORPUS
    record_path = os.path.join(source, "finding.json")
    if not os.path.isfile(record_path):
        raise FileNotFoundError(f"no finding.json in {source}")
    with open(record_path) as f:
        record = json.load(f)
    bucket = record.get("bucket") or os.path.basename(os.path.normpath(source))
    where = os.path.join(corpus, bucket)
    if os.path.isdir(where):
        raise FileExistsError(f"{os.path.relpath(where, ROOT)} is already promoted")
    os.makedirs(where, exist_ok=True)
    for name in sorted(os.listdir(source)):
        if name.startswith("case."):
            shutil.copy2(os.path.join(source, name), os.path.join(where, name))
    record["bucket"] = bucket
    if owner:
        record["owner"] = owner
    if note:
        record["note"] = note
    with open(os.path.join(where, "finding.json"), "w") as f:
        json.dump(record, f, indent=1, sort_keys=True)
    return where


def explain(code: str) -> str:
    spec = CODES.get(code.upper())
    if spec is None:
        return ""
    return f"-- {spec.code}  {spec.title}\n   severity: {spec.severity.value}\n\n{spec.page}\n"


def render(records: list[dict], fmt: str = "text", color: bool = False) -> str:
    """Findings in whichever shape the reader is: a terminal, an editor, CI.

    The four renderers are anoieu's, unchanged. A fuzzer finding and a check
    finding therefore land in a GitHub annotation or a SARIF report looking
    like what they are -- two findings from one project -- distinguished by
    their code and by nothing else they have to remember to do.
    """
    from anoieu.diagnostics import (  # noqa: PLC0415
        render_github,
        render_json,
        render_sarif,
        render_text,
    )

    sources = SourceMap()
    diags = [diagnostic(r, sources) for r in records]
    if fmt == "json":
        return render_json(diags, ROOT)
    if fmt == "sarif":
        return render_sarif(diags, ROOT)
    if fmt == "github":
        return render_github(diags, ROOT)
    return render_text(diags, sources, ROOT, color=color)
