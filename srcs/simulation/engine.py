from dataclasses import dataclass
from math import inf

from srcs.simulation.game_state import GameState
from srcs.simulation.drone import Drone
from srcs.algorithms.dijkstra import algo
from srcs.parsing.entities import ZoneType, Hub, Connection


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

    def above_max_drones(self, best_candidate: Hub) -> bool:
        drones = self.game_state.drones
        max_drones = best_candidate.max_drones
        if not max_drones:
            return False
        counter = 0
        for drone in drones:
            if (
                drone.has_moved_this_turn and
                drone.current_position == best_candidate
            ):
                counter += 1
        if counter >= max_drones:
            return True
        return False

    def get_next_destination(
            self, drone: Drone, distances: dict[str, float]) -> Hub:
        game_map = self.game_state.game_map
        hnb = self.hub_neighbours_names()
        hnl = game_map.hub_name_lookup
        neighbours = hnb[drone.current_position.name]
        best_possible_distance = inf
        best_available_distance = inf
        best_possible_route = neighbours[0]
        best_available_route: str | None = None

        for destination in neighbours:
            priority: bool = False
            destination_hub = hnl[destination]
            if destination_hub.zone == ZoneType.GOAL:
                return destination_hub
            if destination_hub.zone == ZoneType.PRIORITY:
                priority = True
            candidate_dist = distances[destination]

            if candidate_dist == best_possible_distance and priority:
                best_possible_route = destination
                best_possible_distance = candidate_dist
            if candidate_dist < best_possible_distance:
                best_possible_route = destination
                best_possible_distance = candidate_dist

            if (
                candidate_dist < best_available_distance and
                destination_hub.zone != ZoneType.RESTRICTED
                and not self.above_max_drones(destination_hub)
            ):
                best_available_route = destination
                best_available_distance = candidate_dist
            if (
                candidate_dist == best_available_distance and
                priority
                and not self.above_max_drones(destination_hub)
            ):
                best_available_route = destination
                best_available_distance = candidate_dist
        if (
            best_available_route is not None
            and best_available_distance <= best_possible_distance
        ):
            return game_map.hub_name_lookup[best_available_route]
        return game_map.hub_name_lookup[best_possible_route]

    def move_drone(self, drone: Drone, distances: dict[str, float]) -> None:
        game_map = self.game_state.game_map
        next_destination = self.get_next_destination(drone, distances)
        drone.current_position = next_destination
        drone.has_moved_this_turn = True
        if drone.current_position == game_map.end_hub:
            drone.goal_reached = True

    def run_simulation(self) -> None:
        print(self.display_turn())

        while self.drones_traveling():
            self.run_turn()
            print(self.display_turn())

    def run_turn(self) -> None:
        drones = self.game_state.drones
        state = self.game_state
        distances = algo(state.game_map)

        for drone in drones:
            drone.has_moved_this_turn = False
        connection_capacities: dict[Connection, int] = {}
        for con in self.game_state.game_map.connections:
            connection_capacities[con] = 0
        for drone in drones:
            if drone.goal_reached:
                continue
            if drone.in_transit:
                drone.in_transit = False
                drone.traveling_to_restricted = None
                self.move_drone(drone, distances)
                continue

            next_destination = self.get_next_destination(drone, distances)
            if next_destination.max_drones:
                counter = 0
                for d in drones:
                    if (
                        d.current_position == next_destination
                        and not d.in_transit
                    ):
                        counter += 1
                if (
                    counter >= next_destination.max_drones
                    and next_destination.zone != ZoneType.RESTRICTED
                ):
                    continue

            connections = state.game_map.neighbours[next_destination.name]
            connection: Connection | None = None
            for c in connections:
                if (
                    (
                        c.name1 == drone.current_position.name and
                        c.name2 == next_destination.name
                    )
                    or (
                        c.name2 == drone.current_position.name and
                        c.name1 == next_destination.name
                    )
                ):
                    connection = c
            if not connection:
                continue

            if (
                connection_capacities[connection] >=
                connection.max_link_capacity
            ):
                continue

            if next_destination.zone == ZoneType.RESTRICTED:
                t_counter = 0
                for d_t in drones:
                    if d_t.traveling_to_restricted == next_destination:
                        t_counter += 1
                if (
                    next_destination.max_drones is not None and
                    t_counter >= next_destination.max_drones
                ):
                    continue
                drone.in_transit = True
                drone.traveling_to_restricted = next_destination
                connection_capacities[connection] += 1
                continue
            if not drone.goal_reached:
                self.move_drone(drone, distances)
                connection_capacities[connection] += 1

        state.turn += 1
        print(self.display_turn())

    def display_turn(self) -> str:
        cons = self.game_state.game_map.connections
        
        drones = "".join(
            f"{drone.id}-"
            f"{f'{drone.traveling_to_restricted.name}'
               if drone.traveling_to_restricted is not None
               else drone.current_position.name} "
            for drone in self.game_state.drones
        )

        return f"{drones}"
