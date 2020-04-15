![unimport](https://raw.githubusercontent.com/hakancelik96/unimport/master/images/logo/Unimport.png)

**A python CLI library to detect or auto remove unused Python imports.**

[![MIT License](https://img.shields.io/github/license/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/blob/master/LICENSE) [![releases](https://img.shields.io/github/release/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/releases) [![last-commit](https://img.shields.io/github/last-commit/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/commits/master) [![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black) [![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort) [![style](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport) [![](https://img.shields.io/github/contributors/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/graphs/contributors) [![](https://pepy.tech/badge/unimport)](https://pepy.tech/badge/unimport) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unimport)

### Installation and Usage
## Installation
Unimport can be installed by running `pip install unimport`. It requires Python 3.6.0+ to run.

## Usage

`unimport {source_file_or_directory}` or write just `unimport` to scan current path.

## Command line options
You can list many options by running unimport --help

```
usage: unimport [-h] [-c PATH] [-r | -p] [-d] [--check] [-v] [sources [sources ...]]

Detect or remove unused Python imports.

positional arguments:
  sources               files and folders to find the unused imports.

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --config PATH
                        read configuration from PATH.
  -r, --remove          remove unused imports automatically.
  -p, --permission      Refactor permission after see diff.
  -d, --diff            Prints a diff of all the changes unimport would make to a file.
  --check               Prints which file the unused imports are in.
  -v, --version         Prints version of unimport
```


**Please insert this badge into your project**

`[![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)`

[![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)

## Configuring Unimport
It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if you have.

If you want to use `pyproject.toml` to configure, you must to install it.
Try this; `pip install toml==0.10.0`

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

## 🤝 [CONTRIBUTING.md](https://github.com/hakancelik96/unimport/blob/master/CONTRIBUTING.md) 🤝

[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/0)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/0)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/1)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/1)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/2)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/2)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/3)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/3)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/4)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/4)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/5)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/5)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/6)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/6)[![](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/images/7)](https://sourcerer.io/fame/hakancelik96/hakancelik96/unimport/links/7)

## Author / Social

👤 **Hakan Çelik** 👤

- [![](https://img.shields.io/twitter/follow/hakancelik96?style=social)](https://twitter.com/hakancelik96)
- [![](https://img.shields.io/github/followers/hakancelik96?label=hakancelik96&style=social)](https://github.com/hakancelik96)

## Who's using Unimport?

[![radity.com](https://raw.githubusercontent.com/hakancelik96/unimport/master/images/clients/radity.jpg)](https://radity.com/?ref=unimport)
