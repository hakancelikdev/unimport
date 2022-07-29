import sys

import pytest

from unimport.color import RED, RESET, TERMINAL_SUPPORT_COLOR, paint


@pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows")
def test_terminal_support_color_on_win():
    from unimport.color import _enable

    try:
        _enable()
    except OSError:
        assert TERMINAL_SUPPORT_COLOR is False
    else:
        assert TERMINAL_SUPPORT_COLOR is True


@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_terminal_support_color():
    assert TERMINAL_SUPPORT_COLOR is True


def test_red_paint():
    text = "test text"

    action_text = paint(text, RED)
    assert RED + text + RESET == action_text


def test_paint_use_color_false():
    text = "test text"

    action_text = paint(text, RED, False)
    assert text == action_text


def test_use_color_setting_true():
    text = "test text"

    action_text = paint(text, RED, True)
    assert RED + text + RESET == action_text
