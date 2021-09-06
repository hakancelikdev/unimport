import os
import unittest

import unimport.main
import unimport.utils
from tests.utils import reopenable_temp_file


class LineSepTestCase(unittest.TestCase):
    source = "\n".join(
        [
            "import os",
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )
    result = "\n".join(
        [
            "import sys",
            "",
            "print(sys.executable)\n",
        ]
    )

    def test_platform_native_linesep(self):
        with reopenable_temp_file(self.source, newline=os.linesep) as tmp_path:
            unimport.main.main(["--remove", tmp_path.as_posix()])
            with open(tmp_path, encoding="utf-8") as tmp_py_file:
                tmp_py_file.read()
                self.assertEqual(os.linesep, tmp_py_file.newlines)
            self.assertEqual(self.result, unimport.utils.read(tmp_path)[0])

    def test_non_platform_native_linesep(self):
        if os.linesep == "\n":
            non_os_sep = "\r\n"
        else:
            non_os_sep = "\n"
        with reopenable_temp_file(self.source, newline=non_os_sep) as tmp_path:
            unimport.main.main(["--remove", tmp_path.as_posix()])
            with open(tmp_path, encoding="utf-8") as tmp_py_file:
                tmp_py_file.read()
                self.assertEqual(non_os_sep, tmp_py_file.newlines)
            self.assertEqual(self.result, unimport.utils.read(tmp_path)[0])
