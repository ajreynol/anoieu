#!/usr/bin/env python3
"""Count what the checks report on the signatures we can find.

A library rather than a command: `tools/run.py` writes `docs/corpus.md` from
`measure_all()` and `render()` here, together with the versions those counts are
relative to, because a count without a version is a number that was true once.

    python3 tools/run.py            # rewrite docs/corpus.md
    python3 tools/run.py --check    # exit 1 if it is stale

A staleness failure means one of two things, and both are worth a look: upstream
moved, or a check of ours changed what it reports. Neither is an error in
itself, and the diff says which.

The table counts findings. It is not a score and not a comparison between
repositories: a corpus with fewer findings has not been shown to be better, only
to have tripped fewer of the checks that exist. See *What we do not publish* in
the top-level README.
"""

from __future__ import annotations

import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anoieu.checks import Context, load_checks, run_all  # noqa: E402
from anoieu.cli import _embedding_vocabulary  # noqa: E402
from anoieu.diagnostics import Severity  # noqa: E402
from anoieu.loader import load  # noqa: E402
from anoieu.semantics import load_set  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each target: a label, the signatures of one profile, and optionally the other
# legs of a triple. Paths are relative to a repository root named below.
TARGETS = [
    ("CPC", "cvc5", ["proofs/eo/cpc/Cpc.eo"], None),
    (
        "CPC with the expert signature",
        "cvc5",
        ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
        None,
    ),
    ("ethos test signatures", "ethos", ["tests"], None),
    ("logos installed definitions", "logos", ["install/defs"], None),
    # `examples/hello` only: `examples/cpc` is a vendored copy of cvc5's
    # signature, so checking it reports cvc5's findings under eudaimonia's name.
    ("eudaimonia examples", "eudaimonia", ["examples/hello"], None),
    (
        "the CPC triple",
        "cvc5",
        ["proofs/eo/cpc/Cpc.eo"],
        {
            "semantics": ("logos", "install/defs/Cpc.eos"),
            "smt": ("ethos", "tools/eoc/semantics/smt.eos"),
            "embedding": ("ethos", "plugins/model_smt/model_smt.eo"),
        },
    ),
]

# Files a project carries but is not the author of, and which are therefore not
# audited at all. Reporting against one puts somebody else's findings under its
# name, and the copy having drifted from the original is a different question
# from the original being wrong -- one that belongs to whatever keeps the two in
# sync rather than to a static analyzer.
#
# `logos/install/defs/Cpc.cached.eo` is a copy of cvc5's `Cpc.eo`, which is the
# ground truth; cvc5's CI is the planned place for the sync check. Eudaimonia's
# `examples/cpc` is the same situation, handled above by naming `examples/hello`
# in the target rather than the whole directory.
NOT_AUDITED = {
    "logos": ("install/defs/Cpc.cached.eo",),
}


def not_audited(repo: str, root: str) -> set:
    """The absolute paths this repo's entry excludes."""
    return {
        os.path.abspath(os.path.join(root, rel)) for rel in NOT_AUDITED.get(repo, ())
    }


# Where the sources live: clones this project manages, never a checkout somebody
# else owns. See tools/deps.py.
from deps import roots as _dep_roots  # noqa: E402

DEFAULT_ROOTS = _dep_roots()


def roots_for(deps_dir: str) -> dict:
    """The same projects, under a different directory of clones."""
    return {name: os.path.join(deps_dir, name) for name in DEFAULT_ROOTS}


def signatures(paths: list[str], skip: set | None = None) -> list[list[str]]:
    """A directory is one profile per file; files together are one profile.

    `skip` is `not_audited`: a file in it is never an entry point, and any
    finding that lands in it is dropped by the caller as well, in case it was
    reached through an include rather than named directly.
    """
    skip = skip or set()
    out: list[list[str]] = []
    files: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, names in os.walk(p):
                for n in sorted(names):
                    full = os.path.join(root, n)
                    if n.endswith(".eo") and os.path.abspath(full) not in skip:
                        out.append([full])
        elif os.path.abspath(p) not in skip:
            files.append(p)
    return ([files] if files else []) + out


def measure(paths: list[str], triple: dict | None, roots: dict,
            skip: set | None = None) -> tuple[collections.Counter, int]:
    load_checks()
    sem = smt = None
    embed: set[str] = set()
    if triple:
        r, rel = triple["semantics"]
        sem = load_set(os.path.join(roots[r], rel))
        r, rel = triple["smt"]
        smt = load_set(os.path.join(roots[r], rel))
        r, rel = triple["embedding"]
        embed = _embedding_vocabulary(os.path.join(roots[r], rel))

    codes: collections.Counter = collections.Counter()
    files: set[str] = set()
    # the same dedupe the command line does: a finding in a file two profiles
    # both read is one finding, not two
    seen: set[tuple] = set()
    for group in signatures(paths, skip):
        result = load(group)
        ctx = Context(
            signature=result.signature,
            files=result.files,
            sources=result.sources,
            root=os.path.dirname(group[0]),
            include_edges=result.include_edges,
            semantics=sem,
            smt_semantics=smt,
            embedding_names=embed,
        )
        files |= set(result.files)
        for d in list(result.diagnostics) + run_all(ctx):
            if skip and os.path.abspath(d.span.path) in skip:
                continue
            key = (d.span.path, d.span.line, d.span.col, d.code, d.message)
            if key in seen:
                continue
            seen.add(key)
            codes[(d.code, d.severity)] += 1
    return codes, len(files)


def render(rows: list[tuple[str, collections.Counter, int, bool]]) -> str:
    out = ["""## The counts

Every number here is a count of *findings*, at the severities that are on by
default.

**This is not a score, and not a comparison between repositories.** These
numbers say which of our checks tripped, not how much of a subject is sound, so
a corpus with fewer findings has not been shown to be better. See *measure the
subject, never our own coverage* in [`reporting-philosophy.md`](reporting-philosophy.md).

"""]
    out.append("| corpus | files | errors | warnings | hints |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    for label, codes, nfiles, ok in rows:
        if not ok:
            out.append(f"| {label} | — | — | — | — |")
            continue
        sev = collections.Counter()
        for (_code, s), n in codes.items():
            sev[s] += n
        out.append(
            f"| {label} | {nfiles} | {sev[Severity.ERROR]} | "
            f"{sev[Severity.WARNING]} | {sev[Severity.HINT]} |"
        )
    out.append("")
    out.append("## By check")
    out.append("")
    for label, codes, _nfiles, ok in rows:
        if not ok:
            out.append(f"**{label}** — not measured: the repository was not found.\n")
            continue
        out.append(f"**{label}**")
        out.append("")
        if not codes:
            out.append("Nothing reported by the checks that are on by default.\n")
            continue
        out.append("| code | severity | count |")
        out.append("| --- | --- | ---: |")
        for (code, sev), n in sorted(codes.items(), key=lambda kv: (-kv[1], kv[0][0])):
            out.append(f"| {code} | {sev.value} | {n} |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def measure_all(roots: dict) -> list:
    """Every corpus, measured. A corpus whose files are absent is reported as
    not measured rather than as reporting nothing — the difference matters, and
    the render says which."""
    rows = []
    for label, repo, rels, triple in TARGETS:
        paths = [os.path.join(roots[repo], r) for r in rels]
        needed = list(paths) + (
            [os.path.join(roots[r], rel) for r, rel in triple.values()] if triple else []
        )
        if not all(os.path.exists(p) for p in needed):
            rows.append((label, collections.Counter(), 0, False))
            continue
        codes, nfiles = measure(paths, triple, roots, not_audited(repo, roots[repo]))
        rows.append((label, codes, nfiles, True))
    return rows
