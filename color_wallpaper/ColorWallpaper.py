"""Main file"""

import re
import sys

from pathlib import Path
from typing import Tuple, Union, List

try:
    from PIL import Image, ImageDraw
except ImportError:
    print(f'Unable to import PIL. Install it by running "{sys.executable} -m pip install Pillow".')
    exit(-1)

from .common import *
from .data import *
from .Color import *
from .CLI import *


__all__ = ["Wallpaper"]


newline_re = re.compile(r"(?:\n|\\n)")


class Wallpaper:
    """Main class"""

    USABLE_SIZE = 112

    # File options
    output: Union[str, Path]
    yes: bool

    # Color options
    color: Color
    color2: Color
    display: str
    min_contrast: float
    overlay_color: Color
    overlay_contrast: float

    # Display options
    resolution: Tuple[int, int]
    scale: int
    formats: List[str]

    def __init__(self, **kwargs):
        options = get_options()

        for arg in self.__class__.__annotations__:
            setattr(self, arg, kwargs.get(arg, getattr(options, arg)))

        self.output = Path(self.output).absolute()

        random = False

        if type(self.color) is str:
            random = normalized(self.color) == "random"

            if random:
                self.color = Color.random()
            else:
                self.color = Color.from_str(self.color)

        inverted = type(self.color2) is str and normalized(self.color2) == "inverted"

        while True:
            if self.overlay_color is not None:
                if not random and self.color / self.overlay_color < self.overlay_contrast:
                    raise RuntimeError(
                        f"Contrast of {self.color} and {self.overlay_color} is lower than "
                        f"{self.overlay_contrast} ({self.color / self.overlay_color})"
                    )

                while self.color / self.overlay_color < self.overlay_contrast:
                    self.color = Color.random()

            if inverted:
                try:
                    self.color2 = self.color.inverted(self.min_contrast)
                except RuntimeError:
                    if random:
                        self.color = Color.random()
                    else:
                        raise
                else:
                    break
            else:
                self.color2 = Color.from_str(self.color2)
                break

    @classmethod
    def _split_word(cls, word: str) -> List[str]:
        head = ""
        word_length = 0
        word = list(word)

        while word:
            next_char = word.pop(0)

            next_char_length = len(font(next_char)[0])

            if word_length + next_char_length <= cls.USABLE_SIZE:
                head += next_char
                word_length += next_char_length
            else:
                word.insert(0, next_char)
                break

        return [head, "".join(word)]

    @classmethod
    def _arrange_text(cls, text: str) -> Tuple[List[str], int]:
        """Wraps the text

        :param text: Text to wrap
        :return: Tuple of Wrapped text and max pixel width
        """
        first_glyph_whitespace = len(font(" ")[0]) + 1

        texts = [[]]
        max_text_length = 0
        text_length = -first_glyph_whitespace
        words = newline_re.sub(r" \n ", text).split(" ")

        while words:
            next_word = words.pop(0)

            next_word_length = sum(len(font(char)[0]) for char in f" {next_word}")

            if next_word_length - 4 > cls.USABLE_SIZE:
                words = cls._split_word(next_word) + words
                continue

            if next_word == "\n":
                texts.append([])
                text_length = -first_glyph_whitespace
            elif text_length + next_word_length <= cls.USABLE_SIZE:
                texts[-1].append(next_word)
                text_length += next_word_length
            else:
                texts.append([next_word])
                text_length = next_word_length - first_glyph_whitespace
            max_text_length = min(max(text_length, max_text_length), cls.USABLE_SIZE)

        return [" ".join(text) for text in texts], max_text_length

    def _generate_text(self, text: str) -> Image.Image:
        """Renders text into image

        :param text: text to render
        :return: Image with the rendered text
        """
        texts, max_text_length = self._arrange_text(text)

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

    def _generate_decoration(self) -> Image.Image:
        """Generates the highlight from :param self:

        :return: Image of the highlight
        """
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127), outline=self.color2.rgb, width=3)

        y = -4
        if self.display != "":
            name = self.color.name if self.display is None else self.display
            img_name = self._generate_text(name)
            x, y = img_name.size

            img.alpha_composite(img_name, (8, 8))

            if y > self.USABLE_SIZE:
                print("Display text is too long and will be cut off", file=sys.stderr)

        rows = {
            "hex": ("HEX ", self.color.hex(True)),
            "#hex": ("HEX ", "#" + self.color.hex(True)),
            "HEX": ("HEX ", self.color.hex(False)),
            "#HEX": ("HEX ", "#" + self.color.hex(False)),
            **{k: (f"{k.upper()} ", " ".join(map(str, getattr(self.color, k)))) for k in ("rgb", "hsv", "hsl", "cmyk")},
            "empty": (" ", " "),
        }

        for i, key in enumerate(self.formats):
            if y > self.USABLE_SIZE:
                ignored = len(self.formats) - i
                if ignored:
                    print(
                        f"Unable to display {ignored} format{'' if ignored == 1 else 's'}: "
                        f"{', '.join(self.formats[i:])}",
                        file=sys.stderr,
                    )

                break

            y += 12
            img_label = self._generate_text(rows[key][0])
            img.alpha_composite(img_label, (8, y))
            img.alpha_composite(self._generate_text(rows[key][1]), (3 + 5 + img_label.size[0], y))

        return img

    def generate_image(self, save: bool = True) -> Image.Image:
        """Generates a wallpaper from :param self:

        :param save: Whether to save the image to `self.output`
        :return: The generated image
        """
        img = Image.new("RGBA", self.resolution, self.color.rgb)

        smaller = min(self.resolution)
        decor_size = 128 * min(self.scale, (smaller - 22) // 128)

        decoration = self._generate_decoration()
        decoration = decoration.resize((decor_size, decor_size), resample=Image.NEAREST)

        img.alpha_composite(
            decoration, ((self.resolution[0] - decor_size) // 2, (self.resolution[1] - decor_size) // 2)
        )

        generate = True

        if save:
            if not self.output.exists():
                self.output.parent.mkdir(parents=True, exist_ok=True)
                img.save(str(self.output))
            elif self.output.is_file():
                generate = self.yes or input(f'File "{self.output}" exists.\nOverwrite? [y/n] ').lower().startswith("y")

                if generate:
                    img.save(str(self.output))
            else:
                raise IOError(f'The "{self.output}" exists and is not a file')

        if generate:
            print(f'Image "{self.output}" successfully generated')

        return img
