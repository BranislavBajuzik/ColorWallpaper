from io import StringIO
from unittest.mock import patch

from src.Color import *
from tests.TestBase import TestBase


class Create(TestBase):
    def test_ok(self):
        args = (
            ((0x00, 0x00, 0x00), 'Black'),
            ((0xFF, 0x00, 0x00), 'Red'),
            ((0xFF, 0xFF, 0xFF), 'White'),
            ((0x12, 0x34, 0x56), 'Anonymous')
        )

        for rgb, name in args:
            self.color_compare(Color(rgb), rgb, name)

        self.color_compare(Color((0x12, 0x34, 0x56), 'Custom'), (0x12, 0x34, 0x56), 'Custom')

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


class StrRepr(TestBase):
    def test(self):
        self.assertEqual('Color(rgb=(0, 0, 0), name=\'Black\')', str(Color((0x00, 0x00, 0x00), 'Black')))
        self.assertEqual('Color(rgb=(0, 0, 0), name=\'Black\')', repr(Color((0x00, 0x00, 0x00), 'Black')))


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


class Luminance(TestBase):
    def test(self):
        args = (
            (0.0, (0x00, 0x00, 0x00)),
            (1.0, (0xFF, 0xFF, 0xFF)),
            (0.2126, (0xFF, 0x00, 0x00)),
            (0.7151, (0x00, 0xFF, 0x00)),
            (0.0722, (0x00, 0x00, 0xFF)),
        )

        for luminance, rgb in args:
            self.assertEqual(luminance, int(Color(rgb).luminance*10_000)/10_000)


class TrueDiv(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF), 21.0),
            ((0x00, 0x00, 0xFF), (0xFF, 0xFF, 0xFF), 8.59),
            ((0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), 2.14),
            ((0x00, 0x00, 0x00), (0x00, 0x00, 0x00), 1.0),
            ((0xFF, 0xFF, 0xFF), (0xFF, 0xFF, 0xFF), 1.0)
        )

        for a, b, result in args:
            a, b = Color(a), Color(b)
            self.assertEqual(a / b, b / a)
            self.assertEqual(result, int((a / b)*100)/100)


class Div(TestBase):
    def test(self):
        args = (
            ((0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF), 21),
            ((0x00, 0x00, 0xFF), (0xFF, 0xFF, 0xFF), 8),
            ((0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), 2),
            ((0x00, 0x00, 0x00), (0x00, 0x00, 0x00), 1),
            ((0xFF, 0xFF, 0xFF), (0xFF, 0xFF, 0xFF), 1)
        )

        for a, b, result in args:
            a, b = Color(a), Color(b)
            self.assertEqual(a // b, b // a)
            self.assertEqual(result, a // b)


class Inverted(TestBase):  # ToDo
    pass


class Random(TestBase):
    def test(self):
        color = Color.random()
        from data import hex_to_color

        self.assertIn(color.hex(), hex_to_color)
        self.assertEqual(color.name, hex_to_color[color.hex()])


class FromHSL(TestBase):
    def test_ok(self):
        args = (
            ((0, 0, 0), (0x00, 0x00, 0x00), 'Black'),
            ((0, 100, 50), (0xFF, 0x00, 0x00), 'Red'),
            ((210, 68, 80.5), (0xAB, 0xCD, 0xEF), 'Anonymous')
        )

        for (h, s, l), rgb, name in args:
            self.color_compare(Color.from_hsl(h, s, l), rgb, name)

    def test_nok(self):
        args = (
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
            (361, 0, 0),
            (0, 361, 0),
            (0, 0, 361),
        )

        with patch('sys.stderr', new=StringIO()):
            for arg in args:
                self.assertRaises(ValueError, Color.from_hsl, *arg)


class FromStr(TestBase):  # ToDo
    def test_ok(self):
        pass
