import textwrap

from unimport.analyzer import Analyzer
from unimport.statement import Import, ImportFrom, Name


def test_union_import():
    source = """\
        import typing
        if typing.TYPE_CHECKING:
           from PyQt5.QtWebEngineWidgets import QWebEngineHistory
           from PyQt5.QtWebKit import QWebHistory

        HistoryType = typing.Union['QWebEngineHistory', 'QWebHistory']
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="typing.TYPE_CHECKING"),
            Name(lineno=6, name="HistoryType"),
            Name(lineno=6, name="QWebEngineHistory"),
            Name(lineno=6, name="QWebHistory"),
            Name(lineno=6, name="typing.Union"),
        ]
        assert Import.imports == [
            Import(
                lineno=1,
                column=1,
                name="typing",
                package="typing",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebEngineHistory",
                package="PyQt5.QtWebEngineWidgets",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="QWebHistory",
                package="PyQt5.QtWebKit",
                star=False,
                suggestions=[],
            ),
        ]


def test_union_from():
    source = """\
        from typing import TYPE_CHECKING, Union
        if TYPE_CHECKING:
           from PyQt5.QtWebEngineWidgets import QWebEngineHistory
           from PyQt5.QtWebKit import QWebHistory

        HistoryType = Union['QWebEngineHistory', 'QWebHistory']
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="TYPE_CHECKING"),
            Name(lineno=6, name="HistoryType"),
            Name(lineno=6, name="QWebEngineHistory"),
            Name(lineno=6, name="QWebHistory"),
            Name(lineno=6, name="Union"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="TYPE_CHECKING",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="Union",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebEngineHistory",
                package="PyQt5.QtWebEngineWidgets",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="QWebHistory",
                package="PyQt5.QtWebKit",
                star=False,
                suggestions=[],
            ),
        ]


def test_union_attribute():
    source = """\
        from typing import TYPE_CHECKING, Union
        if TYPE_CHECKING:
           from PyQt5 import QtWebEngineWidgets
           from PyQt5 import QtWebKit

        HistoryType = Union['QtWebEngineWidgets.QWebEngineHistory', 'QtWebKit.QWebHistory']
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="TYPE_CHECKING"),
            Name(lineno=6, name="HistoryType"),
            Name(lineno=6, name="QtWebEngineWidgets.QWebEngineHistory"),
            Name(lineno=6, name="QtWebKit.QWebHistory"),
            Name(lineno=6, name="Union"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="TYPE_CHECKING",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=1,
                column=2,
                name="Union",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QtWebEngineWidgets",
                package="PyQt5",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=4,
                column=1,
                name="QtWebKit",
                package="PyQt5",
                star=False,
                suggestions=[],
            ),
        ]


def test_cast_import():
    source = """\
        import typing
        if typing.TYPE_CHECKING:
           from PyQt5.QtWebKit import QWebHistory

        HistoryType = typing.cast('QWebHistory', None)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="typing.TYPE_CHECKING"),
            Name(lineno=5, name="HistoryType"),
            Name(lineno=5, name="QWebHistory"),
            Name(lineno=5, name="typing.cast"),
        ]
        assert Import.imports == [
            Import(
                lineno=1,
                column=1,
                name="typing",
                package="typing",
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebHistory",
                package="PyQt5.QtWebKit",
                star=False,
                suggestions=[],
            ),
        ]


def test_cast_from():
    source = """\
        from typing import TYPE_CHECKING
        if TYPE_CHECKING:
           from PyQt5.QtWebKit import QWebHistory

        HistoryType = cast('QWebHistory', return_value)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="TYPE_CHECKING"),
            Name(lineno=5, name="HistoryType"),
            Name(lineno=5, name="QWebHistory"),
            Name(lineno=5, name="cast"),
            Name(lineno=5, name="return_value"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="TYPE_CHECKING",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QWebHistory",
                package="PyQt5.QtWebKit",
                star=False,
                suggestions=[],
            ),
        ]


def test_cast_attribute():
    source = """\
        from typing import TYPE_CHECKING
        if TYPE_CHECKING:
           from PyQt5 import QtWebKit

        HistoryType = cast('QtWebKit.QWebHistory', return_value)
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=2, name="TYPE_CHECKING"),
            Name(lineno=5, name="HistoryType"),
            Name(lineno=5, name="QtWebKit.QWebHistory"),
            Name(lineno=5, name="cast"),
            Name(lineno=5, name="return_value"),
        ]
        assert Import.imports == [
            ImportFrom(
                lineno=1,
                column=1,
                name="TYPE_CHECKING",
                package="typing",
                star=False,
                suggestions=[],
            ),
            ImportFrom(
                lineno=3,
                column=1,
                name="QtWebKit",
                package="PyQt5",
                star=False,
                suggestions=[],
            ),
        ]
