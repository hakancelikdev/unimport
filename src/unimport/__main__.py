def main():
    from unimport import emoji
    from unimport.color import Color, paint
    from unimport.main import Main

    main = Main.run()
    if not main.is_unused_imports and main.config.check:
        print(
            paint(
                f"{emoji.STAR} Congratulations there is no unused import in your project. {emoji.STAR}",
                Color.GREEN,
                main.config.use_color,
            )
        )

    raise SystemExit(main.exit_code())


if __name__ == "__main__":
    main()
