import pytest

from argparse import ArgumentParser
from color_wallpaper.Color import Color
from typing import Tuple, Sequence


@pytest.fixture
def color_equal():
    """Returns Color equality check helper"""

    def is_color_equal(color: Color, rgb: Tuple[int, int, int], name: str = None) -> bool:
        """Checks that :param color: has its attributes equal to the :param rgb: and :param name:

        :param color: Color to check
        :param rgb: RGB tuple to check against
        :param name: Name string to check against
        :return: True if the color matches
        """
        ret = rgb == color.rgb

        if name is not None:
            ret &= name == color.name

        return ret

    return is_color_equal


@pytest.fixture
def set_cli(monkeypatch):
    """Returns CLI override helper"""

    original_cli = ArgumentParser.parse_args

    def override_cli(cli: Sequence[str] = ()) -> None:
        """CLI setter

        :param cli: CLI args to set
        """
        monkeypatch.setattr(ArgumentParser, "parse_args", lambda self, _: original_cli(self, cli))

    return override_cli


@pytest.fixture
def set_color_random(monkeypatch):
    """Returns Color.random override helper"""

    def override_random(*colors: Tuple[int, int, int]) -> None:
        """Color.random setter

        :param colors: "Random" colors
        """
        colors_it = reversed(colors)
        monkeypatch.setattr(Color, "random", lambda: Color(next(colors_it)))

    return override_random
