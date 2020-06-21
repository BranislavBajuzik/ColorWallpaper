import pytest

from color_wallpaper.common import *


@pytest.mark.parametrize(
    "expected,source",
    (
        ((0x00, 0x00, 0x00), "000000"),
        ((0xFF, 0x00, 0x00), "Ff0000"),
        ((0x01, 0x23, 0x45), "012345"),
        ((0x67, 0x89, 0xAB), "6789AB"),
        ((0xCD, 0xEF, 0xAB), "CDEFab"),
        ((0xCD, 0xEF, 0x42), "cdef42"),
        ((0x00, 0x00, 0x00), "000"),
        ((0xFF, 0x00, 0xFF), "F0f"),
        ((0x00, 0x11, 0x22), "012"),
        ((0x33, 0x44, 0x55), "345"),
        ((0x66, 0x77, 0x88), "678"),
        ((0x99, 0xAA, 0xBB), "9AB"),
        ((0xCC, 0xDD, 0xEE), "CDE"),
        ((0xFF, 0xAA, 0xBB), "Fab"),
        ((0xCC, 0xDD, 0xEE), "cde"),
        ((0xFF, 0x44, 0x22), "f42"),
    ),
)
def test_parse_hex_valid(expected, source):
    assert expected == parse_hex(source)


@pytest.mark.parametrize("source", ("12", "12h", "1234", "12345", "12345h", "1234567"))
def test_parse_hex_invalid(source):
    with pytest.raises(ValueError):
        parse_hex(source)


@pytest.mark.parametrize(
    "expected,source",
    (
        ((1, 2), {1: None, 2: None}),
        ((1, 2, 3), [1, 2, 3]),
        ((1, 2, 3, 4), (1.5, 2.6, 3.7, 4.8)),
        ((1, 2, 3, 4, 5), ["1.5", 2.6, "3", 4.8, "5.9"]),
    ),
)
def test_int_tuple(expected, source):
    assert expected == int_tuple(source)
    assert expected == int_tuple(*source)


@pytest.mark.parametrize(
    "expected,source",
    (
        ("normalized", "NoRmAliZeD"),
        ("normalized", " n o r m a l i z e d "),
        ("normalized", "\t\n no\n   \v rmalize   d "),
        ("[/*+abcd+*/#$%^", "[/  * + a B C d  +*  / # $ % ^ "),
    ),
)
def test_normalized(expected, source):
    assert expected == normalized(source)
