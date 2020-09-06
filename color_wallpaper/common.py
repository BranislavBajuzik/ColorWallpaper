"""Common functions."""
import logging
from typing import Any, Optional, Tuple

__all__ = ["parse_hex", "int_tuple", "normalized", "init_logging"]


def parse_hex(arg: str) -> Tuple[int, int, int]:
    """Parse hex string into (R, G, B).

    :param arg: 3 or 6 hexadecimal chars
    :return: (R, G, B)
    """
    length = len(arg)
    if length == 3:
        return tuple(int(arg[i : i + 1] * 2, 16) for i in range(3))  # type: ignore
    if length == 6:
        return tuple(int(arg[2 * i : 2 * (i + 1)], 16) for i in range(3))  # type: ignore

    raise ValueError(f"Length of input has to be either 3 or 6 not {length}")


def int_tuple(*source: Any) -> Tuple[int, ...]:
    """Map int over input params and returns them as int.

    :param source: Iterable to iterate over
    :return: Tuple of ints
    """
    if len(source) == 1:
        source = source[0]

    return tuple(int(float(t)) for t in source)


def normalized(s: str) -> str:
    """Normalize string for easier comparison.

    :param s: String to normalize
    :return: Lowered string without whitespace
    """
    return "".join(s.split()).casefold()


class Logging:
    logger: Optional[logging.Logger] = None

    @classmethod
    def init_logging(cls, logging_level: int) -> None:
        """Initialize logging for this module.

        :param logging_level: Requested log level.
        """
        if cls.logger is not None:
            return

        cls.logger = logging.getLogger(__package__ or "color_wallpaper")
        cls.logger.setLevel(logging_level)

        # Disable logging
        if logging_level == logging.NOTSET:
            cls.logger.setLevel(logging.CRITICAL)

        # Logging format
        handler = logging.StreamHandler()
        handler.setLevel(logging_level)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        cls.logger.addHandler(handler)


init_logging = Logging.init_logging
