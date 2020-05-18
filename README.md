![unimport](https://raw.githubusercontent.com/hakancelik96/unimport/master/images/logo/Unimport.png)

**A linter & formatter for finding & removing unused import statements.**

[![MIT License](https://img.shields.io/github/license/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/blob/master/LICENSE)
[![releases](https://img.shields.io/github/release/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/releases)
[![last-commit](https://img.shields.io/github/last-commit/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/commits/master)
[![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black)
[![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort)
[![style](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)
[![](https://img.shields.io/github/contributors/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/graphs/contributors)
[![](https://pepy.tech/badge/unimport)](https://pepy.tech/badge/unimport)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unimport)

## Getting Started

---

**Contents:** **[Installation and Usage](#installation-and-usage)** |
**[Command line options](#command-line-options)** |
**[Configuring Unimport](#configuring-unimport)** |
**[Adding pre-commit plugins to your project](#adding-pre-commit-plugins-to-your-project)**
| **[Our badge](#our-badge-)** | **[CONTRIBUTING](#-contributingmd-)** |
**[CHANGELOG.md](#changelogmd)** | **[Author / Social](#author--social)** |
**[Who's using Unimport?](#whos-using-unimport)**

---

## Installation and Usage

### Installation

Unimport requires Python 3.6+ and can be easily installed using most common Python
packaging tools. We recommend installing the latest stable release from PyPI with pip:

```
pip install unimport
```

### Usage

```
$ unimport [sources [sources ...]]
```

_If you do not get any output, congratulations means there is no unused import in your
project._

#### Let's with example with simple a Python code.

**example.py**

```python
import t
from l import t
from x import y, z, t

def function(f=t):
    import x
    return f

from i import t, ii

print(t)
```

```bash
$ unimport example.py

t at example.py:1
t at example.py:2
y at example.py:3
z at example.py:3
x at example.py:6
ii at example.py:9
```

**-d ( diff ) command**

```python
$ unimport example.py -d
--- example.py

+++

@@ -1,11 +1,8 @@

-import t
-from l import t
-from x import y, z, t
+from x import t

 def function(f=t):
-    import x
     return f

-from i import t, ii
+from i import t

print(t)
```

**-p ( permission ) command**

```python
$ unimport example.py -p
--- example.py

+++

@@ -1,11 +1,8 @@

-import t
-from l import t
-from x import y, z, t
+from x import t

 def function(f=t):
-    import x
     return f

-from i import t, ii
+from i import t

 print(t)
Apply suggested changes to 'example.py' [y/n/q] ? >
```

**and -r ( remove ) command**

`$ unimport example.py -r`

```python
from x import t

def function(f=t):
    return f

from i import t

print(t)
```

**Star Import** If you want to include star imports during scanning and refactor. Use
command as follow. ``\$ unimport example.py --include-star-import`

**Rare Cases** We add skip import feature to rare cases import statements.

Leave '#unimport: skip' at the end of the line to skip imports with some rare cases.
**for example:**

```python
try:
  import django #unimport:skip
except ImportError:
  print("install django")
```

## Command line options

You can list many options by running unimport --help

```
usage: unimport [-h] [-c PATH] [--include-star-import] [-d] [-r | -p] [--check] [-v] [sources [sources ...]]

A python CLI library to detect and auto remove unused Python imports by doing static code analysis.

positional arguments:
  sources               files and folders to find the unused imports.

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --config PATH
                        read configuration from PATH.
  --include-star-import
                        Include star imports during scanning and refactor.
  -d, --diff            Prints a diff of all the changes unimport would make to a file.
  -r, --remove          remove unused imports automatically.
  -p, --permission      Refactor permission after see diff.
  --check               Prints which file the unused imports are in.
  -v, --version         Prints version of unimport
```

## Configuring Unimport

It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if
you have.

If you want to use `pyproject.toml` to configure, you must to install it. Try this;
`pip install toml==0.10.0`

Use `exclude` config name to configure glob patterns for exluding files and folders.

For example:

**pyproject.toml**

```ini
[tool.unimport]
exclude = ["tests*", "**/__init__.py"]
```

**setup.cfg**

```ini
[unimport]
exclude =  **/__init__.py
           tests*
```

## Adding pre-commit plugins to your project

Once you have [pre-commit](https://pre-commit.com/)
[installed](https://pre-commit.com/#install), adding pre-commit plugins to your project
is done with the .pre-commit-config.yaml configuration file.

Add a file called .pre-commit-config.yaml to the root of your project. The pre-commit
config file describes what repositories and hooks are installed.

```yaml
repos:
  - repo: https://github.com/hakancelik96/unimport
    rev: v0.2.6
    hooks:
      - id: unimport
        args: [-r]
```

## Our badge [![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)

**Please insert this badge into your project**

`[![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)`

## 🤝 [CONTRIBUTING.md](/CONTRIBUTING.md) 🤝

[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/0)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/0)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/1)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/1)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/2)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/2)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/3)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/3)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/4)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/4)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/5)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/5)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/6)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/6)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/7)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/7)

## [CHANGELOG.md](/CHANGELOG.md)

All notable changes to this project will be documented in this file.

## Author / Social

👤 **Hakan Çelik** 👤

- [![](https://img.shields.io/twitter/follow/hakancelik96?style=social)](https://twitter.com/hakancelik96)
- [![](https://img.shields.io/github/followers/hakancelik96?label=hakancelik96&style=social)](https://github.com/hakancelik96)

## Who's using Unimport?

[![radity.com](https://raw.githubusercontent.com/hakancelik96/unimport/master/images/clients/radity.jpg)](https://radity.com/?ref=unimport)
