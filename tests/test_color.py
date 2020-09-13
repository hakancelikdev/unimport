import textwrap
import unittest

from unimport.color import COLORS, Color # unimport: skip


class TestColor(unittest.TestCase):
    def setUp(self):
        self.test_content = "Test Content"

    for color in COLORS.keys():
        test_template = textwrap.dedent(
            f"""
            def test_{color}(self):
                action_test = COLORS["{color}"] + self.test_content + Color.reset
                expected_text = Color(self.test_content).{color}
                self.assertEqual(action_test, expected_text)
            """
        )
        exec(test_template)
