# coding=utf-8
from typing import Iterable
from itertools import count
from oeis.registry import registry


@registry.register(identifier="A100702")
def buttered_croissant() -> Iterable[int]:
    yield 1  # special case
    for i in count(start=1):
        yield 1 + 2 * pow(3, i - 1)
