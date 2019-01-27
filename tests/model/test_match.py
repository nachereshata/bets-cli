import pytest

from bets.model import match

IDX_TITLE = match.IDX_TITLE
IDX_1 = match.IDX_1
IDX_X = match.IDX_X
IDX_2 = match.IDX_2


def test_match_is_represented_as_tuple():
    assert isinstance(match.new_match("Man utd. - Arsenal", 1.2, 2.2, 1.8), tuple)


def test_match_index_values():
    assert IDX_TITLE == 0
    assert IDX_1 == 1
    assert IDX_X == 2
    assert IDX_2 == 3


def test_match_values_at_positions():
    title = "Man utd. - Arsenal"
    ratio_1 = 1.2
    ratio_x = 2.2
    ratio_2 = 1.8

    _match = match.new_match(title, ratio_1, ratio_x, ratio_2)

    assert title == _match[IDX_TITLE]
    assert ratio_1 == _match[IDX_1]
    assert ratio_x == _match[IDX_X]
    assert ratio_2 == _match[IDX_2]


def test_create_match_with_string_ratios():
    title = "Man utd. - Arsenal"
    ratio_1 = "1.2"
    ratio_x = "2,2"
    ratio_2 = " 1.83"

    _match = match.new_match(title, ratio_1, ratio_x, ratio_2)
    assert _match[IDX_TITLE] == title
    assert _match[IDX_1] == 1.2
    assert _match[IDX_X] == 2.2
    assert _match[IDX_2] == 1.83


def test_parse_line_accepts_only_string():
    with pytest.raises(TypeError):
        match.parse_line(None)

    with pytest.raises(TypeError):
        match.parse_line([])

    with pytest.raises(TypeError):
        match.parse_line(object())

    with pytest.raises(TypeError):
        match.parse_line(1)


def test_parse_line_raises_value_error_on_empty_string():
    with pytest.raises(ValueError):
        match.parse_line("")


def test_parse_line_raises_value_error_on_line_with_less_than_4_parts():
    with pytest.raises(ValueError):
        match.parse_line("1 2 3")


def test_is_match_returns_correct_result():
    # a valid match is a tuple with format: [str, float, float, float]
    assert isinstance(match.is_match(None), bool)
    assert match.is_match(("title", 2.4, 1.5, 6.3))
    assert match.is_match(("longer - title", 2.4, 1.50, 6.3))
    assert not match.is_match(["longer - title", 2.4, 1.50, 6.3])
    assert not match.is_match({"longer - title", 2.4, 1.50, 6.3})
    assert not match.is_match(("longer - title", 2.4, 1.50, 6))
    assert not match.is_match(("longer - title", 2.4, 1, 6.3))
    assert not match.is_match(("longer - title", 2, 1.6, 6.3))
    assert not match.is_match(({}, 2, 1.6, 6.3))
    assert not match.is_match((None, 2, 1.6, 6.3))
    assert not match.is_match((None, 2, 1.6, 6.3))
    assert not match.is_match((None, 2.4, 6.3))


def test_create_match_from_text_line():
    text_line = "Barcelona - Liverpool 2.34 3.40 2.5"
    _match = match.parse_line(text_line)
    assert match.is_match(_match)
    assert _match[IDX_TITLE] == "Barcelona - Liverpool"
    assert _match[IDX_1] == 2.34
    assert _match[IDX_X] == 3.40
    assert _match[IDX_2] == 2.50
