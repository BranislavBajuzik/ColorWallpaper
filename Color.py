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
    def __init__(self, rgb: Tuple[int, int, int], name: str):
        self.rgb = rgb
        self.name = name

    @property
    def hsv(self) -> Tuple[int, int, int]:
        h, s, v = rgb_to_hsv(*(comp/255 for comp in self.rgb))

        return int(h*360), int(s*100), int(v*100)

    @property
    def hsl(self) -> Tuple[int, int, int]:
        h, l, s = rgb_to_hls(*(comp/255 for comp in self.rgb))

        return int(h*360), int(s*100), int(l*100)

    @property
    def cmyk(self) -> Tuple[int, int, int, int]:
        c, m, y = (1 - comp/255 for comp in self.rgb)

        k = min(c, m, y, 1)

        if k == 1:
            return 0, 0, 0, 100

        c = (c - k) / (1.0 - k)
        m = (m - k) / (1.0 - k)
        y = (y - k) / (1.0 - k)

        return tuple(int(comp*100) for comp in (c, m, y, k))

    @property
    def luminance(self) -> float:
        r, g, b = (c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
                   for c in (comp/255 for comp in self.rgb))

        return r*0.2126 + g*0.7152 + b*0.0722

    def __truediv__(self, other) -> float:
        contrasts = sorted((self.luminance, other.luminance), reverse=True)

        return (contrasts[0] + 0.05) / (contrasts[1] + 0.05)

    def __floordiv__(self, other) -> int:
        return int(self / other)

    def inverted(self) -> "Color":
        rgb: Tuple[int, int, int] = tuple(255 - x for x in self.rgb)
        return Color(rgb, hex_to_color.get(''.join(f'{c:02x}' for c in rgb)))

    @staticmethod
    def from_str(arg: str) -> "Color":
        hex_groups = hex_re.fullmatch(arg)
        rgb_groups = rgb_re.fullmatch(arg)

        name = None

        if hex_groups is not None:
            rgb = parse_hex(hex_groups.group(1))
        elif rgb_groups is not None:
            rgb = int_tuple(rgb_groups.group(0),
                            rgb_groups.group(1),
                            rgb_groups.group(2))
            if not all(0 <= c <= 255 for c in rgb):
                raise ValueError('invalid RGB values')
        else:
            name = normalized(arg)

            if name == 'random':
                rgb = choice(tuple(hex_to_color))
                name = hex_to_color[rgb]
            else:
                if name not in color_to_hex:
                    raise NameError(f'{arg} is not a color name')

                rgb = color_to_hex[name]

            rgb = parse_hex(rgb)

        if name is None:
            name = 'anonymous'

        return Color(rgb, pretty_names.get(name, name.capitalize()))
