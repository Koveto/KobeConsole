import pygame

from constants import *

from state.state_manager import StateManager
from state.team_builder_state import TeamBuilderState
from state.battle_state import BattleState


def main():
    pygame.init()

    # ---------------------------------------------------------
    # Window setup
    # ---------------------------------------------------------

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    offset_x = (screen_width - GAME_WIDTH) // 2
    offset_y = (screen_height - GAME_HEIGHT) // 2
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        pygame.NOFRAME
    )
    game_surface = pygame.Surface(
        (GAME_WIDTH, GAME_HEIGHT)
    )
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    # ---------------------------------------------------------
    # State Manager + State Registration
    # ---------------------------------------------------------
    state_manager = StateManager()

    state_manager.register(
        STATE_TEAM_BUILDER,
        TeamBuilderState()
    )

    state_manager.register(
        STATE_BATTLE,
        BattleState()
    )

    state_manager.change(STATE_TEAM_BUILDER)

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    running = True
    while running:

        # -----------------------------
        # Event Handling
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == KEY_QUIT:
                    running = False

                # Toggle Pokédex
                elif event.key == KEY_TEAM_BUILDER:
                    state_manager.change(STATE_TEAM_BUILDER)

                # Toggle Battle
                elif event.key == KEY_BATTLE:
                    state_manager.change(STATE_BATTLE)

            # Pass event to active state
            state_manager.handle_event(event)

        # -----------------------------
        # Update + Draw
        # -----------------------------
        state_manager.update()
        game_surface.fill(COLOR_BLACK)
        state_manager.draw(game_surface)

        screen.fill(COLOR_BLACK)

        pygame.draw.rect(
            screen,
            DISPLAY_BORDER_COLOR,
            (
                offset_x - DISPLAY_BORDER_WIDTH,
                offset_y - DISPLAY_BORDER_WIDTH,
                GAME_WIDTH + DISPLAY_BORDER_WIDTH * 2,
                GAME_HEIGHT + DISPLAY_BORDER_WIDTH * 2
            ),
            DISPLAY_BORDER_WIDTH
        )
        screen.blit(
            game_surface,
            (offset_x, offset_y)
        )

        pygame.display.flip()

        clock.tick(TARGET_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
