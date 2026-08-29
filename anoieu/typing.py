"""Shallow typing: the type of a term, where its *head* settles it.

This is not the type checker of M3. It answers one question -- what type
constructor does this term have -- and only where the answer is read off the
declarations: an application of a symbol whose arrow type is known, a parameter
whose type its list gave, a literal whose category has a `declare-consts`. It
answers `None` everywhere else, and a check that gets `None` says nothing.

That is enough for the questions ethos never asks: is a rule's conclusion a
`Bool`, does a program case return what the program declared, is a symbol
applied to more arguments than it takes.
"""

from __future__ import annotations

from .model import CONSTRUCTOR_ATTRS, Decl, Param, Signature
from .resolve import resolve_decl
from .shape import arrow_parts, strip_requires, type_head
from .syntax.parser import Node

# Terms whose type is the type of a term inside them.
_PASSTHROUGH = {
    "eo::requires": 3,  # (eo::requires a b t)
    "eo::define": 2,  # (eo::define ((v e)) body)
}


def full_arity(decl: Decl) -> tuple[list[Node], Node] | None:
    """The argument types a symbol expects and the type it then has.

    A `declare-parameterized-const` prepends its *explicit* parameters to the
    arrow: `(declare-parameterized-const eq ((T Type)) (-> T T Bool))` is
    applied to three arguments, and one whose parameters are all `:implicit` to
    the two its arrow names.
    """
    if decl.type is None:
        return None
    explicit = [p for p in decl.params if not p.has(":implicit")]
    if any(p.type is None for p in explicit):
        return None
    parts = arrow_parts(decl.type)
    tail = parts if parts is not None else [decl.type]
    args = [p.type for p in explicit] + tail[:-1]
    return args, tail[-1]


def is_variadic(decl: Decl) -> bool:
    return any(a.key in CONSTRUCTOR_ATTRS for a in decl.attrs)


def _subst(node: Node, binding: dict[str, Node]) -> Node:
    """A type with its parameters replaced by what the arguments bound them to."""
    if node.is_atom:
        return binding.get(node.text or "", node)
    out = Node(node.path, node.line, node.col, node.end_line, node.end_col, items=[], kind="list")
    out.items = [_subst(c, binding) for c in node.children]
    return out


def _instantiate(
    ret: Node,
    formals: list[Node],
    actuals: list[Node],
    tvars: set[str],
    params: dict[str, Param],
    sig: Signature,
    depth: int,
) -> Node | None:
    """The return type of an application, with the callee's own type parameters
    bound by the arguments.

    `ite : (-> Bool A A A)` returns `A`, which says nothing until the arguments
    say what `A` is; with a `Bool` second argument it returns `Bool`. Only the
    easy direction is done -- a formal that is a bare type parameter takes the
    type of the actual standing there -- which is what the declarations in
    practice are written as.
    """
    binding: dict[str, Node] = {}
    for formal, actual in zip(formals, actuals):
        if not (formal.is_atom and formal.text in tvars):
            continue
        if formal.text in binding:
            continue
        got = infer(actual, params, sig, depth - 1)
        if got is not None:
            binding[formal.text or ""] = strip_requires(got) or got
    out = _subst(ret, binding) if binding else ret
    if any(nd.is_atom and nd.text in tvars for nd in out.walk()):
        return None
    return out


def infer(
    node: Node, params: dict[str, Param], sig: Signature, depth: int = 6
) -> Node | None:
    """The type of a term, or None where that is not readable off declarations."""
    if depth <= 0:
        return None
    if node.is_atom:
        p = params.get(node.text or "")
        if p is not None:
            return p.type
        cat = node.literal_category
        if cat == "<boolean>":
            return Node(node.path, node.line, node.col, node.line, node.col, text="Bool")
        if cat is not None:
            return sig.literal_type.get(cat)
        decl = resolve_decl(node.text, sig)
        if decl is None:
            return None
        fa = full_arity(decl)
        if fa is None:
            return None
        args, ret = fa
        if args:
            return None  # a bare function name is not applied
        tvars = type_params_of({p.name: p for p in decl.params})
        return None if any(nd.is_atom and nd.text in tvars for nd in ret.walk()) else ret
    head = node.head
    if head is None:
        return None
    if head in _PASSTHROUGH:
        idx = _PASSTHROUGH[head]
        child = node.at(idx)
        return infer(child, params, sig, depth - 1) if child is not None else None
    if head == "eo::ite" and len(node.children) == 4:
        a = infer(node.children[2], params, sig, depth - 1)
        b = infer(node.children[3], params, sig, depth - 1)
        if a is None or b is None:
            return a or b
        return a if type_head(strip_requires(a)) == type_head(strip_requires(b)) else None
    if head.startswith("eo::") or head == "_":
        return None
    prog = sig.programs_by_name.get(head)
    if prog is not None:
        if not prog.sig_args or len(node.children) - 1 != len(prog.sig_args):
            return None
        if prog.sig_ret is None:
            return None
        tvars = type_params_of({p.name: p for p in prog.params})
        return _instantiate(
            prog.sig_ret, prog.sig_args, node.children[1:], tvars, params, sig, depth
        )
    if head in params:
        return None
    define = sig.defines_by_name.get(head)
    if define is not None and define.body is not None:
        inner = {p.name: p for p in define.params}
        return infer(define.body, inner, sig, depth - 1)
    decl = resolve_decl(head, sig)
    if decl is None:
        return None
    fa = full_arity(decl)
    if fa is None:
        return None
    args, ret = fa
    nargs = len(node.children) - 1
    if nargs != len(args):
        return None  # partial application, or an arity this cannot account for
    tvars = type_params_of({p.name: p for p in decl.params})
    return _instantiate(ret, args, node.children[1:], tvars, params, sig, depth)


def type_is(node: Node | None, name: str, type_params: set[str]) -> bool | None:
    """Whether a type is the named constructor: True, False, or None for
    "cannot tell", which is what a type variable answers."""
    head = type_head(strip_requires(node))
    if head is None or head in type_params:
        return None
    return head == name


def type_params_of(params: dict[str, Param]) -> set[str]:
    """The parameters that stand for types, which unify with anything."""
    return {
        name
        for name, p in params.items()
        if p.type is not None and p.type.is_atom and p.type.text == "Type"
    }
