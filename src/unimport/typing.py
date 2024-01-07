import ast
import typing

import libcst as cst

__all__ = (
    "FunctionT",
    "ASTImportableT",
    "ASTFunctionT",
    "CFNT",
    "CSTImportT",
)

ASTImportableT = typing.Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Attribute, ast.Name, ast.alias]
ASTFunctionT = typing.TypeVar("ASTFunctionT", ast.FunctionDef, ast.AsyncFunctionDef)

CFNT = typing.TypeVar("CFNT", ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name)
CSTImportT = typing.TypeVar("CSTImportT", cst.Import, cst.ImportFrom)

FunctionT = typing.TypeVar("FunctionT", bound=typing.Callable[..., typing.Any])
