from constants import *
from func import *
from pkmn import *
from save import *

def change_state(new_state):
    app.previous_state = app.state
    if  (new_state == LAN_HOST_JOIN):
        app.LAN_HOST_JOIN_index = 0
    if  (app.state == LAN_HOST_JOIN) and \
        (new_state == LAN_HOST):
        app.LAN_HOST_last_broadcast_time = 0
        app.LAN_HOST_ip_address = get_local_ip()
        app.LAN_HOST_server_socket = create_server(app.LAN_HOST_ip_address)
        app.LAN_HOST_client_socket = None
        app.LAN_HOST_connected = False
    if  (app.state == LAN_HOST_JOIN) and \
        (new_state == LAN_JOIN):
        app.LAN_JOIN_discovery_socket = (listen_for_hosts())
        app.LAN_JOIN_connected = False
        app.LAN_JOIN_discovered_host_ip = None
        app.LAN_JOIN_client_socket = None
    if  ((app.state == TEAM_SELECT)) and \
        (new_state == TEAM_PREVIEW):
        load_species()
        app.TEAM_PREVIEW_index = 0
        app.TEAM_PREVIEW_column = 0
        if (
            app.connection_socket
            is not None
        ):

            app.opponent_team = (
                app.TEAM_SELECT_opponent_team
            )
        app.player_lead = None
        app.opponent_lead = None
        app.TEAM_PREVIEW_ready_sent = False
        app.TEAM_PREVIEW_opponent_ready = False
    if (
        new_state == PKMN_EDIT
        and
        app.state != KEYBOARD
    ):
        app.PKMN_EDIT_index = 0
        app.PKMN_EDIT_mode = "MAIN"
        app.PKMN_EDIT_ev_index = 0
        app.PKMN_EDIT_stats_index = 0
        app.PKMN_EDIT_move_index = 0
        app.PKMN_EDIT_learnset_index = 0
        app.PKMN_EDIT_selecting_move = False
        app.PKMN_EDIT_error = None
        app.PKMN_EDIT_info_mode = "ACTUAL"
    if  (new_state == PKMN_VIEW):
        app.PKMN_VIEW_move_index = None
        app.PKMN_VIEW_mode = "STATS"
    if  (new_state == SPECIES_VIEW):
        app.SPECIES_VIEW_mode = "STATS"
    if new_state == TEAM_SELECT:

        app.TEAM_SELECT_error = None

        if app.restore_team_select:

            app.restore_team_select = False
            app.player_team = None

        else:

            app.player_team = None
            app.TEAM_SELECT_team_sent = False
            app.TEAM_SELECT_opponent_team = None
            app.TEAM_SELECT_submenu = False
            app.TEAM_SELECT_selecting_pokemon = False

            load_species()

            teams_data = load_teams()

            app.teams_data = (
                teams_data["teams"]
            )

            if (
                app.TEAM_SELECT_mode
                == "IMPORT"
            ):

                app.available_teams = [
                    team["name"]
                    for team
                    in app.teams_data
                ]

            elif (
                app.TEAM_SELECT_mode
                == "TEAMBUILDER"
            ):

                app.available_teams = [
                    "Create Team"
                ]

                for team in app.teams_data:

                    app.available_teams.append(
                        team["name"]
                    )

            else:

                app.available_teams = [
                    "Random Team"
                ]

                for team in app.teams_data:

                    app.available_teams.append(
                        team["name"]
                    )

            if (
                app.TEAM_SELECT_restore_index
                is not None
            ):

                desired_index = (
                    app.TEAM_SELECT_restore_index
                )

                desired_scroll = (
                    app.TEAM_SELECT_restore_scroll
                )

                app.TEAM_SELECT_restore_index = None
                app.TEAM_SELECT_restore_scroll = None

            else:

                desired_index = 0
                desired_scroll = 0

            if len(
                app.available_teams
            ) > 0:

                app.TEAM_SELECT_index = max(
                    0,
                    min(
                        desired_index,
                        len(
                            app.available_teams
                        ) - 1
                    )
                )

            else:

                app.TEAM_SELECT_index = 0

            max_scroll = max(
                0,
                len(
                    app.available_teams
                ) - 7
            )

            app.TEAM_SELECT_scroll = max(
                0,
                min(
                    desired_scroll,
                    max_scroll
                )
            )

            if (
                app.TEAM_SELECT_index
                < app.TEAM_SELECT_scroll
            ):

                app.TEAM_SELECT_scroll = (
                    app.TEAM_SELECT_index
                )

            elif (
                app.TEAM_SELECT_index
                >= app.TEAM_SELECT_scroll + 7
            ):

                app.TEAM_SELECT_scroll = max(
                    0,
                    app.TEAM_SELECT_index - 6
                )

            app.selected_team_data = None
            app.TEAM_SELECT_preview_team = []

            if (
                app.TEAM_SELECT_mode
                == "IMPORT"
            ):

                team_index = (
                    app.TEAM_SELECT_index
                )

            else:

                team_index = (
                    app.TEAM_SELECT_index - 1
                )

            if (
                0
                <= team_index
                < len(
                    app.teams_data
                )
            ):

                app.selected_team_data = (
                    app.teams_data[
                        team_index
                    ]
                )

                app.TEAM_SELECT_preview_team = [

                    Pokemon.from_dict(
                        pokemon_data
                    )

                    for pokemon_data
                    in app.selected_team_data[
                        "pokemon"
                    ]

                ]
    if  (new_state == OPTIONS):
        app.OPTIONS_scroll = 0
        app.OPTIONS_index = 0
    if  (new_state == KEYBOARD):

        app.KEYBOARD_row = 0
        app.KEYBOARD_column = 0

        if (
            app.KEYBOARD_mode
            == "PLAYER_NAME"
        ):

            app.KEYBOARD_text = (
                app.player_name
            )

        elif (
            app.KEYBOARD_mode
            == "RENAME_TEAM"
            and
            app.KEYBOARD_team_index
            is not None
        ):

            save_data = load_save()

            team_index = (
                app.KEYBOARD_team_index
            )

            if (
                0
                <= team_index
                < len(
                    save_data["teams"]
                )
            ):

                app.KEYBOARD_text = (
                    save_data["teams"][
                        team_index
                    ]["name"]
                )

            else:

                app.KEYBOARD_text = ""

        elif (
            app.KEYBOARD_mode
            == "POKEMON_NICKNAME"
            and
            app.KEYBOARD_pokemon
            is not None
        ):

            app.KEYBOARD_text = (
                app.KEYBOARD_pokemon.nickname
            )

        
        else:

            app.KEYBOARD_text = ""

    if  (new_state == OPTIONS_MUSIC):
        if new_state == OPTIONS_MUSIC:
            app.OPTIONS_MUSIC_index = 0
            app.OPTIONS_MUSIC_scroll = 0
            app.music_data = load_music_data()
    if  (new_state == SINGLE_MENU):
        app.SINGLE_MENU_index = 0
        trainers_data = load_trainers()
        app.trainers_data = trainers_data["trainers"]
    if  (new_state == SINGLE_MENU_TRAINER):
        if app.restore_single_menu_trainer:
            app.restore_single_menu_trainer = False
        else:
            app.SINGLE_MENU_TRAINER_index = 0
            app.single_battle_mode = None
            app.selected_trainer_data = None
            trainers_data = load_trainers()
            app.trainers_data = (
                trainers_data["trainers"]
            )
            teams_data = load_teams()
            app.teams_data = (
                teams_data["teams"]
            )
            app.teams_data = [
                team
                for team in app.teams_data
                if team["name"] != "Random Team"
            ]
            app.SINGLE_MENU_TRAINER_selected_trainer = 0
            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )

            app.SINGLE_MENU_TRAINER_preview_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data in
                trainer["team"]
            ]
            if len(app.teams_data) == 0:
                app.SINGLE_MENU_TRAINER_selected_team = None
            else:
                app.SINGLE_MENU_TRAINER_selected_team = 0
            app.SINGLE_MENU_TRAINER_my_team_preview = []

            if (
                app.SINGLE_MENU_TRAINER_selected_team
                is not None
            ):

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
                    
    app.state = new_state