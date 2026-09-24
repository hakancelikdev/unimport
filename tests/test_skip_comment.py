import pytest

from unimport.analyzers.decarators import is_skip_comment


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
