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


def midpoint(start: tuple[int, int], end: tuple[int, int]
             ) -> tuple[int, int]:
    start_x, start_y = start
    end_x, end_y = end
    return ((start_x + end_x) // 2, (start_y + end_y) // 2)


def draw_hud(screen: pygame.Surface, game_state: GameState,
             auto_run: bool, delay: int) -> None:
    turn_font = pygame.font.Font(None, 55)
    hud_font = pygame.font.SysFont("dejavusans", 32, bold=True)
    hud_y = WINDOW_HEIGHT - HUD_HEIGHT
    hud_rect = pygame.Rect(
        0,
        hud_y,
        WINDOW_WIDTH,
        HUD_HEIGHT,
    )

    turn = game_state.turn
    delivered = sum(drone.goal_reached for drone in game_state.drones)
    total = len(game_state.drones)

    if delivered == total:
        mode = "COMPLETE"
    else:
        mode = "AUTO" if auto_run else "MANUAL"

    turn_text = turn_font.render(f"Turn: {turn}", True, "white")
    delivered_text = hud_font.render(f"Delivered: {delivered}/{total}", True,
                                     "white")
    mode_text = hud_font.render(f"Mode: {mode}", True, "white")
    delay_text = hud_font.render(f"Delay: {delay / 1000}s", True, "white")
    controls_text = hud_font.render(
        "SPACE : Next Turn      A : Auto/Pause      ←/→ : Delay      "
        "R : Restart      ESC: Menu",
        True,
        "white",
    )

    pygame.draw.rect(screen, "white", hud_rect, 3)
    screen.blit(turn_text, (40, hud_y + 25))
    screen.blit(delivered_text, (260, hud_y + 38))
    screen.blit(mode_text, (650, hud_y + 38))
    screen.blit(delay_text, (1000, hud_y + 38))
    screen.blit(controls_text, (40, hud_y + 105))


def run_visualizer(
    screen: pygame.Surface,
    engine: Engine
) -> bool:
    game_state = engine.game_state
    game_map = game_state.game_map

    positions = get_hub_positions(game_state)
    hubs = [
        game_state.game_map.start_hub,
        *game_state.game_map.hubs,
        game_state.game_map.end_hub,
    ]
    hub_title_font = pygame.font.Font(None, 18)

    drone_sheet = pygame.image.load("assets/Drones/1/Idle.png").convert_alpha()
    drone_image = drone_sheet.subsurface(pygame.Rect(0, 0, 48, 48))

    old_positions: dict[str, tuple[int, int]] = {}
    progress: float = 0
    auto_run = False
    delay_index = 2
    delay_options = [2000, 1000, 500, 250, 100]

    last_turn_time = pygame.time.get_ticks()

    animation_start = 0
    animating = False

    while True:
        delay = delay_options[delay_index]
        animation_duration = min(400, delay)
        current_time = pygame.time.get_ticks()
        if not engine.drones_traveling():
            auto_run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_r:
                    game_state = GameState(0, game_map)
                    engine = Engine(game_state)
                    old_positions.clear()
                    progress = 0
                    animating = False
                    auto_run = False
                    animation_start = 0
                    last_turn_time = pygame.time.get_ticks()
                if event.key == pygame.K_a:
                    auto_run = not auto_run
                    if auto_run:
                        last_turn_time = pygame.time.get_ticks()
                if event.key == pygame.K_RIGHT:
                    delay_index -= 1
                    if delay_index < 0:
                        delay_index = len(delay_options) - 1
                if event.key == pygame.K_LEFT:
                    delay_index += 1
                    if delay_index > len(delay_options) - 1:
                        delay_index = 0
                if (
                    event.key == pygame.K_SPACE
                    and engine.drones_traveling()
                    and not animating
                    and not auto_run
                ):
                    for drone in game_state.drones:
                        if drone.traveling_to_restricted is not None:
                            old_positions[drone.id] = midpoint(
                                positions[drone.current_position.name],
                                positions[drone.traveling_to_restricted.name])
                        else:
                            old_positions[drone.id] = positions[
                                drone.current_position.name]

                    engine.run_turn()
                    animation_start = pygame.time.get_ticks()
                    last_turn_time = animation_start
                    animating = True
        if (
            auto_run and not animating and engine.drones_traveling()
            and (current_time - last_turn_time >= delay)
        ):
            for drone in game_state.drones:
                if drone.traveling_to_restricted is not None:
                    old_positions[drone.id] = midpoint(
                        positions[drone.current_position.name],
                        positions[drone.traveling_to_restricted.name])
                else:
                    old_positions[drone.id] = positions[
                        drone.current_position.name]

            engine.run_turn()
            animation_start = pygame.time.get_ticks()
            last_turn_time = animation_start
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
            if drone.traveling_to_restricted is not None:
                position = midpoint(
                    positions[drone.current_position.name],
                    positions[drone.traveling_to_restricted.name])
            else:
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

        draw_hud(screen, game_state, auto_run, delay)

        pygame.display.flip()
