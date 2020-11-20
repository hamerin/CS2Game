from __future__ import annotations
from typing import Tuple, Sequence, Any, Dict, Callable, Final
import abc
import math

import pygame as pg

from . import constant as ct
from .helpers.vector import Coordinate, parseVector, Vector, getHat  # 보조 함수 불러오기


class Mover:
    @abc.abstractmethod
    def __init__(self, pos: Coordinate):
        self.pos = parseVector(pos)
        self._frame = 0

    def advance(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
        self._frame += 1

    def in_bound(self) -> bool:  # 경계에 닿았는지
        return 0 <= self.pos[0] <= ct.WIDTH and 0 <= self.pos[1] <= ct.HEIGHT

    def as_tuple(self) -> Sequence[float]:
        return self.pos.as_tuple()

    def as_trimmed_tuple(self) -> Tuple[int, int]:
        return self.pos.as_trimmed_tuple()


def restrict(fun: Callable[..., None]) -> Callable[..., None]:  # 플레이어 동작 구역 제한
    def decorated(self: Mover, *args: Any, **kwargs: Any) -> None:
        lastpos = self.pos
        fun(self, *args, **kwargs)

        if not self.in_bound():
            self.pos = lastpos

    return decorated


class VelocityMover(Mover):  # 속도 벡터
    def __init__(self, pos: Coordinate, vel: Coordinate):
        super().__init__(pos)
        self.vel = parseVector(vel)

    def advance(self, *args: Any, **kwargs: Any) -> None:
        self.pos += self.vel
        super().advance(*args, **kwargs)


class AccelerationMover(VelocityMover):  # 가속도 벡터
    def __init__(self, pos: Coordinate, vel: Coordinate, acc: Coordinate):
        super().__init__(pos, vel)
        self.acc = parseVector(acc)

    def advance(self, *args: Any, **kwargs: Any) -> None:
        self.vel += self.acc
        super().advance(*args, **kwargs)


class EventMover(VelocityMover):  # 플레이어 속력 정의
    amplifier: float = 2.5  # 쉬프트 없을 때 배속

    def __init__(self, pos: Coordinate):
        super().__init__(pos, (0, 0))
        self.magnitude: float = 4.8  # 플레이어 속력/프레임

    @restrict  # 구역 제한
    def advance(self, *args: Any, **kwargs: Any) -> None:
        if 'event' in kwargs:
            e: pg.event.Event = kwargs['event']
            dic: Dict[int, Vector] = {pg.K_UP: Vector(0, -1),
                                      pg.K_LEFT: Vector(-1, 0),
                                      pg.K_DOWN: Vector(0, 1),
                                      pg.K_RIGHT: Vector(1, 0)}  # 이동 방향 결정

            if e.type == pg.KEYDOWN:  # 방향키 눌렀을 때
                if e.key == pg.K_LSHIFT:  # 쉬프트 누르면 속력 감소
                    self.magnitude /= EventMover.amplifier
                    self.vel /= EventMover.amplifier
                else:
                    self.vel += dic.get(e.key, Vector(0, 0)) * self.magnitude
            elif e.type == pg.KEYUP:
                if e.key == pg.K_LSHIFT:  # 쉬프트 떼면 속력 증가
                    self.magnitude *= EventMover.amplifier
                    self.vel *= EventMover.amplifier
                else:
                    self.vel -= dic.get(e.key, Vector(0, 0)) * self.magnitude
        else:
            super().advance(*args, **kwargs)


class TrackingMover(VelocityMover):  # 유도
    maxDeg: Final[float] = 2 * math.pi / 360  # 최대,최소 트는 각
    minDot: Final[float] = getHat(0) @ getHat(maxDeg)
    trackTime: Final[float] = 12  # 방향 트는 시간간격
    maxtrackTime: Final[float] = 3  # 실질 따라오는 시간

    def __init__(self, pos: Coordinate, vel: Coordinate, toTrack: Mover):
        super().__init__(pos, vel)

        self.vsize = abs(self.vel)
        self.theta = self.vel.get_theta()
        self.toFollow = toTrack

        self._followframe: Final[float] = min(TrackingMover.maxtrackTime,
                                              TrackingMover.trackTime / self.vsize) * ct.FPS  # 플레이어를 향해 움직임

    def advance(self, *args: Any, **kwargs: Any) -> None:
        if self._frame <= self._followframe:
            newtheta = (self.toFollow.pos - self.pos).get_theta()
            if getHat(self.theta) @ getHat(newtheta) >= TrackingMover.minDot:
                self.theta = newtheta
            elif getHat(self.theta).ccw(getHat(newtheta)) > 0:
                self.theta += TrackingMover.maxDeg
            else:
                self.theta -= TrackingMover.maxDeg

            self.theta %= (2 * math.pi)
            self.vel = getHat(self.theta) * self.vsize
        super().advance(*args, **kwargs)
