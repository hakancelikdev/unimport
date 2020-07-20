import configparser
from pathlib import Path

try:
    import toml
except ImportError:
    HAS_TOML = False
else:
    HAS_TOML = True

CONFIG_FILES = {"setup.cfg": "unimport"}

if HAS_TOML is True:
    CONFIG_FILES.update({"pyproject.toml": "tool.unimport"})


class Config:
    attrs = ("include", "exclude")

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
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_file)
        if parser.has_section(self.section):
            for attr in self.attrs:
                get_value = parser.get(self.section, attr)
                if get_value:
                    setattr(self, attr, get_value)

    def parse_toml(self) -> None:
        parsed_toml = toml.loads(self.config_file.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        for attr in self.attrs:
            get_value = config.get(attr, None)
            if get_value:
                setattr(self, attr, get_value)
