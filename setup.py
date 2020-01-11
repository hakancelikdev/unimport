import sys
from pathlib import Path

from setuptools import setup

import unimport

assert sys.version_info >= (3, 6, 0), "unimport requires Python 3.6+"

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="unimport",
    version=unimport.__version__,
    description=unimport.__description__,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=["unused", "import"],
    author=unimport.__author__,
    author_email="hakancelik96@outlook.com",
    url="https://github.com/hakancelik96/unimport",
    license="MIT",
    python_requires=">=3.6.0",
    packages=["unimport"],
    dependency_links=[
        "https://github.com/isidentical/BRM/tarball/master#egg=brm-0.1.0b0"
    ],
    install_requires=["brm"],
    extras_require={"pyproject": ["toml"]},
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": ["unimport = unimport.console:console_scripts"]
    },
)
