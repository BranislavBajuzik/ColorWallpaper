import re

from typing import Tuple
from random import choice
from colorsys import rgb_to_hsv, rgb_to_hls

from data import *
from common import *

__all__ = ['Color']


hex_re = re.compile(r'\s*#?([\da-f]{6}|[\da-f]{3})\s*', re.I)
rgb_re = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\s*')


class Color:
    """Class for color handling"""

    def __init__(self, rgb: Tuple[int, int, int], name: str = None):
        """Color constructor

        :param rgb: (R,G,B) of the color
        :param name: Overrides the color name lookup
        """
        self.rgb = rgb

        if name is None:
            name = hex_to_color.get(self.hex, 'anonymous')
            self.name = pretty_names.get(name, name.capitalize())
        else:
            self.name = name

    @staticmethod
    def __normalize(components: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Helper function for converting int RGB to float RGB"""
        return tuple(component/255 for component in components)

    @property
    def hex(self) -> str:
        return ''.join(f'{c:02x}' for c in self.rgb)

    @property
    def hsv(self) -> Tuple[int, int, int]:
        """Returns HSV representation of :param self:"""
        h, s, v = rgb_to_hsv(*self.__normalize(self.rgb))

        return int(h*360), int(s*100), int(v*100)

    @property
    def hsl(self) -> Tuple[int, int, int]:
        """Returns HSL representation of :param self:"""
        h, l, s = rgb_to_hls(*self.__normalize(self.rgb))

        return int(h*360), int(s*100), int(l*100)

    @property
    def cmyk(self) -> Tuple[int, int, int, int]:
        """Returns CMYK representation of :param self:"""
        c, m, y = (1 - component/255 for component in self.rgb)

        k = min(c, m, y, 1)

        if k == 1:
            return 0, 0, 0, 100

        c = (c - k) / (1.0 - k)
        m = (m - k) / (1.0 - k)
        y = (y - k) / (1.0 - k)

        return tuple(int(component*100) for component in (c, m, y, k))

    @property
    def luminance(self) -> float:
        """Returns relative luminance of :param self:"""
        r, g, b = (c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
                   for c in self.__normalize(self.rgb))

        return r*0.2126 + g*0.7152 + b*0.0722

    def __truediv__(self, other) -> float:
        contrasts = sorted((self.luminance, other.luminance), reverse=True)

        return (contrasts[0] + 0.05) / (contrasts[1] + 0.05)

    def __floordiv__(self, other) -> int:
        return int(self / other)

    def inverted(self) -> "Color":
        """Returns a new Color object of inverted :param self:"""
        return Color(tuple(255 - x for x in self.rgb))

    def contrasted(self, min_contrast: float = 4.5) -> "Color":
        """Returns a new Color that is in contrast with :param self:

        :param min_contrast: Minimum contrast. Must be in range (0-21)
        """
        pass

    @staticmethod
    def from_str(arg: str) -> "Color":
        """Creates a Color object from string

        :param arg: Input string. Must be either "random", Color name, (R,G,B), #HEX or HEX
        :return: New Color object
        """
        hex_groups = hex_re.fullmatch(arg)
        rgb_groups = rgb_re.fullmatch(arg)

        if hex_groups is not None:
            rgb = parse_hex(hex_groups.group(1))
        elif rgb_groups is not None:
            rgb = int_tuple(rgb_groups.group(1), rgb_groups.group(2), rgb_groups.group(3))
            if not all(0 <= c <= 255 for c in rgb):
                raise ValueError('Invalid RGB values')
        else:
            name = normalized(arg)

            if name == 'random':
                rgb = choice(tuple(hex_to_color))
            else:
                if name not in color_to_hex:
                    raise NameError(f'"{arg}" is not a color name')

                rgb = color_to_hex[name]

            rgb = parse_hex(rgb)

        return Color(rgb)
