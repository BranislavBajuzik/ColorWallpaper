from io import StringIO
from unittest.mock import patch

from src.ColorWallpaper import *
from tests.TestBase import *


class InitColor(TestBase):
    def test_default(self):
        with override_cli():
            self.assertIsColorInstance(Wallpaper().color)
            self.assertNotEqual(Wallpaper().color, Wallpaper().color)

    def test_ok(self):
        args = (
            (["-c", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--color", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["-c", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--color", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["-c", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--color", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        )

        for cli, rgb, name in args:
            with override_cli(cli):
                self.assertColorEqual(Wallpaper().color, rgb, name)

    @override_color_random([(0x7F, 0x7F, 0x7F), (0x00, 0x00, 0x00)])
    def test_ok_random(self):
        args = (["-c", "RandOm"], ["--color", "RandOm"])
        colors = (((0x7F, 0x7F, 0x7F),), ((0x00, 0x00, 0x00), "Black"))

        for cli, color in zip(args, colors):
            with override_cli(cli):
                pape = Wallpaper()

                self.assertIsColorInstance(pape.color)
                self.assertColorEqual(pape.color, *color)

    def test_nok(self):
        args = (
            ["-c", "Custom"],
            ["--color", "Custom"],
            ["-c", ""],
            ["--color", ""],
            ["-c", "1234"],
            ["--color", "#12"],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                with override_cli(cli):
                    self.assertRaises(ValueError, Wallpaper)


class InitColor2(TestBase):
    def test_default(self):
        pape = Wallpaper()

        self.assertEqual(pape.color2, pape.color.inverted(pape.min_contrast))

        self.assertColorEqual(Wallpaper(color="black").color2, (0xFF, 0xFF, 0xFF), "White")

    def test_ok(self):
        args = (
            (["-c2", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--color2", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["-c2", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--color2", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["-c2", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--color2", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        )

        for cli, rgb, name in args:
            with override_cli(cli):
                self.assertColorEqual(Wallpaper().color2, rgb, name)

    def test_nok(self):
        args = (
            ["-c2", "Custom"],
            ["--color2", "Custom"],
            ["-c2", ""],
            ["--color2", ""],
            ["-c2", "1234"],
            ["--color2", "#12"],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                with override_cli(cli):
                    self.assertRaises(ValueError, Wallpaper)

    def test_ok_inverted(self):
        args = (
            (["-c", "white", "-c2", "inverted"], (0x00, 0x00, 0x00), "Black"),
            (["-c", "black", "-c2", "inverted"], (0xFF, 0xFF, 0xFF), "White"),
            (["-c", "red", "-c2", "inverted"], (0x00, 0xFF, 0xFF), "Cyan"),
            (["-c", "cyan", "-c2", "inverted"], (0xFF, 0x00, 0x00), "Red"),
        )

        for cli, rgb, name in args:
            with override_cli(cli):
                self.assertColorEqual(Wallpaper().color2, rgb, name)

    def test_impossible_inverted(self):
        with patch("sys.stderr", new=StringIO()), override_cli(
            ["-c", "7F7F7F", "-c2", "inverted", "--min-contrast", "21"]
        ):
            self.assertRaises(RuntimeError, Wallpaper)

    @override_color_random([(0x7F, 0x7F, 0x7F), (0x00, 0x00, 0x00)])
    def test_random_inverted(self):
        with override_cli(["-c2", "inverted", "--min-contrast", "21"]):
            self.assertColorEqual(Wallpaper().color2, (0xFF, 0xFF, 0xFF), "White")


class InitOverlayColor(TestBase):
    def test_nok_contrast(self):
        args = (
            ["-c", "7F7F7F", "--overlay-color", "7F7F7F", "--overlay-contrast", "6"],
            ["-c", "000001", "--overlay-color", "white", "--overlay-contrast", "21"],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                with override_cli(cli):
                    self.assertRaises(RuntimeError, Wallpaper)

    @override_color_random([(0x7F, 0x7F, 0x7F), (0x00, 0x00, 0x00)])
    def test_random_regenerate(self):
        with override_cli(["--overlay-color", "7F7F7F", "--overlay-contrast", "3"]):
            pape = Wallpaper()

            self.assertColorEqual(pape.color, (0x00, 0x00, 0x00), "Black")
            self.assertColorEqual(pape.color2, (0xFF, 0xFF, 0xFF), "White")
            self.assertColorEqual(pape.overlay_color, (0x7F, 0x7F, 0x7F))
