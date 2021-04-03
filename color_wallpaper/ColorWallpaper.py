import logging
import re
import sys
from pathlib import Path
from random import sample
from typing import Any, Generator, Iterable, List, Optional, Tuple

from .cli import get_options
from .color import Color
from .common import normalized, safe_path_name
from .data import color_hexes, font, hex_to_color

try:
    from PIL import Image, ImageDraw
except ImportError:
    print(f'Unable to import PIL. Install it by running "{sys.executable} -m pip install Pillow".')
    exit(-1)


__all__ = ["Wallpaper"]

newline_re = re.compile(r"(?:\n|\\n)")


class Wallpaper:
    """Main class."""

    USABLE_SIZE = 112

    # File options
    output: Path
    yes: bool

    # Color options
    color: Color
    color2: Color
    display: Optional[str]
    min_contrast: float
    overlay_color: Color
    overlay_contrast: float

    # Display options
    resolution: Tuple[int, int]
    scale: int
    formats: List[str]

    # Misc options
    log_level: int

    def __init__(self, args: List[str] = None, logger: logging.Logger = None, **kwargs: Any):
        """Wallpaper object constructor.

        :param args: Will override :ref:`sys.argv`
        :param logger: Logger to use.
        :param kwargs: Used to override the default values of the class arguments.
        """
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger("color-wallpaper")
            self.logger.setLevel(logging.CRITICAL)

        if args is None:
            args = sys.argv[1:]

        options = get_options(args)

        for arg in self.__class__.__annotations__:
            setattr(self, arg, kwargs.get(arg, getattr(options, arg)))

        self._process_args()

    def _process_args(self) -> None:
        """Process the arguments passed to this object."""
        self.output = Path(self.output).absolute()

        random = False

        if type(self.color) is str:  # type: ignore
            random = normalized(self.color) == "random"  # type: ignore

            if random:
                self.color = Color.random()
            else:
                self.color = Color.from_str(self.color)  # type: ignore

        inverted = type(self.color2) is str and normalized(self.color2) == "inverted"  # type: ignore

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
                self.color2 = Color.from_str(self.color2)  # type: ignore
                break

    @classmethod
    def _split_word(cls, word: str) -> List[str]:
        """Split the word so it fits.

        :param word: Word to split
        :return: List of head and rest of the word
        """
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
        """Wrap the text.

        :param text: Text to wrap
        :return: Tuple of Wrapped text and max pixel width
        """
        first_glyph_whitespace = len(font(" ")[0]) + 1

        texts: List[List[str]] = [[]]
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
        """Render text into image.

        :param text: text to render
        :return: Image with the rendered text
        """
        self.logger.debug("Rendering text `%s`", text)

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
        """Generate the highlight from :param self:.

        :return: Image of the highlight
        """
        self.logger.debug("Generating the decoration")

        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

        ImageDraw.Draw(img).rectangle((0, 0, 127, 127), outline=self.color2.rgb, width=3)

        y = -4
        if self.display != "":
            self.logger.debug("Adding color name")

            name = self.color.name if self.display is None else self.display
            img_name = self._generate_text(name)
            x, y = img_name.size

            img.alpha_composite(img_name, (8, 8))

            if y > self.USABLE_SIZE:
                self.logger.warning("Display text is too long (tall) and will be cut off")

        rows = {
            "hex": ("HEX ", self.color.hex),
            "HEX": ("HEX ", self.color.HEX),
            "#hex": ("HEX ", "#" + self.color.hex),
            "#HEX": ("HEX ", "#" + self.color.HEX),
            **{
                variant: (f"{variant.upper()} ", " ".join(map(str, getattr(self.color, variant))))
                for variant in ("rgb", "hsv", "hsl", "cmyk")
            },
            "empty": (" ", " "),
        }

        for i, key in enumerate(self.formats):
            self.logger.debug("Adding `%s` format", key)

            if y > self.USABLE_SIZE:
                ignored = len(self.formats) - i
                if ignored:
                    self.logger.warning(
                        "Unable to display %s format%s: %s",
                        ignored,
                        "" if ignored == 1 else "s",
                        ", ".join(self.formats[i:]),
                    )

                break

            y += 12
            label, value = rows[key]
            img_label = self._generate_text(label)
            img.alpha_composite(img_label, (8, y))
            img.alpha_composite(self._generate_text(value), (3 + 5 + img_label.size[0], y))

        return img

    def generate_image(self, save: bool = False) -> Image.Image:
        """Generate a wallpaper from :param self:.

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
                try:
                    self.output.parent.mkdir(parents=True, exist_ok=True)
                except Exception as ex:
                    raise OSError(f"Unable to create output directory: {ex}") from None

                img.save(str(self.output))
            elif self.output.is_file():
                generate = self.yes or input(f'File "{self.output}" exists.\nOverwrite? [y/n] ').lower().startswith("y")

                if generate:
                    if not self.output.suffix:
                        self.output.with_suffix(".png")

                    img.save(str(self.output))
            else:
                raise FileExistsError(f'The "{self.output}" exists and is not a file')

        if generate:
            self.logger.info('Image "%s" successfully generated', self.output)

        return img

    @staticmethod
    def generate_all_images(
        output_dir: str = None, count: int = -1, extension: str = "png", logger: logging.Logger = None, **kwargs: Any
    ) -> Generator[Image.Image, None, None]:
        """Generate a wallpaper from :param self:.

        :param output_dir: Where to generate the wallpapers to
        :param count: How many wallpapers to generate. Negative values will generate all the wallpapers.
        :param extension: File extension (and format) of the generated wallpapers.
        :param logger: Logger to use.
        :param kwargs: Will be passed to the Wallpaper constructor.
        :return: Generator of the generated images.
        """
        kwargs.pop("color", None)
        kwargs.pop("output", None)

        if output_dir is not None:
            save = True
            output = Path(output_dir)
        else:
            save = False
            output = Path()

        hexes: Iterable[str] = color_hexes
        if count >= 0:
            hexes = sample(color_hexes, count)

        for hex_code in hexes:
            try:
                yield Wallpaper(
                    output=output.joinpath(
                        safe_path_name(f"{hex_to_color[hex_code]}_#{hex_code}.{extension.lstrip('.')}")
                    ),
                    color=hex_code,
                    logger=logger,
                    **kwargs,
                ).generate_image(save=save)
            except RuntimeError:
                pass
