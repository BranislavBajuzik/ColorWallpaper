import pytest

from typing import Tuple
from color_wallpaper.Color import Color


@pytest.fixture
def assert_color_equal():
    """Returns Color equality check helper"""

    def inner(color: Color, rgb: Tuple[int, int, int], name: str = None) -> None:
        """Asserts that :param color: has its attributes equal to the :param rgb: and :param name:

        :param color: Color to check
        :param rgb: RGB tuple to check against
        :param name: Name string to check against
        """
        assert rgb == color.rgb

        if name is not None:
            assert name == color.name

    return inner
