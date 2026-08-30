"""Checks over the triple: a signature, its calculus semantics, and the SMT one.

These are the questions no single file can answer, and the ones the compiler
either answers late -- at stage six, in a language the author was not writing in
-- or does not answer at all. Each runs only when the run was given the leg it
needs, and says nothing otherwise.

Written to survive the `.eos` language moving: nothing here enumerates the forms
of a set. What it uses is which names a set defines, which names it mentions, and
what its entries say about themselves by attribute -- all of which a new form
inherits for free. See `anoieu/semantics.py`.
"""

from __future__ import annotations

import os
from typing import Iterator

from ..desugar import is_ground
from ..diagnostics import Diagnostic, Severity, Span
from ..model import NIL_ATTRS, Decl
from ..semantics import SemSet
from . import Context, check

# Names the model-smt stage exempts from needing a meaning: a signature's own
# helpers, and what the desugar stage introduces.
INTERNAL_PREFIXES = ("$", "@@")

# Declaration kinds an input's semantics is expected to speak about. A datatype
# and what it declares is the embedding's business, not a theory's.
MEANINGFUL_KINDS = {"const", "parameterized-const", "sort"}


def _semantic_names(sem: SemSet) -> set[str]:
    """Every name a set speaks about: an entry's own, and any it is written
    under after the desugar stage renames an overload."""
    out = set()
    for e in sem.entries:
        out.add(e.name)
        if e.overload:
            out.add(e.overload)
    return out


def _interesting(decl: Decl) -> bool:
    return decl.kind in MEANINGFUL_KINDS and not decl.name.startswith(INTERNAL_PREFIXES)


def _sem_span(sem: SemSet, span: Span | None = None) -> Span:
    return span or Span(sem.path, 1, 1)


@check(
    "TRI0001",
    "a declared symbol the calculus semantics says nothing about",
    page="""
Every symbol a signature declares needs a meaning, or the model-smt stage stops
with `no model semantics found for <name>` — by design, since a symbol with no
meaning is a symbol a model would silently say nothing about. That check runs at
stage six of the compiler, after the semantics have been compiled, the signature
desugared and trimmed. This one runs before any of it, from the two files.

Names beginning `$` or `@@` are exempt, being a signature's own helpers and what
the desugar stage introduces, and so is anything the semantics excludes.
""",
)
def missing_semantics(ctx: Context) -> Iterator[Diagnostic]:
    sem = ctx.semantics
    if sem is None:
        return
    known = _semantic_names(sem)
    seen: set[str] = set()
    for decl in ctx.signature.decls:
        if not _interesting(decl) or decl.name in known or decl.name in seen:
            continue
        seen.add(decl.name)
        yield Diagnostic(
            code="TRI0001",
            severity=Severity.ERROR,
            message=f"`{decl.name}` is declared and the semantics says nothing about it",
            span=decl.span,
            label="no meaning",
            notes=[
                f"{os.path.basename(sem.path)} has no entry for it",
                "the model-smt stage stops here with `no model semantics found`",
            ],
            help="give it an entry, or say `:exclude` if the compilation has no place "
            "for it",
        )


@check(
    "TRI0002",
    "a semantics entry for a symbol nothing declares",
    page="""
The other direction, which nothing reports today: an entry whose symbol the
signature does not declare is configuration that no compilation reaches. It is
either a symbol that was renamed or removed on the signature side, or a
misspelling that has been quietly doing nothing.
""",
)
def orphan_semantics(ctx: Context) -> Iterator[Diagnostic]:
    sem = ctx.semantics
    if sem is None:
        return
    from ..resolve import BUILTINS

    sig = ctx.signature
    declared = (
        set(sig.by_name)
        | set(sig.defines_by_name)
        | set(sig.programs_by_name)
        | set(sig.rules_by_name)
        | set(BUILTINS)
    )
    for e in sem.entries:
        if e.name in declared or e.name.startswith(INTERNAL_PREFIXES):
            continue
        yield Diagnostic(
            code="TRI0002",
            severity=Severity.WARNING,
            message=f"the semantics has an entry for `{e.name}`, which the signature "
            f"does not declare",
            span=e.span,
            label="nothing reaches this",
        )


@check(
    "TRI0003",
    "the `:is-list-nil` obligations do not match the signature",
    page="""
The compiler's own worst seam, and the check its documentation asks for by name
(`ethos/docs/README.md`, direction #2).

An n-ary operator whose nil terminator depends on the type — `str.++`, whose nil
is `""` at strings and `(seq.empty T)` at sequences — gets a *forward
declaration* from the desugar stage and no body, because that stage declines to
call `eo::typeof`. The body is supplied by hand, as an `:is-list-nil` attribute
in the semantics. The desugar stage decides whether to declare one by looking at
the signature; a human decides whether to define one by typing an attribute; and
nothing compares the two decisions.

Forgetting one leaves an undefined program reaching the backends: under SMT-LIB
a free uninterpreted function the solver may read as it likes, under Lean a name
that was never written. Writing one for an operator whose nil is ground is a
definition nothing uses.

Both directions are decidable from the signature alone, because whether a nil is
ground is syntactic — so this needs no stage to run.
""",
)
def is_list_nil_diff(ctx: Context) -> Iterator[Diagnostic]:
    sem = ctx.semantics
    if sem is None:
        return
    by_name = sem.by_name
    for decl in ctx.signature.decls:
        attr = next((a for a in decl.attrs if a.key in NIL_ATTRS), None)
        if attr is None or attr.value is None:
            continue
        entry = by_name.get(decl.name)
        has_case = entry is not None and entry.has(":is-list-nil")
        needs = not is_ground(attr.value, decl)
        if needs and not has_case:
            yield Diagnostic(
                code="TRI0003",
                severity=Severity.ERROR,
                message=f"`{decl.name}` needs an `:is-list-nil` case and the semantics "
                f"has none",
                span=decl.span,
                label=f"its nil {attr.value} depends on the type",
                notes=[
                    "the desugar stage forward-declares the predicate and supplies no "
                    "body, so the semantics has to",
                    "without one the backends get an undefined program: a free "
                    "uninterpreted function under SMT-LIB, a missing name under Lean",
                ],
            )
        elif has_case and not needs and entry is not None:
            case = entry.attr(":is-list-nil")
            yield Diagnostic(
                code="TRI0003",
                severity=Severity.WARNING,
                message=f"`{decl.name}` has an `:is-list-nil` case and does not need one",
                span=case.span if case else entry.span,
                label="its nil is ground",
                notes=[
                    f"the nil {attr.value} is one term, so the desugar stage emits the "
                    "predicate itself and this definition is unused"
                ],
            )


@check(
    "TRI0004",
    "an exclusion that names nothing, or that is not closed",
    page="""
`:exclude` says the compilation has no place for what it is written on, and the
names are matched literally: the compiler "neither checks that a name exists nor
computes a dependency closure", so a misspelled exclusion excludes nothing,
silently, and an exclusion that leaves its dependents behind leaves a later stage
naming something that was dropped. `ethos/docs/README.md` direction #5 asks for
both halves of this.
""",
)
def exclusion_hygiene(ctx: Context) -> Iterator[Diagnostic]:
    sem = ctx.semantics
    if sem is None:
        return
    sig = ctx.signature
    declared = set(sig.by_name) | set(sig.programs_by_name) | set(sig.rules_by_name)
    declared |= set(sig.defines_by_name)
    excluded = {e.name for e in sem.entries if e.has(":exclude")}

    for e in sem.entries:
        if not e.has(":exclude") or e.name in declared:
            continue
        yield Diagnostic(
            code="TRI0004",
            severity=Severity.ERROR,
            message=f"`{e.name}` is excluded and the signature declares no such name",
            span=e.span,
            label="this exclusion excludes nothing",
            notes=["exclusions are matched literally, so a misspelling is silent"],
        )

    if not excluded:
        return
    for rule in sig.rules:
        if rule.name in excluded:
            continue
        nodes = [rule.conclusion, rule.assumption, *rule.premises, *rule.args]
        nodes += [n for pair in rule.requires for n in pair]
        used = {s.text or "" for n in nodes if n is not None for s in n.symbols()}
        hit = sorted(used & excluded)
        if not hit:
            continue
        yield Diagnostic(
            code="TRI0004",
            severity=Severity.ERROR,
            message=f"rule `{rule.name}` names {', '.join(hit)}, which the semantics "
            f"excludes, and is not excluded itself",
            span=rule.span,
            label="the exclusion is not closed",
            notes=[
                "the compiler computes no dependency closure, so every declaration "
                "that goes with an excluded one has to say so for itself"
            ],
        )


@check(
    "TRI0005",
    "a transformation whose target the SMT semantics does not define",
    page="""
An entry of a calculus's semantics says what a symbol *becomes*: a term over the
SMT-LIB signature. A bare name at term level is a symbol of that signature, so
the target set has to define it. One it does not define is a name the model-smt
stage will not find, reported here against the two configuration files rather
than against the generated one.

Only the heads of applications are checked, and only where the name is not a
macro of the set, a program it writes, something the case's own pattern bound, a
quoted native, or a `$`-name of the embedding — which is the vocabulary the
compiler itself resolves.

The check needs `--embedding`, the `.eo` file that declares what the deep
embedding *is* (`plugins/model_smt/model_smt.eo`): its constructors and types are
named by no configuration set, so without them every term of the embedding would
read as a missing target. Given no embedding, this check says nothing.
""",
)
def transform_target(ctx: Context) -> Iterator[Diagnostic]:
    sem, target = ctx.semantics, ctx.smt_semantics
    if sem is None or target is None or not ctx.embedding_names:
        # without the embedding's own vocabulary -- the constructors and types
        # `model_smt.eo` declares, which no configuration set mentions -- every
        # term of the embedding would read as a missing target. Pass `--embedding`.
        return
    known = (
        target.defines()
        | set(target.macros)
        | _semantic_names(target)
        | ctx.embedding_names
    )
    seen: set[str] = set()

    def walk(nd, bound: set[str]) -> Iterator[tuple[str, object]]:
        """Heads of applications, with what an `eo::define` binds put in scope."""
        if not nd.is_list or not nd.children:
            return
        head = nd.head or ""
        if head == "eo::define" and len(nd.children) == 3:
            inner = set(bound)
            for pair in nd.children[1].children if nd.children[1].is_list else []:
                if pair.is_list and len(pair.children) == 2 and pair.children[0].is_atom:
                    inner.add(pair.children[0].text or "")
                    yield from walk(pair.children[1], bound)
            yield from walk(nd.children[2], inner)
            return
        op = nd.children[0]
        if head and not op.is_string:
            yield head, nd
        for child in nd.children[1:]:
            yield from walk(child, bound)

    for e in sem.entries:
        local = sem.defines() | {p.name for p in e.params} | {"none", "true", "false"}
        for a in e.attrs:
            if a.key not in (":term", ":type"):
                continue
            # an attribute given two values matches with the first and returns
            # the second, so the first binds names the second may use
            bound = set(local)
            if len(a.values) > 1:
                bound |= {s.text or "" for s in a.values[0].symbols()}
            for value in a.values[-1:]:
                for head, nd in walk(value, bound):
                    if (
                        head in bound
                        or head in known
                        or head.startswith(("$", "eo.", "smt.", "eo::"))
                        or head in seen
                    ):
                        continue
                    seen.add(head)
                    yield Diagnostic(
                        code="TRI0005",
                        severity=Severity.ERROR,
                        message=f"`{e.name}` transforms into `{head}`, which the SMT "
                        f"semantics does not define",
                        span=nd.span,
                        label="no such symbol in the target",
                        notes=[f"the target is {os.path.basename(target.path)}"],
                    )
