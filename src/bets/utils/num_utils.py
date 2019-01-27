import logging

from bets.utils.constants import (
    COMMA,
    DOT,
    EMPTY,
    SPACE
)

_log = logging.getLogger(__name__)


def parse_float(value) -> float:
    """Helper method to convert values to floats"""

    try:
        return float(value)

    except (ValueError, TypeError):

        if isinstance(value, str):
            value = value.strip().replace(SPACE, EMPTY)

            try:
                return float(value)

            except (ValueError, TypeError):
                if COMMA in value:

                    if DOT in value:
                        return float(value.replace(COMMA, EMPTY))

                    return float(value.replace(COMMA, DOT))

        raise ValueError(f"Could not parse value to float", value)
