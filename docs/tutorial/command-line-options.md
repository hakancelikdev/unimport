You can list many options by running unimport --help

```bash
usage: unimport [-h] [--color {auto,always,never}] [--check] [-c PATH]
                    [--include include] [--exclude exclude] [--gitignore]
                    [--ignore-init] [--include-star-import] [-d] [-r | -p] [-v]
                    [sources [sources ...]]

    A linter, formatter for finding and removing unused import statements.

    positional arguments:
      sources               Files and folders to find the unused imports.

    optional arguments:
      -h, --help            show this help message and exit
      --color {auto,always,never}
                            Select whether to use color in the output. Defaults to
                            `auto`.
      --check               Prints which file the unused imports are in.
      -c PATH, --config PATH
                            Read configuration from PATH.
      --include include     File include pattern.
      --exclude exclude     File exclude pattern.
      --gitignore           Exclude .gitignore patterns. if present.
      --ignore-init         Ignore the __init__.py file.
      --include-star-import
                            Include star imports during scanning and refactor.
      -d, --diff            Prints a diff of all the changes unimport would make
                            to a file.
      -r, --remove          Remove unused imports automatically.
      -p, --permission      Refactor permission after see diff.
      -v, --version         Prints version of unimport

    Get rid of all unused imports 🥳
```

---

## Sources

> (optional: default `the file directory you are in`) -> `Path(".")`

You can give as many file or directory paths as you want.

**Usage**

- `$ unimport`
- `$ unimport example`
- `$ unimport example example1 example2 example/example.py`

---

## Check

> (optional: default `True`) Prints which file the unused imports are in.

When the `--diff`, `--permission` and `--remove` flags are used, the `--check` flag set
as `False` If you still want to see the results, use the `--check` flag.

**Usage**

- `$ unimport`
- `$ unimport --check`
- `$ unimport --check --diff`
- `$ unimport --check --remove`

---

## Config

> (optional: default `the file directory you are in`) -> `Path(".")`

Read configuration from PATH

**Usage**

- `$ unimport --config path/to/pyproject.toml`

---

## Include

> (optional: default '\\.(py)$') file include pattern

**Usage**

- `$ unimport --include mypackage`
- `$ unimport --include "mypackage|tests`

---

## Exclude

> (optional: default '^$') file exclude pattern

**Usage**

- `$ unimport --exclude __init__.py`
- `$ unimport --exclude "__init__.py|tests|.tox`

---

## Gitignore

> (optional: default `False`)

It's possible to skip `.gitignore` glob patterns.

**Usage**

- `$ unimport --gitignore`

**Warning:**

For more accurate results when using `--gitignore` parameter, please do not use Python
3.6 and Windows. For more information, please visit ->
https://github.com/hakancelikdev/unimport/issues/240

---

## Ignore init

> (optional: default `False`)

Ignore the **init**.py file.

**Usage**

- `$ unimport --ignore-init`

---

## Include star import

> (optional: default `False`) Include star imports during scanning and refactor.

**Usage**

- `$ unimport --include-star-import`

---

## Diff

> (optional: default `False`) Prints a diff of all the changes unimport would make to a
> file.

**Usage**

- `$ unimport -d`
- `$ unimport --diff`

---

## Remove

> (optional: default `False`) remove unused imports automatically.

**Usage**

- `$ unimport -r`
- `$ unimport --remove`

---

## Permission

> (optional: default `False`) Refactor permission after seeing the diff.

**Usage**

- `$ unimport -p`
- `$ unimport --permission`

---

## Color

> (optional: default `auto`) choices: (always, never, auto)

Select whether to use color in the output.

**Usage**

- `unimport --color always`
- `unimport --color never`
- `unimport --color auto`
