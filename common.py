from typing import Tuple


__all__ = ['parse_hex', 'int_tuple', 'normalized']


def parse_hex(arg: str) -> Tuple[int, int, int]:
    le = len(arg)
    return tuple(int(arg[le//3*i:le//3*(i+1)], 16) for i in range(3))


def int_tuple(*t) -> Tuple[int, ...]:
    return tuple(map(int, t))


def normalized(s: str) -> str:
    return ''.join(s.split()).lower()
