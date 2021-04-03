import logging

from . import Wallpaper
from .cli import DEFAULT_OUTPUT, get_options


def make_logger(log_level: int) -> logging.Logger:
    """Initialize logging for this module."""
    logger = logging.getLogger("color-wallpaper")

    logger.setLevel(log_level)

    # Disable logging
    if log_level == logging.NOTSET:
        logger.setLevel(logging.CRITICAL)

    # Logging format
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger


options = get_options()
pape_logger = make_logger(options.log_level)

if options.multiple_count == 1:
    Wallpaper(logger=pape_logger).generate_image(save=True)
else:
    if options.output is DEFAULT_OUTPUT:
        options.output = "generated"

    for _ in Wallpaper.generate_all_images(
        options.output, options.multiple_count, options.multiple_extension, pape_logger
    ):
        pass
