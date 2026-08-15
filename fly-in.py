import pygame
import os

from srcs.parsing.create_map import create_entities
from srcs.simulation.game_state import GameState
from srcs.simulation.engine import Engine
from srcs.visualization.menu import run_menu
from srcs.visualization.visualizer import run_visualizer
from srcs.visualization.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_X,
    WINDOW_Y,
)


def run() -> None:
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{WINDOW_X},{WINDOW_Y}"

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Fly-in")
    while True:
        path = run_menu(screen)

        if path is None:
            break

        game_map = create_entities(path)
        game_state = GameState(0, game_map)

        back_to_menu = run_visualizer(screen, game_state)

        if not back_to_menu:
            break

    pygame.quit()


if __name__ == "__main__":
    run()
