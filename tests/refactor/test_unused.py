from tests.refactor.utils import RefactorTestCase


class UnusedTestCase(RefactorTestCase):
    def test_do_not_remove_augmented_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from django.conf.global_settings import AUTHENTICATION_BACKENDS, TEMPLATE_CONTEXT_PROCESSORS
            AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)
            """,
            """\
            from django.conf.global_settings import AUTHENTICATION_BACKENDS
            AUTHENTICATION_BACKENDS += ('foo.bar.baz.EmailBackend',)
            """,
        )

    def test_multiple_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import x
            import x.y
            import x.y.z
            import x, x.y
            import x, x.y, x.y.z
            import x.y, x.y.z, x.y.z
            import x.y, x.y, x.y.z
            from x import y
            from x import y, z
            from x.y import z, q
            from x.y.z import z, q, zq
            some()
            calls()
            # and comments
            def maybe_functions():
                after()
            from x import (
                y
            )
            from x import (
                y,
                z
            )
            from x import (
                y,
                z,
            )
            from x.y import (
                z,
                q,
                u,
            )
            from x.y import (
                z,
                q,
                u,
                z,
                q,
            )
            """,
            """\
            some()
            calls()
            # and comments
            def maybe_functions():
                after()
            """,
        )

    def test_future_from_import(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from __future__ import (
                absolute_import, division, print_function, unicode_literals
            )
            """
        )

    def test_future_import(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            import __future__
            __future__.absolute_import
            """
        )

    def test_local_import(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            from .x import y
            from ..z import t
            from ...t import a
            from .x import y, hakan
            from ..z import u, b
            from ...t import z, q
            hakan
            b
            q()
            """,
            """\
            from .x import hakan
            from ..z import b
            from ...t import q
            hakan
            b
            q()
            """,
        )

    def test_remove_unused_from_imports(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import datetime
            from dateutil.relativedelta import relativedelta
            print(f'The date is {datetime.datetime.now()}.')
            """,
            """\
            import datetime
            print(f'The date is {datetime.datetime.now()}.')
            """,
        )

    def test_inside_function_unused(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            def foo():
                from x import y, z
                try:
                    import t
                    print(t)
                except ImportError as exception:
                    pass
                return math.pi
            """,
            """\
            def foo():
                try:
                    import t
                    print(t)
                except ImportError as exception:
                    pass
                return math.pi
            """,
        )

    def test_comment(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            # This is not unused import, but it is unused import according to unimport.
            # CASE 1
            from codeop import compile_command
            compile_command
            """,
            """\
            # This is not unused import, but it is unused import according to unimport.
            # CASE 1
            from codeop import compile_command
            compile_command
            """,
        )

    def test_star(self):
        self.assertActionAfterRefactorEqualToAction(
            """\
            from os import *
            walk
            """
        )

    def test_startswith_name(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            import xx
            xxx = "test"
            """,
            """\
            xxx = "test"
            """,
        )

    def test_get_star_imp_none(self):
        self.assertActionAfterRefactorEqualToExpected(
            """\
            try:
                from x import *
            except ImportError:
                pass
            import t
            """,
            """\
            try:
                from x import *
            except ImportError:
                pass
            """,
        )
