import pytest

from unimport.analyzers import MainAnalyzer
from unimport.analyzers.decarators import is_skip_comment
from unimport.statement import Import


@pytest.mark.parametrize(
    "source, expected",
    [
        ("import os", False),
        ("import os  # unimport: skip", True),
        ("import os  # unimport:skip", True),
        ("import os  # noqa", True),
        ("import os  # NOQA", True),
        ("import os  # noqa - kept for side effects", True),
        ("import os  # noqa: F401", True),
        ("import os  # noqa:F401", True),
        ("import os  # noqa: E501,F401", True),
        ("import os  # noqa: E501, F401", True),
        ("import os  # type: ignore  # noqa", True),
        ("import os  # noqa: E501", False),
        ("import os  # noqa:E501,W291", False),
        ("import os  # some comment", False),
        ("from x import (  # noqa\n    y,\n)", True),
        ("from x import (  # noqa: E501\n    y,\n)", False),
    ],
)
def test_is_skip_comment(source: str, expected: bool):
    assert is_skip_comment(source) is expected


@pytest.mark.parametrize("separator", ["\f", "\v", "\x1c", "\x85", " "])
def test_skip_comment_line_after_other_line_separators(separator: str):
    source = f'x = "a{separator}b"\nimport os  # noqa\nimport sys\n'
    with MainAnalyzer(source=source):
        assert [imp.name for imp in Import.get_unused_imports()] == ["sys"]
