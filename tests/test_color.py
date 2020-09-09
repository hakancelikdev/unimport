import unittest

from unimport.color import COLORS, Color


class TestColor(unittest.TestCase):
    def test_color(self):
        reset = "\033[0m"
        styled_str = Color("Unimport")
        self.assertGreater(len(COLORS), 0, "No-colors")
        color = list(COLORS.keys())[0]
        value = COLORS[color]
        template = styled_str.template(color)
        self.assertTrue(template.startswith(value))
        self.assertTrue(template.endswith(reset))
        self.assertTrue(getattr(styled_str, color).startswith(value))
        self.assertTrue(getattr(styled_str, color).endswith(reset))
