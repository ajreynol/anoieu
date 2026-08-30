"""Checks on programs and on the patterns rules and programs match with.

Matching in ethos binds a parameter to whatever stands in its place --
`TypeChecker::match` says so in a comment, "note that we do not ensure the types
match here" -- so a case whose arguments are all parameters matches everything,
and every case after it is dead. The `:list` checks are the other half: a
parameter that is a *tail* of an n-ary application has to say so, and one that
says so in the wrong place makes the pattern illegal.
"""

from __future__ import annotations

from typing import Iterator

from ..diagnostics import Diagnostic, Severity
from ..model import EO_OPERATORS, NIL_ATTRS, Param, ProgramDecl, Signature
from ..desugar import Scope, desugar
from ..resolve import canonical_head, resolve_decl, resolve_name
from ..syntax.parser import Node
from . import Context, check

_RIGHT_NIL = {":right-assoc-nil", ":right-assoc-non-singleton-nil"}
_LEFT_NIL = {":left-assoc-nil", ":left-assoc-non-singleton-nil"}


def _nil_attr(sig: Signature, head: str | None):
    if head is None:
        return None
    d = resolve_decl(head, sig)
    if d is None:
        return None
    for a in d.attrs:
        if a.key in NIL_ATTRS:
            return (d, a)
    return None


def _param_map(params: list[Param]) -> dict[str, Param]:
    return {p.name: p for p in params}


def _walk_pattern(
    node: Node, params: dict[str, Param], sig: Signature, where: str
) -> Iterator[Diagnostic]:
    """Findings about one pattern: a program case's left-hand side, a rule's
    premise or argument pattern."""
    if not node.is_list or not node.children:
        return
    for child in node.children[1:]:
        yield from _walk_pattern(child, params, sig, where)
    found = _nil_attr(sig, node.head)
    if found is None:
        return
    decl, attr = found
    args = node.children[1:]
    if len(args) < 2:
        return
    right = attr.key in _RIGHT_NIL
    tail_index = len(args) - 1 if right else 0

    tail = args[tail_index]
    if tail.is_atom and tail.text in params and not params[tail.text].has(":list"):
        p = params[tail.text]
        yield Diagnostic(
            code="EO0054",
            severity=Severity.HINT,
            message=f"this pattern matches an `{decl.name}` of exactly "
            f"{len(args)} element(s)",
            span=tail.span,
            label=f"`{p.name}` is one element, not the tail",
            notes=[
                f"`{decl.name}` is `{attr.key}`, so the parser builds "
                f"{desugar(node, Scope(sig, params))} from this, which matches an "
                f"{decl.name}-list of exactly {len(args)} elements",
                f"in {where}",
            ],
            help=f"mark `{p.name}` with `:list` in the parameter list to match the tail",
        )


@check(
    "EO0054",
    "a pattern matches a fixed number of elements of an n-ary operator",
    page="""
For an operator with a nil terminator, `(or l xs)` is sugar for
`(or l (or xs false))`: it matches an `or` of *exactly two* elements. Marking
`xs` with `:list` in the enclosing parameter list is what makes it match the
tail. The manual gives this as its own worked "incorrect version": the program
works on two-element lists and silently fails to evaluate on longer ones, which
in a proof surfaces as a checking failure with no indication of the cause.

A pattern that really does mean "exactly two elements" is legal and common, so
this is a hint: it says what the pattern matches, and leaves the question of
whether that was the intention to the reader.
""",
)
def list_annotation(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for prog in sig.programs:
        params = _param_map(prog.params)
        for lhs, _rhs in prog.cases:
            for arg in lhs.children[1:]:
                yield from _walk_pattern(arg, params, sig, f"program `{prog.name}`")
    for rule in sig.rules:
        params = _param_map(rule.params)
        pats = list(rule.premises) + list(rule.args)
        if rule.assumption is not None:
            pats.append(rule.assumption)
        for pat in pats:
            yield from _walk_pattern(pat, params, sig, f"rule `{rule.name}`")


@check(
    "EO0055",
    "a pattern desugars to something that cannot be matched on",
    page="""
A pattern is matched, not evaluated, so it may not hold a term the evaluator
would rewrite. The sugar is what usually puts one there: a `:list` parameter
anywhere but the tail of an n-ary application is folded in with
`eo::list_concat`, and an operator with a type-dependent nil inserts an
`eo::nil` where the pattern ends.

anoieu desugars the pattern and looks at the result, which is the same rule
ethos applies -- it answers `Cannot match on evaluatable subterm`, naming the
built term rather than the annotation that produced it. `anoieu desugar --term`
prints the same form.
""",
)
def unmatchable_pattern(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature

    def evaluatable(node: Node, params: dict[str, Param]) -> Node | None:
        """The first subterm ethos would rewrite, which a pattern may not hold."""
        from ..typing import infer

        stack = [node]
        while stack:
            nd = stack.pop()
            if not nd.is_list:
                continue
            if nd.head not in EO_OPERATORS:
                stack.extend(nd.children)
                continue
            if nd.head == "eo::nil" and len(nd.children) == 3:
                # `(eo::nil f (eo::typeof x))` is the placeholder the parser
                # inserts for a nil that depends on the type. Where x's type is
                # ground it resolves to a term, and the pattern is fine; where it
                # is not, it stays, and ethos refuses the case.
                arg = nd.children[2]
                subject = arg.children[1] if arg.is_list and len(arg.children) == 2 else None
                if subject is not None:
                    t = infer(subject, params, sig)
                    if t is not None and not any(
                        x.is_atom and x.text in params for x in t.walk()
                    ):
                        continue  # resolved by evaluation, subtree and all
            return nd
        return None

    def scan(pattern: Node, params: dict[str, Param], where: str) -> Iterator[Diagnostic]:
        built = desugar(pattern, Scope(sig, params))
        bad = evaluatable(built, params)
        if bad is None:
            return
        yield Diagnostic(
            code="EO0055",
            severity=Severity.ERROR,
            message=f"this pattern cannot be matched on: the parser builds "
            f"{bad.head} into it",
            span=pattern.span,
            label=f"becomes {built}",
            notes=[
                f"in {where}",
                "a pattern is matched rather than evaluated, so it may hold no "
                "application the evaluator would rewrite",
                "ethos reports this as `Cannot match on evaluatable subterm`",
            ],
        )

    for prog in sig.programs:
        params = _param_map(prog.params)
        for lhs, _rhs in prog.cases:
            for arg in lhs.children[1:]:
                yield from scan(arg, params, f"program `{prog.name}`")
    for rule in sig.rules:
        params = _param_map(rule.params)
        pats = list(rule.premises) + list(rule.args)
        if rule.assumption is not None:
            pats.append(rule.assumption)
        for pat in pats:
            yield from scan(pat, params, f"rule `{rule.name}`")


@check(
    "EO0051",
    "a program case does not match the program's signature",
    page="""
A program declares its arity with `:signature`, and every case has to match it.
A case of the wrong arity can never fire.
""",
)
def case_arity(ctx: Context) -> Iterator[Diagnostic]:
    for prog in ctx.signature.programs:
        if not prog.cases or not prog.sig_args:
            continue
        want = len(prog.sig_args)
        for lhs, _rhs in prog.cases:
            if not lhs.is_list:
                continue
            got = len(lhs.children) - 1
            if got != want:
                yield Diagnostic(
                    code="EO0051",
                    severity=Severity.ERROR,
                    message=f"this case of `{prog.name}` takes {got} argument(s), "
                    f"but its signature declares {want}",
                    span=lhs.span,
                    help="every case matches an application of the program to all its arguments",
                )


@check(
    "EO0052",
    "a program case can never be reached",
    page="""
A program is an *ordered* list of rewrite rules, first match wins, and matching
does not check types -- `TypeChecker::match` binds a parameter to whatever term
stands in its place. So an earlier case shadows a later one whenever its pattern
is the more general of the two: a case whose arguments are all parameters
matches every application, and `(($p (or x xs) l) ...)` matches everything
`(($p (or a xs) l) ...)` does.

Patterns are compared after desugaring, since that is what matching sees: a
`:list` parameter in a tail position stands for a list of any length, and one
that is not stands for a list of exactly the length written.
""",
)
def unreachable_case(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for prog in ctx.signature.programs:
        params = _param_map(prog.params)
        scope = Scope(sig, params)
        built = [(lhs, desugar(lhs, scope)) for lhs, _rhs in prog.cases]
        for j in range(1, len(built)):
            for i in range(j):
                if not _subsumes(built[i][1], built[j][1], params):
                    continue
                earlier = built[i][0]
                general = all(
                    a.is_atom and a.text in params
                    for a in (earlier.children[1:] if earlier.is_list else [])
                )
                why = (
                    "matches every application, since its arguments are all parameters"
                    if general
                    else "matches everything this one matches"
                )
                yield Diagnostic(
                    code="EO0052",
                    severity=Severity.WARNING,
                    message=f"this case of `{prog.name}` can never be reached",
                    span=built[j][0].span,
                    label="shadowed",
                    notes=[
                        f"the case at line {earlier.line} {why}, and a program takes "
                        "the first case that matches"
                    ],
                )
                break


def _subsumes(general: Node, special: Node, params: dict[str, Param]) -> bool:
    """Whether every application the second pattern matches, the first matches.

    One-way matching: a parameter of the *general* pattern stands for anything,
    consistently, and everything in the special one is rigid.
    """
    binding: dict[str, str] = {}

    def walk(g: Node, s: Node) -> bool:
        if g.is_atom and g.text in params:
            prev = binding.setdefault(g.text or "", str(s))
            return prev == str(s)
        if g.is_atom or s.is_atom:
            return g.is_atom and s.is_atom and g.text == s.text
        if len(g.children) != len(s.children):
            return False
        return all(walk(a, b) for a, b in zip(g.children, s.children))

    return walk(general, special)


@check(
    "EO0053",
    "a program walks a list and has no case for its end",
    page="""
A program that matches `(f x xs)` with `xs` marked `:list` and then calls itself
on `xs` is walking an f-list, and needs a case for the nil that ends it --
`(($p false) ...)` for an `or`-list, `(($p true) ...)` for an `and`-list -- or a
parameter that catches it. Without one the last step does not evaluate, and what
a proof reports is that a step failed to check, not that a case was missing.

The recursive call is what identifies a walk. A program that merely *matches* an
application of an n-ary operator -- to say what its unit is, say -- is not
walking anything and is not reported.
""",
)
def missing_nil_case(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    for prog in sig.programs:
        if not prog.cases:
            continue
        params = _param_map(prog.params)
        arity = max((len(lhs.children) - 1) for lhs, _ in prog.cases if lhs.is_list)
        for i in range(arity):
            walkers: dict[str, tuple] = {}
            shapes: list[Node] = []
            covered = False
            for lhs, rhs in prog.cases:
                arg = lhs.at(i + 1)
                if arg is None:
                    continue
                shapes.append(arg)
                if arg.is_atom and arg.text in params:
                    # at a program's own argument position a parameter matches
                    # anything, `:list` or not: the annotation only says how it
                    # behaves as a child of an n-ary application.
                    covered = True
                    break
                if not arg.is_list or len(arg.children) < 3:
                    continue
                found = _nil_attr(sig, arg.head)
                if found is None:
                    continue
                decl, attr = found
                tail = arg.children[-1] if attr.key in _RIGHT_NIL else arg.children[1]
                if not (tail.is_atom and tail.text in params and params[tail.text].has(":list")):
                    continue
                if _recurses_on(rhs, prog.name, i, tail.text or ""):
                    walkers.setdefault(decl.name, (decl, attr, arg))
            if covered:
                continue
            for name, (decl, attr, arg) in walkers.items():
                if attr.value is None or any(_is_same_term(s, attr.value, sig) for s in shapes):
                    continue
                if any(_stops_before_nil(s, name, attr, params, sig) for s in shapes):
                    # a case matching a fixed number of elements -- `(re.inter c1)`,
                    # one element and the nil -- ends the walk one step early, so
                    # the nil itself is never reached.
                    continue
                if not _is_ground_nil(attr.value, decl):
                    # a nil that depends on the instantiation -- `(seq.empty T)`,
                    # `(eo::to_bin m 0)` -- is spelt differently in each base case
                    # a program writes, e.g. `""` for the string instance, so
                    # whether a case covers it is not decidable here.
                    continue
                yield Diagnostic(
                    code="EO0053",
                    severity=Severity.WARNING,
                    message=f"`{prog.name}` walks an `{name}`-list and has no case for "
                    f"its nil `{attr.value}`",
                    span=arg.span,
                    label=f"this case takes the head and recurses on the tail",
                    notes=[
                        f"`{name}` is `{attr.key}`, so a list of it ends in {attr.value}",
                        "the last step of the recursion does not evaluate",
                    ],
                    help=f"add a case matching `{attr.value}` in this position, "
                    "or a parameter that catches it",
                )


def _recurses_on(rhs: Node, prog: str, index: int, tail: str) -> bool:
    """Whether the body calls the program again with `tail` in the same place,
    unguarded.

    A call under an `eo::ite` or `eo::requires` whose condition mentions the
    tail is guarded -- `(eo::ite (eo::eq r1 re.none) n ($p r1))` stops at the nil
    without ever applying the program to it -- so it is not a walk that needs a
    base case.
    """
    return _find_call(rhs, prog, index, tail, guarded=False)


def _find_call(node: Node, prog: str, index: int, tail: str, guarded: bool) -> bool:
    if not node.is_list:
        return False
    head = node.head
    if head in ("eo::ite", "eo::requires") and len(node.children) >= 3:
        cond = node.children[1:3] if head == "eo::requires" else node.children[1:2]
        mentions = any(
            any(s.text == tail for s in c.symbols()) for c in cond
        )
        rest_guarded = guarded or mentions
        for child in node.children[1:]:
            if _find_call(child, prog, index, tail, rest_guarded):
                return True
        return False
    if head == prog and not guarded:
        arg = node.at(index + 1)
        if arg is not None and arg.is_atom and arg.text == tail:
            return True
    for child in node.children:
        if _find_call(child, prog, index, tail, guarded):
            return True
    return False


def _stops_before_nil(
    shape: Node, opname: str, attr, params: dict[str, Param], sig: Signature
) -> bool:
    """Whether a case matches a list of the same operator of fixed length."""
    if not shape.is_list or resolve_name(shape.head, sig) != opname:
        return False
    args = shape.children[1:]
    if not args:
        return False
    tail = args[-1] if attr.key in _RIGHT_NIL else args[0]
    return not (tail.is_atom and tail.text in params and params[tail.text].has(":list"))


def _is_ground_nil(nil: Node, decl) -> bool:
    """Whether a nil terminator is one term rather than a family of them."""
    params = {p.name for p in decl.params}
    for nd in nil.walk():
        if not nd.is_atom:
            continue
        text = nd.text or ""
        if text in params:
            return False
        if text.startswith("eo::") or text.startswith("$"):
            return False
    return True


def _is_same_term(a: Node, b: Node, sig: Signature) -> bool:
    """Whether two terms could be the same term, modulo `define` aliases.

    A signature spells one constructor several ways -- `@list.nil` for
    `eo::List::nil`, `@re.empty` for `(str.to_re "")` -- so a case covers a nil
    when the two agree once the aliases are expanded. Comparison is by head,
    which is deliberately generous: this decides whether to stay quiet.
    """
    ha, hb = canonical_head(a, sig), canonical_head(b, sig)
    return ha is not None and ha == hb


@check(
    "EO0057",
    "a program is declared and never defined",
    page="""
`program` with no body is a forward declaration, to be defined later. One that
never is reaches the backends as a name with no meaning: under SMT-LIB a free
uninterpreted function the solver may read as it likes, under Lean a name that
was never written. Ethos itself simply never evaluates it.
""",
)
def forward_declared(ctx: Context) -> Iterator[Diagnostic]:
    defined: set[str] = {p.name for p in ctx.signature.programs if p.cases}
    reported: set[str] = set()
    for prog in ctx.signature.programs:
        if prog.cases or prog.name in defined or prog.name in reported:
            continue
        reported.add(prog.name)
        yield Diagnostic(
            code="EO0057",
            severity=Severity.WARNING,
            message=f"`{prog.name}` is declared with no cases and never defined "
            f"under this entry point",
            span=prog.span,
            notes=[
                "a forward declaration is defined by some later file; whether it is "
                "depends on which file the run started from"
            ],
            help="give it a body, or check that the entry point includes the file "
            "that does",
        )


@check(
    "EO0060",
    "a program nothing reaches",
    page="""
A program no rule, program or definition names is dead: it is compiled, trimmed
and published for nothing, and if it was meant to be used, the rule that meant
to use it does not.

**Reachability is relative to a profile**, and this check was wrong about that
once: cvc5 declined a finding that `$is_app` was dead, because the rule using it
is in the expert signature and cvc5 loads the base and expert files in order
into one symbol table. Several files given to a run are now one ordered profile,
and where a run has more than one profile a finding is reported only if it holds
in every profile that read the file. See the log in `docs/reports.md`.
""",
    default_on=False,
)
def dead_program(ctx: Context) -> Iterator[Diagnostic]:
    sig = ctx.signature
    used: set[str] = set()

    def note(node: Node | None, skip: str = "") -> None:
        if node is None:
            return
        for nd in node.symbols():
            if nd.text != skip:
                used.add(nd.text or "")

    for prog in sig.programs:
        for lhs, rhs in prog.cases:
            note(rhs, prog.name)
            for arg in lhs.children[1:]:
                note(arg)
        for a in prog.sig_args:
            note(a)
        note(prog.sig_ret)
    for rule in sig.rules:
        for pat in list(rule.premises) + list(rule.args):
            note(pat)
        note(rule.conclusion)
        note(rule.assumption)
        for a, b in rule.requires:
            note(a)
            note(b)
    for d in sig.defines:
        note(d.body)
        for p in d.params:
            note(p.type)
    for decl in sig.decls:
        # a program is reached from a declaration too: a type rule that calls
        # one, a nil terminator built by one
        note(decl.type)
        for p in decl.params:
            note(p.type)
        for a in decl.attrs:
            note(a.value)

    for prog in sig.programs:
        if prog.name not in used:
            yield Diagnostic(
                code="EO0060",
                severity=Severity.HINT,
                message=f"nothing reaches `{prog.name}`",
                span=prog.span,
            )


@check(
    "EO0070",
    "a program case that calls itself with the arguments it just matched",
    page="""
A case whose whole right-hand side is the program applied to exactly what its
pattern matched does not compute anything: evaluating it evaluates it again,
with the same arguments, for as long as the checker is willing to keep going.
This is the shape a case takes when an argument was meant to shrink and does
not -- a tail that was written as the list, an index that was meant to be
decremented.
""",
)
def self_recursion(ctx: Context) -> Iterator[Diagnostic]:
    for prog in ctx.signature.programs:
        for lhs, rhs in prog.cases:
            if not (rhs.is_list and rhs.head == prog.name and lhs.is_list):
                continue
            if len(rhs.children) != len(lhs.children):
                continue
            if any(str(a) != str(b) for a, b in zip(rhs.children[1:], lhs.children[1:])):
                continue
            yield Diagnostic(
                code="EO0070",
                severity=Severity.ERROR,
                message=f"this case of `{prog.name}` returns the same application it "
                f"matched",
                span=rhs.span,
                label="evaluating this evaluates it again",
                notes=["nothing in the arguments changes, so the recursion does not end"],
            )
