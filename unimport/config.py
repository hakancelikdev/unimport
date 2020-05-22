import configparser

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

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config_path, self.section = self.find_config()
        if self.config_path is not None:
            self.parse()

    @staticmethod
    def is_available_to_parse(config_path):
        if config_path.suffix == ".toml" and HAS_TOML is False:
            return False
        return config_path.exists()

    def find_config(self):
        config_files = dict(CONFIG_FILES)
        if (
            self.config_file is not None
            and self.config_file.name in config_files
        ):
            return self.config_file, config_files[self.config_file.name]
        if self.config_file:
            for file_name, section in config_files.items():
                config_path = self.config_file / file_name
                if self.is_available_to_parse(config_path):
                    return config_path, section
        return None, None

    def parse(self):
        getattr(self, f"parse_{self.config_path.suffix.strip('.')}")()

    def parse_cfg(self):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_path)
        for attr in self.attrs:
            setattr(self, attr, parser.get(self.section, attr) or None)

    def parse_toml(self):
        parsed_toml = toml.loads(self.config_path.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        for attr in self.attrs:
            setattr(self, attr, config.get(attr, None))
