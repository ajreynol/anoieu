"""A small evaluator for ground `eo::` applications.

Not the evaluator: enough of one to finish the terms the *parser* leaves behind.
When an operator's nil terminator depends on its type -- `bvor`, whose nil is a
zero of the operand's width -- the parser inserts a placeholder,
`(eo::nil f (eo::typeof t))`, and ethos then evaluates it wherever the type is
ground. To say what a term becomes, anoieu has to do the same.

Everything here answers `None` rather than guessing, and only these operators
are implemented; a term over anything else stays as it stands.
"""

from __future__ import annotations

from fractions import Fraction

from .syntax.parser import Node
from .syntax.lexer import literal_category


def _value(node: Node):
    """The Python value of a literal, or None."""
    if not node.is_atom:
        return None
    text = node.text or ""
    if node.kind == "string":
        return node.string_value()
    if text == "true":
        return True
    if text == "false":
        return False
    cat = literal_category(text)
    if cat == "<numeral>":
        return int(text)
    if cat == "<rational>":
        n, d = text.split("/")
        return Fraction(int(n), int(d))
    if cat == "<binary>":
        return ("bin", len(text) - 2, int(text[2:], 2) if len(text) > 2 else 0)
    return None


def _binary(width: int, value: int, like: Node) -> Node:
    bits = format(value % (1 << width), f"0{width}b") if width else ""
    return Node(like.path, like.line, like.col, like.end_line, like.end_col, text="#b" + bits)


def _numeral(value: int, like: Node) -> Node:
    return Node(like.path, like.line, like.col, like.end_line, like.end_col, text=str(value))


def evaluate(node: Node) -> Node | None:
    """The value of a ground term over the operators below, or None."""
    if node.is_atom:
        return node if _value(node) is not None else None
    head = node.head
    args = [evaluate(c) for c in node.children[1:]]
    if head is None or any(a is None for a in args):
        return None
    vals = [_value(a) for a in args]
    if any(v is None for v in vals):
        return None

    def ints() -> list[int] | None:
        return vals if all(isinstance(v, int) and not isinstance(v, bool) for v in vals) else None

    if head == "eo::to_bin" and len(vals) == 2:
        width = vals[0]
        if not isinstance(width, int) or isinstance(width, bool) or width < 0:
            return None
        if isinstance(vals[1], tuple):
            return _binary(width, vals[1][2], node)
        if isinstance(vals[1], int) and not isinstance(vals[1], bool):
            return _binary(width, vals[1], node)
        return None
    if head == "eo::add" and (vs := ints()) is not None:
        return _numeral(sum(vs), node)
    if head == "eo::mul" and (vs := ints()) is not None:
        out = 1
        for v in vs:
            out *= v
        return _numeral(out, node)
    if head == "eo::neg" and (vs := ints()) is not None and len(vs) == 1:
        return _numeral(-vs[0], node)
    if head == "eo::zdiv" and (vs := ints()) is not None and len(vs) == 2 and vs[1]:
        return _numeral(vs[0] // vs[1], node)
    if head == "eo::zmod" and (vs := ints()) is not None and len(vs) == 2 and vs[1]:
        return _numeral(vs[0] % vs[1], node)
    if head == "eo::len" and len(vals) == 1:
        v = vals[0]
        if isinstance(v, tuple):
            return _numeral(v[1], node)
        if isinstance(v, str):
            return _numeral(len(v), node)
        return None
    if head == "eo::concat" and len(vals) >= 2:
        if all(isinstance(v, tuple) for v in vals):
            width = sum(v[1] for v in vals)
            acc = 0
            for v in vals:
                acc = (acc << v[1]) | v[2]
            return _binary(width, acc, node)
        return None
    if head == "eo::not" and len(vals) == 1 and isinstance(vals[0], bool):
        return Node(node.path, node.line, node.col, node.end_line, node.end_col,
                    text="false" if vals[0] else "true")
    return None
