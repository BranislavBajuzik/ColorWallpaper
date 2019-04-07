from ColorWallpaper import *
from unittest import TestCase


class TestResolutionColor(TestCase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(options.color, ((255, 105, 180), 'hotpink'))

    def test_ok(self):
        args = (
            (['-c', 'black'], ((0, 0, 0), 'black')),
            (['-c', '000'], ((0, 0, 0), 'black')),
            (['-c', '000000'], ((0, 0, 0), 'black')),
            (['-c', '#000000'], ((0, 0, 0), 'black')),
            (['--color', 'black'], ((0, 0, 0), 'black')),
            (['--color', '000'], ((0, 0, 0), 'black')),
            (['--color', '000000'], ((0, 0, 0), 'black')),
            (['--color', '#000000'], ((0, 0, 0), 'black')),

            (['--color', '#ff69b4'], ((255, 105, 180), 'hotpink'))
        )

        for cli, result in args:
            self.assertEqual(get_options(cli).color, result)

    def test_nok(self):
        raise NotImplementedError


class TestResolutionOptions(TestCase):
    def test_default(self):
        options = get_options([])

        self.assertEqual(options.resolution, (1920, 1080))

    def test_ok(self):
        args = (
            (['-r', '690x420'], (690, 420)),
            (['-r', '690:420'], (690, 420)),
            (['--resolution', '690x420'], (690, 420)),
            (['--resolution', '690:420'], (690, 420))
        )

        for cli, result in args:
            self.assertEqual(get_options(cli).resolution, result)

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
