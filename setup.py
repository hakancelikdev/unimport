import sys
from pathlib import Path

from setuptools import setup

assert sys.version_info >= (3, 5, 0), "umimport requires Python 3.5+"

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="unimport",
    version="0.0.2",
    description="",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=["unused", "import"],
    author="Hakan Çelik",
    author_email="hakancelik96@outlook.com",
    url="https://github.com/hakancelik96/unimport",
    license="MIT",
    python_requires=">=3.5.0",
    py_modules=["unimport"],
    packages=[],
    zip_safe=False,
    package_data={},
    include_package_data=True,
    install_requires=[],
    extras_require={},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["unimport=unimport:unimport"]},
)
