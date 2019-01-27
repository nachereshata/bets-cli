import pytest

from bets.utils import num_utils


def test_parse_float_handles_string_integer():
    assert isinstance(num_utils.parse_float("2"), float)
    assert num_utils.parse_float("2") == 2.0


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
