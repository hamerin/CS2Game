import os
import sys
from typing import Final, Tuple

import pygame as pg

from . import constant as ct
from .element import BlackBlock, RedBlock
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .generator import Player


def game() -> None:
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)
    clock = pg.time.Clock()

    dprect = displaysurf.get_rect()
    center = dprect.center

    G_playerbullet = pg.sprite.Group()
    S_player = Player(EventMover(dprect.midbottom),
                      G_playerbullet, *ct.ELEMENTSIZE)
    G_player = pg.sprite.Group(S_player)

    G_testBaseDanmaku1 = RadialBaseDanmaku(center, 4, 32, 0.5,
                                           RedBlock, *ct.ELEMENTSIZE,
                                           track=S_player)
    G_testBaseDanmaku2 = BurstBaseDanmaku(center, 1.5, 32, 13,
                                          BlackBlock, *ct.ELEMENTSIZE)
    G_testBaseDanmaku3 = PlaneBaseDanmaku(dprect.midtop, 6, 50, 22,
                                          BlackBlock, *ct.ELEMENTSIZE)
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
