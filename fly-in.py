from srcs.parsing.input_parser import parse_input


def run() -> None:
    test = parse_input("maps/easy/01_linear_path.txt")
    for line in test:
        print(line)


if __name__ == "__main__":
    run()
