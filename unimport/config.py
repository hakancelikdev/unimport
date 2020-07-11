import configparser
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

HAS_TOML: bool

try:
    import toml
except ImportError:
    HAS_TOML = False
else:
    HAS_TOML = True

CONFIG_FILES: Dict[str, str] = {"setup.cfg": "unimport"}

if HAS_TOML is True:
    CONFIG_FILES.update({"pyproject.toml": "tool.unimport"})


class Config:
    attrs: Tuple[str, str] = ("include", "exclude")

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.section = CONFIG_FILES[config_file.name]
        self.parse()

    @staticmethod
    def is_available_to_parse(config_path: Path) -> bool:
        if config_path.suffix == ".toml" and HAS_TOML is False:
            return False
        return config_path.exists()

    def parse(self) -> None:
        getattr(self, f"parse_{self.config_file.suffix.strip('.')}")()

    def parse_cfg(self) -> None:
        parser: configparser.ConfigParser = configparser.ConfigParser(
            allow_no_value=True
        )
        parser.read(self.config_file)
        if parser.has_section(self.section):
            for attr in self.attrs:
                get_value: Optional[str] = parser.get(self.section, attr)
                if get_value:
                    setattr(self, attr, get_value)

    def parse_toml(self) -> None:
        parsed_toml: MutableMapping[str, Any] = toml.loads(
            self.config_file.read_text()
        )
        config: Dict[str, str] = parsed_toml.get("tool", {}).get(
            "unimport", {}
        )
        for attr in self.attrs:
            get_value: Optional[str] = config.get(attr, None)
            if get_value:
                setattr(self, attr, get_value)
