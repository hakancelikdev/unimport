import textwrap
import unittest

from unimport.color import Color  # unimport: skip
from unimport.color import terminal_supports_color  # unimport: skip
from unimport.color import COLORS


class TestColor(unittest.TestCase):
    def setUp(self):
        self.test_content = "Test Content"

    for color in COLORS:
        test_template = textwrap.dedent(
            f"""
            def test_{color}(self):
                if terminal_supports_color:
                    action_test = COLORS["{color}"] + self.test_content + Color.reset
                else:
                    action_test = self.test_content
                expected_text = Color(self.test_content).{color}
                self.assertEqual(expected_text, action_test)
            """
        )
        exec(test_template)
