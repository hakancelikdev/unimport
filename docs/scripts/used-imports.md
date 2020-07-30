## How to find used imports in my project.

```python
from pathlib import Path
from unimport.session import Session

session = Session()


def get_all_modules(project_path):  # write the path of your own project
    def get_module(imports):
        return {imp.module.__name__.split(".")[0] for imp in imports if imp.module}

    for path in session.list_paths(Path(project_path)):
        try:
            source = session.read(path)[0]
        except SyntaxError:
            continue
        session.scanner.run_visit(source)
        import_names = get_module(session.scanner.imports)
        unused_imp_names = get_module(session.scanner.unused_imports)
        session.scanner.clear()
        yield import_names - unused_imp_names

if __name__ == "__main__":
    modules = set()
    for module in get_all_modules("unimport/"):
        modules.update(module)
    print(modules)
```

## Output

```python
{
    're', 'libcst', 'inspect', 'pathlib', 'typing_extensions', 'contextlib', 'ast', 'unimport', 'importlib',
    'difflib', 'io', 'builtins', 'argparse', 'functools', 'tokenize', 'typing', 'types', 'sys',
    'configparser'
}
```
