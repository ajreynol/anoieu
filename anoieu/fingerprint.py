"""A finding's identity, independent of where it sits in a file.

A baseline that keyed on line numbers would go stale on the first edit above a
finding, so a fingerprint is taken from what the finding is about -- its code,
its file, and the text of the line it points at -- and survives everything that
does not touch that line.
"""

from __future__ import annotations

import hashlib
import os

from .diagnostics import Diagnostic, SourceMap


def fingerprint(diag: Diagnostic, sources: SourceMap, root: str) -> str:
    try:
        rel = os.path.relpath(diag.span.path, root)
    except ValueError:
        rel = diag.span.path
    line = sources.line(diag.span.path, diag.span.line).strip()
    material = " ".join([diag.code, rel, line or diag.message])
    return hashlib.sha1(material.encode("utf-8")).hexdigest()[:16]
