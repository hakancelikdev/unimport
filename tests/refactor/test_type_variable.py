from tests.refactor.utils import RefactorTestCase


class TypeVariableTestCase(RefactorTestCase):
    def test_type_assing_union(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebEngineWidgets import QWebEngineHistory
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.Union['QWebEngineHistory', 'QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, Union
                if TYPE_CHECKING:
                   from PyQt5.QtWebEngineWidgets import QWebEngineHistory
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = Union['QWebEngineHistory', 'QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, Union
                if TYPE_CHECKING:
                   from PyQt5 import QtWebEngineWidgets, QtWebKit

                HistoryType = Union['QtWebEngineWidgets.QWebEngineHistory', 'QtWebKit.QWebHistory']

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)

    def test_type_assing_list(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.List['QWebHistory']

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING, List
                if TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = List['QWebHistory']

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)

    def test_type_assing_cast(self):
        actions = [
            (
                """\
                import typing
                if typing.TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = typing.cast('QWebHistory', None)

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING
                if TYPE_CHECKING:
                   from PyQt5.QtWebKit import QWebHistory

                HistoryType = cast('QWebHistory', return_value)

                """
            ),
            (
                """\
                from typing import TYPE_CHECKING
                if TYPE_CHECKING:
                   from PyQt5 import QtWebKit

                HistoryType = cast('QtWebKit.QWebHistory', return_value)

                """
            ),
        ]
        for action in actions:
            self.assertActionAfterRefactorEqualToAction(action)
