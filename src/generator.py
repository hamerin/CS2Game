from __future__ import annotations
from typing import Any, Final, Type, Sequence, Dict
import abc

import pygame as pg

from . import constant as ct
from .mover import Mover
from .element import Element, BlackBlock
from .basedanmaku import BaseDanmaku, BurstBaseDanmaku


class Generator(Element):
    @abc.abstractmethod
    def __init__(self, mover: Mover, group: pg.sprite.Group) -> None:
        super().__init__(mover)

        self.group = group


class Player(Generator):
    bulletSpeed: Final[float] = 10
    danmakuType: Final[Type[BaseDanmaku]] = BurstBaseDanmaku
    danmakuArgs: Final[Sequence[Any]] = (10, 18, 3, BlackBlock, *ct.ELEMENTSIZE)
    danmakuKwargs: Final[Dict[str, Any]] = {'direction': ct.PI / 2 * 3}

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
            self.group.add(*Player.danmakuType(self.mover.pos,
                                               *Player.danmakuArgs,
                                               **Player.danmakuKwargs))
