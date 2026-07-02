from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    nb_drones: int = 2
    start_hub: str = "start 0 0 [color=green]"
    hub_list: list[str] = ["hub: waypoint1 1 0 [color=blue]",
                           "hub: waypoint2 2 0 [color=blue]"]
    end_hub: str = "end_hub: goal 3 0 [color=red]"
    connection_list: list[str] = ["connection: start-waypoint1",
                                  "connection: waypoint1-waypoint2",
                                  "connection: waypoint2-goal"]
