from srcs.parsing.entities import Map
from srcs.simulation.drone import Drone


class GameState:
    def __init__(self, turn: int, game_map: Map) -> None:
        self.turn = turn
        self.game_map = game_map
        self.drones: list[Drone] = []
        self.first_setup()

    def first_setup(self) -> None:
        for drone in range(1, self.game_map.nb_drones + 1):
            self.drones.append(Drone(
                id=f"D{drone}",
                current_position=self.game_map.start_hub,
                goal_reached=False,
                in_transit=False
            ))
