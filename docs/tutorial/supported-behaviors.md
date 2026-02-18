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

## Subpackage Imports

`import a.b` binds `a` in the namespace, so any reference to `a.*` relies on that
import. Unimport recognizes this and won't remove a subpackage import when its root
package is used in the code.

```python
import urllib.request

def parse_url(url):
    return urllib.parse.urlparse(url)
```

In this example, `import urllib.request` is kept because removing it would remove
`urllib` from the namespace, breaking the `urllib.parse.urlparse()` call.

However, when a more specific import exists, unimport correctly identifies the redundant
one:

**input**

```python
import urllib.request
import urllib.parse

urllib.parse.urlparse('http://example.com')
```

**output**

```python
import urllib.parse

urllib.parse.urlparse('http://example.com')
```

Here `import urllib.parse` directly provides the needed namespace, so
`import urllib.request` is correctly flagged as unused.

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

### Deferred Execution

Function and async function bodies are deferred — they only execute when called. So a
module-level import that appears textually after a function definition is still
available when the function runs. Unimport understands this and won't remove such
imports.

```python
def bob():
    print(sys.path)

import sys  # kept: sys is available when bob() is called
```

This applies to regular functions, async functions, nested functions, and methods:

```python
async def fetch():
    return aiohttp.get(url)

import aiohttp  # kept
```

Class bodies execute immediately (not deferred), so the lineno check still applies:

```python
class Foo:
    x = sys.platform

import sys  # removed: class body runs before this import
```
