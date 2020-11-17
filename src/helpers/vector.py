from __future__ import annotations
from typing import Tuple, Union, Sequence, Iterator
import math


class Vector:
    def __init__(self, *arg: float):
        self.data = [*arg]
        self.dimension = len(self.data)

    def __getitem__(self, key: int) -> float:  # 값 가져오기
        return self.data[key]

    def __setitem__(self, key: int, item: float) -> None:  # 아이템 대입
        self.data[key] = item

    def __iter__(self) -> Iterator[float]:  # 이터레이션
        return self.data.__iter__()

    def __len__(self) -> int:  # 벡터 길이
        return len(self.data)

    def __add__(self, rhs: Vector) -> Vector:  # 벡터합
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] + t[1], zip(self, rhs)))

    def __iadd__(self, rhs: Vector) -> Vector:  # 벡터 + 실수
        return self.__add__(rhs)

    def __sub__(self, rhs: Vector) -> Vector:  # 벡터차
        if not isinstance(rhs, Vector):
            raise TypeError

        if self.dimension != rhs.dimension:
            raise ValueError

        return Vector(*map(lambda t: t[0] - t[1], zip(self, rhs)))

    def __isub__(self, rhs: Vector) -> Vector:  # 벡터-실수
        return self.__sub__(rhs)

    def __abs__(self) -> float:  # 절댓값
        return sum(map(lambda x: x**2, self))**0.5

    def __mul__(self, rhs: Union[int, float]) -> Vector:  # 벡터 * 실수
        if not isinstance(rhs, (int, float)):
            raise TypeError

        return Vector(*map(lambda x: x*rhs, self))

    def __matmul__(self, rhs: Vector) -> float:  # 내적
        if not isinstance(rhs, Vector):
            raise TypeError

        if len(self) != len(rhs):
            raise ValueError

        ret: float = 0
        for i, el in enumerate(self):
            ret += (el * rhs[i])

        return ret

    def __truediv__(self, rhs: Union[int, float]) -> Vector:  # 나눗셈
        if not isinstance(rhs, (int, float)):
            raise TypeError
        return Vector(*map(lambda x: x/rhs, self))

    def ccw(self, rhs: Vector) -> float:  # 외적
        if not isinstance(rhs, Vector):
            raise TypeError
        return self[0]*rhs[1] - self[1]*rhs[0]

    def normalize(self) -> Vector:  # 단위벡터
        return self / abs(self)

    def as_tuple(self) -> Sequence[float]:  # 성분 호출
        return tuple(self)

    def as_trimmed_tuple(self) -> Tuple[int, int]:  # 절대값 성분 호출
        return (int(self[0]), int(self[1]))

    def get_theta(self) -> float:  # 각 호출
        return math.atan2(self[1], self[0])

    def rotate(self, deg: float) -> Vector:  # 회전
        def _get_hat(theta: float) -> Vector:
            return Vector(math.cos(theta), math.sin(theta))

        return _get_hat(self.get_theta() + deg) * abs(self)

Coordinate = Union[Vector, Tuple[float, float]]  # 순서쌍 종류

def parseVector(cor: Coordinate) -> Vector:  # 벡터로 변환
    if len(cor) != 2:
        raise ValueError

    if not isinstance(cor, (Vector, tuple)):
        raise TypeError

    return Vector(*cor)


def getHat(theta: float) -> Vector:  # 단위벡터
    return Vector(math.cos(theta), math.sin(theta))
