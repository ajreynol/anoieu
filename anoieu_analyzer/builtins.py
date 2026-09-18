"""The builtin operators, as the user manual defines them.

Arity and the categories an operator evaluates on are written down in the manual
and nowhere a tool can read, so they are written here: an application that gets
either wrong is a term that never evaluates, and inside a program body or a rule
nothing asks.

`(min, max)` bounds an operator's arity; `None` for the maximum is variadic. An
operator absent from the table is one this file does not claim to know.
"""

from __future__ import annotations

# name -> (min arity, max arity or None)
EO_ARITY: dict[str, tuple[int, int | None]] = {
    # core
    "eo::is_ok": (1, 1),
    "eo::ite": (3, 3),
    "eo::eq": (2, 2),
    "eo::is_eq": (2, 2),
    "eo::requires": (3, 3),
    "eo::hash": (1, 1),
    "eo::typeof": (1, 1),
    "eo::nameof": (1, 1),
    "eo::cmp": (2, 2),
    "eo::is_z": (1, 1),
    "eo::is_q": (1, 1),
    "eo::is_bin": (1, 1),
    "eo::is_str": (1, 1),
    "eo::is_bool": (1, 1),
    "eo::is_var": (1, 1),
    "eo::var": (2, 2),
    "eo::define": (2, 2),
    "eo::as": (2, 2),
    # boolean and bitwise
    "eo::and": (2, None),
    "eo::or": (2, None),
    "eo::xor": (2, None),
    "eo::not": (1, 1),
    # arithmetic
    "eo::add": (2, None),
    "eo::mul": (2, None),
    "eo::pow": (2, 2),
    "eo::log": (2, 2),
    "eo::neg": (1, 1),
    "eo::qdiv": (2, 2),
    "eo::zdiv": (2, 2),
    "eo::zmod": (2, 2),
    "eo::is_neg": (1, 1),
    "eo::gt": (2, 2),
    # strings and bit-vectors
    "eo::len": (1, 1),
    "eo::concat": (2, None),
    "eo::extract": (3, 3),
    "eo::find": (2, 2),
    # conversions
    "eo::to_z": (1, 1),
    "eo::to_q": (1, 1),
    "eo::to_bin": (2, 2),
    "eo::to_str": (1, 1),
    # datatypes
    "eo::dt_constructors": (1, 1),
    "eo::dt_selectors": (1, 1),
    # lists: each takes the operator first
    "eo::nil": (1, 2),
    "eo::cons": (3, 3),
    "eo::list_len": (2, 2),
    "eo::list_concat": (3, 3),
    "eo::list_nth": (3, 3),
    "eo::list_find": (3, 3),
    "eo::list_rev": (2, 2),
    "eo::list_erase": (3, 3),
    "eo::list_erase_all": (3, 3),
    "eo::list_setof": (2, 2),
    "eo::list_minclude": (3, 3),
    "eo::list_meq": (3, 3),
    "eo::list_diff": (3, 3),
    "eo::list_inter": (3, 3),
    "eo::list_singleton_elim": (2, 2),
    "eo::list_singleton_intro": (2, 2),
    "eo::list_repeat": (3, 3),
}

# Operators that evaluate only where both arguments are values of *one*
# category: "no mixed arithmetic", as the manual puts it, so `(eo::add 2 1/3)`
# is a term that stays as it is.
SAME_CATEGORY: set[str] = {
    "eo::add",
    "eo::mul",
    "eo::qdiv",
    "eo::zdiv",
    "eo::zmod",
    "eo::gt",
    "eo::concat",
}

ARITHMETIC = {"<numeral>", "<decimal>", "<rational>"}
BITWISE = {"<binary>", "<hexadecimal>"}
