from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.CLI import *
from tests.TestBase import *


class Help(TestBase):
    def test(self):
        args = (["-h"], ["--help"])

        with patch("sys.stdout", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


# General Options
class Output(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(Path("out.png"), options.output)

    def test_ok(self):
        args = (
            (Path("picture"), ["-o", "picture"]),
            (Path("picture.png"), ["-o", "picture.png"]),
            (Path("picture"), ["--output", "picture"]),
            (Path("picture.png"), ["--output", "picture.png"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).output)


class Yes(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(False, options.yes)

    def test_ok(self):
        args = ((True, ["-y"]), (True, ["--yes"]))

        for result, cli in args:
            self.assertEqual(result, get_options(cli).yes)


# Color Options
class Color(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(options.color, "random")

    def test_ok(self):
        args = (
            ["-c", "  Black"],
            ["--color", "255  ,   216,0"],
            ["-c", " F00"],
            ["--color", "#F00 "],
            ["-c", "  FF0000"],
            ["--color", "#FF0000  "],
        )

        for cli in args:
            self.assertEqual(get_options(cli).color, cli[-1])


class Color2(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(options.color2, "inverted")

    def test_ok(self):
        args = (
            ["-c2", "  Black"],
            ["--color2", "255  ,   216,0"],
            ["-c2", " F00"],
            ["--color2", "#F00 "],
            ["-c2", "  FF0000"],
            ["--color2", "#FF0000  "],
        )

        for cli in args:
            self.assertEqual(get_options(cli).color2, cli[-1])


class Display(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(None, options.display)

    def test(self):
        args = (("", ["-d", ""]), ("Custom", ["-d", "Custom"]), ("Custom", ["--display", "Custom"]))

        for result, cli in args:
            self.assertEqual(result, get_options(cli).display)


class MinContrast(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(1, options.min_contrast)

    def test_ok(self):
        args = (
            (1, ["-c", "black", "--min-contrast", "1"]),
            (21, ["-c", "black", "--min-contrast", "21"]),
            (4.5, ["-c", "black", "--min-contrast", "4.5"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).min_contrast)

    def test_nok(self):
        args = (["--min-contrast", "0.9"], ["--min-contrast", "21.1"], ["--min-contrast", "a"], ["--min-contrast", ""])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class OverlayColor(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(None, options.overlay_color)

    def test_ok(self):
        args = (
            (["--overlay-color", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--overlay-color", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["--overlay-color", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        )

        for cli, rgb, name in args:
            self.assertColorEqual(get_options(cli).overlay_color, rgb, name)

    def test_nok(self):
        args = (
            ["--overlay-color", "Custom"],
            ["--overlay-color", ""],
            ["--overlay-color", "1234"],
            ["--overlay-color", "#12"],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class OverlayContrast(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(1, options.overlay_contrast)

    def test_ok(self):
        args = (
            (1, ["--overlay-contrast", "1"]),
            (21, ["--overlay-contrast", "21"]),
            (4.5, ["--overlay-contrast", "4.5"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).overlay_contrast)

    def test_nok(self):
        args = (
            ["--overlay-contrast", "0.9"],
            ["--overlay-contrast", "21.1"],
            ["--overlay-contrast", "a"],
            ["--overlay-contrast", ""],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


# Display options
class Resolution(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual((1920, 1080), options.resolution)

    def test_ok(self):
        args = (
            ((690, 420), ["-r", "690x420"]),
            ((690, 420), ["-r", "690:420"]),
            ((690, 420), ["--resolution", "690x420"]),
            ((690, 420), ["--resolution", "690:420"]),
            ((150, 150), ["--resolution", "150:150"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).resolution)

    def test_nok(self):
        args = (
            ["-r", "149:420"],
            ["-r", "690:149"],
            ["-r", "149:149"],
            ["-r", "690 420"],
            ["-r", "420:690a"],
            ["-r", "420a:690"],
            ["-r", "420::690"],
            ["-r", "420xx690"],
            ["-r", "420:x690"],
            ["-r", "420x:690"],
            ["-r", ""],
        )

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Scale(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(3, options.scale)

    def test_ok(self):
        args = (
            (1, ["-s", "1"]),
            (420, ["-s", "420"]),
            (1, ["--scale", "1"]),
            (420, ["--scale", "420"]),
            (1, ["--scale", "0"]),
            (1, ["--scale", "0.9"]),
            (1, ["--scale", "1.5"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).scale)

    def test_nok(self):
        args = (["-s", "a"], ["-s", "nan"], ["-s", ""])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Formats(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(["empty", "HEX", "rgb"], options.formats)

    def test_ok(self):
        args = (
            (["empty"], ["-f", "empty"]),
            (["hex"], ["-f", "hex"]),
            (["#hex"], ["-f", "#hex"]),
            (["rgb"], ["-f", "rgb"]),
            (["hsv"], ["-f", "hsv"]),
            (["hsl"], ["-f", "hsl"]),
            (["cmyk"], ["-f", "cmyk"]),
            (["empty"], ["--formats", "empty"]),
            (["hex"], ["--formats", "hex"]),
            (["#hex"], ["--formats", "#hex"]),
            (["rgb"], ["--formats", "rgb"]),
            (["hsv"], ["--formats", "hsv"]),
            (["hsl"], ["--formats", "hsl"]),
            (["cmyk"], ["--formats", "cmyk"]),
            (
                ["empty", "hex", "#hex", "rgb", "hsv", "hsl", "cmyk"],
                ["--formats", "eMptY", "hex", "#hex", "Rgb", "hSv", "Hsl", "cMyK"],
            ),
            (["rgb", "rgb", "rgb", "rgb", "rgb", "rgb"], ["--formats", "rgb", "rgB", "RGb", "rgb", "rgb", "rgb"]),
        )

        for result, cli in args:
            self.assertEqual(sorted(result), sorted(get_options(cli).formats))

    def test_nok(self):
        args = (["-f", "r g b"], ["-f", "heX"], ["-f", "#Hex"], ["-f", "a"], ["-f", ""], ["-f"])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)
