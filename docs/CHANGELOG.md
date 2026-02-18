# Changelog

All notable changes to this project will be documented in this file.

## [1.3.1] - 2026-02-18

### Fixed

- Fix false positive when import and usage are on the same semicolon-separated line
  [#292](https://github.com/hakancelikdev/unimport/issues/292)
- Fix nested if statement dispatch not recognized (e.g. TYPE_CHECKING inside version
  check) [#294](https://github.com/hakancelikdev/unimport/issues/294)
- Fix incorrect removal of runtime import shadowed by TYPE_CHECKING import
  [#313](https://github.com/hakancelikdev/unimport/issues/313)
- Fix import after use in function incorrectly removed
  [#178](https://github.com/hakancelikdev/unimport/issues/178)
- Fix subpackage import incorrectly removed when sibling subpackage is used
  [#180](https://github.com/hakancelikdev/unimport/issues/180)
- Fix/deduplicate clashing star import suggestions
- Preserve comments when removing unused imports

## [1.3.0] - 2025-08-01

### Added

- Python 3.13 support added

### Changed

- Python 3.8 support dropped
  - Updated minimum Python version requirement from 3.8+ to 3.9+
  - Removed Python 3.8 from CI/CD pipeline and testing environments
  - Updated all configuration files to reflect Python 3.9+ support
- Upgraded all package versions in use

### Fixed

- Replace deprecated lib2to3 imports with ast module in test cases
  - Fixed deprecation warning in Python 3.10+ compatibility
  - Updated test cases to use modern ast module instead of deprecated lib2to3 package
  - All tests now pass without deprecation warnings

## [1.2.1] - 2023-12-24

### Added

- Python 3.12 support added

## [1.2.0] - 2023-12-22

### Changed

- Python 3.6 support dropped
- Python 3.7 support dropped

### Fixed

- Improved Type Comment Analysis

  > To ensure accurate type comment analysis, a crucial fix was implemented in the code.
  > The update involves refining the process by adding a check within ast.AnnAssign and
  > ast.arg types. Specifically, the code now includes a verification that
  > visit_Constant occurs under an annotation, addressing unnecessary name discovery
  > issues for better accuracy in type_comment assessment.

  ```python
  import sys
  from typing import (
      List,
  )


  test_list: List[str] = ["spam", "eggs"]  # it thought spam and eggs were a ast.Name object.
  ```

## [1.1.0] - 2023-11-17

### Added

- Support for Python version 3.11.

## [1.0.1] - 2023-11-17

### Changed

- Implement `strtobool` function (and remove distutils dependency)
  [#297](https://github.com/hakancelikdev/unimport/issues/297)

## [1.0.0] - 2023-07-07

### Added

- Automatically pick up config options from setup.cfg if it is present in the project
  root else check and if it exists use pyproject.toml.
  [#256](https://github.com/hakancelikdev/unimport/issues/256)

  If you want you can disable this feature by passing `--disable-auto-discovery-config`

- Add github-action [#229](https://github.com/hakancelikdev/unimport/issues/229)
- Add support like command line commands in configuration files. #287

### Fixed

- ignore-init setting is not working from command line call
  [#263](https://github.com/hakancelikdev/unimport/issues/263)
- Running without options or a config file
  [#281](https://github.com/hakancelikdev/unimport/issues/281)
- Attribute as import refactor #284

### Changed

- Raise more human-readable exceptions when the key is mistyped in the configuration
  [#286](https://github.com/hakancelikdev/unimport/issues/286)

## [0.16.1] - 2023-07-05

### Fixed

- Fix: ignore-init setting is not working from command line call
  [#263](https://github.com/hakancelikdev/unimport/issues/263)

## [0.16.0] - 2023-04-04

### Added

- Add support like command line commands in configuration files. #287

### Changed

- Raise more human-readable exceptions when the key is mistyped in the configuration.
  #286

## [0.15.0] - 2023-03-31

### Fixed

- Fix: attribute as import refactor #284

## [0.14.1] - 2023-02-04

### Fixed

- Running without options or a config file #281.

## [0.14.0] - 2023-02-03

### Added

- Automatically pick up config options from setup.cfg if it is present in the project
  root else check and if it exists use pyproject.toml. #256

  If you want you can disable this feature by passing `--disable-auto-discovery-config`

## [0.13.0] - 2023-02-01

### Changed

- The remove command is set to the default behavior. #273

### Fixes

- pre-commit autoupdate yields a weird result #275

## [0.12.3] - 2022-12-04

### Added

- Multiple versions of the docs

## [0.12.2] - 2022-11-09

### 🐛 Fixes

- `--color=never` is now respected when showing the diffs

## 0.12.1

### 🐛 Fixes

- Changelog url PR #250
- Name Error PR #250

## 0.12.0

### 🔥 Features

- Add if condition analysis and 🧪 Refactor PR #247

  For example;

  ```python
  import sys

  if sys.version_info >= (3, 8):
      from typing import Literal
  else:
      from typing_extensions import Literal
  ```

- setup.py remove and pyproject.toml was added. PR #245

## 0.11.3

### 🐛 Fixes

- Fix main.py to run unimport

## 0.11.2

### 🐛 Fixes

- Re complile fail mentioning 'ps_d' when using --gitignore PR #241

### Internal

For Python 3.7 and above

- Drop support for patspec, 0.5.0 above and below 0.10.0 versions.
- Only 0.10.0 and above versions are supported, in these versions the gitignore
  parameter works more accurately.
- For more accurate results when using --gitignore parameter, please do not use Python
  3.6 and Windows.

### 📝 Docs

- Docs update

### Internal

- Refactor main.py and add tests PR #238

## 0.11.1

### 🐛 Fixes

- Setup

## 0.11.0

### 📝 Docs

- Update docs

### Deprecated

- Remove requirements feature PR #234
  > This feature alone is not enough and can be developed as a new project using
  > unimport, it should not be a feature of unimport.

## 0.10.0

### 🐛 Fixes

- Configurations flow PR #230
- Exit code behavior PR #225

### Internal

- 🔥 Support Github action PR #231

## 0.9.6

### Internal

- 3.10+ Support 🔥 PR #26

## 0.9.5

### 🐛 Fixes

- Refactor: tests using pytest, fix check method PR #208

## 0.9.4

### 🐛 Fixes

- i199 Refactor options & commands & Option color output PR #205

### Internal

- 🔥 Build Docker image PR #202

## 0.9.2

### 🐛 Fixes

- setup.py

## 0.9.1

### 🐛 Fixes

- EOLs not being respected in modified files per PR #193
  - Respect the file's current EOL (LF/CRLF) instead of the platform default
  - Add unit and integration tests that EOLs are respected

## 0.9.0

### 🔥 Features

- Scope analyzer PR #189
  - Scope analyzer
  - Duplicate import feature has been enabled again.

### 🐛 Fixes

- Adding unnecessary rpar in vertical style PR #191

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

### 🐛 Fixes

- Emoji issues PR #185

## 0.8.0

- 👎 Temporarily drop support for duplicate imports. Commit ->
  [35fa7239019fc4b4a68c98d3bde64f0302c367f6](https://github.com/hakancelikdev/unimport/commit/35fa7239019fc4b4a68c98d3bde64f0302c367f6)

## 0.7.4

### 🐛 Fixes

- list_paths in utils PR #172

## 0.7.3

### 🔥 Features

- Add `--ignore-init` flag PR #169

## 0.7.2

### 🔥 Features

- Python3.9 Support PR #166

## 0.7.1

### 🐛 Fixes

- Fix PR #161

## 0.7.0

### 🔥 Features

- Star import more accurate suggestion PR #158

### Internal

- %15 performance increase & remove show-error flag PR #159

### 🐛 Fixes

- Fix: scanner PR #157
- PR #155
  - Configuration Bug Fix ( Configuration priority, reading and merge )
  - %136 - %150 performance increase

## 0.6.8

### 🐛 Fixes

- Extra type check on `utils.is_std`, Commit
  [b9e226ef18984189b4154b739b9b186a2c7a2418](https://github.com/hakancelikdev/unimport/commit/b9e226ef18984189b4154b739b9b186a2c7a2418)
- Import skip PR #147

## 0.6.6

### 🔥 Features

- Support multiline skip import only py3.8 and plus PR #138
- Support type variable PR #128
- Support Windows OS coloring and encoding PR #116

### 🐛 Fixes

- Call attribute scanner PR #145
- Requirements feature & star import suggestion PR #142
- Initial imports from sys.modules PR #136
- Import and name matcher PR #133
- Type comment PR #130
- Same line duplicates PR #125

## 0.3.0

### 🔥 Features

- Configuration extend and refactoring PR #111
- General refactoring PR #108
  - Support append and extend `__all__` list
  - Star import suggestions improved
- Support .gitignore exclude patterns PR #102
- Support async def Issue #92

### 🐛 Fixes

- Improve: Names, Imports and star suggestion PR #112
- Unnecessary refactoring PR #107

### Internal

- Optimize Python >=3.8 type comments support method PR #95
- Improve test coverage PR #93

## 0.2.10

### 🔥 Features

- Getting rid of some bad practice & Fix: pre-commit bug
  [bd93a0cf6b1d5d27bf6a669f2a029faaf225ae5f](https://github.com/hakancelikdev/unimport/commit/bd93a0cf6b1d5d27bf6a669f2a029faaf225ae5f)

### 🐛 Fixes

- Vertical style issue PR #86

```python
from foo import (
    Foo,
    Bar,
    FooBar,
)
Foo, Bar
```

- More than one star import exist on the same file. Commit
  [46e585044f690413c198ac7f356f9a5ef21597bc](https://github.com/hakancelikdev/unimport/commit/46e585044f690413c198ac7f356f9a5ef21597bc)

## 0.2.9

### 🔥 Features

- Support for exit code and add some enhancement PR #81

### 🐛 Fixes

- Double underscore in builtins imports PR #82
- Incorrect matching import and name PR #78

## 0.2.8

### 🔥 Features

- Support: file-wide skips PR #77
  - Now, you can skip a file by typing `# unimport: skip_file` anywhere in that file.
- Support: requirements.txt file PR #75
  - Now, You can automatically delete unused modules from the requirements.txt file (
    `unimport --requirements --remove`), see the difference (
    `unimport --requirements --diff`), delete it by requesting permission (
    `unimport --requirements --permission`), or just check ( `unimport --requirements`).
- Support for type hints (#58) & string typing PR #71

```python
from typing import List, TYPE_TEST
test: 'List[TYPE_TEST]'
```

```python
from typing import List, TYPE_TEST
test: "List['TYPE_TEST']"
```

### 🐛 Fixes

- Preserve import styles PR #76
- Match error between import name and name PR #74
- get_suggestion_modules function fix for `__all__` name when import is star PR #64
