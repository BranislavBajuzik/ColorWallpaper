"""Handles CLI parsing."""

import argparse
import logging
import re
from pathlib import Path
from typing import Callable, List, Sequence, Tuple, Type, TypeVar

from .color import Color
from .common import int_tuple

__all__ = ["get_options", "DEFAULT_OUTPUT"]

DEFAULT_OUTPUT = Path("out.png")

Number = TypeVar("Number", float, int)
T = TypeVar("T")

resolution_re = re.compile(r"\s*(\d+)\s*[x:]\s*(\d+)\s*")


def log_level(arg: str) -> int:
    level = logging._nameToLevel.get(arg.upper())

    if level is None:
        raise argparse.ArgumentTypeError(f"Invalid choice '{arg}', pick from {tuple(logging._nameToLevel)}")

    return level


def resolution(arg: str) -> Tuple[int, int]:
    """Parse resolution CLI argument."""
    groups = resolution_re.fullmatch(arg)

    if groups is None:
        raise argparse.ArgumentTypeError("Unable to parse the resolution")

    res = int_tuple(groups.group(1), groups.group(2))

    if any(dimension < 150 for dimension in res):
        raise argparse.ArgumentTypeError("Minimal resolution is 150x150")

    return res  # type: ignore


def positive(typ: Type[Number]) -> Callable[[str], Number]:
    """Bind a type to the inner function.

    :param typ: Type to be bound
    :return: A function that returns a number of max(:param typ:, 1)
    """

    def typed_positive(arg: str) -> Number:
        """Parse a number from :param arg:. The smallest number returned is 1."""
        return max(typ(1), typ(float(arg)))

    return typed_positive


def in_range(typ: Type[Number], low: float, high: float) -> Callable[[str], Number]:
    """Bind a range and type to the inner function.

    :param typ: Type to be bound
    :param low: Lower bound
    :param high: Upper bound
    :return: A function that raises if a number is not in range.
    """
    low, high = sorted((low, high))

    def is_in_range(arg: str) -> Number:
        """Parse a number from :param arg:.

        :raises AssertionError: If not in the bound range
        """
        arg = typ(float(arg))
        if not low <= arg <= high:
            raise argparse.ArgumentTypeError(f'"{arg}" must be in range ({low}, {high})')

        return arg

    return is_in_range


def fix_casing(names: Sequence[str]) -> Callable[[str], str]:
    """Binds :param names: to the inner function.

    :param names: Templates for the fixing, non-empty
    :return: A function that fixes casing

    Usage:
        >>> fix_casing(('One', 'Two', 'Three'))('tHreE')
        'Three'
        >>> fix_casing(('aaa', 'Aaa', 'bbb'))('BbB')
        'bbb'
        >>> fix_casing(('aaa', 'Aaa', 'bbb'))('aaa')
        'aaa'
        >>> fix_casing(('aaa', 'Aaa', 'bbb'))('aAa')
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
          File "<stdin>", line 36, in cased
        argparse.ArgumentTypeError: Ambiguous choice: aAa. Unable to decide between ['aaa', 'Aaa']
    """

    def cased(arg: str) -> str:
        """Fix the casing of :param arg: using the bound :param names: as template.

        :param arg: Argument that needs to be fixed
        :return: Correctly cased :param arg:
        """
        low_names = tuple(name.lower() for name in names)

        if not isinstance(arg, str) or arg.lower() not in low_names:
            raise argparse.ArgumentTypeError(f'Invalid choice: "{arg}". Chose from {names}')

        duplicate_names = {name for name in low_names if low_names.count(name) > 1}

        if arg in names:
            arg = names[names.index(arg)]
        elif arg.lower() not in duplicate_names:
            arg = names[low_names.index(arg.lower())]
        else:
            raise argparse.ArgumentTypeError(
                f"Ambiguous choice: {arg}. Unable to decide between "
                f"{[name for name in names if name.lower() in duplicate_names and name.lower() == arg.lower()]}"
            )
        return arg

    return cased


class ArgumentDefaultsHelpFormatter(argparse.HelpFormatter):
    """Help message formatter which adds default values to argument help."""

    __format_map = {
        "yes": lambda _: None,
        "resolution": lambda s: "x".join(map(str, s)),
        "formats": lambda s: " ".join(map(str, s)),
        "log_level": lambda _: "NOTSET",
    }

    def __init__(self, prog):
        super().__init__(prog)

        self.default = None

    def _get_help_string(self, action):
        self.default = None

        if action.default not in (None, argparse.SUPPRESS):
            if action.option_strings or action.nargs in (argparse.OPTIONAL, argparse.ZERO_OR_MORE):
                self.default = self.__format_map.get(action.dest, lambda s: s)(action.default)

        return action.help

    def _split_lines(self, text: str, width: int) -> List[str]:
        lines = super()._split_lines(text, width)

        if self.default is not None:
            lines.append(f"Default: {self.default}")

        return lines


def get_options(args: Sequence[str] = None) -> argparse.Namespace:
    """Parse CLI options.

    :param args: None for `sys.argv`
    :return: Object with options as attributes
    """
    ret = argparse.ArgumentParser(
        prog="color_wallpaper",
        allow_abbrev=False,
        description="Minimalist wallpaper generator",
        usage="Try --help for more information",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    ret.add_argument("--log-level", type=log_level, default=logging.CRITICAL, help="Sets logging level")

    general_g = ret.add_argument_group("File options")
    general_g.add_argument(
        "-o", "--output", metavar="PATH", type=Path, default=DEFAULT_OUTPUT, help="Image output path"
    )

    general_g.add_argument("-y", "--yes", action="store_true", help="Force overwrite of --output")

    color_g = ret.add_argument_group("Color options")
    color_g.add_argument("-c", "--color", default="random", help="Background color. #Hex / R,G,B / random / NAME")

    color_g.add_argument(
        "-c2", "--color2", metavar="COLOR", default="inverted", help="Highlight color. #Hex / R,G,B / inverted / NAME"
    )

    color_g.add_argument(
        "-d", "--display", help="Override the display name of --color. Empty string disables the name row"
    )

    color_g.add_argument(
        "--min-contrast",
        type=in_range(float, 1, 21),
        default=1,
        help="Min contrast of --color and --color2, if --color2 is `inverted`. "
        "Must be in range (1-21). Will be raise if this can not be satisfied",
    )

    color_g.add_argument(
        "--overlay-color",
        metavar="COLOR",
        type=Color.from_str,
        help="Color of potential overlay, like icons or text. #Hex / R,G,B / name",
    )

    color_g.add_argument(
        "--overlay-contrast",
        type=in_range(float, 1, 21),
        default=1,
        help="Min contrast of --color and --overlay-color. "
        "Must be in range (1-21). Will be raise if this can not be satisfied",
    )

    display_g = ret.add_argument_group("Display options")
    display_g.add_argument(
        "-r",
        "--resolution",
        type=resolution,
        default=(1920, 1080),
        help="The dimensions of the result image. WIDTHxHEIGHT",
    )

    display_g.add_argument(
        "-s", "--scale", type=positive(int), default=3, help="The size of the highlight will be multiplied by this"
    )

    display_g.add_argument(
        "-f",
        "--formats",
        type=fix_casing(("empty", "hex", "#hex", "HEX", "#HEX", "rgb", "hsv", "hsl", "cmyk")),
        default=["empty", "HEX", "rgb"],
        nargs="*",
        help="Declares the order and formats to display. Available choices: "
        "{empty, hex, #hex, HEX, #HEX, rgb, hsv, hsl, cmyk}",
    )

    display_g = ret.add_argument_group("Multiple wallpapers generation options")
    display_g.add_argument(
        "--multiple-count",
        type=int,
        default=1,
        help="Generate all colors, that pass other options filtering. negative numbers will produce all colors",
    )

    display_g.add_argument(
        "--multiple-extension", type=str, default="png", help="The extension/format of the wallpapers"
    )

    return ret.parse_args(args)
