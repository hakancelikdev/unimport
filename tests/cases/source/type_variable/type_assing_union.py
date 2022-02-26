from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
   from PyQt5 import QtWebEngineWidgets, QtWebKit


HistoryType = Union['QtWebEngineWidgets.QWebEngineHistory', 'QtWebKit.QWebHistory']

