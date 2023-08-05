# coding=utf-8
from typing import Iterable
from itertools import count
from .registry import registry


@registry.register("A003261")
def woodall() -> Iterable[int]:
    for n in count(start=1):
        yield n * (2 ** n) - 1
