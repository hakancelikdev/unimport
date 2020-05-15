import difflib
import fnmatch
import tokenize
from lib2to3.pgen2.parse import ParseError
from pathlib import Path

from unimport.config import Config
from unimport.refactor import refactor_string
from unimport.scan import Scanner


class Session:
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.scanner = Scanner()

    def _read(self, path):
        try:
            with tokenize.open(path) as stream:
                source = stream.read()
                encoding = stream.encoding
        except OSError as exc:
            print(f"{exc} Can't read")
            return "", "utf-8"
        else:
            return source, encoding

    def _list_paths(self, start, pattern="**/*.py"):
        start = Path(start)

        def _is_excluded(path):
            for pattern_exclude in self.config.exclude:
                if fnmatch.fnmatch(path, pattern_exclude):
                    return True
            return False

        if not start.is_dir():
            if not _is_excluded(start):
                yield start
        else:
            for dir_ in start.iterdir():
                if not _is_excluded(dir_):
                    for path in dir_.glob(pattern):
                        if not _is_excluded(path):
                            yield path

    def refactor(self, source):
        self.scanner.run_visit(source)
        refactor = refactor_string(self.scanner)
        self.scanner.clear()
        return refactor

    def refactor_file(self, path, apply=False):
        path = Path(path)
        source, encoding = self._read(path)
        result = self.refactor(source)
        if apply:
            path.write_text(result, encoding=encoding)
        else:
            return result

    def diff(self, source):
        return tuple(
            difflib.unified_diff(
                source.splitlines(), self.refactor(source).splitlines()
            )
        )

    def diff_file(self, path):
        source, _ = self._read(path)
        try:
            result = self.refactor_file(path, apply=False)
        except ParseError:
            print(f"\033[91m Invalid python file '{path}'\033[00m")
            return tuple()
        return tuple(
            difflib.unified_diff(
                source.splitlines(), result.splitlines(), fromfile=str(path)
            )
        )
