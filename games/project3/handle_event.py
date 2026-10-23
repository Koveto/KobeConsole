from constants import *
from state import *

def handle_event(event):
    if app.state == LAUNCHER_MENU:
        handle_event_LAUNCHER_MENU(event)
    elif app.state == LAN_HOST_JOIN:
        handle_event_LAN_HOST_JOIN(event)
    elif app.state == LAN_HOST:
        handle_event_LAN_HOST(event)
    elif app.state == LAN_JOIN:
        handle_event_LAN_JOIN(event)
    elif app.state == TEAM_PREVIEW:
        handle_event_TEAM_PREVIEW(event)
    elif app.state == PKMN_VIEW:
        handle_event_PKMN_VIEW(event)
    elif app.state == SPECIES_VIEW:
        handle_event_SPECIES_VIEW(event)
    elif app.state == BATTLE_START:
        handle_event_BATTLE_START(event)
    elif app.state == TEAM_SELECT:
        handle_event_TEAM_SELECT(event)
    elif app.state == OPTIONS:
        handle_event_OPTIONS(event)
    elif app.state == KEYBOARD:
        handle_event_KEYBOARD(event)
    elif app.state == OPTIONS_MUSIC:
        handle_event_OPTIONS_MUSIC(event)

def handle_event_OPTIONS_MUSIC(event):
    filenames = sorted(
        app.music_data.keys()
    )
    if is_up(event):
        app.OPTIONS_MUSIC_index = max(
            0,
            app.OPTIONS_MUSIC_index - 1
        )
        if (
            app.OPTIONS_MUSIC_index
            <
            app.OPTIONS_MUSIC_scroll
        ):
            app.OPTIONS_MUSIC_scroll -= 1
    elif is_down(event):
        app.OPTIONS_MUSIC_index = min(
            len(filenames) - 1,
            app.OPTIONS_MUSIC_index + 1
        )
        if (
            app.OPTIONS_MUSIC_index
            >=
            app.OPTIONS_MUSIC_scroll + 8
        ):
            app.OPTIONS_MUSIC_scroll += 1
    elif is_confirm(event):
        filename = filenames[app.OPTIONS_MUSIC_index]
        if app.current_music == filename:
            stop_music()
        else:
            play_music(filename)
    elif is_cancel(event):
        change_state(OPTIONS)
    elif is_cx(event):
        filename = filenames[app.OPTIONS_MUSIC_index]
        app.music_data[
            filename
        ]["menu"] = (
            not
            app.music_data[
                filename
            ]["menu"]
        )
        save_music_data(app.music_data)
    elif is_vy(event):
        filename = filenames[
            app.OPTIONS_MUSIC_index
        ]
        app.music_data[
            filename
        ]["battle"] = (
            not
            app.music_data[
                filename
            ]["battle"]
        )
        save_music_data(app.music_data)

def handle_event_KEYBOARD(event):
    if not using_controller():
        if event.type == pygame.KEYDOWN:
            if (
                event.unicode.isalnum()
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += (
                    event.unicode.upper()
                )
            elif (
                event.key == pygame.K_SPACE
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += " "
            elif (
                event.key == pygame.K_RETURN
            ):
                app.player_name = (
                    app.KEYBOARD_text
                )
                save_player()
                change_state(
                    OPTIONS
                )
            elif (
                event.key == pygame.K_BACKSPACE
            ):
                app.KEYBOARD_text = (
                    app.KEYBOARD_text[:-1]
                )
    else:
        if is_up(event):
            app.KEYBOARD_row = max(
                0,
                app.KEYBOARD_row - 1
            )
        elif is_down(event):
            app.KEYBOARD_row = min(
                len(KEYBOARD_GRID) - 1,
                app.KEYBOARD_row + 1
            )
        elif is_left(event):
            app.KEYBOARD_column = max(
                0,
                app.KEYBOARD_column - 1
            )
        elif is_right(event):
            max_column = (
                len(
                    KEYBOARD_GRID[
                        app.KEYBOARD_row
                    ]
                ) - 1
            )
            app.KEYBOARD_column = min(
                max_column,
                app.KEYBOARD_column + 1
            )
        elif is_confirm(event):
            row = KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
            app.KEYBOARD_column = min(
                app.KEYBOARD_column,
                len(row) - 1
            )
            selected = row[
                app.KEYBOARD_column
            ]
            if (
                selected == "SPACE"
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += " "
            elif (
                selected == "BACK"
            ):
                app.KEYBOARD_text = (
                    app.KEYBOARD_text[:-1]
                )
            elif (
                selected == "DONE"
            ):
                app.player_name = (
                    app.KEYBOARD_text
                )
                save_player()
                change_state(
                    OPTIONS
                )
            elif (
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += (
                    selected
                )
        elif is_cancel(event):
            app.KEYBOARD_text = app.KEYBOARD_text[:-1]
    app.KEYBOARD_column = min(
        app.KEYBOARD_column,
        len(
            KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
        ) - 1
    )

def handle_event_OPTIONS(event):
    if is_up(event):
        app.OPTIONS_index = max(0, app.OPTIONS_index - 1)
    elif is_down(event):
        app.OPTIONS_index = min(5, app.OPTIONS_index + 1)
    elif is_left(event):
        if app.OPTIONS_index == 1:
            app.player_sprite -= 1
            if app.player_sprite < 0:
                app.player_sprite = 161
            save_player()
    elif is_right(event):
        if app.OPTIONS_index == 1:
            app.player_sprite += 1
            if app.player_sprite > 161:
                app.player_sprite = 1
            save_player()
    elif is_confirm(event):
        if app.OPTIONS_index == 0:
            change_state(KEYBOARD)
        elif app.OPTIONS_index == 2:
            change_state(OPTIONS_MUSIC)
        elif app.OPTIONS_index == 3:
            app.option_omniscient = not app.option_omniscient
            save_options()
        elif app.OPTIONS_index == 4:
            app.option_pkmn_animation = not app.option_pkmn_animation
            save_options()
        elif app.OPTIONS_index == 5:
            app.option_music_shuffle = not app.option_music_shuffle
            save_options()
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)

def handle_event_TEAM_SELECT(event):
    if (
        is_up(event)
        and
        app.selected_team is None
    ):
        app.TEAM_SELECT_index = max(
            0,
            app.TEAM_SELECT_index - 1
        )
        app.TEAM_SELECT_selected_team_data = (
            app.teams_data[
                app.TEAM_SELECT_index
            ]
        )
        if (
            app.TEAM_SELECT_selected_team_data["name"]
            == "Random Team"
        ):
            app.TEAM_SELECT_preview_team = []
        else:
            app.TEAM_SELECT_preview_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in app.TEAM_SELECT_selected_team_data["pokemon"]
            ]
    elif (
        is_down(event)
        and
        app.selected_team is None
    ):
        app.TEAM_SELECT_index = min(
            len(app.available_teams) - 1,
            app.TEAM_SELECT_index + 1
        )
        app.TEAM_SELECT_selected_team_data = (
            app.teams_data[
                app.TEAM_SELECT_index
            ]
        )
        if (
            app.TEAM_SELECT_selected_team_data["name"]
            == "Random Team"
        ):
            app.TEAM_SELECT_preview_team = []
        else:
            app.TEAM_SELECT_preview_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in app.TEAM_SELECT_selected_team_data["pokemon"]
            ]
    elif (
        is_confirm(event)
        and
        app.selected_team is None
    ):
        load_species()
        app.TEAM_SELECT_selected_team_data = (
            app.teams_data[
                app.TEAM_SELECT_index
            ]
        )
        if (
            app.TEAM_SELECT_selected_team_data["name"]
            == "Random Team"
        ):
            app.selected_team = [
                Pokemon.from_species_number(
                    random.choice(
                        list(
                            SPECIES.keys()
                        )
                    )
                )
                for _ in range(6)
            ]
        else:
            app.selected_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in app.TEAM_SELECT_selected_team_data["pokemon"]
            ]
        app.TEAM_SELECT_team_sent = False

def handle_event_BATTLE_START(event):
    pass

def handle_event_SPECIES_VIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(0, app.TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(5, app.TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        app.TEAM_PREVIEW_column = 1
    elif is_vy(event):
        if app.SPECIES_VIEW_mode == "STATS":
            app.SPECIES_VIEW_mode = "AFFINITIES"
        else:
            app.SPECIES_VIEW_mode = "STATS"
    elif is_cancel(event):
        change_state(app.previous_state)
    if app.TEAM_PREVIEW_column == 0:
        app.SPECIES_VIEW_pokemon = app.TEAM_PREVIEW_team[app.TEAM_PREVIEW_index]
    elif app.TEAM_PREVIEW_index < len(app.TEAM_PREVIEW_opponent_team):
        app.SPECIES_VIEW_pokemon = app.TEAM_PREVIEW_opponent_team[app.TEAM_PREVIEW_index]

def handle_event_PKMN_VIEW(event):
    if is_up(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_index = max(
                0,
                app.TEAM_PREVIEW_index - 1
            )
        else:
            app.PKMN_VIEW_move_index = max(
                0,
                app.PKMN_VIEW_move_index - 1
            )
    elif is_down(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_index = min(
                5,
                app.TEAM_PREVIEW_index + 1
            )
        else:
            app.PKMN_VIEW_move_index = min(
                len(
                    app.PKMN_VIEW_pokemon.moves
                ) - 1,
                app.PKMN_VIEW_move_index + 1
            )
    elif is_left(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        if ((app.PKMN_VIEW_move_index is None) and \
            (app.option_omniscient)):
            app.TEAM_PREVIEW_column = 1
    elif is_cx(event):
        if app.PKMN_VIEW_mode == "STATS":
            app.PKMN_VIEW_mode = "EVS"
        else:
            app.PKMN_VIEW_mode = "STATS"
    elif is_vy(event):
        if app.PKMN_VIEW_mode == "AFFINITIES":
            app.PKMN_VIEW_mode = "STATS"
        else:
            app.PKMN_VIEW_mode = "AFFINITIES"
    elif is_confirm(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_move_index = 0
    elif is_cancel(event):
        if app.PKMN_VIEW_move_index is not None:
            app.PKMN_VIEW_move_index = None
        else:
            change_state(
                app.previous_state
            )
    if app.TEAM_PREVIEW_column == 0:
        app.PKMN_VIEW_pokemon = (
            app.TEAM_PREVIEW_team[
                app.TEAM_PREVIEW_index
            ]
        )
    elif (
        app.option_omniscient and
        app.TEAM_PREVIEW_index < len(app.TEAM_PREVIEW_opponent_team)
    ):
        app.PKMN_VIEW_pokemon = (
            app.TEAM_PREVIEW_opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )


def handle_event_TEAM_PREVIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(0, app.TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(5, app.TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        if app.option_omniscient:
            app.TEAM_PREVIEW_column = 1
    elif is_confirm(event):
        if app.TEAM_PREVIEW_column == 0:
            app.TEAM_PREVIEW_selected_lead = app.TEAM_PREVIEW_index
    elif is_cvxy(event):
        if app.TEAM_PREVIEW_column == 0:
            app.PKMN_VIEW_pokemon = (
                app.TEAM_PREVIEW_team[
                    app.TEAM_PREVIEW_index
                ]
            )
            change_state(PKMN_VIEW)
        elif (
            app.option_omniscient
            and
            app.TEAM_PREVIEW_index
            < len(
                app.TEAM_PREVIEW_opponent_team
            )
        ):
            app.PKMN_VIEW_pokemon = (
                app.TEAM_PREVIEW_opponent_team[
                    app.TEAM_PREVIEW_index
                ]
            )
            change_state(PKMN_VIEW)

def handle_event_LAN_JOIN(event):
    if is_cancel(event):
        disconnect()
        change_state(LAN_HOST_JOIN)

def handle_event_LAN_HOST(event):
    if is_cancel(event):
        disconnect()
        change_state(LAN_HOST_JOIN)

def handle_event_LAN_HOST_JOIN(event):
    if is_up(event):
        app.LAN_HOST_JOIN_index = max(0, app.LAN_HOST_JOIN_index - 1)
    elif is_down(event):
        app.LAN_HOST_JOIN_index = min(1, app.LAN_HOST_JOIN_index + 1)
    elif is_confirm(event):
        if app.LAN_HOST_JOIN_index == 0:
            change_state(LAN_HOST)
        elif app.LAN_HOST_JOIN_index == 1:
            change_state(LAN_JOIN)
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)

def handle_event_LAUNCHER_MENU(event):
    if is_up(event):
        app.LAUNCHER_MENU_index = max(0, app.LAUNCHER_MENU_index - 1)
    elif is_down(event):
        app.LAUNCHER_MENU_index = min(len(app.LAUNCHER_MENU_options) - 1, app.LAUNCHER_MENU_index + 1)
    elif is_confirm(event):
        if app.LAUNCHER_MENU_index == 0:
            pass
        elif app.LAUNCHER_MENU_index == 1:
            change_state(LAN_HOST_JOIN)
        elif app.LAUNCHER_MENU_index == 2:
            change_state(OPTIONS)