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
from .parser import Parser  # 보조 함수들 불러오기

def prompt_difficulty() -> str:  # 난이도 입력(한글자)
    _allow: List[str] = ['e', 'easy', 'n', 'normal', 'h', 'hard', 'i', 'insane', 'x', 'extra']
    inp = input("select difficulty /n e: easy  n: normal  h: hard  i: insane  x: extra /n Difficulty: ")

    if not inp in _allow:  # 다른 글자 들어오면 에러
        raise ValueError
    idx = _allow.index(inp)
    if idx % 2 == 0:
        idx += 1

    return _allow[idx]

def game() -> None:  # 본체
    diff = prompt_difficulty()  # 난이도 불러오기
    pg.init()  # 초기화

    pg.display.set_caption('막장 피하기 슈팅')  # 제목
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)  # 게임 크기 설정
    clock = pg.time.Clock()  # 시간 설정

    screenrect = displaysurf.get_rect()  # 게임 영역 설정

    groupdict: Dict[str, pg.sprite.Group] = dict()  # 그룹 불러오기
    groupdict = {'bullet': pg.sprite.Group(),
                 'player': pg.sprite.Group(),
                 'enemy': pg.sprite.Group(),
                 'danmaku': pg.sprite.Group()}

    spritedict: Dict[str, Element] = dict()

    parser = Parser(screenrect, groupdict, spritedict)  # 패턴 구문분석
    spritedict['player'] = parser.load("assets/player.json")

    groupdict['player'].add(spritedict['player'])  #플레이어 추가

    def enemychoose():  # 랜덤 적 생성기
        nn = random.randrange(21)   # 경우 별 출현 적
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
    _frame , _crashed, _limittime, onon = 0 , 0, 80, 0  # 변수 결정

    while True:  # 게임 구동기
        _frame += 1  # 시간 증가
        if _frame == _limittime // 1 and onon == 0:  # 게임 중 적 생성 시간일 때
            enemychoose()  # 적 생성
            _frame = 0  # 적 생성 시간 초기화
            print(_limittime)
            if _limittime > 10: _limittime -= 0.7  # 적 생성 주기 단축
            if _limittime <= 10: onon = 1  # 게임 종료 시간

        if onon == 1:  # 게임 끝
            if _frame == 450:
                pg.quit()
                sys.exit()

        G_all_sprites = pg.sprite.Group(
            *groupdict['danmaku'], *groupdict['player'], *groupdict['enemy'], *groupdict['bullet'])
        G_event_sprites = pg.sprite.Group(*groupdict['player'])

        for event in pg.event.get():
            G_event_sprites.update(event=event)  # 객체 위치 이동
            if event.type == pg.QUIT:  # 종료 버튼
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.WHITE)  # 배경 색

        if pg.sprite.groupcollide(groupdict['player'], groupdict['danmaku'], False, False):
            _crashed += 1  # 부딫혔을 때 충돌 카운트 +1
            print(f"Crashed {_crashed} times")

        pg.sprite.groupcollide(groupdict['bullet'], groupdict['enemy'], False, True)  # 쏜 총이 적 맞았을 때 적 kill

        G_all_sprites.update()  # 모든 객체 위치 업데이트
        G_all_sprites.draw(displaysurf)

        pg.display.update()
        clock.tick(ct.FPS)  # 시간 업데이트