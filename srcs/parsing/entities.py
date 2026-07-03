from dataclasses import dataclass, field
from abc import ABC
from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass(frozen=True)
class Hub(ABC):
    name: str
    coordinates: tuple[int, int]
    color: str | None = None
    zone: ZoneType = field(default=ZoneType.NORMAL)
    max_drones: int = field(default=1)
