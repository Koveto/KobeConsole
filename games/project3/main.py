import pygame

from constants import *
from update import *
from handle_event import *
from draw import *
from font import *

def main():
    pygame.init()
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    game_scale = min(
        screen_width / W_SCREEN_LOGICAL,
        screen_height / H_SCREEN_LOGICAL
    )
    game_width = W_SCREEN_LOGICAL * game_scale
    game_height = H_SCREEN_LOGICAL * game_scale
    offset_x = (screen_width - game_width) // 2
    offset_y = (screen_height - game_height) // 2
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        pygame.NOFRAME
    )
    app.screen = pygame.Surface(
        (
            W_SCREEN_LOGICAL,
            H_SCREEN_LOGICAL
        )
    )
    init_draw()
    pygame.display.set_caption(TEXT_WINDOW_TITLE)
    clock = pygame.time.Clock()
    app.state = LAUNCHER_MENU
    app.font0 = Font(
                "font_menu.png",
                glyph_w=6,
                glyph_h=13,
                scale=1,
                spacing=6)
    running = True
    while running:
        for event in pygame.event.get():
            if is_quit(event):
                if app.connection_socket is not None:
                    send_packet({"type":"DISCONNECT"})
                disconnect()
                running = False
            handle_event(event)
        update()
        app.screen.fill(COLOR_BLUE)
        draw()
        screen.fill(COLOR_BLACK)
        screen_game_scaled = pygame.transform.scale(
            app.screen,
            (
                game_width,
                game_height
            )
        )
        screen.blit(
            screen_game_scaled,
            (
                offset_x,
                offset_y
            )
        )
        pygame.display.flip()
        clock.tick(NUM_TARGET_FPS)
    pygame.quit()

if __name__ == "__main__":
    main()