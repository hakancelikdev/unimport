import io
import textwrap
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from unimport.commands import check, requirements_check
from unimport.statement import Import, ImportFrom


@pytest.mark.parametrize(
    "use_color_setting, stdout", [[True, ""], [False, ""]]
)
def test_emty_print_check(use_color_setting: bool, stdout: str) -> None:
    with redirect_stdout(io.StringIO()) as f:
        check(Path("tests/commands/test_check.py"), [], use_color_setting)
    assert f.getvalue() == stdout


@pytest.mark.parametrize(
    "use_color_setting, stdout",
    [
        [
            True,
            "\x1b[33mz\x1b[0m at \x1b[32mtests/commands/test_check.py\x1b[0m:\x1b[32m1\x1b[0m\n",
        ],
        [False, "z at tests/commands/test_check.py:1\n"],
    ],
)
def test_import_print_check(use_color_setting: bool, stdout: str) -> None:
    with redirect_stdout(io.StringIO()) as f:
        check(
            Path("tests/commands/test_check.py"),
            [
                ImportFrom(
                    lineno=1,
                    column=1,
                    name="z",
                    package="x",
                    star=False,
                    suggestions=[],
                )
            ],
            use_color_setting,
        )
    assert f.getvalue() == stdout


@pytest.mark.parametrize(
    "use_color_setting, stdout",
    [
        [
            True,
            textwrap.dedent(
                """\
                \x1b[33mss\x1b[0m at \x1b[32mtests/commands/test_check.py\x1b[0m:\x1b[32m3\x1b[0m
                \x1b[33mx\x1b[0m at \x1b[32mtests/commands/test_check.py\x1b[0m:\x1b[32m4\x1b[0m
                """
            ),
        ],
        [
            False,
            textwrap.dedent(
                """\
                ss at tests/commands/test_check.py:3
                x at tests/commands/test_check.py:4
                """
            ),
        ],
    ],
)
def test_import_and_fromimport_print_check(
    use_color_setting: bool, stdout: str
) -> None:
    with redirect_stdout(io.StringIO()) as f:
        check(
            Path("tests/commands/test_check.py"),
            [
                ImportFrom(
                    lineno=3,
                    column=1,
                    name="ss",
                    package="t",
                    star=False,
                    suggestions=[],
                ),
                Import(lineno=4, column=1, name="x", package="le"),
            ],
            use_color_setting,
        )
    assert f.getvalue() == stdout


@pytest.mark.parametrize(
    "use_color_setting, stdout",
    [
        [
            True,
            "\x1b[36munimport\x1b[0m at \x1b[36mtests/commands/test_check.py\x1b[0m:\x1b[36m2\x1b[0m\n",
        ],
        [False, "unimport at tests/commands/test_check.py:2\n"],
    ],
)
def test_requirements_check(use_color_setting: bool, stdout: str) -> None:
    with redirect_stdout(io.StringIO()) as f:
        requirements_check(
            Path("tests/commands/test_check.py"),
            1,
            "unimport",
            use_color_setting,
        )

    assert f.getvalue() == stdout
