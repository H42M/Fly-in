from dataclasses import dataclass
from math import inf

from srcs.simulation.game_state import GameState
from srcs.simulation.drone import Drone
from srcs.algorithms.dijkstra import algo
from srcs.parsing.entities import ZoneType, Hub


@dataclass
class Engine:
    game_state: GameState

    def drones_traveling(self) -> bool:
        drones = self.game_state.drones
        for drone in drones:
            if not drone.goal_reached:
                return True
        return False

    def hub_neighbours_names(self) -> dict[str, list[str]]:
        hub_neighbours_names: dict[str, list[str]] = {}
        game_map = self.game_state.game_map
        for hub_name, neighbours in game_map.neighbours.items():
            neighbour_ids: list[str] = []
            for n in neighbours:
                if n.name1 != hub_name:
                    neighbour_ids.append(n.name1)
                else:
                    neighbour_ids.append(n.name2)
            hub_neighbours_names[hub_name] = neighbour_ids
        return hub_neighbours_names

    def get_next_destination(
            self, drone: Drone, distances: dict[str, float]) -> Hub:
        game_map = self.game_state.game_map
        hnb = self.hub_neighbours_names()
        neighbours = hnb[drone.current_position.name]
        best_destination = inf
        best_candidate = ""
        for destination in neighbours:
            candidate_dist = distances[destination]
            if candidate_dist < best_destination:
                best_destination = candidate_dist
                best_candidate = destination
        return game_map.hub_name_lookup[best_candidate]

    def move_drone(self, drone: Drone, distances: dict[str, float]) -> None:
        game_map = self.game_state.game_map
        next_destination = self.get_next_destination(drone, distances)
        drone.current_position = next_destination
        if drone.current_position == game_map.end_hub:
            drone.goal_reached = True

    def run_simulation(self) -> None:
        drones = self.game_state.drones
        state = self.game_state
        distances = algo(state.game_map)

        while self.drones_traveling():
            for drone in drones:
                next_destination = self.get_next_destination(drone, distances)

                if drone.in_transit:
                    drone.in_transit = False
                    self.move_drone(drone, distances)
                    continue

                if next_destination.zone == ZoneType.RESTRICTED:
                    drone.in_transit = True
                    continue
                if not drone.goal_reached:
                    self.move_drone(drone, distances)

            state.turn += 1
