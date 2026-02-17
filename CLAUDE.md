# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository.

## Project Overview

Unimport is a Python linter and formatter that detects and removes unused import
statements. It uses `ast` for analysis and `libcst` for refactoring (preserving
formatting). Supports Python 3.9–3.13.

## Common Commands

```bash
# Install for development
pip install -e ".[test]"

# Run all tests
pytest tests -x -v --disable-warnings

# Run a single test file
pytest tests/cases/test_cases.py -x -v

# Run a single test by name
pytest tests -x -v -k "test_name"

# Run with coverage (used by tox)
pytest -vv --cov unimport

# Run the tool itself
unimport [sources]
```

Linting uses pre-commit (black, isort, mypy, docformatter). Line length is 120
characters.

## Architecture

### Pipeline

The core flow is: **parse source → analyze AST → identify unused imports → refactor with
libcst**.

`Main.run()` in `src/unimport/main.py` orchestrates this:

1. `Config` resolves settings from CLI args + config files (pyproject.toml/setup.cfg)
2. `Config.get_paths()` yields Python files matching include/exclude/gitignore rules
3. For each file, `MainAnalyzer.traverse()` parses and analyzes the AST
4. `Import.get_unused_imports()` returns unused imports from class-level state
5. `refactor_string()` uses libcst to produce the cleaned source

### Statement Module (`src/unimport/statement.py`)

Central data model using **class-level mutable state** (important pattern to
understand):

- `Import.imports` (ClassVar list) — all registered imports for current file
- `Name.names` (ClassVar list) — all registered name usages for current file
- `Scope.scopes` / `Scope.current_scope` (ClassVar lists) — scope tracking

These are populated during analysis and cleared via `MainAnalyzer.clear()` after each
file. The `MainAnalyzer` context manager handles this lifecycle.

### Analyzers (`src/unimport/analyzers/`)

Three AST visitors run in sequence during `MainAnalyzer.traverse()`:

1. **`NameAnalyzer`** — collects all name usages (identifiers, attributes, type
   comments, string annotations)
2. **`ImportableNameWithScopeAnalyzer`** — collects names from `__all__` definitions
   (for star import suggestions)
3. **`ImportAnalyzer`** — collects import statements, handles `if`/`try` dispatch,
   generates star import suggestions

### Refactoring (`src/unimport/refactor.py`)

Uses `libcst` with `_RemoveUnusedImportTransformer` (a `CSTTransformer` with
`PositionProvider` metadata) to surgically remove unused imports while preserving
formatting.

### Commands (`src/unimport/commands/`)

CLI actions: `check` (report), `diff` (show changes), `remove` (apply changes),
`permission` (interactive prompt). The `--remove` and `--permission` options are
mutually exclusive.

### Config (`src/unimport/config.py`)

Auto-discovers `setup.cfg` or `pyproject.toml` (under `[tool.unimport]`). Config keys
support both underscore (`include_star_import`) and hyphen (`include-star-import`)
forms.

## Test Structure

Tests in `tests/cases/` use a **three-directory convention**:

- `tests/cases/source/<category>/<case>.py` — input Python source
- `tests/cases/analyzer/<category>/<case>.py` — expected analysis results (`NAMES`,
  `IMPORTS`, `UNUSED_IMPORTS` lists)
- `tests/cases/refactor/<category>/<case>.py` — expected output after refactoring

`test_cases.py` parametrizes over all source files and validates both analysis and
refactoring. To add a new test case, create matching files in all three directories.

The `# unimport: skip_file` comment in source files tells unimport to skip analysis.
