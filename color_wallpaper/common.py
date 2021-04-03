"""Common functions."""
import os
import re
from typing import Any, Tuple

__all__ = ["parse_hex", "int_tuple", "normalized", "safe_path_name"]


windows_path_sub_re = re.compile('[<>:"/\\\\|?*\0-\37]')
windows_forbidden_path_re = re.compile(r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])$", re.I)
unix_path_sub_re = re.compile("[\0:/]")


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


def safe_path_name(filename: str) -> str:
    """Return a sanitized up valid file name under current OS.

    :param filename: Filename to sanitize.
    :return: The sanitized filename.
    """
    sub_re = windows_path_sub_re if os.name == "nt" else unix_path_sub_re

    filename = sub_re.sub("_", filename)

    if os.name == "nt":
        filename = windows_forbidden_path_re.sub("", filename.rstrip(". "))

    return filename or "unnamed"
