from . import Wallpaper
from .cli import DEFAULT_OUTPUT, get_options

options = get_options()

if options.multiple_count == 1:
    Wallpaper().generate_image(save=True)
else:
    if options.output is DEFAULT_OUTPUT:
        options.output = "generated"

    for _ in Wallpaper.generate_all_images(options.output, options.multiple_count, options.multiple_extension):
        pass
