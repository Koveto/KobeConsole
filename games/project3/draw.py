from constants import *
from app import app

def draw():
    if app.state == STATE_LAUNCHER_MENU:
        draw_state_LAUNCHER_MENU()

def draw_state_LAUNCHER_MENU():
    app.screen.fill(COLOR_WHITE)
    app.font0.draw_text(
        app.screen,
        "Pokemon Battle Simulator",
        70,
        40
    )
    for i, option in enumerate(["LAN Multiplayer"]):
        y = 80 + (i * 20)
        if i == app.STATE_LAUNCHER_MENU_index:
            pass