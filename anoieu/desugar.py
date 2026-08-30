"""The surface-to-core map: what the parser builds from what you wrote.

Eunoia's sugar is where its characteristic bugs live -- a nil terminator
inserted at a tail, a `:list` parameter folded in with `eo::list_concat`, a
chain expanded into a conjunction that is itself expanded again -- and none of
it is visible in the file. This module computes it, so a finding can say what a
term *means* rather than what it looks like, and so `anoieu desugar` can answer
the question that today costs a stage run: what did my sugar become.

The rules are the ones in the user manual, under "Declarations with attributes"
and "Parameterized constants with Attributes". Desugaring runs bottom-up, and
applies at parse time only: a higher-order application `(_ f a b)` does not
trigger the policy for `f`, and neither does macro expansion.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import Decl, Param, Signature
from .resolve import resolve_decl
from .syntax.parser import Node

_RIGHT_NIL = {":right-assoc-nil", ":right-assoc-non-singleton-nil"}
_LEFT_NIL = {":left-assoc-nil", ":left-assoc-non-singleton-nil"}
_NS_NIL = {":right-assoc-non-singleton-nil", ":left-assoc-non-singleton-nil"}


def atom(text: str, like: Node | None = None) -> Node:
    src = like or Node("<desugar>", 0, 0, 0, 0, text="")
    return Node(src.path, src.line, src.col, src.end_line, src.end_col, text=text)


def app(items: list[Node], like: Node | None = None) -> Node:
    src = like or items[0]
    node = Node(src.path, src.line, src.col, src.end_line, src.end_col, items=[], kind="list")
    node.items = items
    return node


def call(name: str, args: list[Node], like: Node | None = None) -> Node:
    return app([atom(name, like)] + args, like)


@dataclass
class Scope:
    """What the desugarer needs to know beside the signature: which names in
    scope are parameters, and which of those are marked `:list`."""

    sig: Signature
    params: dict[str, Param] = field(default_factory=dict)
    bound: dict[str, Node] = field(default_factory=dict)  # binder variables

    def is_list(self, node: Node) -> bool:
        if not node.is_atom:
            return False
        p = self.params.get(node.text or "")
        return p is not None and p.has(":list")

    def child(self, extra: dict[str, Node]) -> "Scope":
        return Scope(self.sig, self.params, {**self.bound, **extra})


def is_ground(node: Node, decl: Decl) -> bool:
    """Whether a nil terminator is one term, or a family indexed by the type.

    A nil that names a parameter of the declaration is a family -- `(bvzero m)`
    is a different zero per width -- and an application inserts
    `(eo::nil f (eo::typeof t1))` in its place rather than the term itself. A nil
    that names no parameter is one term, however it is written: `eo::List::nil`
    is a constant, and `($arith_mk_one Int)` is a call that will evaluate to one.
    """
    names = {p.name for p in decl.params}
    return not any(nd.is_atom and nd.text in names for nd in node.walk())


def match_type(pattern: Node, actual: Node, names: set[str]) -> dict[str, Node] | None:
    """Bind a declaration's parameters by matching its argument type against a
    concrete one: `(BitVec m)` against `(BitVec 4)` binds `m` to `4`."""
    if pattern.is_atom:
        if pattern.text in names:
            return {pattern.text or "": actual}
        return {} if actual.is_atom and actual.text == pattern.text else None
    if not actual.is_list or len(pattern.children) != len(actual.children):
        return None
    out: dict[str, Node] = {}
    for p, a in zip(pattern.children, actual.children):
        got = match_type(p, a, names)
        if got is None:
            return None
        for k, v in got.items():
            if k in out and str(out[k]) != str(v):
                return None
            out[k] = v
    return out


def _substitute(node: Node, binding: dict[str, Node]) -> Node:
    if node.is_atom:
        return binding.get(node.text or "", node)
    return app([_substitute(c, binding) for c in node.children], node)


def _expand_defines(node: Node, sig: Signature, depth: int = 6) -> Node:
    """Definitions are macros, so a nil written as one is that macro applied."""
    if depth <= 0:
        return node
    if node.is_atom:
        d = sig.defines_by_name.get(node.text or "")
        if d is not None and not d.params and d.body is not None:
            return _expand_defines(d.body, sig, depth - 1)
        return node
    kids = [_expand_defines(c, sig, depth - 1) for c in node.children]
    head = node.head
    d = sig.defines_by_name.get(head or "")
    if d is not None and d.params and d.body is not None and len(kids) - 1 == len(d.params):
        binding = {p.name: k for p, k in zip(d.params, kids[1:])}
        return _expand_defines(_substitute(d.body, binding), sig, depth - 1)
    return app(kids, node)


def _ground_nil(decl: Decl, value: Node, first: Node, scope: "Scope", like: Node) -> Node | None:
    """The nil an application actually gets, where the type settles it.

    `(bvor u v)` with `u : (BitVec 4)` inserts `(eo::nil bvor (eo::typeof u))`,
    which ethos then evaluates to `#b0000`. This does the same, and answers None
    -- leaving the placeholder in place -- wherever it cannot.
    """
    from .eval import evaluate
    from .typing import full_arity, infer

    t = infer(first, scope.params, scope.sig)
    if t is None or any(nd.is_atom and nd.text in scope.params for nd in t.walk()):
        return None
    fa = full_arity(decl)
    if fa is None or not fa[0]:
        return None
    binding = match_type(fa[0][0], t, {p.name for p in decl.params})
    if binding is None:
        return None
    nil = _expand_defines(_substitute(value, binding), scope.sig)
    return evaluate(nil) or (nil if is_ground(nil, decl) else None)


def _nil_for(decl: Decl, value: Node, args: list[Node], like: Node, scope: "Scope") -> Node:
    if is_ground(value, decl):
        return value
    settled = _ground_nil(decl, value, args[0], scope, like)
    if settled is not None:
        return settled
    # the type of the first argument settles the parameters of the nil, since an
    # operator with a non-ground nil is required to be of type (-> T T T)
    return call("eo::nil", [atom(decl.name, like), call("eo::typeof", [args[0]], like)], like)


def _var_list(node: Node) -> list[tuple[str, Node]] | None:
    """`((x Int) (y Int))` -- the variable list a binder may take, or None."""
    if not node.is_list or not node.children:
        return None
    out: list[tuple[str, Node]] = []
    for item in node.children:
        if not (item.is_list and len(item.children) == 2 and item.children[0].is_atom):
            return None
        out.append((item.children[0].text or "", item.children[1]))
    return out


def _replace(node: Node, binding: dict[str, Node]) -> Node:
    """Put what a binding names in place of the name, everywhere in a term."""
    if not binding:
        return node
    if node.is_atom:
        return binding.get(node.text or "", node)
    return app([_replace(c, binding) for c in node.children], node)


def desugar(node: Node, scope: Scope) -> Node:
    """The term the parser builds from this one."""
    if node.is_atom:
        return scope.bound.get(node.text or "", node)
    if not node.children:
        return node
    head = node.children[0]
    args = node.children[1:]
    name = head.text if head.is_atom else None

    # `(as X T)` is an opaque application: a constant indexed by its type
    if name == "as" and len(args) == 2:
        return call("_", [desugar(args[0], scope), args[1]], node)
    # `eo::define` binds a name to a term while the body is read; the parser
    # inlines it, so the built term holds neither the binding nor the name
    if name == "eo::define" and len(args) == 2 and args[0].is_list:
        binding: dict[str, Node] = {}
        for pair in args[0].children:
            if pair.is_list and len(pair.children) == 2 and pair.children[0].is_atom:
                # the value is put in as written and desugared with the body, so
                # that a `:list` parameter it names still reads as a tail
                binding[pair.children[0].text or ""] = pair.children[1]
        return desugar(_replace(args[1], binding), scope)
    # a higher-order application does not re-enter the policy for its operator
    if name == "_" or (name or "").startswith("eo::"):
        return app([head] + [desugar(a, scope) for a in args], node)
    if name is None or name in scope.params or name in scope.bound:
        return app([desugar(c, scope) for c in node.children], node)

    decl = resolve_decl(name, scope.sig)
    attr = decl.constructor_attr if decl is not None else None
    if decl is None or attr is None:
        return app([head] + [desugar(a, scope) for a in args], node)

    # a binder may take a variable list as its first argument, which binds those
    # names while the rest of the application is read
    if attr.key == ":binder" and args:
        vlist = _var_list(args[0])
        if vlist is not None and attr.value is not None:
            vars_ = [
                call("eo::var", [atom(f'"{n}"', args[0]), t], args[0]) for n, t in vlist
            ]
            inner = scope.child({n: v for (n, _t), v in zip(vlist, vars_)})
            cons = desugar(call(attr.value.text or "", vars_, args[0]), inner)
            rest = [desugar(a, inner) for a in args[1:]]
            return app([head, cons] + rest, node)
        return app([head] + [desugar(a, scope) for a in args], node)

    args = [desugar(a, scope) for a in args]
    return _apply_attr(head, decl, attr.key, attr.value, args, scope, node)


def _apply_attr(
    head: Node,
    decl: Decl,
    key: str,
    value: Node | None,
    args: list[Node],
    scope: Scope,
    like: Node,
) -> Node:
    n = len(args)

    if key in (":right-assoc", ":left-assoc"):
        if n <= 2:
            return app([head] + args, like)
        if key == ":right-assoc":
            r = args[-1]
            for t in reversed(args[:-1]):
                r = app([head, t, r], like)
        else:
            r = args[0]
            for t in args[1:]:
                r = app([head, r, t], like)
        return r

    if key in _RIGHT_NIL or key in _LEFT_NIL:
        if value is None or not args:
            return app([head] + args, like)
        right = key in _RIGHT_NIL
        nil = _nil_for(decl, value, args, like, scope)
        edge = args[-1] if right else args[0]
        if scope.is_list(edge):
            r = edge
            rest = args[:-1] if right else args[1:]
        else:
            r = nil
            rest = list(args)
        for t in reversed(rest) if right else rest:
            if scope.is_list(t):
                r = call("eo::list_concat", [atom(decl.name, like), t, r], like)
            else:
                r = app([head, t, r], like) if right else app([head, r, t], like)
        if key in _NS_NIL and sum(1 for a in args if not scope.is_list(a)) < 2:
            r = call("eo::list_singleton_elim", [atom(decl.name, like), r], like)
        return r

    if key in (":chainable", ":pairwise"):
        if value is None:
            return app([head] + args, like)
        combiner = resolve_decl(value.text, scope.sig)
        if n == 1:
            # a chain of one is the unit of the combining operator
            if combiner is not None and combiner.nil is not None:
                return combiner.nil
            return app([head] + args, like)
        if n <= 2:
            return app([head] + args, like)
        if key == ":chainable":
            parts = [app([head, args[i], args[i + 1]], like) for i in range(n - 1)]
        else:
            parts = [
                app([head, args[i], args[j]], like)
                for i in range(n)
                for j in range(i + 1, n)
            ]
        return desugar(app([value] + parts, like), scope)

    if key == ":arg-list":
        if value is None:
            return app([head] + args, like)
        if n == 1 and scope.is_list(args[0]):
            return app([head, args[0]], like)
        return app([head, desugar(app([value] + args, like), scope)], like)

    return app([head] + args, like)


# ---------------------------------------------------------------- printing


def curry(node: Node) -> Node:
    """The term as the core sees it: every application unary.

    `(f a b)` is `(f a)` applied to `b`, printed the way ethos prints it --
    the first application bare, every one after it under `_`.
    """
    if node.is_atom:
        return node
    kids = [curry(c) for c in node.children]
    if len(kids) <= 2:
        return app(kids, node) if kids else node
    r = app(kids[:2], node)
    for a in kids[2:]:
        r = app([atom("_", node), r, a], node)
    return r


def uncurry(node: Node) -> Node:
    """The inverse, so that two terms can be compared however they were built."""
    if node.is_atom:
        return node
    kids = [uncurry(c) for c in node.children]
    if kids and kids[0].is_atom and kids[0].text == "_" and len(kids) == 3:
        inner = kids[1]
        if inner.is_list:
            return app(list(inner.children) + [kids[2]], node)
        return app([inner, kids[2]], node)
    return app(kids, node)


def scope_of(sig: Signature, params: list[Param] | None = None) -> Scope:
    return Scope(sig, {p.name: p for p in (params or [])})
