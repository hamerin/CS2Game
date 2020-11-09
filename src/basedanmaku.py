from __future__ import annotations
from typing import Type, Any
import math

import pygame as pg

from .vector import Coordinate, parseVector, getHat
from .mover import VelocityMover, FollowingMover
from .element import Element


class BaseDanmaku(pg.sprite.Group):
    def __init__(self, pos: Coordinate, vel: float, N: int,
                 BaseElement: Type[Element]):
        super().__init__()

        self.pos = parseVector(pos)
        self.vel = vel
        self.N = N
        self.Element = BaseElement


class RadialBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, N: int, offset: float,
                 BaseElement: Type[Element], *args: Any):
        super().__init__(pos, vel, N, BaseElement)

        self.offset = offset

        theta = 2 * math.pi / self.N
        for i in range(self.N):
            hatVector = getHat(theta * (i + offset))
            self.add(self.Element(VelocityMover(pos, hatVector * self.vel),
                                  *args))

class RadialFollowingBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, N: int, offset: float,
                 toFollow: Element, BaseElement: Type[Element], *args: Any):
        super().__init__(pos, vel, N, BaseElement)

        self.offset = offset
        self.toFollow = toFollow

        theta = 2 * math.pi / self.N
        for i in range(self.N):
            hatVector = getHat(theta * (i + offset))
            self.add(self.Element(FollowingMover(pos, hatVector * self.vel, self.toFollow.mover),
                                  *args))

class BurstBaseDanmaku(BaseDanmaku):
    def __init__(self, pos: Coordinate, vel: float, baseN: int, N: int,
                 BaseElement: Type[Element], *args: Any):
        super().__init__(pos, vel, N, BaseElement)

        self.baseN = baseN

        theta = 2 * math.pi / self.baseN
        initialtheta = math.pi / 2 - math.pi * (self.N - 1) / self.baseN

        for i in range(self.N):
            hatVector = getHat(initialtheta + theta * i)
            self.add(self.Element(VelocityMover(pos, hatVector * self.vel),
                                  *args))
