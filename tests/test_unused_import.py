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
                suggestions=["removedirs", "walk"],
                name="os",
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
                suggestions=["removedirs", "walk"],
                name="os",
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
                suggestions=["removedirs", "walk"],
                name="os",
                star=True,
            ),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_star_unused(self):
        # in this case this import is unused
        source = "from os import *\n" "__all__ = ['test']"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="os", star=True),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_plus_bin_op(self):
        # NOTE no support.
        source = "from os import *\n" "__all__ = ['w' + 'alk']"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="os", star=True),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_list_comprehension(self):
        # NOTE no support.
        source = (
            "from os import *\n"
            "__all__ = [expression for item in ['os', 'walk']]"
        )
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="os", star=True),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_unknown(self):
        source = "from x import *\n" "__all__ = ['xx']"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="x", star=True),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)


class TestUnusedImport(UnusedTestCase):
    include_star_import = True

    def test_comma(self):
        source = "from os import (\n" "    waitpid,\n" "    scandir,\n" ")\n"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="waitpid", star=False),
            ImportFrom(lineno=1, suggestions=[], name="scandir", star=False),
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
            ImportFrom(lineno=1, suggestions=[], name="Path", star=False),
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
            Import(lineno=2, name="d.f.a.s"),
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
            ImportFrom(lineno=2, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=2, name="z", star=False, suggestions=[]),
            Import(
                lineno=5,
                name="x",
            ),
            ImportFrom(lineno=7, name="ii", star=False, suggestions=[]),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_import_after_usage(self):
        source = "def function():\n" "    print(os)\n" "import os\n"
        expected_unused_imports = []
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
            ImportFrom(lineno=1, name="os", star=True, suggestions=[]),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_used(self):
        source = "from os import *\n" "print(walk)\n"
        expected_unused_imports = [
            ImportFrom(lineno=1, name="os", star=True, suggestions=["walk"]),
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
                name="lib2to3.fixer_util",
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
                name="lib2to3.pytree",
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
                name="lib2to3.fixer_util",
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
                name="lib2to3.pytree",
                star=True,
                suggestions=["Leaf", "Node"],
            ),
            ImportFrom(
                lineno=3,
                name="lib2to3.pgen2.token",
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
                suggestions=[],
                name="compile_command",
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
            ImportFrom(lineno=1, suggestions=[], name="y", star=False),
            ImportFrom(lineno=2, suggestions=[], name="y", star=False),
            ImportFrom(lineno=3, suggestions=[], name="x", star=False),
            Import(lineno=4, name="re"),
            Import(lineno=5, name="ll"),
            Import(lineno=6, name="ll"),
            ImportFrom(lineno=7, suggestions=[], name="e", star=False),
            Import(lineno=8, name="e"),
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
            ImportFrom(lineno=1, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=2, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="x", star=False, suggestions=[]),
            Import(lineno=4, name="re"),
            Import(lineno=5, name="ll"),
            Import(lineno=6, name="ll"),
            ImportFrom(lineno=7, name="e", star=False, suggestions=[]),
            Import(
                lineno=8,
                name="e",
            ),
            ImportFrom(lineno=9, name="Path", star=False, suggestions=[]),
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
            ImportFrom(lineno=1, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=2, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="x", star=False, suggestions=[]),
            Import(lineno=4, name="re"),
            Import(lineno=5, name="ll"),
            ImportFrom(lineno=7, name="e", star=False, suggestions=[]),
            Import(
                lineno=8,
                name="e",
            ),
            ImportFrom(lineno=9, name="Path", star=False, suggestions=[]),
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
            ImportFrom(lineno=1, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=2, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="x", star=False, suggestions=[]),
            Import(lineno=4, name="re"),
            Import(
                lineno=5,
                name="ll",
            ),
            ImportFrom(lineno=7, name="e", star=False, suggestions=[]),
            ImportFrom(lineno=9, name="Path", star=False, suggestions=[]),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_different_duplicate_unused(self):
        source = "from x import z\n" "from y import z\n"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="z", star=False),
            ImportFrom(lineno=2, suggestions=[], name="z", star=False),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_different_duplicate_used(self):
        source = "from x import z\n" "from y import z\n" "print(z)\n"
        expected_unused_imports = [
            ImportFrom(lineno=1, suggestions=[], name="z", star=False),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)

    def test_multi_duplicate(self):
        source = "from x import y, z, t\n" "import t\n" "from l import t\n"
        expected_unused_imports = [
            ImportFrom(lineno=1, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=1, name="z", star=False, suggestions=[]),
            ImportFrom(lineno=1, name="t", star=False, suggestions=[]),
            Import(
                lineno=2,
                name="t",
            ),
            ImportFrom(lineno=3, name="t", star=False, suggestions=[]),
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
            ImportFrom(lineno=1, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=1, name="z", star=False, suggestions=[]),
            ImportFrom(lineno=1, name="t", star=False, suggestions=[]),
            Import(
                lineno=2,
                name="t",
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
            Import(
                lineno=1,
                name="t",
            ),
            ImportFrom(lineno=2, name="t", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="z", star=False, suggestions=[]),
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
                name="t",
            ),
            ImportFrom(lineno=2, name="t", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="z", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="t", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="ii", star=False, suggestions=[]),
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
                name="t",
            ),
            ImportFrom(lineno=2, name="t", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=3, name="z", star=False, suggestions=[]),
            Import(
                lineno=6,
                name="x",
            ),
            ImportFrom(lineno=8, name="ii", star=False, suggestions=[]),
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
            ImportFrom(lineno=4, name="t", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="y", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="z", star=False, suggestions=[]),
            Import(
                lineno=8,
                name="x",
            ),
            ImportFrom(lineno=10, name="ii", star=False, suggestions=[]),
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
            ImportFrom(lineno=1, name="z", star=False, suggestions=[]),
            Import(
                lineno=2,
                name="x",
            ),
            ImportFrom(lineno=3, name="ss", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="c", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="k", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="ii", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="bar", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="i", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="z", star=False, suggestions=[]),
            Import(
                lineno=6,
                name="x",
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
            ImportFrom(lineno=1, name="z", star=False, suggestions=[]),
            Import(
                lineno=2,
                name="x",
            ),
            ImportFrom(lineno=3, name="ss", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="c", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="k", star=False, suggestions=[]),
            ImportFrom(lineno=4, name="ii", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="bar", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="i", star=False, suggestions=[]),
            ImportFrom(lineno=5, name="z", star=False, suggestions=[]),
        ]
        self.assertUnimportEqual(source, expected_unused_imports)
