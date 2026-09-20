"""Choose entry points without checking include fragments in isolation."""
from __future__ import annotations

import os

from .syntax.parser import parse


def profiles(paths: list[str], skip: set[str] | None = None) -> list[list[str]]:
    """Explicit files form one ordered profile; directories supply entry points.

    Follow include edges before selecting directory roots. A fragment still gets
    checked in every consumer's context. Disconnected include cycles retain an
    entry point too, so root selection cannot hide a cycle or an orphaned file.
    Explicitly naming a fragment continues to request standalone analysis.
    """
    skip = {os.path.abspath(p) for p in (skip or ())}
    explicit: list[str] = []
    candidates: set[str] = set()
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs.sort()
                candidates.update(os.path.abspath(os.path.join(root, name))
                                  for name in names if name.endswith(".eo"))
        elif os.path.abspath(path) not in skip:
            explicit.append(path)
    candidates -= skip
    edges: dict[str, set[str]] = {}
    pending = sorted(candidates | {os.path.abspath(p) for p in explicit})
    while pending:
        path = pending.pop()
        if path in edges:
            continue
        edges[path] = set()
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                parsed = parse(path, fh.read())
        except OSError:
            continue  # the loader reports the missing/unreadable input
        for form in parsed.forms:
            arg = form.at(1)
            if form.head == "include" and arg is not None and arg.is_string:
                target = os.path.abspath(os.path.join(os.path.dirname(path), arg.string_value()))
                edges[path].add(target)
                pending.append(target)

    covered: set[str] = set()

    def cover(path: str) -> None:
        todo = [path]
        while todo:
            current = todo.pop()
            if current not in covered:
                covered.add(current)
                todo.extend(edges.get(current, ()))

    out = [explicit] if explicit else []
    for path in explicit:
        cover(os.path.abspath(path))
    included = set().union(*edges.values()) if edges else set()
    for path in sorted(candidates - included):
        if path not in covered:
            out.append([path])
            cover(path)
    # Anything not reached from a root is in, or downstream of, an include
    # cycle. Keep it observable instead of silently returning no profiles.
    for path in sorted(candidates - covered):
        if path not in covered:
            out.append([path])
            cover(path)
    return out
