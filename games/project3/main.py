import pygame

from constants import *
from update import *
from handle_event import *
from draw import *
from font import *
from save import *

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
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
    player_data = load_player()
    app.player_name = player_data["player_name"]
    app.player_sprite = player_data["player_sprite"]
    options_data = load_options()
    app.option_omniscient = options_data["omniscient"]
    app.option_pkmn_animation = options_data["pkmn_animation"]
    app.option_music_shuffle = options_data["music_shuffle"]
    app.option_mute = options_data["mute"]
    app.option_level = options_data["level"]
    app.option_level_npc = options_data["level_npc"]
    if app.option_mute:
        pygame.mixer.music.set_volume(0.0)
    else:
        pygame.mixer.music.set_volume(1.0)
    app.music_data = load_music_data()
    play_random_menu_music()
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
            elif event.type == MUSIC_END_EVENT:
                if app.option_music_shuffle:
                    if app.current_music_mode == "MENU":
                        play_random_menu_music()
                    elif app.current_music_mode == "BATTLE":
                        play_random_battle_music()
            elif is_mute_toggle(event):
                app.muted = not app.muted
                if app.muted:
                    pygame.mixer.music.set_volume(0.0)
                else:
                    pygame.mixer.music.set_volume(1.0)
            elif is_skip_song(event):
                if app.current_music_mode == "MENU":
                    play_random_menu_music()
                elif app.current_music_mode == "BATTLE":
                    play_random_battle_music()
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