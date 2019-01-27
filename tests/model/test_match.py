import pytest
import tempfile

from os import path
from os import unlink

from bets.model import match

IDX_TITLE = match.IDX_TITLE
IDX_1 = match.IDX_1
IDX_X = match.IDX_X
IDX_2 = match.IDX_2


def test_match_is_represented_as_tuple():
    assert isinstance(match.new_match("Man utd. - Arsenal", 1.2, 2.2, 1.8), tuple)


def test_match_index_values():
    assert match.IDX_TITLE == 0
    assert match.IDX_1 == 1
    assert match.IDX_X == 2
    assert match.IDX_2 == 3


def test_test_indexes_are_properly_set():
    assert IDX_TITLE == match.IDX_TITLE
    assert IDX_1 == match.IDX_1
    assert IDX_X == match.IDX_X
    assert IDX_2 == match.IDX_2


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


def test_parse_text_raises_type_error_if_not_string():
    with pytest.raises(TypeError):
        match.parse_text(1)
    with pytest.raises(TypeError):
        match.parse_text(object())
    with pytest.raises(TypeError):
        match.parse_text(None)
    with pytest.raises(TypeError):
        match.parse_text([])


def test_parse_text_returns_list_of_single_match_when_one():
    text = """

    Barcelona - Liverpool 2.34 3.40 2.5
    2134
    
    not a match pal
    """

    _matches = match.parse_text(text)
    assert isinstance(_matches, list)
    assert len(_matches) == 1

    _match = _matches[0]
    assert match.is_match(_match)
    assert _match[IDX_TITLE] == "Barcelona - Liverpool"
    assert _match[IDX_1] == 2.34
    assert _match[IDX_X] == 3.40
    assert _match[IDX_2] == 2.5


def test_parse_text_returns_list_of_matches_when_many():
    text = """
    
    Barcelona - Liverpool 2.34 3.40 2.5
    2134
    Man utd. - Arsenal 2.78 3.9 3.5
    123
    """

    _matches = match.parse_text(text)
    assert isinstance(_matches, list)
    assert len(_matches) == 2

    for _match in _matches:
        assert match.is_match(_match)

    assert _matches[0][IDX_TITLE] == "Barcelona - Liverpool"
    assert _matches[0][IDX_1] == 2.34
    assert _matches[0][IDX_X] == 3.40
    assert _matches[0][IDX_2] == 2.5
    assert _matches[1][IDX_TITLE] == "Man utd. - Arsenal"
    assert _matches[1][IDX_1] == 2.78
    assert _matches[1][IDX_X] == 3.90
    assert _matches[1][IDX_2] == 3.50


def test_parse_text_raises_value_error_if_no_matches_in_text():
    with pytest.raises(ValueError):
        match.parse_text("")

    with pytest.raises(ValueError):
        match.parse_text("""
        no
        matches here
        pal
        """)
    with pytest.raises(ValueError):
        match.parse_text("""
        no matches here too
        """)


def test_parse_file_raises_type_error_if_not_string():
    with pytest.raises(TypeError):
        match.parse_file(1)
    with pytest.raises(TypeError):
        match.parse_file(None)
    with pytest.raises(TypeError):
        match.parse_file([])
    with pytest.raises(TypeError):
        match.parse_file(object())


def test_parse_file_raises_value_error_if_empty_string():
    with pytest.raises(ValueError):
        match.parse_file("")


def test_parse_file_returns_list_of_matches_when_in_file():
    text = """
        Barcelona - Liverpool 2.34 3.40 2.5
        2134
        Man utd. - Arsenal 2.78 3.9 3.5
        123
        """

    file_path = path.join(tempfile.gettempdir(), "matches.txt")

    with open(file_path, "wb") as fp:
        fp.write(text.encode("utf-8"))

    _matches = match.parse_file(file_path)

    unlink(file_path)

    assert isinstance(_matches, list)
    assert len(_matches) == 2

    for _match in _matches:
        assert match.is_match(_match)

    assert _matches[0][IDX_TITLE] == "Barcelona - Liverpool"
    assert _matches[0][IDX_1] == 2.34
    assert _matches[0][IDX_X] == 3.40
    assert _matches[0][IDX_2] == 2.5
    assert _matches[1][IDX_TITLE] == "Man utd. - Arsenal"
    assert _matches[1][IDX_1] == 2.78
    assert _matches[1][IDX_X] == 3.90
    assert _matches[1][IDX_2] == 3.50
