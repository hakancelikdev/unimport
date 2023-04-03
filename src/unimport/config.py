import argparse
import configparser
import contextlib
import dataclasses
import functools
import sys
from ast import literal_eval
from pathlib import Path
from typing import Any, ClassVar, Dict, Iterator, List, Optional, Tuple

import toml
from pathspec.patterns import GitWildMatchPattern

from unimport import constants as C
from unimport import utils
from unimport.color import TERMINAL_SUPPORT_COLOR
from unimport.exceptions import ConfigFileNotFound, UnknownConfigKeyException, UnsupportedConfigFile

if C.PY38_PLUS:
    from typing import Literal
else:
    from typing_extensions import Literal  # type: ignore

__all__ = ("Config", "ParseConfig")


CONFIG_FILES: Dict[str, str] = {
    "setup.cfg": "unimport",
    "pyproject.toml": "tool.unimport",
}

CONFIG_ANNOTATIONS_MAPPING = {
    "sources": List[Path],
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
    #
    "include-star-import": bool,
    "ignore-init": bool,
}

CONFIG_LIKE_COMMANDS_MAPPING = {
    "include-star-import": "include_star_import",
    "ignore-init": "ignore_init",
}


@dataclasses.dataclass
class Config:
    default_sources: ClassVar[List[Path]] = [Path(".")]  # Not init attribute
    gitignore_patterns: List[GitWildMatchPattern] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False
    )  # Not init attribute
    use_color: bool = dataclasses.field(init=False)  # Not init attribute

    sources: Optional[List[Path]] = None
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
    color: Literal["auto", "always", "never"] = "auto"

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _get_init_fields(cls):
        return [
            key
            for key, field in cls.__dataclass_fields__.items()
            if field._field_type == dataclasses._FIELD and field.init
        ]

    def __post_init__(self):
        if self.sources is None:
            self.sources = self.default_sources

        self.diff = self.diff or self.permission
        self.remove = self.remove or not any((self.diff, self.check))
        self.use_color = self.is_use_color(self.color)

        if self.gitignore:
            self.gitignore_patterns = utils.get_exclude_list_from_gitignore()

        elif self.ignore_init:
            self.exclude = "|".join([self.exclude, C.INIT_FILE_IGNORE_REGEX])

    def get_paths(self) -> Iterator[Path]:
        for source_path in self.sources:
            yield from utils.list_paths(
                source_path,
                include=self.include,
                exclude=self.exclude,
                gitignore_patterns=self.gitignore_patterns,
            )

    @classmethod
    def get_color_choices(cls) -> Tuple[str]:
        return getattr(
            Config.__annotations__["color"],
            "__args__" if C.PY37_PLUS else "__values__",
        )

    @classmethod
    def is_use_color(cls, color: str) -> bool:
        if color not in cls.get_color_choices():
            raise ValueError(color)

        return color == "always" or (color == "auto" and sys.stderr.isatty() and TERMINAL_SUPPORT_COLOR)

    @classmethod
    def build(
        cls,
        *,
        args: Optional[Dict[str, Any]] = None,
        config_context: Optional[Dict[str, Any]] = None,
    ) -> "Config":
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

    def parse(self) -> Dict[str, Any]:
        return getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> Dict[str, Any]:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.config_section):

            def get_config_as_list(name: str) -> List[str]:
                return literal_eval(
                    parser.get(
                        self.config_section,
                        name,
                        fallback=getattr(Config, name),
                    )
                )

            cfg_context: Dict[str, Any] = {}
            for key, value in parser[self.config_section].items():
                if key not in CONFIG_ANNOTATIONS_MAPPING:
                    raise UnknownConfigKeyException(key)

                key_type = CONFIG_ANNOTATIONS_MAPPING[key]
                if key_type == bool:
                    cfg_context[key] = parser.getboolean(self.config_section, key)
                elif key_type == str:
                    cfg_context[key] = value  # type: ignore
                elif key_type == List[Path]:
                    cfg_context[key] = [Path(p) for p in get_config_as_list(key)]  # type: ignore

                expected_key = CONFIG_LIKE_COMMANDS_MAPPING.get(key, None)
                if expected_key is not None:
                    cfg_context[expected_key] = cfg_context.pop(key)
            return cfg_context
        else:
            return {}

    def parse_toml(self) -> Dict[str, Any]:
        parsed_toml = toml.loads(self.config_file.read_text())
        toml_context_from_conf: Dict[str, Any] = dict(
            functools.reduce(lambda x, y: x.get(y, {}), self.config_section.split("."), parsed_toml)  # type: ignore[attr-defined]
        )
        toml_context: Dict[str, Any] = {}
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
    def parse_args(cls, args: argparse.Namespace) -> "Config":
        config_context: Optional[Dict[str, Any]] = None

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
