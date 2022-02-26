import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, ImportFrom, Name


def test_comma():
    source = """\
        from os import (
            waitpid,
            scandir,
        )
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="waitpid",
                package="os",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="scandir",
                package="os",
                star=False,
                suggestions=[],
            ),
        ]


def test_module_used():
    source = """\
        from pathlib import Path
        CURRENT_DIR = Path(".").parent
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="Path",
                package="pathlib",
                star=False,
                suggestions=[],
            )
        ]
        assert Name.names == [
            Name(lineno=2, name="CURRENT_DIR", is_all=False),
            Name(lineno=2, name="Path", is_all=False),
        ]
        assert list(Import.get_unused_imports()) == []


def test_module_unused():
    source = """\
        from pathlib import Path
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                suggestions=[],
                name="Path",
                package="pathlib",
                star=False,
            ),
        ]


def test_unknown_module_used():
    source = """\
        import x.y
        CURRENT_DIR = x.y(".").parent
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            Import(lineno=1, column=1, name="x.y", package="x.y")
        ]
        assert list(Import.get_unused_imports()) == []


def test_unknown_module_unused():
    source = """\
        import x.y
        import d.f.a.s
        CURRENT_DIR = x.y(".").parent
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            Import(
                lineno=2,
                column=1,
                name="d.f.a.s",
                package="d.f.a.s",
            ),
        ]


def test_import_in_function():
    source = """\
        import t
        from x import y, z

        def function(f=t):
            import x
            return f
        from i import t, ii
        print(t)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == [
            ImportFrom(
                lineno=7,
                column=2,
                name="ii",
                package="i",
                star=False,
                suggestions=[],
            ),
            Import(lineno=5, column=1, name="x", package="x"),
            ImportFrom(
                lineno=2,
                column=2,
                name="z",
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
        ]


def test_import_after_usage():
    source = """\
        def function():
            print(os)
            import os
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Import.imports == [
            Import(lineno=3, column=1, name="os", package="os")
        ]


def test_double_underscore_builtins_names():
    source = """\
        from globals import (
            __name__, __doc__, __package__,
           __loader__, __spec__, __annotations__,
           __builtins__
        )
        __name__, __doc__, __package__,
        __loader__, __spec__, __annotations__,
        __builtins__
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert list(Import.get_unused_imports()) == []
