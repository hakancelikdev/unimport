import lib2to3.fixer_util
import lib2to3.pgen2.token
import lib2to3.pytree
import os
import pathlib
import re
import unittest

from unimport.session import Session


class TestUnusedImport(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_unused_import_1(self):
        source = (
            "from pathlib import Path\n" "CURRENT_DIR = Path('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual([], list(self.session.scanner.get_unused_imports()))

    def test_unused_import_2(self):
        source = "from pathlib import Path"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [{"lineno": 1, "module": pathlib, "modules": [], "name": "Path", "star": False}],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_3(self):
        source = (
            "import x.y\n" "import d.f.a.s\n" "CURRENT_DIR = x.y('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [{"lineno": 2, "module": None, "modules": [], "name": "d.f.a.s", "star": False}],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_4(self):
        source = (
            "from os import *\n"
            "#from sys import *\n"
            "#import re\n"
            "variable=1\n"
            "print(walk)\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    "lineno": 1,
                    "name": "os",
                    "star": True,
                    "module": os,
                    "modules": ["walk"],
                }
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_5(self):
        source = "from os import *\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    "lineno": 1,
                    "module": os,
                    "name": "os",
                    "star": True,
                    "modules": [],
                }
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_6(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2 import token\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "token.NAME, token.STAR\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    "lineno": 1,
                    "module": lib2to3.fixer_util,
                    "name": "lib2to3.fixer_util",
                    "star": True,
                    "modules": [
                        "BlankLine",
                        "FromImport",
                        "Leaf",
                        "Newline",
                        "Node",
                        "token",
                        "token.NAME",
                        "token.STAR",
                    ],
                },
                {
                    "lineno": 2,
                    "module": lib2to3.pytree,
                    "name": "lib2to3.pytree",
                    "star": True,
                    "modules": ["Leaf", "Node"],
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_7(self):
        source = (
            "from lib2to3.fixer_util import *\n"
            "from lib2to3.pytree import *\n"
            "from lib2to3.pgen2.token import *\n"
            "BlankLine, FromImport, Leaf, Newline, Node\n"
            "NAME, STAR\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {
                    "lineno": 1,
                    "name": "lib2to3.fixer_util",
                    "module": lib2to3.fixer_util,
                    "star": True,
                    "modules": [
                        "BlankLine",
                        "FromImport",
                        "Leaf",
                        "Newline",
                        "Node",
                    ],
                },
                {
                    "lineno": 2,
                    "name": "lib2to3.pytree",
                    "module": lib2to3.pytree,
                    "star": True,
                    "modules": ["Leaf", "Node"],
                },
                {
                    "lineno": 3,
                    "name": "lib2to3.pgen2.token",
                    "star": True,
                    "module": lib2to3.pgen2.token,
                    "modules": ["NAME", "STAR"],
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 2, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 7, "name": "ii", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_import_after_usage(self):
        source = (
            "def function():\n"
            "    print(os)\n"
            "import os\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [], list(self.session.scanner.get_unused_imports()),
        )


class TestDuplicate(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "module": None, "modules": [], "name": "y", "star": False},
                {"lineno": 2, "module": None, "modules": [], "name": "y", "star": False},
                {"lineno": 3, "module": None, "modules": [], "name": "x", "star": False},
                {"lineno": 4, "module": re, "modules": [], "name": "re", "star": False},
                {"lineno": 5, "module": None, "modules": [], "name": "ll", "star": False},
                {"lineno": 6, "module": None, "modules": [], "name": "ll", "star": False},
                {"lineno": 7, "module": None, "modules": [], "name": "e", "star": False},
                {"lineno": 8, "module": None, "modules": [], "name": "e", "star": False},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "re", "star": False, "module": re, "modules": []},
                {"lineno": 5, "name": "ll", "star": False, "module": None, "modules": []},
                {"lineno": 6, "name": "ll", "star": False, "module": None, "modules": []},
                {"lineno": 7, "name": "e", "star": False, "module": None, "modules": []},
                {"lineno": 8, "name": "e", "star": False, "module": None, "modules": []},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                    "modules": []
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "re", "star": False, "module": re, "modules": []},
                {"lineno": 5, "name": "ll", "star": False, "module": None, "modules": []},
                {"lineno": 7, "name": "e", "star": False, "module": None, "modules": []},
                {"lineno": 8, "name": "e", "star": False, "module": None, "modules": []},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                    "modules": []
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "re", "star": False, "module": re, "modules": []},
                {"lineno": 5, "name": "ll", "star": False, "module": None, "modules": []},
                {"lineno": 7, "name": "e", "star": False, "module": None, "modules": []},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                    "modules": []
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_different_duplicate_unused(self):
        source = "from x import z\n" "from y import z\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "module": None, "modules": [], "name": "z", "star": False},
                {"lineno": 2, "module": None, "modules": [], "name": "z", "star": False},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_different_duplicate_used(self):
        source = "from x import z\n" "from y import z\n" "print(z)\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [{"lineno": 1, "module": None, "modules": [], "name": "z", "star": False},],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_multi_duplicate(self):
        source = "from x import y, z, t\n" "import t\n" "from l import t\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 1, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 1, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "t", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_multi_duplicate_one_used(self):
        source = (
            "from x import y, z, t\n"
            "import t\n"
            "from l import t\n"
            "print(t)\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 1, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 1, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "t", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_one_used_bottom_multi_duplicate(self):
        source = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "print(t)\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "z", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_two_multi_duplicate_one_used(self):
        source = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "ii", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 6, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 8, "name": "ii", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 4, "name": "t", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "y", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 8, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 10, "name": "ii", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )


class TesAsImport(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_as_import_all_unused_all_cases(self):
        source = (
            "from x import y as z\n"
            "import x\n"
            "from t import s as ss\n"
            "from f import a as c, l as k, i as ii\n"
            "from fo import (bar, i, x as z)\n"
            "import le as x\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "ss", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "c", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "k", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "ii", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "bar", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "i", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 6, "name": "x", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

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
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "z", "star": False, "module": None, "modules": []},
                {"lineno": 2, "name": "x", "star": False, "module": None, "modules": []},
                {"lineno": 3, "name": "ss", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "c", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "k", "star": False, "module": None, "modules": []},
                {"lineno": 4, "name": "ii", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "bar", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "i", "star": False, "module": None, "modules": []},
                {"lineno": 5, "name": "z", "star": False, "module": None, "modules": []},
            ],
            list(self.session.scanner.get_unused_imports()),
        )
