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


__all__ = ["Wallpaper"]


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

    @staticmethod
    def __split_word(word: str) -> List[str]:
        head = ""
        word_length = 0
        word = list(word)

        while word:
            next_char = word.pop(0)

            next_char_length = len(font(next_char)[0])

            if word_length + next_char_length <= 112:
                head += next_char
                word_length += next_char_length
            else:
                word.insert(0, next_char)
                break

        return [head, "".join(word)]

    @staticmethod
    def __arrange_text(text: str) -> Tuple[List[str], int]:
        """Wraps the text

        :param text: Text to wrap
        :return: Tuple of Wrapped text and max pixel width
        """
        first_glyph_whitespace = len(font(" ")[0]) + 1

        texts = [[]]
        max_text_length = 0
        text_length = -first_glyph_whitespace
        words = text.split(" ")

        while words:
            next_word = words.pop(0)

            next_word_length = sum(len(font(char)[0]) for char in f" {next_word}")

            if next_word_length > 112:
                words = Wallpaper.__split_word(next_word) + words
                continue

            if text_length + next_word_length <= 112:
                texts[-1].append(next_word)
                text_length += next_word_length
            else:
                texts.append([next_word])
                text_length = next_word_length - first_glyph_whitespace
            max_text_length = min(max(text_length, max_text_length), 112)

        return [" ".join(text) for text in texts], max_text_length

    def __generate_text(self, text: str) -> Image.Image:
        """Renders text into image

        :param text: text to render
        :return: Image with the rendered text
        """
        texts, max_text_length = self.__arrange_text(text)

        x = 0
        x_offset = 0
        y_offset = 0
        width = max_text_length
        height = len(texts) * 12 - 4
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        for text in texts:
            for char in text:
                pixel_map = font(char)

                for y, row in enumerate(pixel_map):

                    for x, pixel in enumerate(row):
                        if pixel and x_offset + x < width and y_offset + y < height:
                            img.putpixel((x_offset + x, y_offset + y), self.color2.rgb)

                x_offset += x + 1
            x_offset = 0
            y_offset += 12

        return img

    def __generate_decoration(self) -> Image.Image:
        """Generates the highlight from :param self:

        :return: Image of the highlight
        """
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127), outline=self.color2.rgb, width=3)

        y = -4
        if self.display != "":
            name = self.color.name if self.display is None else self.display
            img_name = self.__generate_text(name)
            x, y = img_name.size

            img.alpha_composite(img_name, (8, 8))

        rows = {
            "hex": ("HEX ", self.color.hex(True)),
            "#hex": ("HEX ", "#" + self.color.hex(True)),
            "HEX": ("HEX ", self.color.hex(False)),
            "#HEX": ("HEX ", "#" + self.color.hex(False)),
            **{k: (f"{k.upper()} ", " ".join(map(str, getattr(self.color, k)))) for k in ("rgb", "hsv", "hsl", "cmyk")},
            "empty": (" ", " "),
        }

        for i, key in enumerate(self.formats, 1):
            y += 12
            img_label = self.__generate_text(rows[key][0])
            img.alpha_composite(img_label, (8, y))
            img.alpha_composite(self.__generate_text(rows[key][1]), (3 + 5 + img_label.size[0], y))

            if y >= 116:
                ignored = len(self.formats) - i
                if ignored:
                    print(
                        f"Too many formats specified. "
                        f"Ignoring {ignored} format{'' if ignored == 1 else 's'}: "
                        f"{', '.join(self.formats[i:])}",
                        file=sys.stderr,
                    )

                break

        return img

    def generate_image(self):
        """Generates a wallpaper from :param self:"""
        img = Image.new("RGBA", self.resolution, self.color.rgb)

        smaller = min(self.resolution)
        decor_size = 128 * max(round(smaller / self.scale / 128), 1)

        decoration = self.__generate_decoration()
        decoration = decoration.resize((decor_size, decor_size), resample=Image.NEAREST)

        img.alpha_composite(
            decoration, ((self.resolution[0] - decor_size) // 2, (self.resolution[1] - decor_size) // 2)
        )

        generate = True

        if not self.output.exists():
            self.output.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(self.output))
        elif self.output.is_file():
            generate = self.yes or input(f'File "{self.output}" exists.\n' f"Overwrite? [y/n] ").lower().startswith("y")

            if generate:
                img.save(str(self.output))
        else:
            raise IOError(f'The "{self.output}" exists and is not a file')

        if generate:
            print(f'Image "{self.output}" successfully generated')


if __name__ == "__main__":
    Wallpaper(get_options()).generate_image()
