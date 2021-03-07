import sys
import unittest

from unimport.color import RED, RESET, TERMINAL_SUPPORT_COLOR, paint


class ColorTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.content = "test content"

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

    @unittest.skipUnless(sys.platform == "win32", "requires Windows32")
    def test_red_paint_on_win(self):
        action_content = paint(self.content, RED)
        if TERMINAL_SUPPORT_COLOR:
            expected_content = RED + self.content + RESET
        else:
            expected_content = self.content
        self.assertEqual(expected_content, action_content)

    @unittest.skipUnless(sys.platform != "win32", "requires Windows32")
    def test_red_paint(self):
        action_content = paint(self.content, RED)
        expected_content = RED + self.content + RESET
        self.assertEqual(expected_content, action_content)
