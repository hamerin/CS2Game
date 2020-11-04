import os
import sys
from typing import Final, Tuple

import pygame as pg

from .element import BlackBlock
from .mover import AccelerationMover
from .basedanmaku import RadialBaseDanmaku
from .spriteseq import SpriteDelayer, SpriteSequence

width: Final[int] = 2400
height: Final[int] = 1600
white: Final[Tuple[int, int, int]] = (255, 255, 255)
black: Final[Tuple[int, int, int]] = (0,   0,   0)
fps: Final[int] = 60


def game() -> None:
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((width, height), 0, 32)
    clock = pg.time.Clock()

    G_testBaseDanmaku1 = SpriteDelayer(RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 4, 16, 0, 20, 20), 0)
    G_testBaseDanmaku2 = SpriteDelayer(RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 3, 16, 0.5, 20, 20), 5)
    G_testBaseDanmaku3 = SpriteDelayer(RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 2, 16, 0, 20, 20), 10)
    G_testDanmaku = SpriteSequence(
        G_testBaseDanmaku1, G_testBaseDanmaku2, G_testBaseDanmaku3)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        displaysurf.fill(white)

        G_testDanmaku.update()
        G_all_sprites = pg.sprite.Group(*G_testDanmaku)
        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(fps)
