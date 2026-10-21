from constants import *
from func import *

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

def draw_bar(x,y,value,max_value):
    width = int(value / max_value * 40)
    pygame.draw.rect(
        app.screen,
        COLOR_BLACK,
        (x,y,40,6),
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
        pokemon.species_name + pokemon.gender,
        10, 10
    )
    app.screen.blit(
        pokemon.front_sprite,
        (100, 10)
    )
    if app.PKMN_VIEW_mode == "STATS":
        app.font0.draw_text(
            app.screen,
            f"HP  {pokemon.hp_max}",
            10, 50
        )
        app.font0.draw_text(
            app.screen,
            f"ATK {pokemon.attack}",
            10, 65
        )
        app.font0.draw_text(
            app.screen,
            f"DEF {pokemon.defense}",
            10, 80
        )
        app.font0.draw_text(
            app.screen,
            f"SPA {pokemon.special_attack}",
            10, 95
        )
        app.font0.draw_text(
            app.screen,
            f"SPD {pokemon.special_defense}",
            10, 110
        )
        app.font0.draw_text(
            app.screen,
            f"SPE {pokemon.speed}",
            10, 125
        )
        draw_bar(55,55,pokemon.hp_max,400)
        draw_bar(55,70,pokemon.attack,400)
        draw_bar(55,85,pokemon.defense,400)
        draw_bar(55,100,pokemon.special_attack,400)
        draw_bar(55,115,pokemon.special_defense,400)
        draw_bar(55,130,pokemon.speed,400)
    elif app.PKMN_VIEW_mode == "EVS":
        app.font0.draw_text(
            app.screen,
            "HP  " + str(pokemon.hp_ev),
            10, 50
        )
        app.font0.draw_text(
            app.screen,
            "ATK " + str(pokemon.attack_ev) + pokemon.nature_symbol("atk"),
            10, 65
        )
        app.font0.draw_text(
            app.screen,
            "DEF " + str(pokemon.defense_ev) + pokemon.nature_symbol("def"),
            10, 80
        )
        app.font0.draw_text(
            app.screen,
            "SPA " + str(pokemon.special_attack_ev) + pokemon.nature_symbol("spa"),
            10, 95
        )
        app.font0.draw_text(
            app.screen,
            "SPD " + str(pokemon.special_defense_ev) + pokemon.nature_symbol("spd"),
            10, 110
        )
        app.font0.draw_text(
            app.screen,
            "SPE " + str(pokemon.speed_ev) + pokemon.nature_symbol("spe"),
            10, 125
        )
        draw_bar(55,55,pokemon.hp_ev,400)
        draw_bar(55,70,pokemon.attack_ev,400)
        draw_bar(55,85,pokemon.defense_ev,400)
        draw_bar(55,100,pokemon.special_attack_ev,400)
        draw_bar(55,115,pokemon.special_defense_ev,400)
        draw_bar(55,130,pokemon.speed_ev,400)
    for i, move in enumerate(pokemon.moves):
        if (app.PKMN_VIEW_move_index == i):
            pygame.draw.rect(
                app.screen,
                COLOR_BLACK,
                (115,
                 89 + i * 15,
                 90,
                 14),
                 1
            )
        app.font0.draw_text(
            app.screen,
            move.name,
            120, 90 + i * 15
        )
    if app.PKMN_VIEW_move_index is not None:
        selected_move = pokemon.moves[app.PKMN_VIEW_move_index]
        pygame.draw.rect(
            app.screen,
            COLOR_WHITE,
            (62,
             80,
             50,
             75)
        )
        app.screen.blit(
            get_type_icon(selected_move.type),
            (70,90)
        )
        app.font0.draw_text(
            app.screen,
            "PWR " + str(selected_move.power),
            70, 110
        )
        app.font0.draw_text(
            app.screen,
            "ACC " + str(selected_move.accuracy),
            70, 125
        )

def draw_TEAM_PREVIEW():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "YOUR TEAM",
        10, 10
    )
    app.font0.draw_text(
        app.screen,
        "OPPONENT",
        170, 10
    )
    for i, pokemon in enumerate(
        app.TEAM_PREVIEW_team
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
        if i < len(app.TEAM_PREVIEW_opponent_team):
            opponent = app.TEAM_PREVIEW_opponent_team[i]
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
            app.TEAM_PREVIEW_team[
                app.TEAM_PREVIEW_index
            ]
        )
    elif (
        app.TEAM_PREVIEW_index
        < len(
            app.TEAM_PREVIEW_opponent_team
        )
    ):
        pokemon = (
            app.TEAM_PREVIEW_opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )
    if pokemon is not None:
        app.screen.blit(
            pokemon.front_sprite,
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
        10,130
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
        70, 40
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