from __future__ import annotations
from typing import Tuple, Union
import math


class Vector(list):
    def __init__(self, *arg):
        super().__init__([*arg])

    def __add__(self, rhs: Vector) -> Vector:
        if not isinstance(rhs, Vector):
            return super().__add__(rhs)
        return Vector(*map(sum, zip(self, rhs)))

    def __iadd__(self, rhs: Vector) -> Vector:
        return self + rhs

    def __sub__(self, rhs: Vector) -> Vector:
        if not isinstance(rhs, Vector):
            return super().__add__(rhs)
        return Vector(*map(lambda t: t[0] - t[1], zip(self, rhs)))

    def __isub__(self, rhs: Vector) -> Vector:
        return self - rhs

    def __abs__(self) -> float:
        return sum(map(lambda x: x**2, self))**0.5

    def __mul__(self, rhs: Union[int, float]) -> Vector:
        if not isinstance(rhs, (int, float)):
            return super().__mul__(rhs)
        return Vector(*map(lambda x: x*rhs, self))

    def __truediv__(self, rhs: Union[int, float]) -> Vector:
        if not isinstance(rhs, (int, float)):
            raise TypeError
        return Vector(*map(lambda x: x/rhs, self))

    def normalize(self) -> Vector:
        return self * abs(self)

    def as_tuple(self) -> Tuple:
        return tuple(self)


Coordinate = Union[Vector, Tuple[float, float]]


def parseVector(cor: Coordinate) -> Vector:
    if len(cor) != 2:
        raise ValueError

    if not isinstance(cor, (Vector, tuple)):
        raise TypeError

    return Vector(*cor)


def getHat(theta: float) -> Vector:
    return Vector(math.cos(theta), math.sin(theta))
