import configparser
import pathlib

try:
    import toml

    HAS_TOML = True
except ImportError:
    HAS_TOML = False

DEFAULT_CONFIG_NAME = ".unimport.cfg"
CONFIG_FILES = [(DEFAULT_CONFIG_NAME, None), ("setup.cfg", "unimport")]

if HAS_TOML is True:
    CONFIG_FILES.insert(1, ("pyproject.toml", "tool.unimport"))

DEFAULT_IGNORED_FOLDERS = {
    ".*(.git)",
    ".*(.github)",
    ".*(build)",
    ".*(__pycache__)",
    ".*(develop-eggs)",
    ".*(dist)",
    ".*(downloads)",
    ".*(eggs)",
    ".*(lib)",
    ".*(lib64)",
    ".*(parts)",
    ".*(sdist)",
    ".*(var)",
    ".*(wheels)",
    ".*(.egg-info)",
    ".*(MANIFEST)",
    ".*(htmlcov)",
    ".*(.tox)",
    ".*(.hypothesis)",
    ".*(.pytest_cache)",
    ".*(instance)",
    ".*(docs)",
    ".*(target)",
    ".*(celerybeat-schedule)",
    ".*(.venv)",
    ".*(env)",
    ".*(venv)",
    ".*(site)",
    ".*(.mypy_cache)",
}
DEFAULT_IGNORED_FILES = {".*(.sage.py)", ".*(local_settings.py)"}


class Config(object):
    ignored_folders = set()
    ignored_files = set()

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config_path, self.section = self.find_config()
        if self.config_path is not None:
            self.parse()

        self.ignored_folders.update(DEFAULT_IGNORED_FOLDERS)
        self.ignored_files.update(DEFAULT_IGNORED_FILES)

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

        for file_name, section in config_files.items():
            current_dir = pathlib.Path().cwd()
            search_depth = len(current_dir.parts)

            for _ in range(search_depth):
                config_path = current_dir / file_name
                if self.is_available_to_parse(config_path):
                    return config_path, section
                current_dir = current_dir.parent

        return None, None

    def parse(self):
        getattr(
            self, f"parse_{self.config_path.suffix.strip('.')}", "parse_cfg"
        )()

    def parse_cfg(self):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_path)

        if self.section is None:

            def get_values(k):
                return parser[k]

        else:

            def get_values(k):
                if parser.has_section(self.section):
                    return parser.get(self.section, k).split()
                return []

        self.ignored_folders.update(get_values("folders"))
        self.ignored_files.update(get_values("files"))

    def parse_toml(self):
        parsed_toml = toml.loads(self.config_path.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        self.ignored_folders.update(set(config.get("folders", [])))
        self.ignored_files.update(set(config.get("files", [])))
