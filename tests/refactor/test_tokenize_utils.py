from tokenize import TokenInfo
import token

import textwrap

from unimport.refactor.tokenize_utils import (
    generate_tokens,
    set_tokens_parent,
    set_tokens_child,
    get_child_tokens,
    first_child_token_match,
)


def test_generate_tokens():
    source = textwrap.dedent(
        """
        def foo():
            pass
        """
    )
    tokens = generate_tokens(source)
    assert next(tokens) == TokenInfo(type=token.NL, string='\n', start=(1, 0), end=(1, 1), line='\n')
    assert next(tokens) == TokenInfo(type=token.NAME, string='def', start=(2, 0), end=(2, 3), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.NAME, string='foo', start=(2, 4), end=(2, 7), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.OP, string='(', start=(2, 7), end=(2, 8), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.OP, string=')', start=(2, 8), end=(2, 9), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.OP, string=':', start=(2, 9), end=(2, 10), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.NEWLINE, string='\n', start=(2, 10), end=(2, 11), line='def foo():\n')
    assert next(tokens) == TokenInfo(type=token.INDENT, string='    ', start=(3, 0), end=(3, 4), line='    pass\n')
    assert next(tokens) == TokenInfo(type=token.NAME, string='pass', start=(3, 4), end=(3, 8), line='    pass\n')
    assert next(tokens) == TokenInfo(type=token.NEWLINE, string='\n', start=(3, 8), end=(3, 9), line='    pass\n')
    assert next(tokens) == TokenInfo(type=token.DEDENT, string='', start=(4, 0), end=(4, 0), line='')
    assert next(tokens) == TokenInfo(type=token.ENDMARKER, string='', start=(4, 0), end=(4, 0), line='')


def test_set_tokens_parent():
    source = textwrap.dedent(
        """
        def foo():
            pass
        """
    )
    tokens = list(generate_tokens(source))
    set_tokens_parent(tokens)

    assert tokens[0].parent is None
    for index in range(1, len(tokens)):
        assert tokens[index].parent == tokens[index - 1]


def test_set_tokens_child():
    source = textwrap.dedent(
        """
        def foo():
            pass
        """
    )
    tokens = list(generate_tokens(source))
    set_tokens_child(tokens)

    assert tokens[-1].child is None
    for index in range(len(tokens) - 1):
        assert tokens[index].child == tokens[index + 1]


def test_get_child_tokens():
    source = textwrap.dedent(
        """
        def foo():
            pass
        """
    )
    tokens = list(generate_tokens(source))
    set_tokens_child(tokens)

    for index in range(len(tokens)):
        assert list(get_child_tokens(tokens[index])) == tokens[index + 1:]


def test_first_child_token_match():
    source = textwrap.dedent(
        """
        # comment 1
        
        def foo():  # comment 2
            # comment 3
            pass  # comment 4
        """
    )
    tokens = list(generate_tokens(source))
    set_tokens_child(tokens)

    assert first_child_token_match(tokens[0]) == TokenInfo(type=token.COMMENT, string='# comment 1', start=(2, 0), end=(2, 11), line='# comment 1\n')
    assert first_child_token_match(tokens[1]) == TokenInfo(type=token.NAME, string='def', start=(4, 0), end=(4, 3), line='def foo():  # comment 2\n')
    assert first_child_token_match(tokens[2]) is None


