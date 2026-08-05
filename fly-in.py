from srcs.parsing.create_map import create_entities
from srcs.simulation.game_state import GameState
from srcs.simulation.engine import Engine


def run() -> None:
    game_map = create_entities("maps/easy/02_simple_fork.txt")
    game_state = GameState(0, game_map)
    engine = Engine(game_state)
    engine.run_simulation()


if __name__ == "__main__":
    run()
