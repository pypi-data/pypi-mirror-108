from typing import Callable, Dict, Iterable, TypeVar, Generic

T = TypeVar("T", bound=Callable[[], Iterable[int]])


class OEISRegistry(Generic[T]):
    def __init__(self) -> None:
        self.sequences: Dict[str, T] = {}

    def __getitem__(self, identifier: str) -> T:
        return self.sequences[identifier]

    def add(self, identifier: str, func: T) -> None:
        self.sequences[identifier] = func

    def register(self, identifier: str) -> Callable[[T], T]:
        def wrapper(func: T) -> T:
            self.sequences[identifier] = func
            return func

        return wrapper


registry = OEISRegistry[Callable[[], Iterable[int]]]()

__all__ = [
    "registry",
    "OEISRegistry",
]
