import unittest

import semantic_version

from unimport.constants import DESCRIPTION, VERSION


class TestMetadata(unittest.TestCase):
    def test_description(self):
        self.assertIsInstance(DESCRIPTION, str)
        self.assertGreater(len(DESCRIPTION), 0, "Too short description.")

    def test_version(self):
        # It follows strictly the 2.0.0 version of the SemVer scheme.
        # For more information: https://semver.org/spec/v2.0.0.html
        self.assertIsInstance(VERSION, str)
        self.assertTrue(semantic_version.validate(VERSION), "Invalid semantic-version.")
