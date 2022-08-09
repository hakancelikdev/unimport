from unimport import color, emoji
from unimport.main import Main

if __name__ == "__main__":
    main = Main.run()
    if not main.is_unused_imports and main.config.check:
        print(
            color.paint(
                f"{emoji.STAR} Congratulations there is no unused import in your project. {emoji.STAR}",
                color.GREEN,
                main.config.use_color,
            )
        )

    raise SystemExit(main.exit_code())
