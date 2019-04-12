from ColorWallpaper import *
from unittest import TestCase


class TestOptionsColor(TestCase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(((255, 2, 141), 'hotpink'), options.color)

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

    def test_nok(self):
        raise NotImplementedError


class TestOptionsColor2(TestCase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(((0, 253, 114), None), options.color2)

    def test_ok(self):
        raise NotImplementedError
        args = (
            (((255, 255, 255), 'white'), ['-c', 'black']),

            (((0, 253, 114), None), ['--color', '#ff028d'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).color2)


class TestOptionsResolution(TestCase):
    def test_default(self):
        options = get_options([])

        self.assertEqual((1920, 1080), options.resolution)

    def test_ok(self):
        args = (
            ((690, 420), ['-r', '690x420']),
            ((690, 420), ['-r', '690:420']),
            ((690, 420), ['--resolution', '690x420']),
            ((690, 420), ['--resolution', '690:420'])
        )

        for result, cli in args:
            self.assertEqual(result, get_options(cli).resolution)

    def test_nok(self):
        args = (
            ['-r', '690 420'],
            ['-r', '420:690a'],
            ['-r', '420a:690'],
            ['-r', '420::690'],
            ['-r', '420xx690'],
            ['-r', '420:x690'],
            ['-r', '420x:690'],
            ['-r', ''],
        )

        for cli in args:
            self.assertRaises(SystemExit, get_options, cli)
