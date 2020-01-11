import pathlib
import tokenize

from unimport.unused import filter_unused_imports

pattern_python_file = "**/*.py"


def get_files(src, config):
    p = pathlib.Path(src)

    def _is_excluded(path):
        for pattern_exclude in config.exclude:
            for i in p.glob(pattern_exclude):
                if str(path).startswith(str(i)):
                    return True

    for file in p.glob(pattern_python_file):
        if not _is_excluded(file):
            yield file


def overwrite(file_path, unused_imports):
    with tokenize.open(file_path) as stream:
        source = stream.read()
        encoding = stream.encoding
    unused_imports = [
        unused_import["name"] for unused_import in unused_imports
    ]
    destination = filter_unused_imports(
        source=source, unused_imports=unused_imports
    )
    pathlib.Path(file_path).write_text(destination, encoding=encoding)
