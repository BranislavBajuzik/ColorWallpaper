# ColorWallpaper

[![Build Status](https://travis-ci.com/BranislavBajuzik/ColorWallpaper.svg?branch=master)](https://travis-ci.com/BranislavBajuzik/ColorWallpaper)
[![Codecov](https://codecov.io/gh/BranislavBajuzik/ColorWallpaper/branch/master/graph/badge.svg)](https://codecov.io/gh/BranislavBajuzik/ColorWallpaper)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/af954c94432a446a95e004079d089f6a)](https://www.codacy.com/app/BranislavBajuzik/ColorWallpaper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=BranislavBajuzik/ColorWallpaper&amp;utm_campaign=Badge_Grade)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Minimalist wallpaper generator

Generates wallpapers such as:
![Example](example.png "Example")

## Usage
General options
- `-o`/`--output` `PATH`
  - Used to specify image output path. Defaults to `out.png`.
- `-y`/`--yes`
  - Forces overwrite of `--output`

Color options
- `-c`/`--color` `COLOR`
  - Used to specify Background color. Also accepts `random` (the default) which picks random named color.
- `-c2`/`--color2` `COLOR`
  - Used to specify text color. Also accepts `inverted` (the default) which is the inverse of `--color`.
- `-d`/`--display` `NAME`
  - Overrides the display name of the `--color`. Empty string disables the name row.
- `--min-contrast` `CONTRAST`
  - Min contrast of `--color` and `--color2`, if `--color2` is `inverted`. Will raise if this can not be satisfied. Defaults to `1`
- `--overlay-color` `COLOR`
  - Used to specify color of potential overlay, like icons or text.
- `--overlay-contrast` `CONTRAST`
  - Min contrast of --color and --overlay-color. Will raise if this can not be satisfied. Defaults to `1`

Display options
- `-r`/`--resolution` `RESOLUTION`
  - Used to specify image resolution. Defaults to `1920x1080`.
- `-s`/`--scale` `SCALE`
  - The size of the highlight will be divided by this. Defaults to `3`.
- `-f`/`--formats` `FORMAT` [`FORMAT` ...]
  - Declares the order and formats to display
- `-l`/`--lowercase`
  - Controls the casing of hex output

### Argument formats
- `COLOR`
  - `#Hex`: Three or six hexadecimal digits optionally starting with `#`.
  - `R,G,B`: Three comma separated numbers in range 0-255.
  - Valid name of a color.
- `CONTRAST`
  - A float in range 1-21.
- `RESOLUTION`
  - Two positive integers greater or equal to 150, separated by `x` or `:`.
- `FORMAT`
  - Self explanatory: `hex`, `rgb`, `hsv`, `hsl`, `cmyk` 
  - `empty`: Empty row.
  - `#hex`: `hex`, but starting with `#`
  - `#HEX`, `HEX`: Like `hex`, but uppercase

## Dependencies
- [PIL](https://github.com/python-pillow/Pillow)
