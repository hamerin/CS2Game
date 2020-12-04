from typing import TypeVar, Optional, Generator

import pygame as pg

T = TypeVar('T')


def get_actual(opt: Optional[T]) -> T:
    """Optional 변수의 실제 값을 반환한다.

    Args:
        opt: Optional 변수.

    Returns:
        opt의 실제 값.

    Raises:
         ValueError: opt is None일 경우

    """
    if opt is None:
        raise ValueError

    actual: T = opt
    return actual


def get_uniform_dispersion(center: float, sep: float, N: int) -> Generator[float, None, None]:
    """수의 균등 분포를 반환한다.

    Args:
        center: 수의 평균
        sep: 수의 간격
        N: 수의 개수

    Yields:
        균등 분포의 첫째 수부터 차례로 반환한다.

    """
    ret = center - sep * (N - 1) / 2

    for _ in range(N):
        yield ret
        ret += sep
