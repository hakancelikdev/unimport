import unittest
from unimport.session import Session

# These imports to write in modules below.
import pathlib
import re

class TestDuplicate(unittest.TestCase):
	maxDiff = None

	def setUp(self):
		self.session = Session()

	def test_full_unused(self):
		source = (
			"from x import y\n"
			"from x import y\n"
			"from t import x\n"
			"import re\n"
			"import ll\n"
			"import ll\n"
			"from c import e\n"
			"import e\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'y', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'y', 'star': False
				},
				{
					'lineno': 3, 'module': None, 'name': 'x', 'star': False
				},
				{
					'lineno': 4, 'module': re, 'name': 're', 'star': False
				},
				{
					'lineno': 5, 'module': None, 'name': 'll', 'star': False
				},
				{
					'lineno': 6, 'module': None, 'name': 'll', 'star': False
				},
				{
					'lineno': 7, 'module': None, 'name': 'e', 'star': False
				},
			  	{
				  'lineno': 8, 'module': None, 'name': 'e', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_one_used(self):
		source = (
			"from x import y\n"           # 1 - unused
			"from x import y\n"           # 2 - unused
			"from t import x\n"           # 3 - unused
			"import re\n"                 # 4 - unused
			"import ll\n"                 # 5 - unused
			"import ll\n"                 # 6 - unused
			"from c import e\n"           # 7 - unused
			"import e\n"                  # 8 - unused
			"from pathlib import Path\n"  # 9 - unused
			"from pathlib import Path\n"  # 10 -
			"p = Path()"                  # 11 -
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{'lineno': 1, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 2, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 3, 'name': 'x', 'star': False, 'module': None},
				{'lineno': 4, 'name': 're', 'star': False, 'module': re},
				{'lineno': 5, 'name': 'll', 'star': False, 'module': None},
				{'lineno': 6, 'name': 'll', 'star': False, 'module': None},
				{'lineno': 7, 'name': 'e', 'star': False, 'module': None},
				{'lineno': 8, 'name': 'e', 'star': False, 'module': None},
				{'lineno': 9, 'name': 'Path', 'star': False, 'module': pathlib}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_two_used(self):
		source = (
			"from x import y\n"           # 1 - unused
			"from x import y\n"           # 2 - unused
			"from t import x\n"           # 3 - unused
			"import re\n"                 # 4 - unused
			"import ll\n"                 # 5 - unused
			"import ll\n"                 # 6
			"from c import e\n"           # 7 - unused
			"import e\n"                  # 8 - unused
			"from pathlib import Path\n"  # 9 - unused
			"from pathlib import Path\n"  # 10
			"p = Path()\n"                # 11
			"print(ll)\n"                 # 12
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{'lineno': 1, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 2, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 3, 'name': 'x', 'star': False, 'module': None},
				{'lineno': 4, 'name': 're', 'star': False, 'module': re},
				{'lineno': 7, 'name': 'e', 'star': False, 'module': None},
				{'lineno': 8, 'name': 'e', 'star': False, 'module': None},
				{'lineno': 5, 'name': 'll', 'star': False, 'module': None},
				{'lineno': 9, 'name': 'Path', 'star': False, 'module': pathlib}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_three_used(self):
		source = (
			"from x import y\n"           # 1 - unused
			"from x import y\n"           # 2 - unused
			"from t import x\n"           # 3 - unused
			"import re\n"                 # 4 - unused
			"import ll\n"                 # 5 - unused
			"import ll\n"                 # 6
			"from c import e\n"           # 7 - unused
			"import e\n"                  # 8 -
			"from pathlib import Path\n"  # 9 - unused
			"from pathlib import Path\n"  # 10
			"p = Path()\n"                # 11
			"print(ll)\n"                 # 12
			"def function(e=e):pass\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{'lineno': 1, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 2, 'name': 'y', 'star': False, 'module': None},
				{'lineno': 3, 'name': 'x', 'star': False, 'module': None},
				{'lineno': 4, 'name': 're', 'star': False, 'module': re},
				{'lineno': 5, 'name': 'll', 'star': False, 'module': None},
				{'lineno': 7, 'name': 'e', 'star': False, 'module': None},
				{'lineno': 9, 'name': 'Path', 'star': False, 'module': pathlib}
			], list(self.session.scanner.get_unused_imports())
		)


	def test_different_duplicate_unused(self):
		source = (
			"from x import z\n"
			"from y import z\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'z', 'star': False
				},
				{
					'lineno': 2, 'module': None, 'name': 'z', 'star': False
				}
			], list(self.session.scanner.get_unused_imports())
		)

	def test_different_duplicate_used(self):
		source = (
			"from x import z\n"
			"from y import z\n"
			"print(z)\n"
		)
		self.session.scanner.run_visit(source)
		self.assertEqual(
			[
				{
					'lineno': 1, 'module': None, 'name': 'z', 'star': False
				},
			], list(self.session.scanner.get_unused_imports())
		)
