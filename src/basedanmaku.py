from __future__ import annotations
from typing import Optional, Generator
import abc

import pygame as pg

from . import constant as ct
from .helpers import get_uniform_dispersion
from .helpers.vector import Coordinate, Vector, parseVector, getHat
from .mover import VelocityMover, TrackingMover
from .element import Element


ElementGenerator = Generator[Element, None, None]


class BaseDanmaku(pg.sprite.Group):
    """스프라이트 그룹을 상속한, 기본적인 탄막을 구현하는 추상 클래스이다."""
    @abc.abstractmethod
    def __init__(self, pos: Coordinate, vel: float, N: int,
                 image: pg.surface.Surface,
                 track: Optional[Element] = None):
        super().__init__()

        self.pos = parseVector(pos)
        self.vel = vel
        self.N = N
        self.image = image
        self.toTrack = track

        self.add(*self._compose_element())

    def _compose_element(self) -> ElementGenerator:
        pass


class RadialBaseDanmaku(BaseDanmaku):
    """방사형 탄막 객체이다.

    Attributes:
        pos: 탄막 중심의 위치
        vel: 총알의 속력
        N: 탄막을 이루는 총알의 개수
        offset: 탄막이 정위치에서 회전한 정도. 일반적으로 [0, 1)의 값을 가짐.
        image: 총알을 렌더링할 이미지
        track: 유도할 대상 or None

    """
    def __init__(self, pos: Coordinate, vel: float, N: int, offset: float,
                 image: pg.surface.Surface,
                 track: Optional[Element] = None):
        self.offset = offset

        super().__init__(pos, vel, N, image, track=track)

    def _compose_element(self) -> ElementGenerator:
        theta = 2 * ct.PI / self.N

        for i in range(self.N):
            hatVector = getHat(theta * (i + self.offset))

            if self.toTrack is None:
                yield Element(VelocityMover(self.pos, hatVector * self.vel),
                              self.image)
            else:
                yield Element(TrackingMover(self.pos, hatVector * self.vel, self.toTrack.mover),
                              self.image)


class BurstBaseDanmaku(BaseDanmaku):
    """분사형 탄막 객체이다.

    방사형 탄막의 일부분을 취하는 방식으로 구현된다.

    Attributes:
        pos: 탄막 중심의 위치
        vel: 총알의 속력
        baseN: 원래 방사형 탄막을 이루는 총알의 개수
        N: 탄막을 이루는 총알의 개수
        image: 총알을 렌더링할 이미지
        track: 유도할 대상 or None
        direction: 탄막의 방향

    """
    def __init__(self, pos: Coordinate, vel: float, baseN: int, N: int,
                 image: pg.surface.Surface,
                 track: Optional[Element] = None, direction: float = ct.PI / 2):
        self.baseN = baseN
        self.direction = direction

        super().__init__(pos, vel, N, image, track=track)

    def _compose_element(self) -> ElementGenerator:
        gen = get_uniform_dispersion(self.direction,
                                     2 * ct.PI / self.baseN, self.N)
        for theta in gen:
            hatVector = getHat(theta)

            if self.toTrack is None:
                yield Element(VelocityMover(self.pos, hatVector * self.vel),
                              self.image)
            else:
                yield Element(TrackingMover(self.pos, hatVector * self.vel, self.toTrack.mover),
                              self.image)


class PlaneBaseDanmaku(BaseDanmaku):
    """평면형 탄막 객체이다.

    Attributes:
        pos: 탄막 중심의 위치
        vel: 총알의 속력
        N: 탄막을 이루는 총알의 개수
        sep: 총알 사이의 간격
        image: 총알을 렌더링할 이미지
        track: 유도할 대상 or None
        direction: 탄막의 방향

    """
    def __init__(self, pos: Coordinate, vel: float, N: int, sep: float,
                 image: pg.surface.Surface,
                 track: Optional[Element] = None, direction: float = ct.PI / 2):
        self.sep = sep
        self.direction = direction

        super().__init__(pos, vel, N, image, track=track)

    def _compose_element(self) -> ElementGenerator:
        velocityHat: Vector
        if self.toTrack is None:
            velocityHat = getHat(self.direction)
        else:
            velocityHat = (self.toTrack.mover.pos - self.pos).normalize()

        seperateHat = velocityHat.rotate(ct.PI / 2)

        gen = get_uniform_dispersion(0, self.sep, self.N)
        for dist in gen:
            if self.toTrack is None:
                yield Element(VelocityMover(self.pos + seperateHat * dist, velocityHat * self.vel),
                              self.image)
            else:
                yield Element(TrackingMover(self.pos + seperateHat * dist, velocityHat * self.vel, self.toTrack.mover),
                              self.image)
