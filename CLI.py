import re
import argparse

from pathlib import Path
from typing import Tuple, Sequence, Type

from common import *
from Color import *


__all__ = ['get_options']


resolution_re = re.compile(r'\s*(\d+)\s*[x:]\s*(\d+)\s*')


def resolution(arg: str) -> Tuple[int, int]:
    """Parses resolution CLI argument"""
    groups = resolution_re.fullmatch(arg)

    if groups is None:
        raise argparse.ArgumentTypeError('Unable to parse the resolution')

    res = int_tuple(groups.group(1), groups.group(2))

    if any(dimension < 150 for dimension in res):
        raise argparse.ArgumentTypeError('Minimal resolution is 150x150')

    return res


def positive(typ: Type):
    def typed_positive(arg: str):
        """Parses a positive number of :param type: from CLI"""
        return max(1, typ(float(arg)))
    return typed_positive


def in_range(typ: Type, low: float, high: float):
    low, high = sorted((low, high))

    def is_in_range(arg: str):
        arg = typ(float(arg))
        if not (low <= arg <= high):
            raise AssertionError(f'"{arg}" must be in range ({low}, {high})')

        return arg
    return is_in_range


def get_options(args: Sequence[str] = None) -> argparse.Namespace:
    """Parses CLI options

    :param args: None for `sys.argv`
    :return: Object with options as attributes
    """
    ret = argparse.ArgumentParser(description='Minimalist wallpaper generator', usage=f'python %(prog)s ...')

    general_g = ret.add_argument_group('General options')
    general_g.add_argument('-o', '--output',
                           metavar='PATH',
                           type=Path,
                           default=Path('out.png'),
                           help='Image output path')

    general_g.add_argument('-y', '--yes',
                           action='store_true',
                           help='Force overwrite of --output')

    color_g = ret.add_argument_group('Color options')
    color_g.add_argument('-c', '--color',
                         type=Color.from_str,
                         default=Color((255, 2, 141), 'Hot Pink'),
                         help='Background color. #Hex / R,G,B / random / name')

    color_g.add_argument('-c2', '--color2',
                         metavar='COLOR',
                         type=Color.from_str,
                         help='Highlight color. #Hex / R,G,B / random / name')

    color_g.add_argument('-d', '--display',
                         help='Override the display name of --color. Empty string disables the name row')

    color_g.add_argument('--min-contrast',
                         type=in_range(float, 0, 21),
                         default=4.5,
                         help='Min contrast of --color and --color2. Must be in range (0-21). '
                              'RuntimeError will be raised if this can not be satisfied')

    display_g = ret.add_argument_group('Display options')
    display_g.add_argument('-r', '--resolution',
                           type=resolution,
                           default=(1920, 1080),
                           help='The dimensions of the result image. WIDTHxHEIGHT')

    display_g.add_argument('-s', '--scale',
                           type=positive(int),
                           default=3,
                           help='The size of the highlight will be divided by this')

    display_g.add_argument('-f', '--formats',
                           type=normalized,
                           default=['empty', 'hex', 'rgb'],
                           nargs='+',
                           choices=['empty', 'hex', '#hex', 'rgb', 'hsv', 'hsl', 'cmyk'],
                           help='Declares the order and formats to display')

    display_g.add_argument('-l', '--lowercase',
                           action='store_true',
                           help='Casing of hex output')

    ret = ret.parse_args(args)

    if ret.color2 is None:
        ret.color2 = ret.color.inverted()

    return ret
