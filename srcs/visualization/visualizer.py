import pygame

from srcs.simulation.engine import Engine
from srcs.simulation.game_state import GameState
from srcs.visualization.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GRAPH_MARGIN,
    HUD_HEIGHT,
    MAX_GRAPH_SCALE,
)


def get_hub_positions(
    game_state: GameState,
) -> dict[str, tuple[int, int]]:
    game_map = game_state.game_map

    hubs = [
        game_map.start_hub,
        *game_map.hubs,
        game_map.end_hub,
    ]

    xs = [hub.coordinates[0] for hub in hubs]
    ys = [hub.coordinates[1] for hub in hubs]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    map_width = max(max_x - min_x, 1)
    map_height = max(max_y - min_y, 1)

    graph_width = WINDOW_WIDTH - GRAPH_MARGIN * 2
    graph_height = WINDOW_HEIGHT - HUD_HEIGHT - GRAPH_MARGIN * 2

    scale_x = min(graph_width / map_width, MAX_GRAPH_SCALE)
    scale_y = min(graph_height / map_height, MAX_GRAPH_SCALE)

    actual_width = (max_x - min_x) * scale_x
    actual_height = (max_y - min_y) * scale_y

    offset_x = GRAPH_MARGIN + (graph_width - actual_width) / 2
    offset_y = GRAPH_MARGIN + (graph_height - actual_height) / 2

    positions: dict[str, tuple[int, int]] = {}

    for hub in hubs:
        x, y = hub.coordinates

        screen_x = offset_x + (x - min_x) * scale_x
        screen_y = offset_y + (max_y - y) * scale_y

        positions[hub.name] = (int(screen_x), int(screen_y))

    return positions


def run_visualizer(
    screen: pygame.Surface,
    engine: Engine
) -> bool:
    game_state = engine.game_state
    positions = get_hub_positions(game_state)
    hubs = [
        game_state.game_map.start_hub,
        *game_state.game_map.hubs,
        game_state.game_map.end_hub,
    ]
    hub_title_font = pygame.font.Font(None, 18)

    drone_sheet = pygame.image.load("assets/Drones/1/Idle.png").convert_alpha()
    drone_image = drone_sheet.subsurface(pygame.Rect(0, 0, 48, 48))

    animation_start = 0
    animation_duration = 400
    animating = False
    old_positions: dict[str, tuple[int, int]] = {}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if (
                    event.key == pygame.K_SPACE
                    and engine.drones_traveling()
                    and not animating
                ):
                    old_positions = {
                        drone.id: positions[drone.current_position.name]
                        for drone in game_state.drones}
                    engine.run_turn()
                    animation_start = pygame.time.get_ticks()
                    animating = True

        screen.fill("black")

        # Connection (lines) display
        for connection in game_state.game_map.connections:
            start_pos = positions[connection.name1]
            end_pos = positions[connection.name2]

            pygame.draw.line(
                screen,
                "white",
                start_pos,
                end_pos,
                2,
            )

        # Hub display
        for hub in hubs:
            position = positions[hub.name]
            pygame.draw.circle(screen, "black", position, 25)
            if hub.color:
                try:
                    color = pygame.Color(hub.color)
                except ValueError:
                    color = pygame.Color("white")
                pygame.draw.circle(screen, color, position, 25, 3)
            else:
                pygame.draw.circle(screen, "white", position, 25, 3)
            hub_title = hub_title_font.render(hub.name, True, "white")
            x, y = position
            screen.blit(hub_title, hub_title.get_rect(center=(x, y + 35)))

        # Drone display
        for drone in game_state.drones:
            position = positions[drone.current_position.name]
            if not old_positions:
                screen.blit(
                    drone_image,
                    drone_image.get_rect(center=position)
                )
                continue
            elapsed = pygame.time.get_ticks() - animation_start
            start_x, start_y = old_positions[drone.id]
            end_x, end_y = position
            progress = min(elapsed / animation_duration, 1.0)

            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            current_pos = (current_x, current_y)

            if animating:
                screen.blit(
                    drone_image,
                    drone_image.get_rect(center=(current_pos))
                )
            else:
                screen.blit(
                    drone_image,
                    drone_image.get_rect(center=position)
                )
                if progress >= 1.0:
                    animating = False

        pygame.display.flip()
