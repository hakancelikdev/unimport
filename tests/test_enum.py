import pytest

from unimport.enums import Color, ColorSelect, Emoji


def test_emoji():
    assert Emoji.STAR == "🤩"
    assert Emoji.PARTYING_FACE == "🥳"


@pytest.mark.parametrize("member", [*Emoji, *Color, *ColorSelect])
def test_str_and_format_use_the_value(member):
    assert str(member) == member.value
    assert f"{member}" == member.value
    assert "%s" % member == member.value


def test_color_choices():
    from unimport.config import Config

    assert Config.get_color_choices() == ["auto", "always", "never"]
