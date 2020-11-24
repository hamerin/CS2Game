from typing import Final, Tuple
import math

WIDTH: Final[int] = 512     #너비
HEIGHT: Final[int] = 768    #높이

WHITE: Final[Tuple[int, int, int]] = (255, 255, 255)        #색깔 지정
BLACK: Final[Tuple[int, int, int]] = (0, 0, 0)
RED: Final[Tuple[int, int, int]] = (255, 0, 0)
REDTRACK: Final[Tuple[int, int, int]] = (255, 0, 128)
GREEN: Final[Tuple[int, int, int]] = (0, 140, 0)
GREENTRACK: Final[Tuple[int, int, int]] = (0, 255, 0)
BLUE: Final[Tuple[int, int, int]] = (0, 0, 255)
BLUETRACK: Final[Tuple[int, int, int]] = (0, 175, 255)
YELLOW: Final[Tuple[int, int, int]] = (255, 240, 0)
GRAY: Final[Tuple[int, int, int]] = (150, 150, 150)

PI: Final[float] = math.pi      #3.1415
ELEMENTSIZE: Final[Tuple[int, int]] = (10, 10)      #객체 기본 크기
FPS: Final[int] = 60        #FPS

INITIALSCORE: Final[int] = 1000
PENALTY: Final[int] = 80
LIMITTIME: Final[float] = 80
LIMITREDUCE: Final[float] = 0.6
OVERLIMIT: Final[float] = 10
OVERTIME: Final[int] = 450  # 기타 상수

PATTERNDIR: Final[str] = 'assets'
AUDIODIR: Final[str] = 'audio'
SCOREDIR: Final[str] = 'scores'
