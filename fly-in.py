from srcs.parsing.create_map import create_entities


def run() -> None:
    map = create_entities("maps/hard/03_ultimate_challenge.txt")
    print(map)


if __name__ == "__main__":
    run()
