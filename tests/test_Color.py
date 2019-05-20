from io import StringIO
from unittest.mock import patch

from Color import *
from tests.TestBase import TestBase


def color_compare(color: Color, rgb: tuple, name: str) -> bool:
    return color.rgb == rgb and color.name == name


class Create(TestBase):
    def test_ok(self):
        args = (
            ((0x00, 0x00, 0x00), 'Black'),
            ((0xFF, 0x00, 0x00), 'Red'),
            ((0xFF, 0xFF, 0xFF), 'White'),
            ((0x12, 0x34, 0x56), 'Anonymous')
        )

        for rgb, name in args:
            self.assertTrue(color_compare(Color(rgb), rgb, name))

        self.assertTrue(color_compare(Color((0x12, 0x34, 0x56), 'Custom'), (0x12, 0x34, 0x56), 'Custom'))

    def test_nok(self):
        args = (
            (0x00, 0x00),
            (0x00, 0x00, 0x00, 0x00),
            (0x1FF, 0x00, 0x00),
            (-0x01, 0x00, 0x00)
        )

        with patch('sys.stderr', new=StringIO()):
            for arg in args:
                self.assertRaises(ValueError, Color, arg)


class Hex(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), True, '000000'),
            ((0xFF, 0x00, 0x00), True, 'ff0000'),
            ((0xFF, 0x00, 0x00), False, 'FF0000'),
            ((0xAB, 0xCD, 0xEF), True, 'abcdef'),
            ((0xAB, 0xCD, 0xEF), False, 'ABCDEF')
        )

        for rgb, lowercase, result in args:
            self.assertEqual(result, Color(rgb).hex(lowercase))


class HSV(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), (0, 0, 0)),
            ((0xFF, 0x00, 0x00), (0, 100, 100)),
            ((0xAB, 0xCD, 0xEF), (210, 28, 93))
        )

        for rgb, result in args:
            self.assertEqual(result, Color(rgb).hsv)


class HSL(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), (0, 0, 0)),
            ((0xFF, 0x00, 0x00), (0, 100, 50)),
            ((0xAB, 0xCD, 0xEF), (210, 68, 80))
        )

        for rgb, result in args:
            self.assertEqual(result, Color(rgb).hsl)


class CMYK(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), (0, 0, 0, 100)),
            ((0xFF, 0x00, 0x00), (0, 100, 100, 0)),
            ((0xAB, 0xCD, 0xEF), (28, 14, 0, 6))
        )

        for rgb, result in args:
            self.assertEqual(result, Color(rgb).cmyk)


class Random(TestBase):
    def test(self):
        color = Color.random()
        from data import hex_to_color

        self.assertIn(color.hex(), hex_to_color)
        self.assertEqual(color.name, hex_to_color[color.hex()])


class FromStr(TestBase):
    def test_ok(self):
        pass
