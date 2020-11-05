from __future__ import annotations
from typing import Tuple, Union, Sequence, Iterator
import math


class Vector:
    def __init__(self, *arg: float):
        self.data = [*arg]
        self.dimension = len(self.data)

    def __getitem__(self, key: int) -> float:
        return self.data[key]

    def __setitem__(self, key:int, item: float) -> None:
        self.data[key] = item

    def __iter__(self) -> Iterator[float]:
        return self.data.__iter__()

    def __len__(self) -> int:
        return len(self.data)

    def __add__(self, rhs: Vector) -> Vector:
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] + t[1], zip(self, rhs)))

    def __iadd__(self, rhs: Vector) -> Vector:
        return self.__add__(rhs)

    def __sub__(self, rhs: Vector) -> Vector:
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] - t[1], zip(self, rhs)))

    def __isub__(self, rhs: Vector) -> Vector:
        return self.__sub__(rhs)

    def __abs__(self) -> float:
        return sum(map(lambda x: x**2, self))**0.5

    def __mul__(self, rhs: Union[int, float]) -> Vector:
        if not isinstance(rhs, (int, float)):
            raise TypeError
        return Vector(*map(lambda x: x*rhs, self))

    def __truediv__(self, rhs: Union[int, float]) -> Vector:
        if not isinstance(rhs, (int, float)):
            raise TypeError
        return Vector(*map(lambda x: x/rhs, self))

    def normalize(self) -> Vector:
        return self * abs(self)

    def as_tuple(self) -> Sequence[float]:
        return tuple(self)

    def as_trimmed_tuple(self) -> Tuple[int, int]:
        return (int(self[0]), int(self[1]))


Coordinate = Union[Vector, Tuple[float, float]]

def parseVector(cor: Coordinate) -> Vector:
    if len(cor) != 2:
        raise ValueError

    if not isinstance(cor, (Vector, tuple)):
        raise TypeError

    return Vector(*cor)


def getHat(theta: float) -> Vector:
    return Vector(math.cos(theta), math.sin(theta))
