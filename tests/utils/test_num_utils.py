import pytest

from bets.utils import num_utils


def test_parse_float_handles_string_integer():
    string_integer = "2"
    assert isinstance(num_utils.parse_float(string_integer), float)
    assert num_utils.parse_float(string_integer) == 2.0


def test_parse_float_handles_string_integer_with_spaces():
    string_integer_with_spaces = "10 000"
    assert isinstance(num_utils.parse_float(string_integer_with_spaces), float)
    assert num_utils.parse_float(string_integer_with_spaces) == 10000.0


def test_parse_float_handles_string_float_with_dot():
    float_with_dot = "3.14"
    assert isinstance(num_utils.parse_float(float_with_dot), float)
    assert num_utils.parse_float(float_with_dot) == 3.14


def test_parse_float_handles_string_float_with_comma():
    float_with_comma = "3,14"
    assert isinstance(num_utils.parse_float(float_with_comma), float)
    assert num_utils.parse_float(float_with_comma) == 3.14


def test_parse_float_handles_string_float_with_thousands_comma():
    float_with_thousands_comma = "2,000.2"
    assert isinstance(num_utils.parse_float(float_with_thousands_comma), float)
    assert num_utils.parse_float(float_with_thousands_comma) == 2000.2


def test_parse_float_handles_string_float_with_thousands_comma_and_spaces():
    float_with_thousands_comma_and_spaces = "3, 000, 000 . 4 "
    assert isinstance(num_utils.parse_float(float_with_thousands_comma_and_spaces), float)
    assert num_utils.parse_float(float_with_thousands_comma_and_spaces) == 3000000.4


def test_parse_float_raises_value_error_when_not_parsed():
    with pytest.raises(ValueError):
        num_utils.parse_float(object())
