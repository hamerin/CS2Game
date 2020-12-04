from __future__ import annotations
from inspect import signature, Parameter, _ParameterKind
from typing import Dict, Any, Tuple, Union, List, Final, TypeVar, Callable
from pathlib import Path
import re
import json
import random

import pygame as pg

from . import constant as ct
from .helpers.vector import Vector, parseVector
from .mover import VelocityMover, AccelerationMover, EventMover, TrackingMover
from .basedanmaku import BaseDanmaku, RadialBaseDanmaku, BurstBaseDanmaku, PlaneBaseDanmaku
from .image import BlockImage
from .element import Element
from .generator import Generator

T = TypeVar('T')


class Parser:
    """JSON 파일을 파싱하여 해당하는 객체를 반환한다.

    Attributes:
        screenrect: 최상위 Surface의 boundary box
        groupdict: 스프라이트 그룹을 포함하는 dict
        spritedict: 스프라이트를 포함하는 dict

    """
    allow = {"Gen": Generator,
             "Generator": Generator,
             "Radial": RadialBaseDanmaku,
             "Burst": BurstBaseDanmaku,
             "Plane": PlaneBaseDanmaku,
             "Velocity": VelocityMover,
             "Acceleration": AccelerationMover,
             "Event": EventMover,
             "Tracking": TrackingMover,
             "Block": BlockImage}

    def __init__(self,
                 screenrect: pg.rect.Rect,
                 groupdict: Dict[str, pg.sprite.Group],
                 spritedict: Dict[str, Element]):
        self.screenrect = screenrect
        self.groupdict = groupdict
        self.spritedict = spritedict

    def _parseRandom(self, mode: str) -> Vector:
        """랜덤 위치를 반환한다.

        mode의 값은
        'random',
        'rdleft', 'rdright', 'rdtop', 'rdbottom',
        'rdmidx', 'rdmidy'
        이 중 하나에 양쪽으로 언더스코어 두 개를 붙인 꼴이다.
        Ex) '__random__'

        Args:
            mode: 위치 모드

        Returns:
            mode에 따른 랜덤 위치 벡터

        Raises:
            ValueError: mode의 값이 위에 명시된 값이 아닐 경우

        """
        w = self.screenrect.width
        h = self.screenrect.height
        rx = random.randint(0, w)
        ry = random.randint(0, h)
        mx = w // 2
        my = h // 2

        if mode == 'random':
            return Vector(rx, ry)

        elif mode == 'rdleft':
            return Vector(0, ry)
        elif mode == 'rdright':
            return Vector(w, ry)
        elif mode == 'rdtop':
            return Vector(rx, 0)
        elif mode == 'rdbottom':
            return Vector(rx, h)

        elif mode == 'rdmidx':
            return Vector(mx, ry)
        elif mode == 'rdmidy':
            return Vector(rx, my)

        else:
            raise ValueError

    def _parseColor(self, data: Union[List[int], str]) -> Tuple[int, int, int]:
        """색상을 파싱하여 반환한다.

        data가 str인 경우, 다음 형식 중 하나여야 한다.
            constant.py에 정의된 색상 상수 이름 x에 대해, '__x__'꼴
                Ex) '__blue__'
            색상 코드 꼴
                Ex) '01abc2'

        data가 list일 경우, [0, 256)의 정수값을 담은 길이 3의 list여야한다.

        Args:
            data: 색상 데이터

        Returns:
            파싱된 색상 객체(길이 3의 tuple)

        Raises:
            TypeError: data의 type이 str이나 list가 아닐 경우
            ValueError: 위의 파싱 규칙에 해당되지 않는 경우

        """
        st: str
        ret: Tuple[int, int, int]

        if isinstance(data, str):
            if match := re.search(r'(?<=__).*(?=__)', data):
                st = match.group().upper()

                if not st in vars(ct):
                    raise ValueError
                if not isinstance(vars(ct)[st], tuple):
                    raise ValueError

                ret = vars(ct)[st]
                return ret

            if match := re.search(r'(?<=#)[0-9a-f]{6}', data):
                st = match.group()

                return(int(st[:2], 16),
                       int(st[2:4], 16),
                       int(st[4:], 16))

        elif isinstance(data, list):
            if len(data) != 3:
                raise ValueError
            if [*filter(lambda x: not isinstance(x, int), data)]:
                raise ValueError
            if [*filter(lambda x: x < 0 or x >= 256, data)]:
                raise ValueError

            return (data[0], data[1], data[2])

        else:
            raise TypeError

        raise ValueError

    def _parsePosition(self, data: Union[str, List[Union[int, float]]]) -> Vector:
        """위치를 파싱하여 반환한다.

        data가 str인 경우,
        'center',
        'topleft', 'bottomleft', 'topright', 'bottomright',
        'midtop', 'midleft', 'midbottom', 'midright',
        'random',
        'rdleft', 'rdright', 'rdtop', 'rdbottom',
        'rdmidx', 'rdmidy'
        이 중 하나에 양쪽으로 언더스코어 두 개를 붙인 꼴이다.
        Ex) __center__

        data가 list일 경우, 정수 혹은 실수를 포함하는 길이 2의 list여야한다.

        Args:
            data: 위치 데이터

        Returns:
            파싱된 2차원 위치 벡터

        Raises:
            TypeError: data의 type이 str이나 list가 아닐 경우
            ValueError: 위의 파싱 규칙에 해당되지 않는 경우

        """
        allow: Final[List[str]] = ['center',
                                   'topleft', 'bottomleft', 'topright', 'bottomright',
                                   'midtop', 'midleft', 'midbottom', 'midright']
        allow_rd: Final[List[str]] = ['random',
                                      'rdleft', 'rdright', 'rdtop', 'rdbottom',
                                      'rdmidx', 'rdmidy']

        st: str

        if isinstance(data, str):
            if match := re.search(r'(?<=__).*(?=__)', data):
                st = match.group().lower()

                if st in allow:
                    coor: Tuple[int, int] = getattr(self.screenrect, st)
                    return parseVector(coor)
                if st in allow_rd:
                    return self._parseRandom(st)

                raise ValueError

        elif isinstance(data, list):
            if len(data) != 2:
                raise ValueError
            if [*filter(lambda x: not isinstance(x, (int, float)), data)]:
                raise ValueError

            return parseVector((data[0], data[1]))

        else:
            raise TypeError

        raise ValueError

    def parse(self, data: Dict[str, Any]) -> Any:
        """dict 형태의 JSON 데이터를 파싱하여 반환한다.

        기본적으로 파싱할 객체의 signature를 runtime에 인식하여 자동으로 객체를 생성한다.
        data는 default값이 정의되어 있지 않은 argument의 이름을 모두 key로 가지고 있어야 한다.

        argument의 이름이 아닌 특수한 key값은 다음과 같다.
            '__type__': 필수. 반환할 객체의 type을 정의한다.
            '__wrap__': 정의되어 있을 경우 파싱된 객체를 반환하는 Callable를 반환한다.
            'args': *args의 값을 정의한다. 이때 value는 list형이어야 한다.
            'kwargs': **kwargs의 값을 정의한다. 이때 value는 dict형이어야 한다.

        특수한 value값은 다음과 같다.
            '__arg__': '__wrap__'이 정의되어 있을 경우, 반환될 Callable의 argument를 사용한다.

        Args:
            data: 파싱할 JSON 데이터

        Returns:
            파싱된 객체

        Raises:
            ValueError: 위의 파싱 규칙에 해당되지 않는 경우

        """
        if not '__type__' in data:
            raise ValueError
        if not data['__type__'] in self.allow:
            raise ValueError

        wrap: bool = False
        if '__wrap__' in data and data['__wrap__']:
            wrap = True

        elem = self.allow[data['__type__']]
        sig = signature(elem)

        args: List[Any] = list()
        kwargs: Dict[str, Any] = dict()
        for name in sig.parameters:
            tmp: Any
            param = sig.parameters[name]

            if param.kind == _ParameterKind.VAR_POSITIONAL:
                if "args" in data:
                    data_args: List[Any] = data["args"]
                    args += data_args

            elif param.kind == _ParameterKind.VAR_KEYWORD:
                if "kwargs" in data:
                    data_kwargs: Dict[str, Any] = data["kwargs"]
                    kwargs.update(data_kwargs)

            else:
                if param.default == Parameter.empty:
                    if not name in data:
                        raise ValueError

                if not name in data:
                    continue

                tmp = data[name]

                if tmp == "__arg__":
                    continue

                if isinstance(tmp, dict) and "__type__" in tmp:
                    tmp = self.parse(tmp)

                if elem == Generator and name in ("danmaku",):
                    def parseBase(data: Dict[str, Any]) -> Tuple[int, Callable[[Tuple[int, int]], BaseDanmaku]]:
                        if not "refresh" in data:
                            raise ValueError

                        ref: int = data["refresh"]
                        gen: Callable[[Tuple[int, int]],
                                      BaseDanmaku] = self.parse(data)
                        return (ref, gen)

                    tmp = [*map(parseBase, tmp)]

                if name in ("direction",):
                    tmp *= ct.PI

                if param.annotation in ("pg.sprite.Group",):
                    if not tmp in self.groupdict:
                        raise ValueError
                    tmp = self.groupdict[tmp]
                if param.annotation in ("Element", "Optional[Element]"):
                    if not tmp in self.spritedict:
                        raise ValueError
                    tmp = self.spritedict[tmp]

                if param.annotation in ("Coordinate",):
                    tmp = self._parsePosition(tmp)
                if param.annotation in ("Tuple[int, int, int]",):
                    tmp = self._parseColor(tmp)

                if param.default == Parameter.empty:
                    args.append(tmp)
                else:
                    kwargs.update({name: tmp})

        if not wrap:
            return elem(*args, **kwargs)
        else:
            def ret(*wrap_args: Any) -> Any:
                return elem(*wrap_args, *args, **kwargs)
            return ret

    def load(self, rel_path: str) -> Any:
        """상대 경로에 정의되어 있는 json 확장자의 파일을 읽어서 파싱한다.

        Args:
            rel_path: json 파일의 상대 경로

        Returns:
            파싱된 객체

        """
        path: Path = Path.cwd() / rel_path

        ret: Any = None
        with path.open() as f:
            ret = self.parse(json.loads(f.read()))

        return ret
