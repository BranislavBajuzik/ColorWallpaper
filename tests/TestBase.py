from functools import wraps
from unittest import TestCase
from typing import Any, Callable, Tuple, Type, Union, List


from src.CLI import Color


__all__ = ["TestBase", "override_color_random"]


class TestBase(TestCase):
    def assertRaises(
        self,
        exception: Union[Type[BaseException], Tuple[Type[BaseException], ...]],
        callable: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            super().assertRaises(exception, callable, *args, *kwargs)
        except AssertionError:
            args_str = ", ".join(map(str, args))
            kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())

            if args and kwargs:
                args_str += ", "

            raise AssertionError(
                f'{getattr(callable, "__name__", repr(callable))}({args_str}{kwargs_str}) '
                f"did not raise {exception.__name__}"
            ) from None

    def assertColorEqual(self, color: Color, rgb: tuple, name: str) -> None:
        self.assertEqual(rgb, color.rgb)
        self.assertEqual(name, color.name)

    def assertIsColorInstance(self, obj: Any) -> None:
        self.assertIsInstance(obj, Color)


def override_color_random(colors: List[Tuple[int, int, int]]):
    if not colors:
        raise TypeError("At least one color required")

    def fake_random():
        return Color(colors.pop(0))

    def wrapper(func):

        @wraps(func)
        def color_overrider(*args, **kwargs):
            original_random = Color.random
            Color.random = fake_random

            ret = func(*args, **kwargs)

            Color.random = original_random

            return ret

        return color_overrider

    return wrapper
