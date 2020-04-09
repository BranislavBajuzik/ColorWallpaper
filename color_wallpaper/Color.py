"""Handles color calculation"""

import re

from typing import Tuple
from random import choice
from colorsys import rgb_to_hsv, rgb_to_hls, hls_to_rgb

from .data import *
from .common import *

__all__ = ["Color"]


# http://colorizer.org/ <-- Very nice
hex_re = re.compile(r"\s*#?([\da-f]{6}|[\da-f]{3})\s*", re.I)
rgb_re = re.compile(r"\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\s*")


class Color:
    """Class for color handling"""

    def __init__(self, rgb: Tuple[int, int, int], name: str = None):
        """Color constructor

        :param rgb: (R,G,B) of the color
        :param name: Overrides the color name lookup
        """
        if len(rgb) != 3 or not all(0 <= c <= 255 for c in rgb):
            raise ValueError("Invalid RGB values")
        self.rgb = rgb

        if name is None:
            self.name = hex_to_color.get(self.hex(), "Anonymous")
        else:
            self.name = name

    def __str__(self):
        return f"Color(rgb={self.rgb}, name='{self.name}')"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.rgb == other.rgb and self.name == other.name

    @staticmethod
    def __normalize(components: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Helper function for converting int RGB to float RGB"""
        return tuple(component / 255 for component in components)

    def hex(self, lowercase: bool = True) -> str:
        """Returns HEX representation of :param self:"""
        format_string = f'{{0:02{"x" if lowercase else "X"}}}'
        return "".join(format_string.format(c) for c in self.rgb)

    @property
    def hsv(self) -> Tuple[int, int, int]:
        """Returns HSV representation of :param self:"""
        h, s, v = rgb_to_hsv(*self.__normalize(self.rgb))

        return int(h * 360), int(s * 100), int(v * 100)

    @property
    def hsl(self) -> Tuple[int, int, int]:
        """Returns HSL representation of :param self:"""
        h, l, s = rgb_to_hls(*self.__normalize(self.rgb))

        return int(h * 360), int(s * 100), int(l * 100)

    @property
    def cmyk(self) -> Tuple[int, int, int, int]:
        """Returns CMYK representation of :param self:"""
        c, m, y = (1 - component / 255 for component in self.rgb)

        k = min(c, m, y, 1)

        if k == 1:
            return 0, 0, 0, 100

        c, m, y = ((component - k) / (1.0 - k) for component in (c, m, y))

        return int_tuple(component * 100 for component in (c, m, y, k))

    @property
    def luminance(self) -> float:
        """Returns relative luminance of :param self:"""
        r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in self.__normalize(self.rgb))

        return r * 0.2126 + g * 0.7152 + b * 0.0722

    def __truediv__(self, other) -> float:
        contrasts = sorted((self.luminance, other.luminance), reverse=True)

        return (contrasts[0] + 0.05) / (contrasts[1] + 0.05)

    def __floordiv__(self, other) -> int:
        return int(self / other)

    def inverted(self, min_contrast: float = None) -> "Color":
        """Returns a new Color that is in contrast with :param self:

        :param min_contrast: Minimum contrast. Must be in range (1-21)
        """
        ret = Color(tuple(255 - x for x in self.rgb))

        if min_contrast in (1, None):
            return ret

        if not 1 <= min_contrast <= 21:
            raise ValueError(f"min_contrast is outside of [1, 21]: {min_contrast}")

        if self / ret >= min_contrast:
            return ret

        h, s, l = ret.hsl
        l_down, l_up = l - 1, l + 1

        while l_down >= 0 and l_up <= 100:
            if l_down >= 0:
                ret = self.from_hsl(h, s, l_down)

                if self / ret >= min_contrast:
                    return ret

                l_down -= 1

            if l_up <= 100:
                ret = self.from_hsl(h, s, l_up)

                if self / ret >= min_contrast:
                    return ret

                l_up += 1

        raise RuntimeError(f"Unable to to find a color that has contrast of at least {min_contrast} with {self}")

    @staticmethod
    def random() -> "Color":
        """Returns random named color"""
        return Color(parse_hex(choice(color_hexes)))

    @staticmethod
    def from_hsl(h: int, s: int, l: int) -> "Color":
        """Creates a Color object from hue, saturation and luminance

        :param h: Hue
        :param s: Saturation
        :param l: Luminance
        :return: New Color object
        """
        components = (360, h, "h"), (100, l, "l"), (100, s, "s")

        for bound, component, name in components:
            if not 0 <= component <= bound:
                raise ValueError(f"{name} is outside of [0, {bound}]: {component}")

        rgb = hls_to_rgb(*(component / bound for bound, component, name in components))

        return Color(int_tuple(component * 255 for component in rgb))

    @staticmethod
    def from_str(arg: str) -> "Color":
        """Creates a Color object from string

        :param arg: Input string. Must be either Color name, (R,G,B), #HEX or HEX
        :return: New Color object
        """
        hex_groups = hex_re.fullmatch(arg)
        rgb_groups = rgb_re.fullmatch(arg)

        if hex_groups is not None:
            rgb = parse_hex(hex_groups.group(1))
        elif rgb_groups is not None:
            rgb = int_tuple(rgb_groups.group(1), rgb_groups.group(2), rgb_groups.group(3))
            if not all(0 <= c <= 255 for c in rgb):
                raise ValueError("Invalid RGB values")
        else:
            name = normalized(arg)

            if name not in color_to_hex:
                raise ValueError(f'"{arg}" is not a color name')

            rgb = parse_hex(color_to_hex[name])

        return Color(rgb)
