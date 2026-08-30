"""Per-repository configuration.

A CI job should say `anoieu check` and nothing else: which signatures a
repository has, which checks it runs, and what it has agreed to live with are
properties of the repository, so they are written down in it. The file is
`anoieu.json`, beside the signatures or at the root above them:

    {
      "entry_points": ["proofs/eo/cpc/Cpc.eo", "proofs/eo/cpc/expert/CpcExpert.eo"],
      "baseline": "proofs/eo/anoieu-baseline.json",
      "disable": ["DOC0011"],
      "severity": {"EO0054": "hint"},
      "pedantic": false
    }

Every field is optional, and every one can be overridden on the command line,
because a person debugging one finding should not have to edit the repository's
policy to do it.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

CONFIG_NAME = "anoieu.json"


@dataclass
class Config:
    path: str | None = None
    root: str = ""
    entry_points: list[str] = field(default_factory=list)
    baseline: str | None = None
    enable: list[str] = field(default_factory=list)
    disable: list[str] = field(default_factory=list)
    severity: dict[str, str] = field(default_factory=dict)
    pedantic: bool = False

    @property
    def found(self) -> bool:
        return self.path is not None

    def resolve(self, rel: str) -> str:
        return rel if os.path.isabs(rel) else os.path.join(self.root, rel)


def discover(start: str, explicit: str | None = None) -> Config:
    """The configuration governing a path: the nearest `anoieu.json` at or above
    it, or an empty one."""
    if explicit:
        return load(explicit)
    here = os.path.abspath(start)
    if os.path.isfile(here):
        here = os.path.dirname(here)
    while True:
        candidate = os.path.join(here, CONFIG_NAME)
        if os.path.isfile(candidate):
            return load(candidate)
        parent = os.path.dirname(here)
        if parent == here:
            return Config()
        here = parent


def load(path: str) -> Config:
    with open(path) as f:
        data = json.load(f)
    return Config(
        path=os.path.abspath(path),
        root=os.path.dirname(os.path.abspath(path)),
        entry_points=list(data.get("entry_points", [])),
        baseline=data.get("baseline"),
        enable=[c.upper() for c in data.get("enable", [])],
        disable=[c.upper() for c in data.get("disable", [])],
        severity={k.upper(): v for k, v in data.get("severity", {}).items()},
        pedantic=bool(data.get("pedantic", False)),
    )
