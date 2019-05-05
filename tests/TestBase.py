from unittest import TestCase
from typing import Any, Callable, Tuple, Type, Union


__all__ = ['TestBase']


class TestBase(TestCase):
    def assertRaises(self,
                     exception: Union[Type[BaseException], Tuple[Type[BaseException], ...]],
                     callable: Callable[..., Any],
                     *args: Any, **kwargs: Any) -> None:
        try:
            super().assertRaises(exception, callable, *args, *kwargs)
        except AssertionError:
            args_str = ', '.join(map(str, args))
            kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())

            if args and kwargs:
                args_str += ', '

            raise AssertionError(f'{getattr(callable, "__name__", repr(callable))}({args_str}{kwargs_str}) '
                                 f'did not raise {exception.__name__}') from None
