from typing import TypeVar, Generic;

T = TypeVar("T");

class Pointer(Generic[T]):

    __value: T | None = None;

    def __init__(self, value: T | None) -> None:
        self.__value = value;

    def read(self) -> T | None:
        return self.__value;

    def set(self, value: T | None):
        self.__value = value;

    def readSure(self) -> T:
        if self.__value == None:
            raise Exception("attempt to call readSure method when the pointer's value is None.");
        return self.__value;


def useValue(value: T) -> Pointer[T]:
    """
    You can use typing.cast in the event you are initializing with a null literal to convert to the desired type.
    """
    return Pointer(value);