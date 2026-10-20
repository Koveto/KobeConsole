from constants import *
from state import *

def handle_event(event):
    if app.state == STATE_LAUNCHER_MENU:
        handle_event_LAUNCHER_MENU(event)
    elif app.state == STATE_LAN_HOST_JOIN:
        handle_event_LAN_HOST_JOIN(event)
    elif app.state == STATE_LAN_HOST:
        handle_event_LAN_HOST(event)
    elif app.state == STATE_LAN_JOIN:
        handle_event_LAN_JOIN(event)
    elif app.state == STATE_LAN_TEAM_PREVIEW:
        handle_event_LAN_TEAM_PREVIEW(event)

def handle_event_LAN_TEAM_PREVIEW(event):
    if is_up(event):
        app.STATE_LAN_TEAM_PREVIEW_index = max(0, app.STATE_LAN_TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.STATE_LAN_TEAM_PREVIEW_index = min(5, app.STATE_LAN_TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.STATE_LAN_TEAM_PREVIEW_column = 0
    elif is_right(event):
        app.STATE_LAN_TEAM_PREVIEW_column = 1

def handle_event_LAN_JOIN(event):
    if is_cancel(event):
        change_state(STATE_LAN_HOST_JOIN)

def handle_event_LAN_HOST(event):
    if is_cancel(event):
        change_state(STATE_LAN_HOST_JOIN)

def handle_event_LAN_HOST_JOIN(event):
    if is_up(event):
        app.STATE_LAN_HOST_JOIN_index = max(0, app.STATE_LAN_HOST_JOIN_index - 1)
    elif is_down(event):
        app.STATE_LAN_HOST_JOIN_index = min(1, app.STATE_LAN_HOST_JOIN_index + 1)
    elif is_confirm(event):
        if app.STATE_LAN_HOST_JOIN_index == 0:
            change_state(STATE_LAN_HOST)
        elif app.STATE_LAN_HOST_JOIN_index == 1:
            change_state(STATE_LAN_JOIN)
    elif is_cancel(event):
        change_state(STATE_LAUNCHER_MENU)

def handle_event_LAUNCHER_MENU(event):
    if is_up(event):
        app.STATE_LAUNCHER_MENU_index = max(0, app.STATE_LAUNCHER_MENU_index - 1)
    elif is_down(event):
        app.STATE_LAUNCHER_MENU_index = min(len(app.STATE_LAUNCHER_MENU_options) - 1, app.STATE_LAUNCHER_MENU_index + 1)
    elif is_confirm(event):
        if app.STATE_LAUNCHER_MENU_index == 0:
            pass
        elif app.STATE_LAUNCHER_MENU_index == 1:
            change_state(STATE_LAN_HOST_JOIN)