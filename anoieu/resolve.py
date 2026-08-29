"""Resolving a name to the declaration that gives it its behaviour.

Two things stand between a name and its declaration, and both matter for every
check that asks "is this operator n-ary, and what is its nil?":

- **definitions.** `(define @list () eo::List::cons)` makes `@list` another name
  for a constructor, and CPC writes its patterns and its `:binder` attribute
  with the alias rather than with the name behind it.
- **the builtin signature.** `eo::List::cons` is declared by ethos itself, as a
  right-associative operator with nil `eo::List::nil`, and no file says so.
"""

from __future__ import annotations

from .diagnostics import Span
from .model import Attribute, Decl, Signature
from .syntax.parser import Node


def _atom(text: str) -> Node:
    return Node("<builtin>", 0, 0, 0, 0, text=text)


def _builtin(name: str, attrs: list[Attribute], type_text: str | None = None) -> Decl:
    return Decl(
        name=name,
        kind="builtin",
        type=_atom(type_text) if type_text else None,
        params=[],
        attrs=attrs,
        span=Span("<builtin>", 0, 0),
    )


_BUILTIN_SPAN = Span("<builtin>", 0, 0)

# The signature ethos assumes: see "Generic Reasoning about Datatypes" in the
# user manual, which states these three declarations exactly.
BUILTINS: dict[str, Decl] = {
    "eo::List": _builtin("eo::List", [], "Type"),
    "eo::List::nil": _builtin("eo::List::nil", [], "eo::List"),
    "eo::List::cons": _builtin(
        "eo::List::cons",
        [Attribute(":right-assoc-nil", _atom("eo::List::nil"), _BUILTIN_SPAN)],
    ),
    "Bool": _builtin("Bool", [], "Type"),
    "true": _builtin("true", [], "Bool"),
    "false": _builtin("false", [], "Bool"),
    "Type": _builtin("Type", []),
}


def resolve_decl(name: str | None, sig: Signature, depth: int = 8) -> Decl | None:
    """The declaration a name stands for, following `define` aliases."""
    if not name or depth <= 0:
        return None
    ds = sig.by_name.get(name)
    if ds:
        return ds[-1]
    d = sig.defines_by_name.get(name)
    if d is not None and not d.params and d.body is not None and d.body.is_atom:
        return resolve_decl(d.body.text, sig, depth - 1)
    return BUILTINS.get(name)


def resolve_name(name: str | None, sig: Signature, depth: int = 8) -> str | None:
    """The name behind an alias, for saying which symbol a finding is about."""
    if not name or depth <= 0:
        return name
    if name in sig.by_name or name in BUILTINS:
        return name
    d = sig.defines_by_name.get(name)
    if d is not None and not d.params and d.body is not None and d.body.is_atom:
        return resolve_name(d.body.text, sig, depth - 1)
    return name


def expand_alias(node: Node, sig: Signature, depth: int = 8) -> Node:
    """A term with its nullary `define` aliases expanded.

    `@re.empty` is `(str.to_re "")` and `@list.nil` is `eo::List::nil`; a
    signature writes the alias in one place and the thing itself in another, and
    a check comparing two terms has to see through that.
    """
    if depth <= 0 or not node.is_atom:
        return node
    d = sig.defines_by_name.get(node.text or "")
    if d is None or d.params or d.body is None:
        return node
    return expand_alias(d.body, sig, depth - 1)


def canonical_head(node: Node, sig: Signature) -> str | None:
    """The head a term has once its aliases are expanded."""
    expanded = expand_alias(node, sig)
    if expanded.is_atom:
        return resolve_name(expanded.text, sig)
    return resolve_name(expanded.head, sig)
