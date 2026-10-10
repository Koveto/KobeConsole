import pygame
import subprocess
import random
import os
import sys
from input_manager import *

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
print(
    "Launcher Running From:",
    BASE_DIR
)

pygame.init()


display_info = pygame.display.Info()
#1750x1100
screen = pygame.display.set_mode(
    (display_info.current_w, display_info.current_h),
    pygame.NOFRAME
)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
pygame.display.set_caption("KobeConsole")

title_font = pygame.font.SysFont(None, 56)
game_font = pygame.font.SysFont(None, 36)
info_font = pygame.font.SysFont(None, 28)

def create_particles(count):

    particles = []

    for _ in range(count):
        particles.append({
            "x": random.randint(0, screen.get_width()),
            "y": random.randint(0, screen.get_height()),
            "speed": random.uniform(0.2, 1.0),
            "size": random.randint(2, 5)
        })

    return particles
particles = create_particles(80)

selected_index = 0
fullscreen = False
time = 0

games = [
    {
        "title": "Update",
        "path": None,
        "color": (220, 180, 0),
        "logo": os.path.join(
            BASE_DIR,
            "assets",
            "logos",
            "logo1.png"
        )
    },
    {
        "title": "Tic Tac Toe",
        "path": "games/tic_tac_toe.py",
        "color": (0, 180, 0),
        "logo": os.path.join(
            BASE_DIR,
            "assets",
            "logos",
            "logo2.png"
        )
    },
    {
        "title": "Pokemon SMT Game",
        "path": "games/project1/main.py",
        "color": (0, 100, 255),
        "logo": os.path.join(
            BASE_DIR,
            "assets",
            "logos",
            "logo0.png"
        )
    },
]

#background = pygame.image.load("assets/backgrounds/bg0.jpg")
#background = pygame.transform.scale(background, (800, 600))

for game in games:
    game["logo_surface"] = pygame.image.load(game["logo"]).convert_alpha()


def update_kobeconsole():
    result = subprocess.run(
        ["git", "pull"],
        cwd=BASE_DIR
    )
    pygame.event.clear()
    os.execv(
        sys.executable,
        [
            sys.executable,
            os.path.abspath(__file__)
        ]
    )

def launch_game(path):

    full_path = os.path.join(
        BASE_DIR,
        path
    )

    game_dir = os.path.dirname(
        full_path
    )

    subprocess.run(
        [
            "python3",
            os.path.basename(full_path)
        ],
        cwd=game_dir
    )
    pygame.event.clear()

def draw_text_outline(
    surface,
    text,
    font,
    color,
    outline_color,
    center
):
    outline = font.render(text, True, outline_color)

    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx or dy:
                rect = outline.get_rect(center=(center[0] + dx, center[1] + dy))
                surface.blit(outline, rect)

    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, rect)


running = True

while running:

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    screen.fill((20, 20, 40))
    for particle in particles:

        particle["y"] += particle["speed"]

        if particle["y"] > HEIGHT:
            particle["y"] = 0
            particle["x"] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (100, 100, 160),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    for event in pygame.event.get():

        if is_right(event):
            selected_index += 1

        elif is_left(event):
            selected_index -= 1

        elif is_confirm(event):

            selected_game = games[selected_index]

            if selected_game["title"] == "Update":

                update_kobeconsole()

            else:

                launch_game(
                    selected_game["path"]
                )

        elif is_cancel(event):
            running = False


    selected_index = max(0, min(selected_index, len(games) - 1))


    #
    # Draw selected game title
    #
    selected_name = games[selected_index]["title"]

    draw_text_outline(
        screen,
        selected_name,
        title_font,
        (255, 255, 255),
        (0, 0, 0),
        (WIDTH // 2, 80)
    )

    #
    # Draw game cards
    #
    card_y = HEIGHT // 2 - 90
    center_x = WIDTH // 2
    spacing = 220

    for index, game in enumerate(games):

        offset = index - selected_index
        if abs(offset) > 2:
            continue

        card_x = center_x + offset * spacing

        if index == selected_index:

            rect = pygame.Rect(
                card_x - 90,
                card_y,
                180,
                180
            )

            logo = pygame.transform.smoothscale(
                game["logo_surface"],
                (rect.width, rect.height)
            )

            screen.blit(logo, rect)

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                rect,
                4
            )

        else:

            rect = pygame.Rect(
                card_x - 70,
                card_y + 20,
                140,
                140
            )

            logo = pygame.transform.smoothscale(
                game["logo_surface"],
                (rect.width, rect.height)
            )

            screen.blit(logo, rect)

    #
    # Draw instructions
    #
    draw_text_outline(
        screen,
        "LEFT/RIGHT = Select    ENTER = Launch    F11 = Fullscreen",
        info_font,
        (255, 255, 255),
        (0, 0, 0),
        (WIDTH // 2, HEIGHT - 50)
    )

    pygame.display.flip()

pygame.quit()