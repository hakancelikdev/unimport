import unittest

from unimport.session import Session
from unimport.statement import Import, ImportFrom


class UnusedTestCase(unittest.TestCase):
    maxDiff = None
    include_star_import = False

    def setUp(self):
        self.session = Session(include_star_import=self.include_star_import)

    def assertUnimportEqual(self, source, expected_unused_imports):
        self.session.scanner.scan(source)
        self.assertEqual(
            expected_unused_imports,
            self.session.scanner.unused_imports,
        )
        self.session.scanner.clear()


class TestBuiltin(UnusedTestCase):
    include_star_import = True

    def test_ConnectionError(self):
        source = (
            "from x.y import ConnectionError\n"
            "try:\n"
            "   pass\n"
            "except ConnectionError:\n"
            "   pass\n"
        )
        expected_unused_imports = []
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_ValueError(self):
        source = "from x import ValueError\n" "print(ValueError)\n"
        expected_unused_imports = []
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_builtins(self):
        source = (
            "from builtins import next, object, range\n"
            "__all__ = ['next', 'object']\n"
            "for i in range(8):\n"
            "   pass\n"
        )
        expected_unused_imports = []
        self.assertUnimportEqual(source, expected_unused_imports)


class Test__All__(UnusedTestCase):
    include_star_import = True

    def test_from_import(self):
        # in this case this import is used
        source = (
            "from codeop import compile_command\n"
            "__all__ = ['compile_command']"
        )
        self.assertUnimportEqual(source, [])

    def test_star(self):
        # in this case this import is used
        source = "from os import *\n" "__all__ = ['walk', 'removedirs']"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=["removedirs", "walk"],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_append(self):
        source = (
            "from os import *\n"
            "__all__ = ['walk']\n"
            "__all__.append('removedirs')\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=["removedirs", "walk"],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_extend(self):
        source = (
            "from os import *\n"
            "__all__ = ['walk']\n"
            "__all__.extend(['removedirs'])\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=["removedirs", "walk"],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_star_unused(self):
        # in this case this import is unused
        source = "from os import *\n" "__all__ = ['test']"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_plus_bin_op(self):
        # NOTE no support.
        source = "from os import *\n" "__all__ = ['w' + 'alk']"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_list_comprehension(self):
        # NOTE no support.
        source = (
            "from os import *\n"
            "__all__ = [expression for item in ['os', 'walk']]"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="os",
                package="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_unknown(self):
        source = "from x import *\n" "__all__ = ['xx']"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="x",
                package="x",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)


class TestUnusedImport(UnusedTestCase):
    include_star_import = True

    def test_comma(self):
        source = "from os import (\n" "    waitpid,\n" "    scandir,\n" ")\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="waitpid",
                package="os",
                star=False,
            ),
            ImportFrom(
                lineno=1,
                column=2,
                suggestions=[],
                name="scandir",
                package="os",
                star=False,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_module_used(self):
        source = (
            "from pathlib import Path\n" "CURRENT_DIR = Path('.').parent\n"
        )
        expected_unused_imports = []
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_module_unused(self):
        source = "from pathlib import Path"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="Path",
                package="pathlib",
                star=False,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_unknown_module_used(self):
        source = "import x.y\n" "CURRENT_DIR = x.y('.').parent\n"
        expected_unused_imports = []
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_unknown_module_unused(self):
        source = (
            "import x.y\n" "import d.f.a.s\n" "CURRENT_DIR = x.y('.').parent\n"
        )
        expected_unused_imports = [
            Import(
                lineno=2,
                column=1,
                name="d.f.a.s",
                package="d.f.a.s",
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_import_in_function(self):
        source = (
            "import t\n"
            "from x import y, z\n\n"
            "def function(f=t):\n"
            "    import x\n"
            "    return f\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=5,
                column=1,
                name="x",
                package="x",
            ),
            ImportFrom(
                lineno=7,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_import_after_usage(self):
        source = "def function():\n" "    print(os)\n" "import os\n"
        expected_unused_imports = [
            Import(lineno=3, column=1, name="os", package="os")
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_double_underscore_builtins_names(self):
        source = (
            "from globals import (\n"
            "    __name__, __doc__, __package__,\n"
            "   __loader__, __spec__, __annotations__,\n"
            "   __builtins__"
            ")\n"
            "__name__, __doc__, __package__,\n"
            "__loader__, __spec__, __annotations__,\n"
            "__builtins__\n"
        )
        self.assertUnimportEqual(source, [])


class TestStarImport(UnusedTestCase):
    include_star_import = True

    def test_unused(self):
        source = "from os import *\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_used(self):
        source = "from os import *\n" "print(walk)\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="os",
                package="os",
                star=True,
                suggestions=["walk"],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_used_and_unused(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2 import token\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "token.NAME, token.STAR\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="lib2to3.fixer_util",
                package="lib2to3.fixer_util",
                star=True,
                suggestions=[
                    "BlankLine",
                    "FromImport",
                    "Leaf",  #
                    "Newline",
                    "Node",  #
                    "token",  #
                ],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="lib2to3.pytree",
                package="lib2to3.pytree",
                star=True,
                suggestions=["Leaf", "Node"],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_used_and_unused_2(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2.token import *\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "NAME, STAR\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="lib2to3.fixer_util",
                package="lib2to3.fixer_util",
                star=True,
                suggestions=[
                    "BlankLine",
                    "FromImport",
                    "Leaf",  #
                    "Newline",
                    "Node",  #
                ],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="lib2to3.pytree",
                package="lib2to3.pytree",
                star=True,
                suggestions=["Leaf", "Node"],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="lib2to3.pgen2.token",
                package="lib2to3.pgen2.token",
                star=True,
                suggestions=["NAME", "STAR"],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)


class TestDuplicate(UnusedTestCase):
    def test__all__(self):
        source = (
            "from codeop import compile_command\n"
            "import compile_command\n"
            "__all__ = ['compile_command']"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="compile_command",
                package="codeop",
                star=False,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_full_unused(self):
        source = (
            "from x import y\n"
            "from x import y\n"
            "from t import x\n"
            "import re\n"
            "import ll\n"
            "import ll\n"
            "from c import e\n"
            "import e\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="y",
                package="x",
                star=False,
            ),
            ImportFrom(
                lineno=2,
                column=1,
                suggestions=[],
                name="y",
                package="x",
                star=False,
            ),
            ImportFrom(
                lineno=3,
                column=1,
                suggestions=[],
                name="x",
                package="t",
                star=False,
            ),
            Import(lineno=4, column=1, name="re", package="re"),
            Import(lineno=5, column=1, name="ll", package="ll"),
            Import(lineno=6, column=1, name="ll", package="ll"),
            ImportFrom(
                lineno=7,
                column=1,
                suggestions=[],
                name="e",
                package="c",
                star=False,
            ),
            Import(lineno=8, column=1, name="e", package="e"),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_one_used(self):
        source = (
            "from x import y\n"
            "from x import y\n"
            "from t import x\n"
            "import re\n"
            "import ll\n"
            "import ll\n"
            "from c import e\n"
            "import e\n"
            "from pathlib import Path\n"
            "from pathlib import Path\n"
            "p = Path()"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=4,
                column=1,
                name="re",
                package="re",
            ),
            Import(
                lineno=5,
                column=1,
                name="ll",
                package="ll",
            ),
            Import(
                lineno=6,
                column=1,
                name="ll",
                package="ll",
            ),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=8,
                column=1,
                name="e",
                package="e",
            ),
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_two_used(self):
        source = (
            "from x import y\n"
            "from x import y\n"
            "from t import x\n"
            "import re\n"
            "import ll\n"
            "import ll\n"
            "from c import e\n"
            "import e\n"
            "from pathlib import Path\n"
            "from pathlib import Path\n"
            "p = Path()\n"
            "print(ll)\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=4,
                column=1,
                name="re",
                package="re",
            ),
            Import(
                lineno=5,
                column=1,
                name="ll",
                package="ll",
            ),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=8,
                column=1,
                name="e",
                package="e",
            ),
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_three_used(self):
        source = (
            "from x import y\n"
            "from x import y\n"
            "from t import x\n"
            "import re\n"
            "import ll\n"
            "import ll\n"
            "from c import e\n"
            "import e\n"
            "from pathlib import Path\n"
            "from pathlib import Path\n"
            "p = Path()\n"
            "print(ll)\n"
            "def function(e=e):pass\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="x",
                package="t",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=4,
                column=1,
                name="re",
                package="re",
            ),
            Import(
                lineno=5,
                column=1,
                name="ll",
                package="ll",
            ),
            ImportFrom(
                lineno=7,
                column=1,
                name="e",
                package="c",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=9,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_different_duplicate_unused(self):
        source = "from x import z\n" "from y import z\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="z",
                package="x",
                star=False,
            ),
            ImportFrom(
                lineno=2,
                column=1,
                suggestions=[],
                name="z",
                package="y",
                star=False,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_different_duplicate_used(self):
        source = "from x import z\n" "from y import z\n" "print(z)\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="z",
                package="x",
                star=False,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_multi_duplicate(self):
        source = "from x import y, z, t\n" "import t\n" "from l import t\n"
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=2,
                column=1,
                name="t",
                package="t",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_multi_duplicate_one_used(self):
        source = (
            "from x import y, z, t\n"
            "import t\n"
            "from l import t\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=2,
                column=1,
                name="t",
                package="t",
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_one_used_bottom_multi_duplicate(self):
        source = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            Import(lineno=1, column=1, name="t", package="t"),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_two_multi_duplicate_one_used(self):
        source = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            Import(
                lineno=1,
                column=1,
                name="t",
                package="t",
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=3,
                name="t",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_import_in_function(self):
        source = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n\n"
            "def function(f=t):\n"
            "    import x\n"
            "    return f\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            Import(
                lineno=1,
                column=1,
                name="t",
                package="t",
            ),
            ImportFrom(
                lineno=2,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=6,
                column=1,
                name="x",
                package="x",
            ),
            ImportFrom(
                lineno=8,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_import_in_function_used_two_different(self):
        source = (
            "import t\n"
            "print(t)\n\n"
            "from l import t\n"
            "from x import y, z, t\n\n"
            "def function(f=t):\n"
            "    import x\n"
            "    return f\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=4,
                column=1,
                name="t",
                package="l",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=1,
                name="y",
                package="x",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=2,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=8,
                column=1,
                name="x",
                package="x",
            ),
            ImportFrom(
                lineno=10,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_same_line(self):
        source = (
            "import x, x, yt\n"
            "import e, y, e\n"
            "from z import u, u\n"
            "from bb import c, d, c, c\n"
            "import ff, tt, ff, ff, tt\n"
            "from ee import (\n"
            "   ll,\n"
            "   el,\n"
            "   ll,\n"
            "   el,\n"
            "   tl,\n"
            "   tl,\n"
            ")\n"
            "import iss as si, si\n"
            "from gu import ug,\\\n"
            "ug"
            "\n"
            "x, e, u, c, ff, tt, ll, el, tl, si, ug, yt"
        )
        expected_unused_imports = [
            Import(
                lineno=1,
                column=1,
                name="x",
                package="x",
            ),
            Import(
                lineno=2,
                column=1,
                name="e",
                package="e",
            ),
            Import(
                lineno=2,
                column=2,
                name="y",
                package="y",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="u",
                package="z",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="c",
                package="bb",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=2,
                name="d",
                package="bb",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=3,
                name="c",
                package="bb",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=5,
                column=1,
                name="ff",
                package="ff",
            ),
            Import(
                lineno=5,
                column=2,
                name="tt",
                package="tt",
            ),
            Import(
                lineno=5,
                column=3,
                name="ff",
                package="ff",
            ),
            ImportFrom(
                lineno=6,
                column=1,
                name="ll",
                package="ee",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=6,
                column=2,
                name="el",
                package="ee",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=6,
                column=5,
                name="tl",
                package="ee",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=14,
                column=1,
                name="si",
                package="iss",
            ),
            ImportFrom(
                lineno=15,
                column=1,
                name="ug",
                package="gu",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)


class TestAsImport(UnusedTestCase):
    def test_as_import_all_unused_all_cases(self):
        source = (
            "from x import y as z\n"
            "import x\n"
            "from t import s as ss\n"
            "from f import a as c, l as k, i as ii\n"
            "from fo import (bar, i, x as z)\n"
            "import le as x\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=2,
                column=1,
                name="x",
                package="x",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="ss",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="c",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=2,
                name="k",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=3,
                name="ii",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=1,
                name="bar",
                package="fo",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=2,
                name="i",
                package="fo",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=3,
                name="z",
                package="fo",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=6,
                column=1,
                name="x",
                package="le",
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_as_import_one_used_in_function_all_cases(self):
        source = (
            "from x import y as z\n"
            "import x\n"
            "from t import s as ss\n"
            "from f import a as c, l as k, i as ii\n"
            "from fo import (bar, i, x as z)\n"
            "import le as x\n"
            "def x(t=x):pass\n"
        )
        expected_unused_imports = [
            ImportFrom(
                lineno=1,
                column=1,
                name="z",
                package="x",
                star=False,
                suggestions=[],
            ),
            Import(
                lineno=2,
                column=1,
                name="x",
                package="x",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="ss",
                package="t",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="c",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=2,
                name="k",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=3,
                name="ii",
                package="f",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=1,
                name="bar",
                package="fo",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=2,
                name="i",
                package="fo",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=5,
                column=3,
                name="z",
                package="fo",
                star=False,
                suggestions=[],
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)
