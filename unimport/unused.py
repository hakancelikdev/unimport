import tokenize

from unimport.dedect import DetectUnusedImport


def get_unused(source):
    "Yield unused imports."
    dedect = DetectUnusedImport(source)
    for imp in dedect.imports:
        len_dot = len(imp["name"].split("."))
        for name in dedect.names:
            if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                break
        else:
            yield imp


def get_unused_from_file(file_path):
    try:
        with tokenize.open(file_path) as f:
            source = f.read()
    except OSError:
        pass
    else:
        for imports in get_unused(source=source):
            imports.update(path=file_path)
            yield imports
