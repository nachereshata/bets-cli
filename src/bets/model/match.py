import logging

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


def is_match(instance) -> bool:
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
    return title, parse_float(ratio_1), parse_float(ratio_x), parse_float(ratio_2)


def parse_line(line: str):
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


def parse_text(text: str):
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
