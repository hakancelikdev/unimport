import sys
from pathlib import Path

from setuptools import setup

import unimport.constants as C

assert sys.version_info >= (3, 6), "unimport requires Python 3.6+"

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="unimport",
    version=C.VERSION,
    description=C.DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=["unused", "import"],
    author="Hakan Çelik",
    author_email="hakancelik96@outlook.com",
    url="https://github.com/hakancelik96/unimport",
    project_urls={
        "Documentation": "https://unimport.hakancelik.dev/",
        "Issues": "https://github.com/hakancelik96/unimport/issues",
    },
    license="MIT",
    license_file="LICENSE",
    python_requires=">=3.6",
    packages=["unimport"],
    install_requires=[
        "libcst==0.3.16",
        "pathspec==0.8.1",
        "toml==0.10.2",
        "importlib_metadata==3.4.0",
    ],
    extras_require={},
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["unimport = unimport.__main__:main"]},
)
