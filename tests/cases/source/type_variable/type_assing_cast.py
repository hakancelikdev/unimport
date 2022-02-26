from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from PyQt5 import QtWebKit


HistoryType = cast('QtWebKit.QWebHistory', return_value)

