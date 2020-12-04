from __future__ import annotations
from typing import Any

import pygame as pg

from .mover import Mover
from .helpers import get_actual  # 함수 불러오기


class Element(pg.sprite.Sprite):
    """화면에 나타나는 스프라이트를 구현한다.

    Attributes:
        mover: 스프라이트의 이동을 처리하는 Mover 객체
        image: 총알을 렌더링할 이미지

    """
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
        """객체의 1프레임 후 상태를 업데이트한다."""
        self._frame += 1
        self.mover.advance(*args, **kwargs)
        if not self.mover.in_bound():  # 경계에 닿으면 kill
            self.kill()

        get_actual(self.rect).center = self.mover.as_trimmed_tuple()
