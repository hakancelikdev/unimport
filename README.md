<h1 align="center">UNIMPORT</h1>
<p align="center">
  The purpose of this library is to detect unused python libraries.
 </p>
 <p>
   <a href="https://github.com/hakancelik96/unimport/blob/master/LICENSE" target="_blank">
   <img alt="MIT License" title="MIT License" src="https://img.shields.io/github/license/hakancelik96/unimport.svg"/>
   </a>
   <a href="https://github.com/hakancelik96/unimport/releases" target="_blank">
     <img alt="releases" title="releases" src="https://img.shields.io/github/release/hakancelik96/unimport.svg"/>
   </a>
   <img alt="last-commit" title="last-commit" src="https://img.shields.io/github/last-commit/hakancelik96/unimport.svg"/>
   <a href="https://www.codacy.com/app/hakancelik96/coogger?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hakancelik96/unimport&amp;utm_campaign=Badge_Grade" target="_blank">
  <img alt="Codacy Badge" title="Codacy Badge" src="https://img.shields.io/codacy/grade/e8add9e8f86e433696cab7f2e4d9633c"/>
   </a>
   <a href="https://github.com/psf/black" target="_blank">
  <img alt="Code style" title="Code style" src="https://img.shields.io/badge/Code%20style-black-black"/>
   </a>
    <a href="https://github.com/timothycrosley/isort" target="_blank">
  <img alt="Code style" title="Code style" src="https://img.shields.io/badge/code%20style-isort-lightgrey"/>
   </a>
   <br>
  <a href="https://pepy.tech/badge/unimport" target="_blank" title="Downloads">
    <img alt="pepy" title="pepy" src="https://pepy.tech/badge/unimport"/>
   </a>
 </p>

### 🚀 Installation and Usage 🚀
## Installation
Unimport can be installed by running `pip install unimport`. It requires Python 3.5.0+ to run.

## Usage

unimport {source_file_or_directory}

## Configuring Unimport
To configure unimport for a single user create a ~/.unimport.cfg and type the names of files or folders that you do not want scanning.

for example;

To django project
**blablabla/.unimport.cfg**
```
__init__.py
apps.py
migrations
manage.py
```

## Author

👤 **Hakan Çelik** 👤

- Twitter: [@hakancelik96](https://twitter.com/hakancelik96)
- Github: [@hakancelik96](https://github.com/hakancelik96)

## 📝 License 📝

Copyright © 2019 [Hakan Çelik](https://github.com/hakancelik96/unimport).<br/>
This project is [MIT](https://github.com/hakancelik96/unimport/blob/master/LICENSE) licensed.
