import sys
import argparse

from pathlib import Path
from typing import Tuple, Union, List

try:
    from PIL import Image, ImageDraw
except ImportError:
    print(f'Unable to import PIL. Install it by running '
          f'"{sys.executable} -m pip install Pillow".')
    exit(-1)

from data import *
from CLI import *
from Color import *


__all__ = ['Wallpaper']


class Wallpaper:
    def __init__(self, options: argparse.Namespace):
        self.output: Union[str, Path] = options.output
        self.resolution: Tuple[int, int] = options.resolution
        self.scale: int = options.scale
        self.color: Color = options.color
        self.color2: Color = options.color2
        self.display: str = options.display
        self.formats: List[str] = options.formats
        self.x: str = 'x' if options.lowercase else 'X'
        self.y: bool = options.yes

    def __generate_text(self, text: str) -> Image.Image:
        text_length = sum(len(font(char)[0]) for char in text) - 1
        img = Image.new('RGBA', (text_length, 8), (0, 0, 0, 0))
        offset = 0
        x = 0

        for char in text:
            pixel_map = font(char)

            for y, row in enumerate(pixel_map):
                for x, pixel in enumerate(row):
                    if pixel:
                        img.putpixel((offset + x, y), self.color2.rgb)

            offset += x + 1

        return img

    def __generate_decoration(self) -> Image.Image:
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127),
                                      outline=self.color2.rgb, width=3)

        y = -4
        if self.display != '':
            name = self.color.name if self.display is None else self.display
            img_name = self.__generate_text(name)
            x, y = img_name.size

            if x <= 112:
                img.alpha_composite(img_name, (8, y))
            else:
                text1, text2 = name.rsplit(' ', 1)
                img.alpha_composite(self.__generate_text(text1), (8, y))
                y += 12
                img.alpha_composite(self.__generate_text(text2), (8, y))

        hex_format = f'{{0:02{self.x}}}'

        rows = {
            'hex': (
                'HEX ',
                ''.join(hex_format.format(c) for c in self.color.rgb)
            ),
            '#hex': (
                'HEX ',
                '#' + ''.join(hex_format.format(c) for c in self.color.rgb)
            ),
            'rgb': ('RGB ', ' '.join(map(str, self.color.rgb))),
            'hsv': ('HSV ', ' '.join(map(str, self.color.hsv))),
            'hsl': ('HSL ', ' '.join(map(str, self.color.hsl))),
            'cmyk': ('CMYK ', ' '.join(map(str, self.color.cmyk))),
            'empty': (' ', ' ')
        }

        for key in self.formats:
            y += 12
            img_label = self.__generate_text(rows[key][0])
            img.alpha_composite(img_label, (8, y))
            img.alpha_composite(self.__generate_text(rows[key][1]),
                                (3 + 5 + img_label.size[0], y))

        return img

    def generate_image(self) -> Image:
        img = Image.new('RGBA', self.resolution, self.color.rgb)

        smaller = min(self.resolution)
        decor_size = 128 * max(round(smaller / self.scale / 128), 1)

        decoration = self.__generate_decoration()
        decoration = decoration.resize((decor_size, decor_size))

        img.alpha_composite(decoration, ((self.resolution[0]-decor_size) // 2,
                                         (self.resolution[1]-decor_size) // 2))

        if not self.output.exists():
            self.output.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(self.output))
        elif self.output.is_file():
            if self.y or input(f'File "{self.output}" exists.\n'
                               f'Overwrite? [y/n] ').lower().startswith('y'):
                img.save(str(self.output))
        else:
            raise IOError(f'The "{self.output}" exists and is not a file')

        print(f'Image "{self.output}" successfully generated')


if __name__ == '__main__':
    while True:
        env_options = get_options()

        if Color((255, 255, 255), '') / env_options.color > 2:
            break

    Wallpaper(get_options()).generate_image()
