"""Reading a signature: commands to model, following the include graph.

Structural findings that fall out of reading a command -- a field written out
of order, an attribute that is not in the language, an include that does not
resolve -- are reported here, since this is the pass that knows what was
written where.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .diagnostics import Diagnostic, Severity, SourceMap, Span
from .docstrings import parse_docstring
from .model import (
    KNOWN_ATTRS,
    LITERAL_CATEGORIES,
    Attribute,
    Decl,
    DefineDecl,
    LiteralDecl,
    Param,
    ProgramDecl,
    RuleDecl,
    Signature,
)
from .syntax.parser import Node, ParsedFile, parse

# The fields of declare-rule, in the order the parser expects them.
RULE_FIELDS = [
    ":assumption",
    ":premises",
    ":premise-list",
    ":args",
    ":requires",
    ":conclusion",
    ":conclusion-explicit",
]
RULE_FIELD_RANK = {
    ":assumption": 0,
    ":premises": 1,
    ":premise-list": 1,
    ":args": 2,
    ":requires": 3,
    ":conclusion": 4,
    ":conclusion-explicit": 4,
}

# The SMT-LIB commands a *reference* file may hold. A signature file may not:
# ethos answers `Expected Eunoia command, got declare-fun`.
SMTLIB_COMMANDS = {
    "assert",
    "check-sat",
    "check-sat-assuming",
    "declare-fun",
    "define-const",
    "define-fun",
    "define-fun-rec",
    "define-funs-rec",
    "define-sort",
    "reset-assertions",
    "set-info",
    "set-logic",
    "push",
    "pop",
}

COMMANDS = {
    "declare-const",
    "declare-parameterized-const",
    "declare-consts",
    "declare-datatype",
    "declare-datatypes",
    "declare-sort",
    "declare-rule",
    "define",
    "program",
    "include",
    "reference",
    "assume",
    "assume-push",
    "step",
    "step-pop",
    "echo",
    "exit",
    "reset",
    "set-option",
}


@dataclass
class LoadResult:
    signature: Signature
    files: dict[str, ParsedFile] = field(default_factory=dict)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    sources: SourceMap = field(default_factory=SourceMap)
    include_edges: list[tuple[str, str]] = field(default_factory=list)


def _attrs_from(nodes: list[Node], out: list[Diagnostic], where: str) -> list[Attribute]:
    """Read a trailing `:key [value]` sequence, as ethos does."""
    attrs: list[Attribute] = []
    i = 0
    while i < len(nodes):
        nd = nodes[i]
        if not nd.is_keyword:
            i += 1
            continue
        value = None
        if i + 1 < len(nodes) and not nodes[i + 1].is_keyword:
            value = nodes[i + 1]
            i += 1
        attrs.append(Attribute(nd.text or "", value, nd.span))
        if (nd.text or "") not in KNOWN_ATTRS:
            out.append(
                Diagnostic(
                    code="EO0020",
                    severity=Severity.ERROR,
                    message=f"`{nd.text}` is not an attribute of the language",
                    span=nd.span,
                    label="ignored",
                    notes=[
                        "ethos prints `Unsupported attribute` and carries on, so the "
                        "declaration keeps its meaning minus this annotation",
                        f"seen on {where}",
                    ],
                    help="check the spelling against the attribute list in the user manual",
                )
            )
        i += 1
    return attrs


def _params_from(node: Node | None, out: list[Diagnostic]) -> list[Param]:
    """Read a `((x T :attr) ...)` typed parameter list."""
    params: list[Param] = []
    if node is None or not node.is_list:
        return params
    for item in node.children:
        if not item.is_list or not item.children:
            out.append(
                Diagnostic(
                    code="EO0022",
                    severity=Severity.ERROR,
                    message="a typed parameter is written `(<symbol> <type> <attr>*)`",
                    span=item.span,
                )
            )
            continue
        name = item.children[0].text or "?"
        ptype = item.children[1] if len(item.children) > 1 else None
        attrs = _attrs_from(item.children[2:], out, "a parameter")
        params.append(Param(name, ptype, attrs, item.span))
    return params


def _pairs_from(node: Node | None) -> list[tuple[Node, Node]]:
    pairs: list[tuple[Node, Node]] = []
    if node is None or not node.is_list:
        return pairs
    for item in node.children:
        if item.is_list and len(item.children) == 2:
            pairs.append((item.children[0], item.children[1]))
    return pairs


def _load_rule(form: Node, out: list[Diagnostic]) -> RuleDecl | None:
    name_node = form.at(1)
    if name_node is None or not name_node.is_atom:
        return None
    params = _params_from(form.at(2), out)
    rest = form.children[3:]
    assumption = None
    premises: list[Node] = []
    premise_list = None
    args: list[Node] = []
    requires: list[tuple[Node, Node]] = []
    conclusion = None
    conc_explicit = False
    attrs: list[Node] = []
    order: list[tuple[str, Span]] = []

    i = 0
    while i < len(rest):
        nd = rest[i]
        key = nd.text if nd.is_keyword else None
        if key is None:
            i += 1
            continue
        if key in RULE_FIELDS:
            order.append((key, nd.span))
        if key == ":assumption":
            assumption = rest[i + 1] if i + 1 < len(rest) else None
            i += 2
        elif key == ":premises":
            nxt = rest[i + 1] if i + 1 < len(rest) else None
            premises = list(nxt.children) if nxt is not None and nxt.is_list else []
            i += 2
        elif key == ":premise-list":
            pat = rest[i + 1] if i + 1 < len(rest) else None
            cons = rest[i + 2] if i + 2 < len(rest) else None
            if pat is not None and cons is not None:
                premise_list = (pat, cons)
                premises = [pat]
            i += 3
        elif key == ":args":
            nxt = rest[i + 1] if i + 1 < len(rest) else None
            args = list(nxt.children) if nxt is not None and nxt.is_list else []
            i += 2
        elif key == ":requires":
            requires = _pairs_from(rest[i + 1] if i + 1 < len(rest) else None)
            i += 2
        elif key in (":conclusion", ":conclusion-explicit"):
            conclusion = rest[i + 1] if i + 1 < len(rest) else None
            conc_explicit = key == ":conclusion-explicit"
            i += 2
        else:
            attrs.append(nd)
            if i + 1 < len(rest) and not rest[i + 1].is_keyword:
                attrs.append(rest[i + 1])
                i += 1
            i += 1

    # the parser reads these fields positionally, so an out-of-order field is
    # reported as a missing conclusion, several lines away.
    ranks = [(k, s) for k, s in order]
    for (k1, _), (k2, s2) in zip(ranks, ranks[1:]):
        if RULE_FIELD_RANK[k2] < RULE_FIELD_RANK[k1]:
            out.append(
                Diagnostic(
                    code="EO0021",
                    severity=Severity.ERROR,
                    message=f"`{k2}` is written after `{k1}`",
                    span=s2,
                    label="out of order",
                    notes=[
                        "declare-rule reads its fields positionally, in the order "
                        ":assumption, :premises | :premise-list, :args, :requires, "
                        ":conclusion | :conclusion-explicit",
                        "ethos reports this as `Expected conclusion in declare-rule`, "
                        "at the end of the command rather than here",
                    ],
                )
            )
            break

    if conclusion is None:
        out.append(
            Diagnostic(
                code="EO0023",
                severity=Severity.ERROR,
                message=f"rule `{name_node.text}` has no conclusion",
                span=form.span,
                help="every rule ends with :conclusion or :conclusion-explicit",
            )
        )

    return RuleDecl(
        name=name_node.text or "?",
        params=params,
        assumption=assumption,
        premises=premises,
        premise_list=premise_list,
        args=args,
        requires=requires,
        conclusion=conclusion,
        conclusion_explicit=conc_explicit,
        attrs=_attrs_from(attrs, out, f"rule `{name_node.text}`"),
        field_order=order,
        span=form.span,
        form=form,
    )


def _load_program(form: Node, out: list[Diagnostic]) -> ProgramDecl | None:
    name_node = form.at(1)
    if name_node is None or not name_node.is_atom:
        return None
    params = _params_from(form.at(2), out)
    rest = form.children[3:]
    sig_args: list[Node] = []
    sig_ret = None
    cases: list[tuple[Node, Node]] = []
    i = 0
    while i < len(rest):
        nd = rest[i]
        if nd.is_keyword and nd.text == ":signature":
            arglist = rest[i + 1] if i + 1 < len(rest) else None
            sig_args = list(arglist.children) if arglist is not None and arglist.is_list else []
            sig_ret = rest[i + 2] if i + 2 < len(rest) else None
            i += 3
            continue
        if nd.is_list:
            for case in nd.children:
                if case.is_list and len(case.children) == 2:
                    cases.append((case.children[0], case.children[1]))
                else:
                    out.append(
                        Diagnostic(
                            code="EO0024",
                            severity=Severity.ERROR,
                            message="a program case is a pair `(<pattern> <term>)`",
                            span=case.span,
                        )
                    )
        i += 1
    return ProgramDecl(
        name=name_node.text or "?",
        params=params,
        sig_args=sig_args,
        sig_ret=sig_ret,
        cases=cases,
        span=form.span,
        form=form,
    )


def _datatype_decls(name: str, dt: Node, out: list[Diagnostic], sig: Signature) -> None:
    """Record the constructors and selectors a datatype declaration introduces."""
    body = dt
    if body.is_list and body.children and (body.children[0].text == "par"):
        body = body.children[2] if len(body.children) > 2 else body
    for cons in body.children if body.is_list else []:
        if not cons.is_list or not cons.children:
            continue
        cname = cons.children[0].text or "?"
        sig.add_decl(Decl(cname, "constructor", None, [], [], cons.children[0].span, cons))
        for sel in cons.children[1:]:
            if sel.is_list and sel.children:
                sig.add_decl(
                    Decl(
                        sel.children[0].text or "?",
                        "selector",
                        sel.children[1] if len(sel.children) > 1 else None,
                        [],
                        [],
                        sel.children[0].span,
                        sel,
                    )
                )


def load(path: str, include_dirs: list[str] | None = None) -> LoadResult:
    root = os.path.dirname(os.path.abspath(path))
    sig = Signature(root=os.path.abspath(path))
    res = LoadResult(signature=sig)
    seen: set[str] = set()

    def read(fpath: str, origin: Span | None, role: str = "signature") -> None:
        real = os.path.realpath(fpath)
        if real in seen:
            return
        if not os.path.isfile(real):
            if origin is not None:
                res.diagnostics.append(
                    Diagnostic(
                        code="EO0010",
                        severity=Severity.ERROR,
                        message=f"cannot find included file `{os.path.basename(fpath)}`",
                        span=origin,
                        notes=[f"looked for {fpath}"],
                        help="an include path is resolved against the directory of the "
                        "file that includes it",
                    )
                )
            return
        seen.add(real)
        text = open(real, encoding="utf-8", errors="replace").read()
        parsed = parse(real, text)
        res.files[real] = parsed
        res.sources.add(real, text)
        sig.files.append(real)
        res.diagnostics.extend(parsed.diagnostics)
        walk(parsed, role)

    def walk(parsed: ParsedFile, role: str = "signature") -> None:
        out = res.diagnostics
        for form in parsed.forms:
            if not form.is_list or not form.children:
                continue
            head = form.head
            doc = parse_docstring(parsed.docblocks.get(form.line, []), form.path)
            if head == "include" or head == "reference":
                target = form.at(1)
                if target is None:
                    continue
                rel = target.string_value()
                base = os.path.dirname(parsed.path)
                res.include_edges.append((parsed.path, os.path.join(base, rel)))
                read(
                    os.path.join(base, rel),
                    target.span,
                    "reference" if head == "reference" else role,
                )
            elif head == "declare-const":
                name = form.at(1)
                if name is None:
                    continue
                attrs = _attrs_from(form.children[3:], out, f"`{name.text}`")
                sig.add_decl(
                    Decl(name.text or "?", "const", form.at(2), [], attrs, name.span, form)
                )
            elif head == "declare-parameterized-const":
                name = form.at(1)
                if name is None:
                    continue
                params = _params_from(form.at(2), out)
                attrs = _attrs_from(form.children[4:], out, f"`{name.text}`")
                sig.add_decl(
                    Decl(
                        name.text or "?",
                        "parameterized-const",
                        form.at(3),
                        params,
                        attrs,
                        name.span,
                        form,
                    )
                )
            elif head == "declare-sort":
                name = form.at(1)
                if name is not None:
                    sig.add_decl(Decl(name.text or "?", "sort", None, [], [], name.span, form))
            elif head == "declare-consts":
                cat = form.at(1)
                if cat is None:
                    continue
                category = cat.text or "?"
                if category not in LITERAL_CATEGORIES:
                    out.append(
                        Diagnostic(
                            code="EO0025",
                            severity=Severity.ERROR,
                            message=f"`{category}` is not a literal category",
                            span=cat.span,
                            notes=["the categories are " + ", ".join(sorted(LITERAL_CATEGORIES))],
                        )
                    )
                lit = LiteralDecl(category, form.at(2), cat.span)
                sig.literals.append(lit)
                if lit.type is not None:
                    sig.literal_type.setdefault(category, lit.type)
            elif head == "declare-datatype":
                name = form.at(1)
                if name is None:
                    continue
                sig.add_decl(Decl(name.text or "?", "datatype", None, [], [], name.span, form))
                dt = form.at(2)
                if dt is not None:
                    _datatype_decls(name.text or "?", dt, out, sig)
            elif head == "declare-datatypes":
                sorts, bodies = form.at(1), form.at(2)
                names = []
                for sd in sorts.children if sorts and sorts.is_list else []:
                    if sd.is_list and sd.children:
                        names.append(sd.children[0])
                        sig.add_decl(
                            Decl(
                                sd.children[0].text or "?",
                                "datatype",
                                None,
                                [],
                                [],
                                sd.children[0].span,
                                form,
                            )
                        )
                for idx, dt in enumerate(bodies.children if bodies and bodies.is_list else []):
                    nm = names[idx].text if idx < len(names) else "?"
                    _datatype_decls(nm or "?", dt, out, sig)
            elif head == "define":
                name = form.at(1)
                if name is None:
                    continue
                params = _params_from(form.at(2), out)
                body = form.at(3)
                attrs = _attrs_from(form.children[4:], out, f"`{name.text}`")
                d = DefineDecl(name.text or "?", params, body, attrs, name.span, form)
                sig.defines.append(d)
                sig.defines_by_name[d.name] = d
            elif head == "program":
                prog = _load_program(form, out)
                if prog is not None:
                    prog.doc = doc
                    sig.programs.append(prog)
                    sig.programs_by_name[prog.name] = prog
            elif head == "declare-rule":
                rule = _load_rule(form, out)
                if rule is not None:
                    rule.doc = doc
                    sig.rules.append(rule)
                    sig.rules_by_name[rule.name] = rule
            elif role == "reference" and (head in SMTLIB_COMMANDS or head.startswith("get-")):
                # every `get-` command only produces solver output, so ethos
                # parses and ignores it rather than keeping a list of them
                if head == "declare-fun":
                    name = form.at(1)
                    if name is not None:
                        sig.add_decl(
                            Decl(name.text or "?", "const", form.at(3), [], [], name.span, form)
                        )
            elif head in SMTLIB_COMMANDS:
                out.append(
                    Diagnostic(
                        code="EO0026",
                        severity=Severity.ERROR,
                        message=f"`{head}` is an SMT-LIB command, and this file is read "
                        f"as a signature",
                        span=(form.at(0) or form).span,
                        notes=[
                            "ethos answers `Expected Eunoia command`; SMT-LIB commands are "
                            "read only in a file named by `reference`"
                        ],
                        help="a signature declares with declare-const or "
                        "declare-parameterized-const",
                    )
                )
            elif head not in COMMANDS:
                out.append(
                    Diagnostic(
                        code="EO0026",
                        severity=Severity.ERROR,
                        message=f"`{head}` is not a command of the language",
                        span=(form.at(0) or form).span,
                        help="see the full command syntax in the user manual",
                    )
                )

    read(os.path.abspath(path), None)
    for d in include_dirs or []:
        read(os.path.abspath(d), None)
    return res
