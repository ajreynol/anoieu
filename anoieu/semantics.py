"""Reading a semantic configuration set (`*.eos`).

**Deliberately vocabulary-agnostic.** The `.eos` language is younger than the
signature language and still moving: measuring the sets in the wild against the
grammar in `tools/eoc/semantics/README.md` already turns up three forms and five
attributes the document does not mention, and more are expected. A reader that
enumerated the forms it knows would be wrong by the time it shipped.

So this reads *shape* instead:

    (<head> <name> (<parameter>*)? (:key <value>*)*)

Anything with a head and a name is an **entry** of kind `<head>`; a keyword
starts an attribute and takes every value up to the next keyword, so an
attribute that grows a second value needs no change here. `program`,
`define-macro` and `section` are the three shapes that are not entries, and they
are recognised by shape too.

What this cannot do is tell you whether an entry *means* anything -- that is the
compiler's business, and it changes when the language does. What it can do is
answer the questions that survive the language moving: which names a set
defines, which names it reaches for, and what it says about each.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .diagnostics import Diagnostic, Severity, Span
from .model import Param
from .syntax.parser import Node, parse

# The shapes that are not entries.
NON_ENTRY = {"section", "define-macro", "program"}

# What we have seen in the wild, kept only so that a form outside it can be
# *mentioned* rather than refused. Adding one here is not required for the
# reader to work; it only quiets EOS0001.
KNOWN_FORMS = {
    "define-symbol",
    "define-sort",
    "define-value",
    "define-literal",
    "define-method",
    "define-rule",
    "define-native-method",
    "declare-native",
    "declare-native-type",
    "declare-constructor",
    "declare-aggregate-method",
    "declare-embed-datatype",
} | NON_ENTRY


@dataclass
class SemAttr:
    key: str
    values: list[Node]
    span: Span

    @property
    def value(self) -> Node | None:
        return self.values[0] if self.values else None

    def __str__(self) -> str:
        return self.key + ("".join(" " + str(v) for v in self.values))


@dataclass
class SemEntry:
    kind: str
    name: str
    params: list[Param]
    attrs: list[SemAttr]
    span: Span
    form: Node

    def attr(self, key: str) -> SemAttr | None:
        return next((a for a in self.attrs if a.key == key), None)

    def has(self, key: str) -> bool:
        return self.attr(key) is not None

    @property
    def overload(self) -> str | None:
        """The name the desugar stage gives this symbol, where it gives one."""
        a = self.attr(":overload")
        return a.value.text if a is not None and a.value is not None else None

    def names_used(self) -> set[str]:
        """Every name this entry's attribute values mention."""
        out: set[str] = set()
        for a in self.attrs:
            for v in a.values:
                out |= {s.text or "" for s in v.symbols()}
        return out


@dataclass
class SemProgram:
    name: str
    params: list[Param]
    sig_args: list[Node]
    sig_ret: Node | None
    cases: list[tuple[Node, Node]]
    span: Span


@dataclass
class SemSet:
    """One configuration set: a file, and whatever it includes."""

    path: str
    entries: list[SemEntry] = field(default_factory=list)
    programs: list[SemProgram] = field(default_factory=list)
    macros: dict[str, Node] = field(default_factory=dict)
    sections: list[tuple[str, Span]] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    text: str = ""

    @property
    def by_name(self) -> dict[str, SemEntry]:
        out: dict[str, SemEntry] = {}
        for e in self.entries:
            out.setdefault(e.name, e)
        return out

    @property
    def role(self) -> str:
        """`target` (an SMT-LIB semantics) or `input` (a calculus's).

        A set is told apart by what only one of them holds: the target declares
        the types, values and literals of the embedding; an input says what its
        symbols become. The compiler distinguishes them by the option that names
        them, so this is a guess -- reported as such where it matters.
        """
        kinds = {e.kind for e in self.entries}
        if kinds & {"define-sort", "define-value", "define-literal"}:
            return "target"
        if any(e.has(":term") or e.has(":is-list-nil") for e in self.entries):
            return "input"
        return "unknown"

    def defines(self) -> set[str]:
        return (
            {e.name for e in self.entries}
            | {p.name for p in self.programs}
            | set(self.macros)
        )


def _attrs_of(nodes: list[Node]) -> list[SemAttr]:
    """A keyword takes every value up to the next keyword.

    That is what makes this survive an attribute growing a second value, which
    `:eval` and the aggregate attributes already have and others may.
    """
    out: list[SemAttr] = []
    current: SemAttr | None = None
    for nd in nodes:
        if nd.is_keyword:
            current = SemAttr(nd.text or "", [], nd.span)
            out.append(current)
        elif current is not None:
            current.values.append(nd)
    return out


def _params_of(node: Node | None) -> list[Param]:
    """`(x)`, `((! x :raw) y)`, `((s "String"))` -- a parameter list, loosely."""
    if node is None or not node.is_list:
        return []
    out: list[Param] = []
    for item in node.children:
        if item.is_atom:
            out.append(Param(item.text or "?", None, [], item.span))
            continue
        kids = item.children
        if kids and kids[0].is_atom and kids[0].text == "!":
            name = kids[1].text if len(kids) > 1 and kids[1].is_atom else "?"
            marks = [
                type("A", (), {"key": k.text or "", "value": None, "span": k.span})()
                for k in kids[2:]
                if k.is_keyword
            ]
            out.append(Param(name or "?", None, marks, item.span))  # type: ignore[arg-type]
        elif kids and kids[0].is_atom:
            out.append(
                Param(kids[0].text or "?", kids[1] if len(kids) > 1 else None, [], item.span)
            )
    return out


def load_set(path: str) -> SemSet:
    """Read one configuration set."""
    real = os.path.realpath(path)
    text = open(real, encoding="utf-8", errors="replace").read()
    parsed = parse(real, text)
    out = SemSet(path=real, diagnostics=list(parsed.diagnostics), text=text)

    for form in parsed.forms:
        if not form.is_list or not form.children:
            continue
        head = form.head
        if head == "section":
            arg = form.at(1)
            out.sections.append((arg.string_value() if arg else "", form.span))
            continue
        if head == "define-macro":
            name = form.at(1)
            body = form.at(3)
            if name is not None and name.is_atom and body is not None:
                out.macros[name.text or "?"] = body
            continue
        if head == "program":
            name = form.at(1)
            if name is None or not name.is_atom:
                continue
            rest = form.children[3:]
            sig_args: list[Node] = []
            sig_ret = None
            cases: list[tuple[Node, Node]] = []
            i = 0
            while i < len(rest):
                nd = rest[i]
                if nd.is_keyword and nd.text == ":signature":
                    arglist = rest[i + 1] if i + 1 < len(rest) else None
                    sig_args = list(arglist.children) if arglist and arglist.is_list else []
                    sig_ret = rest[i + 2] if i + 2 < len(rest) else None
                    i += 3
                    continue
                if nd.is_list:
                    for case in nd.children:
                        if case.is_list and len(case.children) == 2:
                            cases.append((case.children[0], case.children[1]))
                i += 1
            out.programs.append(
                SemProgram(
                    name.text or "?",
                    _params_of(form.at(2)),
                    sig_args,
                    sig_ret,
                    cases,
                    form.span,
                )
            )
            continue

        name_node = form.at(1)
        if head is None or name_node is None or not name_node.is_atom:
            out.diagnostics.append(
                Diagnostic(
                    code="EOS0001",
                    severity=Severity.HINT,
                    message=f"`{head}` is not a form this reader knows",
                    span=form.span,
                    notes=[
                        "the `.eos` language is still moving; a form outside the "
                        "vocabulary is read for its names and otherwise passed over"
                    ],
                )
            )
            continue
        params_node = form.at(2)
        rest_from = 3 if params_node is not None and params_node.is_list else 2
        out.entries.append(
            SemEntry(
                kind=head,
                name=name_node.text or "?",
                params=_params_of(params_node) if rest_from == 3 else [],
                attrs=_attrs_of(form.children[rest_from:]),
                span=name_node.span,
                form=form,
            )
        )
        if head not in KNOWN_FORMS:
            out.diagnostics.append(
                Diagnostic(
                    code="EOS0001",
                    severity=Severity.HINT,
                    message=f"`{head}` is not a form this reader knows",
                    span=form.span,
                    label="read generically",
                    notes=[
                        "its name and attributes are read; nothing is assumed about "
                        "what it means"
                    ],
                )
            )
    return out
