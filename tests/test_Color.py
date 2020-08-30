import pytest

from color_wallpaper.color import *


class TestCreate:
    @pytest.mark.parametrize(
        "rgb, name",
        (
            ((0x00, 0x00, 0x00), "Black"),
            ((0xFF, 0x00, 0x00), "Red"),
            ((0xFF, 0xFF, 0xFF), "White"),
            ((0x12, 0x34, 0x56), "Anonymous"),
        ),
    )
    def test_valid(self, color_equal, rgb, name):
        assert color_equal(Color(rgb), rgb, name)

    def test_custom_name(self, color_equal):
        assert color_equal(Color((0x12, 0x34, 0x56), "Custom"), (0x12, 0x34, 0x56), "Custom")

    @pytest.mark.parametrize("rgb", ((0x00, 0x00), (0x00, 0x00, 0x00, 0x00), (0x1FF, 0x00, 0x00), (-0x01, 0x00, 0x00)))
    def test_invalid(self, rgb):
        with pytest.raises(ValueError):
            Color(rgb)


class TestStrRepr:
    def test(self):
        black = Color((0x00, 0x00, 0x00), "Black")

        assert str(black) == repr(black)
        assert "Color(rgb=(0, 0, 0), name='Black')" == str(black)


class TestHex:
    @pytest.mark.parametrize(
        "rgb, result",
        (
            ((0x00, 0x00, 0x00), "000000"),
            ((0xFF, 0x00, 0x00), "ff0000"),
            ((0xAB, 0xCD, 0xEF), "abcdef"),
            ((0xFF, 0xFF, 0xFF), "ffffff"),
        ),
    )
    def test_lower(self, rgb, result):
        assert result == Color(rgb).hex

    @pytest.mark.parametrize(
        "rgb, result",
        (
            ((0x00, 0x00, 0x00), "000000"),
            ((0xFF, 0x00, 0x00), "FF0000"),
            ((0xAB, 0xCD, 0xEF), "ABCDEF"),
            ((0xFF, 0xFF, 0xFF), "FFFFFF"),
        ),
    )
    def test_upper(self, rgb, result):
        assert result == Color(rgb).HEX


class TestHSV:
    @pytest.mark.parametrize(
        "rgb, result",
        (
            ((0x00, 0x00, 0x00), (0, 0, 0)),
            ((0xFF, 0x00, 0x00), (0, 100, 100)),
            ((0x12, 0x34, 0x56), (210, 79, 33)),
            ((0xAB, 0xCD, 0xEF), (210, 28, 93)),
        ),
    )
    def test(self, rgb, result):
        assert result == Color(rgb).hsv


class TestHSL:
    @pytest.mark.parametrize(
        "rgb, result",
        (
            ((0x00, 0x00, 0x00), (0, 0, 0)),
            ((0xFF, 0x00, 0x00), (0, 100, 50)),
            ((0x12, 0x34, 0x56), (210, 65, 20)),
            ((0xAB, 0xCD, 0xEF), (210, 68, 80)),
        ),
    )
    def test(self, rgb, result):
        assert result == Color(rgb).hsl


class TestCMYK:
    @pytest.mark.parametrize(
        "rgb, result",
        (
            ((0x00, 0x00, 0x00), (0, 0, 0, 100)),
            ((0xFF, 0x00, 0x00), (0, 100, 100, 0)),
            ((0xAB, 0xCD, 0xEF), (28, 14, 0, 6)),
            ((0xAB, 0xCD, 0xEF), (28, 14, 0, 6)),
        ),
    )
    def test(self, rgb, result):
        assert result == Color(rgb).cmyk


class TestLuminance:
    @pytest.mark.parametrize(
        "rgb, luminance",
        (
            ((0x00, 0x00, 0x00), 0.0),
            ((0xFF, 0xFF, 0xFF), 1.0),
            ((0xFF, 0x00, 0x00), 0.2126),
            ((0x00, 0xFF, 0x00), 0.7151),
            ((0x00, 0x00, 0xFF), 0.0722),
        ),
    )
    def test(self, rgb, luminance):
        assert luminance == int(Color(rgb).luminance * 10_000) / 10_000


class TestTrueDiv:
    @pytest.mark.parametrize(
        "rgb1, rgb2, result",
        (
            ((0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF), 21.0),
            ((0x00, 0x00, 0xFF), (0xFF, 0xFF, 0xFF), 8.59),
            ((0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), 2.14),
            ((0x00, 0x00, 0x00), (0x00, 0x00, 0x00), 1.0),
            ((0xFF, 0xFF, 0xFF), (0xFF, 0xFF, 0xFF), 1.0),
        ),
    )
    def test(self, rgb1, rgb2, result):
        color1, color2 = Color(rgb1), Color(rgb2)

        assert color1 / color2 == color2 / color1
        assert result == int((color1 / color2) * 100) / 100


class TestDiv:
    @pytest.mark.parametrize(
        "rgb1, rgb2, result",
        (
            ((0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF), 21),
            ((0x00, 0x00, 0xFF), (0xFF, 0xFF, 0xFF), 8),
            ((0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), 2),
            ((0x00, 0x00, 0x00), (0x00, 0x00, 0x00), 1),
            ((0xFF, 0xFF, 0xFF), (0xFF, 0xFF, 0xFF), 1),
        ),
    )
    def test(self, rgb1, rgb2, result):
        color1, color2 = Color(rgb1), Color(rgb2)

        assert color1 // color2 == color2 // color1
        assert result == color1 // color2


class TestInverted:
    @pytest.mark.parametrize(
        "rgb, rgb_inverted, name",
        (
            ((0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF), "White"),
            ((0xFF, 0xFF, 0xFF), (0x00, 0x00, 0x00), "Black"),
            ((0x00, 0xFF, 0xFF), (0xFF, 0x00, 0x00), "Red"),
            ((0xFF, 0x00, 0x00), (0x00, 0xFF, 0xFF), "Cyan"),
        ),
    )
    def test_valid(self, color_equal, rgb, rgb_inverted, name):
        assert color_equal(Color(rgb).inverted(), rgb_inverted, name)

    @pytest.mark.parametrize(
        "rgb, min_contrast, rgb_inverted",
        (((0x50, 0x50, 0x50), 4, (0xB7, 0xB7, 0xB7)), ((0xB7, 0xB7, 0xB7), 6, (0x35, 0x35, 0x35))),
    )
    def test_valid_calculate(self, color_equal, rgb, min_contrast, rgb_inverted):
        assert color_equal(Color(rgb).inverted(min_contrast), rgb_inverted)

    @pytest.mark.parametrize("min_contrast", (1, 5, 21))
    def test_valid_contrast(self, min_contrast):
        Color((0, 0, 0)).inverted(min_contrast)

    @pytest.mark.parametrize("min_contrast", (-5, 0, 0.9, 21.1))
    def test_invalid_contrast(self, min_contrast):
        with pytest.raises(ValueError):
            Color((0, 0, 0)).inverted(min_contrast)

    @pytest.mark.parametrize("rgb, min_contrast", (((0x7F, 0x7F, 0x7F), 10), ((0x00, 0xFF, 0xFF), 21)))
    def test_impossible(self, rgb, min_contrast):
        with pytest.raises(RuntimeError):
            Color(rgb).inverted(min_contrast)


class TestRandom:
    def test(self):
        from color_wallpaper.data import hex_to_color

        color = Color.random()

        assert color.name == hex_to_color[color.hex]


class TestFromHSL:
    @pytest.mark.parametrize(
        "hsl, rgb, name",
        (
            ((0, 0, 0), (0x00, 0x00, 0x00), "Black"),
            ((0, 100, 50), (0xFF, 0x00, 0x00), "Red"),
            ((210, 68, 80.5), (0xAB, 0xCD, 0xEF), "Anonymous"),
        ),
    )
    def test_valid(self, color_equal, hsl, rgb, name):
        assert color_equal(Color.from_hsl(*hsl), rgb, name)

    @pytest.mark.parametrize("hsl", ((-1, 0, 0), (0, -1, 0), (0, 0, -1), (361, 0, 0), (0, 361, 0), (0, 0, 361)))
    def test_invalid(self, hsl):
        with pytest.raises(ValueError):
            Color.from_hsl(*hsl)


class TestFromStr:
    @pytest.mark.parametrize(
        "string, rgb, name",
        (
            ("Black", (0x00, 0x00, 0x00), "Black"),
            ("reD", (0xFF, 0x00, 0x00), "Red"),
            ("School Bus Yellow", (0xFF, 0xD8, 0x00), "School Bus Yellow"),
        ),
    )
    def test_valid_name(self, color_equal, string, rgb, name):
        assert color_equal(Color.from_str(string), rgb, name)

    @pytest.mark.parametrize("name", ("", "random", "Not a color", "Anonymous"))
    def test_invalid_name(self, name):
        with pytest.raises(ValueError):
            Color.from_str(name)

    @pytest.mark.parametrize(
        "string, rgb, name",
        (
            ("00, 0, 0 ", (0x00, 0x00, 0x00), "Black"),
            ("255, 0, 0", (0xFF, 0x00, 0x00), "Red"),
            ("255,216,0", (0xFF, 0xD8, 0x00), "School Bus Yellow"),
        ),
    )
    def test_valid_rgb(self, color_equal, string, rgb, name):
        assert color_equal(Color.from_str(string), rgb, name)

    @pytest.mark.parametrize("string", ("-1, 0, 0", "0, -1, 0", "0, 0, -1", "256, 0, 0", "0, 256, 0", "0, 0, 256"))
    def test_invalid_rgb(self, string):
        with pytest.raises(ValueError):
            Color.from_str(string)

    @pytest.mark.parametrize(
        "string, rgb, name",
        (
            ("000000", (0x00, 0x00, 0x00), "Black"),
            ("#000000", (0x00, 0x00, 0x00), "Black"),
            ("000", (0x00, 0x00, 0x00), "Black"),
            ("#000", (0x00, 0x00, 0x00), "Black"),
            ("F00", (0xFF, 0x00, 0x00), "Red"),
            ("#F00", (0xFF, 0x00, 0x00), "Red"),
            ("FF0000", (0xFF, 0x00, 0x00), "Red"),
            ("#FF0000", (0xFF, 0x00, 0x00), "Red"),
            ("FFD800", (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            ("#FFD800", (0xFF, 0xD8, 0x00), "School Bus Yellow"),
        ),
    )
    def test_valid_hex(self, color_equal, string, rgb, name):
        assert color_equal(Color.from_str(string), rgb, name)

    @pytest.mark.parametrize("string", ("1", "11", "hhh", "1111", "11111", "hhhhhh", "1111111", "##000000"))
    def test_invalid_hex(self, string):
        with pytest.raises(ValueError):
            Color.from_str(string)
