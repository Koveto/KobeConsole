from constants import *
from state import *

def handle_event(
    event
):

    if app.state == LAUNCHER_MENU:

        handle_event_LAUNCHER_MENU(
            event
        )

    elif app.state == LAN_HOST_JOIN:

        handle_event_LAN_HOST_JOIN(
            event
        )

    elif app.state == LAN_HOST:

        handle_event_LAN_HOST(
            event
        )

    elif app.state == LAN_JOIN:

        handle_event_LAN_JOIN(
            event
        )

    elif app.state == ONLINE_MENU:

        handle_event_ONLINE_MENU(
            event
        )

    elif app.state == ONLINE_HOST:

        handle_event_ONLINE_HOST(
            event
        )

    elif app.state == ONLINE_JOIN:

        handle_event_ONLINE_JOIN(
            event
        )

    elif app.state == TEAM_PREVIEW:

        handle_event_TEAM_PREVIEW(
            event
        )

    elif app.state == BATTLE_START:

        handle_event_BATTLE_START(
            event
        )

    elif app.state == TEAM_SELECT:

        if (
            app.TEAM_SELECT_mode
            == "SAVE"
        ):

            handle_event_TEAM_SELECT_save(
                event
            )

        else:

            handle_event_TEAM_SELECT(
                event
            )

    elif app.state == OPTIONS:

        handle_event_OPTIONS(
            event
        )

    elif app.state == KEYBOARD:

        handle_event_KEYBOARD(
            event
        )

    elif app.state == OPTIONS_MUSIC:

        handle_event_OPTIONS_MUSIC(
            event
        )

    elif app.state == SINGLE_MENU:

        handle_event_SINGLE_MENU(
            event
        )

    elif app.state == SINGLE_MENU_TRAINER:

        handle_event_SINGLE_MENU_TRAINER(
            event
        )

    elif app.state == BATTLE_END:

        handle_event_BATTLE_END(
            event
        )

    elif app.state == SINGLE_BRACKET:

        handle_event_SINGLE_BRACKET(
            event
        )

    elif app.state == SINGLE_DEFEND_GYM:

        handle_event_SINGLE_DEFEND_GYM(
            event
        )

    elif app.state == DAMAGE_CALCULATOR:

        handle_event_DAMAGE_CALCULATOR(
            event
        )

    elif app.state == PKMN_INFO:

        handle_event_PKMN_INFO(
            event
        )

    elif app.state == SPECIES_EDIT:

        handle_event_SPECIES_EDIT(
            event
        )

def handle_event_ONLINE_MENU(
    event
):

    if is_up(
        event
    ):

        app.ONLINE_MENU_index = max(
            0,
            app.ONLINE_MENU_index - 1
        )

    elif is_down(
        event
    ):

        app.ONLINE_MENU_index = min(
            1,
            app.ONLINE_MENU_index + 1
        )

    elif is_confirm(
        event
    ):

        if (
            app.ONLINE_MENU_index
            == 0
        ):

            change_state(
                ONLINE_HOST
            )

        else:

            change_state(
                ONLINE_JOIN
            )

    elif is_cancel(
        event
    ):

        disconnect_multiplayer()

        change_state(
            LAUNCHER_MENU
        )


def handle_event_ONLINE_HOST(
    event
):

    if is_cancel(
        event
    ):

        disconnect_multiplayer()

        change_state(
            ONLINE_MENU
        )


def handle_event_ONLINE_JOIN(
    event
):

    if (
        app.ONLINE_connected
    ):

        if is_cancel(
            event
        ):

            disconnect_multiplayer()

            change_state(
                ONLINE_MENU
            )

        return

    if is_confirm(
        event
    ):

        app.KEYBOARD_mode = (
            "ONLINE_ROOM_CODE"
        )

        app.KEYBOARD_return_state = (
            ONLINE_JOIN
        )

        app.KEYBOARD_team_index = None
        app.KEYBOARD_pokemon = None

        app.ONLINE_JOIN_entering_code = (
            True
        )

        app.ONLINE_error = None

        change_state(
            KEYBOARD
        )

    elif is_cancel(
        event
    ):

        disconnect_multiplayer()

        change_state(
            ONLINE_MENU
        )

def apply_species_edit_sort(
    sort_mode,
    preserve_species_number=None
):

    current_species_list = (
        app.SPECIES_EDIT_species_list
    )

    if (
        preserve_species_number
        is None
        and
        0
        <= app.SPECIES_EDIT_index
        < len(
            current_species_list
        )
    ):

        preserve_species_number = (
            current_species_list[
                app.SPECIES_EDIT_index
            ].no
        )

    species_list = (
        get_species_edit_base_list()
    )

    stat_sort = (
        app.SPECIES_EDIT_stat_sort
    )

    if stat_sort is not None:

        species_list = sorted(
            species_list,
            key=lambda species: (
                -get_species_edit_stat_value(
                    species,
                    stat_sort
                ),
                species.no
            )
        )

    elif sort_mode == "NAME":

        species_list = sorted(
            species_list,
            key=lambda species: (
                species.name.lower(),
                species.no
            )
        )

    else:

        sort_mode = "DEXNO"

        species_list = sorted(
            species_list,
            key=lambda species: species.no
        )

    app.SPECIES_EDIT_species_list = (
        species_list
    )

    app.SPECIES_EDIT_sort_mode = (
        sort_mode
    )

    app.SPECIES_EDIT_index = 0
    app.SPECIES_EDIT_scroll_row = 0

    if (
        preserve_species_number
        is not None
    ):

        selected_index = (
            find_species_edit_index(
                preserve_species_number
            )
        )

        if (
            selected_index
            is not None
        ):

            app.SPECIES_EDIT_index = (
                selected_index
            )

    sync_species_edit_scroll()

    rebuild_species_edit_preview()

    sync_species_edit_dex_to_selection()

    reset_species_edit_hold()

    app.SPECIES_EDIT_error = None

def cycle_species_edit_sort():

    current_species_number = None

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if (
        0
        <= app.SPECIES_EDIT_index
        < len(
            species_list
        )
    ):

        current_species_number = (
            species_list[
                app.SPECIES_EDIT_index
            ].no
        )

    app.SPECIES_EDIT_stat_sort = None

    if (
        app.SPECIES_EDIT_sort_mode
        == "DEXNO"
    ):

        new_sort_mode = "NAME"

    else:

        new_sort_mode = "DEXNO"

    apply_species_edit_sort(
        new_sort_mode,
        preserve_species_number=(
            current_species_number
        )
    )

def cycle_species_edit_type_filter(
    direction
):

    type_filters = (
        get_species_edit_type_filters()
    )

    if len(
        type_filters
    ) == 0:

        return

    current_filter = (
        app.SPECIES_EDIT_type_filter
    )

    if current_filter in type_filters:

        current_index = (
            type_filters.index(
                current_filter
            )
        )

    else:

        current_index = 0

    new_index = (
        current_index
        + direction
    ) % len(
        type_filters
    )

    preserve_species_number = None

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if (
        0
        <= app.SPECIES_EDIT_index
        < len(
            species_list
        )
    ):

        preserve_species_number = (
            species_list[
                app.SPECIES_EDIT_index
            ].no
        )

    app.SPECIES_EDIT_type_filter = (
        type_filters[
            new_index
        ]
    )

    apply_species_edit_sort(
        app.SPECIES_EDIT_sort_mode,
        preserve_species_number=(
            preserve_species_number
        )
    )



def get_species_edit_stat_sorts():

    return [
        None,
        "BST",
        "HP",
        "ATK",
        "DEF",
        "SPA",
        "SPD",
        "SPE"
    ]


def get_species_edit_stat_value(
    species,
    stat_sort
):

    if stat_sort == "BST":

        return sum(
            species.stats.values()
        )

    stat_keys = {
        "HP": "HP",
        "ATK": "Atk",
        "DEF": "Def",
        "SPA": "SpAtk",
        "SPD": "SpDef",
        "SPE": "Spd"
    }

    stat_key = (
        stat_keys.get(
            stat_sort
        )
    )

    if stat_key is None:

        return 0

    return species.stats.get(
        stat_key,
        0
    )

def cycle_species_edit_stat_sort(
    direction
):

    stat_sorts = (
        get_species_edit_stat_sorts()
    )

    if len(
        stat_sorts
    ) == 0:

        return

    current_stat_sort = (
        app.SPECIES_EDIT_stat_sort
    )

    if current_stat_sort in stat_sorts:

        current_index = (
            stat_sorts.index(
                current_stat_sort
            )
        )

    else:

        current_index = 0

    new_index = (
        current_index
        + direction
    ) % len(
        stat_sorts
    )

    preserve_species_number = None

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if (
        0
        <= app.SPECIES_EDIT_index
        < len(
            species_list
        )
    ):

        preserve_species_number = (
            species_list[
                app.SPECIES_EDIT_index
            ].no
        )

    app.SPECIES_EDIT_stat_sort = (
        stat_sorts[
            new_index
        ]
    )

    apply_species_edit_sort(
        app.SPECIES_EDIT_sort_mode,
        preserve_species_number=(
            preserve_species_number
        )
    )

def get_species_edit_type_filters():

    type_names = set()

    for species in SPECIES.values():

        for type_name in species.types:

            type_names.add(
                type_name
            )

    return [
        None
    ] + sorted(
        type_names
    )


def get_species_edit_base_list():

    species_list = list(
        SPECIES.values()
    )

    type_filter = (
        app.SPECIES_EDIT_type_filter
    )

    if type_filter is None:

        return species_list

    return [
        species
        for species in species_list
        if type_filter in species.types
    ]

def find_species_edit_index(
    species_number
):

    for index, species in enumerate(
        app.SPECIES_EDIT_species_list
    ):

        if (
            species.no
            == species_number
        ):

            return index

    return None


def get_species_edit_dex_number():

    digits = (
        app.SPECIES_EDIT_dex_digits
    )

    if len(
        digits
    ) != 3:

        return 0

    return (
        digits[0] * 100
        + digits[1] * 10
        + digits[2]
    )


def set_species_edit_dex_number(
    species_number
):

    species_number = max(
        0,
        min(
            999,
            species_number
        )
    )

    app.SPECIES_EDIT_dex_digits = [
        species_number // 100,
        (
            species_number
            // 10
        ) % 10,
        species_number % 10
    ]


def sync_species_edit_scroll():

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if len(
        species_list
    ) == 0:

        app.SPECIES_EDIT_index = 0
        app.SPECIES_EDIT_scroll_row = 0

        rebuild_species_edit_preview()

        return

    app.SPECIES_EDIT_index = max(
        0,
        min(
            len(
                species_list
            ) - 1,
            app.SPECIES_EDIT_index
        )
    )

    columns = max(
        1,
        app.SPECIES_EDIT_columns
    )

    visible_rows = max(
        1,
        app.SPECIES_EDIT_visible_rows
    )

    selected_row = (
        app.SPECIES_EDIT_index
        // columns
    )

    old_scroll_row = (
        app.SPECIES_EDIT_scroll_row
    )

    if (
        selected_row
        < app.SPECIES_EDIT_scroll_row
    ):

        app.SPECIES_EDIT_scroll_row = (
            selected_row
        )

    elif (
        selected_row
        >= (
            app.SPECIES_EDIT_scroll_row
            + visible_rows
        )
    ):

        app.SPECIES_EDIT_scroll_row = (
            selected_row
            - visible_rows
            + 1
        )

    max_row = (
        (
            len(
                species_list
            )
            - 1
        )
        // columns
    )

    max_scroll_row = max(
        0,
        max_row
        - visible_rows
        + 1
    )

    app.SPECIES_EDIT_scroll_row = max(
        0,
        min(
            max_scroll_row,
            app.SPECIES_EDIT_scroll_row
        )
    )

    if (
        app.SPECIES_EDIT_scroll_row
        != old_scroll_row
    ):

        rebuild_species_edit_preview()


def sync_species_edit_dex_to_selection():

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if not (
        0
        <= app.SPECIES_EDIT_index
        < len(
            species_list
        )
    ):

        return

    selected_species = (
        species_list[
            app.SPECIES_EDIT_index
        ]
    )

    set_species_edit_dex_number(
        selected_species.no
    )


def jump_species_edit_to_dex_number():

    desired_number = (
        get_species_edit_dex_number()
    )

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    exact_index = (
        find_species_edit_index(
            desired_number
        )
    )

    if exact_index is None:

        species_exists = any(

            species.no
            == desired_number

            for species
            in SPECIES.values()

        )

        if species_exists:

            app.SPECIES_EDIT_error = (
                "EXCLUDED BY FILTER"
            )

        else:

            app.SPECIES_EDIT_error = (
                "INVALID DEX NO."
            )

        return False

    old_scroll_row = (
        app.SPECIES_EDIT_scroll_row
    )

    app.SPECIES_EDIT_index = (
        exact_index
    )

    sync_species_edit_scroll()

    if (
        app.SPECIES_EDIT_scroll_row
        == old_scroll_row
    ):

        rebuild_species_edit_preview()

    sync_species_edit_dex_to_selection()

    app.SPECIES_EDIT_error = None

    reset_species_edit_hold()

    return True


def handle_species_edit_dex_mode(
    event
):

    if is_left(event):

        app.SPECIES_EDIT_dex_digit_index = max(
            0,
            app.SPECIES_EDIT_dex_digit_index - 1
        )

    elif is_right(event):

        app.SPECIES_EDIT_dex_digit_index = min(
            2,
            app.SPECIES_EDIT_dex_digit_index + 1
        )

    elif is_up(event):

        digit_index = (
            app.SPECIES_EDIT_dex_digit_index
        )

        app.SPECIES_EDIT_dex_digits[
            digit_index
        ] = (
            app.SPECIES_EDIT_dex_digits[
                digit_index
            ]
            + 1
        ) % 10

        app.SPECIES_EDIT_error = None

    elif is_down(event):

        digit_index = (
            app.SPECIES_EDIT_dex_digit_index
        )

        app.SPECIES_EDIT_dex_digits[
            digit_index
        ] = (
            app.SPECIES_EDIT_dex_digits[
                digit_index
            ]
            - 1
        ) % 10

        app.SPECIES_EDIT_error = None

    elif is_confirm(event):

        jumped = (
            jump_species_edit_to_dex_number()
        )

        if jumped:

            app.SPECIES_EDIT_dex_mode = (
                False
            )

    elif (
        is_cancel(event)
        or
        is_vy(event)
    ):

        app.SPECIES_EDIT_dex_mode = (
            False
        )

        app.SPECIES_EDIT_error = None

        sync_species_edit_dex_to_selection()

        reset_species_edit_hold()

def move_species_edit_selection(
    direction
):

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if len(
        species_list
    ) == 0:

        return False

    old_index = (
        app.SPECIES_EDIT_index
    )

    columns = max(
        1,
        app.SPECIES_EDIT_columns
    )

    if direction == "LEFT":

        app.SPECIES_EDIT_index = max(
            0,
            app.SPECIES_EDIT_index - 1
        )

    elif direction == "RIGHT":

        app.SPECIES_EDIT_index = min(
            len(
                species_list
            ) - 1,
            app.SPECIES_EDIT_index + 1
        )

    elif direction == "UP":

        app.SPECIES_EDIT_index = max(
            0,
            app.SPECIES_EDIT_index
            - columns
        )

    elif direction == "DOWN":

        new_index = (
            app.SPECIES_EDIT_index
            + columns
        )

        if (
            new_index
            < len(
                species_list
            )
        ):

            app.SPECIES_EDIT_index = (
                new_index
            )

        else:

            final_row_start = (
                (
                    len(
                        species_list
                    )
                    - 1
                )
                // columns
                * columns
            )

            target_column = (
                app.SPECIES_EDIT_index
                % columns
            )

            app.SPECIES_EDIT_index = min(
                len(
                    species_list
                ) - 1,
                final_row_start
                + target_column
            )

    else:

        return False

    if (
        app.SPECIES_EDIT_index
        == old_index
    ):

        return False

    sync_species_edit_scroll()

    sync_species_edit_dex_to_selection()

    app.SPECIES_EDIT_error = None

    return True

def handle_event_SPECIES_EDIT(
    event
):

    if (
        app.SPECIES_EDIT_dex_mode
    ):

        handle_species_edit_dex_mode(
            event
        )

        return

    if is_left_shoulder_back(
        event
    ):

        cycle_species_edit_type_filter(
            -1
        )

        return

    if is_right_shoulder_back(
        event
    ):

        cycle_species_edit_type_filter(
            1
        )

        return

    if is_minus(event):

        cycle_species_edit_stat_sort(
            -1
        )

        return

    if is_plus(event):

        cycle_species_edit_stat_sort(
            1
        )

        return

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    if len(
        species_list
    ) == 0:

        if is_cancel(event):

            close_species_edit()

        return

    if is_cx(event):

        cycle_species_edit_sort()

        return

    if is_vy(event):

        sync_species_edit_dex_to_selection()

        app.SPECIES_EDIT_dex_mode = (
            True
        )

        app.SPECIES_EDIT_dex_digit_index = (
            0
        )

        app.SPECIES_EDIT_error = None

        reset_species_edit_hold()

        return

    if is_left(event):

        move_species_edit_selection(
            "LEFT"
        )

    elif is_right(event):

        move_species_edit_selection(
            "RIGHT"
        )

    elif is_up(event):

        move_species_edit_selection(
            "UP"
        )

    elif is_down(event):

        move_species_edit_selection(
            "DOWN"
        )

    elif is_confirm(event):

        pokemon = (
            app.SPECIES_EDIT_pokemon
        )

        if pokemon is None:

            app.SPECIES_EDIT_error = (
                "NO POKEMON"
            )

            return

        if not (
            0
            <= app.SPECIES_EDIT_index
            < len(
                species_list
            )
        ):

            app.SPECIES_EDIT_error = (
                "INVALID SPECIES"
            )

            return

        selected_species = (
            species_list[
                app.SPECIES_EDIT_index
            ]
        )

        pokemon.set_species(
            selected_species
        )

        app.PKMN_INFO_pokemon = (
            pokemon
        )

        save_pkmn_info_pokemon()

        close_species_edit()

        return

    elif is_cancel(event):

        close_species_edit()

        return

def get_pkmn_info_source_team():

    if (
        app.PKMN_INFO_source
        == "TEAMBUILDER"
    ):

        return (
            app.TEAM_SELECT_preview_team
        )

    if (
        app.PKMN_INFO_source
        == "TEAM_PREVIEW"
    ):

        if (
            app.TEAM_PREVIEW_column
            == 0
        ):

            return (
                app.player_team
                or []
            )

        return (
            app.opponent_team
            or []
        )

    return []


def load_pkmn_info_pokemon(
    pokemon
):

    if pokemon is None:
        return False

    app.PKMN_INFO_pokemon = (
        Pokemon.from_pokemon(
            pokemon
        )
    )

    app.PKMN_INFO_mode = (
        "MAIN"
    )

    app.PKMN_INFO_error = None
    app.PKMN_INFO_selecting_move = False

    return True

def navigate_pkmn_info_team(
    direction
):

    if (
        app.PKMN_INFO_source
        == "TEAMBUILDER"
    ):

        team_index = (
            app.PKMN_INFO_team_index
        )

        current_index = (
            app.PKMN_INFO_pokemon_index
        )

        if (
            team_index is None
            or
            current_index is None
        ):

            return False

        save_pkmn_info_pokemon()

        save_data = load_save()

        if not (
            0
            <= team_index
            < len(
                save_data["teams"]
            )
        ):

            return False

        team_data = (
            save_data["teams"][
                team_index
            ]["pokemon"]
        )

        if len(
            team_data
        ) == 0:

            return False

        new_index = max(
            0,
            min(
                len(team_data) - 1,
                current_index + direction
            )
        )

        if (
            new_index
            == current_index
        ):

            return False

        new_pokemon = (
            Pokemon.from_dict(
                team_data[
                    new_index
                ]
            )
        )

        app.PKMN_INFO_pokemon_index = (
            new_index
        )

        app.TEAM_SELECT_pokemon_index = (
            new_index
        )

        app.TEAM_SELECT_preview_team = [

            Pokemon.from_dict(
                pokemon_data
            )

            for pokemon_data
            in team_data

        ]

        app.PKMN_INFO_species = False
        app.PKMN_INFO_editable = True

        return load_pkmn_info_pokemon(
            new_pokemon
        )

    if (
        app.PKMN_INFO_source
        == "TEAM_PREVIEW"
    ):

        player_team = (
            app.player_team
            or []
        )

        opponent_team = (
            app.opponent_team
            or []
        )

        visible_entries = []

        for pokemon_index, pokemon in enumerate(
            player_team
        ):

            visible_entries.append(
                {
                    "column": 0,
                    "index": pokemon_index,
                    "pokemon": pokemon
                }
            )

        if app.option_omniscient:

            for pokemon_index, pokemon in enumerate(
                opponent_team
            ):

                visible_entries.append(
                    {
                        "column": 1,
                        "index": pokemon_index,
                        "pokemon": pokemon
                    }
                )

        if len(
            visible_entries
        ) == 0:

            return False

        current_position = None

        for position, entry in enumerate(
            visible_entries
        ):

            if (
                entry["column"]
                == app.TEAM_PREVIEW_column
                and
                entry["index"]
                == app.TEAM_PREVIEW_index
            ):

                current_position = (
                    position
                )

                break

        if current_position is None:

            current_position = 0

        new_position = max(
            0,
            min(
                len(visible_entries) - 1,
                current_position + direction
            )
        )

        if (
            new_position
            == current_position
        ):

            return False

        new_entry = (
            visible_entries[
                new_position
            ]
        )

        app.TEAM_PREVIEW_column = (
            new_entry["column"]
        )

        app.TEAM_PREVIEW_index = (
            new_entry["index"]
        )

        app.PKMN_INFO_species = False
        app.PKMN_INFO_editable = False

        return load_pkmn_info_pokemon(
            new_entry["pokemon"]
        )

    return False

def handle_event_PKMN_INFO_species(
    event
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:

        if is_cancel(event):

            change_state(
                app.PKMN_INFO_return_state
            )

        return

    if is_left_shoulder_back(
        event
    ):

        navigate_pkmn_info_source(
            -1
        )

        return

    if is_right_shoulder_back(
        event
    ):

        navigate_pkmn_info_source(
            1
        )

        return

    if (
        app.PKMN_INFO_mode
        == "MOVES"
    ):

        learnset_size = len(
            pokemon.learnset
        )

        if learnset_size == 0:

            if is_cancel(event):

                app.PKMN_INFO_mode = (
                    "MAIN"
                )

                app.PKMN_INFO_index = 3

            return

        if is_up(event):

            app.PKMN_INFO_learnset_index = max(
                0,
                app.PKMN_INFO_learnset_index - 1
            )

        elif is_down(event):

            app.PKMN_INFO_learnset_index = min(
                learnset_size - 1,
                app.PKMN_INFO_learnset_index + 1
            )

        elif (
            is_cancel(event)
            or
            is_confirm(event)
            and
            app.PKMN_INFO_learnset_index
            == learnset_size
        ):

            app.PKMN_INFO_mode = (
                "MAIN"
            )

            app.PKMN_INFO_index = 3

        return

    if is_left(event):

        if (
            app.PKMN_INFO_index
            == 4
        ):

            app.PKMN_INFO_index = 3

    elif is_right(event):

        if (
            app.PKMN_INFO_index
            == 3
        ):

            app.PKMN_INFO_index = 4

    elif is_confirm(event):

        if (
            app.PKMN_INFO_index
            == 3
        ):

            app.PKMN_INFO_mode = (
                "MOVES"
            )

            app.PKMN_INFO_learnset_index = 0
            app.PKMN_INFO_error = None

    elif is_cancel(event):

        change_state(
            app.PKMN_INFO_return_state
        )


def switch_pkmn_info_calculator_side():

    source = (
        app.PKMN_INFO_source
    )

    if (
        source
        == "DAMAGE_CALCULATOR_ATTACKER"
    ):

        save_pkmn_info_pokemon()

        defender = (
            app.DAMAGE_CALCULATOR_defender
        )

        if defender is None:
            return False

        app.PKMN_INFO_source = (
            "DAMAGE_CALCULATOR_DEFENDER"
        )

        app.DAMAGE_CALCULATOR_column = 2

        return load_pkmn_info_pokemon(
            defender
        )

    if (
        source
        == "DAMAGE_CALCULATOR_DEFENDER"
    ):

        save_pkmn_info_pokemon()

        attacker = (
            app.DAMAGE_CALCULATOR_attacker
        )

        if attacker is None:
            return False

        app.PKMN_INFO_source = (
            "DAMAGE_CALCULATOR_ATTACKER"
        )

        app.DAMAGE_CALCULATOR_column = 0

        return load_pkmn_info_pokemon(
            attacker
        )

    return False


def navigate_pkmn_info_source(
    direction
):

    if (
        app.PKMN_INFO_source
        in (
            "TEAMBUILDER",
            "TEAM_PREVIEW"
        )
    ):

        return navigate_pkmn_info_team(
            direction
        )

    if (
        app.PKMN_INFO_source
        in (
            "DAMAGE_CALCULATOR_ATTACKER",
            "DAMAGE_CALCULATOR_DEFENDER"
        )
    ):

        return switch_pkmn_info_calculator_side()

    return False

def handle_event_PKMN_INFO_stats(
    event
):

    if is_cx(event):

        cycle_pkmn_info_info_mode()

        return

    if is_up(event):

        app.PKMN_INFO_stats_index = max(
            0,
            app.PKMN_INFO_stats_index - 1
        )

        app.PKMN_INFO_error = None

    elif is_down(event):

        app.PKMN_INFO_stats_index = min(
            9,
            app.PKMN_INFO_stats_index + 1
        )

        app.PKMN_INFO_error = None

    elif is_left(event):

        if (
            not app.PKMN_INFO_editable
            and
            app.PKMN_INFO_stats_index
            != 0
        ):

            return

        if (
            app.PKMN_INFO_stats_index
            == 0
        ):

            cycle_pkmn_info_info_mode()

        elif (
            app.PKMN_INFO_stats_index
            == 1
        ):

            change_pkmn_info_nature(
                -1
            )

        elif (
            app.PKMN_INFO_stats_index
            == 2
        ):

            adjust_pkmn_info_level(
                -1
            )

        elif (
            3
            <= app.PKMN_INFO_stats_index
            <= 8
        ):

            app.PKMN_INFO_ev_index = (
                app.PKMN_INFO_stats_index
                - 3
            )

            adjust_pkmn_info_ev(
                -1
            )

    elif is_right(event):

        if (
            not app.PKMN_INFO_editable
            and
            app.PKMN_INFO_stats_index
            != 0
        ):

            return

        if (
            app.PKMN_INFO_stats_index
            == 0
        ):

            cycle_pkmn_info_info_mode()

        elif (
            app.PKMN_INFO_stats_index
            == 1
        ):

            change_pkmn_info_nature(
                1
            )

        elif (
            app.PKMN_INFO_stats_index
            == 2
        ):

            adjust_pkmn_info_level(
                1
            )

        elif (
            3
            <= app.PKMN_INFO_stats_index
            <= 8
        ):

            app.PKMN_INFO_ev_index = (
                app.PKMN_INFO_stats_index
                - 3
            )

            adjust_pkmn_info_ev(
                1
            )

    elif is_confirm(event):

        if (
            app.PKMN_INFO_stats_index
            == 0
        ):

            cycle_pkmn_info_info_mode()

        elif (
            app.PKMN_INFO_stats_index
            == 9
        ):

            app.PKMN_INFO_mode = (
                "MAIN"
            )

            app.PKMN_INFO_index = 4
            app.PKMN_INFO_error = None

    elif is_cancel(event):

        app.PKMN_INFO_mode = (
            "MAIN"
        )

        app.PKMN_INFO_index = 4
        app.PKMN_INFO_error = None

def handle_event_PKMN_INFO_moves(
    event
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:

        app.PKMN_INFO_mode = (
            "MAIN"
        )

        return

    if (
        app.PKMN_INFO_selecting_move
    ):

        learnset_size = len(
            pokemon.learnset
        )

        if learnset_size == 0:

            if is_cancel(event):

                app.PKMN_INFO_selecting_move = (
                    False
                )

                app.PKMN_INFO_error = None

            return

        if is_up(event):

            app.PKMN_INFO_learnset_index = max(
                0,
                app.PKMN_INFO_learnset_index - 1
            )

            app.PKMN_INFO_error = None

        elif is_down(event):

            app.PKMN_INFO_learnset_index = min(
                learnset_size - 1,
                app.PKMN_INFO_learnset_index + 1
            )

            app.PKMN_INFO_error = None

        elif is_confirm(event):

            if not app.PKMN_INFO_editable:
                return

            selected_move = (
                pokemon.learnset[
                    app.PKMN_INFO_learnset_index
                ]
            )

            move_is_duplicate = any(

                index
                != app.PKMN_INFO_move_index

                and

                known_move.name
                == selected_move.name

                for index, known_move
                in enumerate(
                    pokemon.moves
                )

            )

            if move_is_duplicate:

                app.PKMN_INFO_error = (
                    "MOVE ALREADY KNOWN"
                )

                return

            pokemon.set_move(
                app.PKMN_INFO_move_index,
                selected_move
            )

            save_pkmn_info_pokemon()

            app.PKMN_INFO_error = None

            app.PKMN_INFO_selecting_move = (
                False
            )

        elif is_cancel(event):

            app.PKMN_INFO_selecting_move = (
                False
            )

            app.PKMN_INFO_error = None

        return

    if is_up(event):

        app.PKMN_INFO_move_index = max(
            0,
            app.PKMN_INFO_move_index - 1
        )

    elif is_down(event):

        app.PKMN_INFO_move_index = min(
            4,
            app.PKMN_INFO_move_index + 1
        )

    elif is_confirm(event):

        if (
            app.PKMN_INFO_move_index
            == 4
        ):

            app.PKMN_INFO_mode = (
                "MAIN"
            )

            app.PKMN_INFO_index = 3
            app.PKMN_INFO_error = None

            return

        if not app.PKMN_INFO_editable:
            return

        if not (
            0
            <= app.PKMN_INFO_move_index
            < len(
                pokemon.moves
            )
        ):

            return

        if len(
            pokemon.learnset
        ) == 0:

            return

        current_move = (
            pokemon.moves[
                app.PKMN_INFO_move_index
            ]
        )

        app.PKMN_INFO_learnset_index = 0

        for index, move in enumerate(
            pokemon.learnset
        ):

            if (
                move.name
                == current_move.name
            ):

                app.PKMN_INFO_learnset_index = (
                    index
                )

                break

        app.PKMN_INFO_selecting_move = (
            True
        )

        app.PKMN_INFO_error = None

    elif is_cancel(event):

        app.PKMN_INFO_mode = (
            "MAIN"
        )

        app.PKMN_INFO_index = 3
        app.PKMN_INFO_error = None

def handle_event_PKMN_INFO_main(
    event
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:

        if is_cancel(event):

            change_state(
                app.PKMN_INFO_return_state
            )

        return

    if is_left_shoulder_back(
        event
    ):

        navigate_pkmn_info_source(
            -1
        )

        return

    if is_right_shoulder_back(
        event
    ):

        navigate_pkmn_info_source(
            1
        )

        return

    if is_cx(event):

        cycle_pkmn_info_info_mode()

        return

    if not app.PKMN_INFO_editable:

        if is_left(event):

            if (
                app.PKMN_INFO_index
                == 4
            ):

                app.PKMN_INFO_index = 3

        elif is_right(event):

            if (
                app.PKMN_INFO_index
                == 3
            ):

                app.PKMN_INFO_index = 4

        elif is_confirm(event):

            if (
                app.PKMN_INFO_index
                == 3
            ):

                app.PKMN_INFO_mode = (
                    "MOVES"
                )

                app.PKMN_INFO_move_index = 0
                app.PKMN_INFO_learnset_index = 0
                app.PKMN_INFO_selecting_move = False
                app.PKMN_INFO_error = None

            elif (
                app.PKMN_INFO_index
                == 4
            ):

                app.PKMN_INFO_mode = (
                    "STATS"
                )

                app.PKMN_INFO_stats_index = 0
                app.PKMN_INFO_error = None

        elif is_cancel(event):

            change_state(
                app.PKMN_INFO_return_state
            )

        return

    if is_up(event):

        if (
            app.PKMN_INFO_index
            in (
                3,
                4
            )
        ):

            app.PKMN_INFO_index = 2

        else:

            app.PKMN_INFO_index = max(
                0,
                app.PKMN_INFO_index - 1
            )

    elif is_down(event):

        if (
            app.PKMN_INFO_index
            < 2
        ):

            app.PKMN_INFO_index += 1

        elif (
            app.PKMN_INFO_index
            == 2
        ):

            app.PKMN_INFO_index = 3

    elif is_left(event):

        if (
            app.PKMN_INFO_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_info_pokemon()

        elif (
            app.PKMN_INFO_index
            == 4
        ):

            app.PKMN_INFO_index = 3

    elif is_right(event):

        if (
            app.PKMN_INFO_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_info_pokemon()

        elif (
            app.PKMN_INFO_index
            == 3
        ):

            app.PKMN_INFO_index = 4

    elif is_confirm(event):

        if (
            app.PKMN_INFO_index
            == 0
        ):

            open_species_edit(
                pokemon=pokemon,
                return_state=PKMN_INFO
            )

        elif (
            app.PKMN_INFO_index
            == 1
        ):

            app.KEYBOARD_mode = (
                "POKEMON_NICKNAME"
            )

            app.KEYBOARD_return_state = (
                PKMN_INFO
            )

            app.KEYBOARD_team_index = None

            app.KEYBOARD_pokemon = (
                pokemon
            )

            change_state(
                KEYBOARD
            )

        elif (
            app.PKMN_INFO_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_info_pokemon()

        elif (
            app.PKMN_INFO_index
            == 3
        ):

            app.PKMN_INFO_mode = (
                "MOVES"
            )

            app.PKMN_INFO_move_index = 0
            app.PKMN_INFO_learnset_index = 0
            app.PKMN_INFO_selecting_move = False
            app.PKMN_INFO_error = None

        elif (
            app.PKMN_INFO_index
            == 4
        ):

            app.PKMN_INFO_mode = (
                "STATS"
            )

            app.PKMN_INFO_stats_index = 0
            app.PKMN_INFO_error = None

    elif is_cancel(event):

        save_pkmn_info_pokemon()

        change_state(
            app.PKMN_INFO_return_state
        )

def get_damage_calculator_save_pokemon():

    if (
        app.TEAM_SELECT_import_target
        == "ATTACKER"
    ):

        return (
            app.DAMAGE_CALCULATOR_attacker
        )

    if (
        app.TEAM_SELECT_import_target
        == "DEFENDER"
    ):

        return (
            app.DAMAGE_CALCULATOR_defender
        )

    return None


def save_damage_calculator_pokemon_to_team():

    pokemon = (
        get_damage_calculator_save_pokemon()
    )

    if pokemon is None:

        app.TEAM_SELECT_error = (
            "NO POKEMON TO SAVE"
        )

        return False

    team_index = (
        app.TEAM_SELECT_index
    )

    pokemon_index = (
        app.TEAM_SELECT_pokemon_index
    )

    save_data = load_save()

    if not (
        0
        <= team_index
        < len(
            save_data["teams"]
        )
    ):

        app.TEAM_SELECT_error = (
            "INVALID TEAM"
        )

        return False

    team_pokemon = (
        save_data["teams"][
            team_index
        ]["pokemon"]
    )

    if not (
        0
        <= pokemon_index
        < len(
            team_pokemon
        )
    ):

        app.TEAM_SELECT_error = (
            "INVALID SLOT"
        )

        return False

    team_pokemon[
        pokemon_index
    ] = pokemon.to_dict()

    save_save(
        save_data
    )

    app.TEAM_SELECT_error = None

    return True


def handle_event_TEAM_SELECT_save(
    event
):

    if (
        app.TEAM_SELECT_selecting_pokemon
    ):

        if is_cancel(event):

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            app.TEAM_SELECT_error = None

            return

        if is_confirm(event):

            saved = (
                save_damage_calculator_pokemon_to_team()
            )

            if not saved:
                return

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            change_state(
                app.TEAM_SELECT_return_state
            )

            return

        handle_team_select_pokemon_navigation(
            event
        )

        return

    if is_up(event):

        handle_team_select_navigation(
            -1
        )

    elif is_down(event):

        handle_team_select_navigation(
            1
        )

    elif is_confirm(event):

        if len(
            app.TEAM_SELECT_preview_team
        ) == 0:

            app.TEAM_SELECT_error = (
                "TEAM HAS NO POKEMON"
            )

            return

        app.TEAM_SELECT_error = None

        app.TEAM_SELECT_selecting_pokemon = (
            True
        )

        app.TEAM_SELECT_pokemon_index = 0

    elif is_cancel(event):

        change_state(
            app.TEAM_SELECT_return_state
        )

def apply_battle_level_cap(
    team,
    level_cap
):

    for pokemon in team:

        battle_level = min(
            pokemon.level,
            level_cap
        )

        pokemon.set_level(
            battle_level
        )

def cycle_pkmn_info_info_mode():

    if (
        app.PKMN_INFO_info_mode
        == "ACTUAL"
    ):
        app.PKMN_INFO_info_mode = (
            "BASE"
        )

    elif (
        app.PKMN_INFO_info_mode
        == "BASE"
    ):
        app.PKMN_INFO_info_mode = (
            "EVS"
        )

    else:
        app.PKMN_INFO_info_mode = (
            "ACTUAL"
        )

    app.PKMN_INFO_error = None

def adjust_pkmn_info_level(
    direction
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:
        return

    new_level = max(
        Pokemon.MIN_LEVEL,
        min(
            Pokemon.MAX_LEVEL,
            pokemon.level + direction
        )
    )

    if new_level == pokemon.level:
        return

    pokemon.set_level(
        new_level
    )

    save_pkmn_info_pokemon()

def change_pkmn_info_nature(
    direction
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:
        return

    natures = list(
        NATURES.values()
    )

    nature_index = next(
        index
        for index, nature
        in enumerate(
            natures
        )
        if nature.name
        == pokemon.nature.name
    )

    nature_index = (
        nature_index + direction
    ) % len(
        natures
    )

    pokemon.nature = (
        natures[
            nature_index
        ]
    )

    pokemon.set_level(
        pokemon.level
    )

    save_pkmn_info_pokemon()

def adjust_pkmn_info_ev(
    direction
):

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:
        return

    evs = get_pkmn_info_evs(
        pokemon
    )

    ev_index = (
        app.PKMN_INFO_ev_index
    )

    if direction < 0:

        new_value = max(
            0,
            evs[ev_index] - 4
        )

        if (
            new_value
            == evs[ev_index]
        ):

            app.PKMN_INFO_error = (
                "STAT EV MIN 0"
            )

            return

        evs[ev_index] = (
            new_value
        )

        app.PKMN_INFO_error = None

        set_pkmn_info_evs(
            pokemon,
            evs
        )

        return

    if direction > 0:

        current_total = sum(
            evs
        )

        available_evs = (
            508 - current_total
        )

        increase = min(
            4,
            252 - evs[ev_index],
            available_evs
        )

        if increase <= 0:

            if (
                evs[ev_index]
                >= 252
            ):

                app.PKMN_INFO_error = (
                    "STAT EV MAX 252"
                )

            else:

                app.PKMN_INFO_error = (
                    "TOTAL EV MAX 508"
                )

            return

        evs[ev_index] += (
            increase
        )

        app.PKMN_INFO_error = None

        set_pkmn_info_evs(
            pokemon,
            evs
        )


def get_pkmn_info_evs(
    pokemon
):

    return [
        pokemon.hp_ev,
        pokemon.attack_ev,
        pokemon.defense_ev,
        pokemon.special_attack_ev,
        pokemon.special_defense_ev,
        pokemon.speed_ev
    ]


def set_pkmn_info_evs(
    pokemon,
    evs
):

    if pokemon is None:
        return

    pokemon.set_evs(
        evs
    )

    save_pkmn_info_pokemon()

def save_pkmn_info_pokemon():

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:

        return

    if (
        app.PKMN_INFO_source
        == "TEAMBUILDER"
    ):

        team_index = (
            app.PKMN_INFO_team_index
        )

        pokemon_index = (
            app.PKMN_INFO_pokemon_index
        )

        save_data = load_save()

        if (
            team_index is not None
            and
            pokemon_index is not None
            and
            0
            <= team_index
            < len(
                save_data["teams"]
            )
            and
            0
            <= pokemon_index
            < len(
                save_data["teams"][
                    team_index
                ]["pokemon"]
            )
        ):

            save_data["teams"][
                team_index
            ]["pokemon"][
                pokemon_index
            ] = (
                pokemon.to_dict()
            )

            save_save(
                save_data
            )

    elif (
        app.PKMN_INFO_source
        == "DAMAGE_CALCULATOR_ATTACKER"
    ):

        app.DAMAGE_CALCULATOR_attacker = (
            Pokemon.from_pokemon(
                pokemon
            )
        )

        save_damage_calculator(
            app.DAMAGE_CALCULATOR_attacker,
            app.DAMAGE_CALCULATOR_defender
        )

    elif (
        app.PKMN_INFO_source
        == "DAMAGE_CALCULATOR_DEFENDER"
    ):

        app.DAMAGE_CALCULATOR_defender = (
            Pokemon.from_pokemon(
                pokemon
            )
        )

        save_damage_calculator(
            app.DAMAGE_CALCULATOR_attacker,
            app.DAMAGE_CALCULATOR_defender
        )

def handle_team_select_pokemon_navigation(
    event
):

    team_size = len(
        app.TEAM_SELECT_preview_team
    )

    if team_size == 0:
        return

    max_index = (
        team_size - 1
    )

    if is_left(event):

        app.TEAM_SELECT_pokemon_index = max(
            0,
            app.TEAM_SELECT_pokemon_index - 1
        )

    elif is_right(event):

        app.TEAM_SELECT_pokemon_index = min(
            max_index,
            app.TEAM_SELECT_pokemon_index + 1
        )

    elif is_up(event):

        app.TEAM_SELECT_pokemon_index = max(
            0,
            app.TEAM_SELECT_pokemon_index - 2
        )

    elif is_down(event):

        new_index = (
            app.TEAM_SELECT_pokemon_index
            + 2
        )

        if new_index <= max_index:

            app.TEAM_SELECT_pokemon_index = (
                new_index
            )

        elif (
            app.TEAM_SELECT_pokemon_index
            % 2
            == 0
            and
            max_index % 2 == 1
        ):

            app.TEAM_SELECT_pokemon_index = (
                max_index
            )

def handle_event_PKMN_INFO(
    event
):

    if app.PKMN_INFO_species:

        handle_event_PKMN_INFO_species(
            event
        )

        return

    if (
        app.PKMN_INFO_mode
        == "MOVES"
    ):

        handle_event_PKMN_INFO_moves(
            event
        )

        return

    if (
        app.PKMN_INFO_mode
        == "STATS"
    ):

        handle_event_PKMN_INFO_stats(
            event
        )

        return

    handle_event_PKMN_INFO_main(
        event
    )

def generate_teambuilder_team():

    load_species()

    candidates = []

    for species in SPECIES.values():

        bst = sum(
            species.stats.values()
        )

        if bst > 480:

            candidates.append(
                species.no
            )

    if len(candidates) == 0:

        raise ValueError(
            "No species found with BST over 480"
        )

    return [

        Pokemon.from_species_number(
            random.choice(
                candidates
            )
        )

        for _ in range(6)

    ]

def complete_keyboard_entry():

    text = (
        app.KEYBOARD_text.strip()
    )

    if (
        app.KEYBOARD_mode
        == "ONLINE_ROOM_CODE"
    ):

        room_code = "".join(

            character

            for character
            in text.upper()

            if (
                character
                in ONLINE_ROOM_CODE_CHARACTERS
            )

        )

        if (
            len(
                room_code
            )
            != ONLINE_ROOM_CODE_LENGTH
        ):

            app.ONLINE_error = (
                "ENTER 6 LETTERS"
            )

            return False

        app.ONLINE_join_code = (
            room_code
        )

        app.ONLINE_JOIN_connect_requested = (
            True
        )

        app.ONLINE_JOIN_entering_code = (
            False
        )

        app.ONLINE_error = None

        app.KEYBOARD_text = ""

        change_state(
            ONLINE_JOIN
        )

        return True

    if len(
        text
    ) == 0:

        return False

    if (
        app.KEYBOARD_mode
        == "PLAYER_NAME"
    ):

        app.player_name = text

        save_player()

        change_state(
            OPTIONS
        )

        return True

    if (
        app.KEYBOARD_mode
        == "CREATE_TEAM"
    ):

        team = (
            generate_teambuilder_team()
        )

        save_data = (
            load_save()
        )

        save_data["teams"].insert(
            0,
            {
                "name": text,
                "pokemon": [
                    pokemon.to_dict()
                    for pokemon in team
                ]
            }
        )

        save_save(
            save_data
        )

        app.TEAM_SELECT_restore_index = 1
        app.TEAM_SELECT_restore_scroll = 0
        app.TEAM_SELECT_submenu = False

        change_state(
            TEAM_SELECT
        )

        return True

    if (
        app.KEYBOARD_mode
        == "RENAME_TEAM"
    ):

        team_index = (
            app.KEYBOARD_team_index
        )

        save_data = (
            load_save()
        )

        if (
            team_index is not None
            and
            0
            <= team_index
            < len(
                save_data["teams"]
            )
        ):

            save_data["teams"][
                team_index
            ]["name"] = text

            save_save(
                save_data
            )

        app.TEAM_SELECT_restore_index = (
            team_index + 1
            if team_index is not None
            else 0
        )

        app.TEAM_SELECT_restore_scroll = (
            app.TEAM_SELECT_scroll
        )

        app.TEAM_SELECT_submenu = False

        change_state(
            TEAM_SELECT
        )

        return True

    if (
        app.KEYBOARD_mode
        == "POKEMON_NICKNAME"
    ):

        pokemon = (
            app.KEYBOARD_pokemon
        )

        if pokemon is None:

            return False

        pokemon.nickname = text

        app.PKMN_INFO_pokemon = (
            pokemon
        )

        app.KEYBOARD_pokemon = None

        save_pkmn_info_pokemon()

        change_state(
            PKMN_INFO
        )

        return True

    return False

def handle_event_DAMAGE_CALCULATOR(
    event
):

    if is_left(event):

        app.DAMAGE_CALCULATOR_column = max(
            0,
            app.DAMAGE_CALCULATOR_column - 1
        )

        app.DAMAGE_CALCULATOR_index = 0

    elif is_right(event):

        app.DAMAGE_CALCULATOR_column = min(
            2,
            app.DAMAGE_CALCULATOR_column + 1
        )

        app.DAMAGE_CALCULATOR_index = 0

    elif is_up(event):

        app.DAMAGE_CALCULATOR_index = max(
            0,
            app.DAMAGE_CALCULATOR_index - 1
        )

    elif is_down(event):

        if (
            app.DAMAGE_CALCULATOR_column
            == 1
        ):

            move_count = 0

            if (
                app.DAMAGE_CALCULATOR_attacker
                is not None
            ):

                move_count = len(
                    app.DAMAGE_CALCULATOR_attacker.moves
                )

            if move_count > 0:

                app.DAMAGE_CALCULATOR_index = min(
                    move_count - 1,
                    app.DAMAGE_CALCULATOR_index + 1
                )

        else:

            app.DAMAGE_CALCULATOR_index = min(
                2,
                app.DAMAGE_CALCULATOR_index + 1
            )

    elif is_cancel(event):

        change_state(
            LAUNCHER_MENU
        )

    elif is_confirm(event):

        if (
            app.DAMAGE_CALCULATOR_column
            == 0
        ):

            if (
                app.DAMAGE_CALCULATOR_index
                == 0
            ):

                open_team_select(
                    mode="IMPORT",
                    return_state=DAMAGE_CALCULATOR,
                    target="ATTACKER"
                )

            elif (
                app.DAMAGE_CALCULATOR_index
                == 1
            ):

                if (
                    app.DAMAGE_CALCULATOR_attacker
                    is None
                ):

                    return

                open_pokemon_details(
                    pokemon=(
                        app.DAMAGE_CALCULATOR_attacker
                    ),
                    editable=True,
                    return_state=DAMAGE_CALCULATOR,
                    source=(
                        "DAMAGE_CALCULATOR_ATTACKER"
                    )
                )

            elif (
                app.DAMAGE_CALCULATOR_index
                == 2
            ):

                if (
                    app.DAMAGE_CALCULATOR_attacker
                    is None
                ):

                    return

                open_team_select(
                    mode="SAVE",
                    return_state=DAMAGE_CALCULATOR,
                    target="ATTACKER"
                )

        elif (
            app.DAMAGE_CALCULATOR_column
            == 2
        ):

            if (
                app.DAMAGE_CALCULATOR_index
                == 0
            ):

                open_team_select(
                    mode="IMPORT",
                    return_state=DAMAGE_CALCULATOR,
                    target="DEFENDER"
                )

            elif (
                app.DAMAGE_CALCULATOR_index
                == 1
            ):

                if (
                    app.DAMAGE_CALCULATOR_defender
                    is None
                ):

                    return

                open_pokemon_details(
                    pokemon=(
                        app.DAMAGE_CALCULATOR_defender
                    ),
                    editable=True,
                    return_state=DAMAGE_CALCULATOR,
                    source=(
                        "DAMAGE_CALCULATOR_DEFENDER"
                    )
                )

            elif (
                app.DAMAGE_CALCULATOR_index
                == 2
            ):

                if (
                    app.DAMAGE_CALCULATOR_defender
                    is None
                ):

                    return

                open_team_select(
                    mode="SAVE",
                    return_state=DAMAGE_CALCULATOR,
                    target="DEFENDER"
                )

def ensure_gym_progress():

    save_data = load_save()

    gym_progress = save_data[
        "gym_progress"
    ]

    gyms_data = load_gyms()

    changed = False

    for gym in gyms_data[
        "gyms"
    ]:

        gym_type = gym["type"]

        if gym_type not in gym_progress:

            gym_progress[
                gym_type
            ] = [
                False,
                False,
                False
            ]

            changed = True

    if changed:

        save_save(
            save_data
        )

    return gym_progress

def generate_type_team(
    type_name
):

    load_species()

    candidates = []

    for species in (
        SPECIES.values()
    ):

        if (
            type_name
            in
            species.types
        ):

            candidates.append(
                species.no
            )

    random.shuffle(
        candidates
    )

    return [

        Pokemon.from_species_number(
            species_no
        )

        for species_no
        in
        candidates[:6]

    ]


def team_matches_type(
    team,
    required_type
):

    for pokemon in team:

        if (
            required_type
            not in
            pokemon.species.types
        ):

            return False

    return True

def get_num_completed_gyms():

    gym_progress = (
        ensure_gym_progress()
    )

    count = 0

    for progress in (
        gym_progress.values()
    ):

        if all(progress):

            count += 1

    return count

def handle_event_SINGLE_DEFEND_GYM(
    event
):

    if is_up(event):

        app.SINGLE_DEFEND_GYM_index = max(
            0,
            app.SINGLE_DEFEND_GYM_index - 1
        )

        if (
            app.SINGLE_DEFEND_GYM_index
            <
            app.SINGLE_DEFEND_GYM_scroll
        ):
            app.SINGLE_DEFEND_GYM_scroll -= 1

    elif is_down(event):

        app.SINGLE_DEFEND_GYM_index = min(
            len(app.gyms_data) - 1,
            app.SINGLE_DEFEND_GYM_index + 1
        )

        if (
            app.SINGLE_DEFEND_GYM_index
            >=
            app.SINGLE_DEFEND_GYM_scroll + 2
        ):
            app.SINGLE_DEFEND_GYM_scroll += 1

    elif is_left(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        current = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        app.SINGLE_DEFEND_GYM_trainer_indices[
            gym["type"]
        ] = max(
            0,
            current - 1
        )

    elif is_right(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        current = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        app.SINGLE_DEFEND_GYM_trainer_indices[
            gym["type"]
        ] = min(
            2,
            current + 1
        )

    elif is_confirm(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        trainer_index = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        trainer_name = (
            gym["challengers"][
                trainer_index
            ]
        )

        trainer = next(
            t
            for t
            in app.trainers_data
            if t["name"] == trainer_name
        )

        app.SINGLE_DEFEND_GYM_selected_gym = gym

        app.SINGLE_DEFEND_GYM_selected_type = (
            gym["type"]
        )

        app.SINGLE_DEFEND_GYM_selected_trainer = (
            trainer_name
        )

        app.selected_SINGLE_DEFEND_GYM_trainer_index = (
            trainer_index
        )

        app.selected_trainer_data = (
            trainer
        )

        app.allow_team_change = True

        app.allow_lead_change = True

        app.game_mode = (
            "DEFEND_GYM"
        )

        open_team_select(
            mode="BATTLE",
            return_state=SINGLE_DEFEND_GYM
        )

    elif is_cancel(event):

        change_state(
            SINGLE_MENU
        )

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

            app.allow_team_change = True
            app.allow_lead_change = True
            open_team_select(
                mode="BATTLE",
                return_state=SINGLE_BRACKET
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

        for pokemon_data
        in trainer["team"]

    ]

    apply_battle_level_cap(
        app.opponent_team,
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
        open_team_select(
            mode="BATTLE",
            return_state=SINGLE_MENU_TRAINER
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
    elif is_cvxy(event):

        if (
            app.option_omniscient
            and
            app.SINGLE_MENU_TRAINER_index == 2
        ):

            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )

            save_data = load_save()

            save_data["teams"].insert(
                0,
                {
                    "name": trainer["name"],
                    "pokemon": trainer["team"]
                }
            )

            save_save(
                save_data
            )

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
                app.allow_team_change = True
                app.allow_lead_change = True
                open_team_select(
                    mode="BATTLE",
                    return_state=SINGLE_MENU
                )
        elif app.SINGLE_MENU_index == 2:

            gyms_data = load_gyms()

            app.gyms_data = (
                gyms_data["gyms"]
            )

            change_state(
                SINGLE_DEFEND_GYM
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

def clamp_keyboard_cursor():

    app.KEYBOARD_row = max(
        0,
        min(
            len(
                KEYBOARD_GRID
            ) - 1,
            app.KEYBOARD_row
        )
    )

    current_row = (
        KEYBOARD_GRID[
            app.KEYBOARD_row
        ]
    )

    app.KEYBOARD_column = max(
        0,
        min(
            len(
                current_row
            ) - 1,
            app.KEYBOARD_column
        )
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

def handle_event_KEYBOARD(
    event
):

    is_room_code = (
        app.KEYBOARD_mode
        == "ONLINE_ROOM_CODE"
    )

    if is_room_code:

        text_limit = (
            ONLINE_ROOM_CODE_LENGTH
        )

    else:

        text_limit = 10

    #
    # Physical keyboard text input
    #

    if (
        event.type
        == pygame.TEXTINPUT
    ):

        set_active_input_device(
            INPUT_DEVICE_KEYBOARD
        )

        for character in event.text:

            if (
                len(
                    app.KEYBOARD_text
                )
                >= text_limit
            ):

                break

            if is_room_code:

                character = (
                    character.upper()
                )

                if (
                    character
                    not in ONLINE_ROOM_CODE_CHARACTERS
                ):

                    continue

            else:

                if (
                    not character.isalnum()
                    and
                    character != " "
                ):

                    continue

                character = (
                    character.upper()
                )

            app.KEYBOARD_text += (
                character
            )

        if is_room_code:

            app.ONLINE_error = None

        return

    #
    # Physical keyboard control keys
    #

    if (
        event.type
        == pygame.KEYDOWN
    ):

        set_active_input_device(
            INPUT_DEVICE_KEYBOARD
        )

        if (
            event.key
            == pygame.K_ESCAPE
        ):

            pygame.key.stop_text_input()

            if (
                app.KEYBOARD_mode
                == "POKEMON_NICKNAME"
            ):

                app.KEYBOARD_pokemon = None

            if is_room_code:

                app.ONLINE_JOIN_entering_code = (
                    False
                )

                app.ONLINE_JOIN_connect_requested = (
                    False
                )

                app.ONLINE_error = None

            if (
                app.KEYBOARD_return_state
                is not None
            ):

                change_state(
                    app.KEYBOARD_return_state
                )

            return

        if (
            event.key
            == pygame.K_RETURN
        ):

            completed = (
                complete_keyboard_entry()
            )

            if completed:

                pygame.key.stop_text_input()

            return

        if (
            event.key
            == pygame.K_BACKSPACE
        ):

            app.KEYBOARD_text = (
                app.KEYBOARD_text[:-1]
            )

            if is_room_code:

                app.ONLINE_error = None

            return

        if (
            event.key
            == pygame.K_UP
        ):

            app.KEYBOARD_row = max(
                0,
                app.KEYBOARD_row - 1
            )

            clamp_keyboard_cursor()

            return

        if (
            event.key
            == pygame.K_DOWN
        ):

            app.KEYBOARD_row = min(
                len(
                    KEYBOARD_GRID
                ) - 1,
                app.KEYBOARD_row + 1
            )

            clamp_keyboard_cursor()

            return

        if (
            event.key
            == pygame.K_LEFT
        ):

            app.KEYBOARD_column = max(
                0,
                app.KEYBOARD_column - 1
            )

            clamp_keyboard_cursor()

            return

        if (
            event.key
            == pygame.K_RIGHT
        ):

            current_row = (
                KEYBOARD_GRID[
                    app.KEYBOARD_row
                ]
            )

            app.KEYBOARD_column = min(
                len(
                    current_row
                ) - 1,
                app.KEYBOARD_column + 1
            )

            clamp_keyboard_cursor()

            return

        #
        # Characters are supplied by TEXTINPUT.
        #

        return

    #
    # Controller-only virtual keyboard
    #

    if (
        event.type
        not in (
            pygame.JOYBUTTONDOWN,
            pygame.JOYHATMOTION,
            pygame.JOYAXISMOTION
        )
    ):

        return

    if is_up(
        event
    ):

        app.KEYBOARD_row = max(
            0,
            app.KEYBOARD_row - 1
        )

    elif is_down(
        event
    ):

        app.KEYBOARD_row = min(
            len(
                KEYBOARD_GRID
            ) - 1,
            app.KEYBOARD_row + 1
        )

    elif is_left(
        event
    ):

        app.KEYBOARD_column = max(
            0,
            app.KEYBOARD_column - 1
        )

    elif is_right(
        event
    ):

        current_row = (
            KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
        )

        app.KEYBOARD_column = min(
            len(
                current_row
            ) - 1,
            app.KEYBOARD_column + 1
        )

    elif is_confirm(
        event
    ):

        current_row = (
            KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
        )

        app.KEYBOARD_column = min(
            app.KEYBOARD_column,
            len(
                current_row
            ) - 1
        )

        selected = (
            current_row[
                app.KEYBOARD_column
            ]
        )

        if (
            selected == "SPACE"
        ):

            if (
                not is_room_code
                and
                len(
                    app.KEYBOARD_text
                )
                < text_limit
            ):

                app.KEYBOARD_text += " "

        elif (
            selected == "BACK"
        ):

            app.KEYBOARD_text = (
                app.KEYBOARD_text[:-1]
            )

            if is_room_code:

                app.ONLINE_error = None

        elif (
            selected == "DONE"
        ):

            completed = (
                complete_keyboard_entry()
            )

            if completed:

                pygame.key.stop_text_input()

        elif (
            len(
                app.KEYBOARD_text
            )
            < text_limit
        ):

            app.KEYBOARD_text += (
                selected
            )

            if is_room_code:

                app.ONLINE_error = None

    elif is_cancel(
        event
    ):

        pygame.key.stop_text_input()

        if (
            app.KEYBOARD_mode
            == "POKEMON_NICKNAME"
        ):

            app.KEYBOARD_pokemon = None

        if is_room_code:

            app.ONLINE_JOIN_entering_code = (
                False
            )

            app.ONLINE_JOIN_connect_requested = (
                False
            )

            app.ONLINE_error = None

        if (
            app.KEYBOARD_return_state
            is not None
        ):

            change_state(
                app.KEYBOARD_return_state
            )

        return

    clamp_keyboard_cursor()

def handle_event_OPTIONS(event):
    if is_up(event):
        app.OPTIONS_index = max(0, app.OPTIONS_index - 1)
        if app.OPTIONS_index < app.OPTIONS_scroll:
            app.OPTIONS_scroll -= 1
    elif is_down(event):
        app.OPTIONS_index = min(8, app.OPTIONS_index + 1)
        if app.OPTIONS_index >= app.OPTIONS_scroll + 6:
            app.OPTIONS_scroll += 1
    elif is_left(event):
        if app.OPTIONS_index == 1:
            app.player_sprite -= 1
            if app.player_sprite < 0:
                app.player_sprite = 161
            save_player()
        elif app.OPTIONS_index == 7:
            app.option_level = max(1, app.option_level - 1)
            save_options()
        elif app.OPTIONS_index == 8:
            app.option_level_npc = max(1, app.option_level_npc - 1)
            save_options()
    elif is_right(event):
        if app.OPTIONS_index == 1:
            app.player_sprite += 1
            if app.player_sprite > 161:
                app.player_sprite = 0
            save_player()
        elif app.OPTIONS_index == 7:
            app.option_level = min(100, app.option_level + 1)
            save_options()
        elif app.OPTIONS_index == 8:
            app.option_level_npc = min(100, app.option_level_npc + 1)
            save_options()
    elif is_confirm(event):
        if app.OPTIONS_index == 0:

            app.KEYBOARD_mode = (
                "PLAYER_NAME"
            )

            app.KEYBOARD_return_state = (
                OPTIONS
            )

            app.KEYBOARD_team_index = None

            change_state(
                KEYBOARD
            )
        elif app.OPTIONS_index == 2:
            change_state(OPTIONS_MUSIC)
        elif app.OPTIONS_index == 3:
            app.option_omniscient = not app.option_omniscient
            save_options()
        elif app.OPTIONS_index == 4:
            app.option_pkmn_animation = not app.option_pkmn_animation
            save_options()
        elif app.OPTIONS_index == 5:
            app.option_fanart = (
                not app.option_fanart
            )
            save_options()
        elif app.OPTIONS_index == 6:
            app.option_music_shuffle = not app.option_music_shuffle
            save_options()
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)

def handle_event_TEAM_SELECT(event):
    if (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        if is_cancel(event):

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            return

        if is_confirm(event):

            team_index = (
                app.TEAM_SELECT_index - 1
            )

            pokemon_index = (
                app.TEAM_SELECT_pokemon_index
            )

            open_pokemon_details(
                pokemon=(
                    app.TEAM_SELECT_preview_team[
                        pokemon_index
                    ]
                ),
                editable=True,
                return_state=TEAM_SELECT,
                source="TEAMBUILDER",
                team_index=team_index,
                pokemon_index=pokemon_index
            )

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            app.TEAM_SELECT_restore_index = (
                app.TEAM_SELECT_index
            )

            app.TEAM_SELECT_restore_scroll = (
                app.TEAM_SELECT_scroll
            )

            return

        handle_team_select_pokemon_navigation(
            event
        )

        return
    if (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
        and
        app.TEAM_SELECT_submenu
    ):
        if is_up(event):

            app.TEAM_SELECT_submenu_index = max(
                0,
                app.TEAM_SELECT_submenu_index - 1
            )

        elif is_down(event):

            app.TEAM_SELECT_submenu_index = min(
                3,
                app.TEAM_SELECT_submenu_index + 1
            )

        elif is_cancel(event):

            app.TEAM_SELECT_submenu = False

        elif is_confirm(event):

            action = (
                TEAM_BUILDER_ACTIONS[
                    app.TEAM_SELECT_submenu_index
                ]
            )

            if action == "EDIT":

                if len(
                    app.TEAM_SELECT_preview_team
                ) == 0:

                    app.TEAM_SELECT_error = (
                        "TEAM HAS NO POKEMON"
                    )

                    app.TEAM_SELECT_submenu = False

                    return

                app.TEAM_SELECT_error = None

                app.TEAM_SELECT_submenu = False

                app.TEAM_SELECT_selecting_pokemon = (
                    True
                )

                app.TEAM_SELECT_pokemon_index = 0

            elif action == "RENAME":

                app.KEYBOARD_mode = (
                    "RENAME_TEAM"
                )

                app.KEYBOARD_return_state = (
                    TEAM_SELECT
                )

                app.KEYBOARD_team_index = (
                    app.TEAM_SELECT_index - 1
                )

                change_state(
                    KEYBOARD
                )

            elif action == "DUPLICATE":
                team = copy.deepcopy(
                    app.selected_team_data
                )

                save_data = load_save()

                save_data["teams"].insert(
                    0, team
                )

                save_save(
                    save_data
                )

                app.TEAM_SELECT_restore_index = 1
                app.TEAM_SELECT_restore_scroll = 0
                app.TEAM_SELECT_submenu = False

                change_state(
                    TEAM_SELECT
                )

            elif action == "ERASE":

                old_index = (
                    app.TEAM_SELECT_index
                )

                old_scroll = (
                    app.TEAM_SELECT_scroll
                )

                team_index = (
                    old_index - 1
                )

                save_data = load_save()

                if (
                    0
                    <= team_index
                    < len(
                        save_data["teams"]
                    )
                ):

                    del save_data[
                        "teams"
                    ][
                        team_index
                    ]

                    save_save(
                        save_data
                    )

                remaining_team_count = len(
                    save_data["teams"]
                )

                new_index = min(
                    old_index,
                    remaining_team_count
                )

                available_count = (
                    remaining_team_count
                    + 1
                )

                max_scroll = max(
                    0,
                    available_count - 7
                )

                new_scroll = min(
                    old_scroll,
                    max_scroll
                )

                if (
                    new_index
                    < new_scroll
                ):
                    new_scroll = (
                        new_index
                    )

                elif (
                    new_index
                    >= new_scroll + 7
                ):
                    new_scroll = max(
                        0,
                        new_index - 6
                    )

                app.TEAM_SELECT_restore_index = (
                    new_index
                )

                app.TEAM_SELECT_restore_scroll = (
                    new_scroll
                )

                app.TEAM_SELECT_submenu = False

                change_state(
                    TEAM_SELECT
                )
        
        return

    if (
        app.TEAM_SELECT_mode
        == "IMPORT"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        if is_cancel(event):

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            return

        if is_confirm(event):

            pokemon_index = (
                app.TEAM_SELECT_pokemon_index
            )

            selected_pokemon = (
                Pokemon.from_pokemon(
                    app.TEAM_SELECT_preview_team[
                        pokemon_index
                    ]
                )
            )

            if (
                app.TEAM_SELECT_import_target
                == "ATTACKER"
            ):

                app.DAMAGE_CALCULATOR_attacker = (
                    selected_pokemon
                )

            else:

                app.DAMAGE_CALCULATOR_defender = (
                    selected_pokemon
                )

            save_damage_calculator(
                app.DAMAGE_CALCULATOR_attacker,
                app.DAMAGE_CALCULATOR_defender
            )

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            change_state(
                app.TEAM_SELECT_return_state
            )

            return

        handle_team_select_pokemon_navigation(
            event
        )

        return
    is_lan_battle = app.connection_socket is not None
    if (
        is_up(event)
        and
        app.player_team is None
    ):
        handle_team_select_navigation(
            -1
        )
    elif (
        is_down(event)
        and
        app.player_team is None
    ):
        handle_team_select_navigation(
            1
        )
    elif is_cancel(event):

        if (
            app.connection_socket
            is None
        ):
            change_state(
                app.TEAM_SELECT_return_state
            )
    elif (
        is_confirm(event)
        and
        app.player_team is None
    ):
        if (
            app.TEAM_SELECT_mode
            == "TEAMBUILDER"
        ):

            if (
                app.TEAM_SELECT_index
                == 0
            ):

                app.KEYBOARD_mode = (
                    "CREATE_TEAM"
                )

                app.KEYBOARD_return_state = (
                    TEAM_SELECT
                )

                app.KEYBOARD_team_index = None

                change_state(
                    KEYBOARD
                )
            else:
                app.TEAM_SELECT_submenu = True
                app.TEAM_SELECT_submenu_index = 0

            return
        if (
            app.TEAM_SELECT_mode
            == "IMPORT"
        ):

            if len(
                app.TEAM_SELECT_preview_team
            ) == 0:

                app.TEAM_SELECT_error = (
                    "TEAM HAS NO POKEMON"
                )

                return

            app.TEAM_SELECT_error = None

            app.TEAM_SELECT_selecting_pokemon = (
                True
            )

            app.TEAM_SELECT_pokemon_index = 0

            return
        if (
            app.TEAM_SELECT_mode
            == "SAVE"
        ):

            # Save-mode slot selection will be added next.
            return
        load_species()
        if app.TEAM_SELECT_index == 0:

            if (
                app.game_mode
                == "DEFEND_GYM"
            ):

                app.player_team = (
                    generate_type_team(
                        app.SINGLE_DEFEND_GYM_selected_type
                    )
                )

            else:

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
                app.selected_team_data[
                    "pokemon"
                ]
            ]
        apply_battle_level_cap(
            app.player_team,
            app.option_level
        )
        if (
            app.game_mode
            == "DEFEND_GYM"
        ):

            if not team_matches_type(
                app.player_team,
                app.SINGLE_DEFEND_GYM_selected_type
            ):

                app.TEAM_SELECT_error = (
                    f"ONLY "
                    f"{app.SINGLE_DEFEND_GYM_selected_type.upper()} TYPES"
                )

                app.player_team = None

                return
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
                app.game_mode
                == "DEFEND_GYM"
            ):

                trainer = (
                    app.selected_trainer_data
                )

                app.opponent_team = [

                    Pokemon.from_dict(
                        pokemon_data
                    )

                    for pokemon_data
                    in
                    trainer["team"]

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
            apply_battle_level_cap(
                app.opponent_team,
                app.option_level_npc
            )
            app.TEAM_PREVIEW_return_state = (
                TEAM_SELECT
            )
            change_state(
                TEAM_PREVIEW
            )


def handle_event_BATTLE_START(
    event
):

    if not (
        app.BATTLE_initialized
    ):

        return

    if not is_confirm(
        event
    ):

        return

    if not (
        app.BATTLE_text_complete
    ):

        return

    if (
        not is_multiplayer_battle()
    ):

        change_state(
            BATTLE_END
        )

        return

    if (
        app.BATTLE_advance_requested
    ):

        return

    app.BATTLE_advance_requested = (
        True
    )

    if is_battle_authority():

        send_packet(
            {
                "type": "BATTLE_ADVANCE"
            }
        )

        change_state(
            BATTLE_END
        )

    else:

        sent = (
            send_packet(
                {
                    "type": (
                        "BATTLE_ADVANCE_REQUEST"
                    )
                }
            )
        )

        if not sent:

            app.BATTLE_advance_requested = (
                False
            )

def handle_event_TEAM_PREVIEW(
    event
):

    if is_up(event):

        current_team = (
            app.player_team
            if app.TEAM_PREVIEW_column == 0
            else app.opponent_team
        )

        team_size = len(
            current_team
            or []
        )

        if team_size > 0:

            app.TEAM_PREVIEW_index = max(
                0,
                min(
                    team_size - 1,
                    app.TEAM_PREVIEW_index - 1
                )
            )

    elif is_down(event):

        current_team = (
            app.player_team
            if app.TEAM_PREVIEW_column == 0
            else app.opponent_team
        )

        team_size = len(
            current_team
            or []
        )

        if team_size > 0:

            app.TEAM_PREVIEW_index = min(
                team_size - 1,
                app.TEAM_PREVIEW_index + 1
            )

    elif is_left(event):

        app.TEAM_PREVIEW_column = 0

        player_team_size = len(
            app.player_team
            or []
        )

        if player_team_size > 0:

            app.TEAM_PREVIEW_index = min(
                app.TEAM_PREVIEW_index,
                player_team_size - 1
            )

    elif is_right(event):

        if not app.option_omniscient:
            return

        opponent_team_size = len(
            app.opponent_team
            or []
        )

        if opponent_team_size > 0:

            app.TEAM_PREVIEW_column = 1

            app.TEAM_PREVIEW_index = min(
                app.TEAM_PREVIEW_index,
                opponent_team_size - 1
            )

    elif is_confirm(event):

        if (
            app.TEAM_PREVIEW_column
            == 0
        ):

            app.player_lead = (
                app.TEAM_PREVIEW_index
            )

            if (
                app.connection_socket
                is None
            ):

                change_state(
                    BATTLE_START
                )

    elif is_cvxy(event):

        pokemon = None

        if (
            app.TEAM_PREVIEW_column
            == 0
            and
            app.TEAM_PREVIEW_index
            < len(
                app.player_team
                or []
            )
        ):

            pokemon = (
                app.player_team[
                    app.TEAM_PREVIEW_index
                ]
            )

        elif (
            app.option_omniscient
            and
            app.TEAM_PREVIEW_column
            == 1
            and
            app.TEAM_PREVIEW_index
            < len(
                app.opponent_team
                or []
            )
        ):

            pokemon = (
                app.opponent_team[
                    app.TEAM_PREVIEW_index
                ]
            )

        if pokemon is not None:

            open_pokemon_details(
                pokemon=pokemon,
                editable=False,
                return_state=TEAM_PREVIEW,
                source="TEAM_PREVIEW",
                species=False
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
            app.TEAM_SELECT_return_state
            is not None
        ):

            app.restore_team_select = True

            change_state(
                app.TEAM_PREVIEW_return_state
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

def handle_event_LAUNCHER_MENU(
    event
):

    if is_up(
        event
    ):

        app.LAUNCHER_MENU_index = max(
            0,
            app.LAUNCHER_MENU_index - 1
        )

    elif is_down(
        event
    ):

        app.LAUNCHER_MENU_index = min(
            len(
                app.LAUNCHER_MENU_options
            ) - 1,
            app.LAUNCHER_MENU_index + 1
        )

    elif is_confirm(
        event
    ):

        if (
            app.LAUNCHER_MENU_index
            == 0
        ):

            change_state(
                SINGLE_MENU
            )

        elif (
            app.LAUNCHER_MENU_index
            == 1
        ):

            change_state(
                LAN_HOST_JOIN
            )

        elif (
            app.LAUNCHER_MENU_index
            == 2
        ):

            change_state(
                ONLINE_MENU
            )

        elif (
            app.LAUNCHER_MENU_index
            == 3
        ):

            load_species()

            calculator_data = (
                load_damage_calculator()
            )

            attacker_data = (
                calculator_data.get(
                    "attacker"
                )
            )

            defender_data = (
                calculator_data.get(
                    "defender"
                )
            )

            if attacker_data is not None:

                app.DAMAGE_CALCULATOR_attacker = (
                    Pokemon.from_dict(
                        attacker_data
                    )
                )

            else:

                app.DAMAGE_CALCULATOR_attacker = (
                    Pokemon.from_species_number(
                        6
                    )
                )

            if defender_data is not None:

                app.DAMAGE_CALCULATOR_defender = (
                    Pokemon.from_dict(
                        defender_data
                    )
                )

            else:

                app.DAMAGE_CALCULATOR_defender = (
                    Pokemon.from_species_number(
                        248
                    )
                )

            app.DAMAGE_CALCULATOR_index = 0
            app.DAMAGE_CALCULATOR_column = 1

            change_state(
                DAMAGE_CALCULATOR
            )

        elif (
            app.LAUNCHER_MENU_index
            == 4
        ):

            open_team_select(
                mode="TEAMBUILDER",
                return_state=LAUNCHER_MENU
            )

        elif (
            app.LAUNCHER_MENU_index
            == 5
        ):

            change_state(
                OPTIONS
            )

    elif is_cancel(
        event
    ):

        return

def handle_team_select_navigation(
    move_direction
):

    app.TEAM_SELECT_index = max(
        0,
        min(
            len(app.available_teams) - 1,
            app.TEAM_SELECT_index + move_direction
        )
    )

    if (
        app.TEAM_SELECT_index
        < app.TEAM_SELECT_scroll
    ):
        app.TEAM_SELECT_scroll -= 1

    elif (
        app.TEAM_SELECT_index
        >= app.TEAM_SELECT_scroll + 7
    ):
        app.TEAM_SELECT_scroll += 1

    if (
        app.TEAM_SELECT_mode
        not in (
            "IMPORT",
            "SAVE"
        )
        and
        app.TEAM_SELECT_index == 0
    ):

        app.selected_team_data = None

        app.TEAM_SELECT_preview_team = []

        return

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

    app.selected_team_data = (
        app.teams_data[
            team_index
        ]
    )

    app.TEAM_SELECT_preview_team = [
        Pokemon.from_dict(
            pokemon_data
        )
        for pokemon_data in
        app.selected_team_data[
            "pokemon"
        ]
    ]