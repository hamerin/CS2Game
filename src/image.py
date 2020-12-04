from __future__ import annotations
from typing import Tuple

import pygame as pg

class BlockImage(pg.Surface):
    """기본적인 직사각형 이미지를 나타낸다.

    Attributes:
        width: 직사각형의 너비
        height: 직사각형의 높이
        color: 직사각형의 색상

    """
    def __init__(self, width: int, height: int, color: Tuple[int, int, int]):
        super().__init__([width, height])
        self.fill(color)
