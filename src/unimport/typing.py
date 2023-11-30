import ast
import typing

import libcst as cst

__all__ = (
    "FunctionT",
    "ASTImportableT",
    "ASTFunctionT",
    "ASTNameType",
    "CFNT",
    "CSTImportT",
)

ASTImportableT = typing.Union[ast.AsyncFunctionDef, ast.Attribute, ast.ClassDef, ast.FunctionDef, ast.Name, ast.alias]
ASTFunctionT = typing.TypeVar("ASTFunctionT", ast.FunctionDef, ast.AsyncFunctionDef)
ASTNameType = typing.Union[ast.Name, ast.Constant]

CFNT = typing.TypeVar("CFNT", ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Name)
CSTImportT = typing.TypeVar("CSTImportT", cst.Import, cst.ImportFrom)

FunctionT = typing.TypeVar("FunctionT", bound=typing.Callable[..., typing.Any])
