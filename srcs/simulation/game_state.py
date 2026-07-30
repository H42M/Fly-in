from srcs.parsing.entities import Map
from srcs.simulation.drone import Drone


class GameState:
    def __init__(self, turn: int, game_map: Map, drones: list[Drone]) -> None:
        self.turn = turn
        self.game_map = game_map
        self.drones = drones
