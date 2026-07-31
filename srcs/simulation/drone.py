from dataclasses import dataclass

from srcs.parsing.entities import Hub


@dataclass(slots=True)
class Drone:
    id: str
    current_position: Hub
    goal_reached: bool
    in_transit: bool = False
