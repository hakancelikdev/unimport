It's possible to configure **unimport** from `pyproject.toml` or `setup.cfg` files if
you have.

Automatically pick up config options from setup.cfg if it is present in the project root
else check and if it exists use pyproject.toml.

If you want you can disable this feature by passing `--disable-auto-discovery-config` or
you can pass the path to the configuration file by passing
`--config path/to/pyproject.toml`.

For example:

**pyproject.toml**

```ini
[tool.unimport]
sources = ["path1", "path2"]
exclude = '__init__.py|tests/'
include = 'test|test2|tests.py'
gitignore = true
remove = false
check = true
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
remove = false
check = true
diff = true
include_star_import = true
ignore_init = true
```

## Manage like CLI in configuration

```ini
[tool.unimport]
include-star-import = true
ignore-init = true
```

**setup.cfg**

```ini
[unimport]
include-star-import = true
ignore-init = true
```
