from __future__ import annotations
from typing import Type, Any, Optional, Generator
import abc
import math

import pygame as pg

from .helpers import get_uniform_dispersion
from .helpers.vector import Coordinate, Vector, parseVector, getHat
from .mover import VelocityMover, TrackingMover
from .element import Element


ElementGenerator = Generator[Element, None, None]


class BaseDanmaku(pg.sprite.Group):
    @abc.abstractmethod
    def __init__(self, pos: Coordinate, vel: float, N: int,
                 toTrack: Optional[Element], BaseElement: Type[Element], *args: Any):
        super().__init__()

        self.pos = parseVector(pos)
        self.vel = vel
        self.N = N
        self.Element = BaseElement
        self.toTrack = toTrack

        self.add(*self._compose_element(*args))

    def _compose_element(self, *args: Any) -> ElementGenerator:
        pass


class RadialBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, N: int, offset: float,
                 toTrack: Optional[Element], BaseElement: Type[Element], *args: Any):
        self.offset = offset

        super().__init__(pos, vel, N, toTrack, BaseElement, *args)

    def _compose_element(self, *args: Any) -> ElementGenerator:
        theta = 2 * math.pi / self.N

        for i in range(self.N):
            hatVector = getHat(theta * (i + self.offset))

            if self.toTrack is None:
                yield self.Element(VelocityMover(self.pos, hatVector * self.vel),
                                   *args)
            else:
                yield self.Element(TrackingMover(self.pos, hatVector * self.vel, self.toTrack.mover),
                                   *args)


class BurstBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, baseN: int, N: int,
                 toTrack: Optional[Element], BaseElement: Type[Element], *args: Any):
        self.baseN = baseN

        super().__init__(pos, vel, N, toTrack, BaseElement, *args)

    def _compose_element(self, *args: Any) -> ElementGenerator:
        gen = get_uniform_dispersion(
            math.pi / 2, 2 * math.pi / self.baseN, self.N)
        for theta in gen:
            hatVector = getHat(theta)

            if self.toTrack is None:
                yield self.Element(VelocityMover(self.pos, hatVector * self.vel),
                                   *args)
            else:
                yield self.Element(TrackingMover(self.pos, hatVector * self.vel, self.toTrack.mover),
                                   *args)


class PlaneBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, N: int, sep: float,
                 toTrack: Optional[Element], BaseElement: Type[Element], *args: Any):
        self.sep = sep

        super().__init__(pos, vel, N, toTrack, BaseElement, *args)

    def _compose_element(self, *args: Any) -> ElementGenerator:
        velocityHat: Vector
        if self.toTrack is None:
            velocityHat = Vector(0, 1)
        else:
            velocityHat = (self.toTrack.mover.pos - self.pos).normalize()

        seperateHat = velocityHat.rotate(math.pi / 2)

        gen = get_uniform_dispersion(0, self.sep, self.N)
        for dist in gen:
            if self.toTrack is None:
                yield self.Element(VelocityMover(self.pos + seperateHat * dist, velocityHat * self.vel),
                                   *args)
            else:
                yield self.Element(TrackingMover(self.pos + seperateHat * dist, velocityHat * self.vel, self.toTrack.mover),
                                   *args)
