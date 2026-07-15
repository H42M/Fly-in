from srcs.parsing.entities import Map, Hub, Connection, ZoneType
from srcs.parsing.input_parser import parse_input


def create_hub(hub_data: str) -> Hub:
    if not hub_data:
        raise ValueError("Missing hub data.")
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
                zone = ZoneType[zonetype]
        if item.startswith("max_drones"):
            max_drones = int(item.removeprefix("max_drones="))

    if not name or not coordinates:
        raise ValueError("Missing hub data.")

    kwargs = {"name": name, "coordinates": coordinates}
    if color is not None:
        kwargs["color"] = color

    if zone is not None:
        kwargs["zone"] = zone

    if max_drones is not None:
        kwargs["max_drones"] = max_drones
    return Hub(**kwargs)


def create_connection(connection_data: str) -> Connection:
    if not connection_data:
        raise ValueError("Missing connection data")
    if "[" not in connection_data:
        route = connection_data.split("-", 1)
        return Connection(route[0], route[1])

    data = connection_data.split("[", 1)
    standard_data = data[0]
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
    hubs = []
    connections_raw = config.connection_list
    connections = []

    start_hub = create_hub(config.start_hub)
    for hub in hubs_raw:
        hubs.append(create_hub(hub))
    end_hub = create_hub(config.end_hub)
    for connection in connections_raw:
        connections.append(create_connection(connection))

    return Map(
        nb_drones=config.nb_drones,
        start_hub=start_hub,
        hubs=hubs,
        end_hub=end_hub,
        connections=connections
    )


if __name__ == "__main__":
    test = create_entities("maps/easy/01_linear_path.txt")
    for i in test.__slots__:
        print(i, test.__getattribute__(i))