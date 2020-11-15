from __future__ import annotations
from typing import Any

import pygame as pg

from .mover import Mover
from .helpers import get_actual


class Element(pg.sprite.Sprite):
    def __init__(self, mover: Mover, image: pg.surface.Surface):
        if not isinstance(mover, Mover):
            raise TypeError

        super().__init__()

        self.mover = mover
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.mover.as_trimmed_tuple()

        self._frame = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._frame += 1
        self.mover.advance(*args, **kwargs)
        if not self.mover.in_bound():
            self.kill()

        get_actual(self.rect).center = self.mover.as_trimmed_tuple()
