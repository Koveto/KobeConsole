from constants import *
from func import *
from pkmn import *
from save import *

def consume_pkmn_info_request():

    request = (
        app.PKMN_INFO_pending_request
    )

    if request is None:
        return False

    source_pokemon = (
        request["pokemon"]
    )

    app.PKMN_INFO_pokemon = (
        Pokemon.from_pokemon(
            source_pokemon
        )
    )

    app.PKMN_INFO_editable = (
        request["editable"]
    )

    app.PKMN_INFO_species = (
        request["species"]
    )

    app.PKMN_INFO_return_state = (
        request["return_state"]
    )

    app.PKMN_INFO_source = (
        request["source"]
    )

    app.PKMN_INFO_team_index = (
        request["team_index"]
    )

    app.PKMN_INFO_pokemon_index = (
        request["pokemon_index"]
    )

    app.PKMN_INFO_pending_request = None

    return True

def open_pokemon_details(
    pokemon,
    editable,
    return_state,
    source=None,
    team_index=None,
    pokemon_index=None,
    species=False
):

    if pokemon is None:
        return

    app.PKMN_INFO_pending_request = {
        "pokemon": pokemon,
        "editable": editable,
        "species": species,
        "return_state": return_state,
        "source": source,
        "team_index": team_index,
        "pokemon_index": pokemon_index
    }

    change_state(
        PKMN_INFO
    )

def open_team_select(
    mode,
    return_state,
    target=None
):

    valid_modes = (
        "BATTLE",
        "TEAMBUILDER",
        "IMPORT",
        "SAVE"
    )

    if mode not in valid_modes:

        raise ValueError(
            f"Invalid TEAM_SELECT mode: {mode}"
        )

    app.TEAM_SELECT_pending_mode = (
        mode
    )

    app.TEAM_SELECT_pending_return_state = (
        return_state
    )

    app.TEAM_SELECT_pending_target = (
        target
    )

    change_state(
        TEAM_SELECT
    )


def consume_team_select_request(
    old_state
):

    if (
        app.TEAM_SELECT_pending_mode
        is not None
    ):

        app.TEAM_SELECT_mode = (
            app.TEAM_SELECT_pending_mode
        )

        app.TEAM_SELECT_return_state = (
            app.TEAM_SELECT_pending_return_state
        )

        if (
            app.TEAM_SELECT_mode
            in (
                "IMPORT",
                "SAVE"
            )
        ):

            app.TEAM_SELECT_import_target = (
                app.TEAM_SELECT_pending_target
            )

        else:

            app.TEAM_SELECT_import_target = (
                None
            )

        app.TEAM_SELECT_pending_mode = None
        app.TEAM_SELECT_pending_return_state = None
        app.TEAM_SELECT_pending_target = None

        return

    preserving_existing_mode = (
        old_state
        in (
            TEAM_SELECT,
            KEYBOARD,
            PKMN_INFO
        )
    )

    if not preserving_existing_mode:

        app.TEAM_SELECT_mode = (
            "BATTLE"
        )

        app.TEAM_SELECT_import_target = (
            None
        )


def load_team_select_data():

    load_species()

    teams_data = load_teams()

    app.teams_data = (
        teams_data["teams"]
    )

    if (
        app.TEAM_SELECT_mode
        in (
            "IMPORT",
            "SAVE"
        )
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


def restore_team_select_position():

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


def load_team_select_preview():

    app.selected_team_data = None

    app.TEAM_SELECT_preview_team = []

    if (
        app.TEAM_SELECT_mode
        in (
            "IMPORT",
            "SAVE"
        )
    ):

        team_index = (
            app.TEAM_SELECT_index
        )

    else:

        team_index = (
            app.TEAM_SELECT_index - 1
        )

    if not (
        0
        <= team_index
        < len(
            app.teams_data
        )
    ):

        return

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


def initialize_team_select(
    old_state
):

    consume_team_select_request(
        old_state
    )

    app.TEAM_SELECT_error = None

    if app.restore_team_select:

        app.restore_team_select = False

        app.player_team = None

        return

    app.player_team = None
    app.TEAM_SELECT_team_sent = False
    app.TEAM_SELECT_opponent_team = None
    app.TEAM_SELECT_submenu = False
    app.TEAM_SELECT_selecting_pokemon = False

    load_team_select_data()

    restore_team_select_position()

    load_team_select_preview()


def initialize_team_preview(
    old_state
):

    if old_state != TEAM_SELECT:
        return

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


def initialize_pkmn_info(
    old_state
):

    entered_with_request = (
        consume_pkmn_info_request()
    )

    returning_from_keyboard = (
        old_state == KEYBOARD
        and
        not entered_with_request
    )

    if returning_from_keyboard:
        return

    if (
        app.PKMN_INFO_pokemon
        is None
    ):
        return

    if app.PKMN_INFO_species:

        app.PKMN_INFO_editable = False

    if app.PKMN_INFO_editable:

        app.PKMN_INFO_index = 0

    else:

        app.PKMN_INFO_index = 3

    app.PKMN_INFO_mode = "MAIN"

    app.PKMN_INFO_ev_index = 0
    app.PKMN_INFO_stats_index = 0
    app.PKMN_INFO_move_index = 0
    app.PKMN_INFO_learnset_index = 0

    app.PKMN_INFO_selecting_move = False
    app.PKMN_INFO_error = None
    app.PKMN_INFO_info_mode = "ACTUAL"


def initialize_keyboard():

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


def initialize_options():

    app.OPTIONS_scroll = 0
    app.OPTIONS_index = 0


def initialize_options_music():

    app.OPTIONS_MUSIC_index = 0
    app.OPTIONS_MUSIC_scroll = 0

    app.music_data = (
        load_music_data()
    )


def initialize_single_menu():

    app.SINGLE_MENU_index = 0

    trainers_data = load_trainers()

    app.trainers_data = (
        trainers_data["trainers"]
    )


def initialize_single_menu_trainer():

    if app.restore_single_menu_trainer:

        app.restore_single_menu_trainer = False

        return

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

        for team
        in app.teams_data

        if team["name"]
        != "Random Team"

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

        for pokemon_data
        in trainer["team"]

    ]

    if len(
        app.teams_data
    ) == 0:

        app.SINGLE_MENU_TRAINER_selected_team = None

    else:

        app.SINGLE_MENU_TRAINER_selected_team = 0

    app.SINGLE_MENU_TRAINER_my_team_preview = []

    if (
        app.SINGLE_MENU_TRAINER_selected_team
        is None
    ):

        return

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
        in selected_team[
            "pokemon"
        ]

    ]


def initialize_lan_host_join():

    app.LAN_HOST_JOIN_index = 0


def initialize_lan_host(
    old_state
):

    if old_state != LAN_HOST_JOIN:
        return

    app.LAN_HOST_last_broadcast_time = 0

    app.LAN_HOST_ip_address = (
        get_local_ip()
    )

    app.LAN_HOST_server_socket = (
        create_server(
            app.LAN_HOST_ip_address
        )
    )

    app.LAN_HOST_client_socket = None
    app.LAN_HOST_connected = False


def initialize_lan_join(
    old_state
):

    if old_state != LAN_HOST_JOIN:
        return

    app.LAN_JOIN_discovery_socket = (
        listen_for_hosts()
    )

    app.LAN_JOIN_connected = False
    app.LAN_JOIN_discovered_host_ip = None
    app.LAN_JOIN_client_socket = None


def change_state(
    new_state
):

    old_state = (
        app.state
    )

    app.previous_state = (
        old_state
    )

    if new_state == LAN_HOST_JOIN:

        initialize_lan_host_join()

    elif new_state == LAN_HOST:

        initialize_lan_host(
            old_state
        )

    elif new_state == LAN_JOIN:

        initialize_lan_join(
            old_state
        )

    elif new_state == TEAM_SELECT:

        initialize_team_select(
            old_state
        )

    elif new_state == TEAM_PREVIEW:

        initialize_team_preview(
            old_state
        )

    elif new_state == PKMN_INFO:

        initialize_pkmn_info(
            old_state
        )

    elif new_state == OPTIONS:

        initialize_options()

    elif new_state == KEYBOARD:

        initialize_keyboard()

    elif new_state == OPTIONS_MUSIC:

        initialize_options_music()

    elif new_state == SINGLE_MENU:

        initialize_single_menu()

    elif new_state == SINGLE_MENU_TRAINER:

        initialize_single_menu_trainer()

    app.state = (
        new_state
    )