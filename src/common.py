"""Common functions"""

from typing import Tuple, Any


__all__ = ['parse_hex', 'int_tuple', 'normalized']


def parse_hex(arg: str) -> Tuple[int, int, int]:
    """Parses hex string into (R, G, B)

    :param arg: 3 or 6 hexadecimal chars
    :return: (R, G, B)
    """
    length = len(arg)
    if length not in (3, 6):
        raise ValueError(f'Length of input has to be either 3 or 6 not {length}')
    return tuple(int(arg[length//3*i:length//3*(i+1)], 16) for i in range(3))


def int_tuple(*source: Any) -> Tuple[int, ...]:
    """Maps int over input params and returns them as int

    :param source: Iterable to iterate over
    :return: Tuple of ints
    """
    return tuple(int(float(t)) for t in source)


def normalized(s: str) -> str:
    """Normalizes string for easier comparison

    :param s: String to normalize
    :return: Lowered string without whitespace
    """
    return ''.join(s.split()).lower()
