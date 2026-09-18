"""Syntactic reasoning about types, short of a type checker.

M1 has no type checker. What it has is the shape of a declared type -- `->` is
right associative, so `(-> A B C)` and `(-> A (-> B C))` are one type -- and a
conservative way to name the type of a *simple* term: a literal, a declared
constant, or an application of one. Everything else answers `None`, and a check
that gets `None` says nothing. That is the whole discipline: report only what is
decidable from the declarations themselves.
"""

from __future__ import annotations

from .model import Signature
from .syntax.parser import Node


def arrow_parts(node: Node | None) -> list[Node] | None:
    """`(-> A B C)` -> [A, B, C], flattening the right-associative spelling."""
    if node is None or not node.is_list or not node.children:
        return None
    if node.children[0].text != "->":
        return None
    parts = list(node.children[1:])
    if not parts:
        return None
    tail = arrow_parts(parts[-1])
    if tail is not None:
        parts = parts[:-1] + tail
    return parts


def strip_requires(node: Node | None) -> Node | None:
    """`(eo::requires a b T)` stands for `T` wherever the requirement holds, so
    a type written that way is that type as far as its shape goes."""
    seen = 0
    while (
        node is not None
        and node.is_list
        and node.head == "eo::requires"
        and len(node.children) == 4
        and seen < 16
    ):
        node = node.children[3]
        seen += 1
    return node


def type_head(node: Node | None) -> str | None:
    """The outermost type constructor: `Bool` -> Bool, `(Seq T)` -> Seq."""
    if node is None:
        return None
    if node.is_atom:
        return node.text
    return node.head


def same_type(a: Node | None, b: Node | None) -> bool | None:
    """Syntactic equality of two type expressions, or None if undecidable."""
    if a is None or b is None:
        return None
    return str(a) == str(b)


def declared_type(name: str, sig: Signature) -> Node | None:
    from .resolve import BUILTINS

    ds = sig.by_name.get(name)
    if not ds:
        b = BUILTINS.get(name)
        return b.type if b is not None else None
    # an overloaded name has no one type; say nothing rather than guess
    types = {str(d.type) for d in ds if d.type is not None}
    if len(types) != 1:
        return None
    return ds[-1].type


def infer_simple_type(node: Node, sig: Signature) -> Node | None:
    """The type of a term, where that is readable off the declarations alone."""
    if node.is_atom:
        if node.text in ("true", "false"):
            return Node(node.path, node.line, node.col, node.end_line, node.end_col, text="Bool")
        cat = node.literal_category
        if cat is not None:
            return sig.literal_type.get(cat)
        return declared_type(node.text or "", sig)
    head = node.head
    if head is None:
        return None
    if head == "as" and len(node.children) == 3:
        return node.children[2]
    if head in ("eo::var",) and len(node.children) == 3:
        return node.children[2]
    decl_type = declared_type(head, sig)
    parts = arrow_parts(decl_type)
    if parts is None:
        return None
    nargs = len(node.children) - 1
    if nargs >= len(parts):
        return None
    remaining = parts[nargs:]
    if len(remaining) == 1:
        return remaining[0]
    return None  # a partial application: say nothing


def is_pattern_variable(node: Node, params: dict[str, object]) -> bool:
    return node.is_atom and (node.text in params)
