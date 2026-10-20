from constants import *

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
    if app.state == STATE_LAUNCHER_MENU:
        draw_LAUNCHER_MENU()
    elif app.state == STATE_LAN_HOST_JOIN:
        draw_LAN_HOST_JOIN()
    elif app.state == STATE_LAN_HOST:
        draw_LAN_HOST()
    elif app.state == STATE_LAN_JOIN:
        draw_LAN_JOIN()
    elif app.state == STATE_LAN_TEAM_PREVIEW:
        draw_LAN_TEAM_PREVIEW()

def draw_LAN_TEAM_PREVIEW():

    app.screen.fill(COLOR_WHITE)

    app.font0.draw_text(
        app.screen,
        "YOUR TEAM",
        10, 10
    )

    app.font0.draw_text(
        app.screen,
        "OPPONENT",
        130, 10
    )

    #
    # Your Team
    #

    for i, pokemon in enumerate(
        app.STATE_LAN_TEAM_PREVIEW_team
    ):

        y = 30 + i * 15

        if (
            app.STATE_LAN_TEAM_PREVIEW_column == 0
            and
            i == app.STATE_LAN_TEAM_PREVIEW_index
        ):
            app.screen.blit(
                cursor,
                (15, y + 3)
            )

        app.font0.draw_text(
            app.screen,
            pokemon.species_name,
            30,
            y
        )

    #
    # Opponent Team
    #

    for i in range(6):

        y = 30 + i * 15

        if (
            app.STATE_LAN_TEAM_PREVIEW_column == 1
            and
            i == app.STATE_LAN_TEAM_PREVIEW_index
        ):
            app.screen.blit(
                cursor,
                (130, y + 3)
            )

        app.font0.draw_text(
            app.screen,
            "-----",
            145,
            y
        )

    #
    # Selected Pokemon
    #

    pokemon = None

    if app.STATE_LAN_TEAM_PREVIEW_column == 0:

        pokemon = (
            app.STATE_LAN_TEAM_PREVIEW_team[
                app.STATE_LAN_TEAM_PREVIEW_index
            ]
        )

    elif (
        app.STATE_LAN_TEAM_PREVIEW_index
        < len(
            app.STATE_LAN_TEAM_PREVIEW_opponent_team
        )
    ):

        pokemon = (
            app.STATE_LAN_TEAM_PREVIEW_opponent_team[
                app.STATE_LAN_TEAM_PREVIEW_index
            ]
        )

    #
    # Draw Selected Pokemon
    #

    if pokemon is not None:

        app.font0.draw_text(
            app.screen,
            pokemon.species_name,
            10,
            130
        )

        app.screen.blit(
            pokemon.front_sprite,
            (
                80,
                40
            )
        )

def draw_LAN_JOIN():
    app.screen.fill(COLOR_WHITE)
    if app.STATE_LAN_JOIN_discovered_host_ip:
        app.font0.draw_text(
            app.screen,
            app.STATE_LAN_JOIN_discovered_host_ip,
            40, 80
        )
    status = ("CONNECTED" if app.STATE_LAN_JOIN_connected else "SEARCHING...")
    app.font0.draw_text(
        app.screen,
        status,
        40, 40
    )

def draw_LAN_HOST():
    app.screen.fill(COLOR_WHITE)
    status = ("CONNECTED" if app.STATE_LAN_HOST_connected else "HOSTING...")
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
        if i == app.STATE_LAN_HOST_JOIN_index:
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
    for i, option in enumerate(app.STATE_LAUNCHER_MENU_options):
        y = 80 + (i * 20)
        if i == app.STATE_LAUNCHER_MENU_index:
            app.screen.blit(
                cursor,
                (30, y + 3)
            )
        app.font0.draw_text(
            app.screen,
            option,
            45, y
        )