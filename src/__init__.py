import sys
import json
import random
import copy
from pathlib import Path
from typing import Final, Tuple, Dict, List, Any

import pygame as pg

from . import constant as ct
from .element import Element
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .image import BlockImage
from .parser import Parser  # 보조 함수들 불러오기


def prompt_difficulty() -> str:  # 난이도 입력(한글자)
    allow: List[str] = ['e', 'easy', 'n', 'normal',
                        'h', 'hard', 'i', 'insane', 'x', 'extra']
    inp = input(
        'select difficulty\ne: easy  n: normal  h: hard  i: insane  x: extra\nDifficulty: ')

    if not inp in allow:  # 다른 글자 들어오면 에러
        raise ValueError

    idx = allow.index(inp)
    if idx % 2 == 0:
        idx += 1

    return allow[idx]


def _loadfiles(diff: str) -> Dict[str, Dict[str, Any]]:
    patterndir = Path.cwd() / ct.PATTERNDIR / diff

    ret: Dict[str, Any] = dict()
    for path in patterndir.iterdir():
        with path.open() as f:
            ret[path.stem] = json.loads(f.read())

    return ret


def _loadsounds() -> Dict[str, pg.mixer.Sound]:
    audiodir: Path = Path.cwd() / ct.AUDIODIR

    ret: Dict[str, pg.mixer.Sound] = dict()
    for path in audiodir.iterdir():
        ret[path.stem] = pg.mixer.Sound(path.open())

    return ret


def _enemychoose(enemygroup: pg.sprite.Group, parser: Parser,
                 loadeddict: Dict[str, Dict[str, Any]]) -> None:
    def _add(*args: str) -> None:
        for st in args:
            enemygroup.add(parser.parse(loadeddict[st]))

    rn: int = random.randrange(21)

    if rn == 0:
        _add('mix')
    if 1 <= rn <= 3:
        _add('burst')
    if 4 <= rn <= 6:
        _add('plane')
    if 7 <= rn <= 9:
        _add('radial')
    if 10 <= rn <= 11:
        _add('burst_follow')
    if 12 <= rn <= 13:
        _add('plane_follow')
    if 14 <= rn <= 15:
        _add('radial_follow')
    if rn == 16:
        _add('burst', 'radial')
    if rn == 17:
        _add('burst', 'plane')
    if rn == 18:
        _add('plane', 'radial')
    if rn == 19:
        _add('burst', 'plane', 'radial')


def game() -> None:  # 본체
    diff = prompt_difficulty()  # 난이도 불러오기

    pg.init()  # 초기화
    pg.mixer.init()

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

    spritedict['player'] = parser.load('assets/player.json')
    groupdict['player'].add(spritedict['player'])  # 플레이어 추가

    loadeddict = _loadfiles(diff)  # 패턴 파일 로드
    sounddict = _loadsounds()

    _frame: int = 0
    frame: int = 0
    score: int = 0
    limittime: float = ct.LIMITTIME
    onon: int = 0  # 변수 결정

    pg.mixer.Sound.play(sounddict['bgm'])

    while True:  # 게임 구동기
        _frame += 1  # 시간 증가
        frame += 1

        if frame == limittime // 1 and onon == 0:  # 게임 중 적 생성 시간일 때
            _enemychoose(groupdict['enemy'], parser, loadeddict)  # 적 생성
            frame = 0  # 적 생성 시간 초기화
            if limittime > ct.OVERLIMIT:
                limittime -= ct.LIMITREDUCE  # 적 생성 주기 단축
            else:
                onon = 1  # 게임 종료 시간

        if onon == 1:  # 게임 끝
            if frame == ct.OVERTIME:
                print(f"FINAL SCORE: {-score}")
                pg.quit()
                sys.exit()

        for event in pg.event.get():
            groupdict['player'].update(event=event)  # 객체 위치 이동
            if event.type == pg.QUIT:  # 종료 버튼
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.WHITE)  # 배경 색
        if pg.sprite.groupcollide(groupdict['player'], groupdict['danmaku'], False, False):
            score += 1  # 부딫혔을 때 충돌 카운트 +1
            pg.mixer.Sound.play(sounddict['gothit'])

        # 쏜 총이 적 맞았을 때 적 kill
        pg.sprite.groupcollide(groupdict['bullet'], groupdict['enemy'],
                               False, True)

        enemyn = len(groupdict['enemy'])
        for key in groupdict:
            groupdict[key].update()  # 모든 객체 위치 업데이트
            groupdict[key].draw(displaysurf)
        score += ct.PENALTY * (enemyn - len(groupdict['enemy']))

        if _frame % 60 == 0:
            print(f"Score: {-score}")
        pg.display.update()
        clock.tick(ct.FPS)  # 시간 업데이트
