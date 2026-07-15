from dataclasses import dataclass, field
from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass(frozen=True)
class Hub:
    name: str
    coordinates: tuple[int, int]
    color: str | None = None
    zone: ZoneType = field(default=ZoneType.NORMAL)
    max_drones: int = field(default=1)


@dataclass(frozen=True)
class Connection:
    name1: str
    name2: str
    max_link_capacity: int = 1


@dataclass(frozen=True, slots=True)
class Map:
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    end_hub: Hub
    connections: list[Connection]
