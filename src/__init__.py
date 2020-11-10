import os
import sys
from typing import Final, Tuple

import pygame as pg

from . import constant as ct
from .element import BlackBlock, BlueBlock
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, RadialFollowingBaseDanmaku
from .spriteseq import SpriteDelayer, SpriteSequence


def game() -> None:
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)
    clock = pg.time.Clock()

    dprect = displaysurf.get_rect()
    center = dprect.center

    S_player = BlueBlock(EventMover(dprect.midbottom), 10, 10)
    G_player = pg.sprite.Group(S_player)

    G_testBaseDanmaku1 = RadialFollowingBaseDanmaku(center, 3, 16, 0, S_player,
                                                    BlackBlock, 10, 10)
    G_testBaseDanmaku2 = BurstBaseDanmaku(center, 1.5, 16, 7,
                                          BlackBlock, 10, 10)
    G_testBaseDanmaku3 = BurstBaseDanmaku(center, 1, 16, 7,
                                          BlackBlock, 10, 10)
    G_testDanmaku = pg.sprite.Group(
        *G_testBaseDanmaku1, *G_testBaseDanmaku2, *G_testBaseDanmaku3)

    G_all_sprites = pg.sprite.Group(*G_testDanmaku, *G_player)
    G_event_sprites = pg.sprite.Group(*G_player)
    G_danmaku = pg.sprite.Group(*G_testDanmaku)

    while True:
        for event in pg.event.get():
            G_event_sprites.update(event=event)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.WHITE)

        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(ct.FPS)
