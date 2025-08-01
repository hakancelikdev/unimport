import contextlib
import importlib
import re
from pathlib import Path

import pytest

from unimport.analyzers import MainAnalyzer
from unimport.constants import PY310_PLUS, PY312_PLUS, PY313_PLUS  # noqa using eval expression
from unimport.refactor import refactor_string
from unimport.statement import Import, Name
from unimport.utils import list_paths


@pytest.mark.parametrize("path", list(list_paths(Path("tests/cases/source"))))
def test_cases(path: Path, logger):
    refactor_path = Path("tests/cases/refactor")
    analyzer_path = Path("tests/cases/analyzer")

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
    skip_if = re.search(r"# pytest.mark.skipif\((?P<condition>.*), reason: (?P<reason>.*)\)", source, re.IGNORECASE)
    if (
        skip_if
        and (condition := skip_if.group("condition"))
        and condition in ("not PY310_PLUS", "not PY312_PLUS", "not PY313_PLUS")
    ):
        reason = skip_if.group("reason")
        pytest.mark.skipif(False, reason, allow_module_level=True)

    with contextlib.suppress(SyntaxError):
        with MainAnalyzer(source=source, include_star_import=True):
            assert Name.names == analyzer.NAMES
            assert Import.imports == analyzer.IMPORTS
            assert list(Import.get_unused_imports()) == analyzer.UNUSED_IMPORTS

    # refactor tests
    refactor = refactor_string(source, analyzer.UNUSED_IMPORTS)
    assert refactor == refactor_path_.read_text()
