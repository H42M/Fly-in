from srcs.parsing.config import Config


def parse_input(path: str) -> Config:
    if not path:
        return Config()
    with open(path, "r") as file:
        raw = file.read()
    list_raw = raw.split("\n")
    list_raw_cpy = list_raw.copy()

    base_config = Config()
    hub_list = []
    connection_list = []
    for line in list_raw:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#"):
            list_raw_cpy.remove(line)

        elif line.startswith("nb_drones"):
            if not line[-1] in '0123456789':
                nb_drones = base_config.nb_drones
            else:
                nb_drones = ""
                for char in line[::-1]:
                    if char in "0123456789":
                        nb_drones += char
                nb_drones = int(nb_drones[::-1])

        elif line.startswith("start_hub"):
            start_hub = line.removeprefix("start_hub: ")

        elif line.startswith("hub"):
            hub_list.append(line.removeprefix("hub: "))

        elif line.startswith("end_hub"):
            end_hub = line.removeprefix("end_hub: ")

        elif line.startswith("connection"):
            connection_list.append(line.removeprefix("connection: "))

    return Config(
        nb_drones=nb_drones,
        start_hub=start_hub,
        hub_list=tuple(hub_list),
        end_hub=end_hub,
        connection_list=tuple(connection_list)
    )


if __name__ == "__main__":
    test = parse_input("maps/easy/02_simple_fork.txt")
    for i in test.__slots__:
        print(i, test.__getattribute__(i))
