import sys
import json
import random
import copy
import pickle
from pathlib import Path
from typing import Final, Tuple, Dict, List, Any

import pygame as pg

from . import constant as ct
from .element import Element
from .mover import AccelerationMover, EventMover
from .basedanmaku import RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .image import BlockImage
from .helpers.vector import Coordinate, parseVector, Vector
from .parser import Parser  # 보조 함수들 불러오기


def _loadfiles(diff: str) -> Dict[str, Dict[str, Any]]:
    patterndir = Path.cwd() / ct.PATTERNDIR / diff

    ret: Dict[str, Any] = dict()
    for path in patterndir.iterdir():
        with path.open() as f:
            ret[path.stem] = json.loads(f.read())  # 파일 불러오기

    return ret


def _loadsounds() -> Dict[str, pg.mixer.Sound]:
    audiodir: Path = Path.cwd() / ct.AUDIODIR

    ret: Dict[str, pg.mixer.Sound] = dict()
    for path in audiodir.iterdir():
        ret[path.stem] = pg.mixer.Sound(path.open())  # 소리 불러오기

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
        _add('burst', 'plane', 'radial')  # 적 고르기


def _write_text(screen: pg.surface.Surface, size: int, pos: Coordinate,
                text: str, color: Tuple[int, int, int]) -> None:
    font = pg.font.SysFont(pg.font.get_default_font(), size)

    textsurf = font.render(text, True, color)
    screen.blit(textsurf, parseVector(pos).as_trimmed_tuple())


def _write_text_ct(screen: pg.surface.Surface, size: int, pos: Coordinate,
                   text: str, color: Tuple[int, int, int]) -> None:
    font = pg.font.SysFont(pg.font.get_default_font(), size)

    textsurf = font.render(text, True, color)

    blit_pos = parseVector(pos) - Vector(*textsurf.get_size()) / 2
    screen.blit(textsurf, blit_pos.as_trimmed_tuple())


def _write_text_rt(screen: pg.surface.Surface, size: int, pos: Coordinate,
                   text: str, color: Tuple[int, int, int]) -> None:
    font = pg.font.SysFont(pg.font.get_default_font(), size)

    textsurf = font.render(text, True, color)

    blit_pos = parseVector(pos) - Vector(textsurf.get_width(), 0)
    screen.blit(textsurf, blit_pos.as_trimmed_tuple())


def init() -> Tuple[pg.surface.Surface, pg.time.Clock]:
    pg.init()  # 초기화

    pg.display.set_caption('막장 피하기&슈팅')  # 제목
    displaysurf = pg.display.set_mode((ct.WIDTH, ct.HEIGHT), 0, 32)  # 게임 크기 설정
    clock = pg.time.Clock()  # 시간 설정

    return displaysurf, clock


# 난이도 입력(한글자)
def prompt_difficulty(displaysurf: pg.surface.Surface, clock: pg.time.Clock) -> Tuple[str, Tuple[int, int, int]]:
    allow: Dict[int, Tuple[str, Tuple[int, int, int]]] = {ord('e'): ('easy', ct.BLUETRACK),
                                                          ord('n'): ('normal', ct.GREENTRACK),
                                                          ord('h'): ('hard', ct.YELLOW),
                                                          ord('i'): ('insane', ct.REDTRACK),
                                                          ord('x'): ('extra', ct.RED)}

    _write_text_ct(displaysurf, 60, (ct.WIDTH / 2, ct.HEIGHT * 0.15),
                   'Select difficulty', ct.WHITE)

    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.3),
                   'e: easy', ct.BLUETRACK)
    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.4),
                   'n: normal', ct.GREENTRACK)
    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.5),
                   'h: hard', ct.YELLOW)
    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.6),
                   'i: insane', ct.REDTRACK)
    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.7),
                   'x: extra', ct.RED)

    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.85),
                   'q: quit', ct.WHITE)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT\
               or (event.type == pg.KEYDOWN and event.key == ord('q')):  # 종료
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key in allow:
                return allow[event.key]

        pg.display.update()
        clock.tick(ct.FPS)


# 본체
def game(displaysurf: pg.surface.Surface, clock: pg.time.Clock) -> Tuple[str, Tuple[int, int, int], int]:
    diff, diff_color = prompt_difficulty(displaysurf, clock)  # 난이도 불러오기

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
    score: int = ct.INITIALSCORE
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
                return diff, diff_color, score

        for event in pg.event.get():
            groupdict['player'].update(event=event)  # 객체 위치 이동
            if event.type == pg.QUIT:  # 종료 버튼
                pg.quit()
                sys.exit()

        displaysurf.fill(ct.BLACK)  # 배경 색
        if pg.sprite.groupcollide(groupdict['player'], groupdict['danmaku'], False, False):
            score -= 1  # 부딫혔을 때 충돌 카운트 +1
            pg.mixer.Sound.play(sounddict['gothit'])

        # 쏜 총이 적 맞았을 때 적 kill
        pg.sprite.groupcollide(groupdict['bullet'], groupdict['enemy'],
                               False, True)

        enemyn = len(groupdict['enemy'])
        for key in groupdict:
            groupdict[key].update()  # 모든 객체 위치 업데이트
            groupdict[key].draw(displaysurf)
        # 적이 자연적으로 죽을 경우 페널티
        score -= ct.PENALTY * (enemyn - len(groupdict['enemy']))

        _write_text(displaysurf, 60, (20, 20),
                    f"{score}", ct.WHITE)
        _write_text_rt(displaysurf, 60, (ct.WIDTH-20, 20),
                       diff, diff_color)

        pg.display.update()
        clock.tick(ct.FPS)  # 시간 업데이트


def result(displaysurf: pg.surface.Surface, clock: pg.time.Clock,
           diff: str, diff_color: Tuple[int, int, int], score: int) -> None:
    scorefile: Path = Path.cwd() / ct.SCOREDIR / f"{diff}.pkl"

    scores: List[int] = []

    try:
        scores = pickle.load(scorefile.open("rb"))
    except FileNotFoundError:
        pass

    scores.append(score)
    scores.sort()
    scores.reverse()
    scores = scores[:5]

    pickle.dump(scores, scorefile.open("wb"))

    displaysurf.fill(ct.BLACK)
    _write_text_ct(displaysurf, 60, (ct.WIDTH / 2, ct.HEIGHT * 0.15),
                   f'Score ({diff})', diff_color)

    for i, sco in enumerate(scores):
        _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * (0.3 + 0.1*i)),
                       f'{i + 1}. {sco}', ct.WHITE)

    _write_text_ct(displaysurf, 40, (ct.WIDTH / 2, ct.HEIGHT * 0.85),
                   f'Your score: {score}', ct.WHITE)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT\
               or (event.type == pg.KEYDOWN and event.key == ord('q')):  # 종료
                pg.quit()
                sys.exit()

        pg.display.update()
        clock.tick(ct.FPS)
