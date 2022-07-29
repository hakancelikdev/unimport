## Get Started

![unimport](assets/logo/unimport.png ":size=60%")

**A linter, formatter for finding and removing unused import statements.**

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/hakancelikdev/unimport/main.svg)](https://results.pre-commit.ci/latest/github/hakancelikdev/unimport/main)
![test](https://github.com/hakancelikdev/unimport/workflows/Test/badge.svg)

[![Pypi](https://img.shields.io/pypi/v/unimport)](https://pypi.org/project/unimport/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unimport)
[![Downloads](https://static.pepy.tech/personalized-badge/unimport?period=total&units=international_system&left_color=grey&right_color=red&left_text=downloads)](https://pepy.tech/project/unimport)
[![License](https://img.shields.io/github/license/hakancelikdev/unimport.svg)](https://github.com/hakancelikdev/unimport/blob/main/LICENSE)

[![Forks](https://img.shields.io/github/forks/hakancelikdev/unimport)](https://github.com/hakancelikdev/unimport/fork)
[![Issues](https://img.shields.io/github/issues/hakancelikdev/unimport)](https://github.com/hakancelikdev/unimport/issues)
[![Stars](https://img.shields.io/github/stars/hakancelikdev/unimport)](https://github.com/hakancelikdev/unimport/stargazers)

[![Codecov](https://codecov.io/gh/hakancelikdev/unimport/branch/main/graph/badge.svg)](https://codecov.io/gh/hakancelikdev/unimport)
[![Contributors](https://img.shields.io/github/contributors/hakancelikdev/unimport)](https://github.com/hakancelikdev/unimport/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/hakancelikdev/unimport.svg)](https://github.com/hakancelikdev/unimport/commits/main)

## Installation

Unimport requires Python 3.6+ and can be easily installed using most common Python
packaging tools. We recommend installing the latest stable release from PyPI with pip:

```shell
$ pip install unimport
```

## Sources

> (optional: default `the file directory you are in`) -> `Path(".")`

You can give as many file or directory paths as you want.

**Usage**

- `$ unimport`
- `$ unimport example`
- `$ unimport example example1 example2 example/example.py`

## Check

> (optional: default `True`) Prints which file the unused imports are in.

When the `--diff`, `--permission` and `--remove` flags are used, the `--check` flag set
as `False` If you still want to see the results, use the `--check` flag.

**Usage**

- `$ unimport`
- `$ unimport --check`
- `$ unimport --check --diff`
- `$ unimport --check --remove`

## Config

> (optional: default `the file directory you are in`) -> `Path(".")`

Read configuration from PATH

**Usage**

- `$ unimport --config path/to/pyproject.toml`

## Include

> (optional: default '\\.(py)$') file include pattern

**Usage**

- `$ unimport --include mypackage`
- `$ unimport --include "mypackage|tests`

## Exclude

> (optional: default '^$') file exclude pattern

**Usage**

- `$ unimport --exclude __init__.py`
- `$ unimport --exclude "__init__.py|tests|.tox`

## Gitignore

> (optional: default `False`)

It's possible to skip `.gitignore` glob patterns.

**Usage**

- `$ unimport --gitignore`

## Ignore init

> (optional: default `False`)

Ignore the **init**.py file.

**Usage**

- `$ unimport --ignore-init`

## Include star import

> (optional: default `False`) Include star imports during scanning and refactor.

**Usage**

- `$ unimport --include-star-import`

## Diff

> (optional: default `False`) Prints a diff of all the changes unimport would make to a
> file.

**Usage**

- `$ unimport -d`
- `$ unimport --diff`

## Remove

> (optional: default `False`) remove unused imports automatically.

**Usage**

- `$ unimport -r`
- `$ unimport --remove`

## Permission

> (optional: default `False`) Refactor permission after seeing the diff.

**Usage**

- `$ unimport -p`
- `$ unimport --permission`

## Requirements

> (optional: default `False`)

You can automatically delete unused modules from the requirements.txt file

**Usage**

- `unimport --requirements` to check
- `unimport --check --requirements` to check
- `unimport --requirements --diff` to check and seeing diff
- `unimport --requirements --permission` to refactor permission after seeing the diff.
- `unimport --requirements --remove` to remove automatically.

## Color

> (optional: default `auto`) choices: (always, never, auto)

Select whether to use color in the output.

**Usage**

- `unimport --color always`
- `unimport --color never`
- `unimport --color auto`

## Typing

Unimport can understand that imports are used these cases.

```python
from typing import List, Dict
def test(arg: List[Dict]) -> None:
   pass
```

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

#### Comments

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

## Exit code behavior

Exit code 1 if there is a syntax error Exit code 0 if unused import versa and auto
removed for all other cases exit code 1 Exit code 0 if there is no unused import.

## Command line options

You can list many options by running unimport --help

```
usage: unimport [-h] [--check] [-c PATH] [--color {auto,always,never}] [--include include] [--exclude exclude] [--gitignore] [--ignore-init] [--include-star-import] [-d]
                [-r | -p] [--requirements] [-v]
                [sources ...]

A linter, formatter for finding and removing unused import statements.

positional arguments:
  sources               Files and folders to find the unused imports.

optional arguments:
  -h, --help            show this help message and exit
  --check               Prints which file the unused imports are in.
  -c PATH, --config PATH
                        Read configuration from PATH.
  --color {auto,always,never}
                        Select whether to use color in the output. Defaults to `auto`.
  --include include     File include pattern.
  --exclude exclude     File exclude pattern.
  --gitignore           Exclude .gitignore patterns. if present.
  --ignore-init         Ignore the __init__.py file.
  --include-star-import
                        Include star imports during scanning and refactor.
  -d, --diff            Prints a diff of all the changes unimport would make to a file.
  -r, --remove          Remove unused imports automatically.
  -p, --permission      Refactor permission after see diff.
  --requirements        Include requirements.txt file, You can use it with all other arguments
  -v, --version         Prints version of unimport

Get rid of all unused imports 🥳
```

## Configuring Unimport

It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if
you have.

**When reading your configurations, it gives priority to the configurations you enter
from the console.**

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
ignore_init = true
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
ignore_init = true
```

## Adding pre-commit plugins to your project

Once you have [pre-commit](https://pre-commit.com/)
[installed](https://pre-commit.com/#install), adding pre-commit plugins to your project
is done with the .pre-commit-config.yaml configuration file.

Add a file called .pre-commit-config.yaml to the root of your project. The pre-commit
config file describes what repositories and hooks are installed.

```yaml
repos:
  - repo: https://github.com/hakancelikdev/unimport
    rev: stable
    hooks:
      - id: unimport
        args:
          [--remove, --requirements, --include-star-import, --ignore-init, --gitignore]
```

## Use as a Docker image

Install from the command line:

To use the latest

```
$ docker pull ghcr.io/hakancelikdev/unimport:latest
```

To use the stable

```
$ docker pull ghcr.io/hakancelikdev/unimport:stable
```

To use the other versions

```
$ docker pull ghcr.io/hakancelikdev/unimport:{version_number}
```

For more information see:
https://github.com/hakancelikdev/unimport/pkgs/container/unimport

## Use with Github action

```yaml
name: Unimport
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
      - name: Check unused imports
        uses: hakancelikdev/unimport@stable
        with:
          extra_args: --include src/
```
