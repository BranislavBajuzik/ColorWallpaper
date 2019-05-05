"""Main file"""

import sys
import argparse

from pathlib import Path
from typing import Tuple, Union, List

try:
    from PIL import Image, ImageDraw
except ImportError:
    print(f'Unable to import PIL. Install it by running "{sys.executable} -m pip install Pillow".')
    exit(-1)

from data import *
from CLI import *
from Color import *


__all__ = ['Wallpaper']


class Wallpaper:
    """Main class"""
    def __init__(self, options: argparse.Namespace):
        # General options
        self.output: Union[str, Path] = options.output
        self.yes: bool = options.yes

        # Color options
        self.color: Color = options.color
        self.color2: Color = options.color2
        self.display: str = options.display

        # Display options
        self.resolution: Tuple[int, int] = options.resolution
        self.scale: int = options.scale
        self.formats: List[str] = options.formats

    def __generate_text(self, text: str) -> Image.Image:
        """Renders text into image

        :param text: text to render
        :return: Image with the rendered text
        """
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
        """Generates the highlight from :param self:

        :return: Image of the highlight
        """
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127), outline=self.color2.rgb, width=3)

        y = -4
        if self.display != '':
            name = self.color.name if self.display is None else self.display
            img_name = self.__generate_text(name)
            x, y = img_name.size

            if x <= 112:  # ToDo Split the words. Needs a proper implementation
                img.alpha_composite(img_name, (8, y))
            else:
                text1, text2 = name.rsplit(' ', 1)
                img.alpha_composite(self.__generate_text(text1), (8, y))
                y += 12
                img.alpha_composite(self.__generate_text(text2), (8, y))

        rows = {
            'hex': ('HEX ', self.color.hex(True)),
            '#hex': ('HEX ', '#' + self.color.hex(True)),
            'HEX': ('HEX ', self.color.hex(False)),
            '#HEX': ('HEX ', '#' + self.color.hex(False)),
            **{k: (f'{k.upper()} ', ' '.join(map(str, getattr(self.color, k))))
               for k in ('rgb', 'hsv', 'hsl', 'cmyk')},
            'empty': (' ', ' ')
        }

        for key in self.formats:
            y += 12
            img_label = self.__generate_text(rows[key][0])
            img.alpha_composite(img_label, (8, y))
            img.alpha_composite(self.__generate_text(rows[key][1]), (3 + 5 + img_label.size[0], y))

        return img

    def generate_image(self):
        """Generates a wallpaper from :param self:"""
        img = Image.new('RGBA', self.resolution, self.color.rgb)

        smaller = min(self.resolution)
        decor_size = 128 * max(round(smaller / self.scale / 128), 1)

        decoration = self.__generate_decoration()
        decoration = decoration.resize((decor_size, decor_size))

        img.alpha_composite(decoration, ((self.resolution[0]-decor_size) // 2, (self.resolution[1]-decor_size) // 2))

        if not self.output.exists():
            self.output.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(self.output))
        elif self.output.is_file():
            if self.yes or input(f'File "{self.output}" exists.\n'
                                 f'Overwrite? [y/n] ').lower().startswith('y'):
                img.save(str(self.output))
        else:
            raise IOError(f'The "{self.output}" exists and is not a file')

        print(f'Image "{self.output}" successfully generated')


if __name__ == '__main__':
    Wallpaper(get_options()).generate_image()
