from io import StringIO
from unittest.mock import patch

from src.data import *
from tests.TestBase import TestBase


class UniqueColors(TestBase):
    def test(self):
        self.assertTrue(len(hex_to_color) == len(color_hexes) == len(hex_to_color))


class Font(TestBase):
    def test_default(self):
        f = False
        t = True

        self.assertEqual(
            [
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
                [t, t, t, t, t, t, t, f],
            ],
            font('👌')
        )

    def test_ok(self):
        f = False
        t = True
        
        self.assertEqual(
            [
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
                [f, f, f, f],
            ],
            font(' ')
        )

        self.assertEqual(
            [
                [f, t, f, t, f, f],
                [f, t, f, t, f, f],
                [t, t, t, t, t, f],
                [f, t, f, t, f, f],
                [t, t, t, t, t, f],
                [f, t, f, t, f, f],
                [f, t, f, t, f, f],
                [f, f, f, f, f, f],
            ],
            font('#')
        )

        self.assertEqual(
            [
                [f, t, t, t, f, f],
                [t, f, f, f, t, f],
                [t, f, f, t, t, f],
                [t, f, t, f, t, f],
                [t, t, f, f, t, f],
                [t, f, f, f, t, f],
                [f, t, t, t, f, f],
                [f, f, f, f, f, f],
            ],
            font('0')
        )

    def test_nok(self):
        with patch('sys.stderr', new=StringIO()):
            self.assertRaises(AssertionError, font, '')
            self.assertRaises(AssertionError, font, '12')
