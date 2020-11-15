from __future__ import annotations
from typing import Tuple

import pygame as pg

class BlockImage(pg.Surface):
    def __init__(self, width: int, height: int, color: Tuple[int, int, int]):
        super().__init__([width, height])
        self.fill(color)
