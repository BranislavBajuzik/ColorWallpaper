from functools import wraps
from unittest import TestCase
from typing import Any, Callable, Dict, Tuple, Type, Union, List


from src.CLI import Color


__all__ = ["TestBase", "override_color_random"]


def make_signature(func: Callable[..., Any], args: Tuple[Any], kwargs: Dict[str, Any]):
    args_str = ", ".join(map(str, args))
    kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

    if args and kwargs:
        args_str += ", "

    return f"{getattr(func, '__name__', repr(func))}({args_str}{kwargs_str})"


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
            raise AssertionError(
                f"{make_signature(callable, args, kwargs)} did not raise {exception.__name__}"
            ) from None

    def assertPasses(self, callable: Callable[..., Any], *args, **kwargs):
        try:
            callable(*args, **kwargs)
        except BaseException as ex:
            raise AssertionError(
                f"{make_signature(callable, args, kwargs)} raised {ex.__class__.__name__}: {ex}"
            ) from None

    def assertColorEqual(self, color: Color, rgb: tuple, name: str = None) -> None:
        self.assertEqual(rgb, color.rgb)
        if name is not None:
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
