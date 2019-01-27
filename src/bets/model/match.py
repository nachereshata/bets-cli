import logging

from bets.utils.num_utils import parse_float

_log = logging.getLogger(__name__)

INDEX = {
    "title": 0,
    "1": 1,
    "X": 2,
    "2": 3
}


def new_match(title, ratio_1, ratio_x, ratio_2):
    return title, parse_float(ratio_1), parse_float(ratio_x), parse_float(ratio_2)
