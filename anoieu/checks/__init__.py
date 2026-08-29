"""The check registry.

One module per family, one function per code. A check is a generator over a
`Context` yielding `Diagnostic`s, and it carries its own manual page: writing
the check and writing the page it explains is one task, because the pages are
the half of this project that is a specification of the language.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator

from ..diagnostics import Diagnostic, SourceMap
from ..model import Signature
from ..syntax.parser import ParsedFile


@dataclass
class Context:
    signature: Signature
    files: dict[str, ParsedFile]
    sources: SourceMap
    root: str = ""
    pedantic: bool = False
    include_edges: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class Check:
    code: str
    title: str
    fn: Callable[[Context], Iterator[Diagnostic]]
    page: str = ""
    default_on: bool = True


REGISTRY: dict[str, Check] = {}


def check(code: str, title: str, page: str = "", default_on: bool = True):
    def wrap(fn):
        REGISTRY[code] = Check(code=code, title=title, fn=fn, page=page.strip(), default_on=default_on)
        return fn

    return wrap


def page(code: str, title: str, text: str, default_on: bool = True) -> None:
    """Register the manual page of a diagnostic the front end emits.

    The parser and the loader report as they read, rather than as a pass over
    the model, so their codes have a page here and no function.
    """
    REGISTRY[code] = Check(
        code=code, title=title, fn=lambda ctx: iter(()), page=text.strip(), default_on=default_on
    )


def run_all(ctx: Context, enabled: set[str] | None = None) -> list[Diagnostic]:
    """Run the checks and keep what was asked for.

    Filtering happens on the findings rather than on the checks, because one
    traversal may report under more than one code.
    """
    out: list[Diagnostic] = []
    for code, chk in REGISTRY.items():
        if not chk.default_on and not ctx.pedantic and (enabled is None or code not in enabled):
            continue
        out.extend(chk.fn(ctx))
    if enabled is not None:
        out = [d for d in out if d.code in enabled]
    return out


def load_checks() -> None:
    from . import attributes, docs, parse, programs, structure  # noqa: F401
