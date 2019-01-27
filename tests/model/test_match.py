import pytest

from bets.model import match

IDX_TITLE = match.INDEX["title"]
IDX_1 = match.INDEX["1"]
IDX_X = match.INDEX["X"]
IDX_2 = match.INDEX["2"]


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
