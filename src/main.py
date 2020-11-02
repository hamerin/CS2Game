import os
import sys
from typing import Final, Tuple

import pygame as pg
from pygame.locals import QUIT

from element import BlackBlock
from mover import AccelerationMover
from basedanmaku import RadialBaseDanmaku

width: Final[int] = 2400
height: Final[int] = 1600
white: Final[Tuple[int, int, int]] = (255, 255, 255)
black: Final[Tuple[int, int, int]] = (0,   0,   0)
fps: Final[int] = 60

def game():
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((width, height), 0, 32)
    clock = pg.time.Clock()

    G_testDanmaku1 = RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 4, 16, 0, 20, 20)
    G_testDanmaku2 = RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 3, 16, 0.5, 20, 20)
    G_testDanmaku3 = RadialBaseDanmaku(
        BlackBlock, displaysurf.get_rect().center, 2, 16, 0, 20, 20)
    G_all_sprites = pg.sprite.Group(*G_testDanmaku1, *G_testDanmaku2, *G_testDanmaku3)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        displaysurf.fill(white)

        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(fps)
