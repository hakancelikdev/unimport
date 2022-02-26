import os
from pathlib import Path

import pytest

from tests.utils import refactor, reopenable_temp_file
from unimport import utils


@pytest.mark.parametrize(
    "path, count",
    [
        ("tests", 186),
        ("tests/analyzer", 0),
        ("tests/config", 1),
        ("tests/config/configs", 0),
        ("tests/config/configs/no_unimport", 0),
        ("tests/refactor", 0),
        ("tests/test_config.py", 1),
    ],
)
def test_list_paths(path, count):
    path = Path(path)

    assert len(list(utils.list_paths(path))) == count


def test_bad_encoding():
    # Make conflict between BOM and encoding Cookie.
    # https://docs.python.org/3/library/tokenize.html#tokenize.detect_encoding
    bad_encoding = "\ufeff\n# -*- coding: utf-32 -*-\nbad encoding"

    with reopenable_temp_file(bad_encoding) as tmp_path:
        assert refactor(tmp_path) == ""


def test_refactor_file():
    with reopenable_temp_file("import os") as tmp_path:
        assert refactor(tmp_path) == ""


def test_diff_file():
    with reopenable_temp_file("import os") as tmp_path:
        source = utils.read(tmp_path)[0]
        refactor_result = refactor(tmp_path)
        diff_file = utils.diff(
            source=source,
            refactor_result=refactor_result,
            fromfile=tmp_path,
        )
        diff = (
            f"--- {tmp_path.as_posix()}\n",
            "+++ \n",
            "@@ -1 +0,0 @@\n",
            "-import os",
        )
        assert diff == diff_file


def test_read():
    source = "b�se"

    with reopenable_temp_file(source) as tmp_path:
        assert (source, "utf-8", None) == utils.read(tmp_path)


def test_read_newline_native():
    source = "\n".join(
        [
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )

    with reopenable_temp_file(source, newline=os.linesep) as tmp_path:
        assert (source, "utf-8", os.linesep) == utils.read(tmp_path)


def test_read_newline_nonnative(non_native_linesep):
    source = "\n".join(
        [
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )

    with reopenable_temp_file(source, newline=non_native_linesep) as tmp_path:
        assert (source, "utf-8", non_native_linesep) == utils.read(tmp_path)
