from srcs.parsing.entities import Map, Hub, Connection
from srcs.parsing.input_parser import parse_input
from srcs.parsing.config import Config


def create_hub(hub_data: str) -> Hub:
    data = hub_data.split("[", 1)
    standard_data = data[0]
    metadata = data[1].removesuffix("]")

    data_items = standard_data.split()
    name = data_items[0]
    coordinates = (int(data_items[1]), int(data_items[2]))
    
    for item in metadata:
        if item.startswith("color"):
            color = item.removeprefix("color=")


    return Hub(
        name=name,
        coordinates=coordinates,
        color=color if color else None,
        
    )
    



def create_entities(path: str) -> Map:
    config = parse_input(path)
    hubs = config.hub_list
    connections = config.connection_list
    create_hub(config.start_hub)


if __name__ == "__main__":
    create_entities("maps/easy/03_basic_capacity.txt")