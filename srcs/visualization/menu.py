import pygame
from enum import Enum
from pathlib import Path


WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
MAPS_DIR = Path("maps")


class Category(str, Enum):
    BASE_MENU = "base_menu"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    CHALLENGER = "challenger"
    CUSTOM = "custom"


def run_menu() -> Path | None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Fly-in")

    title_font = pygame.font.Font(None, 110)
    menu_font = pygame.font.Font(None, 55)

    button_width = 400
    button_height = 130

    easy_rect = pygame.Rect(420, 390, button_width, button_height)
    medium_rect = pygame.Rect(1100, 390, button_width, button_height)
    hard_rect = pygame.Rect(420, 600, button_width, button_height)
    challenger_rect = pygame.Rect(1100, 600, button_width, button_height)
    back_rect = pygame.Rect(100, 100, 200, 80)

    running = True
    selected_category: Category = Category.BASE_MENU

    while running:
        map_buttons: list[tuple[Path, pygame.Rect]] = []

        if selected_category not in (
            Category.BASE_MENU,
            Category.CUSTOM,
        ):
            category_path = MAPS_DIR / selected_category.value
            map_files = sorted(category_path.glob("*.txt"))

            for i, map_file in enumerate(map_files):
                map_rect = pygame.Rect(
                    WINDOW_WIDTH // 2 - 350,
                    300 + i * 200,
                    700,
                    100,
                )
                map_buttons.append((map_file, map_rect))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if selected_category == Category.BASE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if easy_rect.collidepoint(event.pos):
                        selected_category = Category.EASY

                    elif medium_rect.collidepoint(event.pos):
                        selected_category = Category.MEDIUM

                    elif hard_rect.collidepoint(event.pos):
                        selected_category = Category.HARD

                    elif challenger_rect.collidepoint(event.pos):
                        selected_category = Category.CHALLENGER
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_rect.collidepoint(event.pos):
                        selected_category = Category.BASE_MENU
                    else:
                        for map_file, map_rect in map_buttons:
                            if map_rect.collidepoint(event.pos):
                                pygame.quit()
                                return map_file
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                and selected_category != Category.BASE_MENU
            ):
                selected_category = Category.BASE_MENU

        screen.fill("black")
        if selected_category == Category.BASE_MENU:
            title = title_font.render("FLY-IN", True, "white")
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 140))
            screen.blit(title, title_rect)

            subtitle = menu_font.render("SELECT A MAP", True, "white")
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 260))
            screen.blit(subtitle, subtitle_rect)

            pygame.draw.rect(screen, "white", easy_rect, 3)
            easy_text = menu_font.render("EASY", True, "white")
            screen.blit(easy_text, easy_text.get_rect(center=easy_rect.center))

            pygame.draw.rect(screen, "white", medium_rect, 3)
            medium_text = menu_font.render("MEDIUM", True, "white")
            screen.blit(
                medium_text, medium_text.get_rect(center=medium_rect.center))

            pygame.draw.rect(screen, "white", hard_rect, 3)
            hard_text = menu_font.render("HARD", True, "white")
            screen.blit(hard_text, hard_text.get_rect(center=hard_rect.center))

            pygame.draw.rect(screen, "white", challenger_rect, 3)
            challenger_text = menu_font.render("CHALLENGER", True, "white")
            screen.blit(
                challenger_text, challenger_text.get_rect(
                    center=challenger_rect.center))

        else:
            category_text = title_font.render(
                selected_category.value.upper(), True, "white"
            )
            screen.blit(
                category_text,
                category_text.get_rect(center=(WINDOW_WIDTH // 2, 140))
            )

            pygame.draw.rect(screen, "white", back_rect, 3)
            back_text = menu_font.render("BACK", True, "white")
            screen.blit(
                back_text,
                back_text.get_rect(center=back_rect.center)
            )

            for map_file, map_rect in map_buttons:
                pygame.draw.rect(screen, "white", map_rect, 3)

                map_text = menu_font.render(map_file.stem, True, "white")

                screen.blit(
                    map_text,
                    map_text.get_rect(center=map_rect.center),
                )

        pygame.display.flip()

    pygame.quit()
    return None
