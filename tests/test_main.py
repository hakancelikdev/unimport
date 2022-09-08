from textwrap import dedent

import pytest

from tests.utils import reopenable_temp_file
from unimport.config import Config
from unimport.main import Main


def test_empty_main():
    main = Main([])

    assert main.argv == []
    assert main.config == Config()
    assert main.is_syntax_error is False
    assert main.is_unused_imports is False
    assert main.refactor_applied is False


def test_main_run_under_path():
    source = dedent(
        """\
        import os

        """
    )
    with reopenable_temp_file(source) as temp_file:
        main = Main.run(["--include", temp_file.as_posix()])

    assert main.argv == ["--include", temp_file.as_posix()]
    assert main.config == Config(include=temp_file.as_posix())
    assert main.is_syntax_error is False
    assert main.is_unused_imports is False
    assert main.refactor_applied is False


@pytest.mark.parametrize("command_name", ["check", "diff", "permission", "remove"])
def test_main_command(command_name, monkeypatch):
    def mock_command(*args, **kwargs):
        if not hasattr(mock_command, "call_count"):
            mock_command.call_count = 0

        mock_command.call_count += 1

    monkeypatch.setattr(Main, command_name, mock_command)

    source = dedent(
        """\
        import os
        
        """
    )
    with reopenable_temp_file(source) as temp_file:
        Main.run([f"--{command_name}", temp_file.as_posix()])

    assert mock_command.call_count == 1, f"command_name='{command_name}'"


def test_exit_code():
    main = Main([])
    assert main.exit_code() == 0

    main.is_syntax_error = True
    assert main.exit_code() == 1

    # reset syntax error
    main.is_syntax_error = False

    main.is_unused_imports = True
    assert main.exit_code() == 1

    main.refactor_applied = True
    assert main.exit_code() == 0
