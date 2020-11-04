from __future__ import annotations
from typing import Tuple, Sequence
import abc

from .vector import Coordinate, parseVector


class Mover():
    @abc.abstractmethod
    def __init__(self, pos: Coordinate):
        self.pos = parseVector(pos)

    def advance(self) -> None:
        pass

    def as_tuple(self) -> Sequence[float]:
        return self.pos.as_tuple()

    def as_trimmed_tuple(self) -> Tuple[int, int]:
        return self.pos.as_trimmed_tuple()


class VelocityMover(Mover):
    def __init__(self, pos: Coordinate, vel: Coordinate):
        super().__init__(pos)
        self.vel = parseVector(vel)

    def advance(self) -> None:
        super().advance()
        self.pos += self.vel


class AccelerationMover(VelocityMover):
    def __init__(self, pos: Coordinate, vel: Coordinate, acc: Coordinate):
        super().__init__(pos, vel)
        self.acc = parseVector(acc)

    def advance(self) -> None:
        self.vel += self.acc
        super().advance()
