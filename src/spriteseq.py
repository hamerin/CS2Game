from __future__ import annotations
from typing import Any

import pygame as pg

class SpriteDelayer(pg.sprite.Group):
    def __init__(self, group: pg.sprite.Group, delay: int):
        self.group = group
        self.delay = delay

class SpriteSequence(pg.sprite.Group):
    def __init__(self, *arg: SpriteDelayer):
        super().__init__()

        self.frameCount = 0
        self.seq = [*arg]
        self.seq.reverse()

    def update(self, *args: Any, **kwargs: Any) -> None:
        while len(self.seq) > 0 and self.seq[-1].delay == self.frameCount:
            self.add(*self.seq[-1].group)
            del self.seq[-1]

        self.frameCount += 1
        super().update(*args, **kwargs)
