import logging

_log = logging.getLogger(__name__)


def parse_float(value) -> float:
    """Helper method to convert values to floats"""

    try:
        return float(value)
    except ValueError:
        if isinstance(value, str):

            value = value.strip().replace(",", ".").replace(" ", "")
