# ColorWallpaper

[![Build Status](https://travis-ci.com/BranislavBajuzik/ColorWallpaper.svg?branch=master)](https://travis-ci.com/BranislavBajuzik/ColorWallpaper)
[![Codecov](https://codecov.io/gh/BranislavBajuzik/ColorWallpaper/branch/master/graph/badge.svg)](https://codecov.io/gh/BranislavBajuzik/ColorWallpaper)

A Minimalist wallpaper generator

Generates wallpapers such as:
![Example](example.png "Example")

## Usage
- `-o`/`--output` `PATH`
  - Used to specify image output path. Defaults to `out.png`.
- `-c`/`--color` `COLOR`
  - Used to specify Background color. Must be of `#Hex`/`R,G,B`/`name` format. Defaults to `Hot Pink`.
- `-c2`/`--color2` `COLOR`
  - Used to specify text color. Must be of `#Hex`/`R,G,B`/`name` format. Defaults to inverse of `-c`.
- `-r`/`--resolution` `RESOLUTION`
  - Used to specify image resolution. Must be in `WIDTHxHEIGHT` format. Defaults to `1920x1080`.
- `-l`/`--lowercase`
  - Controls the casing of hex output
- `-f`/`--formats` `hex`/`rgb`/`hsv` [`hex`/`rgb`/`hsv` ...]
  - Declares the order and formats to display
