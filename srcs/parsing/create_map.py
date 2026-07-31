from __future__ import annotations
from typing import Any
from srcs.parsing.entities import Map, Hub, Connection, ZoneType
from srcs.parsing.input_parser import parse_input


def create_hub(hub_data: str, special_case: bool) -> Hub:
    if not hub_data:
        raise ValueError("Missing hub data.")
    if "[" not in hub_data:
        metadata = ""
        standard_data = hub_data

    else:
        data = hub_data.split("[", 1)
        standard_data = data[0]
        metadata = data[1].removesuffix("]")

    data_items = standard_data.split()
    name = data_items[0]
    coordinates = (int(data_items[1]), int(data_items[2]))
    color = None
    zone = None
    max_drones = None

    for item in metadata.split():
        if item.startswith("color"):
            color = item.removeprefix("color=")
        if item.startswith("zone"):
            zonetype = item.removeprefix("zone=")
            if zonetype in ZoneType:
                zone = ZoneType(zonetype)
        if item.startswith("max_drones"):
            max_drones = int(item.removeprefix("max_drones="))

    if not name or not coordinates:
        raise ValueError("Missing hub data.")

    kwargs: dict[str, Any] = {"name": name, "coordinates": coordinates}
    if color is not None:
        kwargs["color"] = color

    if zone is not None:
        kwargs["zone"] = zone

    if max_drones is not None:
        kwargs["max_drones"] = max_drones
    if special_case:
        kwargs["max_drones"] = None
    return Hub(**kwargs)


def create_connection(connection_data: str) -> Connection:
    if not connection_data:
        raise ValueError("Missing connection data")
    if "[" not in connection_data:
        route = connection_data.split("-", 1)
        return Connection(route[0], route[1])

    data = connection_data.split("[", 1)
    standard_data = data[0].strip()
    metadata = data[1].removesuffix("]")

    route = standard_data.split("-", 1)
    name1 = route[0]
    name2 = route[1]
    if not metadata.startswith("max_link_capacity"):
        raise ValueError(
            f"Incorrect metadata for connection: {connection_data}")
    max_link_capacity = int(metadata.removeprefix("max_link_capacity="))

    return Connection(
        name1=name1,
        name2=name2,
        max_link_capacity=max_link_capacity
    )


def create_entities(path: str) -> Map:
    config = parse_input(path)
    hubs_raw = config.hub_list
    hubs: list[Hub] = []
    connections_raw = config.connection_list
    connections = []

    start_hub = create_hub(config.start_hub, True)
    for hub in hubs_raw:
        hubs.append(create_hub(hub, False))
    end_hub = create_hub(config.end_hub, True)
    for connection in connections_raw:
        connections.append(create_connection(connection))

    neighbours: dict[str, list[Connection]] = {}
    eligible_connections: list[Connection] = []
    for con in connections:
        if start_hub.name in (con.name1, con.name2):
            eligible_connections.append(con)
    neighbours[start_hub.name] = eligible_connections
    for h in hubs:
        eligible_connections = []
        for con in connections:
            if h.name == con.name1 or h.name == con.name2:
                eligible_connections.append(con)
        neighbours[h.name] = eligible_connections
    eligible_connections = []
    for con in connections:
        if end_hub.name in (con.name1, con.name2):
            eligible_connections.append(con)
        neighbours[end_hub.name] = eligible_connections

    hub_name_lookup: dict[str, Hub] = {}
    hub_name_lookup[start_hub.name] = start_hub
    for h in hubs:
        hub_name_lookup[h.name] = h
    hub_name_lookup[end_hub.name] = end_hub

    return Map(
        nb_drones=config.nb_drones,
        start_hub=start_hub,
        hubs=hubs,
        end_hub=end_hub,
        connections=connections,
        neighbours=neighbours,
        hub_name_lookup=hub_name_lookup
    )


if __name__ == "__main__":
    test = create_entities("maps/easy/02_simple_fork.txt")
    for i in test.__slots__:
        print(i, test.__getattribute__(i))
