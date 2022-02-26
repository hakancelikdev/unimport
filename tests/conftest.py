import os

import pytest


@pytest.fixture(scope="session")
def non_native_linesep() -> str:
    """Return an end of line character not native to the current platform."""
    return "\r\n" if os.linesep == "\n" else "\n"
