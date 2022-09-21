import ast
from typing import Any, Callable, TypeVar, Union

import libcst as cst

__all__ = (
    "FunctionT",
    "ASTImportableT",
    "ASTFunctionT",
    "ASTNameType",
    "CFNT",
    "CSTImportT",
)

ASTImportableT = Union[ast.AsyncFunctionDef, ast.Attribute, ast.ClassDef, ast.FunctionDef, ast.Name, ast.alias]
ASTFunctionT = TypeVar("ASTFunctionT", ast.FunctionDef, ast.AsyncFunctionDef)
ASTNameType = Union[ast.Name, ast.Constant]

CFNT = TypeVar("CFNT", ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name)
CSTImportT = TypeVar("CSTImportT", cst.Import, cst.ImportFrom)

FunctionT = TypeVar("FunctionT", bound=Callable[..., Any])
