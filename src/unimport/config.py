from __future__ import annotations

import argparse
import configparser
import contextlib
import dataclasses
import fnmatch
import functools
import os
import sys
import typing
from ast import literal_eval
from pathlib import Path

import toml
from pathspec.patterns import GitWildMatchPattern

from unimport import constants as C
from unimport import utils
from unimport.color import TERMINAL_SUPPORT_COLOR
from unimport.enums import ColorSelect
from unimport.exceptions import ConfigFileNotFound, UnknownConfigKeyException, UnsupportedConfigFile

__all__ = ("Config", "ParseConfig")


CONFIG_FILES: dict[str, str] = {
    "setup.cfg": "unimport",
    "pyproject.toml": "tool.unimport",
}

CONFIG_ANNOTATIONS_MAPPING = {
    "sources": list[Path],
    "include": str,
    "exclude": str,
    "gitignore": bool,
    "remove": bool,
    "diff": bool,
    "include_star_import": bool,
    "permission": bool,
    "check": bool,
    "ignore_init": bool,
    "color": str,
    "jobs": int,
    "format": str,
    "per_file_ignores": dict,
    #
    "include-star-import": bool,
    "ignore-init": bool,
    "per-file-ignores": dict,
}

CONFIG_LIKE_COMMANDS_MAPPING = {
    "include-star-import": "include_star_import",
    "ignore-init": "ignore_init",
    "per-file-ignores": "per_file_ignores",
}


@dataclasses.dataclass
class Config:
    default_sources: typing.ClassVar[list[Path]] = [Path(".")]  # Not init attribute
    gitignore_patterns: list[GitWildMatchPattern] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False
    )  # Not init attribute
    use_color: bool = dataclasses.field(init=False)  # Not init attribute

    sources: list[Path] | None = None
    disable_auto_discovery_config: bool = False
    include: str = C.INCLUDE_REGEX_PATTERN
    exclude: str = C.EXCLUDE_REGEX_PATTERN
    gitignore: bool = False
    remove: bool = False
    diff: bool = False
    include_star_import: bool = False
    permission: bool = False
    check: bool = False
    ignore_init: bool = False
    color: ColorSelect = ColorSelect.AUTO
    jobs: int = 1
    format: str = C.OUTPUT_FORMAT_TEXT
    per_file_ignores: dict[str, list[str]] | None = None  # file glob -> import name patterns

    @classmethod
    @functools.cache
    def _get_init_fields(cls):
        return [
            key
            for key, field in cls.__dataclass_fields__.items()
            if field._field_type == dataclasses._FIELD and field.init
        ]

    def __post_init__(self):
        if self.sources is None:
            self.sources = self.default_sources

        if self.format not in C.OUTPUT_FORMATS:
            raise ValueError(f"format must be one of {', '.join(C.OUTPUT_FORMATS)}, got {self.format!r}")
        if self.format == C.OUTPUT_FORMAT_JSON:
            if any((self.diff, self.remove, self.permission)):
                raise ValueError(
                    "--format json only reports unused imports; it can't be combined with --diff, --remove or --permission"
                )
            self.check = True

        self.diff = self.diff or self.permission
        self.remove = self.remove or not any((self.diff, self.check))
        self.use_color = self.is_use_color(self.color)
        self.jobs = self.get_jobs(self.jobs, permission=self.permission)
        self.per_file_ignores = self.normalize_per_file_ignores(self.per_file_ignores)

        if self.gitignore:
            self.gitignore_patterns = utils.get_exclude_list_from_gitignore()

        if self.ignore_init:
            self.exclude = "|".join([self.exclude, C.INIT_FILE_IGNORE_REGEX])

    def get_paths(self) -> typing.Iterator[Path]:
        for source_path in self.sources:
            yield from utils.list_paths(
                source_path,
                include=self.include,
                exclude=self.exclude,
                gitignore_patterns=self.gitignore_patterns,
            )

    @staticmethod
    def get_jobs(jobs: int, *, permission: bool = False) -> int:
        if jobs < 0:
            raise ValueError(f"jobs must be 0 or a positive number, got {jobs}")
        if permission:  # asks for confirmation file by file
            return 1
        if jobs == 0:
            return os.cpu_count() or 1
        return jobs

    @staticmethod
    def normalize_per_file_ignores(value: dict | None) -> dict[str, list[str]]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError(f"per-file-ignores must be a table of file pattern -> import names, got {value!r}")
        normalized: dict[str, list[str]] = {}
        for file_pattern, names in value.items():
            if isinstance(names, str):
                names = names.split(",")
            if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
                raise ValueError(f"per-file-ignores[{file_pattern!r}] must be a list of import names, got {names!r}")
            normalized[str(file_pattern)] = [name.strip() for name in names if name.strip()]
        return normalized

    def is_ignored_import(self, path: Path, import_name: str) -> bool:
        """Whether per-file-ignores keeps import_name in the file at path.

        A file pattern matches the whole path (``src/*/conftest.py``) or,
        without a slash, the file name in any directory (``__init__.py``).
        """
        posix_path = path.as_posix()
        for file_pattern, name_patterns in self.per_file_ignores.items():  # type: ignore[union-attr]
            file_matches = fnmatch.fnmatch(posix_path, file_pattern) or (
                "/" not in file_pattern and fnmatch.fnmatch(path.name, file_pattern)
            )
            if file_matches and any(fnmatch.fnmatch(import_name, pattern) for pattern in name_patterns):
                return True
        return False

    @classmethod
    def get_color_choices(cls) -> list[str]:
        return [color.value for color in ColorSelect]

    @classmethod
    def is_use_color(cls, color: ColorSelect) -> bool:
        if color not in list(ColorSelect):
            raise ValueError(color)

        return color == ColorSelect.ALWAYS or (
            color == ColorSelect.AUTO and sys.stderr.isatty() and TERMINAL_SUPPORT_COLOR
        )

    @classmethod
    def build(cls, *, args: dict | None = None, config_context: dict | None = None) -> Config:
        if args is None and config_context is None:
            return cls()

        args = args if args is not None else {}
        config_context = config_context if config_context is not None else {}

        context = {}
        for field_name in cls._get_init_fields():
            config_value = args.get(field_name, None)
            if config_value is None or config_value == getattr(cls, field_name):
                config_value = config_context.get(field_name, getattr(cls, field_name))
            context[field_name] = config_value

        return cls(**context)  # Only init attribute values


@dataclasses.dataclass
class ParseConfig:
    config_file: Path

    def __post_init__(self):
        if not self.config_file.exists():
            raise ConfigFileNotFound(self.config_file)

        self.config_section = CONFIG_FILES.get(self.config_file.name, None)
        if self.config_section is None:
            raise UnsupportedConfigFile(self.config_file)

    def parse(self) -> dict:
        return getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> dict:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.config_section):

            def get_config_as_list(name: str) -> list[str]:
                return literal_eval(
                    parser.get(
                        self.config_section,
                        name,
                        fallback=getattr(Config, name),
                    )
                )

            cfg_context: dict = {}
            for key, value in parser[self.config_section].items():
                if key not in CONFIG_ANNOTATIONS_MAPPING:
                    raise UnknownConfigKeyException(key)

                key_type = CONFIG_ANNOTATIONS_MAPPING[key]
                if key_type == bool:
                    cfg_context[key] = parser.getboolean(self.config_section, key)
                elif key_type == str:
                    cfg_context[key] = value  # type: ignore
                elif key_type == int:
                    cfg_context[key] = parser.getint(self.config_section, key)
                elif key_type == list[Path]:
                    cfg_context[key] = [Path(p) for p in get_config_as_list(key)]  # type: ignore
                elif key_type == dict:
                    # One "file pattern: name, name" entry per line, like flake8's per-file-ignores.
                    cfg_context[key] = {
                        file_pattern.strip(): names
                        for file_pattern, _, names in (
                            line.partition(":") for line in value.splitlines() if line.strip()  # type: ignore
                        )
                    }

                expected_key = CONFIG_LIKE_COMMANDS_MAPPING.get(key, None)
                if expected_key is not None:
                    cfg_context[expected_key] = cfg_context.pop(key)
            return cfg_context
        else:
            return {}

    def parse_toml(self) -> dict:
        parsed_toml = toml.loads(self.config_file.read_text())
        toml_context_from_conf: dict = dict(
            functools.reduce(lambda x, y: x.get(y, {}), self.config_section.split("."), parsed_toml)  # type: ignore[attr-defined]
        )
        toml_context: dict = {}
        if toml_context_from_conf:
            for key, value in toml_context_from_conf.items():
                key = CONFIG_LIKE_COMMANDS_MAPPING.get(key, key)

                if key not in CONFIG_ANNOTATIONS_MAPPING:
                    raise UnknownConfigKeyException(key)

                toml_context[key] = value

            sources = toml_context.get("sources", None)
            if sources is not None:
                toml_context["sources"] = [Path(path) for path in sources]
        return toml_context

    @classmethod
    def parse_args(cls, args: argparse.Namespace) -> Config:
        config_context: dict | None = None

        if args.config is not None:
            config_context = cls(args.config).parse()
        elif args.config is None and args.disable_auto_discovery_config is False:
            for path in CONFIG_FILES.keys():
                with contextlib.suppress(FileNotFoundError):
                    config_context = cls(Path(path)).parse()
                    if config_context:
                        break

        if not config_context:
            config_context = None

        return Config.build(args=vars(args), config_context=config_context)
