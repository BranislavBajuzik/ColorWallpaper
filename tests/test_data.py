import PIL

from io import StringIO
from unittest.mock import patch

from color_wallpaper.data import font, hex_to_color, color_hexes, load_font, font_chars
from tests.TestBase import TestBase


f = False
t = True


class UniqueColors(TestBase):
    def test(self):
        self.assertTrue(len(hex_to_color) == len(color_hexes) == len(hex_to_color))


class Font(TestBase):
    def test_default(self):
        self.assertEqual(
            (
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
                (t, t, t, t, t, t, t, f),
            ),
            font("👌"),
        )

    def test_ok(self):
        self.assertEqual(
            (
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
            ),
            font(" "),
        )

        self.assertEqual(
            (
                (f, t, f, t, f, f),
                (f, t, f, t, f, f),
                (t, t, t, t, t, f),
                (f, t, f, t, f, f),
                (t, t, t, t, t, f),
                (f, t, f, t, f, f),
                (f, t, f, t, f, f),
                (f, f, f, f, f, f),
            ),
            font("#"),
        )

        self.assertEqual(
            (
                (f, t, t, t, f, f),
                (t, f, f, f, t, f),
                (t, f, f, t, t, f),
                (t, f, t, f, t, f),
                (t, t, f, f, t, f),
                (t, f, f, f, t, f),
                (f, t, t, t, f, f),
                (f, f, f, f, f, f),
            ),
            font("0"),
        )

        self.assertEqual(
            (
                (t, f, t, f),
                (t, f, t, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
                (f, f, f, f),
            ),
            font('"'),
        )

    def test_nok(self):
        with patch("sys.stderr", new=StringIO()):
            self.assertRaises(AssertionError, font, "")
            self.assertRaises(AssertionError, font, "12")

    @patch("sys.stderr", new=StringIO())
    def test_invalid_font_file(self):
        for size in ((8, 8), (len(font_chars), 7)):
            with patch("PIL.Image.open", new=lambda *_, **__: PIL.Image.new("RGBA", size)):
                self.assertRaises(AssertionError, load_font)
                self.assertRaises(AssertionError, load_font)
