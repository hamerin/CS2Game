from typing import Final, Tuple
import math

WIDTH: Final[int] = 768
HEIGHT: Final[int] = 576

WHITE: Final[Tuple[int, int, int]] = (255, 255, 255)
BLACK: Final[Tuple[int, int, int]] = (0, 0, 0)
RED: Final[Tuple[int, int, int]] = (140, 0, 0)
REDTRACK: Final[Tuple[int, int, int]] = (255, 0, 128)
GREEN: Final[Tuple[int, int, int]] = (0, 140, 0)
GREENTRACK: Final[Tuple[int, int, int]] = (0, 255, 0)
BLUE: Final[Tuple[int, int, int]] = (0, 0, 255)
BLUETRACK: Final[Tuple[int, int, int]] = (0, 175, 255)
#CYAN: Final[Tuple[int, int, int]] = (0, 255, 255)
#MAGENTA: Final[Tuple[int, int, int]] = (255, 0, 255)
#YELLOW: Final[Tuple[int, int, int]] = (255, 255, 0)

PI: Final[float] = math.pi
ELEMENTSIZE: Final[Tuple[int, int]] = (10, 10)
FPS: Final[int] = 60
