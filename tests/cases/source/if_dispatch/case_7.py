from qtpy import QtCore
import typing as t

if t.TYPE_CHECKING:
    from PySide6 import QtCore


class MyThread(QtCore.QThread):
    pass
