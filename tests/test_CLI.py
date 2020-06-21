import pytest

from io import StringIO
from pathlib import Path
from unittest.mock import patch

from color_wallpaper.CLI import *
from tests.TestBase import *


class TestHelp:
    @pytest.mark.parametrize("cli", (["-h"], ["--help"]))
    def test(self, monkeypatch, cli):
        monkeypatch.setattr("sys.stdout", StringIO())

        with pytest.raises(SystemExit):
            get_options(cli)


# General Options
class TestOutput:
    def test_default(self):
        assert Path("out.png") == get_options([]).output

    @pytest.mark.parametrize(
        "cli,result",
        (
            (["-o", "picture"], Path("picture")),
            (["-o", "picture.png"], Path("picture.png")),
            (["--output", "picture"], Path("picture")),
            (["--output", "picture.png"], Path("picture.png")),
        ),
    )
    def test_valid(self, cli, result):
        assert result == get_options(cli).output


class TestYes:
    def test_default(self):
        assert not get_options([]).yes

    @pytest.mark.parametrize("cli", (["-y"], ["--yes"]))
    def test_valid(self, cli):
        assert get_options(cli).yes


# Color Options
class TestColor:
    def test_default(self):
        assert "random", get_options([]).color

    @pytest.mark.parametrize(
        "cli",
        (
            ["-c", "  Black"],
            ["--color", "255  ,   216,0"],
            ["-c", " F00"],
            ["--color", "#F00 "],
            ["-c", "  FF0000"],
            ["--color", "#FF0000  "],
        ),
    )
    def test_valid(self, cli):
        assert cli[-1] == get_options(cli).color


class TestColor2:
    def test_default(self):
        assert "inverted" == get_options([]).color2

    @pytest.mark.parametrize(
        "cli",
        (
            ["-c2", "  Black"],
            ["--color2", "255  ,   216,0"],
            ["-c2", " F00"],
            ["--color2", "#F00 "],
            ["-c2", "  FF0000"],
            ["--color2", "#FF0000  "],
        ),
    )
    def test_valid(self, cli):
        assert cli[-1] == get_options(cli).color2


class TestDisplay:
    def test_default(self):
        assert get_options([]).display is None

    @pytest.mark.parametrize("cli", (["-d", ""], ["-d", "Custom"], ["--display", "Custom"]))
    def test(self, cli):
        assert cli[-1] == get_options(cli).display


class MinContrast(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(1, options.min_contrast)

    def test_valid(self):
        args = (
            (1, ["-c", "black", "--min-contrast", "1"]),
            (21, ["-c", "black", "--min-contrast", "21"]),
            (4.5, ["-c", "black", "--min-contrast", "4.5"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).min_contrast)

    def test_invalid(self):
        args = (["--min-contrast", "0.9"], ["--min-contrast", "21.1"], ["--min-contrast", "a"], ["--min-contrast", ""])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class OverlayColor(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(None, options.overlay_color)

    def test_valid(self):
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

    def test_invalid(self):
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

    def test_valid(self):
        args = (
            (1, ["--overlay-contrast", "1"]),
            (21, ["--overlay-contrast", "21"]),
            (4.5, ["--overlay-contrast", "4.5"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).overlay_contrast)

    def test_invalid(self):
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

    def test_valid(self):
        args = (
            ((690, 420), ["-r", "690x420"]),
            ((690, 420), ["-r", "690:420"]),
            ((690, 420), ["--resolution", "690x420"]),
            ((690, 420), ["--resolution", "690:420"]),
            ((150, 150), ["--resolution", "150:150"]),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).resolution)

    def test_invalid(self):
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

    def test_valid(self):
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

    def test_invalid(self):
        args = (["-s", "a"], ["-s", "nan"], ["-s", ""])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Formats(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(["empty", "HEX", "rgb"], options.formats)

    def test_valid(self):
        args = (
            ([], ["-f"]),
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

    def test_invalid(self):
        args = (["-f", "r g b"], ["-f", "heX"], ["-f", "#Hex"], ["-f", "a"], ["-f", ""])

        with patch("sys.stderr", new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)
