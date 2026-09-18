"""A finding's identity, independent of where it sits in a file.

A baseline that keyed on line numbers would go stale on the first edit above a
finding, so a fingerprint is taken from what the finding is about -- its code,
its file, and the text of the line it points at -- and survives everything that
does not touch that line.

**Two producers have to be able to compute it.** The checks derive an id from a
`Diagnostic` they have just produced; an agent working the same targets by hand
has a code, a path and a line of text and nothing else. So the arithmetic is
`id_of`, which takes those three, and `fingerprint` is the wrapper that pulls
them off a diagnostic. `anoieu_analyzer/reporting/finding_id.py` is the same function on a command
line, and it is what the agent prompt tells an assistant to use -- because two
producers whose ids disagree cannot be deduplicated by `koine_append_db`.
"""

from __future__ import annotations

import hashlib
import os

from .diagnostics import Diagnostic, SourceMap


def id_of(code: str, rel: str, line: str) -> str:
    """The id, from the three things it is made of.

    `rel` is the path inside the owner's tree and `line` is the text of the line
    the finding points at, stripped. Where a finding has no line text, callers
    pass the message instead -- that is what the checks have always done.
    """
    material = " ".join([code, rel, line])
    return hashlib.sha1(material.encode("utf-8")).hexdigest()[:16]


def fingerprint(diag: Diagnostic, sources: SourceMap, root: str) -> str:
    try:
        rel = os.path.relpath(diag.span.path, root)
    except ValueError:
        rel = diag.span.path
    line = sources.line(diag.span.path, diag.span.line).strip()
    return id_of(diag.code, rel, line or diag.message)
