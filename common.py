"""Common functions"""

from typing import Tuple, Iterable


__all__ = ['parse_hex', 'int_tuple', 'normalized']


def parse_hex(arg: str) -> Tuple[int, int, int]:
    """Parses hex string into (R, G, B)

    :param arg: 3 or 6 hexadecimal chars
    :return: (R, G, B)
    """
    length = len(arg)
    return tuple(int(arg[length//3*i:length//3*(i+1)], 16) for i in range(3))


def int_tuple(*t: Iterable) -> Tuple[int, ...]:
    """Maps int over an iterable into tuple

    :param t: Iterable to iterate over
    :return: Tuple of ints
    """
    return tuple(map(int, t))


def normalized(s: str) -> str:
    """Normalizes string for easier comparison

    :param s: String to normalize
    :return: Lowered string without whitespace
    """
    return ''.join(s.split()).lower()
