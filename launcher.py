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
fresh_install_armed = False
fresh_install_armed_until = 0
launcher_status = ""

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
        "title": "Fresh Install",
        "path": None,
        "color": (200, 50, 50),
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
        "title": "Pokemon Battle Simulator",
        "path": "games/project2/main.py",
        "color": (0, 100, 255),
        "logo": os.path.join(
            BASE_DIR,
            "assets",
            "logos",
            "logo0.png"
        )
    },
    {
        "title": "Pokemon Battle Simulator V2",
        "path": "games/project3/main.py",
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

    global launcher_status

    launcher_status = (
        "UPDATING..."
    )

    pygame.display.flip()

    result = subprocess.run(
        [
            "git",
            "pull",
            "--ff-only"
        ],
        cwd=BASE_DIR,
        check=False
    )

    if result.returncode != 0:

        launcher_status = (
            "UPDATE FAILED"
        )

        pygame.event.clear()

        return False

    pygame.event.clear()

    os.execv(
        sys.executable,
        [
            sys.executable,
            os.path.abspath(
                __file__
            )
        ]
    )

    return True

def factory_reset_kobeconsole():

    global launcher_status

    launcher_status = (
        "PREPARING FRESH INSTALL..."
    )

    pygame.display.flip()

    try:

        remote_url = (
            subprocess.check_output(
                [
                    "git",
                    "remote",
                    "get-url",
                    "origin"
                ],
                cwd=BASE_DIR,
                text=True
            ).strip()
        )

        branch_name = (
            subprocess.check_output(
                [
                    "git",
                    "branch",
                    "--show-current"
                ],
                cwd=BASE_DIR,
                text=True
            ).strip()
        )

    except (
        OSError,
        subprocess.CalledProcessError
    ):

        launcher_status = (
            "COULD NOT READ GIT REMOTE"
        )

        pygame.event.clear()

        return False

    if not remote_url:

        launcher_status = (
            "NO ORIGIN REMOTE"
        )

        pygame.event.clear()

        return False

    if not branch_name:

        branch_name = "main"

    repository_path = (
        os.path.abspath(
            BASE_DIR
        )
    )

    repository_parent = (
        os.path.dirname(
            repository_path
        )
    )

    repository_name = (
        os.path.basename(
            repository_path
        )
    )

    backup_path = (
        repository_path
        + ".fresh-install-backup"
    )

    launcher_filename = (
        os.path.basename(
            os.path.abspath(
                __file__
            )
        )
    )

    script_path = (
        os.path.join(
            "/tmp",
            "kobeconsole_fresh_install.sh"
        )
    )

    script = f"""#!/bin/bash

set -u

REPOSITORY_PATH={repository_path!r}
REPOSITORY_PARENT={repository_parent!r}
REPOSITORY_NAME={repository_name!r}
BACKUP_PATH={backup_path!r}
REMOTE_URL={remote_url!r}
BRANCH_NAME={branch_name!r}
LAUNCHER_FILENAME={launcher_filename!r}

sleep 1

rm -rf "$BACKUP_PATH"

mv "$REPOSITORY_PATH" "$BACKUP_PATH"

if git clone \\
    --branch "$BRANCH_NAME" \\
    --single-branch \\
    "$REMOTE_URL" \\
    "$REPOSITORY_PATH"
then
    rm -rf "$BACKUP_PATH"

    cd "$REPOSITORY_PATH" || exit 1

    exec python3 "$LAUNCHER_FILENAME"
fi

rm -rf "$REPOSITORY_PATH"

mv "$BACKUP_PATH" "$REPOSITORY_PATH"

cd "$REPOSITORY_PATH" || exit 1

exec python3 "$LAUNCHER_FILENAME"
"""

    try:

        with open(
            script_path,
            "w",
            encoding="utf-8"
        ) as outfile:

            outfile.write(
                script
            )

        os.chmod(
            script_path,
            0o700
        )

    except OSError:

        launcher_status = (
            "COULD NOT CREATE RESET SCRIPT"
        )

        pygame.event.clear()

        return False

    pygame.event.clear()

    pygame.quit()

    os.execv(
        "/bin/bash",
        [
            "/bin/bash",
            script_path
        ]
    )

    return True

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

        if (
            (
                IS_WINDOWS
                and
                is_quit(
                    event
                )
            )
            or
            event.type
            == pygame.QUIT
        ):

            running = False

            continue

        if is_right(
            event
        ):

            selected_index += 1

            fresh_install_armed = False
            fresh_install_armed_until = 0
            launcher_status = ""

        elif is_left(
            event
        ):

            selected_index -= 1

            fresh_install_armed = False
            fresh_install_armed_until = 0
            launcher_status = ""

        elif is_confirm(
            event
        ):

            selected_game = (
                games[
                    selected_index
                ]
            )

            if (
                selected_game["title"]
                == "Update"
            ):

                fresh_install_armed = False
                fresh_install_armed_until = 0

                update_kobeconsole()

            elif (
                selected_game["title"]
                == "Fresh Install"
            ):

                current_time = (
                    pygame.time.get_ticks()
                )

                if (
                    not fresh_install_armed
                    or
                    current_time
                    > fresh_install_armed_until
                ):

                    fresh_install_armed = True

                    fresh_install_armed_until = (
                        current_time
                        + 5000
                    )

                    launcher_status = (
                        "PRESS CONFIRM AGAIN TO ERASE EVERYTHING"
                    )

                else:

                    fresh_install_armed = False
                    fresh_install_armed_until = 0

                    factory_reset_kobeconsole()

            else:

                fresh_install_armed = False
                fresh_install_armed_until = 0
                launcher_status = ""

                launch_game(
                    selected_game[
                        "path"
                    ]
                )

        elif is_cancel(
            event
        ):

            if fresh_install_armed:

                fresh_install_armed = False
                fresh_install_armed_until = 0

                launcher_status = (
                    "FRESH INSTALL CANCELED"
                )

            else:

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
        get_launcher_text(),
        info_font,
        (255, 255, 255),
        (0, 0, 0),
        (WIDTH // 2, HEIGHT - 50)
    )

    if launcher_status:

        draw_text_outline(
            screen,
            launcher_status,
            info_font,
            (
                255,
                220,
                80
            ),
            (
                0,
                0,
                0
            ),
            (
                WIDTH // 2,
                HEIGHT - 95
            )
        )

    pygame.display.flip()

pygame.quit()