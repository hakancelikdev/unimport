import sys
from typing import Optional, Sequence

from unimport import color, commands, emoji, utils
from unimport.analyzer import Analyzer
from unimport.commands import generate_parser
from unimport.config import ParseConfig
from unimport.refactor import refactor_string
from unimport.statement import Import
from unimport.utils import return_exit_code

__all__ = ("main",)


def main(argv: Optional[Sequence[str]] = None) -> int:
    config = ParseConfig.parse_args(
        generate_parser().parse_args(
            argv if argv is not None else sys.argv[1:]
        )
    )
    unused_import_names, is_syntax_error, refactor_applied = (
        set(),
        False,
        False,
    )
    for path in config.get_paths():
        source, encoding, newline = utils.read(path)

        analysis = Analyzer(
            source=source,
            path=path,
            include_star_import=config.include_star_import,
        )
        try:
            analysis.traverse()
        except SyntaxError as exc:
            print(
                color.paint(str(exc), color.RED)
                + " at "
                + color.paint(path.as_posix(), color.GREEN)
            )
            is_syntax_error = True
            continue

        unused_imports = list(
            Import.get_unused_imports(config.include_star_import)
        )
        unused_import_names.update({imp.name for imp in unused_imports})
        analysis.clear()

        if config.check:
            commands.check(path, unused_imports, config.use_color)
        if any((config.diff, config.remove)):
            refactor_result = refactor_string(
                source=source, unused_imports=unused_imports
            )
            if config.diff:
                exists_diff = commands.diff(path, source, refactor_result)
                if config.permission and exists_diff:
                    commands.permission(
                        path,
                        encoding,
                        newline,
                        refactor_result,
                        config.use_color,
                    )
            if config.remove and source != refactor_result:
                commands.remove(
                    path, encoding, newline, refactor_result, config.use_color
                )
                refactor_applied = True

    if not unused_import_names and config.check:
        print(
            color.paint(
                f"{emoji.STAR} Congratulations there is no unused import in your project. {emoji.STAR}",
                color.GREEN,
                config.use_color,
            )
        )

    return return_exit_code(
        is_unused_import_names=bool(unused_import_names),
        is_syntax_error=is_syntax_error,
        refactor_applied=refactor_applied,
    )


if __name__ == "__main__":
    raise SystemExit(main())
