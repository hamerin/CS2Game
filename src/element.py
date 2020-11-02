from __future__ import annotations
from typing import Type
import abc

import pygame as pg

from mover import Mover


class Element(pg.sprite.Sprite):
    @abc.abstractmethod
    def __init__(self, mover: Type[Mover]):
        if not isinstance(mover, Mover):
            raise TypeError

        self.mover = mover
        super().__init__()

    def update(self) -> None:
        self.mover.advance()
        self.rect.center = self.mover.as_tuple()


class BlackBlock(Element):
    def __init__(self, mover: Type[Mover], width: int, height: int):
        super().__init__(mover)

        self.image = pg.Surface([width, height])
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = self.mover.as_tuple()
