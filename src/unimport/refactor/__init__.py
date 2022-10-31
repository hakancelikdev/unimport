import dataclasses
import tokenize
from typing import List, Union

import libcst as cst

from unimport.refactor.tokenize_utils import comments_to_strings, prepare_tokens, string_to_comments
from unimport.refactor.transformer import RemoveUnusedImportTransformer
from unimport.statement import Import, ImportFrom

__all__ = ("refactor_string",)


@dataclasses.dataclass
class _Refactor:
    source: str
    unused_imports: List[Union[Import, ImportFrom]]

    def __post_init__(self):
        self.tokens = prepare_tokens(self.source)

    def refactor_string(self, source: str) -> str:
        if self.unused_imports:
            wrapper = cst.MetadataWrapper(cst.parse_module(source))
            remove_unused_import_transformer = RemoveUnusedImportTransformer(self.unused_imports)
            fixed_module = wrapper.visit(remove_unused_import_transformer)
            return fixed_module.code

        return source

    def __call__(self, *args, **kwargs) -> str:
        source_without_comments = tokenize.untokenize(comments_to_strings(self.tokens))
        refactored_source_without_comments = self.refactor_string(source_without_comments)
        if refactored_source_without_comments != self.source:
            return tokenize.untokenize(string_to_comments(prepare_tokens(refactored_source_without_comments)))

        return self.source


def refactor_string(source: str, unused_imports: List[Union[Import, ImportFrom]]) -> str:
    refactor = _Refactor(source, unused_imports)
    return refactor()
