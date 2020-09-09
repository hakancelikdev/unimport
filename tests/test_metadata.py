import unittest

from semantic_version import Version

from unimport.constants import DESCRIPTION, VERSION


class TestMetadata(unittest.TestCase):
    def test_description(self):
        self.assertEqual(type(DESCRIPTION), str)
        self.assertGreater(len(DESCRIPTION), 0, "Too short description.")

    def test_version(self):
        try:
            valid = bool(Version(VERSION))
        except ValueError:
            valid = False
        # It follows strictly the 2.0.0 version of the SemVer scheme.
        # For more information: https://semver.org/spec/v2.0.0.html
        self.assertTrue(valid, "Invalid semantic-version.")
