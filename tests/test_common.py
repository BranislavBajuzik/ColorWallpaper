from unittest import mock

import pytest

from color_wallpaper.common import *


@pytest.mark.parametrize(
    "expected, source",
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
    assert parse_hex(source) == expected


@pytest.mark.parametrize("source", ("12", "12h", "1234", "12345", "12345h", "1234567"))
def test_parse_hex_invalid(source):
    with pytest.raises(ValueError):
        parse_hex(source)


@pytest.mark.parametrize(
    "expected, source",
    (
        ((1, 2), {1: None, 2: None}),
        ((1, 2, 3), [1, 2, 3]),
        ((1, 2, 3, 4), (1.5, 2.6, 3.7, 4.8)),
        ((1, 2, 3, 4, 5), ["1.5", 2.6, "3", 4.8, "5.9"]),
    ),
)
def test_int_tuple(expected, source):
    assert int_tuple(source) == expected
    assert int_tuple(*source) == expected


@pytest.mark.parametrize(
    "expected, source",
    (
        ("normalized", "NoRmAliZeD"),
        ("normalized", " n o r m a l i z e d "),
        ("normalized", "\t\n no\n   \v rmalize   d "),
        ("[/*+abcd+*/#$%^", "[/  * + a B C d  +*  / # $ % ^ "),
    ),
)
def test_normalized(expected, source):
    assert normalized(source) == expected


@pytest.mark.parametrize(
    "name,windows,linux",
    (
        ("file.txt", "file.txt", "file.txt"),
        ('a\0file<>:"/\\|?*\37of\40hell . ', "a_file__________of\40hell", 'a_file<>_"_\\|?*\37of\40hell . '),
        ("con", "unnamed", "con"),
        ("prn", "unnamed", "prn"),
        ("aux", "unnamed", "aux"),
        ("nul", "unnamed", "nul"),
        ("com0", "com0", "com0"),
        ("com1", "unnamed", "com1"),
        ("com9", "unnamed", "com9"),
        ("lpt0", "lpt0", "lpt0"),
        ("lpt1", "unnamed", "lpt1"),
        ("lpt9", "unnamed", "lpt9"),
        ("", "unnamed", "unnamed"),
        (" ", "unnamed", " "),
        ("...", "unnamed", "..."),
    ),
)
def test_safe_path_name(name, windows, linux):
    with mock.patch("os.name", new="nt"):
        assert safe_path_name(name) == windows

    with mock.patch("os.name", new="posix"):
        assert safe_path_name(name) == linux
