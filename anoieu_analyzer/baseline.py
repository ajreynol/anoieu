"""Baselines: what a repository has already agreed to live with.

A calculus written before the analyzer existed reports findings on the first
run, and a team that has to fix all of them before turning anything on turns
nothing on. A baseline records today's findings so that CI can fail on
tomorrow's. A stale entry -- one nothing produces any more -- is reported rather
than kept, so the file does not become a memory of things that were fixed.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from .diagnostics import Diagnostic, SourceMap
from .fingerprint import fingerprint

VERSION = 1


@dataclass
class Baseline:
    path: str
    entries: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str) -> "Baseline":
        if not os.path.isfile(path):
            return cls(path=path)
        with open(path) as f:
            data = json.load(f)
        entries = {e["id"]: e for e in data.get("findings", [])}
        return cls(path=path, entries=entries)

    def filter(
        self, diags: list[Diagnostic], sources: SourceMap, root: str
    ) -> tuple[list[Diagnostic], int, list[dict]]:
        """What is new, how much was held back, and what the file remembers that
        nothing produces any more."""
        fresh: list[Diagnostic] = []
        seen: set[str] = set()
        held = 0
        for d in diags:
            fp = fingerprint(d, sources, root)
            seen.add(fp)
            if fp in self.entries:
                held += 1
                continue
            fresh.append(d)
        stale = [e for fp, e in self.entries.items() if fp not in seen]
        return fresh, held, stale

    def write(self, diags: list[Diagnostic], sources: SourceMap, root: str) -> int:
        findings = []
        for d in diags:
            rel = d.span.path
            if os.path.isabs(rel):
                try:
                    rel = os.path.relpath(rel, root)
                except ValueError:
                    pass
            findings.append(
                {
                    "id": fingerprint(d, sources, root),
                    "code": d.code,
                    "severity": d.severity.value,
                    "file": rel,
                    "line": d.span.line,
                    "message": d.message,
                }
            )
        findings.sort(key=lambda e: (e["file"], e["line"], e["code"], e["id"]))
        payload = {
            "version": VERSION,
            "note": (
                "written by `anoieu check --update-baseline`; each entry is a "
                "finding this repository has agreed to live with"
            ),
            "findings": findings,
        }
        parent = os.path.dirname(os.path.abspath(self.path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
        return len(findings)
