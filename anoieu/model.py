"""The model of a signature: what the commands of a `.eo` file declare.

This is deliberately a *surface* model. It records what each command said, in
the order the include graph reads them, with spans intact. Desugaring and
typing are later passes over it (M2, M3), and both need to be able to point at
the text that produced a finding.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Span
from .syntax.parser import Node

# The attributes ethos knows, from src/expr_parser.cpp. An attribute outside
# this set is accepted by ethos with a warning and then ignored, which silently
# changes what a term means -- see check EO0020.
KNOWN_ATTRS = {
    ":implicit",
    ":is_eq",
    ":type",
    ":list",
    ":left-assoc",
    ":right-assoc",
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
    ":chainable",
    ":pairwise",
    ":binder",
    ":let-binder",
    ":arg-list",
    ":opaque",
    ":syntax",
    ":restrict",
    ":sorry",
}

# Attributes that make an operator variadic, i.e. that let the parser hand it
# any number of arguments.
NARY_ATTRS = {
    ":left-assoc",
    ":right-assoc",
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
    ":chainable",
    ":pairwise",
    ":arg-list",
}

NIL_ATTRS = {
    ":left-assoc-nil",
    ":right-assoc-nil",
    ":left-assoc-non-singleton-nil",
    ":right-assoc-non-singleton-nil",
}

# Attributes that say how applications of a symbol are built. A declaration may
# carry at most one.
CONSTRUCTOR_ATTRS = NARY_ATTRS | {":binder", ":let-binder"}

LITERAL_CATEGORIES = {
    "<boolean>",
    "<numeral>",
    "<decimal>",
    "<rational>",
    "<hexadecimal>",
    "<binary>",
    "<string>",
}


@dataclass
class Attribute:
    key: str
    value: Node | None
    span: Span


@dataclass
class Param:
    """One `(<symbol> <type> <attr>*)` of a typed parameter list."""

    name: str
    type: Node | None
    attrs: list[Attribute]
    span: Span

    def has(self, key: str) -> bool:
        return any(a.key == key for a in self.attrs)


@dataclass
class Decl:
    """A declared symbol: declare-const, declare-parameterized-const, and the
    symbols a datatype declaration introduces."""

    name: str
    kind: str  # const | parameterized-const | datatype | constructor | selector | sort
    type: Node | None
    params: list[Param]
    attrs: list[Attribute]
    span: Span
    form: Node | None = None

    def attr(self, key: str) -> Attribute | None:
        for a in self.attrs:
            if a.key == key:
                return a
        return None

    @property
    def constructor_attr(self) -> Attribute | None:
        for a in self.attrs:
            if a.key in CONSTRUCTOR_ATTRS:
                return a
        return None

    @property
    def is_nary(self) -> bool:
        return any(a.key in NARY_ATTRS for a in self.attrs)

    @property
    def nil(self) -> Node | None:
        for a in self.attrs:
            if a.key in NIL_ATTRS:
                return a.value
        return None


@dataclass
class ProgramDecl:
    name: str
    params: list[Param]
    sig_args: list[Node]
    sig_ret: Node | None
    cases: list[tuple[Node, Node]]
    span: Span
    form: Node | None = None
    doc: "Docstring | None" = None

    @property
    def arity(self) -> int:
        return len(self.sig_args)


@dataclass
class RuleDecl:
    name: str
    params: list[Param]
    assumption: Node | None
    premises: list[Node]
    premise_list: tuple[Node, Node] | None  # (pattern, constructor)
    args: list[Node]
    requires: list[tuple[Node, Node]]
    conclusion: Node | None
    conclusion_explicit: bool
    attrs: list[Attribute]
    field_order: list[tuple[str, Span]]
    span: Span
    form: Node | None = None
    doc: "Docstring | None" = None


@dataclass
class DefineDecl:
    name: str
    params: list[Param]
    body: Node | None
    attrs: list[Attribute]
    span: Span
    form: Node | None = None


@dataclass
class LiteralDecl:
    category: str
    type: Node | None
    span: Span


@dataclass
class Docstring:
    """A `; rule:`/`; program:` documentation block, as CPC writes them."""

    name: str | None
    kind: str | None  # rule | program
    fields: dict[str, list[str]]  # field -> its `- item` lines
    prose: dict[str, str]  # field -> free text on the field's own line
    span: Span


@dataclass
class Signature:
    """Everything the include graph declared, in order."""

    root: str
    decls: list[Decl] = field(default_factory=list)
    programs: list[ProgramDecl] = field(default_factory=list)
    rules: list[RuleDecl] = field(default_factory=list)
    defines: list[DefineDecl] = field(default_factory=list)
    literals: list[LiteralDecl] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    by_name: dict[str, list[Decl]] = field(default_factory=dict)
    programs_by_name: dict[str, ProgramDecl] = field(default_factory=dict)
    rules_by_name: dict[str, RuleDecl] = field(default_factory=dict)
    defines_by_name: dict[str, DefineDecl] = field(default_factory=dict)
    literal_type: dict[str, Node] = field(default_factory=dict)

    def add_decl(self, d: Decl) -> None:
        self.decls.append(d)
        self.by_name.setdefault(d.name, []).append(d)

    def lookup(self, name: str) -> Decl | None:
        """The declaration a name resolves to: the most recent one, which is
        what ethos picks when a name is overloaded and unapplied."""
        ds = self.by_name.get(name)
        return ds[-1] if ds else None

    def all_named(self) -> set[str]:
        return (
            set(self.by_name)
            | set(self.programs_by_name)
            | set(self.rules_by_name)
            | set(self.defines_by_name)
        )
