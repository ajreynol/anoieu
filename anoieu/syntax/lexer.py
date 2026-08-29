"""The lexer for Eunoia signatures (*.eo) and configuration sets (*.eos).

Both languages are s-expressions over the same tokens, so one lexer serves.
A token runs up to whitespace, a bracket, a quote, a bar or a semicolon; a token
beginning with `:` is a keyword; `"..."` is a string, in which `""` stands for a
quote; `|...|` is a quoted symbol; `; ...` is a comment, which is kept rather
than dropped, because the documentation convention of a signature lives in
comments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Tok(Enum):
    LPAREN = "("
    RPAREN = ")"
    SYMBOL = "symbol"
    KEYWORD = "keyword"
    STRING = "string"
    EOF = "eof"


@dataclass
class Token:
    kind: Tok
    text: str
    line: int
    col: int
    end_line: int
    end_col: int


@dataclass
class Comment:
    text: str  # without the leading ';'
    line: int
    col: int


@dataclass
class LexError:
    msg: str
    line: int
    col: int


_NUMERAL = re.compile(r"^-?\d+$")
_DECIMAL = re.compile(r"^-?\d+\.\d+$")
_RATIONAL = re.compile(r"^-?\d+/\d+$")
_BINARY = re.compile(r"^#b[01]+$")
_HEX = re.compile(r"^#x[0-9a-fA-F]+$")

_DELIM = set(' \t\r\n()";|')


def literal_category(text: str) -> str | None:
    """The SMT-LIB 3 syntactic category of a token, if it is a literal."""
    if _NUMERAL.match(text):
        return "<numeral>"
    if _DECIMAL.match(text):
        return "<decimal>"
    if _RATIONAL.match(text):
        return "<rational>"
    if _BINARY.match(text):
        return "<binary>"
    if _HEX.match(text):
        return "<hexadecimal>"
    return None


def lex(text: str) -> tuple[list[Token], list[Comment], list[LexError]]:
    tokens: list[Token] = []
    comments: list[Comment] = []
    errors: list[LexError] = []
    line, col, i, n = 1, 1, 0, len(text)

    def advance(upto: int) -> None:
        """Move the cursor to index `upto`, tracking line and column."""
        nonlocal i, line, col
        while i < upto:
            if text[i] == "\n":
                line += 1
                col = 1
            else:
                col += 1
            i += 1

    while i < n:
        c = text[i]
        if c in " \t\r\n":
            advance(i + 1)
            continue
        if c == ";":
            j = text.find("\n", i)
            j = n if j < 0 else j
            comments.append(Comment(text[i + 1 : j], line, col))
            advance(j)
            continue
        start, sline, scol = i, line, col
        if c in "()":
            advance(i + 1)
            kind = Tok.LPAREN if c == "(" else Tok.RPAREN
            tokens.append(Token(kind, c, sline, scol, line, col))
            continue
        if c == '"':
            j = i + 1
            closed = False
            while j < n:
                if text[j] == '"':
                    if j + 1 < n and text[j + 1] == '"':  # "" escapes a quote
                        j += 2
                        continue
                    closed = True
                    j += 1
                    break
                j += 1
            if not closed:
                errors.append(LexError("unterminated string literal", sline, scol))
                advance(n)
                break
            advance(j)
            tokens.append(Token(Tok.STRING, text[start:j], sline, scol, line, col))
            continue
        if c == "|":
            j = text.find("|", i + 1)
            if j < 0:
                errors.append(LexError("unterminated quoted symbol", sline, scol))
                advance(n)
                break
            advance(j + 1)
            tokens.append(Token(Tok.SYMBOL, text[start : j + 1], sline, scol, line, col))
            continue
        j = i
        while j < n and text[j] not in _DELIM:
            j += 1
        if j == i:
            errors.append(LexError(f"unexpected character {c!r}", sline, scol))
            advance(i + 1)
            continue
        advance(j)
        word = text[start:j]
        kind = Tok.KEYWORD if word.startswith(":") else Tok.SYMBOL
        tokens.append(Token(kind, word, sline, scol, line, col))

    tokens.append(Token(Tok.EOF, "", line, col, line, col))
    return tokens, comments, errors
