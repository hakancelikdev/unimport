from textwrap import dedent
from unittest import mock

import pytest

from tests.utils import reopenable_temp_file
from unimport.config import Config
from unimport.main import Main


def test_empty_main():
    main = Main(["--disable-auto-discovery-config"])

    assert main.argv == ["--disable-auto-discovery-config"]
    assert main.config == Config(disable_auto_discovery_config=True)
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
        main = Main.run(["--disable-auto-discovery-config", "--include", temp_file.as_posix()])

    assert main.argv == ["--disable-auto-discovery-config", "--include", temp_file.as_posix()]
    assert main.config == Config(disable_auto_discovery_config=True, include=temp_file.as_posix())
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


@mock.patch("unimport.main.Main.permission")
def test_commands_in_run(mock_permission):
    source = dedent(
        """\
        import os

        """
    )

    mock_permission.return_value = False

    assert Main(["--disable-auto-discovery-config"]).config.remove is True
    assert Main(["--disable-auto-discovery-config"]).config.permission is False

    with reopenable_temp_file(source) as temp_file:
        main = Main.run(["--disable-auto-discovery-config", f"--permission", temp_file.as_posix()])

    assert main.config.remove is False
    assert main.config.permission is True
