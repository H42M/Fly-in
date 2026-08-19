from dataclasses import dataclass, field
from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    GOAL = "goal"


@dataclass(frozen=True)
class Hub:
    name: str
    coordinates: tuple[int, int]
    color: str | None = None
    zone: ZoneType = field(default=ZoneType.NORMAL)
    max_drones: int | None = field(default=1)


@dataclass(frozen=True)
class Connection:
    name1: str
    name2: str
    max_link_capacity: int = 1

    def connects(self, name1: str, name2: str) -> bool:
        return (
            self.name1 == name1 and self.name2 == name2
        ) or (
            self.name1 == name2 and self.name2 == name1
        )

    def other_end(self, hub_name: str) -> str:
        if hub_name == self.name1:
            return self.name2
        if hub_name == self.name2:
            return self.name1
        raise ValueError(f"{hub_name} is not part of this connection")

    @property
    def name(self) -> str:
        return f"{self.name1}-{self.name2}"


@dataclass(frozen=True, slots=True)
class Map:
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    end_hub: Hub
    connections: list[Connection]
    neighbours: dict[str, list[Connection]]
    hub_name_lookup: dict[str, Hub]

    def get_connection(self, name1: str, name2: str) -> Connection:
        for connection in self.connections:
            if connection.connects(name1, name2):
                return connection
        raise ValueError(f"No connection between {name1} and {name2}")
