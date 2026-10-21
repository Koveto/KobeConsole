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
    elif app.state == PKMN_VIEW:
        handle_event_PKMN_VIEW(event)
    elif app.state == SPECIES_VIEW:
        handle_event_SPECIES_VIEW(event)
    elif app.state == BATTLE_START:
        handle_event_BATTLE_START(event)
    elif app.state == TEAM_SELECT:
        handle_event_TEAM_SELECT(event)

def handle_event_TEAM_SELECT(event):
    if is_up(event):
        app.TEAM_SELECT_index = max(0, app.TEAM_SELECT_index - 1)
        app.TEAM_SELECT_preview_team = [
            Pokemon.from_species_number(random.choice(list(SPECIES.keys())))
            for _ in range(6)
        ]
    elif is_down(event):
        app.TEAM_SELECT_index = min(len(app.available_teams) - 1, app.TEAM_SELECT_index + 1)
        app.TEAM_SELECT_preview_team = [
            Pokemon.from_species_number(random.choice(list(SPECIES.keys())))
            for _ in range(6)
        ]
    elif is_confirm(event):
        load_species()
        selected_team_data = app.teams_data[app.TEAM_SELECT_index]
        if selected_team_data["name"] == "Random Team":
            app.selected_team = [Pokemon.from_species_number(random.choice(list(SPECIES.keys()))) for _ in range(6)]
        app.TEAM_SELECT_team_sent = False

def handle_event_BATTLE_START(event):
    pass

def handle_event_SPECIES_VIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(0, app.TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(5, app.TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        app.TEAM_PREVIEW_column = 1
    elif is_vy(event):
        if app.SPECIES_VIEW_mode == "STATS":
            app.SPECIES_VIEW_mode = "AFFINITIES"
        else:
            app.SPECIES_VIEW_mode = "STATS"
    elif is_cancel(event):
        change_state(app.previous_state)
    if app.TEAM_PREVIEW_column == 0:
        app.SPECIES_VIEW_species = app.TEAM_PREVIEW_team[app.TEAM_PREVIEW_index]
    elif app.TEAM_PREVIEW_index < len(app.TEAM_PREVIEW_opponent_team):
        app.SPECIES_VIEW_species = app.TEAM_PREVIEW_opponent_team[app.TEAM_PREVIEW_index]

def handle_event_PKMN_VIEW(event):
    if is_up(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_index = max(
                0,
                app.TEAM_PREVIEW_index - 1
            )
        else:
            app.PKMN_VIEW_move_index = max(
                0,
                app.PKMN_VIEW_move_index - 1
            )
    elif is_down(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_index = min(
                5,
                app.TEAM_PREVIEW_index + 1
            )
        else:
            app.PKMN_VIEW_move_index = min(
                len(
                    app.PKMN_VIEW_pokemon.moves
                ) - 1,
                app.PKMN_VIEW_move_index + 1
            )
    elif is_left(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        if app.PKMN_VIEW_move_index is None:
            app.TEAM_PREVIEW_column = 1
    elif is_cx(event):
        if app.PKMN_VIEW_mode == "STATS":
            app.PKMN_VIEW_mode = "EVS"
        else:
            app.PKMN_VIEW_mode = "STATS"
    elif is_vy(event):
        if app.PKMN_VIEW_mode == "AFFINITIES":
            app.PKMN_VIEW_mode = "STATS"
        else:
            app.PKMN_VIEW_mode = "AFFINITIES"
    elif is_confirm(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_move_index = 0
    elif is_cancel(event):
        if app.PKMN_VIEW_move_index is not None:
            app.PKMN_VIEW_move_index = None
        else:
            change_state(
                app.previous_state
            )
    if app.TEAM_PREVIEW_column == 0:
        app.PKMN_VIEW_pokemon = (
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
        app.PKMN_VIEW_pokemon = (
            app.TEAM_PREVIEW_opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )


def handle_event_TEAM_PREVIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(0, app.TEAM_PREVIEW_index - 1)
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(5, app.TEAM_PREVIEW_index + 1)
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        app.TEAM_PREVIEW_column = 1
    elif is_confirm(event):
        if app.TEAM_PREVIEW_column == 0:
            app.TEAM_PREVIEW_selected_lead = app.TEAM_PREVIEW_index
    elif is_cvxy(event):
        if app.option_info:
            if app.TEAM_PREVIEW_column == 0:
                app.PKMN_VIEW_pokemon = app.TEAM_PREVIEW_team[app.TEAM_PREVIEW_index]
            elif app.TEAM_PREVIEW_index < len(app.TEAM_PREVIEW_opponent_team):
                app.PKMN_VIEW_pokemon = app.TEAM_PREVIEW_opponent_team[app.TEAM_PREVIEW_index]
            change_state(PKMN_VIEW)
        else:
            if app.TEAM_PREVIEW_column == 0:
                app.SPECIES_VIEW_species = app.TEAM_PREVIEW_team[app.TEAM_PREVIEW_index]
            elif app.TEAM_PREVIEW_index < len(app.TEAM_PREVIEW_opponent_team):
                app.SPECIES_VIEW_species = app.TEAM_PREVIEW_opponent_team[app.TEAM_PREVIEW_index]
            change_state(SPECIES_VIEW)
    elif (
        is_cancel(event) and \
        app.TEAM_PREVIEW_selected_lead is None
    ):
        change_state(TEAM_SELECT)

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