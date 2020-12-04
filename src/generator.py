from __future__ import annotations
from typing import Any, Callable, Tuple, List

import pygame as pg

from .mover import Mover
from .element import Element
from .basedanmaku import BaseDanmaku


class Generator(Element):
    """다른 스프라이트를 생성하는 스프라이트를 구현한다.

    danmaku의 원소의 첫째 원소는 생성 주기이며, 둘째 원소는 생성 함수이다.
    생성 주기는 프레임 단위이며, -1일 경우 객체가 파괴될 때 생성된다.

    Attributes:
        mover: 스프라이트의 이동을 처리하는 Mover 객체
        image: 총알을 렌더링할 이미지
        group: 생성될 스프라이트가 포함될 그룹
        danmaku: 탄막 생성 주기와 생성 함수를 포함하는 list

    """
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
                pg.mixer.Sound.play(pg.mixer.Sound('audio/matched.wav'))

        super().kill()
