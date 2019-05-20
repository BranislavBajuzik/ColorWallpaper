from io import StringIO
from unittest.mock import patch

from src.common import *
from tests.TestBase import TestBase


class ParseHex(TestBase):
    def test_ok(self):
        args = (
            ((0x00, 0x00, 0x00), '000000'),
            ((0xff, 0x00, 0x00), 'Ff0000'),
            ((0x01, 0x23, 0x45), '012345'),
            ((0x67, 0x89, 0xab), '6789AB'),
            ((0xcd, 0xef, 0xab), 'CDEFab'),
            ((0xcd, 0xef, 0x42), 'cdef42'),

            ((0x0, 0x0, 0x0), '000'),
            ((0xf, 0x0, 0xf), 'F0f'),
            ((0x0, 0x1, 0x2), '012'),
            ((0x3, 0x4, 0x5), '345'),
            ((0x6, 0x7, 0x8), '678'),
            ((0x9, 0xa, 0xb), '9AB'),
            ((0xc, 0xd, 0xe), 'CDE'),
            ((0xf, 0xa, 0xb), 'Fab'),
            ((0xc, 0xd, 0xe), 'cde'),
            ((0xf, 0x4, 0x2), 'f42'),
        )

        for expected, source in args:
            self.assertEqual(expected, parse_hex(source))

    def test_nok(self):
        args = (
            '12',
            '12h',
            '1234',
            '12345',
            '12345h',
            '1234567'
        )

        with patch('sys.stderr', new=StringIO()):
            for source in args:
                self.assertRaises(ValueError, parse_hex, source)


class IntTuple(TestBase):
    def test(self):
        args = (
            ((1, 2), {1: None, 2: None}),
            ((1, 2, 3), [1, 2, 3]),
            ((1, 2, 3, 4), (1.5, 2.6, 3.7, 4.8)),
            ((1, 2, 3, 4, 5), ['1.5', 2.6, '3', 4.8, '5.9'])
        )

        for expected, source in args:
            self.assertEqual(expected, int_tuple(*source))


class Normalized(TestBase):
    def test(self):
        args = (
            ('normalized', 'NoRmAliZeD'),
            ('normalized', ' n o r m a l i z e d '),
            ('normalized', '\t\n no\n   \v rmalize   d '),
            ('[/*+abcd+*/#$%^', '[/  * + a B C d  +*  / # $ % ^ ')
        )

        for expected, source in args:
            self.assertEqual(expected, normalized(source))
