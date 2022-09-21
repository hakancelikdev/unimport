import os
import sys
import textwrap
from pathlib import Path

import pytest

from tests.utils import refactor, reopenable_temp_file
from unimport import constants as C
from unimport import utils


@pytest.mark.parametrize(
    "path, count",
    [
        ("tests/commands", 7),
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


@pytest.mark.skipif(
    not C.PY37_PLUS or sys.platform == "win32",
    reason="Patspec version 0.10.0 and above are only supported for Python 3.7 above.",
)
def test_list_paths_with_gitignore():
    gitignore = textwrap.dedent(
        """\
        a
        b
        spam/**
        **/api/
        **/tests
        **/
        """
    )
    with reopenable_temp_file(gitignore) as gitignore_path:
        gitignore_patterns = utils.get_exclude_list_from_gitignore(gitignore_path)
        assert list(utils.list_paths(Path("."), gitignore_patterns=gitignore_patterns)) == []


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


@pytest.mark.parametrize(
    "is_unused_imports, is_syntax_error, refactor_applied, expected_exit_code",
    [
        (True, True, True, 1),
        (True, True, False, 1),
        (True, False, True, 0),
        (True, False, False, 1),
        (True, False, False, 1),
        (False, True, False, 1),
        (False, False, False, 0),
    ],
)
def test_return_exit_code(
    is_unused_imports,
    is_syntax_error,
    refactor_applied,
    expected_exit_code,
):
    assert (
        utils.return_exit_code(
            is_unused_imports=is_unused_imports,
            is_syntax_error=is_syntax_error,
            refactor_applied=refactor_applied,
        )
        == expected_exit_code
    )
