from unimport.meta import MakeSingletonWithParams

__all__ = (
    "UnimportBaseException",
    "UnknownConfigKeyException",
    "ConfigFileNotFound",
)


class UnimportBaseException(Exception, metaclass=MakeSingletonWithParams):
    pass


class UnknownConfigKeyException(UnimportBaseException):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self):
        return f"Unknown config key '{self.key}', please read the documentation for more information."


class ConfigFileNotFound(FileNotFoundError, UnimportBaseException):
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def __str__(self):
        return f"Config file not found '{self.config_file}'"


class UnsupportedConfigFile(UnimportBaseException):
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def __str__(self):
        return f"Unsupported config file '{self.config_file}'"
