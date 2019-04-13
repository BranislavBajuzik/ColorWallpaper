import re
import argparse

from PIL import Image, ImageDraw
from pathlib import Path
from typing import Tuple, Union

from data import *


__all__ = ['Wallpaper']

hex_re = re.compile(r'\s*#?([\da-f]{6}|[\da-f]{3})\s*', re.I)
rgb_re = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\s*')
resolution_re = re.compile(r'\s*(\d+)\s*[x:]\s*(\d+)\s*')


def get_options(args=None) -> argparse.Namespace:
    def normalized(s: str) -> str:
        return ''.join(s.split()).lower()

    def int_tuple(*t) -> Tuple[int, ...]:
        return tuple(map(int, t))

    def parse_hex(arg: str) -> Tuple[int, int, int]:
        le = len(arg)
        return tuple(int(arg[le//3*i:le//3*(i+1)], 16) for i in range(3))

    def color(arg: str) -> Color:
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
                raise argparse.ArgumentTypeError('invalid RGB values')
        else:
            name = normalized(arg)
            if name not in color_to_hex:
                raise argparse.ArgumentTypeError(f'{arg} is not a color')

            rgb = parse_hex(color_to_hex[name])

        if name is None:
            name = hex_to_color.get(''.join(f'{c:02x}' for c in rgb))

        return Color(rgb, pretty_names.get(name, name.capitalize()))

    def inverted_color(source: Tuple[int, int, int]) -> Color:
        rgb: Tuple[int, int, int] = tuple(255 - x for x in source)
        return Color(rgb, hex_to_color.get(''.join(f'{c:02x}' for c in rgb)))

    def resolution(arg: str) -> Tuple[int, int]:
        groups = resolution_re.fullmatch(arg)

        if groups is None:
            raise argparse.ArgumentTypeError('Unable to parse the resolution')

        res = int_tuple(groups.group(1), groups.group(2))

        if any(dimension < 300 for dimension in res):
            raise argparse.ArgumentTypeError('Minimal resolution is 200x200')

        return res

    ret = argparse.ArgumentParser(description='Minimalist wallpaper generator')

    ret.add_argument('-o', '--output', metavar='PATH', default=Path('out.png'),
                     type=color, help='Image output path')

    ret.add_argument('-c', '--color', default=Color((255, 2, 141), 'Hot Pink'),
                     type=color, help='#Hex / R,G,B / name of background color')

    ret.add_argument('-c2', '--color2', metavar='COLOR',
                     type=color, help='#Hex / R,G,B / name of highlight color')

    ret.add_argument('-r', '--resolution', default=(1920, 1080),
                     type=resolution, help='WIDTHxHEIGHT')

    ret = ret.parse_args(args)

    if ret.color2 is None:
        ret.color2 = inverted_color(ret.color.rgb)

    return ret


class Color:
    def __init__(self, rgb: Tuple[int, int, int], name: str):
        self.rgb = rgb
        self.name = name


class Wallpaper:
    def __init__(self, options: argparse.Namespace):
        self.output: Union[str, Path] = options.output
        self.resolution: Tuple[int, int] = options.resolution
        self.color: Color = options.color
        self.color2: Color = options.color2

    def __generate_text(self, text: str) -> Image.Image:
        text_length = sum(len(font[char][0]) for char in text) - 1
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))

        return img

    def __generate_decoration(self) -> Image.Image:
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127),
                                      outline=self.color2.rgb, width=3)

        img.alpha_composite(self.__generate_text(self.color.name), (8, 8))

        label = self.__generate_text('HEX')
        img.alpha_composite(label, (8, 20))
        img.alpha_composite(
            self.__generate_text(''.join(f'{c:02x}' for c in self.color.rgb)),
            (16 + label.size[1], 20)
        )

        label = self.__generate_text('RGB')
        img.alpha_composite(label, (8, 32))
        img.alpha_composite(
            self.__generate_text(' '.join(map(str, self.color.rgb))),
            (16 + label.size[1], 32)
        )

        return img.resize((256, 256))

    def generate_image(self) -> Image:
        def position(size) -> int:
            return (size - decor_size) // 2

        img = Image.new('RGBA', self.resolution, self.color.rgb)

        smaller = min(self.resolution)
        decor_size = smaller // 4

        decoration = self.__generate_decoration()
        decoration = decoration.resize([decor_size]*2)

        img.alpha_composite(decoration,
                            (position(self.resolution[0]),
                             position(self.resolution[1])))

        img.save(str(self.output))


if __name__ == '__main__':
    paper = Wallpaper(get_options())

    paper.generate_image()
