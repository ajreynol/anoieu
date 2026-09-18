"""Suppression comments.

A finding a signature has decided to keep is written down where it is kept, so
that the decision is read together with the code:

    ; anoieu: allow EO0054  matching exactly two is what this rule is about
    (($contains (or l xs) l) true)

A comment governs the line under it, or the line it sits on when it trails code.
`allow-file` governs the whole file. Every suppression carries its reason, and a
run counts what it silenced, so a repository can see what it is holding rather
than losing track of it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .diagnostics import Diagnostic
from .syntax.parser import ParsedFile

_DIRECTIVE = re.compile(
    r"anoieu:\s*(allow|allow-file)\s+([A-Z]+[0-9]+(?:\s+[A-Z]+[0-9]+)*)(.*)"
)


@dataclass
class Suppressions:
    lines: dict[tuple[str, int, str], str] = field(default_factory=dict)
    files: dict[tuple[str, str], str] = field(default_factory=dict)

    def reason(self, diag: Diagnostic) -> str | None:
        key = (diag.span.path, diag.span.line, diag.code)
        if key in self.lines:
            return self.lines[key]
        return self.files.get((diag.span.path, diag.code))

    def __len__(self) -> int:
        return len(self.lines) + len(self.files)


def collect(files: dict[str, ParsedFile]) -> Suppressions:
    out = Suppressions()
    for path, parsed in files.items():
        code_lines = {f.line for f in parsed.forms}
        comment_lines = {c.line for c in parsed.comments}
        for comment in parsed.comments:
            m = _DIRECTIVE.search(comment.text)
            if m is None:
                continue
            kind, codes, reason = m.group(1), m.group(2).split(), m.group(3).strip()
            if kind == "allow-file":
                for code in codes:
                    out.files[(path, code)] = reason
                continue
            # the line it governs: this one if it trails code, otherwise the next
            # line that is not itself a comment
            target = comment.line if comment.line in code_lines else comment.line + 1
            while target in comment_lines and target not in code_lines:
                target += 1
            for code in codes:
                out.lines[(path, target, code)] = reason
    return out


def apply(
    diags: list[Diagnostic], sup: Suppressions
) -> tuple[list[Diagnostic], list[tuple[Diagnostic, str]]]:
    kept: list[Diagnostic] = []
    silenced: list[tuple[Diagnostic, str]] = []
    for d in diags:
        reason = sup.reason(d)
        if reason is None:
            kept.append(d)
        else:
            silenced.append((d, reason))
    return kept, silenced
