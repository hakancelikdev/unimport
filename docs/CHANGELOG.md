# Changelog

All notable changes to this project will be documented in this file.

## 0.12.1

### Fixes

- 🐛 Fix changelog url PR #250 by @hakancelikdev
- 🐛 Fix Name Error PR #250 by @hakancelikdev

## 0.12.0

### Features

- 🔥 Add if condition analysis and 🧪 Refactor PR #247 by @hakancelikdev

  For example;

  ```python
  import sys

  if sys.version_info >= (3, 8):
      from typing import Literal
  else:
      from typing_extensions import Literal
  ```

- 🔥 setup.py remove and pyproject.toml was added. PR #245 by @hakancelikdev

## 0.11.3

### Fixes

- Fix main.py to run unimport

## 0.11.2

### Fixes

- 🐛 Fix Re complile fail mentioning 'ps_d' when using --gitignore PR #241 by
  @hakancelikdev

  For Python 3.7 and above

  - Drop support for patspec, 0.5.0 above and below 0.10.0 versions.
  - Only 0.10.0 and above versions are supported, in these versions the gitignore
    parameter works more accurately.
  - For more accurate results when using --gitignore parameter, please do not use Python
    3.6 and Windows.

### Docs

- 📝 Docs update

### Internal

- 🧪 Refactor main.py and add tests PR #238

## 0.11.1

### Fixes

- 🐛 fix setup

## 0.11.0

- 📝 Update docs
- [Remove requirements feature](https://github.com/hakancelikdev/unimport/pull/234)
  > This feature alone is not enough and can be developed as a new project using
  > unimport, it should not be a feature of unimport.

## 0.10.0

- [🔥 Support Github action](https://github.com/hakancelikdev/unimport/pull/231)
- [🐛 Fix: configurations flow](https://github.com/hakancelikdev/unimport/pull/230)
- [🐛 Fix: exit code behavior](https://github.com/hakancelikdev/unimport/pull/225)

## 0.9.6

- [3.10+ Support 🔥](https://github.com/hakancelikdev/unimport/issues/26)

## 0.9.5

- [🔥 🧪 Refactor: tests using pytest, fix check method](https://github.com/hakancelikdev/unimport/pull/208)

## 0.9.4

- [🔥 🧪 i199 Refactor options & commands & Option color output](https://github.com/hakancelikdev/unimport/pull/205)
- [🔥 Build an Docker image #202](https://github.com/hakancelikdev/unimport/issues/202)

## 0.9.2

- 🐛 Fix setup.py

## 0.9.1

- [🐛 🧪 Fix EOLs not being respected in modified files per #183](https://github.com/hakancelikdev/unimport/pull/193)
  - Respect the file's current EOL (LF/CRLF) instead of the platform default
  - Add unit and integration tests that EOLs are respected

## 0.9.0

- [🔥 🐛 🔥 Scope analyzer; #176, #175 #189](https://github.com/hakancelikdev/unimport/pull/189)
  - Scope analyzer
  - Duplicate import feature has been enabled again.
- [🐛 Fix adding unnecessary rpar in vertical style #86, #190](https://github.com/hakancelikdev/unimport/pull/191)

**İnput**

```python
import sys
from typing import (
    List,
)

test_list: List[str] = ["spam", "eggs"]
```

**Output**

```python
from typing import (
  List,

)

test_list: List[str] = ["spam", "eggs"]
```

## 0.8.4

- [🐛 Fix emoji issues](https://github.com/hakancelikdev/unimport/pull/185)

## 0.8.0

- [👎 Temporarily drop support for duplicate imports.](https://github.com/hakancelikdev/unimport/commit/35fa7239019fc4b4a68c98d3bde64f0302c367f6)

## 0.7.4

- [🐛 Fix list_paths in utils](https://github.com/hakancelikdev/unimport/pull/172)

## 0.7.3

- [🔥 Add `--ignore-init` flag](https://github.com/hakancelikdev/unimport/pull/169)

## 0.7.2

- [🔥 Python3.9 Support](https://github.com/hakancelikdev/unimport/pull/166)

## 0.7.1

- [🐛 Fix #127](https://github.com/hakancelikdev/unimport/pull/161)

## 0.7.0

- [💊 %15 performance increase & remove show-error flag](https://github.com/hakancelikdev/unimport/pull/159)

- [🔥 Star import more accurate suggestion](https://github.com/hakancelikdev/unimport/pull/158)

  - #120 removed to implement it more accurately, later.

- [🐛 Fix: scanner](https://github.com/hakancelikdev/unimport/pull/157)
- [🐛 & 🔥 & 💊 Fix: #150](https://github.com/hakancelikdev/unimport/pull/155)

  - Configuration Bug Fix ( Configuration priority, reading and merge )
  - %136 - %150 performance increase

## 0.6.8

- [🐛 Fix: Extra type check on `utils.is_std`, #148 (#149)](https://github.com/hakancelikdev/unimport/commit/b9e226ef18984189b4154b739b9b186a2c7a2418)
- [🐛 Fix: import skip](https://github.com/hakancelikdev/unimport/issues/146)

## 0.6.6

- [🐛 Fix: call attribute scanner](https://github.com/hakancelikdev/unimport/pull/145)
- [🐛 Fix: requirements feature & star import suggestion](https://github.com/hakancelikdev/unimport/pull/142)
- [🔥 Support multiline skip import only py3.8 and plus](https://github.com/hakancelikdev/unimport/pull/138)
- [🐛 Fix: Initial imports from sys.modules](https://github.com/hakancelikdev/unimport/pull/136)
- [🐛 Fix: import and name matcher](https://github.com/hakancelikdev/unimport/pull/133)
- [🐛 Fix: type comment](https://github.com/hakancelikdev/unimport/pull/130)
- [🔥 Support type variable](https://github.com/hakancelikdev/unimport/pull/128)
- [🐛 Fix same line duplicates](https://github.com/hakancelikdev/unimport/pull/125)
- [🔥 Support Windows OS coloring and encoding](https://github.com/hakancelikdev/unimport/pull/116)

## 0.3.0

- [🐛💊 Fix, improve: Names, Imports and star suggestion](https://github.com/hakancelikdev/unimport/pull/112)
- [🔥💊 Configuration extend and refactoring](https://github.com/hakancelikdev/unimport/pull/111)
- [🔥💊 General refactoring](https://github.com/hakancelikdev/unimport/pull/108)
  - Support append and extend `__all__` list
  - Star import suggestions improved
- [🐛 Fix: Unnecessary refactoring](https://github.com/hakancelikdev/unimport/pull/107)
- [🔥 Support .gitignore exclude patterns](https://github.com/hakancelikdev/unimport/pull/102)
- [💊 Optimize Python >=3.8 type comments support method](https://github.com/hakancelikdev/unimport/pull/95)
- [🔥 Improve test coverage](https://github.com/hakancelikdev/unimport/pull/93)
- [🔥 Support async def](https://github.com/hakancelikdev/unimport/issues/92)

## 0.2.10

- [🐛 Fix: vertical style issue](https://github.com/hakancelikdev/unimport/pull/86)

```python
from foo import (
    Foo,
    Bar,
    FooBar,
)
Foo, Bar
```

- [🐛 Fix: More than one star import exist on the same file.](https://github.com/hakancelikdev/unimport/issues/84)

- [🔥 Getting rid of some bad practice & 🐛 Fix: pre-commit bug](https://github.com/hakancelikdev/unimport/commit/bd93a0cf6b1d5d27bf6a669f2a029faaf225ae5f)

## 0.2.9

- [🔥 Fix: Double underscore in builtins imports](https://github.com/hakancelikdev/unimport/pull/82)
- [🔥 Support for exit code and add some enhancement](https://github.com/hakancelikdev/unimport/pull/81)
- [🔥 Fix: incorrect matching import and name](https://github.com/hakancelikdev/unimport/pull/78)

## 0.2.8

- [🔥 Support: file-wide skips](https://github.com/hakancelikdev/unimport/pull/77)

  - Now, you can skip a file by typing `# unimport: skip_file` anywhere in that file.

- [🔥 Fix: preserve import styles](https://github.com/hakancelikdev/unimport/pull/76)

- [🔥 Support: requirements.txt file](https://github.com/hakancelikdev/unimport/pull/75)

  - Now, You can automatically delete unused modules from the requirements.txt file (
    `unimport --requirements --remove`), see the difference (
    `unimport --requirements --diff`), delete it by requesting permission (
    `unimport --requirements --permission`), or just check ( `unimport --requirements`).

- [🔥 Fix: match error between import name and name](https://github.com/hakancelikdev/unimport/pull/74)

- [🔥 Support for type hints (#58) & string typing @isidentical](https://github.com/hakancelikdev/unimport/pull/71)

```python
from typing import List, TYPE_TEST
test: 'List[TYPE_TEST]'
```

```python
from typing import List, TYPE_TEST
test: "List['TYPE_TEST']"
```

- [🔥 fix: get_suggestion_modules function fix for `__all__` name when import is star](https://github.com/hakancelikdev/unimport/pull/64)

## 0.2.7

- [🔥 If imports inside the `try ... except ImportError, ModuleNotFoundError` block, skip it. ( #46 ) and @isidentical](https://github.com/hakancelikdev/unimport/pull/62)

- [🔥 `--show-error` flag add](https://github.com/hakancelikdev/unimport/pull/61)

- [🐛fix: Skip star imports when the `--include-star-import` flag is not used](https://github.com/hakancelikdev/unimport/pull/60)

- [🐛fix: finding functions during scanning](https://github.com/hakancelikdev/unimport/pull/55)

- [🔥 `#noqa` comment support to skip import (#48)](https://github.com/hakancelikdev/unimport/pull/54)

- [🔥 `typing` imports used in typing comments support only python3.8 (#49)](https://github.com/hakancelikdev/unimport/pull/53)

- [Set default of permission flag as yes (#51)](https://github.com/hakancelikdev/unimport/pull/52)

- [Fix: 'Ignore imports that shadow builtin names' 🐛 🔥 🧪 (#45 & #47)](https://github.com/hakancelikdev/unimport/pull/50)

## 0.2.6.2

- [🐛 Config](https://github.com/hakancelikdev/unimport/commit/ee4dbb1301fef66a0cf99e9cfb9b18c6b2f0587d)

## 0.2.6.1

[PR: 0.2.6](https://github.com/hakancelikdev/unimport/pull/32)

- 🔥 `--include-star-import command add` Include star imports during scanning and
  refactor.

- 🌈 color_diff add It shows the difference between source and refactor better.

- 🐛 All builtins names received during the scan have been fixed. Builtins names will no
  longer be offered as suggestions for star import.

- 🐛 If there is no unused import, the refactor error has been fixed.

- 🔥 Import skip feature has been added. Leave '#unimport: skip' at the end of the line
  to skip imports with some rare cases. **for example:**

```python
try:
  import django #unimport:skip
except ImportError:
  print("install django")
```

- 🔥 Added support for the rare case of **all**. **for example:**

```python
from codeop import compile_command
__all__ = ["compile_command"]
```

Thanks to this feature, we take the values in the `__all__` list and see if there is any
matching import statements. If there isn't, this import is unused import.

- [🔥 Support exclude & include config with regex](https://github.com/hakancelikdev/unimport/pull/36)
  After this feature, we can write the file include and exclude pattern setting with
  regex in the console and in the configuration files.

- [🐛 Show, check and congratulations messages in \__main_](https://github.com/hakancelikdev/unimport/commit/54129bfc9e78f678bb2fea9b2411355d857a0a37)

- [🐛 --include-star-import command refactor & scan](https://github.com/hakancelikdev/unimport/commit/d44b2c6d0c5997fb716d58f00d0d5ab2a8042c26)

- [🐛 \_list_paths in session](https://github.com/hakancelikdev/unimport/commit/179ba9c45031de8d5aa1de43e0449ccdeece8d5e)

- [v0.2.61](https://github.com/hakancelikdev/unimport/commit/dca5265eb4c106aaa190ea67af5f8da46202e00b)

## 0.2.5

[0.2.5](https://github.com/hakancelikdev/unimport/pull/31)

- 🔥 Refactor code rewrite using libcst.
- 🐛 Refactor bugs fix.
- [🧪 Comma rare case support & test.](https://github.com/hakancelikdev/unimport/blob/b8800ec19441bbc452900e1c8b558bea2e43d065/rare_cases/case_comma.py)
- 🔥 pre-commit add & support
- 🐛 Add Sytranx Error Catcher

## 0.2.4

- [🔥 As import refactor support](https://github.com/hakancelikdev/unimport/commit/147ed5e836d6a4589a92db4157bfd299ca935b02)
- [🔥 Duplicate detect and refactor support](https://github.com/hakancelikdev/unimport/pull/23)

## 0.2.2

- [🐛 Fix: Scan & Config - Add test to default exlude](https://github.com/hakancelikdev/unimport/commit/7e789872917c51e5ffa167d26581e5397fd34998)

## 0.2.1

🔥 from x import \* support

- [issue; #19](https://github.com/hakancelikdev/unimport/issues/19)
- [PR; #21](https://github.com/hakancelikdev/unimport/pull/21)

## 0.2.0

- 🔥 Argparse support.

  - [implement an initial arg parser](https://github.com/hakancelikdev/unimport/commit/4e5fbd778112704626c8d708a1077d7d1f345157)
  - [argparse support](https://github.com/hakancelikdev/unimport/commit/837af61fab771b4a09893a7854df42452de7aff9)
  - [argparse (#4)](https://github.com/hakancelikdev/unimport/commit/90cfab776d3e15b417d1566f7ca1b1e2756763dd)
  - Arguments
    - ["-w" / "--write" parameter is fixed in this PR (#9)](https://github.com/hakancelikdev/unimport/commit/5c59f938d3ef3844a5420882ad318a120e4da4af)
    - [#12 diff option & and overwrite permission add](https://github.com/hakancelikdev/unimport/commit/36e7216cd6cc442864460d7b2b7661190c627757)
    - [#12 -dw add](https://github.com/hakancelikdev/unimport/commit/57913e0fb47073f4473e5694470cc2ee9dffdfb6)
    - [#12 bug fix & Some functions have been moved to the corresponding files @hakancelikdev](https://github.com/hakancelikdev/unimport/commit/188370fc7928588a48e9e3dcd0ee70f9f12b733e)
    - [--version add](https://github.com/hakancelikdev/unimport/commit/2112e44e45bc0b34e330bc5320bbcd1462257f1e)
    - [Console Argument (#17)](https://github.com/hakancelikdev/unimport/commit/e4db14dbc74fbc8a51c5d1f62ca9d679af05af9b)

- 🐛 Tests

  - [fix_multiple_problems_at_once_action.py](https://github.com/hakancelikdev/unimport/commit/aee62041b2d625cef0d723c526d5db28d96ce2fd)
  - [test_overwrite source_expected path bug fix](https://github.com/hakancelikdev/unimport/commit/63645dbb4333b3675e57bbc99bddfa133eb33594)

- 🔥 Configuration

  - [example_configuration add](https://github.com/hakancelikdev/unimport/commit/70c70ba0d5ac8f200986c5c0a57acc8ccc574dab)
  - [#8 & glob configuration](https://github.com/hakancelikdev/unimport/commit/c8bd58e28855886c5908a626260820c3894a4600)
  - [ignore config name change as exclude](https://github.com/hakancelikdev/unimport/commit/aef61eb3ddf0c295719dc840390fba16e3d5e3e9)
  - [remove .unimport.cfg](https://github.com/hakancelikdev/unimport/commit/b052ffb336bc0f73a723f5f4938cb7ffb81cd038)
  - [find_config bug fix & console config argument bug fix](https://github.com/hakancelikdev/unimport/commit/860d57791a36c54e1830439bf9e571b1cb608123)

- 🔥 Lib2to3 support

  - [Initial lib2to3 refactor](https://github.com/hakancelikdev/unimport/commit/9030cb2fea518aa9fb887a5d4ef1bb8b34947ed9)
  - [add support for name binding](https://github.com/hakancelikdev/unimport/commit/4a3df83b5b89d00472bed292c23b20693bdf5dd2)
  - [adapt testing suite](https://github.com/hakancelikdev/unimport/commit/c81036fe5b0d845c3220cfda1e4c30250e1107a1)

- 🐛 Bug Fix

  - [setup.cfg bug fix & catch error in detect](https://github.com/hakancelikdev/unimport/commit/a99b3846d55b723a701d6fdbbc7e634772b8c5ba)
  - [get_files bug fix](https://github.com/hakancelikdev/unimport/commit/3d3299f1c82161a8e95d909864ad00dd9fda23f9)
  - [support local imports and @isidentical](https://github.com/hakancelikdev/unimport/commit/8c9b12295cf7c87670a685e59f95f1d83da130f7)

- 💊 Optimization

  - [balamir and @isidentical](https://github.com/hakancelikdev/unimport/commit/d4c1594371e7d3a3646cf2d886e931b50ca104f6)

- 🔥 API Support
  - [General API Cleanup](https://github.com/hakancelikdev/unimport/commit/f3efe4720eaa4eef5d991f838a0bd0872661dfa3)

## 0.1.3

- 🔥 pyproject.toml support
- 🔥 setup.cfg support
- 🧪 test written

## 0.1.0

- 🎉 Some class and function name and position changed.
- 🎉 Future module added to the ignore list.
- 🐛 Blank python file error fix.
- Default .unimport.cfg and extra_config add
- The new usage style `unimport` to scan from current path

## 0.0.3

- 🐛 Op system bug fix Linux and win
- 🐛 File and folders features fix
- 🔥 Add warning message if no enter any path No paths given 'Usage; unimport
  {source_file_or_directory}'"

## 0.0.2

- 🐛 find module bug fix; For example; module: inspect, name; inspect.getsource; result
  unused import = inspect that is the wrong result

## 0.0.1

- unimport {source_file_or_directory}
- .unimport.cfg 'type the names of files or folders that you do not want to scan.'
- Does not replace files only shows results.
