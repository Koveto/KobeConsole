import pygame

from constants import *

from state.state_manager import StateManager
from state.battle_state import BattleState
from state.menu_state import MenuState
from state.lan_menu_state import LanMenuState
from state.host_state import HostState
from state.join_state import JoinState

from input_manager_pkmn import *


def main():
    pygame.init()

    # ---------------------------------------------------------
    # Window setup
    # ---------------------------------------------------------

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    game_scale = min(
        screen_width / LOGICAL_WIDTH,
        screen_height / LOGICAL_HEIGHT
    )
    game_width = LOGICAL_WIDTH * game_scale
    game_height = LOGICAL_HEIGHT * game_scale
    offset_x = (screen_width - game_width) // 2
    offset_y = (screen_height - game_height) // 2
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        pygame.NOFRAME
    )
    game_surface = pygame.Surface(
        (
            LOGICAL_WIDTH,
            LOGICAL_HEIGHT
        )
    )
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    # ---------------------------------------------------------
    # State Manager + State Registration
    # ---------------------------------------------------------
    state_manager = StateManager()

    state_manager.register(
        STATE_BATTLE,
        BattleState()
    )

    state_manager.register(
        STATE_MENU,
        MenuState()
    )

    state_manager.register(
        STATE_LAN_MENU,
        LanMenuState()
    )

    state_manager.register(
        STATE_HOST,
        HostState()
    )

    state_manager.register(
        STATE_JOIN,
        JoinState()
    )

    state_manager.change(STATE_MENU)

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    running = True
    while running:

        # -----------------------------
        # Event Handling
        # -----------------------------
        for event in pygame.event.get():

            if is_quit(event):
                running = False

            state_manager.handle_event(event)

        # -----------------------------
        # Update + Draw
        # -----------------------------
        state_manager.update()
        game_surface.fill(COLOR_BLUE)
        state_manager.draw(game_surface)

        screen.fill(COLOR_BLACK)

        pygame.draw.rect(
            screen,
            DISPLAY_BORDER_COLOR,
            (
                offset_x - DISPLAY_BORDER_WIDTH,
                offset_y - DISPLAY_BORDER_WIDTH,
                game_width + DISPLAY_BORDER_WIDTH * 2,
                game_height + DISPLAY_BORDER_WIDTH * 2
            ),
            DISPLAY_BORDER_WIDTH
        )
        scaled_surface = pygame.transform.scale(
            game_surface,
            (
                game_width,
                game_height
            )
        )

        screen.blit(
            scaled_surface,
            (
                offset_x,
                offset_y
            )
        )

        pygame.display.flip()

        clock.tick(TARGET_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
