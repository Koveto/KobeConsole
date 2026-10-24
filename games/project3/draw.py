from constants import *
from func import *
from pkmn import *

cursor = None

def init_draw():
    global cursor

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

def get_display_sprite(pokemon):
    if app.option_pkmn_animation:
        return pokemon.front_sprite_anim
    return pokemon.front_sprite

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
    elif app.state == SINGLE_TEAM_SELECT:
        draw_SINGLE_TEAM_SELECT()
    elif app.state == SINGLE_TEAM_PREVIEW:
        draw_SINGLE_TEAM_PREVIEW()

def draw_SINGLE_TEAM_PREVIEW():
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
            app.SINGLE_TEAM_PREVIEW_column == 0
            and
            i == app.SINGLE_TEAM_PREVIEW_index
        ):
            app.screen.blit(
                cursor,
                (5, y)
            )
        if app.player_lead == i:
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
                app.SINGLE_TEAM_PREVIEW_column == 1
                and
                i == app.SINGLE_TEAM_PREVIEW_index
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
    if (
        app.SINGLE_TEAM_PREVIEW_column
        == 0
    ):
        pokemon = (
            app.player_team[
                app.SINGLE_TEAM_PREVIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        (
            app.SINGLE_TEAM_PREVIEW_index
            <
            len(app.opponent_team)
        )
    ):
        pokemon = (
            app.opponent_team[
                app.SINGLE_TEAM_PREVIEW_index
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

def draw_SINGLE_TEAM_SELECT():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "TEAM SELECT",
        10, 10
    )
    visible_teams = app.available_teams[
        app.SINGLE_TEAM_SELECT_scroll:
        app.SINGLE_TEAM_SELECT_scroll + 7
    ]
    for row, team_name in enumerate(
        visible_teams
    ):
        actual_index = (
            app.SINGLE_TEAM_SELECT_scroll
            + row
        )
        y = 40 + row * 15
        if (
            actual_index
            ==
            app.SINGLE_TEAM_SELECT_index
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
        app.SINGLE_TEAM_SELECT_preview_team
    ):
        column = i % 2
        row = i // 2
        x = 105 + column * 64
        y = row * 48
        app.screen.blit(
            get_display_sprite(pokemon),
            (x, y)
        )

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
    trainer = app.trainers_data[app.SINGLE_MENU_TRAINER_selected_trainer]
    trainer_sprite = get_trainer_sprite(trainer["sprite"])
    app.screen.blit(
        trainer_sprite,
        (68, 96)
    )
    app.font0.draw_text(
        app.screen,
        trainer["name"],
        68,
        57
    )
    app.font0.draw_text(
        app.screen,
        "DEFEATED",
        68, 69
    )
    if len(app.teams_data) > 0:
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
        preview_team = [
            Pokemon.from_dict(pokemon_data)
            for pokemon_data in selected_team["pokemon"]
        ]
        for i, pokemon in enumerate(preview_team):
            column = i % 2
            row = i // 2
            x = 128 + column * 48
            y = row * 48
            app.screen.blit(
                get_display_sprite(pokemon),
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
        "Trainer Battle        DEFEATED  0",
        "Endless Battle          RECORD  0",
        "Defend Gym                GYMS  0",
        "Tournament              TITLES  0"
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
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "SELECT TEAM",
        10,10
    )
    visible_teams = app.available_teams[
        app.TEAM_SELECT_scroll:
        app.TEAM_SELECT_scroll + 7
    ]
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
    for i, pokemon in enumerate(app.TEAM_SELECT_preview_team):
        column = i % 2
        row = i // 2
        x = 105 + column * 64
        y = row * 48 #48
        app.screen.blit(
            get_display_sprite(pokemon),
            (x,y)
        )
    if app.player_team is not None:
        app.font0.draw_text(
            app.screen,
            "WAITING FOR OPPONENT",
            10,
            145
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
        draw_bar(60,63,pokemon.hp_max,714)
        draw_bar(60,78,pokemon.attack,526)
        draw_bar(60,93,pokemon.defense,526)
        draw_bar(60,108,pokemon.special_attack,526)
        draw_bar(60,123,pokemon.special_defense,526)
        draw_bar(60,138,pokemon.speed,526)
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
            app.TEAM_PREVIEW_column == 0
            and
            i == app.TEAM_PREVIEW_index
        ):
            app.screen.blit(
                cursor,
                (5, y)
            )
        if app.TEAM_PREVIEW_selected_lead == i:
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
                app.TEAM_PREVIEW_column == 1
                and
                i == app.TEAM_PREVIEW_index
            ):
                app.screen.blit(
                    cursor,
                    (160, y)
                )
            if i < len(app.opponent_team):
                opponent = app.opponent_team[i]
                app.font0.draw_text(
                    app.screen,
                    opponent.species_name,
                    175, y
                )
            else:
                app.font0.draw_text(
                    app.screen,
                    "-----",
                    175, y
                )
    pokemon = None
    if app.TEAM_PREVIEW_column == 0:
        pokemon = (
            app.player_team[
                app.TEAM_PREVIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        (app.TEAM_PREVIEW_index < len(app.opponent_team))
    ):
        pokemon = (
            app.opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )
    if pokemon is not None:
        app.screen.blit(
            get_display_sprite(pokemon),
            (
                90,40
            )
        )    
    ready_text = ""
    if (app.TEAM_PREVIEW_opponent_ready):
        ready_text = "OPPONENT READY"
    elif ((app.TEAM_PREVIEW_selected_lead is not None) and 
          (not app.TEAM_PREVIEW_opponent_ready)):
        ready_text = "WAITING FOR OPPONENT"
    app.font0.draw_text(
        app.screen,
        ready_text,
        10,145
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