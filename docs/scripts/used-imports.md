## How to find used imports in my project.

```python
from pathlib import Path
from unimport.session import Session

project_path = "unimport/"  # write the path of your own project

modules = set()
session = Session()
for path in session.list_paths(Path(project_path)):
    try:
        source = session.read(path)[0]
    except SyntaxError:
        continue
    session.scanner.run_visit(source)
    import_names = set(session.scanner.import_names)
    unused_imp_names = {imp["name"] for imp in session.scanner.unused_imports}
    session.scanner.clear()
    used_imports =  import_names - unused_imp_names
    modules.update(used_imports)

print(modules)

# Output
# {'cast', 'Iterable', 'TYPE_IMPORT', 'refactor_string', 'TYPE_NAME', 'inspect', 'importlib',
# 'configparser', 'Iterator', 'difflib', '__version__', 'Optional', 'Union', 'ast', 'TypeVar', '__description__',
# 'Scanner', 'Session', 'builtins', 'Path', 'TYPE_CHECKING', 'List', 'CodeRange',
# 'first_occurrence', 'sys', 'PositionProvider', 'get_parents', 'CONFIG_FILES',
# 'tokenize', 'ModuleType', 'MetadataWrapper', 'io', 'Callable', 'RemovalSentinel',
# 're', 'cst', 'Color', 'contextlib', 'Tuple', 'Any', 'relate', 'argparse', 'TypedDict', 'Config', 'functools'}
```
