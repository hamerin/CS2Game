from __future__ import annotations
from typing import Tuple, Sequence, Any, Dict, Callable
import abc
import math

import pygame as pg

from . import constant as ct
from .vector import Coordinate, parseVector, Vector, getHat


class Mover():
    @abc.abstractmethod
    def __init__(self, pos: Coordinate):
        self.pos = parseVector(pos)

    def advance(self, *args: Any, **kwargs: Any) -> None:
        pass

    def in_bound(self) -> bool:
        return 0 <= self.pos[0] <= ct.WIDTH and 0 <= self.pos[1] <= ct.HEIGHT

    def as_tuple(self) -> Sequence[float]:
        return self.pos.as_tuple()

    def as_trimmed_tuple(self) -> Tuple[int, int]:
        return self.pos.as_trimmed_tuple()


def restrict(fun: Callable[..., None]) -> Callable[..., None]:
    def decorated(self: Mover, *args: Any, **kwargs: Any) -> None:
        lastpos = self.pos
        fun(self, *args, **kwargs)

        if not self.in_bound():
            self.pos = lastpos

    return decorated


class VelocityMover(Mover):
    def __init__(self, pos: Coordinate, vel: Coordinate):
        super().__init__(pos)
        self.vel = parseVector(vel)

    def advance(self, *args: Any, **kwargs: Any) -> None:
        self.pos += self.vel
        super().advance(*args, **kwargs)


class AccelerationMover(VelocityMover):
    def __init__(self, pos: Coordinate, vel: Coordinate, acc: Coordinate):
        super().__init__(pos, vel)
        self.acc = parseVector(acc)

    def advance(self, *args: Any, **kwargs: Any) -> None:
        self.vel += self.acc
        super().advance(*args, **kwargs)


class EventMover(VelocityMover):
    amplifier: float = 4

    def __init__(self, pos: Coordinate):
        super().__init__(pos, (0, 0))
        self.magnitude: float = 8

    @restrict
    def advance(self, *args: Any, **kwargs: Any) -> None:
        if 'event' in kwargs:
            e: pg.event.Event = kwargs['event']
            dic: Dict[int, Vector] = {pg.K_UP: Vector(0, -1),
                                      pg.K_LEFT: Vector(-1, 0),
                                      pg.K_DOWN: Vector(0, 1),
                                      pg.K_RIGHT: Vector(1, 0)}

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_LSHIFT:
                    self.magnitude /= EventMover.amplifier
                    self.vel /= EventMover.amplifier
                else:
                    self.vel += dic.get(e.key, Vector(0, 0)) * self.magnitude
            elif e.type == pg.KEYUP:
                if e.key == pg.K_LSHIFT:
                    self.magnitude *= EventMover.amplifier
                    self.vel *= EventMover.amplifier
                else:
                    self.vel -= dic.get(e.key, Vector(0, 0)) * self.magnitude
        else:
            super().advance(*args, **kwargs)


class FollowingMover(VelocityMover):
    maxDeg = 2 * math.pi / 360
    minDot = getHat(0) @ getHat(maxDeg)
    followTime = 30

    def __init__(self, pos: Coordinate, vel: Coordinate, toFollow: Mover):
        super().__init__(pos, vel)

        self.vsize = abs(self.vel)
        self.theta = self.vel.get_theta()
        self.toFollow = toFollow
        self.frameCount = 0

    def advance(self, *args: Any, **kwargs: Any) -> None:
        self.frameCount += 1

        if self.frameCount <= self.followTime * ct.FPS / self.vsize:
            newtheta = (self.toFollow.pos - self.pos).get_theta()
            if getHat(self.theta) @ getHat(newtheta) >= self.minDot:
                self.theta = newtheta
            elif getHat(self.theta).ccw(getHat(newtheta)) > 0:
                self.theta += self.maxDeg
            else:
                self.theta -= self.maxDeg

            self.theta %= (2 * math.pi)
            self.vel = getHat(self.theta) * self.vsize
        super().advance(*args, **kwargs)
