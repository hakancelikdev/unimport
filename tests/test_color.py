import sys
import unittest

import pytest

from unimport.color import RED, RESET, TERMINAL_SUPPORT_COLOR, paint, use_color


class ColorTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.text = "test text"

    @unittest.skipUnless(sys.platform == "win32", "requires Windows32")
    def test_terminal_support_color_on_win(self):
        from unimport.color import _enable

        try:
            _enable()
        except OSError:
            self.assertFalse(TERMINAL_SUPPORT_COLOR)
        else:
            self.assertTrue(TERMINAL_SUPPORT_COLOR)

    @unittest.skipUnless(sys.platform != "win32", "requires Windows32")
    def test_terminal_support_color(self):
        self.assertTrue(TERMINAL_SUPPORT_COLOR)

    def test_red_paint(self):
        action_text = paint(self.text, RED)
        expected_text = RED + self.text + RESET
        self.assertEqual(expected_text, action_text)

    def test_use_color_setting_false(self):
        action_text = paint(self.text, RED, False)
        expected_text = self.text
        self.assertEqual(expected_text, action_text)

    def test_use_color_setting_true(self):
        action_text = paint(self.text, RED, True)
        expected_text = RED + self.text + RESET
        self.assertEqual(expected_text, action_text)


@pytest.mark.parametrize(
    "option,expected_result",
    [
        ("auto", TERMINAL_SUPPORT_COLOR and sys.stderr.isatty()),
        ("always", True),
        ("never", False),
    ],
)
def test_use_color(option, expected_result):
    assert expected_result == use_color(option)


def test_use_color_none_of_them():
    with pytest.raises(ValueError) as cm:
        use_color("none-of-them")

    assert "none-of-them" in str(cm.value)
