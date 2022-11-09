import io
import textwrap
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from unimport.commands import diff


@pytest.mark.parametrize("use_color", [True, False])
def test_diff_not_exits_diff(use_color):
    with redirect_stdout(io.StringIO()) as f:
        exists_diff = diff(Path("example.py"), "source", "source", use_color)

    assert f.getvalue() == ""
    assert exists_diff is False


@pytest.mark.parametrize(
    ("use_color", "stdout"),
    [
        [
            True,
            textwrap.dedent(
                """\
                \x1b[1;37m--- example.py
                \x1b[0m
                \x1b[1;37m+++ 
                \x1b[0m
                \x1b[36m@@ -1 +1 @@
                \x1b[0m
                \x1b[31m-source\x1b[0m
                \x1b[32m+refactor_result\x1b[0m
                """
            ),
        ],
        [
            False,
            textwrap.dedent(
                """\
                --- example.py

                +++ 

                @@ -1 +1 @@

                -source
                +refactor_result
                """
            ),
        ],
    ],
)
def test_diff_exits_diff(use_color, stdout):
    with redirect_stdout(io.StringIO()) as f:
        exists_diff = diff(Path("example.py"), "source", "refactor_result", use_color)

    assert f.getvalue() == stdout
    assert exists_diff is True
