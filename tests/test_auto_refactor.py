from unittest import TestCase
from unimport.auto_refactor import refactor


class RefactorTests(TestCase):
    def test_remove_unused_modules(self):
        self.assertEqual(refactor("import x\n", ["x"]), "")

        self.assertEqual(refactor("import x, y\n", ["x"]), "import y\n")
        self.assertEqual(refactor("import x, y\n", ["y"]), "import x\n")
        self.assertEqual(refactor("import x, y\n", ["x", "y"]), "")

        self.assertEqual(refactor("import x, y, z\n", ["x"]), "import y, z\n")
        self.assertEqual(refactor("import x, y, z\n", ["y"]), "import x, z\n")
        self.assertEqual(refactor("import x, y, z\n", ["z"]), "import x, y\n")
        self.assertEqual(
            refactor("import x, y, z\n", ["x", "y"]), "import z\n"
        )
        self.assertEqual(
            refactor("import x, y, z # this is OK\n", ["x", "y"]),
            "import z # this is OK\n",
        )
        self.assertEqual(
            refactor("import x, y, z\n", ["x", "z"]), "import y\n"
        )
        self.assertEqual(refactor("import x, y, z\n", ["x", "y", "z"]), "")

        self.assertEqual(
            refactor("import x, y, z.k\n", ["x"]), "import y, z.k\n"
        )
        self.assertEqual(
            refactor("import x, y, z.k\n", ["z"]), "import x, y, z.k\n"
        )
        self.assertEqual(
            refactor("import x.k, y.z, u.k\n", ["y.z"]), "import x.k, u.k\n"
        )

    def test_remove_unused_imports_from(self):
        self.assertEqual(refactor("from x import foo\n", ["x"]), "")
        self.assertEqual(refactor("from x.y.z import foo\n", ["x.y.z"]), "")

        self.assertEqual(refactor("from x import foo\n", ["foo"]), "")
        self.assertEqual(refactor("from x.y.z import foo\n", ["foo"]), "")
