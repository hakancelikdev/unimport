import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from unimport import utils
from unimport.analyzer import Analyzer
from unimport.refactor import refactor_string
from unimport.statement import Import


@contextmanager
def reopenable_temp_file(content: str, newline: Optional[str] = None) -> Iterator[Path]:
    """Create a reopenable tempfile to supporting multiple reads/writes.

    Required to avoid file locking issues on Windows.
    For more information, see:
    https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile

    :param content: string content to write.
    :param newline: Newline character to use, if not platform default.
    :yields: tempfile path.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            newline=newline,
            delete=False,
        ) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(content)
        yield tmp_path
    finally:
        os.unlink(tmp_path)


def refactor(path: Path) -> str:
    source = utils.read(path)[0]

    with Analyzer(source=source) as analyzer:
        return refactor_string(
            source=analyzer.source,
            unused_imports=list(Import.get_unused_imports()),
        )
