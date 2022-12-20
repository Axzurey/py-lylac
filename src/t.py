class Test: ...

from typing import Literal, TypeVar, Generic, TypedDict;

class Types(TypedDict):
    amount: int;
    size: Test;

T = TypeVar('T');

def x(a: T, v: T) -> Types[T]:
    return v

    #keep playin https://docs.python.org/3/library/typing.html#generics