from __future__ import annotations
from typing import Tuple, Union, Sequence, Iterator
import math


class Vector:
    """일반적인 벡터 연산을 위한 객체이다.

    Attributes:
        data: 벡터의 성분값을 가진 list
        dimension: 벡터의 차원
    
    """

    def __init__(self, *arg: float):
        self.data = [*arg]
        self.dimension = len(self.data)

    def __getitem__(self, key: int) -> float:
        """self.data[key]를 반환한다."""
        return self.data[key]

    def __setitem__(self, key: int, item: float) -> None:
        """self.data[key] = item"""
        self.data[key] = item

    def __iter__(self) -> Iterator[float]:
        """self.data의 iterator를 그대로 반환한다."""
        return self.data.__iter__()

    def __len__(self) -> int:
        """len(self.data)"""
        return len(self.data)

    def __add__(self, rhs: Vector) -> Vector:
        """self + rhs"""
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] + t[1], zip(self, rhs)))

    def __iadd__(self, rhs: Vector) -> Vector:
        return self.__add__(rhs)

    def __sub__(self, rhs: Vector) -> Vector:
        """self - rhs"""
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] - t[1], zip(self, rhs)))

    def __isub__(self, rhs: Vector) -> Vector:
        return self.__sub__(rhs)

    def __abs__(self) -> float:
        """유클리드 Norm에 의한 원점과의 거리를 반환한다."""
        return sum(map(lambda x: x**2, self))**0.5

    def __mul__(self, rhs: Union[int, float]) -> Vector:
        """self의 각 성분에 rhs(실수)를 곱하여 반환한다."""
        if not isinstance(rhs, (int, float)):
            raise TypeError

        return Vector(*map(lambda x: x*rhs, self))

    def __truediv__(self, rhs: Union[int, float]) -> Vector:
        """self의 각 성분을 rhs(실수)로 나누어 반환한다."""
        if not isinstance(rhs, (int, float)):
            raise TypeError
        return Vector(*map(lambda x: x/rhs, self))

    def __matmul__(self, rhs: Vector) -> float:
        """self와 rhs를 내적하여 반환한다."""
        if not isinstance(rhs, Vector):
            raise TypeError

        if len(self) != len(rhs):
            raise ValueError

        ret: float = 0
        for i, el in enumerate(self):
            ret += (el * rhs[i])

        return ret

    def ccw(self, rhs: Vector) -> float:
        """self와 rhs를 외적하여 반환한다. 3차원 이상일 경우 앞 2개 성분만 고려한다."""
        if not isinstance(rhs, Vector):
            raise TypeError
        return self[0]*rhs[1] - self[1]*rhs[0]

    def normalize(self) -> Vector:
        """self / abs(self)"""
        return self / abs(self)

    def as_tuple(self) -> Sequence[float]:
        """벡터의 성분을 담은 tuple을 반환한다."""
        return tuple(self)

    def as_trimmed_tuple(self) -> Tuple[int, int]:
        """벡터의 앞 두 성분만 담은 tuple을 반환한다."""
        return (int(self[0]), int(self[1]))

    def get_theta(self) -> float:
        """앞 2개 성분만 고려하여, 2차원 평면 상의 벡터의 편각을 반환한다."""
        return math.atan2(self[1], self[0])

    def rotate(self, deg: float) -> Vector:
        """앞 2개 성분만 고려하여, 2차원 평면 상에서 벡터를 deg만큼 회전하여 반환한다."""
        def _get_hat(theta: float) -> Vector:
            return Vector(math.cos(theta), math.sin(theta))

        return _get_hat(self.get_theta() + deg) * abs(self)


Coordinate = Union[Vector, Tuple[float, float]]  # 순서쌍 종류


def parseVector(cor: Coordinate) -> Vector:
    """Tuple[float, float] 혹은 Vector를 Vector형으로 변환한다."""
    if len(cor) != 2:
        raise ValueError

    if not isinstance(cor, (Vector, tuple)):
        raise TypeError

    return Vector(*cor)


def getHat(theta: float) -> Vector:
    """2차원 평면 상에서, 편각 theta인 단위벡터를 반환한다."""
    return Vector(math.cos(theta), math.sin(theta))
