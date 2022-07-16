import ast
from typing import Any, Callable, TypeVar, Union

import libcst as cst

from unimport.statement import Import, ImportFrom, Name

__all__ = (
    "FunctionT",
    "ASTImportableT",
    "ASTFunctionT",
    "ImportT",
    "StatementT",
    "ASTImport",
    "ASTNameType",
    "CFNT",
    "CSTImportT",
)

FunctionT = TypeVar("FunctionT", bound=Callable[..., Any])
ASTImportableT = Union[
    ast.AsyncFunctionDef,
    ast.Attribute,
    ast.ClassDef,
    ast.FunctionDef,
    ast.Name,
    ast.alias,
]

ASTFunctionT = TypeVar("ASTFunctionT", ast.FunctionDef, ast.AsyncFunctionDef)
ImportT = Union[Import, ImportFrom]
StatementT = Union[Import, ImportFrom, Name]
ASTImport = Union[ast.Import, ast.ImportFrom]
ASTNameType = Union[ast.Name, ast.Constant]
CFNT = TypeVar(
    "CFNT",
    ast.ClassDef,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.Name,
)
CSTImportT = TypeVar("CSTImportT", cst.Import, cst.ImportFrom)
