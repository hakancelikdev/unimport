import importlib
import re
from pathlib import Path

import pytest

from unimport.analyzer import Analyzer
from unimport.constants import PY38_PLUS  # noqa using eval expression
from unimport.refactor import refactor_string
from unimport.statement import Import, Name
from unimport.utils import list_paths


@pytest.fixture(scope="session")
def refactor_path():
    return Path("tests/cases/refactor")


@pytest.fixture(scope="session")
def analyzer_path():
    return Path("tests/cases/analyzer")


@pytest.mark.parametrize("path", list(list_paths(Path("tests/cases/source"))))
def test_cases(path: Path, refactor_path: Path, analyzer_path: Path, logger):
    case_path = f"{path.parent.name}/{path.name}"
    analyzer_path_ = analyzer_path / case_path
    refactor_path_ = refactor_path / case_path

    logger.debug(f"Source path: {path}")
    logger.debug(f"Analyzer path: {analyzer_path_}")
    logger.debug(f"Refactor path: {refactor_path_}")

    # analyzer tests
    analyzer_import_path = ".".join(analyzer_path_.parts[:-1])
    analyzer_import_path += f".{path.stem}"
    analyzer = importlib.import_module(analyzer_import_path)

    source = path.read_text()
    if skip := re.search(
        "# skip; condition: (?P<condition>.*), reason: (?P<reason>.*)",
        source,
        re.IGNORECASE,
    ):
        condition = skip.group("condition")
        if condition in ["not PY38_PLUS"] and eval(condition):
            reason = skip.group("reason")
            pytest.skip(reason, allow_module_level=True)

    with Analyzer(source=source, include_star_import=True):
        assert Name.names == analyzer.NAMES
        assert Import.imports == analyzer.IMPORTS
        assert list(Import.get_unused_imports()) == analyzer.UNUSED_IMPORTS

    # refactor tests
    refactor = refactor_string(source, analyzer.UNUSED_IMPORTS)
    refactor_path_.write_text(refactor)
    assert refactor_path_.read_text() == refactor
