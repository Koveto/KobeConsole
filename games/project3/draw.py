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

    if (
        app.option_fanart
        and
        pokemon.fanart_front
        is not None
    ):
        return (
            pokemon.fanart_front
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
    elif app.state == TEAM_PREVIEW:
        draw_TEAM_PREVIEW()
    elif app.state == PKMN_VIEW:
        draw_PKMN_VIEW()
    elif app.state == SPECIES_VIEW:
        draw_SPECIES_VIEW()
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
    elif app.state == POKEMON_IMPORT:
        draw_POKEMON_IMPORT()

def draw_POKEMON_IMPORT():

    app.screen.fill(
        COLOR_WHITE
    )

    app.font0.draw_text(
        app.screen,
        "IMPORT POKEMON",
        10,
        10
    )

    visible_teams = app.teams_data[
        app.POKEMON_IMPORT_scroll:
        app.POKEMON_IMPORT_scroll + 8
    ]

    if len(app.teams_data) == 0:

        app.font0.draw_text(
            app.screen,
            "NO SAVED TEAMS",
            10,
            40
        )

        app.font0.draw_text(
            app.screen,
            "CREATE ONE FIRST",
            10,
            55
        )

        return

    for row, team in enumerate(
        visible_teams
    ):

        actual_index = (
            app.POKEMON_IMPORT_scroll
            + row
        )

        y = 35 + row * 15

        if (
            actual_index
            ==
            app.POKEMON_IMPORT_index
        ):

            app.screen.blit(
                cursor,
                (
                    5,
                    y
                )
            )

        app.font0.draw_text(
            app.screen,
            team["name"],
            20,
            y
        )

    if len(app.teams_data) > 0:

        for i, pokemon in enumerate(
            app.POKEMON_IMPORT_preview_team
        ):

            column = i % 2
            row = i // 2

            x = 105 + column * 64
            y = row * 48

            draw_sprite = True

            if (
                app.POKEMON_IMPORT_selecting_pokemon
                and
                i
                ==
                app.POKEMON_IMPORT_pokemon_index
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

    #
    # Attacker
    #

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

    #
    # Defender
    #

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

    #
    # Attacker options
    #

    attacker_options = [
        "IMPORT",
        "EDIT"
    ]

    for i, text in enumerate(
        attacker_options
    ):

        y = 115 + i * 15

        if (
            app.DAMAGE_CALCULATOR_column
            == 0
            and
            app.DAMAGE_CALCULATOR_index
            == i
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

    #
    # Moves
    #

    if attacker is not None:

        for i, move in enumerate(
            attacker.moves
        ):

            y = 30 + i * 15

            if (
                app.DAMAGE_CALCULATOR_column
                == 1
                and
                app.DAMAGE_CALCULATOR_index
                == i
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

    #
    # Defender options
    #

    defender_options = [
        "IMPORT",
        "EDIT"
    ]

    for i, text in enumerate(
        defender_options
    ):

        y = 115 + i * 15

        if (
            app.DAMAGE_CALCULATOR_column
            == 2
            and
            app.DAMAGE_CALCULATOR_index
            == i
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

    #
    # Move information
    #

    if (
        attacker is not None
        and
        app.DAMAGE_CALCULATOR_column
        == 1
    ):

        selected_move = (
            attacker.moves[
                app.DAMAGE_CALCULATOR_index
            ]
        )

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
            (
                "PWR "
                +
                str(
                    selected_move.power
                )
            ),
            60,
            130
        )

        app.font0.draw_text(
            app.screen,
            (
                "ACC "
                +
                str(
                    selected_move.accuracy
                )
            ),
            120,
            130
        )

    if (
        attacker is not None
        and
        defender is not None
        and
        app.DAMAGE_CALCULATOR_column
        == 1
    ):

        selected_move = (
            attacker.moves[
                app.DAMAGE_CALCULATOR_index
            ]
        )

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
    app.font0.draw_text(
        app.screen,
        "ENTER NAME",
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
            "ON"
            if app.option_omniscient
            else "OFF"
        ),
        (
            "Pokemon Animation",
            "ON"
            if app.option_pkmn_animation
            else "OFF"
        ),
        (
            "Fanart",
            "ON"
            if app.option_fanart
            else "OFF"
        ),
        (
            "Music Shuffle",
            "ON"
            if app.option_music_shuffle
            else "OFF"
        ),
        (
            "Player Level",
            app.option_level
        ),
        (
            "Opponent Level",
            app.option_level_npc
        )
    ]
    visible_options = options[
        app.OPTIONS_scroll:
        app.OPTIONS_scroll + 6
    ]
    for row, (label, value) in enumerate(visible_options):
        actual_index = app.OPTIONS_scroll + row
        y = 40 + row * 20
        if actual_index == app.OPTIONS_index:
            app.screen.blit(
                cursor,
                (10, y)
            )
        app.font0.draw_text(
            app.screen,
            f"{label}: {value}",
            20,
            y
        )
    app.screen.blit(
        get_trainer_sprite(app.player_sprite),
        (170,30)
    )
    app.font0.draw_text(
        app.screen,
        app.player_name,
        170,
        100
    )

def draw_TEAM_SELECT():

    waiting_text = None

    if (
        app.connection_socket
        is not None
        and
        app.player_team is not None
    ):

        waiting_text = (
            "WAITING FOR OPPONENT"
        )

    draw_generic_team_select(
        "SELECT TEAM",
        waiting_text
    )


def draw_BATTLE_START():
    app.screen.fill(COLOR_WHITE)

def draw_SPECIES_VIEW():
    pokemon = app.SPECIES_VIEW_pokemon
    app.screen.fill(COLOR_WHITE)
    for i, pokemon_type in enumerate(
        pokemon.species.types
    ):
        app.screen.blit(
            get_type_icon(
                pokemon_type
            ),
            (10 + i * 32, 25)
        )
    app.font0.draw_text(
        app.screen,
        pokemon.species_name + pokemon.gender + " LV" + str(pokemon.level),
        10, 10
    )
    if app.SPECIES_VIEW_mode == "STATS":
        app.font0.draw_text(
            app.screen,
            f"HP  {pokemon.hp_base}",
            10, 60
        )
        app.font0.draw_text(
            app.screen,
            f"ATK {pokemon.attack_base}",
            10, 75
        )
        app.font0.draw_text(
            app.screen,
            f"DEF {pokemon.defense_base}",
            10, 90
        )
        app.font0.draw_text(
            app.screen,
            f"SPA {pokemon.special_attack_base}",
            10, 105
        )
        app.font0.draw_text(
            app.screen,
            f"SPD {pokemon.special_defense_base}",
            10, 120
        )
        app.font0.draw_text(
            app.screen,
            f"SPE {pokemon.speed_base}",
            10, 135
        )
        draw_bar(60,63,pokemon.hp_base,255)
        draw_bar(60,78,pokemon.attack_base,190)
        draw_bar(60,93,pokemon.defense_base,230)
        draw_bar(60,108,pokemon.special_attack_base,194)
        draw_bar(60,123,pokemon.special_defense_base,230)
        draw_bar(60,138,pokemon.speed_base,200)
    elif app.SPECIES_VIEW_mode == "AFFINITIES":
        affinities = get_affinities(pokemon)
        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (
                0,
                50,
                256,
                110
            )
        )
        for index, type_name in enumerate(TYPE_ORDER):
            column = index % 6
            row = index // 6
            x = 0 + column * 32
            y = 63 + row * 32
            app.screen.blit(
                get_type_icon(type_name),
                (x,y)
            )
            multiplier = affinities[
                type_name
            ]
            text = None
            if multiplier == 4:
                text = "4x"
            elif multiplier == 2:
                text = "2x"
            elif multiplier == 0.5:
                text = "1/2x"
            elif multiplier == 0.25:
                text = "1/4x"
            elif multiplier == 0:
                text = "0x"
            if text is not None:
                app.font0.draw_text(
                    app.screen,
                    text,
                    x + 3,
                    y + 16
                )
    app.screen.blit(
        get_display_sprite(pokemon),
        (166, 0)
    )

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

def draw_PKMN_VIEW():
    pokemon = app.PKMN_VIEW_pokemon
    app.screen.fill(COLOR_WHITE)
    for i, pokemon_type in enumerate(
        pokemon.species.types
    ):
        app.screen.blit(
            get_type_icon(
                pokemon_type
            ),
            (10 + i * 32, 25)
        )
    app.font0.draw_text(
        app.screen,
        pokemon.species_name + pokemon.gender + " LV" + str(pokemon.level),
        10, 10
    )
    if app.PKMN_VIEW_mode == "STATS":
        app.font0.draw_text(
            app.screen,
            f"HP  {pokemon.hp_max}",
            10, 60
        )
        app.font0.draw_text(
            app.screen,
            f"ATK {pokemon.attack}",
            10, 75
        )
        app.font0.draw_text(
            app.screen,
            f"DEF {pokemon.defense}",
            10, 90
        )
        app.font0.draw_text(
            app.screen,
            f"SPA {pokemon.special_attack}",
            10, 105
        )
        app.font0.draw_text(
            app.screen,
            f"SPD {pokemon.special_defense}",
            10, 120
        )
        app.font0.draw_text(
            app.screen,
            f"SPE {pokemon.speed}",
            10, 135
        )
        STAT_BAR_MAX = 714
        draw_bar(60,63,pokemon.hp_max,STAT_BAR_MAX)
        draw_bar(60,78,pokemon.attack,STAT_BAR_MAX)
        draw_bar(60,93,pokemon.defense,STAT_BAR_MAX)
        draw_bar(60,108,pokemon.special_attack,STAT_BAR_MAX)
        draw_bar(60,123,pokemon.special_defense,STAT_BAR_MAX)
        draw_bar(60,138,pokemon.speed,STAT_BAR_MAX)
    elif app.PKMN_VIEW_mode == "EVS":
        app.font0.draw_text(
            app.screen,
            "HP  " + str(pokemon.hp_ev),
            10, 60
        )
        app.font0.draw_text(
            app.screen,
            "ATK " + str(pokemon.attack_ev) + pokemon.nature_symbol("atk"),
            10, 75
        )
        app.font0.draw_text(
            app.screen,
            "DEF " + str(pokemon.defense_ev) + pokemon.nature_symbol("def"),
            10, 90
        )
        app.font0.draw_text(
            app.screen,
            "SPA " + str(pokemon.special_attack_ev) + pokemon.nature_symbol("spatk"),
            10, 105
        )
        app.font0.draw_text(
            app.screen,
            "SPD " + str(pokemon.special_defense_ev) + pokemon.nature_symbol("spdef"),
            10, 120
        )
        app.font0.draw_text(
            app.screen,
            "SPE " + str(pokemon.speed_ev) + pokemon.nature_symbol("spe"),
            10, 135
        )
        draw_bar(60,63,pokemon.hp_ev,252)
        draw_bar(60,78,pokemon.attack_ev,252)
        draw_bar(60,93,pokemon.defense_ev,252)
        draw_bar(60,108,pokemon.special_attack_ev,252)
        draw_bar(60,123,pokemon.special_defense_ev,252)
        draw_bar(60,138,pokemon.speed_ev,252)
    elif (
        app.PKMN_VIEW_mode
        == "BASE"
    ):

        app.font0.draw_text(
            app.screen,
            f"HP  {pokemon.hp_base}",
            10,
            60
        )

        app.font0.draw_text(
            app.screen,
            f"ATK {pokemon.attack_base}",
            10,
            75
        )

        app.font0.draw_text(
            app.screen,
            f"DEF {pokemon.defense_base}",
            10,
            90
        )

        app.font0.draw_text(
            app.screen,
            f"SPA {pokemon.special_attack_base}",
            10,
            105
        )

        app.font0.draw_text(
            app.screen,
            f"SPD {pokemon.special_defense_base}",
            10,
            120
        )

        app.font0.draw_text(
            app.screen,
            f"SPE {pokemon.speed_base}",
            10,
            135
        )

        BASE_BAR_MAX = 255

        draw_bar(
            60,
            63,
            pokemon.hp_base,
            BASE_BAR_MAX
        )

        draw_bar(
            60,
            78,
            pokemon.attack_base,
            BASE_BAR_MAX
        )

        draw_bar(
            60,
            93,
            pokemon.defense_base,
            BASE_BAR_MAX
        )

        draw_bar(
            60,
            108,
            pokemon.special_attack_base,
            BASE_BAR_MAX
        )

        draw_bar(
            60,
            123,
            pokemon.special_defense_base,
            BASE_BAR_MAX
        )

        draw_bar(
            60,
            138,
            pokemon.speed_base,
            BASE_BAR_MAX
        )
    for i, move in enumerate(pokemon.moves):
        if (app.PKMN_VIEW_move_index == i):
            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (155,
                 89 + i * 15,
                 90,
                 15),
                 1
            )
        app.font0.draw_text(
            app.screen,
            move.name,
            160, 90 + i * 15
        )
    if app.PKMN_VIEW_move_index is not None:
        selected_move = pokemon.moves[app.PKMN_VIEW_move_index]
        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (102,
             81,
             50,
             75)
        )
        app.screen.blit(
            get_type_icon(selected_move.type),
            (110,90)
        )
        app.font0.draw_text(
            app.screen,
            selected_move.category,
            110,
            105
        )
        app.font0.draw_text(
            app.screen,
            "PWR " + str(selected_move.power),
            110, 110
        )
        app.font0.draw_text(
            app.screen,
            "ACC " + str(selected_move.accuracy),
            110, 125
        )
    if app.PKMN_VIEW_mode == "AFFINITIES":
        affinities = get_affinities(pokemon)
        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (
                0,
                50,
                256,
                110
            )
        )
        for index, type_name in enumerate(TYPE_ORDER):
            column = index % 6
            row = index // 6
            x = 0 + column * 32
            y = 63 + row * 32
            app.screen.blit(
                get_type_icon(type_name),
                (x,y)
            )
            multiplier = affinities[
                type_name
            ]
            text = None
            if multiplier == 4:
                text = "4x"
            elif multiplier == 2:
                text = "2x"
            elif multiplier == 0.5:
                text = "1/2x"
            elif multiplier == 0.25:
                text = "1/4x"
            elif multiplier == 0:
                text = "0x"
            if text is not None:
                app.font0.draw_text(
                    app.screen,
                    text,
                    x + 3,
                    y + 16
                )
    app.screen.blit(
        get_display_sprite(pokemon),
        (166, 0)
    )
    

def draw_TEAM_PREVIEW():
    ready_text = ""
    if (
        app.TEAM_PREVIEW_opponent_ready
    ):
        ready_text = (
            "OPPONENT READY"
        )
    draw_generic_team_preview(
        app.TEAM_PREVIEW_index,
        app.TEAM_PREVIEW_column,
        app.player_lead,
        ready_text
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
        40, 30
    )
    for i, option in enumerate(app.LAUNCHER_MENU_options):
        y = 80 + (i * 20)
        if i == app.LAUNCHER_MENU_index:
            app.screen.blit(
                cursor,
                (30, y + 3)
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

def draw_generic_team_preview(
    TEAM_PREVIEW_index,
    TEAM_PREVIEW_column,
    selected_lead,
    ready_text=""
):
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "YOUR TEAM",
        10, 10
    )
    if app.option_omniscient:
        app.font0.draw_text(
            app.screen,
            "OPPONENT",
            170, 10
        )
    for i, pokemon in enumerate(
        app.player_team
    ):
        y = 30 + i * 15
        if (
            TEAM_PREVIEW_column == 0
            and
            i == TEAM_PREVIEW_index
        ):
            app.screen.blit(
                cursor,
                (5, y)
            )
        if selected_lead == i:
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
                TEAM_PREVIEW_column == 1
                and
                i == TEAM_PREVIEW_index
            ):
                app.screen.blit(
                    cursor,
                    (160, y)
                )
            if i < len(app.opponent_team):
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
    if TEAM_PREVIEW_column == 0:
        pokemon = (
            app.player_team[
                TEAM_PREVIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        TEAM_PREVIEW_index
        < len(app.opponent_team)
    ):
        pokemon = (
            app.opponent_team[
                TEAM_PREVIEW_index
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
    app.font0.draw_text(
        app.screen,
        ready_text,
        10,
        145
    )

def draw_generic_team_select(
    title,
    waiting_text=None
):
    app.screen.fill(
        COLOR_WHITE
    )
    app.font0.draw_text(
        app.screen,
        title,
        10,
        10
    )
    visible_teams = app.available_teams[
        app.TEAM_SELECT_scroll:
        app.TEAM_SELECT_scroll + 7
    ]

    if (
        app.TEAM_SELECT_error
        is not None
    ):

        app.font0.draw_text(
            app.screen,
            app.TEAM_SELECT_error,
            5,
            145
        )

    for row, team_name in enumerate(
        visible_teams
    ):
        actual_index = (
            app.TEAM_SELECT_scroll
            + row
        )
        y = 40 + row * 15
        if (
            actual_index
            ==
            app.TEAM_SELECT_index
        ):
            app.screen.blit(
                cursor,
                (10, y)
            )
        app.font0.draw_text(
            app.screen,
            team_name,
            20,
            y
        )
    for i, pokemon in enumerate(
        app.TEAM_SELECT_preview_team
    ):
        column = i % 2
        row = i // 2
        x = 105 + column * 64
        y = row * 48
        app.screen.blit(
            get_display_sprite(
                pokemon
            ),
            (
                x,
                y
            )
        )
    if waiting_text is not None:
        app.font0.draw_text(
            app.screen,
            waiting_text,
            10,
            145
        )