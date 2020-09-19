import logging
from pathlib import Path

import pytest

from color_wallpaper.cli import *


class TestHelp:
    @pytest.mark.parametrize("cli", (["-h"], ["--help"]))
    def test(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


class TestLogLevel:
    def test_default(self):
        assert logging.INFO == get_options([]).log_level

    @pytest.mark.parametrize(
        "cli, level",
        (
            (["--log-level", "CriTiCAl"], logging.CRITICAL),
            (["--log-level", "fatal"], logging.FATAL),
            (["--log-level", "ERROR"], logging.ERROR),
            (["--log-level", "WARN"], logging.WARN),
            (["--log-level", "WARNING"], logging.WARNING),
            (["--log-level", "InFO"], logging.INFO),
            (["--log-level", "DeBUG"], logging.DEBUG),
            (["--log-level", "NOTSET"], logging.NOTSET),
        ),
    )
    def test_vlaid(self, cli, level):
        assert level == get_options(cli).log_level

    @pytest.mark.parametrize(
        "cli",
        (
            ["--log-level", ""],
            ["--log-level", "random"],
            ["--log-level", "123"],
            ["--log-level", "10"],
        ),
    )
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


# General Options
class TestOutput:
    def test_default(self):
        assert Path("out.png") == get_options([]).output

    @pytest.mark.parametrize(
        "cli, result",
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


class TestMinContrast:
    def test_default(self):
        assert 1 == get_options([]).min_contrast

    @pytest.mark.parametrize(
        "cli, result",
        (
            (["-c", "black", "--min-contrast", "1"], 1),
            (["-c", "black", "--min-contrast", "21"], 21),
            (["-c", "black", "--min-contrast", "4.5"], 4.5),
        ),
    )
    def test_valid(self, cli, result):
        assert result == get_options(cli).min_contrast

    @pytest.mark.parametrize(
        "cli",
        (
            ["--min-contrast", "-5"],
            ["--min-contrast", "0.9"],
            ["--min-contrast", "21.1"],
            ["--min-contrast", "a"],
            ["--min-contrast", ""],
        ),
    )
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


class TestOverlayColor:
    def test_default(self):
        assert get_options([]).overlay_color is None

    @pytest.mark.parametrize(
        "cli, rgb, name",
        (
            (["--overlay-color", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--overlay-color", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["--overlay-color", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--overlay-color", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        ),
    )
    def test_valid(self, color_equal, cli, rgb, name):
        assert color_equal(get_options(cli).overlay_color, rgb, name)

    @pytest.mark.parametrize(
        "cli",
        (
            ["--overlay-color", "Custom"],
            ["--overlay-color", ""],
            ["--overlay-color", "1234"],
            ["--overlay-color", "#12"],
        ),
    )
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


class TestOverlayContrast:
    def test_default(self):
        assert 1 == get_options([]).overlay_contrast

    @pytest.mark.parametrize(
        "cli, result",
        (
            (["--overlay-contrast", "1"], 1),
            (["--overlay-contrast", "1."], 1),
            (["--overlay-contrast", "21"], 21),
            (["--overlay-contrast", "6.9"], 6.9),
        ),
    )
    def test_valid(self, cli, result):
        assert result == get_options(cli).overlay_contrast

    @pytest.mark.parametrize(
        "cli",
        (
            ["--overlay-contrast", "0.9"],
            ["--overlay-contrast", "21.1"],
            ["--overlay-contrast", "a"],
            ["--overlay-contrast", ""],
            ["--overlay-contrast", "nan"],
        ),
    )
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


# Display options
class TestResolution:
    def test_default(self):
        assert (1920, 1080) == get_options([]).resolution

    @pytest.mark.parametrize(
        "cli, result",
        (
            (["-r", "690x420"], (690, 420)),
            (["-r", "690:420"], (690, 420)),
            (["--resolution", "690x420"], (690, 420)),
            (["--resolution", "690:420"], (690, 420)),
            (["--resolution", "150:150"], (150, 150)),
        ),
    )
    def test_valid(self, cli, result):
        assert result == get_options(cli).resolution

    @pytest.mark.parametrize(
        "cli",
        (
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
        ),
    )
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


class TestScale:
    def test_default(self):
        assert 3 == get_options([]).scale

    @pytest.mark.parametrize(
        "cli, result",
        (
            (["-s", "1"], 1),
            (["-s", "420"], 420),
            (["--scale", "1"], 1),
            (["--scale", "420"], 420),
            (["--scale", "0"], 1),
            (["--scale", "-1"], 1),
            (["--scale", "-0.1"], 1),
            (["--scale", "0.9"], 1),
            (["--scale", "1.5"], 1),
        ),
    )
    def test_valid(self, cli, result):
        assert result == get_options(cli).scale

    @pytest.mark.parametrize("cli", (["-s", "a"], ["-s", "nan"], ["-s", ""]))
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)


class TestFormats:
    def test_default(self):
        assert ["empty", "HEX", "rgb"] == get_options([]).formats

    @pytest.mark.parametrize(
        "cli, result",
        (
            (["-f"], []),
            (["-f", "empty"], ["empty"]),
            (["-f", "hex"], ["hex"]),
            (["-f", "#hex"], ["#hex"]),
            (["-f", "rgb"], ["rgb"]),
            (["-f", "hsv"], ["hsv"]),
            (["-f", "hsl"], ["hsl"]),
            (["-f", "cmyk"], ["cmyk"]),
            (["--formats", "empty"], ["empty"]),
            (["--formats", "hex"], ["hex"]),
            (["--formats", "#hex"], ["#hex"]),
            (["--formats", "rgb"], ["rgb"]),
            (["--formats", "hsv"], ["hsv"]),
            (["--formats", "hsl"], ["hsl"]),
            (["--formats", "cmyk"], ["cmyk"]),
            (
                ["--formats", "eMptY", "hex", "#hex", "Rgb", "hSv", "Hsl", "cMyK"],
                ["empty", "hex", "#hex", "rgb", "hsv", "hsl", "cmyk"],
            ),
            (["--formats", "rgb", "rgB", "RGb", "rgb", "rgb", "rgb"], ["rgb", "rgb", "rgb", "rgb", "rgb", "rgb"]),
        ),
    )
    def test_valid(self, cli, result):
        assert sorted(result) == sorted(get_options(cli).formats)

    @pytest.mark.parametrize("cli", (["-f", "r g b"], ["-f", "heX"], ["-f", "#Hex"], ["-f", "a"], ["-f", ""]))
    def test_invalid(self, cli):
        with pytest.raises(SystemExit):
            get_options(cli)
