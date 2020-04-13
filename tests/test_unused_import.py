import unittest
from unimport.session import Session

# These imports to write in modules below.
import pathlib
import lib2to3.fixer_util
import lib2to3.pytree
import lib2to3.pgen2.token
import re
import os


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
            [{"lineno": 1, "module": pathlib, "name": "Path", "star": False}],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_unused_import_3(self):
        source = (
            "import x.y\n" "import d.f.a.s\n" "CURRENT_DIR = x.y('.').parent\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [{"lineno": 2, "module": None, "name": "d.f.a.s", "star": False}],
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
                {"lineno": 1, "module": None, "name": "y", "star": False},
                {"lineno": 2, "module": None, "name": "y", "star": False},
                {"lineno": 3, "module": None, "name": "x", "star": False},
                {"lineno": 4, "module": re, "name": "re", "star": False},
                {"lineno": 5, "module": None, "name": "ll", "star": False},
                {"lineno": 6, "module": None, "name": "ll", "star": False},
                {"lineno": 7, "module": None, "name": "e", "star": False},
                {"lineno": 8, "module": None, "name": "e", "star": False},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_one_used(self):
        source = (
            "from x import y\n"  # 1 - unused
            "from x import y\n"  # 2 - unused
            "from t import x\n"  # 3 - unused
            "import re\n"  # 4 - unused
            "import ll\n"  # 5 - unused
            "import ll\n"  # 6 - unused
            "from c import e\n"  # 7 - unused
            "import e\n"  # 8 - unused
            "from pathlib import Path\n"  # 9 - unused
            "from pathlib import Path\n"  # 10 -
            "p = Path()"  # 11 -
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None},
                {"lineno": 2, "name": "y", "star": False, "module": None},
                {"lineno": 3, "name": "x", "star": False, "module": None},
                {"lineno": 4, "name": "re", "star": False, "module": re},
                {"lineno": 5, "name": "ll", "star": False, "module": None},
                {"lineno": 6, "name": "ll", "star": False, "module": None},
                {"lineno": 7, "name": "e", "star": False, "module": None},
                {"lineno": 8, "name": "e", "star": False, "module": None},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_two_used(self):
        source = (
            "from x import y\n"  # 1 - unused
            "from x import y\n"  # 2 - unused
            "from t import x\n"  # 3 - unused
            "import re\n"  # 4 - unused
            "import ll\n"  # 5 - unused
            "import ll\n"  # 6
            "from c import e\n"  # 7 - unused
            "import e\n"  # 8 - unused
            "from pathlib import Path\n"  # 9 - unused
            "from pathlib import Path\n"  # 10
            "p = Path()\n"  # 11
            "print(ll)\n"  # 12
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None},
                {"lineno": 2, "name": "y", "star": False, "module": None},
                {"lineno": 3, "name": "x", "star": False, "module": None},
                {"lineno": 4, "name": "re", "star": False, "module": re},
                {"lineno": 7, "name": "e", "star": False, "module": None},
                {"lineno": 8, "name": "e", "star": False, "module": None},
                {"lineno": 5, "name": "ll", "star": False, "module": None},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_three_used(self):
        source = (
            "from x import y\n"  # 1 - unused
            "from x import y\n"  # 2 - unused
            "from t import x\n"  # 3 - unused
            "import re\n"  # 4 - unused
            "import ll\n"  # 5 - unused
            "import ll\n"  # 6
            "from c import e\n"  # 7 - unused
            "import e\n"  # 8 -
            "from pathlib import Path\n"  # 9 - unused
            "from pathlib import Path\n"  # 10
            "p = Path()\n"  # 11
            "print(ll)\n"  # 12
            "def function(e=e):pass\n"
        )
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None},
                {"lineno": 2, "name": "y", "star": False, "module": None},
                {"lineno": 3, "name": "x", "star": False, "module": None},
                {"lineno": 4, "name": "re", "star": False, "module": re},
                {"lineno": 5, "name": "ll", "star": False, "module": None},
                {"lineno": 7, "name": "e", "star": False, "module": None},
                {
                    "lineno": 9,
                    "name": "Path",
                    "star": False,
                    "module": pathlib,
                },
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_different_duplicate_unused(self):
        source = "from x import z\n" "from y import z\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "module": None, "name": "z", "star": False},
                {"lineno": 2, "module": None, "name": "z", "star": False},
            ],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_different_duplicate_used(self):
        source = "from x import z\n" "from y import z\n" "print(z)\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [{"lineno": 1, "module": None, "name": "z", "star": False},],
            list(self.session.scanner.get_unused_imports()),
        )

    def test_multi_duplicate(self):
        source = "from x import y, z, t\n" "import t\n" "from l import t\n"
        self.session.scanner.run_visit(source)
        self.assertEqual(
            [
                {"lineno": 1, "name": "y", "star": False, "module": None},
                {"lineno": 1, "name": "z", "star": False, "module": None},
                {"lineno": 1, "name": "t", "star": False, "module": None},
                {"lineno": 2, "name": "t", "star": False, "module": None},
                {"lineno": 3, "name": "t", "star": False, "module": None},
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
                {"lineno": 1, "name": "y", "star": False, "module": None},
                {"lineno": 1, "name": "z", "star": False, "module": None},
                {"lineno": 1, "name": "t", "star": False, "module": None},
                {"lineno": 2, "name": "t", "star": False, "module": None},
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
                {"lineno": 3, "name": "y", "star": False, "module": None},
                {"lineno": 3, "name": "z", "star": False, "module": None},
                {"lineno": 1, "name": "t", "star": False, "module": None},
                {"lineno": 2, "name": "t", "star": False, "module": None},
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
                {"lineno": 3, "name": "y", "star": False, "module": None},
                {"lineno": 3, "name": "z", "star": False, "module": None},
                {"lineno": 4, "name": "ii", "star": False, "module": None},
                {"lineno": 1, "name": "t", "star": False, "module": None},
                {"lineno": 2, "name": "t", "star": False, "module": None},
                {"lineno": 3, "name": "t", "star": False, "module": None},
            ],
            list(self.session.scanner.get_unused_imports()),
        )
