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

def handle_event_TEAM_PREVIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(0, app.TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(5, app.TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        app.TEAM_PREVIEW_column = 1

def handle_event_LAN_JOIN(event):
    if is_cancel(event):
        change_state(LAN_HOST_JOIN)

def handle_event_LAN_HOST(event):
    if is_cancel(event):
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
            pass
        elif app.LAUNCHER_MENU_index == 1:
            change_state(LAN_HOST_JOIN)