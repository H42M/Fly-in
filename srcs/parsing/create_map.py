from srcs.parsing.entities import Map, Hub, Connection, ZoneType
from srcs.parsing.input_parser import parse_input
from srcs.parsing.config import Config


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


def create_entities(path: str) -> Map:
    config = parse_input(path)
    hubs = config.hub_list
    connections = config.connection_list
    print(create_hub(config.start_hub))


if __name__ == "__main__":
    create_entities("maps/easy/03_basic_capacity.txt")