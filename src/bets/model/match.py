import logging
from typing import List, Tuple, Union

from bets.utils.num_utils import parse_float

_log = logging.getLogger(__name__)

INDEX = {
    "title": 0,
    "1": 1,
    "X": 2,
    "2": 3
}

IDX_TITLE = INDEX["title"]
IDX_1 = INDEX["1"]
IDX_X = INDEX["X"]
IDX_2 = INDEX["2"]

OUTCOMES = tuple("1 X 2".split(" "))
OUTCOME_INDEX = {o: i for i, o in enumerate(OUTCOMES)}

RANKS = tuple("min med max".split())


def is_match(instance) -> bool:
    """Checks if min requirements to be considered a valid match data are met"""
    # match must be represented as tuple
    if not isinstance(instance, tuple):
        return False

    # match tuple must have at least 4 parts
    if len(instance) < 4:
        return False

    # title must be str
    if not isinstance(instance[IDX_TITLE], str):
        return False

    # ratios must be float
    if not isinstance(instance[IDX_1], float):
        return False
    if not isinstance(instance[IDX_X], float):
        return False
    if not isinstance(instance[IDX_2], float):
        return False

    return True


def new_match(title, ratio_1, ratio_x, ratio_2):
    """Creates a tuple containing match data by doing arg conversions if needed"""
    return title, parse_float(ratio_1), parse_float(ratio_x), parse_float(ratio_2)


def parse_line(line: str) -> Tuple[str, float, float, float]:
    """Parses a string to a tuple with match data"""

    if not isinstance(line, str):
        raise TypeError("Expected string but got {}!".format(type(line).__name__))

    if not line:
        raise ValueError("Expected non-empty string!")

    line_parts = line.strip().split(" ")
    if len(line_parts) < 4:
        raise ValueError("Line should contain at least 4 space-separated parts!")

    title = " ".join(line_parts[:-3])
    r1, rx, r2 = line_parts[-3:]

    return new_match(title, r1, rx, r2)


def parse_text(text: str) -> List[tuple]:
    """Parses text to a list of tuples with match data"""

    if not isinstance(text, str):
        raise TypeError("Expected string!")

    lines = [line.strip()
             for line
             in text.split("\n")
             if line.strip()]

    matches = []

    for line in lines:
        try:
            matches.append(parse_line(line))
        except ValueError:
            continue

    if not matches:
        raise ValueError("The text did not contain any matches!", text)

    return matches


def parse_file(file_path: str) -> List[tuple]:
    """Reads a text file to a list of tuples with match data"""
    if not isinstance(file_path, str):
        raise TypeError("Expected string")

    if not file_path:
        raise ValueError("Expected non-empty string")

    with open(file_path, "rb") as fp:
        text = fp.read().decode("utf-8")

    return parse_text(text)


def get_outcomes_ratios(match):
    # 4.5 2.3 3.1
    return tuple(match[IDX_1:(IDX_2 + 1)])


def get_sorted_ratios(match):
    # 2.3 3.1 4.5
    return tuple(sorted(match[IDX_1: (IDX_2 + 1)]))


def get_ranks_outcomes(match: tuple) -> Union[Tuple[str, str, str], Tuple[str, ...]]:
    # X 2 1
    sorted_ratios = get_sorted_ratios(match)

    outcome2ratio = {
        "1": match[IDX_1],
        "X": match[IDX_X],
        "2": match[IDX_2],
    }

    ranks = [[], [], []]

    for outcome, ratio in outcome2ratio.items():
        for i, sr in enumerate(sorted_ratios):
            if ratio == sr:
                ranks[i].append(outcome)

    return tuple("/".join(_) for _ in ranks)


def get_outcome_ranks(match: tuple):
    # max min med
    ranks = [[], [], []]

    for rank, outcome in zip(RANKS, get_ranks_outcomes(match)):
        for o in outcome.split("/"):
            ranks[OUTCOME_INDEX[o]].append(rank)

    return tuple("/".join(r) for r in ranks)
