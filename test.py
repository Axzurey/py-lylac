from __future__ import annotations

import sys
from typing import Generic, Optional, TypeVar, overload

if sys.version_info < (3, 9):
    from typing import Callable, List, Type
else:
    from builtins import list as List, type as Type
    from collections.abc import Callable

if sys.version_info < (3, 11):
    Self = TypeVar("Self", bound="Tether")
else:
    from typing import Self

T = TypeVar("T")
VT = TypeVar("VT")


class Tether(Generic[T, VT]):
    name: str

    def __init__(self: Self) -> None:
        self.name = ""

    @overload
    def __get__(self: Self, instance: T, owner: Optional[Type[T]] = ...) -> VT:
        ...

    @overload
    def __get__(self: Self, instance: None, owner: Optional[Type[T]] = ...) -> Self:
        ...

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        else:
            return getattr(instance, self.name)

    def __set__(self: Self, instance: T, value: VT) -> None:
        setattr(instance, self.name, value)
        if hasattr(instance, f"{self.name}_connection"):
            getattr(instance, f"{self.name}_connection")(value)

    def __set_name__(self: Self, owner: Type[T], name: str) -> None:
        self.name = f"_{name}"  # Add underscore to avoid overwriting itself.

    def __delete__(self: Self, instance: T) -> None:
        delattr(instance, self.name)

    def connect(self: Self, instance: T, connection: Callable[[VT], object]) -> None:
        setattr(instance, f"{self.name}_connection", connection)

class Instance:
    name: Tether[Instance, str] = Tether()
    date: Tether[Instance, float] = Tether()
    color: Tether[Instance, int] = Tether()

example = Instance()

Instance.color.connect(example, lambda out: print(out))

example.color = 100;
