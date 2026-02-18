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

## Star Import

When used with `--include-star-import`, unimport can refactor star imports into explicit
imports by detecting which names are actually used in the code.

**input**

```python
from os import *
from json import *

print(getcwd())
print(JSONEncoder)
```

**output**

```python
from os import getcwd
from json import JSONEncoder

print(getcwd())
print(JSONEncoder)
```

#### Duplicate Name Resolution

When multiple star imports export the same name, unimport deduplicates suggestions so
that only the last import provides each name (matching Python's shadowing semantics).
This produces correct output in a single pass.

**input**

```python
from _collections import *
from collections import *

print(defaultdict)
```

**output**

```python
from collections import defaultdict

print(defaultdict)
```

If the star imports partially overlap, each import keeps only its unique names:

**input**

```python
from collections import *
from _collections import *

print(Counter)
print(defaultdict)
```

**output**

```python
from collections import Counter
from _collections import defaultdict

print(Counter)
print(defaultdict)
```

Star import suggestions also respect explicit imports — if a name already has an
explicit import, star imports won't produce a duplicate for that name.

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
