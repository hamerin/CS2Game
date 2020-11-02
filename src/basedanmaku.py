from __future__ import annotations
from typing import Type, TypeVar, Generic, Any
import abc
import math

import pygame as pg

from helper import Coordinate, parseVector, getHat
from mover import VelocityMover
from element import Element

T = TypeVar('T', Element, Type[Element])


class RadialBaseDanmaku(pg.sprite.Group, Generic[T]):
    def __init__(self, BaseElement: Type[T],
                 pos: Coordinate, vel: float, N: int, offset: float,
                 *args: Any):
        super().__init__()

        self.pos = parseVector(pos)
        self.vel = vel
        self.N = N

        theta = 2 * math.pi / self.N
        for i in range(self.N):
            hatVector = getHat(theta * (i + offset))
            self.add(BaseElement(VelocityMover(pos, hatVector * self.vel),
                                 *args))
