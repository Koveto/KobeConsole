import pygame
import subprocess
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("KobeConsole")

title_font = pygame.font.SysFont(None, 56)
game_font = pygame.font.SysFont(None, 36)
info_font = pygame.font.SysFont(None, 28)

particles = []

for i in range(40):
    particles.append({
        "x": random.randint(0, 800),
        "y": random.randint(0, 600),
        "speed": random.uniform(0.2, 1.0),
        "size": random.randint(2, 5)
    })

selected_index = 0

games = [
    {
        "title": "Heads or Tails",
        "path": "games/heads_or_tails.py",
        "color": (0, 100, 255),
        "logo": "assets/logos/logo0.png"
    },
    {
        "title": "Test Game",
        "path": "games/test_game.py",
        "color": (0, 180, 0),
        "logo": "assets/logos/logo1.png"

    },
]

#background = pygame.image.load("assets/backgrounds/bg0.jpg")
#background = pygame.transform.scale(background, (800, 600))

for game in games:
    game["logo_surface"] = pygame.image.load(game["logo"]).convert_alpha()


def launch_game(path):
    subprocess.run(["python", path])

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

    screen.fill((20, 20, 40))
    for particle in particles:

        particle["y"] += particle["speed"]

        if particle["y"] > 600:
            particle["y"] = 0

        pygame.draw.circle(
            screen,
            (100, 100, 160),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                selected_index += 1

            elif event.key == pygame.K_LEFT:
                selected_index -= 1

            elif event.key == pygame.K_RETURN:
                launch_game(games[selected_index]["path"])

            selected_index = max(0, min(selected_index, len(games) - 1))

    #screen.blit(background, (0, 0))

    #
    # Draw selected game title
    #
    selected_name = games[selected_index]["title"]

    title_surface = title_font.render(
        selected_name,
        True,
        (255, 255, 255)
    )

    title_rect = title_surface.get_rect(center=(400, 80))
    draw_text_outline(
        screen,
        selected_name,
        title_font,
        (255, 255, 255),
        (0, 0, 0),
        (400, 80)
    )

    #
    # Draw game cards
    #
    card_y = 220
    center_x = 400
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
    instructions = info_font.render(
        "Use LEFT/RIGHT arrows and ENTER",
        True,
        (200, 200, 200)
    )

    instructions_rect = instructions.get_rect(
        center=(400, 525)
    )

    draw_text_outline(
        screen,
        "Use LEFT/RIGHT arrows and ENTER",
        info_font,
        (255, 255, 255),
        (0, 0, 0),
        (400, 525)
    )

    pygame.display.flip()

pygame.quit()