import os

import pytest

import unimport.utils
from tests.utils import reopenable_temp_file
from unimport.main import Main


@pytest.fixture(scope="module")
def source():
    return "\n".join(
        [
            "import os",
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )


@pytest.fixture(scope="module")
def result():
    return "\n".join(
        [
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )


def test_platform_native_linesep(source, result):
    with reopenable_temp_file(source, newline=os.linesep) as tmp_path:
        Main.run(["--remove", tmp_path.as_posix()])
        with open(tmp_path, encoding="utf-8") as tmp_py_file:
            tmp_py_file.read()
            assert os.linesep == tmp_py_file.newlines
        assert result == unimport.utils.read(tmp_path)[0]


def test_platform_non_native_linesep(non_native_linesep, source, result):
    with reopenable_temp_file(source, newline=non_native_linesep) as tmp_path:
        Main.run(["--remove", tmp_path.as_posix()])
        with open(tmp_path, encoding="utf-8") as tmp_py_file:
            tmp_py_file.read()
            assert non_native_linesep == tmp_py_file.newlines
        assert result == unimport.utils.read(tmp_path)[0]
