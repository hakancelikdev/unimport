import unittest

from unimport.session import Session


class TestUnusedRefactor(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_do_not_remove_augmented_imports(self):
        action = (
            "from django.conf.global_settings import AUTHENTICATION_BACKENDS, TEMPLATE_CONTEXT_PROCESSORS\n"
            "AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)\n"
        )
        expected = (
            "from django.conf.global_settings import AUTHENTICATION_BACKENDS\n"
            "AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multiple_imports(self):
        action = (
            "import x\n"
            "import x.y\n"
            "import x.y.z\n"
            "import x, x.y\n"
            "import x, x.y, x.y.z\n"
            "import x.y, x.y.z, x.y.z\n"
            "import x.y, x.y, x.y.z\n"
            "from x import y\n"
            "from x import y, z\n"
            "from x.y import z, q\n"
            "from x.y.z import z, q, zq\n"
            "some()\n"
            "calls()\n\n"
            "# and comments\n"
            "def maybe_functions(): # type: ignore\n"
            "    after()\n"
            "from x import (\n"
            "    y\n"
            ")\n"
            "from x import (\n"
            "    y,\n"
            "    z\n"
            ")\n"
            "from x import (\n"
            "    y,\n"
            "    z,\n"
            ")\n"
            "from x.y import (\n"
            "    z,\n"
            "    q,\n"
            "    u,\n"
            ")\n"
            "from x.y import (\n"
            "    z,\n"
            "    q,\n"
            "    u,\n"
            "    z,\n"
            "    q,\n"
            ")\n"
        )
        expected = (
            "some()\n"
            "calls()\n\n"
            "# and comments\n"
            "def maybe_functions(): # type: ignore\n"
            "    after()\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_star_imports(self):
        action = (
            "from os import *\n"
            "from x import y\n"
            "from re import *\n"
            "from t.s.d import *\n"
            "from lib2to3.pgen2.token import *\n"
            "from lib2to3.fixer_util import *\n\n"
            "print(match)\n"
            "print(search)\n"
            "print(NAME)\n\n"
        )
        expected = (
            "from re import match, search\n"
            "from t.s.d import *\n"
            "from lib2to3.pgen2.token import NAME\n\n"
            "print(match)\n"
            "print(search)\n"
            "print(NAME)\n\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_star_import_2(self):
        action = (
            "from typing import (\n"
            "    Callable,\n"
            "    Iterable,\n"
            "    Iterator,\n"
            "    List,\n"
            "    Optional,\n"
            "    Text,\n"
            "    Tuple,\n"
            "    Pattern,\n"
            "    Union,\n"
            "    cast,\n"
            ")\n"
            "from lib2to3.pgen2.token import *\n"
            "from lib2to3.pgen2.grammar import *\n"
            "print(Grammar)\n"
        )
        expected = (
            "from lib2to3.pgen2.grammar import Grammar\n" "print(Grammar)\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_future(self):
        action = (
            "from __future__ import (\n"
            "    absolute_import, division, print_function, unicode_literals\n"
            ")\n"
        )
        self.assertEqual(
            action, self.session.refactor(action),
        )

    def test_local_import(self):
        action = (
            "from .x import y\n"
            "from ..z import t\n"
            "from ...t import a\n"
            "from .x import y, hakan\n"
            "from ..z import u, b\n"
            "from ...t import z, q\n\n"
            "hakan\n"
            "b\n"
            "q()\n"
        )
        expected = (
            "from .x import hakan\n"
            "from ..z import b\n"
            "from ...t import q\n\n"
            "hakan\n"
            "b\n"
            "q()\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_remove_unused_from_imports(self):
        action = (
            "import datetime\n"
            "from dateutil.relativedelta import relativedelta\n\n"
            "print(f'The date is {datetime.datetime.now()}.')\n"
        )
        expected = (
            "import datetime\n\n"
            "print(f'The date is {datetime.datetime.now()}.')\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_inside_function_unused(self):
        action = (
            "def foo():\n"
            "    from x import y, z\n"
            "    try:\n"
            "        import t\n"
            "        print(t)\n"
            "    except ImportError as exception:\n"
            "        pass\n"
            "    return math.pi\n"
        )
        expected = (
            "def foo():\n"
            "    try:\n"
            "        import t\n"
            "        print(t)\n"
            "    except ImportError as exception:\n"
            "        pass\n"
            "    return math.pi\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_comment(self):
        action = (
            "# This is not unused import, but it is unused import according to unimport.\n"
            "# CASE 1\n"
            "from codeop import compile_command\n\n"
            "compile_command\n"
        )
        expected = (
            "# This is not unused import, but it is unused import according to unimport.\n"
            "# CASE 1\n"
            "from codeop import compile_command\n\n"
            "compile_command\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )


class TestDuplicateUnusedRefactor(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_full_unused(self):
        action = (
            "from x import y\n"
            "from x import y\n"
            "from t import x\n"
            "import re\n"
            "import ll\n"
            "import ll\n"
            "from c import e\n"
            "import e\n"
        )
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_one_used(self):
        action = (
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
        )
        expected = "from pathlib import Path\n" "p = Path()\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_two_used(self):
        action = (
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

        expected = (
            "import ll\n"
            "from pathlib import Path\n"
            "p = Path()\n"
            "print(ll)\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_three_used(self):
        action = (
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
        expected = (
            "import ll\n"
            "import e\n"
            "from pathlib import Path\n"
            "p = Path()\n"
            "print(ll)\n"
            "def function(e=e):pass\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_different_duplicate_unused(self):
        action = "from x import z\n" "from y import z\n"
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_different_duplicate_used(self):
        action = "from x import z\n" "from y import z\n" "print(z)\n"
        expected = "from y import z\n" "print(z)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multi_duplicate(self):
        action = "from x import y, z, t\n" "import t\n" "from l import t\n"
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multi_duplicate_one_used(self):
        action = (
            "from x import y, z, t\n"
            "import t\n"
            "from l import t\n"
            "print(t)\n"
        )
        expected = "from l import t\n" "print(t)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_one_used_bottom_multi_duplicate(self):
        action = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "print(t)\n"
        )
        expected = "from x import t\n" "print(t)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_two_multi_duplicate_one_used(self):
        action = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected = "from i import t\n" "print(t)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_import_in_function(self):
        action = (
            "import t\n"
            "from l import t\n"
            "from x import y, z, t\n\n"
            "def function(f=t):\n"
            "    import x\n"
            "    return f\n"
            "from i import t, ii\n"
            "print(t)\n"
        )
        expected = (
            "from x import t\n\n"
            "def function(f=t):\n"
            "    return f\n"
            "from i import t\n"
            "print(t)\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_import_in_function_used_two_different(self):
        action = (
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
        expected = (
            "import t\n"
            "print(t)\n"
            "from x import t\n\n"
            "def function(f=t):\n"
            "    return f\n"
            "from i import t\n"
            "print(t)\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )


class TesAsImport(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_as_import_all_unused_all_cases(self):
        action = (
            "from x import y as z\n"
            "import x\n"
            "from t import s as ss\n"
            "import le as x\n"
        )
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multiple_from_as_import(self):
        action = (
            "from f import a as c, l as k, i as ii\n"
            "from fo import (bar, i, x as z)\n"
        )
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multiple_import_name_as_import(self):
        action = "import a as c, l as k, i as ii\n" "import bar, i, x as z\n"
        expected = "\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_multiple_import_name_as_import_duplicate(self):
        action = (
            "import a as c, l as k, i as ii\n"
            "import bar, i, x as z\n"
            "import bar, i, x as z\n"
            "print(bar)\n"
        )
        expected = "import bar\n" "print(bar)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_as_import_used_all_cases(self):
        action = (
            "from x import y as z\n"
            "import x\n"
            "from t import s as ss\n"
            "import bar, i, x as z\n"
            "import le as x\n"
            "print(x)\n"
        )
        expected = "import le as x\n" "print(x)\n"
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_inside_function_unused(self):
        action = (
            "def foo():\n"
            "    from abc import *\n"
            "    try:\n"
            "        import t\n"
            "        print(ABCMeta)\n"
            "    except ImportError as exception:\n"
            "        pass\n"
            "    return math.pi\n"
        )
        expected = (
            "def foo():\n"
            "    from abc import ABCMeta\n"
            "    try:\n"
            "        print(ABCMeta)\n"
            "    except ImportError as exception:\n"
            "        pass\n"
            "    return math.pi\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )
