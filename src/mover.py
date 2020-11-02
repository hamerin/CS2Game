from __future__ import annotations
from typing import Tuple
import abc

from helper import Coordinate, parseVector


class Mover():
    @abc.abstractmethod
    def __init__(self, pos: Coordinate):
        self.pos = parseVector(pos)

    def advance(self) -> None:
        pass

    def as_tuple(self) -> Tuple[float, float]:
        return self.pos.as_tuple()


class VelocityMover(Mover):
    @abc.abstractmethod
    def __init__(self, pos: Coordinate, vel: Coordinate):
        super().__init__(pos)
        self.vel = parseVector(vel)

    def advance(self) -> None:
        super().advance()
        self.pos += self.vel


class AccelerationMover(VelocityMover):
    @abc.abstractmethod
    def __init__(self, pos: Coordinate, vel: Coordinate, acc: Coordinate):
        super().__init__(pos, vel)
        self.acc = parseVector(acc)

    def advance(self) -> None:
        self.vel += self.acc
        super().advance()
