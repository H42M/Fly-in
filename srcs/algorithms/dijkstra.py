from math import inf
import heapq

from srcs.parsing.entities import Map


def algo(map: Map) -> None:
    hubs = [map.start_hub, *map.hubs]
    distances: dict[str, float] = {hub.name: inf for hub in hubs}
    distances[map.end_hub.name] = 0

    processed: list[str] = []
    frontier: list[tuple[float, str]] = [(0, map.end_hub.name),]
    not_discovered = hubs.copy()
    del hubs
