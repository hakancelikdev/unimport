## Typing

Unimport can understand that imports are used these cases.

```python
from typing import List, Dict


def test(arg: List[Dict]) -> None:
   pass
```

---

#### String

Unimport supports the following cases

```python
from typing import List, Dict


def test(arg: 'List[Dict]') -> None:
   pass
```

```python
from typing import List, Dict


def test(arg: "List['Dict']") -> None:
   pass
```

---

#### Comments

Imports in the example below aren't flag as unused by unimport.

```python
from typing import Any
from typing import Tuple
from typing import Union


def function(a, b):
    # type: (Any, str) -> Union[Tuple[None, None], Tuple[str, str]]
    pass
```

For more information

[PEP 526 - Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/)

---

#### TYPE_CHECKING

Unimport recognizes `if TYPE_CHECKING:` blocks and skips imports inside them. These
imports only run during static analysis and are not available at runtime, so they should
never shadow or conflict with runtime imports.

```python
from qtpy import QtCore
import typing as t

if t.TYPE_CHECKING:
    from PySide6 import QtCore

class MyThread(QtCore.QThread):
    pass
```

In this example, unimport correctly keeps `from qtpy import QtCore` (the runtime import)
and ignores the `TYPE_CHECKING`-guarded import. Both `if TYPE_CHECKING:` and
`if typing.TYPE_CHECKING:` (or any alias like `if t.TYPE_CHECKING:`) are supported.

---

## All

Unimport looks at the items in the `__all__` list, if it matches the imports, marks it
as being used.

```python
import os

__all__ = ["os"] # this import is used and umimport can understand
```

Other supported operations, **append** and **extend**

```python
from os import *


__all__ = []
__all__.append("removedirs")
__all__.extend(["walk"])
```

after refactoring

```python
from os import removedirs, walk


__all__ = []
__all__.append("removedirs")
__all__.extend(["walk"])
```

---

## Scope

Unimport tries to better understand whether the import is unused by performing scope
analysis.

Let me give a few examples.

**input**

```python
import x


def func():
    import x

    def inner():
        import x
        x

```

**output**

```python
def func():

    def inner():
        import x
        x
```

**input**

```python
import x


class Klass:

  def f(self):
      import x

      def ff():
        import x

        x
```

**output**

```python

class Klass:

  def f(self):

      def ff():
        import x

        x
```
