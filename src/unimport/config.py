import argparse
import configparser
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

if C.PY38_PLUS:
    from typing import Literal  # unimport: skip
else:
    from typing_extensions import Literal  # type: ignore

__all__ = ("Config", "ParseConfig")


@dataclasses.dataclass
class Config:
    default_sources: ClassVar[List[Path]] = [Path(".")]  # Not init attribute
    gitignore_patterns: List[GitWildMatchPattern] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False
    )  # Not init attribute
    use_color: bool = dataclasses.field(init=False)  # Not init attribute

    sources: Optional[List[Path]] = None
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
        self.check = self.check or not any((self.diff, self.remove))
        self.use_color: bool = self._use_color(self.color)

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
    def _get_color_choices(cls) -> Tuple[str]:
        return getattr(
            Config.__annotations__["color"],
            "__args__" if C.PY37_PLUS else "__values__",
        )

    @classmethod
    def _use_color(cls, color: str) -> bool:
        if color not in cls._get_color_choices():
            raise ValueError(color)

        return color == "always" or (
            color == "auto" and sys.stderr.isatty() and TERMINAL_SUPPORT_COLOR
        )

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
            if config_value is None or config_value == getattr(
                cls, field_name
            ):
                config_value = config_context.get(
                    field_name, getattr(cls, field_name)
                )
            context[field_name] = config_value

        return cls(**context)  # Only init attribute values


@dataclasses.dataclass
class ParseConfig:
    CONFIG_FILES: ClassVar[Dict[str, str]] = {
        "setup.cfg": "unimport",
        "pyproject.toml": "tool.unimport",
    }

    config_file: Path

    def __post_init__(self):
        self.section: str = self.CONFIG_FILES[self.config_file.name]

    def parse(self) -> Dict[str, Any]:
        return getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> Dict[str, Any]:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.section):

            def get_config_as_list(name: str) -> List[str]:
                return literal_eval(
                    parser.get(
                        self.section,
                        name,
                        fallback=getattr(Config, name),
                    )
                )

            cfg_context: Dict[str, Any] = {}
            config_annotations_mapping = {
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
            }
            for key, value in parser[self.section].items():
                key_type = config_annotations_mapping[key]
                if key_type == bool:
                    cfg_context[key] = parser.getboolean(self.section, key)
                elif key_type == str:
                    cfg_context[key] = value  # type: ignore
                elif key_type == List[Path]:
                    cfg_context[key] = [Path(p) for p in get_config_as_list(key)]  # type: ignore
            return cfg_context
        else:
            return {}

    def parse_toml(self) -> Dict[str, Any]:
        parsed_toml = toml.loads(self.config_file.read_text())
        toml_context: Dict[str, Any] = parsed_toml.get("tool", {}).get(
            "unimport", {}
        )
        if toml_context:
            sources = toml_context.get("sources", Config.default_sources)
            toml_context["sources"] = [Path(path) for path in sources]
        return toml_context

    @classmethod
    def parse_args(cls, args: argparse.Namespace) -> Config:
        if args.config and args.config.name in cls.CONFIG_FILES:
            config_context = cls(args.config).parse()
            return Config.build(
                args=args.__dict__, config_context=config_context
            )

        return Config.build(args=vars(args))
