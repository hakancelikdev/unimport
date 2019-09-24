<h1 align="center">UNIMPORT</h1>
<p align="center">
  To detect unused python libraries.
 </p>
 <p>
     <a href="https://github.com/hakancelik96/unimport/blob/master/LICENSE" target="_blank">
   <img alt="MIT License" title="MIT License" src="https://img.shields.io/github/license/hakancelik96/unimport.svg"/>
   </a>
   <a href="https://github.com/hakancelik96/unimport/releases" target="_blank">
     <img alt="releases" title="releases" src="https://img.shields.io/github/release/hakancelik96/unimport.svg"/>
   </a>
   <img alt="last-commit" title="last-commit" src="https://img.shields.io/github/last-commit/hakancelik96/unimport.svg"/>
   <a href="https://www.codacy.com/manual/hakancelik96/unimport?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hakancelik96/unimport&amp;utm_campaign=Badge_Grade" target="_blank">
  <img alt="Codacy Badge" title="Codacy Badge" src="https://img.shields.io/codacy/grade/e8add9e8f86e433696cab7f2e4d9633c"/>
   </a>
   <a href="https://github.com/psf/black" target="_blank">
  <img alt="Code style" title="Code style" src="https://img.shields.io/badge/style-black-black"/>
   </a>
    <a href="https://github.com/timothycrosley/isort" target="_blank">
  <img alt="Code style" title="Code style" src="https://img.shields.io/badge/style-isort-lightgrey"/>
   </a>
  <a href="https://pepy.tech/badge/unimport" target="_blank" title="Downloads">
    <img alt="pepy" title="pepy" src="https://pepy.tech/badge/unimport"/>
   </a>
  <br>
 </p>

### 🚀 Installation and Usage 🚀
## Installation
Unimport can be installed by running `pip install unimport`. It requires Python 3.5.0+ to run.

## Usage

unimport {source_file_or_directory} or write direct unimport to current path scan


**Please insert this badge into your project**

`[![](https://img.shields.io/badge/Unnecessary%20library%20detection-unimport-green)](https://github.com/hakancelik96/unimport)`

[![](https://img.shields.io/badge/Unnecessary%20library%20detection-unimport-green)](https://github.com/hakancelik96/unimport)

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

```
[extra_ignore]
.*(some_folder_name)
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
