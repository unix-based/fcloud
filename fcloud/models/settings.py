from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from .driver import Driver

# Data received from the user that Fire
# can convert to another data type
# `script 1.1 hello` -> handler(float, str)
UserArgument = TypeVar("UserArgument", str, int, float)


@dataclass(frozen=True)
class Config:
    service: Driver
    main_folder: Path
    cfl_extension: str


@dataclass
class CloudObj:
    name: str
    size: int | None
    is_directory: bool
    modifed: str | None
