import configparser
import pathlib
import re
import sys

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

    def __init__(self, config_dir=None):
        self.config_dir = config_dir
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
        for file_name, section in CONFIG_FILES:
            current_dir = pathlib.Path().cwd()
            if self.config_dir is None:
                search_depth = len(current_dir.parts)
            else:
                current_dir /= self.config_dir
                search_depth = 1

            for _ in range(search_depth):
                config_path = current_dir / file_name
                if self.is_available_to_parse(config_path):
                    return config_path, section
                current_dir = current_dir.parent

        return None, None

    def parse(self):
        getattr(self, f"parse_{self.config_path.suffix.strip('.')}", "parse_cfg")()

    def parse_cfg(self):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(self.config_path)

        if self.section is None:

            def get_values(k):
                return parser[k]

        else:

            def get_values(k):
                return parser.get(self.section, k).split()

        self.ignored_folders.update(get_values("folders"))
        self.ignored_files.update(get_values("files"))

    def parse_toml(self):
        parsed_toml = toml.loads(self.config_path.read_text())
        config = parsed_toml.get("tool", {}).get("unimport", {})
        self.ignored_folders.update(set(config.get("folders", [])))
        self.ignored_files.update(set(config.get("files", [])))


config = Config(config_dir=sys.argv[1] if len(sys.argv) >= 2 else None)


def is_ignore_folder(path):
    regex = re.compile("|".join(set(config.ignored_folders)))
    return regex.match(path) is not None


def is_ignore_files(path):
    regex = re.compile("|".join(set(config.ignored_files)))
    return regex.match(path) is not None
