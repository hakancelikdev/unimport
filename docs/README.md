## Get Started

![unimport](https://raw.githubusercontent.com/hakancelik96/unimport/master/images/logo/Unimport.png ":size=60%")

**A linter, formatter for finding and removing unused import statements.**

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/hakancelik96/unimport/master.svg)](https://results.pre-commit.ci/latest/github/hakancelik96/unimport/master)
![test](https://github.com/hakancelik96/unimport/workflows/Test/badge.svg)

[![Pypi](https://img.shields.io/pypi/v/unimport)](https://pypi.org/project/unimport/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unimport)
[![Downloads](https://static.pepy.tech/personalized-badge/unimport?period=total&units=none&left_color=grey&right_color=red&left_text=downloads)](https://pepy.tech/project/unimport)
[![License](https://img.shields.io/github/license/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/blob/master/LICENSE)

[![Forks](https://img.shields.io/github/forks/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/fork)
[![Issues](https://img.shields.io/github/issues/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/issues)
[![Stars](https://img.shields.io/github/stars/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/stargazers)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3fbd4686e97b4e19906ca2fa933e4cfc)](https://app.codacy.com/manual/hakancelik96/unimport?utm_source=github.com&utm_medium=referral&utm_content=hakancelik96/unimport&utm_campaign=Badge_Grade_Settings)
[![Codecov](https://codecov.io/gh/hakancelik96/unimport/branch/master/graph/badge.svg)](https://codecov.io/gh/hakancelik96/unimport)
[![Contributors](https://img.shields.io/github/contributors/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/commits/master)

## Installation and Usage

### Installation

Unimport requires Python 3.6+ and can be easily installed using most common Python
packaging tools. We recommend installing the latest stable release from PyPI with pip:

```shell
$ pip install unimport
```

## `sources`

> (optional: default `the file directory you are in`) -> `Path(".")`

You can give as many file or directory paths as you want.

### Usage

- `$ unimport`
- `$ unimport example`
- `$ unimport example example1 example2 example/example.py`

## Check

> (optional: default `True`) Prints which file the unused imports are in.

When the `--diff`, `--permission` and `--remove` flags are used, the `--check` flag set
as `False` If you still want to see the results, use the `--check` flag.

### Usage

- `$ unimport example.py`
- `$ unimport example.py --check`
- `$ unimport example.py --diff --check`
- `$ unimport example.py --check --diff --remove`

## Diff

> (optional: default `False`) Prints a diff of all the changes unimport would make to a
> file.

### Usage

- `$ unimport example.py -d`
- `$ unimport example.py --diff`

## Permission

> (optional: default `False`) Refactor permission after seeing the diff.

### Usage

- `$ unimport example.py -p`
- `$ unimport example.py --permission`

## Remove flag

> (optional: default `False`) remove unused imports automatically.

#### Usage

- `$ unimport example.py -r`
- `$ unimport example.py --remove`

## Include star import

> (optional: default `False`) Include star imports during scanning and refactor.

## Gitignore

> (optional: default `False`)

It's possible to skip `.gitignore` glob patterns using `--gitignore` flag.

## Requirements

> (optional: default `False`)

You can automatically delete unused modules from the requirements.txt file
(`unimport --requirements --remove`), see the difference (
`unimport --requirements --diff`), delete it by requesting permission (
`unimport --requirements --permission`), or just check ( `unimport --requirements`).

## Include

> (optional: default '\\.(py)$') file include pattern

### Usage

- `$ unimport --include mypackage`
- `$ unimport --include "mypackage|tests`

## Exclude

> (optional: default '^$') file exclude pattern

### Usage

- `$ unimport --exclude __init__.py`
- `$ unimport --exclude "__init__.py|tests|.tox`

## Typing

Unimport can understand that imports are used these cases.

```python
from typing import List, Dict
def test(arg: List[Dict]) -> None:
   pass
```

### String

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

### Comments

**This feature is only available for python 3.8.**

Imports in the example below aren't flag as unused by import.

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

## Skip Import

Leave '# unimport: skip' or '# noqa' at the end of the line to skip imports **for
example:**

```python
import x # unimport:skip
```

```python
from x import ( # noqa
  t, y,
  f, r
)
```

**If version of your python is 3.8+** Unimport support multiple skip like below. _It
doesn't matter which line you put the comment on._

```python
from package import (
    module,
    module1,
)  # unimport:skip
```

or

```python
from package import (
    module, # unimport:skip
    module1,
)
```

## File Wide Skips

To skip a file by typing `# unimport: skip_file` anywhere in that file **for example:**

```python
# unimport: skip_file

import x

```

or

```python
import x

# unimport: skip_file

```

## `__all__`

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

## Command line options

You can list many options by running unimport --help

```
usage: unimport [-h] [-c PATH] [--include include] [--exclude exclude] [--gitignore] [--include-star-import] [-d] [-r | -p]
                [--requirements] [--check] [-v]
                [sources [sources ...]]

A linter, formatter for finding and removing unused import statements.

positional arguments:
  sources               files and folders to find the unused imports.

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --config PATH
                        read configuration from PATH.
  --include include     file include pattern.
  --exclude exclude     file exclude pattern.
  --gitignore           exclude .gitignore patterns. if present.
  --include-star-import
                        Include star imports during scanning and refactor.
  -d, --diff            Prints a diff of all the changes unimport would make to a file.
  -r, --remove          remove unused imports automatically.
  -p, --permission      Refactor permission after see diff.
  --requirements        Include requirements.txt file, You can use it with all other arguments
  --check               Prints which file the unused imports are in.
  -v, --version         Prints version of unimport

Get rid of all unused imports 🥳
```

## Configuring Unimport

It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if
you have.

- `exclude` file exclude pattern.
- `include` file include pattern.
- `gitignore` glob exclude patterns.

For example:

**pyproject.toml**

```ini
[tool.unimport]
sources = ["path1", "path2"]
exclude = '__init__.py|tests/'
include = 'test|test2|tests.py'
gitignore = true
requirements = true
remove = false
diff = true
include_star_import = true
```

**setup.cfg**

```ini
[unimport]
sources = ["path1", "path2"]
exclude = __init__.py|tests/
include = test|test2|tests.py
gitignore = true
requirements = true
remove = false
diff = true
include_star_import = true
```

**When reading your configurations, it gives priority to the configurations you enter
from the console.**

## Adding pre-commit plugins to your project

Once you have [pre-commit](https://pre-commit.com/)
[installed](https://pre-commit.com/#install), adding pre-commit plugins to your project
is done with the .pre-commit-config.yaml configuration file.

Add a file called .pre-commit-config.yaml to the root of your project. The pre-commit
config file describes what repositories and hooks are installed.

```yaml
repos:
  - repo: https://github.com/hakancelik96/unimport
    rev: stable
    hooks:
      - id: unimport
        args: [--remove, --requirements, --include-star-import]
```
