You can list many options by running unimport --help

```bash
usage: unimport [-h] [--color {auto,always,never}] [--check] [--format {text,json}] [-c PATH] [--disable-auto-discovery-config] [--include include] [--exclude exclude] [--gitignore] [--ignore-init]
                [--include-star-import] [-d] [-j N] [-r | -p] [-v]
                [sources ...]

A linter, formatter for finding and removing unused import statements.

positional arguments:
  sources               Files and folders to find the unused imports.

options:
  -h, --help            show this help message and exit
  --color {auto,always,never}
                        Select whether to use color in the output. Defaults to `auto`.
  --check               Prints which file the unused imports are in.
  --format {text,json}  Output format. `json` prints one JSON document for tools and implies --check. Defaults to `text`.
  -c PATH, --config PATH
                        Read configuration from PATH.
  --disable-auto-discovery-config
                        Automatically pick up config options from setup.cfg if it is present in the project root else check and if it exists use pyproject.toml.
  --include include     File include pattern.
  --exclude exclude     File exclude pattern.
  --gitignore           Exclude .gitignore patterns. if present.
  --ignore-init         Ignore the __init__.py file.
  --include-star-import
                        Include star imports during scanning and refactor.
  -d, --diff            Prints a diff of all the changes unimport would make to a file.
  -j N, --jobs N        Number of processes to analyze files in parallel; 0 uses all CPUs. Defaults to `1`.
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

> (optional: default `False`) Prints which file the unused imports are in.

**Usage**

- `$ unimport`
- `$ unimport --check`
- `$ unimport --check --diff`
- `$ unimport --check --remove`

---

## Format

> (optional: default `text`) choices: (text, json)

`json` prints one JSON document instead of text lines, for editors, CI annotations and
other tools. It implies `--check` and can't be combined with `--diff`, `--remove` or
`--permission`.

```json
{
  "unused_imports": [
    {
      "path": "src/app.py",
      "line": 1,
      "name": "os",
      "package": "os",
      "star": false,
      "suggestions": []
    }
  ],
  "errors": [
    { "path": "src/broken.py", "message": "invalid syntax (<unknown>, line 1)" }
  ]
}
```

**Usage**

- `$ unimport --format json`

---

## Config

> (optional: default `the file directory you are in`) -> `Path(".")`

Read configuration from PATH

**Usage**

- `$ unimport --config path/to/pyproject.toml`

---

## Disable auto discovery config

> (optional: default `False`)

Automatically pick up config options from setup.cfg if it is present in the project root
else check and if it exists use pyproject.toml.

**Usage**

- `$ unimport --disable-auto-discovery-config`

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
Windows. For more information, please visit ->
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

## Jobs

> (optional: default `1`) Number of processes used to analyze files in parallel.

Unimport's work is CPU-bound, so on large projects running several processes makes it
noticeably faster. `0` uses one process per CPU. Output is printed in the same order as
a sequential run, and files are changed by the main process only.

`--permission` asks for confirmation file by file, so it always runs with a single
process. For a handful of files, starting processes can cost more than it saves.

**Usage**

- `$ unimport -j 4`
- `$ unimport --jobs 0`

---

## Remove

> (optional: default `False`) remove unused imports automatically.

When the `--diff` and `--check` flags are not used, the `--remove` flag set as `True` If
you still want to remove the imports, use the `--remove` flag.

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
