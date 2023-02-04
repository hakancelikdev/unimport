import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def non_native_linesep() -> str:
    """Return an end of line character not native to the current platform."""
    return "\r\n" if os.linesep == "\n" else "\n"


@pytest.fixture(scope="session")
def logger():
    import logging

    logger = logging.getLogger("unimport/tests")
    logger.setLevel(level=logging.DEBUG)

    return logger


def pytest_configure(config):
    config.addinivalue_line("markers", "change_directory(path:str): mark test to change working directory")


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="change_directory"):
        item.original_cwd = Path.cwd()

        directory = marker.args[0]
        os.chdir(directory)


def pytest_runtest_teardown(item, nextitem):
    for marker in item.iter_markers(name="change_directory"):
        os.chdir(item.original_cwd)
