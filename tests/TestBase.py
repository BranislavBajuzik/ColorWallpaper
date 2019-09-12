from unittest import TestCase
from typing import Any, Callable, Tuple, Type, Union


from src.Color import Color


__all__ = ["TestBase"]


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

    def assertWeakIsInstance(self, obj: Any, cls: Union[type, Tuple[type, ...]]) -> None:
        typ = type(obj)

        self.assertEqual(typ.__name__, cls.__name__)
        self.assertEqual(dir(typ), dir(cls))
