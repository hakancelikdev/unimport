import ast
import token
import tokenize
from enum import Enum
from typing import Iterator, List

__all__ = (
    "generate_tokens",
    "set_tokens_parent",
    "set_tokens_child",
    "comment_token",
    "string_token",
    "Position",
    "get_child_tokens",
    "first_child_token_match",
    "pass_token",
    "comments_to_strings",
    "prepare_tokens",
    "string_to_comments",
)


def generate_tokens(source: str) -> Iterator[tokenize.TokenInfo]:
    return tokenize.generate_tokens(readline=iter(ast._splitlines_no_ff(source)).__next__)  # type: ignore # noqa


def set_tokens_parent(tokens: List[tokenize.TokenInfo]) -> None:
    parent = None
    for tok in tokens:
        setattr(tok, "parent", parent)
        parent = tok


def set_tokens_child(tokens: List[tokenize.TokenInfo]) -> None:
    for index, tok in enumerate(tokens):
        try:
            setattr(tok, "child", tokens[index + 1])
        except IndexError:
            setattr(tok, "child", None)


def get_child_tokens(t: tokenize.TokenInfo) -> Iterator[tokenize.TokenInfo]:
    child = t
    while child:
        child = child.child  # type: ignore
        if child:
            yield child


def first_child_token_match(t: tokenize.TokenInfo):  # TODO: rename, nereye pass eklemeliyim ?
    x_offset = t.start[1]

    for child in get_child_tokens(t):
        if all(
            (
                child.start[1] == x_offset,
                child.type
                not in [
                    token.NL,
                    token.NEWLINE,
                    token.ENDMARKER,
                    token.INDENT,
                    token.DEDENT,
                    # token.TYPE_COMMENT,
                    # token.COMMENT
                ],
                not child.string.startswith('"#'),
            )
        ):
            return child
        if child.start[1] < x_offset:
            break

    return None


def comment_token(tok: tokenize.TokenInfo) -> tokenize.TokenInfo:
    assert tok.type == token.STRING

    line = " ".join(tok.line.split()) + "\n" if tok.line[-1] == "\n" else " ".join(tok.line.split())

    return tok._replace(
        type=token.COMMENT,
        string=tok.string.replace('"', ""),
        start=(tok.start[0], tok.start[1]),
        end=(tok.end[0], tok.end[1] - 2),
        line=line.replace('"', ""),
    )


def string_token(tok: tokenize.TokenInfo) -> tokenize.TokenInfo:
    assert tok.type == token.COMMENT

    line = f'{" ".join(tok.line.split())}\n' if tok.line[-1] == "\n" else f'{" ".join(tok.line.split())}'

    return tok._replace(type=token.STRING, string=f'"{tok.string}"', end=(tok.end[0], tok.end[1]), line=line)


def pass_token(tok: tokenize.TokenInfo) -> tokenize.TokenInfo:
    return tok._replace(
        type=token.NAME,
        string="pass",
        # start=(tok.start[0] - 1 , tok.start[1]),
        # end=(tok.end[0] , tok.end[1]),
        # line=f'{tok.start[1] * " "}pass\n',
    )


class Position(int, Enum):
    LINE = 0
    COLUMN = 1


def increase(t: tokenize.TokenInfo, amount: int = 1, page: Position = Position.LINE) -> tokenize.TokenInfo:
    if amount == 0:
        return t

    start, end = list(t.start), list(t.end)

    start[page] += amount
    end[page] += amount

    return t._replace(start=tuple(start), end=tuple(end))


def prepare_tokens(source: str) -> List[tokenize.TokenInfo]:
    tokens = list(generate_tokens(source))
    set_tokens_parent(tokens)
    set_tokens_child(tokens)

    return tokens


def comments_to_strings(tokens: Iterator[tokenize.TokenInfo]) -> Iterator[tokenize.TokenInfo]:
    return (
        string_token(tok)
        if (
            tok.type == tokenize.COMMENT
            and tok.parent  # type: ignore
            and (tok.parent.type == token.NL or tok.parent.type == token.NEWLINE)  # type: ignore
        )
        else tok
        for tok in tokens
    )


def string_to_comments(tokens: Iterator[tokenize.TokenInfo]) -> Iterator[tokenize.TokenInfo]:
    amount = 0
    for t in tokens:
        if t.type == tokenize.STRING and t.parent and t.string.startswith('"#'):  # type: ignore
            if not first_child_token_match(t):
                amount += 1
                yield increase(pass_token(t), amount)
            else:
                yield increase(comment_token(t), amount)
        else:
            yield increase(t, amount)
