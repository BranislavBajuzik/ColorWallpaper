import logging

import pytest

from color_wallpaper.color import Color
from color_wallpaper.ColorWallpaper import *


class TestInitColor:
    def test_default(self, set_cli):
        set_cli()

        assert isinstance(Wallpaper().color, Color)
        assert Wallpaper().color != Wallpaper().color

    @pytest.mark.parametrize(
        "cli, rgb, name",
        (
            (["-c", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--color", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["-c", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--color", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["-c", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--color", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        ),
    )
    def test_ok(self, set_cli, color_equal, cli, rgb, name):
        set_cli(cli)

        assert color_equal(Wallpaper().color, rgb, name)

    @pytest.mark.parametrize(
        "cli, color",
        ((["-c", "RandOm"], ((0x7F, 0x7F, 0x7F),)), (["--color", "RandOm"], ((0x00, 0x00, 0x00), "Black"))),
    )
    def test_ok_random(self, set_color_random, set_cli, color_equal, cli, color):
        set_color_random(color[0])
        set_cli(cli)

        pape = Wallpaper()

        assert isinstance(pape.color, Color)
        assert color_equal(pape.color, *color)

    @pytest.mark.parametrize(
        "cli",
        (["-c", "Custom"], ["--color", "Custom"], ["-c", ""], ["--color", ""], ["-c", "1234"], ["--color", "#12"]),
    )
    def test_nok(self, set_cli, cli):
        set_cli(cli)

        with pytest.raises(ValueError):
            Wallpaper()


class TestInitColor2:
    def test_default(self, set_cli, color_equal):
        set_cli()
        pape = Wallpaper()

        assert pape.color2 == pape.color.inverted(pape.min_contrast)

        set_cli(["--color", "black"])
        assert color_equal(Wallpaper().color2, (0xFF, 0xFF, 0xFF), "White")

    @pytest.mark.parametrize(
        "cli, rgb, name",
        (
            (["-c2", "  Black"], (0x00, 0x00, 0x00), "Black"),
            (["--color2", "255  ,   216,0"], (0xFF, 0xD8, 0x00), "School Bus Yellow"),
            (["-c2", " F00"], (0xFF, 0x00, 0x00), "Red"),
            (["--color2", "#F00 "], (0xFF, 0x00, 0x00), "Red"),
            (["-c2", "  FF0000"], (0xFF, 0x00, 0x00), "Red"),
            (["--color2", "#FF0000  "], (0xFF, 0x00, 0x00), "Red"),
        ),
    )
    def test_ok(self, set_cli, color_equal, cli, rgb, name):
        set_cli(cli)

        assert color_equal(Wallpaper().color2, rgb, name)

    @pytest.mark.parametrize(
        "cli",
        (
            ["-c2", "Custom"],
            ["--color2", "Custom"],
            ["-c2", ""],
            ["--color2", ""],
            ["-c2", "1234"],
            ["--color2", "#12"],
        ),
    )
    def test_nok(self, set_cli, cli):
        set_cli(cli)

        with pytest.raises(ValueError):
            Wallpaper()

    @pytest.mark.parametrize(
        "cli, rgb, name",
        (
            (["-c", "white", "-c2", "inverted"], (0x00, 0x00, 0x00), "Black"),
            (["-c", "black", "-c2", "inverted"], (0xFF, 0xFF, 0xFF), "White"),
            (["-c", "red", "-c2", "inverted"], (0x00, 0xFF, 0xFF), "Cyan"),
            (["-c", "cyan", "-c2", "inverted"], (0xFF, 0x00, 0x00), "Red"),
        ),
    )
    def test_ok_inverted(self, set_cli, color_equal, cli, rgb, name):
        set_cli(cli)

        assert color_equal(Wallpaper().color2, rgb, name)

    def test_impossible_inverted(self, set_cli):
        set_cli(["-c", "7F7F7F", "-c2", "inverted", "--min-contrast", "21"])

        with pytest.raises(RuntimeError):
            Wallpaper()

    def test_random_inverted(self, set_color_random, set_cli, color_equal):
        set_color_random((0x7F, 0x7F, 0x7F), (0x00, 0x00, 0x00))
        set_cli(["-c2", "inverted", "--min-contrast", "21"])

        assert color_equal(Wallpaper().color2, (0xFF, 0xFF, 0xFF), "White")


class TestInitOverlayColor:
    @pytest.mark.parametrize(
        "cli",
        (
            ["-c", "7F7F7F", "--overlay-color", "7F7F7F", "--overlay-contrast", "6"],
            ["-c", "000001", "--overlay-color", "white", "--overlay-contrast", "21"],
        ),
    )
    def test_nok_contrast(self, set_cli, cli):
        set_cli(cli)

        with pytest.raises(RuntimeError):
            Wallpaper()

    def test_random_regenerate(self, set_color_random, set_cli, color_equal):
        set_color_random((0x7F, 0x7F, 0x7F), (0x00, 0x00, 0x00))
        set_cli(["--overlay-color", "7F7F7F", "--overlay-contrast", "3"])

        pape = Wallpaper()

        assert color_equal(pape.color, (0x00, 0x00, 0x00), "Black")
        assert color_equal(pape.color2, (0xFF, 0xFF, 0xFF), "White")
        assert color_equal(pape.overlay_color, (0x7F, 0x7F, 0x7F))


class TestLogging:
    def test_default(self, set_cli):
        set_cli()

        assert Wallpaper().logger.level == logging.INFO

    def test_disabled(self, set_cli):
        set_cli(["--log-level", "NOTSET"])

        assert Wallpaper().logger.level == logging.CRITICAL
