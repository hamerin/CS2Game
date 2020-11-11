from __future__ import annotations
from typing import Any
import abc

import pygame as pg

from . import constant as ct
from .mover import Mover, VelocityMover


class Element(pg.sprite.Sprite):
    @abc.abstractmethod
    def __init__(self, mover: Mover):
        if not isinstance(mover, Mover):
            raise TypeError

        super().__init__()

        self.mover = mover
        self._frame = 0

        self.rect: pg.rect.Rect

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._frame += 1
        self.mover.advance(*args, **kwargs)
        if not self.mover.in_bound():
            self.kill()
        self.rect.center = self.mover.as_trimmed_tuple()


class Generator(Element):
    @abc.abstractmethod
    def __init__(self, mover: Mover, group: pg.sprite.Group) -> None:
        super().__init__(mover)

        self.group = group


class BlackBlock(Element):
    def __init__(self, mover: Mover, width: int, height: int):
        super().__init__(mover)

        self.image = pg.Surface([width, height])
        self.image.fill(ct.BLACK)

        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.center = self.mover.as_trimmed_tuple()


class RedBlock(Element):
    def __init__(self, mover: Mover, width: int, height: int):
        super().__init__(mover)

        self.image = pg.Surface([width, height])
        self.image.fill((255, 0, 0))

        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.center = self.mover.as_trimmed_tuple()


class BlueBlock(Generator):
    def __init__(self, mover: Mover, group: pg.sprite.Group, width: int, height: int):
        super().__init__(mover, group)

        self.image = pg.Surface([width, height])
        self.image.fill(ct.BLUE)

        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.center = self.mover.as_trimmed_tuple()

        self.frameCount = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)

        if self._frame % 10 == 0:
            self.group.add(BlackBlock(VelocityMover(self.mover.pos, (0, -10)), 10, 10))
