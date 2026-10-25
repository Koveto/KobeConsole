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
    elif app.state == SINGLE_MENU:
        handle_event_SINGLE_MENU(event)
    elif app.state == SINGLE_MENU_TRAINER:
        handle_event_SINGLE_MENU_TRAINER(event)
    elif app.state == BATTLE_END:
        handle_event_BATTLE_END(event)
    elif app.state == SINGLE_BRACKET:
        handle_event_SINGLE_BRACKET(event)

def start_tournament():
    app.tournament_semifinals = []
    app.tournament_finals = []
    app.tournament_active = True
    app.tournament_round = 0
    selected_trainers = random.sample(
        app.trainers_data,
        7
    )
    app.tournament_quarterfinals = [
        "PLAYER",
        selected_trainers[0],
        selected_trainers[1],
        selected_trainers[2],
        selected_trainers[3],
        selected_trainers[4],
        selected_trainers[5],
        selected_trainers[6]
    ]
    app.tournament_current_trainer = (
        app.tournament_quarterfinals[1]
    )

def handle_event_SINGLE_BRACKET(
    event
):

    if is_confirm(event):

        if (
            app.tournament_round
            == 0
        ):

            app.team_select_return_state = (
                SINGLE_BRACKET
            )

            app.allow_team_change = True

            app.allow_lead_change = True

            change_state(
                TEAM_SELECT
            )

        else:

            if (
                app.tournament_round
                == 1
            ):

                opponent = (
                    app.tournament_semifinals[
                        1
                    ]
                )

            else:

                opponent = (
                    app.tournament_finals[
                        1
                    ]
                )

            app.tournament_current_trainer = (
                opponent
            )

            app.selected_trainer_data = (
                opponent
            )

            app.opponent_team = [

                Pokemon.from_dict(
                    pokemon_data
                )

                for pokemon_data
                in
                opponent["team"]

            ]

            app.allow_team_change = False

            app.allow_lead_change = True

            change_state(
                TEAM_PREVIEW
            )

def start_next_endless_battle():
    trainer_index = random.randint(
        0,
        len(app.trainers_data) - 1
    )
    app.endless_trainer_index = (
        trainer_index
    )
    trainer = (
        app.trainers_data[
            trainer_index
        ]
    )
    app.selected_trainer_data = (
        trainer
    )
    app.opponent_team = [
        Pokemon.from_dict(
            pokemon_data
        )
        for pokemon_data in
        trainer["team"]
    ]
    for pokemon in app.opponent_team:
        pokemon.set_level(
            app.option_level_npc
        )

def handle_event_BATTLE_END(event):
    pass

def handle_event_SINGLE_MENU_TRAINER(event):
    if is_up(event):
        app.SINGLE_MENU_TRAINER_index = max(0, app.SINGLE_MENU_TRAINER_index - 1)
    elif is_down(event):
        app.SINGLE_MENU_TRAINER_index = min(2, app.SINGLE_MENU_TRAINER_index + 1)
    elif is_cancel(event):
        change_state(SINGLE_MENU)
    elif is_confirm(event):
        if (
            app.SINGLE_MENU_TRAINER_index
            == 0
        ):
            app.single_battle_mode = (
                "RANDOM_TEAM"
            )
        elif (
            app.SINGLE_MENU_TRAINER_index
            == 1
        ):
            app.single_battle_mode = (
                "MY_TEAM"
            )
        else:
            app.single_battle_mode = (
                "TRAINER"
            )
        app.selected_trainer_data = (
            app.trainers_data[
                app.SINGLE_MENU_TRAINER_selected_trainer
            ]
        )
        app.team_select_return_state = (
            SINGLE_MENU_TRAINER
        )

        app.allow_team_change = True
        app.allow_lead_change = True

        if (
            app.single_battle_mode
            == "MY_TEAM"
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is None
        ):
            return

        app.restore_single_menu_trainer = True
        change_state(
            TEAM_SELECT
        )
    elif is_left(event):
        if (
            app.SINGLE_MENU_TRAINER_index == 1
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is not None
        ):
            app.SINGLE_MENU_TRAINER_selected_team = max(
                0,
                app.SINGLE_MENU_TRAINER_selected_team - 1
            )
            selected_team = (
                app.teams_data[
                    app.SINGLE_MENU_TRAINER_selected_team
                ]
            )

            app.SINGLE_MENU_TRAINER_my_team_preview = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                selected_team["pokemon"]
            ]
        elif app.SINGLE_MENU_TRAINER_index == 2:
            app.SINGLE_MENU_TRAINER_selected_trainer = max(
                0,
                app.SINGLE_MENU_TRAINER_selected_trainer - 1
            )
            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )
            app.SINGLE_MENU_TRAINER_preview_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                trainer["team"]
            ]
    elif is_right(event):
        if (
            app.SINGLE_MENU_TRAINER_index == 1
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is not None
        ):
            app.SINGLE_MENU_TRAINER_selected_team = min(
                len(app.teams_data) - 1,
                app.SINGLE_MENU_TRAINER_selected_team + 1
            )
            selected_team = (
                app.teams_data[
                    app.SINGLE_MENU_TRAINER_selected_team
                ]
            )

            app.SINGLE_MENU_TRAINER_my_team_preview = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                selected_team["pokemon"]
            ]
        elif app.SINGLE_MENU_TRAINER_index == 2:
            app.SINGLE_MENU_TRAINER_selected_trainer = min(
                len(app.trainers_data) - 1,
                app.SINGLE_MENU_TRAINER_selected_trainer + 1
            )
            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )
            app.SINGLE_MENU_TRAINER_preview_team = [

                Pokemon.from_dict(
                    pokemon_data
                )

                for pokemon_data
                in
                trainer["team"]

            ]

def generate_test_teams():

    load_species()

    save_data = load_save()

    teams = []

    species_list = list(
        SPECIES.keys()
    )

    for team_index in range(10):

        team = {
            "name":
                f"Test Team {team_index + 1}",
            "pokemon": []
        }

        for _ in range(6):

            pokemon = (
                Pokemon.from_species_number(
                    random.choice(
                        species_list
                    )
                )
            )

            team["pokemon"].append(
                pokemon.to_dict()
            )

        teams.append(
            team
        )

    save_data[
        "teams"
    ] = teams

    save_save(
        save_data
    )


def handle_event_SINGLE_MENU(event):
    if is_up(event):
        app.SINGLE_MENU_index = max(0, app.SINGLE_MENU_index - 1)
    elif is_down(event):
        app.SINGLE_MENU_index = min(len(app.SINGLE_MENU_options) - 1, app.SINGLE_MENU_index + 1)
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)
    elif is_confirm(event):
        if app.SINGLE_MENU_index == 0:
            change_state(
                SINGLE_MENU_TRAINER
            )
        elif app.SINGLE_MENU_index == 1:
            app.game_mode = (
                "ENDLESS"
            )
            if app.endless_active:
                start_next_endless_battle()
                change_state(
                    TEAM_PREVIEW
                )
            else:
                app.endless_active = (
                    True
                )
                app.endless_wins = 0
                app.team_select_return_state = (
                    SINGLE_MENU
                )
                app.allow_team_change = True
                app.allow_lead_change = True
                change_state(
                    TEAM_SELECT
                )
        elif app.SINGLE_MENU_index == 3:
            app.game_mode = "TOURNAMENT"
            start_tournament()
            change_state(SINGLE_BRACKET)
    elif is_vy(event):
        reset_save()
        generate_test_teams()
        change_state(
            SINGLE_MENU
        )

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
        if app.OPTIONS_index < app.OPTIONS_scroll:
            app.OPTIONS_scroll -= 1
    elif is_down(event):
        app.OPTIONS_index = min(7, app.OPTIONS_index + 1)
        if app.OPTIONS_index >= app.OPTIONS_scroll + 6:
            app.OPTIONS_scroll += 1
    elif is_left(event):
        if app.OPTIONS_index == 1:
            app.player_sprite -= 1
            if app.player_sprite < 0:
                app.player_sprite = 161
            save_player()
        elif app.OPTIONS_index == 6:
            app.option_level = max(1, app.option_level - 1)
            save_options()
        elif app.OPTIONS_index == 7:
            app.option_level_npc = max(1, app.option_level_npc - 1)
            save_options()
    elif is_right(event):
        if app.OPTIONS_index == 1:
            app.player_sprite += 1
            if app.player_sprite > 161:
                app.player_sprite = 0
            save_player()
        elif app.OPTIONS_index == 6:
            app.option_level = min(100, app.option_level + 1)
            save_options()
        elif app.OPTIONS_index == 7:
            app.option_level_npc = min(100, app.option_level_npc + 1)
            save_options()
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
    is_lan_battle = app.connection_socket is not None
    if (
        is_up(event)
        and
        app.player_team is None
    ):
        handle_generic_team_select_navigation(
            -1
        )
    elif (
        is_down(event)
        and
        app.player_team is None
    ):
        handle_generic_team_select_navigation(
            1
        )
    elif is_cancel(event):

        if (
            app.connection_socket
            is None
        ):
            change_state(
                app.team_select_return_state
            )
    elif (
        is_confirm(event)
        and
        app.player_team is None
    ):
        load_species()
        if app.team_select_index == 0:
            app.player_team = [
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
            app.player_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data in
                app.selected_team_data["pokemon"]
            ]
        for pokemon in app.player_team:
            pokemon.set_level(app.option_level)
        if is_lan_battle:
            app.TEAM_SELECT_team_sent = False
        else:
            if app.game_mode == "ENDLESS":
                start_next_endless_battle()
            elif app.game_mode == "TOURNAMENT":
                trainer = app.tournament_current_trainer
                app.selected_trainer_data = trainer
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in trainer["team"]
                ]
            elif (
                app.single_battle_mode
                == "RANDOM_TEAM"
            ):
                app.opponent_team = [
                    Pokemon.from_species_number(
                        random.choice(
                            list(
                                SPECIES.keys()
                            )
                        )
                    )
                    for _ in range(6)
                ]
            elif (
                app.single_battle_mode
                == "MY_TEAM"
            ):
                selected_team_data = (
                    app.teams_data[
                        app.SINGLE_MENU_TRAINER_selected_team
                    ]
                )
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in
                    selected_team_data[
                        "pokemon"
                    ]
                ]
            elif (
                app.single_battle_mode
                == "TRAINER"
            ):
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in
                    app.selected_trainer_data[
                        "team"
                    ]
                ]
            for pokemon in app.opponent_team:
                pokemon.set_level(
                    app.option_level_npc
                )
            app.team_preview_return_state = (
                TEAM_SELECT
            )
            change_state(
                TEAM_PREVIEW
            )


def handle_event_BATTLE_START(event):
    pass

def handle_event_SPECIES_VIEW(event):
    if is_up(event):
        app.preview_index = max(
            0,
            app.preview_index - 1
        )
    elif is_down(event):
        app.preview_index = min(
            5,
            app.preview_index + 1
        )
    elif is_left(event):
        if app.option_omniscient:
            app.preview_column = 0
    elif is_right(event):
        if app.option_omniscient:
            app.preview_column = 1
    elif is_vy(event):
        if (
            app.SPECIES_VIEW_mode
            == "STATS"
        ):
            app.SPECIES_VIEW_mode = (
                "AFFINITIES"
            )
        else:
            app.SPECIES_VIEW_mode = (
                "STATS"
            )
    elif is_cancel(event):
        change_state(
            app.previous_state
        )
    if app.preview_column == 0:
        app.SPECIES_VIEW_pokemon = (
            app.player_team[
                app.preview_index
            ]
        )
    elif (
        app.option_omniscient
        and
        app.preview_index
        <
        len(app.opponent_team)
    ):
        app.SPECIES_VIEW_pokemon = (
            app.opponent_team[
                app.preview_index
            ]
        )

def handle_event_PKMN_VIEW(event):
    if is_up(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_index = max(
                0,
                app.PKMN_VIEW_index - 1
            )
        else:
            app.PKMN_VIEW_move_index = max(
                0,
                app.PKMN_VIEW_move_index - 1
            )
    elif is_down(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_index = min(
                5,
                app.PKMN_VIEW_index + 1
            )
        else:
            app.PKMN_VIEW_move_index = min(
                len(
                    app.PKMN_VIEW_pokemon.moves
                ) - 1,
                app.PKMN_VIEW_move_index + 1
            )
    elif is_left(event):

        if (
            app.PKMN_VIEW_move_index
            is None
            and
            app.option_omniscient
        ):
            
            if app.PKMN_VIEW_column == 0:
                app.PKMN_VIEW_column = 1
            else:
                app.PKMN_VIEW_column = 0

    elif is_right(event):

        if (
            app.PKMN_VIEW_move_index
            is None
            and
            app.option_omniscient
        ):
            if app.PKMN_VIEW_column == 0:
                app.PKMN_VIEW_column = 1
            else:
                app.PKMN_VIEW_column = 0
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
    if app.PKMN_VIEW_column == 0:
        app.PKMN_VIEW_pokemon = (
            app.player_team[
                app.PKMN_VIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        app.PKMN_VIEW_index
        <
        len(app.opponent_team)
    ):
        app.PKMN_VIEW_pokemon = (
            app.opponent_team[
                app.PKMN_VIEW_index
            ]
        )


def handle_event_TEAM_PREVIEW(event):
    if is_up(event):
        app.preview_index = max(
            0,
            app.preview_index - 1
        )
    elif is_down(event):
        app.preview_index = min(
            5,
            app.preview_index + 1
        )
    elif is_left(event):
        app.preview_column = 0
    elif is_right(event):
        if app.option_omniscient:
            app.preview_column = 1
    elif is_confirm(event):
        if app.preview_column == 0:
            app.player_lead = (
                app.preview_index
            )
            if (
                app.connection_socket
                is None
            ):
                change_state(
                    BATTLE_START
                )
    elif is_cvxy(event):
        if app.preview_column == 0:
            app.PKMN_VIEW_index = (
                app.preview_index
            )
            app.PKMN_VIEW_column = (
                app.preview_column
            )
            app.PKMN_VIEW_pokemon = (
                app.player_team[
                    app.preview_index
                ]
            )
            change_state(
                PKMN_VIEW
            )
        elif (
            app.option_omniscient
            and
            app.preview_index
            <
            len(app.opponent_team)
        ):
            app.PKMN_VIEW_index = (
                app.preview_index
            )
            app.PKMN_VIEW_column = (
                app.preview_column
            )
            app.PKMN_VIEW_pokemon = (
                app.opponent_team[
                    app.preview_index
                ]
            )
            change_state(
                PKMN_VIEW
            )
    elif is_cancel(event):
        if (
            app.game_mode
            == "ENDLESS"
        ):
            change_state(
                SINGLE_MENU
            )
        elif (
            app.allow_team_change
            and
            app.team_select_return_state
            is not None
        ):
            app.restore_team_select = True
            change_state(
                app.team_preview_return_state
            )
        
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
            change_state(SINGLE_MENU)
        elif app.LAUNCHER_MENU_index == 1:
            change_state(LAN_HOST_JOIN)
        elif app.LAUNCHER_MENU_index == 2:
            change_state(OPTIONS)

def handle_generic_team_select_navigation(
    move_direction
):

    app.team_select_index = max(
        0,
        min(
            len(app.available_teams) - 1,
            app.team_select_index + move_direction
        )
    )

    if (
        app.team_select_index
        < app.team_select_scroll
    ):
        app.team_select_scroll -= 1

    elif (
        app.team_select_index
        >= app.team_select_scroll + 7
    ):
        app.team_select_scroll += 1

    if app.team_select_index == 0:

        app.selected_team_data = None

        app.team_select_preview_team = []

        return

    team_index = (
        app.team_select_index - 1
    )

    app.selected_team_data = (
        app.teams_data[
            team_index
        ]
    )

    app.team_select_preview_team = [
        Pokemon.from_dict(
            pokemon_data
        )
        for pokemon_data in
        app.selected_team_data[
            "pokemon"
        ]
    ]