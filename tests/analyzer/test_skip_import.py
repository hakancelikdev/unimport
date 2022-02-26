import textwrap

import pytest

from unimport.analyzer import Analyzer
from unimport.constants import PY38_PLUS
from unimport.statement import Import, Name


def test_inside_try_except():
    source = """\
        try:
           import django
        except ImportError:
           print('install django')
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == [
            Name(lineno=3, name="ImportError"),
            Name(lineno=4, name="print"),
        ]


def test_as_import():
    source = "from x import y as z # unimport:skip"

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_ongoing_comment():
    source = "import unimport # unimport:skip import test"

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_skip_comment_second_option():
    source = "import x # unimport:skip test"

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_noqa_skip_comment():
    source = "from x import (t, y, f, r) # noqa"

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_noqa_skip_comment_multiple():
    source = """\
        from x import ( # noqa
           t, y,
           f, r
        )
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_skip_file():
    source = """\
        # unimport:skip_file
        import x"
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_skip_file_after_import():
    source = """\
        import x
        # unimport:skip_file
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


def test_skip_comment_after_any_comment():
    source = "import x # any test comment unimport:skip any test comment"

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []


@pytest.mark.skipif(
    not PY38_PLUS, reason="This feature is only available for python 3.8."
)
def test_skip_comment_multiline():
    source = """\
        from package import (
            module
        ) # unimport: skip
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == []

    source = """\
        import x
        import y
        from package import (
            module,
            module,
            module,
        )  # unimport: skip
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == [
            Import(lineno=1, column=1, name="x", package="x"),
            Import(lineno=2, column=1, name="y", package="y"),
        ]


def test_space_between():
    """https://github.com/hakancelik96/unimport/issues/146."""

    source = """\
        import math

        import collections  # noqa
        """

    with Analyzer(source=textwrap.dedent(source)):
        assert Name.names == []
        assert Import.imports == [
            Import(lineno=1, column=1, name="math", package="math"),
        ]
