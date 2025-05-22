from collections.abc import Callable, Generator
from os import PathLike
from typing import Protocol


class Readable(Protocol):
    def read(self, size: int | None = ..., /) -> str: ...


type StrPath = str | PathLike[str]
type ChunkReader = Callable[[Readable], Generator[str]]
