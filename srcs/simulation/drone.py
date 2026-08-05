from dataclasses import dataclass

from srcs.parsing.entities import Hub


@dataclass(slots=True)
class Drone:
    id: str
    current_position: Hub
    goal_reached: bool
    has_moved_this_turn: bool
    in_transit: bool = False
