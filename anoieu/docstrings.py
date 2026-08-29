"""The documentation convention of a signature.

CPC writes a block of comments above each rule and program in a consistent,
YAML-ish shape:

    ; rule: string_length_pos
    ; implements: ProofRule::STRING_LENGTH_POS
    ; args:
    ; - s String: The string term.
    ; conclusion: >
    ;   The length of s is zero and it is the empty string, or ...

Nothing parses these today, so nothing keeps them true. This reads them, and
`checks/docs.py` compares what they say with what the declaration says.
"""

from __future__ import annotations

import re

from .diagnostics import Span
from .model import Docstring
from .syntax.lexer import Comment

_FIELD = re.compile(r"^\s*([a-z][a-z0-9_-]*):\s*(.*)$")
_ITEM = re.compile(r"^\s*-\s+(.*)$")

DOC_KINDS = ("rule", "program")


def parse_docstring(block: list[Comment], path: str) -> Docstring | None:
    if not block:
        return None
    fields: dict[str, list[str]] = {}
    prose: dict[str, str] = {}
    name: str | None = None
    kind: str | None = None
    current: str | None = None
    seen_field = False

    for c in block:
        line = c.text
        m = _ITEM.match(line)
        if m and current:
            fields.setdefault(current, []).append(m.group(1).strip())
            continue
        m = _FIELD.match(line)
        if m:
            key, rest = m.group(1), m.group(2).strip()
            # a continuation line of a `>` block is indented prose, not a field
            if current and rest == "" and line.startswith("   "):
                continue
            seen_field = True
            current = key
            fields.setdefault(key, [])
            if rest and rest != ">":
                prose[key] = rest
            if key in DOC_KINDS and name is None:
                kind, name = key, rest or None
            continue
        if current and line.strip():
            prose[current] = (prose.get(current, "") + " " + line.strip()).strip()

    if not seen_field:
        return None
    first = block[0]
    return Docstring(
        name=name,
        kind=kind,
        fields=fields,
        prose=prose,
        span=Span(path, first.line, first.col, first.line, first.col + len(first.text) + 1),
    )


def item_name(item: str) -> str:
    """The name a `- x Int: description` item introduces."""
    head = item.split(":", 1)[0].strip()
    return head.split()[0] if head else ""
