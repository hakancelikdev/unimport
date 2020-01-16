<p align="center">
  <img src="https://raw.githubusercontent.com/hakancelik96/unimport/master/images/logo/Unimport.png">
  </p>
<p align="center">
  Detect or remove unused Python imports.
 </p>
 
[![MIT License](https://img.shields.io/github/license/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/blob/master/LICENSE) [![releases](https://img.shields.io/github/release/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/releases) [![last-commit](https://img.shields.io/github/last-commit/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/commits/master) [![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black) [![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort) [![style](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport) [![](https://img.shields.io/github/contributors/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/graphs/contributors) [![](https://pepy.tech/badge/unimport)](https://pepy.tech/badge/unimport) [![codecov](https://codecov.io/gh/hakancelik96/unimport/branch/master/graph/badge.svg)](https://codecov.io/gh/hakancelik96/unimport) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unimport)

### Installation and Usage
## Installation
Unimport can be installed by running `pip install unimport`. It requires Python 3.6.0+ to run.

## Usage

unimport {source_file_or_directory} or write direct unimport to current path scan

## Command line options
You can list many options by running unimport --help

```
usage: __main__.py [-h] [-c PATH] [-r | -p] [-d] [--check] [-v]
                   [sources [sources ...]]

Detect or remove unused Python imports.

positional arguments:
  sources               files and folders to find the unused imports.

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --config PATH
                        read configuration from PATH.
  -r, --remove          remove unused imports automatically.
  -p, --permission      Refactor permission after see diff.
  -d, --diff            Prints a diff of all the changes unimport would make
                        to a file.
  --check               Prints which file the unused imports are in.
  -v, --version         Prints version of unimport
```


**Please insert this badge into your project**

`[![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)`

[![](https://img.shields.io/badge/style-unimport-red)](https://github.com/hakancelik96/unimport)

## Configuring Unimport
It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if you have.

Use `exclude` config name to configure glob patterns for exluding files and folders.

For example:

**pyproject.toml**

```ini
[tool.unimport]
exclude = [
  './[0-9].*',
  'tests'
]
```

**setup.cfg**

```ini
[unimport]
exclude =  ./[0-9].*
           tests
```

## Author / Social

👤 **Hakan Çelik** 👤

- [![](https://img.shields.io/twitter/follow/hakancelik96?style=social)](https://twitter.com/hakancelik96)
- [![](https://img.shields.io/github/followers/hakancelik96?label=hakancelik96&style=social)](https://github.com/hakancelik96)


## Who's using Unimport?
<table>
  <tr>
    <td align="center">
      <a href="https://radity.com/?ref=unimport">
        <img src="https://raw.githubusercontent.com/hakancelik96/unimport/master/images/clients/radity.jpg" width="160px;" alt="radity.com"/>
        <br/>
        <sub>
          <b>Radity</b>
        </sub>
      </a>
      <br/>
    </td>
  </tr>
</table>
