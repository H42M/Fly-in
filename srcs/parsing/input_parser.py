def parse_input(file: str) -> list[str]:
    if not file:
        return []
    with open(file, "r") as f:
        raw = f.read()
    list_raw = raw.split("\n")
    list_raw_cpy = list_raw.copy()
    for line in list_raw:
        if line.startswith("#"):
            list_raw_cpy.remove(line)
    # TODO: parse the input and return a Config object
        # elif line.startswith("nb_drones"):

    return list_raw_cpy


if __name__ == "__main__":
    test = parse_input("maps/easy/01_linear_path.txt")
    for line in test:
        print(line)
