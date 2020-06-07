import configparser
from pathlib import PosixPath
from typing import Optional, Tuple, Union

try:
    import toml

    HAS_TOML = True
except ImportError:
    HAS_TOML = False

CONFIG_FILES = {"setup.cfg": "unimport"}

if HAS_TOML is True:
    CONFIG_FILES.update({"pyproject.toml": "tool.unimport"})


class Config:
    attrs = ["include", "exclude"]

    def __init__(self, config_file: Optional[PosixPath] = None) -> None:
        self.config_file = config_file
        self.config_path, self.section = self.find_config()
        if self.config_path is not None and self.section is not None:
            self.parse()

    @staticmethod
    def is_available_to_parse(config_path: PosixPath) -> bool:
        if config_path.suffix == ".toml" and HAS_TOML is False:
            return False
        return config_path.exists()

    def find_config(self) -> Union[Tuple[None, None], Tuple[PosixPath, str]]:
        config_files = dict(CONFIG_FILES)
        if (
            self.config_file is not None
            and self.config_file.name in config_files
        ):
            return self.config_file, config_files[self.config_file.name]
        return None, None

    def parse(self) -> None:
        getattr(self, f"parse_{self.config_path.suffix.strip('.')}")()

    def parse_cfg(self) -> None:
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_path)
        if parser.has_section(self.section):
            for attr in self.attrs:
                get_value = parser.get(self.section, attr)
                if get_value:
                    setattr(self, attr, get_value)

    def parse_toml(self) -> None:
        parsed_toml = toml.loads(self.config_path.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        for attr in self.attrs:
            get_value = config.get(attr, None)
            if get_value:
                setattr(self, attr, get_value)
