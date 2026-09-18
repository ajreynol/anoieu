"""A recovering s-expression parser.

Ethos aborts on the first error; that is right for a checker and wrong for an
edit loop, so this parser recovers: an unbalanced form is closed, an unexpected
`)` is dropped, and parsing continues to the end of the file. Every node carries
the span of the text it came from, because a finding about a desugared term has
to point back at the surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..diagnostics import Diagnostic, Severity, Span
from .lexer import Comment, Tok, Token, lex, literal_category


@dataclass
class Node:
    """An atom or a list. `text` is set for atoms, `items` for lists."""

    path: str
    line: int
    col: int
    end_line: int
    end_col: int
    text: str | None = None
    items: list["Node"] | None = None
    kind: str = "atom"  # atom | list | keyword | string

    # -- shape

    @property
    def is_list(self) -> bool:
        return self.items is not None

    @property
    def is_atom(self) -> bool:
        return self.items is None

    @property
    def is_keyword(self) -> bool:
        return self.kind == "keyword"

    @property
    def is_string(self) -> bool:
        return self.kind == "string"

    @property
    def span(self) -> Span:
        return Span(self.path, self.line, self.col, self.end_line, self.end_col)

    # -- convenience

    @property
    def head(self) -> str | None:
        """The name at the head of an application, or the atom's own text."""
        if self.is_atom:
            return self.text
        if self.items and self.items[0].is_atom:
            return self.items[0].text
        return None

    def at(self, i: int) -> "Node | None":
        if self.items and 0 <= i < len(self.items):
            return self.items[i]
        return None

    @property
    def children(self) -> list["Node"]:
        return self.items or []

    def string_value(self) -> str:
        if self.kind == "string":
            return (self.text or "")[1:-1].replace('""', '"')
        return self.text or ""

    @property
    def literal_category(self) -> str | None:
        if self.kind == "string":
            return "<string>"
        if self.is_atom and self.text in ("true", "false"):
            return "<boolean>"
        return literal_category(self.text) if self.is_atom and self.text else None

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def symbols(self):
        """Every atom that could be a name, i.e. not a literal or keyword."""
        for nd in self.walk():
            if nd.is_atom and nd.kind == "atom" and nd.literal_category is None:
                yield nd

    def __str__(self) -> str:
        if self.is_atom:
            return self.text or ""
        return "(" + " ".join(str(c) for c in self.children) + ")"


@dataclass
class ParsedFile:
    path: str
    text: str
    forms: list[Node]
    comments: list[Comment]
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # comment lines directly above a form, keyed by the form's starting line
    docblocks: dict[int, list[Comment]] = field(default_factory=dict)


def _node_from(tok: Token, path: str) -> Node:
    kind = {Tok.KEYWORD: "keyword", Tok.STRING: "string"}.get(tok.kind, "atom")
    return Node(path, tok.line, tok.col, tok.end_line, tok.end_col, text=tok.text, kind=kind)


def parse(path: str, text: str) -> ParsedFile:
    tokens, comments, lex_errors = lex(text)
    diags: list[Diagnostic] = [
        Diagnostic(
            code="EO0001",
            severity=Severity.ERROR,
            message=e.msg,
            span=Span(path, e.line, e.col),
        )
        for e in lex_errors
    ]

    forms: list[Node] = []
    stack: list[Node] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        i += 1
        if tok.kind is Tok.EOF:
            break
        if tok.kind is Tok.LPAREN:
            node = Node(path, tok.line, tok.col, tok.end_line, tok.end_col, items=[], kind="list")
            stack.append(node)
            continue
        if tok.kind is Tok.RPAREN:
            if not stack:
                diags.append(
                    Diagnostic(
                        code="EO0002",
                        severity=Severity.ERROR,
                        message="unexpected `)` with no form open",
                        span=Span(path, tok.line, tok.col, tok.end_line, tok.end_col),
                        help="a stray close parenthesis; delete it or open the form it closes",
                    )
                )
                continue
            node = stack.pop()
            node.end_line, node.end_col = tok.end_line, tok.end_col
            (stack[-1].items if stack else forms).append(node)
            continue
        atom = _node_from(tok, path)
        if stack:
            stack[-1].items.append(atom)
        else:
            forms.append(atom)
            diags.append(
                Diagnostic(
                    code="EO0003",
                    severity=Severity.ERROR,
                    message=f"`{tok.text}` stands outside any command",
                    span=atom.span,
                    help="every top-level form of a signature is a command, i.e. a list",
                )
            )
    while stack:
        node = stack.pop()
        diags.append(
            Diagnostic(
                code="EO0002",
                severity=Severity.ERROR,
                message="form is never closed",
                span=Span(node.path, node.line, node.col, node.line, node.col + 1),
                label=f"this `(` has no `)`{'' if not node.items else ' — form is ' + (node.head or '?')}",
            )
        )
        node.end_line, node.end_col = tokens[-1].line, tokens[-1].col
        (stack[-1].items if stack else forms).append(node)

    parsed = ParsedFile(path=path, text=text, forms=forms, comments=comments, diagnostics=diags)
    parsed.docblocks = _docblocks(forms, comments)
    return parsed


def _docblocks(forms: list[Node], comments: list[Comment]) -> dict[int, list[Comment]]:
    """The run of comment lines directly above each top-level form.

    A blank line ends a block, which is the same convention `.eos` uses, and
    the one CPC's `; rule:` docstrings are written under.
    """
    by_line = {c.line: c for c in comments}
    out: dict[int, list[Comment]] = {}
    for form in forms:
        block: list[Comment] = []
        line = form.line - 1
        while line in by_line:
            block.append(by_line[line])
            line -= 1
        if block:
            out[form.line] = list(reversed(block))
    return out
