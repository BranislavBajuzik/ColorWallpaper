from io import StringIO
from pathlib import Path
from unittest.mock import patch
from unittest import skip

import Color as ColorModule
from CLI import get_options
from tests.TestBase import TestBase


# General Options
class Output(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(Path('out.png'), options.output)

    def test_ok(self):
        args = (
            (Path('picture'), ['-o', 'picture']),
            (Path('picture.png'), ['-o', 'picture.png']),
            (Path('picture'), ['--output', 'picture']),
            (Path('picture.png'), ['--output', 'picture.png'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).output)

    def test_nok(self):
        pass


class Yes(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(False, options.yes)

    def test_ok(self):
        args = (
            (True, ['-y']),
            (True, ['-y']),
            (True, ['--yes']),
            (True, ['--yes'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).yes)

    def test_nok(self):
        pass


# Color Options
class Color(TestBase):  # ToDo
    def test_default(self):
        options = get_options([])

        self.assertIs(ColorModule.Color, type(options.color))

    @skip
    def test_ok(self):
        args = (
            (((0, 0, 0), 'black'), ['-c', 'black']),
            (((0, 0, 0), 'black'), ['-c', '000']),
            (((0, 0, 0), 'black'), ['-c', '000000']),
            (((0, 0, 0), 'black'), ['-c', '#000000']),
            (((0, 0, 0), 'black'), ['--color', 'black']),
            (((0, 0, 0), 'black'), ['--color', '000']),
            (((0, 0, 0), 'black'), ['--color', '000000']),
            (((0, 0, 0), 'black'), ['--color', '#000000']),

            (((255, 2, 141), 'hotpink'), ['--color', '#ff028d'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).color)

    @skip
    def test_nok(self):
        raise NotImplementedError


class Color2(TestBase):  # ToDo
    @skip
    def test_default(self):
        options = get_options([])

        self.assertEqual(((0, 253, 114), None), options.color2)

    @skip
    def test_ok(self):
        args = (
            (((255, 255, 255), 'white'), ['-c', 'black']),

            (((0, 253, 114), None), ['--color', '#ff028d'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).color2)


class Display(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(None, options.display)

    def test_ok(self):
        args = (
            ('', ['-d', '']),
            ('Custom', ['-d', 'Custom']),
            ('Custom', ['--display', 'Custom'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).display)

    def test_nok(self):
        pass


class MinContrast(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(1, options.min_contrast)

    def test_ok(self):
        args = (
            (1, ['--min-contrast', '1']),
            (21, ['--min-contrast', '21']),
            (4.5, ['--min-contrast', '4.5']),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).min_contrast)

    def test_nok(self):
        args = (
            ['--min-contrast', '0.9'],
            ['--min-contrast', '21.1'],
            ['--min-contrast', 'a'],
            ['--min-contrast', ''],
        )

        with patch('sys.stderr', new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class OverlayColor(TestBase):  # ToDo
    pass


class OverlayContrast(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(1, options.overlay_contrast)

    def test_ok(self):
        args = (
            (1, ['--overlay-contrast', '1']),
            (21, ['--overlay-contrast', '21']),
            (4.5, ['--overlay-contrast', '4.5']),
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).overlay_contrast)

    def test_nok(self):
        args = (
            ['--overlay-contrast', '0.9'],
            ['--overlay-contrast', '21.1'],
            ['--overlay-contrast', 'a'],
            ['--overlay-contrast', ''],
        )

        with patch('sys.stderr', new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


# Display options
class Resolution(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual((1920, 1080), options.resolution)

    def test_ok(self):
        args = (
            ((690, 420), ['-r', '690x420']),
            ((690, 420), ['-r', '690:420']),
            ((690, 420), ['--resolution', '690x420']),
            ((690, 420), ['--resolution', '690:420']),

            ((150, 150), ['--resolution', '150:150'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).resolution)

    def test_nok(self):
        args = (
            ['-r', '149:420'],
            ['-r', '690:149'],
            ['-r', '149:149'],
            ['-r', '690 420'],
            ['-r', '420:690a'],
            ['-r', '420a:690'],
            ['-r', '420::690'],
            ['-r', '420xx690'],
            ['-r', '420:x690'],
            ['-r', '420x:690'],
            ['-r', ''],
        )

        with patch('sys.stderr', new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Scale(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(3, options.scale)

    def test_ok(self):
        args = (
            (1, ['-s', '1']),
            (420, ['-s', '420']),
            (1, ['--scale', '1']),
            (420, ['--scale', '420']),

            (1, ['--scale', '0']),
            (1, ['--scale', '0.9']),
            (1, ['--scale', '1.5'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).scale)

    def test_nok(self):
        args = (
            ['-s', 'a'],
            ['-s', 'nan'],
            ['-s', ''],
        )

        with patch('sys.stderr', new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Formats(TestBase):  # ToDo
    def test_default(self):
        options = get_options([])

        self.assertEqual(3, options.scale)

    def test_ok(self):
        args = (
            (1, ['-s', '1']),
            (420, ['-s', '420']),
            (1, ['--scale', '1']),
            (420, ['--scale', '420']),

            (1, ['--scale', '0']),
            (1, ['--scale', '0.9']),
            (1, ['--scale', '1.5'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).scale)

    def test_nok(self):
        args = (
            ['-s', 'a'],
            ['-s', 'nan'],
            ['-s', ''],
        )

        with patch('sys.stderr', new=StringIO()):
            for cli in args:
                self.assertRaises(SystemExit, get_options, cli)


class Lowercase(TestBase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(False, options.lowercase)

    def test_ok(self):
        args = (
            (True, ['-l']),
            (True, ['-l']),
            (True, ['--lowercase']),
            (True, ['--lowercase'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).lowercase)

    def test_nok(self):
        pass
