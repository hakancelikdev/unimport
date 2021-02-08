import configparser
from ast import literal_eval
from pathlib import Path
from typing import List, NamedTuple

import toml

from unimport import constants as C
from unimport import utils

__all__ = ["DefaultConfig", "Config"]

CONFIG_FILES = {"setup.cfg": "unimport", "pyproject.toml": "tool.unimport"}


class DefaultConfig(NamedTuple):
    sources: List[Path] = [Path(".")]
    include: str = C.INCLUDE_REGEX_PATTERN
    exclude: str = C.EXCLUDE_REGEX_PATTERN
    requirements: bool = False
    gitignore: bool = False
    remove: bool = False
    diff: bool = False
    include_star_import: bool = False
    permission: bool = False
    check: bool = False
    ignore_init: bool = False

    def merge(self, **kwargs):
        diff_dict = set(kwargs) - set(self._asdict())
        # delete keys that are not available.
        for invalid_key in diff_dict:
            del kwargs[invalid_key]
        # delete items if they are the same as default values
        for key, value in kwargs.copy().items():
            if getattr(self, key) == value:
                del kwargs[key]
        config = self._replace(**kwargs)
        diff = kwargs.get("diff") or kwargs.get("permission")
        config = config._replace(
            diff=diff or any((config.diff, config.permission))
        )
        config = config._replace(
            check=kwargs.get("check") or not any((config.diff, config.remove))
        )
        if config.gitignore:
            gitignore_exclude = utils.get_exclude_list_from_gitignore()
            config = config._replace(
                exclude="|".join([config.exclude] + gitignore_exclude)
            )
        if config.ignore_init:
            config = config._replace(
                exclude="|".join([config.exclude, C.INIT_FILE_IGNORE_REGEX])
            )
        return config


class Config:

    default_config = DefaultConfig()

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.section = CONFIG_FILES[config_file.name]

    def parse(self) -> DefaultConfig:
        return getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> DefaultConfig:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.section):

            def get_config_as_list(name: str) -> List[str]:
                return literal_eval(
                    parser.get(
                        self.section,
                        name,
                        fallback=getattr(self.default_config, name),
                    )
                )

            cfg_context = {}
            config_annotations = self.default_config.__annotations__
            for key, value in parser[self.section].items():
                key_type = config_annotations[key]
                if key_type == bool:
                    cfg_context[key] = parser.getboolean(self.section, key)
                elif key_type == str:
                    cfg_context[key] = value  # type: ignore
                elif key_type == List[Path]:
                    cfg_context[key] = [  # type: ignore
                        Path(p) for p in get_config_as_list(key)
                    ]
            return self.default_config._replace(**cfg_context)  # type: ignore
        else:
            return self.default_config

    def parse_toml(self) -> DefaultConfig:
        parsed_toml = toml.loads(self.config_file.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        sources = config.get("sources", self.default_config.sources)
        config["sources"] = [Path(path) for path in sources]
        return self.default_config._replace(**config)
