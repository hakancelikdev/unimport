def main():
    from unimport.color import paint
    from unimport.enums import Color, Emoji
    from unimport.main import Main

    main = Main.run()
    if not main.is_unused_imports and main.config.check:
        print(
            paint(
                f"{Emoji.STAR} Congratulations there is no unused import in your project. {Emoji.STAR}",
                Color.GREEN,
                main.config.use_color,
            )
        )

    raise SystemExit(main.exit_code())


if __name__ == "__main__":
    main()
