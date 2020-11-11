from typing import TypeVar, Optional, Generator

T = TypeVar('T')


def get_actual(opt: Optional[T]) -> T:
    if opt is None:
        raise ValueError

    actual: T = opt
    return actual


def get_uniform_dispersion(center: float, sep: float, N: int) -> Generator[float, None, None]:
    ret = center - sep * (N - 1) / 2

    for _ in range(N):
        yield ret
        ret += sep
