from constants import *
from func import *
from pkmn import *
from handle_event import *

cursor = None
bracket = None

def init_draw():
    global cursor
    global bracket

    cursor_filepath = os.path.join(
        TEXT_ROOT,
        "sprites",
        "cursor.png"
    )

    cursor = pygame.image.load(
        cursor_filepath
    ).convert()

    cursor.set_colorkey(
        COLOR_ALPHA_0
    )

    bracket_filepath = os.path.join(
        TEXT_ROOT,
        "sprites",
        "bracket.png"
    )

    bracket = pygame.image.load(
        bracket_filepath
    ).convert()

def get_display_sprite(
    pokemon
):

    if app.option_fanart:

        if (
            pokemon.front_sprite_anim_state
            and
            pokemon.fanart_front_1
            is not None
        ):
            return (
                pokemon.fanart_front_1
            )

        if (
            pokemon.fanart_front_0
            is not None
        ):
            return (
                pokemon.fanart_front_0
            )

    if (
        app.option_pkmn_animation
    ):
        return (
            pokemon.front_sprite_anim
        )

    return (
        pokemon.front_sprite
    )

def draw():

    if app.state == LAUNCHER_MENU:

        draw_LAUNCHER_MENU()

    elif app.state == LAN_HOST_JOIN:

        draw_LAN_HOST_JOIN()

    elif app.state == LAN_HOST:

        draw_LAN_HOST()

    elif app.state == LAN_JOIN:

        draw_LAN_JOIN()

    elif app.state == ONLINE_MENU:

        draw_ONLINE_MENU()

    elif app.state == ONLINE_HOST:

        draw_ONLINE_HOST()

    elif app.state == ONLINE_JOIN:

        draw_ONLINE_JOIN()

    elif app.state == TEAM_PREVIEW:

        draw_TEAM_PREVIEW()

    elif app.state == BATTLE_START:

        draw_BATTLE_START()

    elif app.state == TEAM_SELECT:

        draw_TEAM_SELECT()

    elif app.state == OPTIONS:

        draw_OPTIONS()

    elif app.state == KEYBOARD:

        draw_KEYBOARD()

    elif app.state == OPTIONS_MUSIC:

        draw_OPTIONS_MUSIC()

    elif app.state == SINGLE_MENU:

        draw_SINGLE_MENU()

    elif app.state == SINGLE_MENU_TRAINER:

        draw_SINGLE_MENU_TRAINER()

    elif app.state == BATTLE_END:

        draw_BATTLE_END()

    elif app.state == SINGLE_BRACKET:

        draw_SINGLE_BRACKET()

    elif app.state == SINGLE_DEFEND_GYM:

        draw_SINGLE_DEFEND_GYM()

    elif app.state == DAMAGE_CALCULATOR:

        draw_DAMAGE_CALCULATOR()

    elif app.state == PKMN_INFO:

        draw_PKMN_INFO()

    elif app.state == SPECIES_EDIT:

        draw_SPECIES_EDIT()


def draw_ONLINE_MENU():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "ONLINE MULTIPLAYER",
        40,
        35
    )

    options = (
        "Create Room",
        "Join Room"
    )

    for index, option in enumerate(
        options
    ):

        y = (
            75
            + index * 22
        )

        if (
            index
            == app.ONLINE_MENU_index
        ):

            app.screen.blit(
                cursor,
                (
                    30,
                    y
                )
            )

        app.font0.draw_text(
            app.screen,
            option,
            45,
            y
        )


def draw_ONLINE_HOST():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "CREATE ONLINE ROOM",
        38,
        25
    )

    status = (
        app.ONLINE_status
        or
        "CONNECTING"
    )

    app.font0.draw_text(
        app.screen,
        status,
        55,
        55
    )

    if (
        app.ONLINE_room_code
    ):

        app.font0.draw_text(
            app.screen,
            "ROOM CODE",
            75,
            82
        )

        app.font0.draw_text(
            app.screen,
            app.ONLINE_room_code,
            94,
            101
        )

        app.font0.draw_text(
            app.screen,
            "SEND THIS CODE",
            63,
            122
        )

    if (
        app.ONLINE_error
        is not None
    ):

        app.font0.draw_text(
            app.screen,
            app.ONLINE_error,
            35,
            142
        )


def draw_ONLINE_JOIN():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "JOIN ONLINE ROOM",
        45,
        25
    )

    status = (
        app.ONLINE_status
        or
        "ENTER ROOM CODE"
    )

    app.font0.draw_text(
        app.screen,
        status,
        55,
        55
    )

    if (
        app.ONLINE_join_code
    ):

        app.font0.draw_text(
            app.screen,
            app.ONLINE_join_code,
            94,
            82
        )

    if not app.ONLINE_connected:

        confirm_hint = (
            get_input_hint(
                INPUT_CONFIRM,
                "ENTER CODE"
            )
        )

        app.font0.draw_text(
            app.screen,
            confirm_hint,
            63,
            108
        )

    if (
        app.ONLINE_error
        is not None
    ):

        app.font0.draw_text(
            app.screen,
            app.ONLINE_error,
            35,
            142
        )

def draw_SPECIES_EDIT_controls():

    sort_hint = (
        get_input_hint(
            INPUT_BUTTON_X,
            "SORT"
        )
    )

    dex_hint = (
        get_input_hint(
            INPUT_BUTTON_Y,
            "DEX"
        )
    )

    previous_type_label = (
        get_input_label(
            INPUT_LEFT_SHOULDER_BACK
        )
    )

    next_type_label = (
        get_input_label(
            INPUT_RIGHT_SHOULDER_BACK
        )
    )

    type_hint = (
        f"{previous_type_label}/"
        f"{next_type_label}:TYPE"
    )

    app.font0.draw_text(
        app.screen,
        sort_hint,
        57,
        147
    )

    app.font0.draw_text(
        app.screen,
        dex_hint,
        106,
        147
    )

    app.font0.draw_text(
        app.screen,
        type_hint,
        151,
        147
    )


def draw_SPECIES_EDIT():

    app.screen.fill(
        COLOR_WHITE
    )

    if (
        app.SPECIES_EDIT_type_filter
        is None
    ):

        filter_text = "ALL"

    else:

        filter_text = (
            app.SPECIES_EDIT_type_filter
        )

    if (
        app.SPECIES_EDIT_stat_sort
        is None
    ):

        ordering_text = (
            app.SPECIES_EDIT_sort_mode
        )

    else:

        ordering_text = (
            app.SPECIES_EDIT_stat_sort
        )

    minus_label = (
        get_input_label(
            INPUT_MINUS
        )
    )

    plus_label = (
        get_input_label(
            INPUT_PLUS
        )
    )

    stat_hint = (
        f"{minus_label}/"
        f"{plus_label}:STAT"
    )

    app.font0.draw_text(
        app.screen,
        stat_hint,
        5,
        2
    )

    app.font0.draw_text(
        app.screen,
        (
            f"{ordering_text} "
            f"{filter_text}"
        ),
        145,
        2
    )

    species_list = (
        app.SPECIES_EDIT_species_list
    )

    preview_pokemon = (
        app.SPECIES_EDIT_preview_pokemon
    )

    if len(
        species_list
    ) == 0:

        app.font0.draw_text(
            app.screen,
            "NO SPECIES",
            10,
            40
        )

        previous_type_label = (
            get_input_label(
                INPUT_LEFT_SHOULDER_BACK
            )
        )

        next_type_label = (
            get_input_label(
                INPUT_RIGHT_SHOULDER_BACK
            )
        )

        type_hint = (
            f"{previous_type_label}/"
            f"{next_type_label}:TYPE"
        )

        app.font0.draw_text(
            app.screen,
            type_hint,
            145,
            147
        )

        return

    columns = (
        app.SPECIES_EDIT_columns
    )

    start_index = (
        app.SPECIES_EDIT_scroll_row
        * columns
    )

    for visible_index, pokemon in enumerate(
        preview_pokemon
    ):

        species_index = (
            start_index
            + visible_index
        )

        if (
            species_index
            >= len(
                species_list
            )
        ):

            break

        column = (
            visible_index
            % columns
        )

        row = (
            visible_index
            // columns
        )

        x = (
            5
            + column * 79
        )

        y = (
            14
            + row * 66
        )

        species = (
            species_list[
                species_index
            ]
        )

        if (
            species_index
            == app.SPECIES_EDIT_index
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    x,
                    y,
                    75,
                    62
                ),
                1
            )

        app.screen.blit(
            get_display_sprite(
                pokemon
            ),
            (
                x + 6,
                y
            )
        )

        app.font0.draw_text(
            app.screen,
            species.name,
            x + 3,
            y + 48
        )

    selected_species = (
        species_list[
            app.SPECIES_EDIT_index
        ]
    )

    app.font0.draw_text(
        app.screen,
        (
            f"NO.{selected_species.no:03d}"
        ),
        5,
        147
    )

    draw_SPECIES_EDIT_controls()

    if (
        app.SPECIES_EDIT_error
        is not None
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (
                55,
                142,
                181,
                18
            )
        )

        app.font0.draw_text(
            app.screen,
            app.SPECIES_EDIT_error,
            58,
            147
        )

    if not app.SPECIES_EDIT_dex_mode:
        return

    pygame.draw.rect(
        app.screen,
        COLOR_WHITE,
        (
            51,
            43,
            138,
            76
        )
    )

    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (
            51,
            43,
            138,
            76
        ),
        1
    )

    app.font0.draw_text(
        app.screen,
        "GO TO DEX NO.",
        67,
        51
    )

    digit_x_positions = [
        91,
        111,
        131
    ]

    for digit_index, digit in enumerate(
        app.SPECIES_EDIT_dex_digits
    ):

        x = (
            digit_x_positions[
                digit_index
            ]
        )

        if (
            digit_index
            == app.SPECIES_EDIT_dex_digit_index
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    x - 4,
                    68,
                    17,
                    19
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            str(
                digit
            ),
            x,
            72
        )

    confirm_hint = (
        get_input_hint(
            INPUT_CONFIRM,
            "GO"
        )
    )

    cancel_hint = (
        get_input_hint(
            INPUT_CANCEL,
            "BACK"
        )
    )

    app.font0.draw_text(
        app.screen,
        confirm_hint,
        68,
        92
    )

    app.font0.draw_text(
        app.screen,
        cancel_hint,
        68,
        105
    )

def draw_PKMN_INFO_species(
    pokemon
):

    if (
        app.PKMN_INFO_mode
        == "MOVES"
    ):

        learnset_size = len(
            pokemon.learnset
        )

        app.font0.draw_text(
            app.screen,
            "LEARNSET",
            10,
            7
        )

        app.font0.draw_text(
            app.screen,
            pokemon.species_name,
            145,
            7
        )

        cancel_hint = (
            get_input_hint(
                INPUT_CANCEL,
                "BACK"
            )
        )

        if learnset_size == 0:

            app.font0.draw_text(
                app.screen,
                "NO LEARNSET",
                10,
                40
            )

            app.font0.draw_text(
                app.screen,
                cancel_hint,
                145,
                146
            )

            return

        app.PKMN_INFO_learnset_index = max(
            0,
            min(
                app.PKMN_INFO_learnset_index,
                learnset_size - 1
            )
        )

        visible_count = 8

        visible_start = max(
            0,
            min(
                app.PKMN_INFO_learnset_index - 3,
                max(
                    0,
                    learnset_size - visible_count
                )
            )
        )

        visible_end = min(
            learnset_size,
            visible_start + visible_count
        )

        for row, learnset_index in enumerate(
            range(
                visible_start,
                visible_end
            )
        ):

            move = (
                pokemon.learnset[
                    learnset_index
                ]
            )

            y = (
                30 + row * 14
            )

            if (
                app.PKMN_INFO_learnset_index
                == learnset_index
            ):

                pygame.draw.rect(
                    app.screen,
                    COLOR_BLACK,
                    (
                        7,
                        y - 2,
                        132,
                        14
                    ),
                    1
                )

            app.font0.draw_text(
                app.screen,
                move.name,
                10,
                y
            )

        selected_move = (
            pokemon.learnset[
                app.PKMN_INFO_learnset_index
            ]
        )

        if (
            selected_move.type
            in TYPE_POSITIONS
        ):

            app.screen.blit(
                get_type_icon(
                    selected_move.type
                ),
                (
                    160,
                    30
                )
            )

        app.font0.draw_text(
            app.screen,
            selected_move.category,
            150,
            52
        )

        app.font0.draw_text(
            app.screen,
            f"PWR {selected_move.power}",
            150,
            70
        )

        app.font0.draw_text(
            app.screen,
            f"ACC {selected_move.accuracy}",
            150,
            88
        )

        app.font0.draw_text(
            app.screen,
            (
                f"{app.PKMN_INFO_learnset_index + 1}"
                f"/{learnset_size}"
            ),
            190,
            112
        )

        app.font0.draw_text(
            app.screen,
            cancel_hint,
            145,
            146
        )

        return

    stat_labels = [
        "HP",
        "ATK",
        "DEF",
        "SPA",
        "SPD",
        "SPE"
    ]

    stat_values = [
        pokemon.hp_base,
        pokemon.attack_base,
        pokemon.defense_base,
        pokemon.special_attack_base,
        pokemon.special_defense_base,
        pokemon.speed_base
    ]

    app.font0.draw_text(
        app.screen,
        pokemon.species_name,
        10,
        8
    )

    for type_index, pokemon_type in enumerate(
        pokemon.species.types
    ):

        app.screen.blit(
            get_type_icon(
                pokemon_type
            ),
            (
                10 + type_index * 32,
                26
            )
        )

    app.font0.draw_text(
        app.screen,
        "SPECIES INFO",
        10,
        48
    )

    app.screen.blit(
        get_display_sprite(
            pokemon
        ),
        (
            166,
            0
        )
    )

    moves_x = 7
    moves_y = 82
    moves_width = 98
    moves_height = 76

    stats_x = 109
    stats_y = 72
    stats_width = 128
    stats_height = 86

    if (
        app.PKMN_INFO_index
        == 3
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                moves_x,
                moves_y,
                moves_width,
                moves_height
            ),
            1
        )

    if (
        app.PKMN_INFO_index
        == 4
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                stats_x,
                stats_y,
                stats_width,
                stats_height
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        "MOVES",
        11,
        85
    )

    for move_index in range(
        4
    ):

        app.font0.draw_text(
            app.screen,
            "?",
            11,
            102 + move_index * 13
        )

    app.font0.draw_text(
        app.screen,
        "BASE",
        113,
        75
    )

    stat_y_positions = [
        88,
        99,
        110,
        121,
        132,
        143
    ]

    for stat_index, (
        label,
        value
    ) in enumerate(
        zip(
            stat_labels,
            stat_values
        )
    ):

        y = (
            stat_y_positions[
                stat_index
            ]
        )

        app.font0.draw_text(
            app.screen,
            f"{label} {value}",
            113,
            y
        )

        draw_small_bar(
            174,
            y + 3,
            value,
            255,
            55,
            6
        )

def draw_small_bar(
    x,
    y,
    value,
    max_value,
    width=36,
    height=6
):

    if max_value <= 0:

        fill_width = 0

    else:

        fill_width = int(
            value
            / max_value
            * width
        )

    fill_width = max(
        0,
        min(
            width,
            fill_width
        )
    )

    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (
            x,
            y,
            width,
            height
        ),
        1
    )

    if fill_width > 0:

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                x,
                y,
                fill_width,
                height
            )
        )

def draw_PKMN_INFO_moves(
    pokemon
):

    if app.PKMN_INFO_editable:

        title = "EDIT MOVES"

    elif app.PKMN_INFO_species:

        title = "LEARNSET"

    else:

        title = "MOVES"

    app.font0.draw_text(
        app.screen,
        title,
        10,
        7
    )

    app.font0.draw_text(
        app.screen,
        pokemon.species_name,
        145,
        7
    )

    if (
        app.PKMN_INFO_selecting_move
    ):

        learnset_size = len(
            pokemon.learnset
        )

        cancel_hint = (
            get_input_hint(
                INPUT_CANCEL,
                "BACK"
            )
        )

        if learnset_size == 0:

            app.font0.draw_text(
                app.screen,
                "NO LEARNSET",
                10,
                40
            )

            app.font0.draw_text(
                app.screen,
                cancel_hint,
                145,
                146
            )

            return

        app.PKMN_INFO_learnset_index = max(
            0,
            min(
                app.PKMN_INFO_learnset_index,
                learnset_size - 1
            )
        )

        app.font0.draw_text(
            app.screen,
            (
                "SLOT "
                f"{app.PKMN_INFO_move_index + 1}"
            ),
            10,
            24
        )

        visible_count = 8

        visible_start = max(
            0,
            min(
                app.PKMN_INFO_learnset_index - 3,
                max(
                    0,
                    learnset_size - visible_count
                )
            )
        )

        visible_end = min(
            learnset_size,
            visible_start + visible_count
        )

        for row, learnset_index in enumerate(
            range(
                visible_start,
                visible_end
            )
        ):

            move = (
                pokemon.learnset[
                    learnset_index
                ]
            )

            y = (
                40 + row * 14
            )

            if (
                app.PKMN_INFO_learnset_index
                == learnset_index
            ):

                pygame.draw.rect(
                    app.screen,
                    COLOR_BLACK,
                    (
                        7,
                        y - 2,
                        132,
                        14
                    ),
                    1
                )

            app.font0.draw_text(
                app.screen,
                move.name,
                10,
                y
            )

        selected_move = (
            pokemon.learnset[
                app.PKMN_INFO_learnset_index
            ]
        )

        if (
            selected_move.type
            in TYPE_POSITIONS
        ):

            app.screen.blit(
                get_type_icon(
                    selected_move.type
                ),
                (
                    160,
                    40
                )
            )

        app.font0.draw_text(
            app.screen,
            selected_move.category,
            150,
            62
        )

        app.font0.draw_text(
            app.screen,
            f"PWR {selected_move.power}",
            150,
            80
        )

        app.font0.draw_text(
            app.screen,
            f"ACC {selected_move.accuracy}",
            150,
            98
        )

        app.font0.draw_text(
            app.screen,
            (
                f"{app.PKMN_INFO_learnset_index + 1}"
                f"/{learnset_size}"
            ),
            190,
            115
        )

        if (
            app.PKMN_INFO_error
            is not None
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_WHITE,
                (
                    102,
                    112,
                    145,
                    17
                )
            )

            app.font0.draw_text(
                app.screen,
                app.PKMN_INFO_error,
                105,
                115
            )

        if app.PKMN_INFO_editable:

            confirm_hint = (
                get_input_hint(
                    INPUT_CONFIRM,
                    "SET"
                )
            )

            app.font0.draw_text(
                app.screen,
                confirm_hint,
                145,
                132
            )

        app.font0.draw_text(
            app.screen,
            cancel_hint,
            145,
            146
        )

        return

    move_slots = []

    for move_index in range(
        4
    ):

        if (
            move_index
            < len(
                pokemon.moves
            )
        ):

            move_slots.append(
                pokemon.moves[
                    move_index
                ]
            )

        else:

            move_slots.append(
                None
            )

    app.PKMN_INFO_move_index = max(
        0,
        min(
            app.PKMN_INFO_move_index,
            4
        )
    )

    for index, move in enumerate(
        move_slots
    ):

        y = (
            30 + index * 24
        )

        if (
            app.PKMN_INFO_move_index
            == index
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    7,
                    y - 3,
                    138,
                    18
                ),
                1
            )

        if move is None:

            move_name = "EMPTY"

        else:

            move_name = move.name

        app.font0.draw_text(
            app.screen,
            (
                f"{index + 1} "
                f"{move_name}"
            ),
            10,
            y
        )

    selected_move = None

    if (
        0
        <= app.PKMN_INFO_move_index
        < len(
            move_slots
        )
    ):

        selected_move = (
            move_slots[
                app.PKMN_INFO_move_index
            ]
        )

    if selected_move is not None:

        if (
            selected_move.type
            in TYPE_POSITIONS
        ):

            app.screen.blit(
                get_type_icon(
                    selected_move.type
                ),
                (
                    160,
                    30
                )
            )

        app.font0.draw_text(
            app.screen,
            selected_move.category,
            150,
            52
        )

        app.font0.draw_text(
            app.screen,
            f"PWR {selected_move.power}",
            150,
            70
        )

        app.font0.draw_text(
            app.screen,
            f"ACC {selected_move.accuracy}",
            150,
            88
        )

        if app.PKMN_INFO_editable:

            confirm_hint = (
                get_input_hint(
                    INPUT_CONFIRM,
                    "CHANGE"
                )
            )

            app.font0.draw_text(
                app.screen,
                confirm_hint,
                145,
                112
            )

        else:

            app.font0.draw_text(
                app.screen,
                "READ ONLY",
                175,
                112
            )

    elif (
        app.PKMN_INFO_move_index
        < 4
    ):

        app.font0.draw_text(
            app.screen,
            "EMPTY SLOT",
            150,
            52
        )

    if (
        app.PKMN_INFO_move_index
        == 4
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                7,
                137,
                62,
                18
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        "BACK",
        10,
        140
    )

def draw_PKMN_INFO():

    app.screen.fill(
        COLOR_WHITE
    )

    pokemon = (
        app.PKMN_INFO_pokemon
    )

    if pokemon is None:

        app.font0.draw_text(
            app.screen,
            "NO POKEMON",
            10,
            10
        )

        return

    if app.PKMN_INFO_species:

        draw_PKMN_INFO_species(
            pokemon
        )

        return

    if (
        app.PKMN_INFO_mode
        == "MOVES"
    ):

        draw_PKMN_INFO_moves(
            pokemon
        )

        return

    stat_labels = [
        "HP",
        "ATK",
        "DEF",
        "SPA",
        "SPD",
        "SPE"
    ]

    nature_stat_names = [
        None,
        "atk",
        "def",
        "spatk",
        "spdef",
        "spe"
    ]

    if (
        app.PKMN_INFO_info_mode
        == "ACTUAL"
    ):

        panel_title = "ACTUAL"

        stat_values = [
            pokemon.hp_max,
            pokemon.attack,
            pokemon.defense,
            pokemon.special_attack,
            pokemon.special_defense,
            pokemon.speed
        ]

        stat_bar_max = 714

    elif (
        app.PKMN_INFO_info_mode
        == "BASE"
    ):

        panel_title = "BASE"

        stat_values = [
            pokemon.hp_base,
            pokemon.attack_base,
            pokemon.defense_base,
            pokemon.special_attack_base,
            pokemon.special_defense_base,
            pokemon.speed_base
        ]

        stat_bar_max = 255

    else:

        panel_title = "EVS"

        stat_values = [
            pokemon.hp_ev,
            pokemon.attack_ev,
            pokemon.defense_ev,
            pokemon.special_attack_ev,
            pokemon.special_defense_ev,
            pokemon.speed_ev
        ]

        stat_bar_max = 252

    if (
        app.PKMN_INFO_mode
        == "STATS"
    ):

        if (
            app.PKMN_INFO_stats_index
            == 0
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    7,
                    5,
                    75,
                    17
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            panel_title,
            10,
            8
        )

        if (
            app.PKMN_INFO_stats_index
            == 1
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    7,
                    23,
                    140,
                    17
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            f"NATURE {pokemon.nature.name}",
            10,
            26
        )

        if (
            app.PKMN_INFO_stats_index
            == 2
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    7,
                    41,
                    85,
                    17
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            f"LEVEL {pokemon.level}",
            10,
            44
        )

        for index, (
            label,
            value
        ) in enumerate(
            zip(
                stat_labels,
                stat_values
            )
        ):

            y = (
                63 + index * 13
            )

            nature_stat_name = (
                nature_stat_names[
                    index
                ]
            )

            nature_symbol = ""

            if (
                nature_stat_name
                is not None
            ):

                nature_symbol = (
                    pokemon.nature_symbol(
                        nature_stat_name
                    )
                )

            if (
                app.PKMN_INFO_stats_index
                == index + 3
            ):

                pygame.draw.rect(
                    app.screen,
                    COLOR_BLACK,
                    (
                        7,
                        y - 2,
                        145,
                        14
                    ),
                    1
                )

            app.font0.draw_text(
                app.screen,
                (
                    f"{label} "
                    f"{value}"
                    f"{nature_symbol}"
                ),
                10,
                y
            )

            draw_small_bar(
                72,
                y + 4,
                value,
                stat_bar_max,
                70
            )

        ev_total = (
            pokemon.hp_ev
            + pokemon.attack_ev
            + pokemon.defense_ev
            + pokemon.special_attack_ev
            + pokemon.special_defense_ev
            + pokemon.speed_ev
        )

        app.font0.draw_text(
            app.screen,
            f"EV {ev_total}/508",
            166,
            112
        )

        if (
            app.PKMN_INFO_error
            is not None
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_WHITE,
                (
                    118,
                    139,
                    130,
                    18
                )
            )

            app.font0.draw_text(
                app.screen,
                app.PKMN_INFO_error,
                121,
                142
            )

        if (
            app.PKMN_INFO_stats_index
            == 9
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    7,
                    141,
                    62,
                    17
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            "BACK",
            10,
            144
        )

        app.screen.blit(
            get_display_sprite(
                pokemon
            ),
            (
                166,
                0
            )
        )

        return

    if (
        app.PKMN_INFO_index
        == 0
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                7,
                5,
                115,
                17
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        pokemon.species_name,
        10,
        8
    )

    for type_index, pokemon_type in enumerate(
        pokemon.species.types
    ):

        app.screen.blit(
            get_type_icon(
                pokemon_type
            ),
            (
                10 + type_index * 32,
                26
            )
        )

    if (
        app.PKMN_INFO_index
        == 1
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                7,
                45,
                145,
                17
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        f"NAME {pokemon.nickname}",
        10,
        48
    )

    if (
        app.PKMN_INFO_index
        == 2
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                7,
                63,
                90,
                17
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        (
            "SHINY? YES"
            if pokemon.is_shiny
            else "SHINY? NO"
        ),
        10,
        66
    )

    app.screen.blit(
        get_display_sprite(
            pokemon
        ),
        (
            166,
            0
        )
    )

    moves_x = 7
    moves_y = 82
    moves_width = 98
    moves_height = 76

    stats_x = 109
    stats_y = 72
    stats_width = 128
    stats_height = 86

    if (
        app.PKMN_INFO_index
        == 3
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                moves_x,
                moves_y,
                moves_width,
                moves_height
            ),
            1
        )

    if (
        app.PKMN_INFO_index
        == 4
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                stats_x,
                stats_y,
                stats_width,
                stats_height
            ),
            1
        )

    app.font0.draw_text(
        app.screen,
        "MOVES",
        11,
        85
    )

    for index, move in enumerate(
        pokemon.moves
    ):

        app.font0.draw_text(
            app.screen,
            move.name,
            11,
            102 + index * 13
        )

    app.font0.draw_text(
        app.screen,
        panel_title,
        113,
        75
    )

    main_stat_y_positions = [
        88,
        99,
        110,
        121,
        132,
        143
    ]

    for index, (
        label,
        value
    ) in enumerate(
        zip(
            stat_labels,
            stat_values
        )
    ):

        y = (
            main_stat_y_positions[
                index
            ]
        )

        nature_stat_name = (
            nature_stat_names[
                index
            ]
        )

        nature_symbol = ""

        if (
            nature_stat_name
            is not None
        ):

            nature_symbol = (
                pokemon.nature_symbol(
                    nature_stat_name
                )
            )

        app.font0.draw_text(
            app.screen,
            (
                f"{label} "
                f"{value}"
                f"{nature_symbol}"
            ),
            113,
            y
        )

        draw_small_bar(
            174,
            y + 3,
            value,
            stat_bar_max,
            55,
            6
        )

def draw_DAMAGE_CALCULATOR():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "DAMAGE CALCULATOR",
        10,
        5
    )

    attacker = (
        app.DAMAGE_CALCULATOR_attacker
    )

    defender = (
        app.DAMAGE_CALCULATOR_defender
    )

    if attacker is not None:

        app.font0.draw_text(
            app.screen,
            attacker.species_name,
            10,
            20
        )

        app.screen.blit(
            get_display_sprite(
                attacker
            ),
            (
                10,
                35
            )
        )

    if defender is not None:

        app.font0.draw_text(
            app.screen,
            defender.species_name,
            170,
            20
        )

        app.screen.blit(
            get_display_sprite(
                defender
            ),
            (
                170,
                35
            )
        )

    calculator_options = [
        "IMPORT",
        "EDIT",
        "SAVE"
    ]

    for index, text in enumerate(
        calculator_options
    ):

        y = (
            108 + index * 15
        )

        if (
            app.DAMAGE_CALCULATOR_column
            == 0
            and
            app.DAMAGE_CALCULATOR_index
            == index
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    5,
                    y - 1,
                    55,
                    15
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            text,
            10,
            y
        )

    if attacker is not None:

        for index, move in enumerate(
            attacker.moves
        ):

            y = (
                30 + index * 15
            )

            if (
                app.DAMAGE_CALCULATOR_column
                == 1
                and
                app.DAMAGE_CALCULATOR_index
                == index
            ):

                pygame.draw.rect(
                    app.screen,
                    COLOR_BLACK,
                    (
                        80,
                        y - 1,
                        80,
                        15
                    ),
                    1
                )

            app.font0.draw_text(
                app.screen,
                move.name,
                85,
                y
            )

    for index, text in enumerate(
        calculator_options
    ):

        y = (
            108 + index * 15
        )

        if (
            app.DAMAGE_CALCULATOR_column
            == 2
            and
            app.DAMAGE_CALCULATOR_index
            == index
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    175,
                    y - 1,
                    55,
                    15
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            text,
            180,
            y
        )

    selected_move = None

    if (
        attacker is not None
        and
        app.DAMAGE_CALCULATOR_column
        == 1
        and
        0
        <= app.DAMAGE_CALCULATOR_index
        < len(
            attacker.moves
        )
    ):

        selected_move = (
            attacker.moves[
                app.DAMAGE_CALCULATOR_index
            ]
        )

    if selected_move is not None:

        if (
            selected_move.type
            in TYPE_POSITIONS
        ):

            app.screen.blit(
                get_type_icon(
                    selected_move.type
                ),
                (
                    60,
                    110
                )
            )

        app.font0.draw_text(
            app.screen,
            selected_move.category,
            95,
            113
        )

        app.font0.draw_text(
            app.screen,
            f"PWR {selected_move.power}",
            60,
            130
        )

        app.font0.draw_text(
            app.screen,
            f"ACC {selected_move.accuracy}",
            120,
            130
        )

    if (
        selected_move is not None
        and
        defender is not None
    ):

        min_percent, max_percent = (
            calculate_damage_percent_range(
                attacker,
                defender,
                selected_move
            )
        )

        app.font0.draw_text(
            app.screen,
            f"MIN {min_percent:.1f}%",
            60,
            145
        )

        app.font0.draw_text(
            app.screen,
            f"MAX {max_percent:.1f}%",
            120,
            145
        )

def draw_SINGLE_DEFEND_GYM():

    app.screen.fill(
        COLOR_WHITE
    )

    start = (
        app.SINGLE_DEFEND_GYM_scroll
    )

    end = min(
        len(app.gyms_data),
        start + 2
    )

    for screen_row, SINGLE_DEFEND_GYM_index in enumerate(
        range(start, end)
    ):

        gym = (
            app.gyms_data[
                SINGLE_DEFEND_GYM_index
            ]
        )

        row_y = (
            10
            +
            screen_row * 72
        )

        #
        # Cursor
        #

        if SINGLE_DEFEND_GYM_index == app.SINGLE_DEFEND_GYM_index:

            app.screen.blit(
                cursor,
                (2, row_y + 8)
            )

        #
        # Type icon
        #

        app.screen.blit(
            get_type_icon(
                gym["type"]
            ),
            (18, row_y + 5)
        )

        #
        # Selected trainer for THIS gym
        #

        trainer_index = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        trainer_x = [
            60,
            105,
            150
        ]

        for i, trainer_name in enumerate(
            gym["challengers"]
        ):

            trainer = next(
                t
                for t
                in app.trainers_data
                if t["name"] == trainer_name
            )

            draw_trainer = True

            gym_progress = (
                ensure_gym_progress()
            )

            progress = (
                gym_progress[
                    gym["type"]
                ]
            )

            if (
                SINGLE_DEFEND_GYM_index
                == app.SINGLE_DEFEND_GYM_index
                and
                i
                == trainer_index
            ):

                draw_trainer = (
                    pygame.time.get_ticks()
                    // 250
                ) % 2 == 0

            if draw_trainer:

                app.screen.blit(
                    get_trainer_sprite(
                        trainer["sprite"]
                    ),
                    (
                        trainer_x[i],
                        row_y
                    )
                )
        selected_trainer = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        if (
            progress[
                selected_trainer
            ]
        ):

            app.font0.draw_text(
                app.screen,
                "DEFEATED",
                10,
                row_y + 32
            )

        #
        # Progress placeholder
        #

        gym_progress = (
            ensure_gym_progress()
        )

        progress = (
            gym_progress[
                gym["type"]
            ]
        )

        num_defeated = sum(
            progress
        )

        app.font0.draw_text(
            app.screen,
            f"{num_defeated}/3",
            220,
            row_y + 10
        )

def draw_SINGLE_BRACKET():

    app.screen.fill(
        COLOR_WHITE
    )

    app.screen.blit(
        bracket,
        (0, 0)
    )

    app.font0.draw_text(
        app.screen,
        "TOURNAMENT",
        180,
        5
    )

    quarterfinal_positions = [
        (10, 3),
        (10, 22),
        (10, 41),
        (10, 60),
        (10, 79),
        (10, 97),
        (10, 115),
        (10, 134)
    ]

    semifinal_positions = [
        (77, 14),
        (77, 49),
        (77, 85),
        (77, 121)
    ]

    final_positions = [
        (143, 41),
        (143, 91)
    ]

    #
    # Quarterfinals
    #

    for i, participant in enumerate(
        app.tournament_quarterfinals
    ):

        if participant == "PLAYER":
            text = app.player_name
        else:
            text = participant["name"]

        x, y = (
            quarterfinal_positions[i]
        )

        app.font0.draw_text(
            app.screen,
            text,
            x,
            y
        )

    #
    # Semifinals
    #

    for i, participant in enumerate(
        app.tournament_semifinals
    ):

        if participant == "PLAYER":
            text = app.player_name
        else:
            text = participant["name"]

        x, y = (
            semifinal_positions[i]
        )

        app.font0.draw_text(
            app.screen,
            text,
            x,
            y
        )

    #
    # Finals
    #

    for i, participant in enumerate(
        app.tournament_finals
    ):

        if participant == "PLAYER":
            text = app.player_name
        else:
            text = participant["name"]

        x, y = (
            final_positions[i]
        )

        app.font0.draw_text(
            app.screen,
            text,
            x,
            y
        )

def draw_BATTLE_END():
    app.screen.fill(COLOR_WHITE)

def draw_SINGLE_MENU_TRAINER():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "TRAINER BATTLE",
        10, 5
    )
    options = [
        "Random Team",
        "My Team",
        "Trainer"
    ]
    for i, text in enumerate(options):
        y = 25 + i * 16
        if i == app.SINGLE_MENU_TRAINER_index:
            app.screen.blit(cursor, (10, y))
        app.font0.draw_text(
            app.screen,
            text,
            20, y
        )
    app.screen.blit(
        get_trainer_sprite(app.player_sprite),
        (4,96)
    )
    trainer = (
        app.trainers_data[
            app.SINGLE_MENU_TRAINER_selected_trainer
        ]
    )
    trainer_name = trainer["name"]
    app.font0.draw_text(
        app.screen,
        trainer_name,
        68,
        57
    )
    if (
        trainer_name
        in
        get_trainer_defeats()
    ):
        app.font0.draw_text(
            app.screen,
            "DEFEATED",
            68,
            69
        )
    preview_team = []
    if (
        app.SINGLE_MENU_TRAINER_index
        == 0
    ):
        pass
    elif (
        app.SINGLE_MENU_TRAINER_index
        == 1
    ):
        app.screen.blit(
            get_trainer_sprite(
                app.player_sprite
            ),
            (68, 96)
        )
        if (
            len(app.teams_data) > 0
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is not None
        ):
            selected_team = (
                app.teams_data[
                    app.SINGLE_MENU_TRAINER_selected_team
                ]
            )
            app.font0.draw_text(
                app.screen,
                "-" + selected_team["name"],
                63,
                41
            )
            preview_team = (
                app.SINGLE_MENU_TRAINER_my_team_preview
            )
    else:
        app.screen.blit(
            get_trainer_sprite(
                trainer["sprite"]
            ),
            (68, 96)
        )
        preview_team = (
            app.SINGLE_MENU_TRAINER_preview_team
        )
    show_preview = (
        app.SINGLE_MENU_TRAINER_index == 1
        or
        app.option_omniscient
    )
    if show_preview:
        for i, pokemon in enumerate(
            preview_team
        ):
            column = i % 2
            row = i // 2
            x = 128 + column * 48
            y = row * 48
            app.screen.blit(
                get_display_sprite(
                    pokemon
                ),
                (x, y)
            )

def draw_SINGLE_MENU():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "SINGLE PLAYER",
        10, 10
    )
    options = [
       f"Trainer Battle        DEFEATED  {get_num_trainer_defeats()}",
       f"Endless Battle          RECORD  {get_endless_record()}",
       f"Defend Gym                GYMS  {get_num_completed_gyms()}",
       f"Tournament              TITLES  {get_num_titles()}"
    ]
    for i, text in enumerate(options):
        y = 40 + i * 20
        if i == app.SINGLE_MENU_index:
            app.screen.blit(cursor, (10, y))
        app.font0.draw_text(
            app.screen,
            text,
            20, y
        )

def draw_OPTIONS_MUSIC():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "MUSIC",
        10, 10
    )
    app.font0.draw_text(
        app.screen,
        "MENU",
        165, 10
    )
    app.font0.draw_text(
        app.screen,
        "BATTLE",
        205, 10
    )
    filenames = sorted(
        app.music_data.keys()
    )
    visible_files = filenames[
        app.OPTIONS_MUSIC_scroll:
        app.OPTIONS_MUSIC_scroll + 8
    ]
    for row, filename in enumerate(visible_files):
        actual_index = app.OPTIONS_MUSIC_scroll + row
        y = 35 + row * 15
        if (
            actual_index
            ==
            app.OPTIONS_MUSIC_index
        ):
            app.screen.blit(
                cursor,
                (
                    5, y
                )
            )
        app.font0.draw_text(
            app.screen,
            filename[:-4],
            20,
            y
        )
        menu_text = (
            "Y"
            if app.music_data[
                filename
            ]["menu"]
            else "N"
        )
        battle_text = (
            "Y"
            if app.music_data[
                filename
            ]["battle"]
            else "N"
        )
        app.font0.draw_text(
            app.screen,
            menu_text,
            175,
            y
        )
        app.font0.draw_text(
            app.screen,
            battle_text,
            215,
            y
        )
        if app.current_music == filename:
            app.font0.draw_text(
                app.screen,
                ">",
                230,
                y
            )

def draw_KEYBOARD():
    app.screen.fill(COLOR_WHITE)
    if (
        app.KEYBOARD_mode
        == "PLAYER_NAME"
    ):

        title = "PLAYER NAME"

    elif (
        app.KEYBOARD_mode
        == "CREATE_TEAM"
    ):

        title = "NEW TEAM"

    elif (
        app.KEYBOARD_mode
        == "RENAME_TEAM"
    ):

        title = "RENAME TEAM"

    elif (
        app.KEYBOARD_mode
        == "POKEMON_NICKNAME"
    ):

        title = "NICKNAME"

    else:

        title = "ENTER NAME"

    app.font0.draw_text(
        app.screen,
        title,
        40,
        10
    )
    app.font0.draw_text(
        app.screen,
        app.KEYBOARD_text,
        120,
        10
    )
    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (
            118,
            8,
            80,
            15
        ),
        1
    )
    for row_index, row in enumerate(
        KEYBOARD_GRID
    ):
        for column_index, text in enumerate(
            row
        ):
            if row_index == len(KEYBOARD_GRID) - 1:
                x_positions = [
                    40,   # SPACE
                    100,  # BACK
                    160   # DONE
                ]
                x = x_positions[column_index]
            else:
                x = 40 + column_index * 20
            y = 30 + row_index * 20
            if (
                row_index
                ==
                app.KEYBOARD_row
                and
                column_index
                ==
                app.KEYBOARD_column
            ):
                app.screen.blit(
                    cursor,
                    (
                        x - 10,
                        y
                    )
                )
            app.font0.draw_text(
                app.screen,
                text,
                x,
                y
            )

def draw_OPTIONS():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "OPTIONS",
        10,
        10
    )

    options = [
        (
            "Player Name",
            app.player_name
        ),
        (
            "Player Sprite",
            str(
                app.player_sprite
            )
        ),
        (
            "Music",
            ""
        ),
        (
            "Omniscient",
            (
                "ON"
                if app.option_omniscient
                else "OFF"
            )
        ),
        (
            "Pokemon Animation",
            (
                "ON"
                if app.option_pkmn_animation
                else "OFF"
            )
        ),
        (
            "Fanart",
            (
                "ON"
                if app.option_fanart
                else "OFF"
            )
        ),
        (
            "Music Shuffle",
            (
                "ON"
                if app.option_music_shuffle
                else "OFF"
            )
        ),
        (
            "Player Level Cap",
            app.option_level
        ),
        (
            "Opponent Level Cap",
            app.option_level_npc
        )
    ]

    visible_options = options[
        app.OPTIONS_scroll:
        app.OPTIONS_scroll + 6
    ]

    for row, (
        label,
        value
    ) in enumerate(
        visible_options
    ):

        actual_index = (
            app.OPTIONS_scroll
            + row
        )

        y = (
            40 + row * 20
        )

        if (
            actual_index
            == app.OPTIONS_index
        ):

            app.screen.blit(
                cursor,
                (
                    10,
                    y
                )
            )

        app.font0.draw_text(
            app.screen,
            f"{label}: {value}",
            20,
            y
        )

    app.screen.blit(
        get_trainer_sprite(
            app.player_sprite
        ),
        (
            170,
            30
        )
    )

    app.font0.draw_text(
        app.screen,
        app.player_name,
        170,
        100
    )

def draw_TEAM_SELECT():

    app.screen.fill(
        COLOR_WHITE
    )

    if (
        app.TEAM_SELECT_mode
        == "IMPORT"
    ):

        title = (
            "IMPORT POKEMON"
        )

    elif (
        app.TEAM_SELECT_mode
        == "SAVE"
    ):

        if (
            app.TEAM_SELECT_import_target
            == "ATTACKER"
        ):

            title = (
                "SAVE ATTACKER"
            )

        else:

            title = (
                "SAVE DEFENDER"
            )

    elif (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
    ):

        title = (
            "TEAM BUILDER"
        )

    else:

        title = (
            "SELECT TEAM"
        )

    app.font0.draw_text(
        app.screen,
        title,
        10,
        10
    )

    if (
        app.TEAM_SELECT_error
        is not None
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (
                2,
                141,
                252,
                18
            )
        )

        app.font0.draw_text(
            app.screen,
            app.TEAM_SELECT_error,
            5,
            145
        )

    visible_teams = (
        app.available_teams[
            app.TEAM_SELECT_scroll:
            app.TEAM_SELECT_scroll + 7
        ]
    )

    for row, team_name in enumerate(
        visible_teams
    ):

        actual_index = (
            app.TEAM_SELECT_scroll
            + row
        )

        y = (
            40 + row * 15
        )

        if (
            actual_index
            == app.TEAM_SELECT_index
        ):

            app.screen.blit(
                cursor,
                (
                    10,
                    y
                )
            )

        app.font0.draw_text(
            app.screen,
            team_name,
            20,
            y
        )

    for index, pokemon in enumerate(
        app.TEAM_SELECT_preview_team
    ):

        column = (
            index % 2
        )

        row = (
            index // 2
        )

        x = (
            105 + column * 64
        )

        y = (
            row * 48
        )

        draw_sprite = True

        if (
            app.TEAM_SELECT_selecting_pokemon
            and
            index
            == app.TEAM_SELECT_pokemon_index
        ):

            draw_sprite = (
                pygame.time.get_ticks()
                // 250
            ) % 2 == 0

        if draw_sprite:

            app.screen.blit(
                get_display_sprite(
                    pokemon
                ),
                (
                    x,
                    y
                )
            )

    if (
        app.TEAM_SELECT_mode
        == "IMPORT"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        app.font0.draw_text(
            app.screen,
            "SELECT TO IMPORT",
            5,
            145
        )

    elif (
        app.TEAM_SELECT_mode
        == "SAVE"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        app.font0.draw_text(
            app.screen,
            "SELECT TO OVERWRITE",
            5,
            145
        )

    elif (
        app.TEAM_SELECT_mode
        not in (
            "IMPORT",
            "SAVE"
        )
        and
        app.connection_socket
        is not None
        and
        app.player_team
        is not None
    ):

        app.font0.draw_text(
            app.screen,
            "WAITING FOR OPPONENT",
            10,
            145
        )

    if (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
        and
        app.TEAM_SELECT_submenu
    ):

        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (
                50,
                25,
                90,
                70
            )
        )

        pygame.draw.rect(
            app.screen,
            COLOR_BLACK,
            (
                50,
                25,
                90,
                70
            ),
            1
        )

        for index, text in enumerate(
            TEAM_BUILDER_ACTIONS
        ):

            y = (
                35 + index * 15
            )

            if (
                index
                == app.TEAM_SELECT_submenu_index
            ):

                app.screen.blit(
                    cursor,
                    (
                        52,
                        y
                    )
                )

            app.font0.draw_text(
                app.screen,
                text,
                65,
                y
            )

def draw_BATTLE_START():
    app.screen.fill(COLOR_WHITE)

def draw_bar(x,y,value,max_value):
    width = int(value / max_value * 80)
    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (x,y,80,6),
        1
    )
    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (x,y,width,6)
    )

def draw_TEAM_PREVIEW():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "YOUR TEAM",
        10,
        10
    )

    if app.option_omniscient:

        app.font0.draw_text(
            app.screen,
            "OPPONENT",
            170,
            10
        )

    for i, pokemon in enumerate(
        app.player_team
    ):

        y = 30 + i * 15

        if (
            app.TEAM_PREVIEW_column
            == 0
            and
            i
            == app.TEAM_PREVIEW_index
        ):

            app.screen.blit(
                cursor,
                (
                    5,
                    y
                )
            )

        if (
            app.player_lead
            == i
        ):

            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (
                    18,
                    y - 1,
                    70,
                    15
                ),
                1
            )

        app.font0.draw_text(
            app.screen,
            pokemon.species_name,
            20,
            y
        )

    if app.option_omniscient:

        for i in range(6):

            y = 30 + i * 15

            if (
                app.TEAM_PREVIEW_column
                == 1
                and
                i
                ==
                app.TEAM_PREVIEW_index
            ):

                app.screen.blit(
                    cursor,
                    (
                        160,
                        y
                    )
                )

            if i < len(
                app.opponent_team
            ):

                opponent = (
                    app.opponent_team[i]
                )

                app.font0.draw_text(
                    app.screen,
                    opponent.species_name,
                    175,
                    y
                )

            else:

                app.font0.draw_text(
                    app.screen,
                    "-----",
                    175,
                    y
                )

    pokemon = None

    if (
        app.TEAM_PREVIEW_column
        == 0
    ):

        pokemon = (
            app.player_team[
                app.TEAM_PREVIEW_index
            ]
        )

    elif (
        app.option_omniscient
        and
        app.TEAM_PREVIEW_index
        <
        len(
            app.opponent_team
        )
    ):

        pokemon = (
            app.opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )

    if pokemon is not None:

        app.screen.blit(
            get_display_sprite(
                pokemon
            ),
            (
                90,
                40
            )
        )

    if (
        app.TEAM_PREVIEW_opponent_ready
    ):

        app.font0.draw_text(
            app.screen,
            "OPPONENT READY",
            10,
            145
        )

def draw_LAN_JOIN():
    app.screen.fill(COLOR_WHITE)
    if app.LAN_JOIN_discovered_host_ip:
        app.font0.draw_text(
            app.screen,
            app.LAN_JOIN_discovered_host_ip,
            40, 80
        )
    status = ("CONNECTED" if app.LAN_JOIN_connected else "SEARCHING...")
    app.font0.draw_text(
        app.screen,
        status,
        40, 40
    )

def draw_LAN_HOST():
    app.screen.fill(COLOR_WHITE)
    status = ("CONNECTED" if app.LAN_HOST_connected else "HOSTING...")
    app.font0.draw_text(
        app.screen,
        status,
        60, 70
    )

def draw_LAN_HOST_JOIN():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "LAN MULTIPLAYER",
        45, 40
    )
    options =  ("Host Battle",
                "Join Battle"
    )
    for i, option in enumerate(options):
        y = 80 + (i * 20)
        if i == app.LAN_HOST_JOIN_index:
            app.screen.blit(
                cursor,
                (30, y + 3)
            )
        app.font0.draw_text(
            app.screen,
            option,
            45, y
        )

def draw_LAUNCHER_MENU():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "Pokemon Battle Simulator",
        30, 30
    )
    for i, option in enumerate(app.LAUNCHER_MENU_options):
        y = 50 + (i * 20)
        if i == app.LAUNCHER_MENU_index:
            app.screen.blit(
                cursor,
                (30, y)
            )
        app.font0.draw_text(
            app.screen,
            option,
            45, y
        )
    
    app.screen.blit(
        get_trainer_sprite(app.player_sprite),
        (170,50)
    )
    app.font0.draw_text(
        app.screen,
        app.player_name,
        170,
        120
    )
