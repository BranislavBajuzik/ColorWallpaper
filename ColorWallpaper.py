import re
import argparse

from PIL import Image
from pathlib import Path
from typing import Tuple, Union

from data import *

hex_re = re.compile(r'\s*#?([\da-f]{6}|[\da-f]{3})\s*', re.I)
rgb_re = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\s*')
resolution_re = re.compile(r'\s*(\d+)\s*[x:]\s*(\d+)\s*')


def normalized(s: str) -> str:
    return ''.join(s.split()).lower()


def int_tuple(*t) -> Tuple[int, ...]:
    return tuple(map(int, t))


def get_options(args=None) -> argparse.Namespace:
    def color(arg: str) -> Tuple[Tuple[int, int, int], str]:
        hex_groups = hex_re.fullmatch(arg)
        rgb_groups = rgb_re.fullmatch(arg)

        name = None

        if hex_groups is not None:
            match = hex_groups.group(1)
            le = len(match)
            rgb = [int(match[le//3*i:le//3*(i+1)], 16) for i in range(3)]
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

            rgb = [int(color_to_hex[name][6//3*i:6//3*(i+1)]) for i in range(3)]

        if name is None:
            name = hex_to_color.get(''.join(f'{c:02x}' for c in rgb))

        return tuple(rgb), name

    def inverted_color(source: Tuple[int, int, int]
                       ) -> Tuple[Tuple[int, int, int], str]:
        rgb: Tuple[int, int, int] = tuple(255 - x for x in source)
        return rgb, hex_to_color.get(''.join(f'{c:02x}' for c in rgb))

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

    ret.add_argument('-c', '--color', default=((255, 2, 141), 'hotpink'),
                     type=color, help='#Hex / R,G,B / name of background color')

    ret.add_argument('-c2', '--color2', metavar='COLOR',
                     type=color, help='#Hex / R,G,B / name of highlight color')

    ret.add_argument('-r', '--resolution', default=(1920, 1080),
                     type=resolution, help='WIDTHxHEIGHT')

    ret = ret.parse_args(args)

    if ret.color2 is None:
        ret.color2 = inverted_color(ret.color[0])

    return ret


def generate_image(target: Union[str, Path], resolution: Tuple[int, int],
                   color: Tuple[Tuple[int, int, int], str],
                   color2: Tuple[Tuple[int, int, int], str]) -> Image:
    img = Image.new('RGB', resolution, color[0])

    img.save(str(target))


if __name__ == '__main__':
    options = get_options()

    generate_image(options.output, options.resolution,
                   options.color, options.color2)
