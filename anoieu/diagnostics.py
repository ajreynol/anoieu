"""Diagnostics: spans, findings, and how a run reports them.

A finding always carries the span of the surface text that produced it, plus
optional notes and a help line. The renderer is deliberately the rustc/gcc
shape, because every editor already parses it.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    HINT = "hint"

    @property
    def rank(self) -> int:
        return {"error": 0, "warning": 1, "hint": 2}[self.value]


@dataclass(frozen=True)
class Span:
    """A half-open region of a file, 1-based line, 1-based column."""

    path: str
    line: int
    col: int
    end_line: int = 0
    end_col: int = 0

    @property
    def end(self) -> tuple[int, int]:
        if self.end_line:
            return (self.end_line, self.end_col)
        return (self.line, self.col + 1)

    def __str__(self) -> str:
        return f"{self.path}:{self.line}:{self.col}"


@dataclass
class Diagnostic:
    code: str
    severity: Severity
    message: str
    span: Span
    label: str = ""
    notes: list[str] = field(default_factory=list)
    help: str = ""

    def key(self) -> tuple:
        return (self.span.path, self.span.line, self.span.col, self.code)


class SourceMap:
    """Keeps the text of every file read, so a diagnostic can quote its line."""

    def __init__(self) -> None:
        self._lines: dict[str, list[str]] = {}

    def add(self, path: str, text: str) -> None:
        self._lines[path] = text.splitlines()

    def line(self, path: str, line: int) -> str:
        lines = self._lines.get(path)
        if lines is None or not (1 <= line <= len(lines)):
            return ""
        return lines[line - 1]


def _rel(path: str, root: str) -> str:
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return path


def render_text(
    diags: Iterable[Diagnostic], sources: SourceMap, root: str, color: bool = True
) -> str:
    def paint(s: str, c: str) -> str:
        if not color:
            return s
        codes = {"red": "31", "yellow": "33", "blue": "34", "bold": "1", "dim": "2"}
        return f"\033[{codes[c]}m{s}\033[0m"

    hue = {Severity.ERROR: "red", Severity.WARNING: "yellow", Severity.HINT: "blue"}
    out: list[str] = []
    for d in diags:
        loc = f"{_rel(d.span.path, root)}:{d.span.line}:{d.span.col}"
        head = f"{paint(d.severity.value, hue[d.severity])}[{d.code}]"
        out.append(f"{loc}: {head}: {d.message}")
        src = sources.line(d.span.path, d.span.line)
        if src:
            gutter = str(d.span.line)
            pad = " " * len(gutter)
            width = 1
            if d.span.end_line == d.span.line and d.span.end_col > d.span.col:
                width = d.span.end_col - d.span.col
            width = max(1, min(width, max(1, len(src) - d.span.col + 1)))
            out.append(f"{pad} {paint('|', 'dim')}")
            out.append(f"{gutter} {paint('|', 'dim')} {src}")
            caret = " " * (d.span.col - 1) + paint("^" * width, hue[d.severity])
            tail = f" {paint(d.label, hue[d.severity])}" if d.label else ""
            out.append(f"{pad} {paint('|', 'dim')} {caret}{tail}")
        for n in d.notes:
            out.append(f"  {paint('= note:', 'dim')} {n}")
        if d.help:
            out.append(f"  {paint('= help:', 'dim')} {d.help}")
        out.append("")
    return "\n".join(out)


def render_json(diags: Iterable[Diagnostic], root: str) -> str:
    payload = [
        {
            "code": d.code,
            "severity": d.severity.value,
            "message": d.message,
            "file": _rel(d.span.path, root),
            "line": d.span.line,
            "column": d.span.col,
            "endLine": d.span.end_line or d.span.line,
            "endColumn": d.span.end_col or d.span.col,
            "label": d.label,
            "notes": d.notes,
            "help": d.help,
        }
        for d in diags
    ]
    return json.dumps(payload, indent=2)


def render_github(diags: Iterable[Diagnostic], root: str) -> str:
    level = {Severity.ERROR: "error", Severity.WARNING: "warning", Severity.HINT: "notice"}
    out = []
    for d in diags:
        msg = d.message.replace("\n", " ")
        out.append(
            f"::{level[d.severity]} file={_rel(d.span.path, root)},"
            f"line={d.span.line},col={d.span.col},title={d.code}::{msg}"
        )
    return "\n".join(out)
