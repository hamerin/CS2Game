import os
import sys
from typing import Final, Tuple

import pygame as pg

from . import constant as ct
from .element import BlackBlock, BlueBlock, RedBlock
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .spriteseq import SpriteDelayer, SpriteSequence


def game() -> None:
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)
    clock = pg.time.Clock()

    dprect = displaysurf.get_rect()
    center = dprect.center

    G_playerbullet = pg.sprite.Group()
    S_player = BlueBlock(EventMover(dprect.midbottom), G_playerbullet, 10, 10)
    G_player = pg.sprite.Group(S_player)

    G_testBaseDanmaku1 = RadialBaseDanmaku(center, 4, 32, 0.5,
                                           S_player, RedBlock, 10, 10)
    G_testBaseDanmaku2 = BurstBaseDanmaku(center, 1.5, 32, 13,
                                          None, BlackBlock, 10, 10)
    G_testBaseDanmaku3 = PlaneBaseDanmaku(dprect.midtop, 6, 50, 22,
                                          None, BlackBlock, 10, 10)
    G_testDanmaku = pg.sprite.Group(*G_testBaseDanmaku1,
                                    *G_testBaseDanmaku2,
                                    *G_testBaseDanmaku3)

    while True:
        G_all_sprites = pg.sprite.Group(
            *G_testDanmaku, *G_player, *G_playerbullet)
        G_event_sprites = pg.sprite.Group(*G_player)
        G_danmaku = pg.sprite.Group(*G_testDanmaku)

        for event in pg.event.get():
            G_event_sprites.update(event=event)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.WHITE)

        if pg.sprite.groupcollide(G_player, G_testDanmaku, False, False):
            print("Crashed")

        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(ct.FPS)
