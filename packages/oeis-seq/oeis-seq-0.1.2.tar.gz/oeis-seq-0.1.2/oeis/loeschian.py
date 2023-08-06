# coding=utf-8
from typing import Iterable
from math import sqrt
from itertools import count
from oeis.registry import registry


@registry.register("A003136")
def loeschian() -> Iterable[int]:
    def is_loeschian(n: int) -> bool:
        if n in [0, 1, 3]:
            return True
        if n % 3 == 2:
            return False
        M: int = 2 * round(sqrt(n / 3))
        for x in range(0, M + 1):
            for y in range(0, x + 1):
                if n == (x ** 2) + (x * y) + (y ** 2):
                    return True
        return False

    for n in count(start=0):
        if is_loeschian(n):
            yield n
