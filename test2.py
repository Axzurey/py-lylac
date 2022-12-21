from typing import Generic, Optional, TypeVar

T = TypeVar("T")

class Tether(Generic[T]):

    value: T;

    def __init__(self, val: T) -> None:
        self.value = val;

    def __get__(self) -> T:
        return self.value;

    def __set__(self, val: T) -> None:
        self.value = val;


t = Tether(3);