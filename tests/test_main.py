import json
from pathlib import Path
from textwrap import dedent
from unittest import mock

import pytest

from tests.utils import reopenable_temp_file
from unimport import utils
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


@pytest.mark.parametrize("color, use_color", [("never", False), ("always", True)])
def test_permission_prompt_uses_color_setting(color, use_color, monkeypatch):
    calls = []

    def fake_permission(path, use_color):
        calls.append(use_color)
        return False

    monkeypatch.setattr("unimport.commands.permission", fake_permission)

    with reopenable_temp_file("import os\n") as temp_file:
        Main.run(["--disable-auto-discovery-config", "--permission", "--color", color, temp_file.as_posix()])

    assert calls == [use_color]


def test_unreadable_files_are_reported(tmp_path, capsys):
    (tmp_path / "bad_encoding.py").write_bytes(b"# -*- coding: not-a-real-encoding -*-\nimport os\n")
    (tmp_path / "bad_bytes.py").write_bytes(b'import os\nx = "\xff"\n')
    (tmp_path / "good.py").write_text("import sys\n")

    main = Main.run(["--disable-auto-discovery-config", "--check", "--color", "never", tmp_path.as_posix()])
    output = capsys.readouterr().out

    assert "unknown encoding" in output and "bad_encoding.py" in output
    assert "can't decode" in output and "bad_bytes.py" in output
    assert "sys at" in output  # the other files are still checked
    assert main.exit_code() == 1


def _write_sources(directory: Path) -> list[Path]:
    sources = {
        "a.py": "import os\nimport sys\n\nprint(sys)\n",
        "b.py": "import re  # comment\nfrom typing import List, Dict\n\nx: List[int] = []\n",
        "c.py": "import json\n\njson.dumps({})\n",
        "d.py": "import ast\ndef broken(:\n",
    }
    paths = []
    for name, source in sources.items():
        path = directory / name
        path.write_text(source)
        paths.append(path)
    return paths


@pytest.mark.parametrize("command", ["--check", "--diff"])
def test_jobs_output_matches_sequential(tmp_path: Path, capsys, command: str):
    _write_sources(tmp_path)
    argv = ["--disable-auto-discovery-config", command, "--color", "never", tmp_path.as_posix()]

    sequential = Main.run([*argv, "--jobs", "1"])
    sequential_output = capsys.readouterr().out

    parallel = Main.run([*argv, "--jobs", "2"])
    parallel_output = capsys.readouterr().out

    assert parallel_output == sequential_output
    assert "os at" in parallel_output or "-import os" in parallel_output
    assert (parallel.is_unused_imports, parallel.is_syntax_error) == (True, True)
    assert parallel.exit_code() == sequential.exit_code() == 1


def test_jobs_remove(tmp_path: Path):
    paths = _write_sources(tmp_path)

    main = Main.run(["--disable-auto-discovery-config", "--remove", "--jobs", "2", tmp_path.as_posix()])

    assert main.refactor_applied is True
    assert paths[0].read_text() == "import sys\n\nprint(sys)\n"
    assert paths[1].read_text() == "from typing import List\n\nx: List[int] = []\n"
    assert paths[2].read_text() == "import json\n\njson.dumps({})\n"


def test_jobs_report_unreadable_files(tmp_path: Path, capsys):
    (tmp_path / "bad_bytes.py").write_bytes(b'import os\nx = "\xff"\n')
    (tmp_path / "good.py").write_text("import sys\n")

    main = Main.run(
        ["--disable-auto-discovery-config", "--check", "--color", "never", "--jobs", "2", tmp_path.as_posix()]
    )
    output = capsys.readouterr().out

    assert "can't decode" in output and "bad_bytes.py" in output
    assert "sys at" in output
    assert main.exit_code() == 1


def test_json_format(tmp_path: Path, capsys):
    (tmp_path / "a.py").write_text("import os\nfrom typing import List, Dict\n\nx: List[int] = []\n")
    (tmp_path / "b.py").write_text("def broken(:\n")
    (tmp_path / "c.py").write_text("import sys\n\nprint(sys)\n")

    main = Main.run(["--disable-auto-discovery-config", "--format", "json", tmp_path.as_posix()])
    report = json.loads(capsys.readouterr().out)

    assert report["unused_imports"] == [
        {
            "path": (tmp_path / "a.py").as_posix(),
            "line": 1,
            "name": "os",
            "package": "os",
            "star": False,
            "suggestions": [],
        },
        {
            "path": (tmp_path / "a.py").as_posix(),
            "line": 2,
            "name": "Dict",
            "package": "typing",
            "star": False,
            "suggestions": [],
        },
    ]
    assert [error["path"] for error in report["errors"]] == [(tmp_path / "b.py").as_posix()]
    assert main.exit_code() == 1


def test_json_format_clean_project_prints_only_json(tmp_path: Path, capsys):
    (tmp_path / "a.py").write_text("import sys\n\nprint(sys)\n")

    from unimport.__main__ import main

    with pytest.raises(SystemExit) as exit_info:
        with mock.patch(
            "sys.argv", ["unimport", "--disable-auto-discovery-config", "--format", "json", tmp_path.as_posix()]
        ):
            main()

    assert exit_info.value.code == 0
    assert json.loads(capsys.readouterr().out) == {"unused_imports": [], "errors": []}


@pytest.mark.parametrize("option", ["--diff", "--remove", "--permission"])
def test_json_format_rejects_commands_that_print(option: str, capsys):
    with pytest.raises(SystemExit) as exit_info:
        Main(["--disable-auto-discovery-config", "--format", "json", option])

    assert exit_info.value.code == 2
    assert "--format json" in capsys.readouterr().err


def test_json_format_with_jobs_and_unreadable_file(tmp_path: Path, capsys):
    (tmp_path / "a.py").write_text("import os\n")
    (tmp_path / "b.py").write_bytes(b'x = "\xff"\n')
    (tmp_path / "c.py").write_text("import sys\n\nprint(sys)\n")

    main = Main.run(["--disable-auto-discovery-config", "--format", "json", "--jobs", "2", tmp_path.as_posix()])
    report = json.loads(capsys.readouterr().out)

    assert [imp["name"] for imp in report["unused_imports"]] == ["os"]
    assert [error["path"] for error in report["errors"]] == [(tmp_path / "b.py").as_posix()]
    assert main.exit_code() == 1


def test_per_file_ignores(tmp_path: Path, capsys):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("from .core import Api\n")
    (tmp_path / "pkg" / "conftest.py").write_text("import json\nimport fixtures.db\n")
    config = tmp_path / "pyproject.toml"
    config.write_text('[tool.unimport]\nper-file-ignores = { "__init__.py" = ["*"], "conftest.py" = ["fixtures.*"] }\n')

    main = Main.run(["--config", config.as_posix(), "--check", "--color", "never", (tmp_path / "pkg").as_posix()])
    output = capsys.readouterr().out

    assert "json at" in output
    assert "fixtures.db" not in output
    assert "Api" not in output
    assert main.is_unused_imports is True


@pytest.mark.parametrize("jobs", ["1", "2"])
def test_per_file_ignores_are_not_removed(tmp_path: Path, jobs: str):
    (tmp_path / "__init__.py").write_text("from .core import Api\nimport os\n")
    (tmp_path / "module.py").write_text("import os\n")
    config = tmp_path / "pyproject.toml"
    config.write_text('[tool.unimport]\nper-file-ignores = { "__init__.py" = ["Api"] }\n')

    Main.run(["--config", config.as_posix(), "--remove", "--jobs", jobs, tmp_path.as_posix()])

    assert (tmp_path / "__init__.py").read_text() == "from .core import Api\n"
    assert "import os" not in (tmp_path / "module.py").read_text()  # not covered by the ignore, so removed


def test_null_bytes_reported_as_syntax_error(tmp_path: Path, capsys):
    (tmp_path / "a.py").write_bytes(b"import os\x00\n")

    main = Main.run(["--disable-auto-discovery-config", "--check", "--color", "never", tmp_path.as_posix()])

    assert "null bytes" in capsys.readouterr().out
    assert main.is_syntax_error is True
    assert main.exit_code() == 1


def test_star_import_suggestions_with_partly_dynamic_all(tmp_path: Path, monkeypatch):
    (tmp_path / "partial_all_core.py").write_text('__all__ = ["alpha"]\nalpha = 1\n')
    (tmp_path / "partial_all_lib.py").write_text(
        "import partial_all_core\n"
        "from partial_all_core import alpha\n\n"
        "__all__ = list(partial_all_core.__all__)\n"
        '__all__ += ["beta"]\n'
        "beta = 2\n"
    )
    user = tmp_path / "user.py"
    user.write_text("from partial_all_lib import *\n\nprint(alpha, beta)\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    utils.get_spec.cache_clear()

    Main.run(["--disable-auto-discovery-config", "--include-star-import", "--remove", user.as_posix()])

    assert user.read_text() == "from partial_all_lib import alpha, beta\n\nprint(alpha, beta)\n"
