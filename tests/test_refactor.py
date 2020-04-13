from unittest import TestCase

from unimport.session import Session


class TestRefactor(TestCase):
    maxDiff = None

    def setUp(self):
        self.session = Session()

    def test_do_not_remove_augmented_imports_action(self):
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

    def test_fix_multiple_problems_at_once_action(self):
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

    def test_from_x_import_star_action(self):
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
            "from lib2to3.pgen2.token import NAME\n\n"
            "print(match)\n"
            "print(search)\n"
            "print(NAME)\n\n"
        )
        self.assertEqual(
            expected, self.session.refactor(action),
        )

    def test_future_action(self):
        action = (
            "from __future__ import (\n"
            "    absolute_import, division, print_function, unicode_literals\n"
            ")\n"
        )
        self.assertEqual(
            action, self.session.refactor(action),
        )

    def test_local_import_action(self):
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

    def test_remove_unused_from_imports_action(self):
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

    def test_star_action(self):
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
