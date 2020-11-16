import os
import sys
import json
from typing import Final, Tuple, Dict

import pygame as pg
from . import constant as ct
from .element import Element
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .image import BlockImage
from .parser import Parser


def game() -> None:
    print(os.getcwd())
    pg.init()  # 초기화

    pg.display.set_caption('Hello, world!')
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)
    clock = pg.time.Clock()

    screenrect = displaysurf.get_rect()

    groupdict: Dict[str, pg.sprite.Group] = dict()
    groupdict = {'bullet': pg.sprite.Group(),
                 'player': pg.sprite.Group(),
                 'enemy': pg.sprite.Group(),
                 'danmaku': pg.sprite.Group()}

    spritedict: Dict[str, Element] = dict()

    parser = Parser(screenrect, groupdict, spritedict)
    spritedict['player'] = parser.load("assets/element/player.json")

    groupdict['player'].add(spritedict['player'])
    #groupdict['danmaku'].add(*parser.load("assets/basedanmaku/test1.json"))
    #groupdict['danmaku'].add(*parser.load("assets/basedanmaku/test2.json"))
    #groupdict['danmaku'].add(*parser.load("assets/basedanmaku/test3.json"))
    _frame = 0
    while True:
        _frame += 1
        if _frame == 100:
            groupdict['enemy'].add(parser.load("assets/element/emix.json"))
        if _frame == 200:
            groupdict['enemy'].add(parser.load("assets/element/nmix.json"))
        if _frame == 300:
            groupdict['enemy'].add(parser.load("assets/element/hmix.json"))
        if _frame == 400:
            groupdict['enemy'].add(parser.load("assets/element/xmix.json"))

        G_all_sprites = pg.sprite.Group(
            *groupdict['danmaku'], *groupdict['player'], *groupdict['enemy'], *groupdict['bullet'])
        G_event_sprites = pg.sprite.Group(*groupdict['player'])

        for event in pg.event.get():
            G_event_sprites.update(event=event)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.WHITE)

        if pg.sprite.groupcollide(groupdict['player'], groupdict['danmaku'], False, False):
            print("Crashed")

        pg.sprite.groupcollide(groupdict['bullet'], groupdict['enemy'], False, True)

        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(ct.FPS)
