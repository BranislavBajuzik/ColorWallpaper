import pytest

from color_wallpaper.data import font, hex_to_color, color_hexes, load_font, font_chars


f = False
t = True


def test_unique_colors():
    assert len(hex_to_color) == len(color_hexes) == len(hex_to_color)


def test_font_unknown():
    assert font("👌") == (
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
        (t, t, t, t, t, t, t, f),
    )


def test_font_valid():
    assert font(" ") == (
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
    )

    assert font("#") == (
        (f, t, f, t, f, f),
        (f, t, f, t, f, f),
        (t, t, t, t, t, f),
        (f, t, f, t, f, f),
        (t, t, t, t, t, f),
        (f, t, f, t, f, f),
        (f, t, f, t, f, f),
        (f, f, f, f, f, f),
    )

    assert font("0") == (
        (f, t, t, t, f, f),
        (t, f, f, f, t, f),
        (t, f, f, t, t, f),
        (t, f, t, f, t, f),
        (t, t, f, f, t, f),
        (t, f, f, f, t, f),
        (f, t, t, t, f, f),
        (f, f, f, f, f, f),
    )

    assert font('"') == (
        (t, f, t, f),
        (t, f, t, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
        (f, f, f, f),
    )


@pytest.mark.parametrize("string", ("", "12"))
def test_font_invalid(string):
    with pytest.raises(AssertionError):
        font(string)


@pytest.mark.parametrize("size", ((8, 8), (len(font_chars), 7), (8, len(font_chars))))
def test_font_invalid_file(monkeypatch, size):
    from PIL import Image

    monkeypatch.setattr(Image, "open", lambda *_, **__: Image.new("RGBA", size))

    with pytest.raises(AssertionError):
        load_font()
