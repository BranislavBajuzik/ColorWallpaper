"""Handles color calculations."""

import re
from colorsys import hls_to_rgb, rgb_to_hls, rgb_to_hsv
from random import choice
from typing import Tuple

from .common import int_tuple, normalized, parse_hex
from .data import color_hexes, color_to_hex, hex_to_color

__all__ = ["Color"]


# http://colorizer.org/ <-- Very nice
hex_re = re.compile(r"\s*#?([\da-f]{6}|[\da-f]{3})\s*", re.I)
rgb_re = re.compile(r"\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\s*")


class Color:
    """Class for color handling."""

    def __init__(self, rgb: Tuple[int, int, int], name: str = None):
        """Color constructor.

        :param rgb: (R,G,B) of the color
        :param name: Overrides the color name lookup
        """
        if len(rgb) != 3 or not all(0 <= c <= 255 for c in rgb):
            raise ValueError("Invalid RGB values")
        self.rgb = rgb

        if name is None:
            self.name = hex_to_color.get(self.hex, "Anonymous")
        else:
            self.name = name

    def __str__(self):
        """Return str(self)."""
        return f"Color(rgb={self.rgb}, name='{self.name}')"

    def __repr__(self):
        """Return repr(self)."""
        return str(self)

    def __eq__(self, other):
        """Return self==other."""
        return self.rgb == other.rgb and self.name == other.name

    @staticmethod
    def __normalize(components: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Convert int RGB to float RGB."""
        return tuple(component / 255 for component in components)  # type: ignore

    @property  # noqa: A003
    def hex(self) -> str:
        """Return lowercase HEX representation of :param self:."""
        return "".join(f"{c:02x}" for c in self.rgb)

    @property
    def HEX(self) -> str:
        """Return uppercase HEX representation of :param self:."""
        return "".join(f"{c:02X}" for c in self.rgb)

    @property
    def hsv(self) -> Tuple[int, int, int]:
        """Return HSV representation of :param self:."""
        h, s, v = rgb_to_hsv(*self.__normalize(self.rgb))

        return int(h * 360), int(s * 100), int(v * 100)

    @property
    def hsl(self) -> Tuple[int, int, int]:
        """Return HSL representation of :param self:."""
        h, l, s = rgb_to_hls(*self.__normalize(self.rgb))

        return int(h * 360), int(s * 100), int(l * 100)

    @property
    def cmyk(self) -> Tuple[int, int, int, int]:
        """Return CMYK representation of :param self:."""
        c, m, y = (1 - component / 255 for component in self.rgb)

        k = min(c, m, y, 1)

        if k == 1:
            return 0, 0, 0, 100

        c, m, y = ((component - k) / (1.0 - k) for component in (c, m, y))

        return int_tuple(component * 100 for component in (c, m, y, k))  # type: ignore

    @property
    def luminance(self) -> float:
        """Return relative luminance of :ref:`self` as defined by WCAG 2.1 (as of August 2020).

        https://www.w3.org/TR/2008/REC-WCAG20-20081211/Overview.html#relativeluminancedef

        :return: Relative luminance
        """
        r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in self.__normalize(self.rgb))

        return r * 0.2126 + g * 0.7152 + b * 0.0722

    def __truediv__(self, other: "Color") -> float:
        """Return contrast ratio of :ref:`self` and :ref:`other` as defined by WCAG 2.1 (as of August 2020).

        https://www.w3.org/TR/2008/REC-WCAG20-20081211/Overview.html#contrast-ratiodef

        :param other: The second Color object to compare against
        :return: Contrast ratio
        """
        lighter, darker = sorted((self.luminance, other.luminance), reverse=True)

        return (lighter + 0.05) / (darker + 0.05)

    def __floordiv__(self, other: "Color") -> int:
        """Floor version of :method:`__truediv__`."""
        return int(self / other)

    def inverted(self, min_contrast: float = None) -> "Color":
        """Return a new Color that is in contrast with :param self:.

        :param min_contrastt: Minimum contrast. Must be in range (1-21)
        """
        ret = Color(tuple(255 - x for x in self.rgb))  # type: ignore

        if min_contrast is None or min_contrast == 1:
            return ret

        if not 1 <= min_contrast <= 21:
            raise ValueError(f"min_contrast is outside of [1, 21]: {min_contrast}")

        if self / ret >= min_contrast:
            return ret

        hue, saturation, lightness = ret.hsl
        lightness_down, lightness_up = lightness - 1, lightness + 1

        while lightness_down >= 0 and lightness_up <= 100:
            if lightness_down >= 0:
                ret = self.from_hsl(hue, saturation, lightness_down)

                if self / ret >= min_contrast:
                    return ret

                lightness_down -= 1

            if lightness_up <= 100:
                ret = self.from_hsl(hue, saturation, lightness_up)

                if self / ret >= min_contrast:
                    return ret

                lightness_up += 1

        raise RuntimeError(f"Unable to to find a color that has contrast of at least {min_contrast} with {self}")

    @staticmethod
    def random() -> "Color":
        """Return random named color."""
        return Color(parse_hex(choice(color_hexes)))

    @staticmethod
    def from_hsl(hue: int, saturation: int, lightness: int) -> "Color":
        """Create a Color object from hue, saturation and luminance.

        :param hue: Hue
        :param saturation: Saturation
        :param lightness: Lightness
        :return: New Color object
        """
        components = (360, hue, "h"), (100, lightness, "l"), (100, saturation, "s")

        for bound, component, name in components:
            if not 0 <= component <= bound:
                raise ValueError(f"{name} is outside of [0, {bound}]: {component}")

        rgb = hls_to_rgb(*(component / bound for bound, component, name in components))

        return Color(int_tuple(component * 255 for component in rgb))  # type: ignore

    @staticmethod
    def from_str(arg: str) -> "Color":
        """Create a Color object from string.

        :param arg: Input string. Must be either Color name, (R,G,B), #HEX or HEX
        :return: New Color object
        """
        hex_groups = hex_re.fullmatch(arg)
        rgb_groups = rgb_re.fullmatch(arg)

        if hex_groups is not None:
            rgb = parse_hex(hex_groups.group(1))
        elif rgb_groups is not None:
            rgb = int_tuple(rgb_groups.group(1), rgb_groups.group(2), rgb_groups.group(3))  # type: ignore
            if not all(0 <= c <= 255 for c in rgb):
                raise ValueError("Invalid RGB values")
        else:
            name = normalized(arg)

            if name not in color_to_hex:
                raise ValueError(f'"{arg}" is not a color name')

            rgb = parse_hex(color_to_hex[name])

        return Color(rgb)
