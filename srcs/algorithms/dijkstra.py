from math import inf
import heapq

from srcs.parsing.entities import Map, Hub, ZoneType


def find_hub(map: Map, hub_name: str) -> Hub | None:
    for hub in [map.start_hub, *map.hubs, map.end_hub]:
        if hub.name == hub_name:
            return hub
    return None


def algo(map: Map) -> dict[str, float]:
    hubs = [map.start_hub, *map.hubs]
    distances: dict[str, float] = {hub.name: inf for hub in hubs}
    distances[map.end_hub.name] = 0

    processed: list[str] = []
    frontier: list[tuple[float, str]] = [
        (0, map.end_hub.name),
    ]
    not_discovered = hubs.copy()
    del hubs

    while frontier:
        current_distance, current_name = heapq.heappop(frontier)

        if distances[current_name] < current_distance:
            continue

        candidates = map.neighbours[current_name]
        c_distances: dict[str, float] = {}
        hub = find_hub(map, current_name)

        for c in candidates:
            if c.name1 == current_name:
                c_name = c.name2
            else:
                c_name = c.name1

            if hub is None:
                continue

            candidate_hub = find_hub(map, c_name)

            if not candidate_hub:
                continue

            if candidate_hub.zone == ZoneType.BLOCKED:
                continue
            elif hub.zone == ZoneType.RESTRICTED:
                c_distances[c_name] = current_distance + 2
            else:
                c_distances[c_name] = current_distance + 1

        for can_name in c_distances:
            if distances[can_name] > c_distances[can_name]:
                distances[can_name] = c_distances[can_name]
                heapq.heappush(
                    frontier,
                    (distances[can_name], can_name),
                )

        processed.append(current_name)

        if hub in not_discovered:
            not_discovered.remove(hub)

    return distances
