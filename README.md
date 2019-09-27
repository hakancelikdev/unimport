<h1 align="center">UNIMPORT</h1>
<p align="center">
  To detect unused python libraries.
 </p>

[![MIT License](https://img.shields.io/github/license/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/blob/master/LICENSE) [![releases](https://img.shields.io/github/release/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/releases) [![last-commit](https://img.shields.io/github/last-commit/hakancelik96/unimport.svg)](https://github.com/hakancelik96/unimport/commits/master) [![Codacy Badge](https://img.shields.io/codacy/grade/e8add9e8f86e433696cab7f2e4d9633c)](https://www.codacy.com/app/hakancelik96/unimport) [![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black) [![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort) [![style](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport) [![](https://img.shields.io/github/contributors/hakancelik96/unimport)](https://github.com/hakancelik96/unimport/graphs/contributors) [![](https://pepy.tech/badge/unimport)](https://pepy.tech/badge/unimport)

### 🚀 Installation and Usage 🚀
## Installation
Unimport can be installed by running `pip install unimport`. It requires Python 3.5.0+ to run.

## Usage

unimport {source_file_or_directory} or write direct unimport to current path scan


**Please insert this badge into your project**

`[![](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport)`

[![](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport)

### Another alternative
```python
import inspect
import os
from unimport.unused from get_unused

for unused in get_unused(source=inspect.getsource(os)):
    print(unused)
```

## Configuring Unimport
To configure unimport for a single user create a ~/.unimport.cfg and type the names of folders that you do not want scanning.

**blablabla/.unimport.cfg**
> regex

```
[folders]
.*(some_folder_name_to_ignore)

[files]
.*(some_file_name_to_ignore)
```

## Author

👤 **Hakan Çelik** 👤

- Twitter: [@hakancelik96](https://twitter.com/hakancelik96)
- Github: [@hakancelik96](https://github.com/hakancelik96)

## 📝 License 📝

Copyright © 2019 [Hakan Çelik](https://github.com/hakancelik96/unimport).<br/>
This project is [MIT](https://github.com/hakancelik96/unimport/blob/master/LICENSE) licensed.


## Version Notes

### V0.1.0
- Some class and function name and position changed.
- Future module added to the ignore list.
- Blank python file error fix.
- Default .unimport.cfg and extra_config add
- The new usage style `unimport` to scan from current path

### V0.0.3
- Op system bug fix Linux and win
- File and folders features fix
- Add warning message if no enter any path No paths given 'Usage; unimport {source_file_or_directory}'"

### V0.0.2
- find module bug fix;
For example; module: inspect, name; inspect.getsource; result unused import = inspect that is the wrong result

### V0.0.1
- unimport {source_file_or_directory}
- .unimport.cfg 'type the names of files or folders that you do not want to scan.'
- Does not replace files only shows results.
