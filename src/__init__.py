import os
import sys
import json
from typing import Final, Tuple, Dict, List

import random

import pygame as pg
from . import constant as ct
from .element import Element
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .image import BlockImage
from .parser import Parser

def prompt_difficulty() -> str:
    _allow: List[str] = ['e', 'easy', 'n', 'normal', 'h', 'hard', 'i', 'insane', 'x', 'extra']
    inp = input("select difficulty /n e: easy  n: normal  h: hard  i: insane  x: extra /n Difficulty: ")

    if not inp in _allow:
        raise ValueError
    idx = _allow.index(inp)
    if idx % 2 == 0:
        idx += 1

    return _allow[idx]

def game() -> None:
    diff = prompt_difficulty()
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
    spritedict['player'] = parser.load("assets/player.json")

    groupdict['player'].add(spritedict['player'])

    def enemychoose():
        nn = random.randrange(21)
        if nn == 0: groupdict['enemy'].add(parser.load(f"assets/{diff}/mix.json"))
        if 1 <= nn and nn <= 3: groupdict['enemy'].add(parser.load(f"assets/{diff}/burst.json"))
        if 4 <= nn and nn <= 6: groupdict['enemy'].add(parser.load(f"assets/{diff}/plane.json"))
        if 7 <= nn and nn <= 9: groupdict['enemy'].add(parser.load(f"assets/{diff}/radial.json"))
        if nn // 2 == 5: groupdict['enemy'].add(parser.load(f"assets/{diff}/burst_follow.json"))
        if nn // 2 == 6: groupdict['enemy'].add(parser.load(f"assets/{diff}/plane_follow.json"))
        if nn // 2 == 7: groupdict['enemy'].add(parser.load(f"assets/{diff}/radial_follow.json"))
        if nn == 16: groupdict['enemy'].add(parser.load(f"assets/{diff}/burst.json")); groupdict['enemy'].add(
            parser.load(f"assets/{diff}/radial.json"))
        if nn == 17: groupdict['enemy'].add(parser.load(f"assets/{diff}/burst.json")); groupdict['enemy'].add(
            parser.load(f"assets/{diff}/plane.json"))
        if nn == 18: groupdict['enemy'].add(parser.load(f"assets/{diff}/plane.json")); groupdict['enemy'].add(
            parser.load(f"assets/{diff}/radial.json"))
        if nn == 19: pass
        if nn == 20:
            groupdict['enemy'].add(parser.load(f"assets/{diff}/burst.json"))
            groupdict['enemy'].add(parser.load(f"assets/{diff}/plane.json"))
            groupdict['enemy'].add(parser.load(f"assets/{diff}/radial.json"))
    _frame , _crashed, _limittime = 0 , 0, 90

    while True:
        _frame += 1
        if _frame == _limittime//1:
            enemychoose()
            _limittime-=0.7
            _frame=0
            print(_limittime)
        if _limittime < 0:
            if _frame > 300:
                #게임 종료 후 점수 기록

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
            _crashed += 1
            print(f"Crashed {_crashed} times")

        pg.sprite.groupcollide(
            groupdict['bullet'], groupdict['enemy'], False, True)

        G_all_sprites.update()
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(ct.FPS)