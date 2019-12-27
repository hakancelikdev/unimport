import token

from brm import NoLineTransposer, TokenTransformer, pattern

from unimport.dedect import DetectUnusedImport

dot_name = "(name( dot name)*)"
newline_group = "(nl|newline)"


class ImportTokenTransformer(TokenTransformer):
    def __init__(self, unused_imports):
        self.unused_imports = unused_imports

    @pattern(
        "name", f"({dot_name}( comma (nl )?{dot_name})*( nl)?)", newline_group,
    )
    def fix_import_statement(self, statement, *tokens):
        if statement.string != "import":
            return

        module = []
        commas = {}
        modules = {}
        newlines = []
        token_info = iter(tokens)

        def add_module(comma):
            pretty_name = "".join(
                token_info.string
                for token_info in module
                if self._get_type(token_info) != token.COMMA
            )
            modules[pretty_name] = module.copy()
            commas[pretty_name] = comma
            module.clear()

        *module_tokens, newline = token_info

        for module_token in module_tokens:
            if self._get_type(module_token) == token.COMMA:
                add_module(module_token)
            elif self._get_type(module_token) == token.NL:
                newlines.append(module_token)
            else:
                module.append(module_token)
        else:
            add_module(None)

        all_imports = tuple(modules.keys())
        first_import = all_imports[0]
        removeds, remove_offset, first_import_offset = 0, 0, 0
        first_import_removed = False
        fixed_tokens = []

        for module, module_tokens in modules.items():
            module_tokens = module_tokens.copy()
            comma = commas.get(module)

            if module in self.unused_imports:
                if module == first_import:
                    first_import_removed = True
                    first_import_offset = -self.directional_length(
                        [module_tokens[0], statement]
                    )

                removeds += 1
                remove_offset += self.directional_length(module_tokens)
                if comma:
                    remove_offset += self.directional_length([comma])
                continue

            if comma:
                module_tokens.append(comma)

            fixed_tokens.extend(
                self.shift_all(module_tokens, x_offset=-remove_offset)
            )

        any_imports = removeds < len(modules)
        if any_imports:
            fixed_tokens.insert(0, statement)

        if fixed_tokens and self._get_type(fixed_tokens[-1]) == token.COMMA:
            remove_offset -= self.directional_length([fixed_tokens[-1]]) + 2
            fixed_tokens.pop()

        if any_imports:
            newline = self.increase(
                newline,
                amount=fixed_tokens[-1].end[1] - newline.start[1],
                page=1,
            )
            fixed_tokens.append(newline)
        else:
            raise NoLineTransposer

        if first_import_removed:
            current_offset = -self.directional_length(
                [fixed_tokens[1], statement]
            )
            current_offset -= first_import_offset
            fixed_tokens = self.shift_after(
                1, fixed_tokens, x_offset=-current_offset
            )

        return self.shift_after(1, fixed_tokens)

    @pattern(
        "name",
        dot_name,
        "name",
        f"({dot_name}( comma {dot_name})*)",
        newline_group,
    )
    def fix_from_import_statement(self, statement, *tokens):
        if statement.string != "from":
            return

        stream_token = iter(tokens)
        module = [next(stream_token)]
        module_parts, current = self.find_module_for_from_import_statement(
            stream_token
        )
        module.extend(module_parts)

        if "".join(token.string for token in module) in self.unused_imports:
            raise NoLineTransposer

        new_imports = self.fix_import_statement(current, *stream_token)
        return [statement, *module, *new_imports]

    def find_module_for_from_import_statement(self, token_iterator):
        module = []
        try:
            current = next(token_iterator)
            while self._get_type(current) == token.DOT:
                module.append(current)
                module.append(next(token_iterator))
                current = next(token_iterator)
        except StopIteration:
            return None
        else:
            return module, current


def get_unused(source):
    "Yield unused imports."
    dedect = DetectUnusedImport(source)
    for imp in dedect.imports:
        len_dot = len(imp["name"].split("."))
        for name in dedect.names:
            if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                break
        else:
            yield imp


def filter_unused_imports(source, unused_imports):
    transformer = ImportTokenTransformer(unused_imports)
    return transformer.transform(source)
