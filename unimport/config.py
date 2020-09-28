import configparser
from ast import literal_eval
from pathlib import Path
from typing import List

import toml

CONFIG_FILES = {"setup.cfg": "unimport", "pyproject.toml": "tool.unimport"}


class Config:
    sources: List[Path] = []
    include: List[str] = []
    exclude: List[str] = []
    requirements = False
    gitignore = False
    remove = False
    diff = False

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.section = CONFIG_FILES[config_file.name]
        self.parse()

    @staticmethod
    def is_available_to_parse(config_path: Path) -> bool:
        return config_path.exists()

    def parse(self) -> None:
        getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> None:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.section):
            sources = literal_eval(
                parser.get(
                    self.section, "sources", fallback=[]  # type: ignore
                )
            )
            self.sources = [Path(path) for path in sources]
            self.include = [parser.get(self.section, "include", fallback="")]  # type: ignore
            self.exclude = [parser.get(self.section, "exclude", fallback="")]  # type: ignore
            self.requirements = parser.getboolean(
                self.section, "requirements", fallback=False
            )
            self.gitignore = parser.getboolean(
                self.section, "gitignore", fallback=False
            )
            self.remove = parser.getboolean(
                self.section, "remove", fallback=False
            )
            self.diff = parser.getboolean(self.section, "diff", fallback=False)

    def parse_toml(self) -> None:
        parsed_toml = toml.loads(self.config_file.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        sources = config.get("sources", [])
        self.sources = [Path(path) for path in sources]
        self.include = [config.get("include", "")]
        self.exclude = [config.get("exclude", "")]
        self.requirements = config.get("requirements", False)
        self.gitignore = config.get("gitignore", False)
        self.remove = config.get("remove", False)
        self.diff = config.get("diff", False)
