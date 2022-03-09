import io
import textwrap
from contextlib import redirect_stdout
from pathlib import Path

from unimport.commands import diff


def test_diff_not_exits_diff():
    with redirect_stdout(io.StringIO()) as f:
        exists_diff = diff(Path("example.py"), "source", "source")

    assert f.getvalue() == ""
    assert exists_diff is False


def test_diff_exits_diff():
    with redirect_stdout(io.StringIO()) as f:
        exists_diff = diff(Path("example.py"), "source", "refactor_result")

    assert f.getvalue() == textwrap.dedent(
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
    )
    assert exists_diff is True
