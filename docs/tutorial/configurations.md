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
