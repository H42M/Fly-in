from srcs.parsing.input_parser import parse_input


def run() -> None:
    test = parse_input("maps/easy/01_linear_path.txt")
    for attribute in test.__slots__:
        print(attribute, test.__getattribute__(attribute))


if __name__ == "__main__":
    run()
