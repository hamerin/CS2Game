from __future__ import annotations
from typing import Any, Callable, Tuple, List

import pygame as pg

from .mover import Mover
from .element import Element
from .basedanmaku import BaseDanmaku


class Generator(Element):
    def __init__(self, mover: Mover, image: pg.Surface,
                 group: pg.sprite.Group,
                 danmaku: List[Tuple[int, Callable[[Tuple[int, int]], BaseDanmaku]]]) -> None:
        super().__init__(mover, image)

        self.group = group
        self.danmaku = danmaku

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)

        for ref, gen in self.danmaku:
            if ref > 0 and self._frame % ref == 0:
                self.group.add(*gen(self.mover.pos.as_trimmed_tuple()))

    def kill(self) -> None:
        for ref, gen in self.danmaku:
            if ref == -1:
                self.group.add(*gen(self.mover.pos.as_trimmed_tuple()))

        super().kill()
