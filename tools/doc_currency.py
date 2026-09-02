#!/usr/bin/env python3
"""How much evidence there is that this repository's documentation is current.

**It does not decide whether a sentence is true, and it never will.** That is
`docs/policy.md`'s central rule and the reason it is stated there rather than
numbered among the checkable ones: a page describing a tree that changed is
mechanically indistinguishable from one that is accurate. Anything claiming
otherwise would be the overclaim this repository exists to avoid.

**What it measures is the evidence, which is a different thing and is
decidable.** A dated claim can be discounted by age; an undated one cannot be
discounted at all, so a reader has to take it on trust. The proportion that can
be discounted rather than trusted is the health number this prints.

Three classes, in descending order of how much a reader can do with them:

  generated   written by a tool and regenerated on every run. Cannot go stale
              in this sense, and is excluded from the count rather than
              flattering it.
  dated       carries at least one explicit date. A reader can decide for
              themselves whether that is recent enough for what they need.
  undated     carries none. Age is unknowable without reading git, and the
              claim inside it may be a week old or a year.

**The sharpest class is a cross-project claim with no date.** A page that says
something about a repository we do not control, and does not say when, is the
one a reader is least able to check and most likely to rely on.

**It fails nothing today, deliberately.** The prototype of the dangling-id half
reported four findings and all four were false -- two from a pattern narrower
than the corpus, two from ids deliberately left unallocated with the reason in
prose a program cannot read. A check that fires wrongly costs more than it
saves, so this reports and does not gate, and the number is what has to move
before gating is worth arguing for.

    python3 tools/doc_currency.py            # the measurement
    python3 tools/doc_currency.py --list     # and every undated document
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

#: Rewritten whole by a generator on every run, so staleness is not a property
#: they can have. Counting them would flatter the number.
GENERATED = {"docs/checks.md", "docs/reports/corpus.md",
             "docs/reports/open-findings.md", "docs/reports/closed-findings.md"}

#: The other repositories this ecosystem talks about. A claim naming one of
#: these is a claim about a tree we do not control.
OTHERS = ("cvc5", "ethos", "logos", "eudaimonia", "dokimasia", "koine",
          "inspect.software")

DATE = re.compile(r"\b20\d{2}-[01]\d-[0-3]\d\b")


def tracked() -> list[str]:
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "*.md"],
                         capture_output=True, text=True).stdout.split()
    return [p for p in out if not p.startswith("deps/")]


def main() -> int:
    show = "--list" in sys.argv
    dated, undated, generated, blind = [], [], [], []
    for rel in tracked():
        if rel in GENERATED:
            generated.append(rel)
            continue
        text = open(os.path.join(ROOT, rel), encoding="utf-8",
                    errors="replace").read()
        if DATE.search(text):
            dated.append(rel)
        else:
            undated.append(rel)
            if any(o in text for o in OTHERS):
                blind.append(rel)

    written = len(dated) + len(undated)
    pct = (100 * len(dated) // written) if written else 100
    print("-- documentation-up-to-date: evidence, not truth")
    print(f"   {len(dated)} of {written} written documents carry a date "
          f"({pct}%)")
    print(f"   {len(generated)} generated, excluded rather than counted")
    print(f"   {len(blind)} undated document(s) make a claim about another "
          "repository")
    if show:
        for rel in sorted(undated):
            print(f"     undated  {rel}"
                  + ("   [names another repository]" if rel in blind else ""))
    print("   nothing fails here: what a sentence says is not decidable, and "
          "the")
    print("   half that is decidable reported 4 findings and 4 false ones "
          "when tried")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
