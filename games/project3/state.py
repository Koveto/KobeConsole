from constants import *
from func import *
from pkmn import *

def change_state(new_state):
    app.previous_state = app.state
    if  (new_state == LAUNCHER_MENU):
        app.LAUNCHER_MENU_index = 0
    if  (new_state == LAN_HOST_JOIN):
        app.LAN_HOST_JOIN_index = 0
    if  (app.state == LAN_HOST_JOIN) and \
        (new_state == LAN_HOST):
        app.LAN_HOST_last_broadcast_time = 0
        app.LAN_HOST_ip_address = get_local_ip()
        app.LAN_HOST_server_socket = create_server(app.LAN_HOST_ip_address)
        app.LAN_HOST_client_socket = None
        app.LAN_HOST_connected = False
    if  (app.state == LAN_HOST_JOIN) and \
        (new_state == LAN_JOIN):
        app.LAN_JOIN_discovery_socket = (listen_for_hosts())
        app.LAN_JOIN_connected = False
        app.LAN_JOIN_discovered_host_ip = None
        app.LAN_JOIN_client_socket = None
    if  ((app.state == TEAM_SELECT)) and \
        (new_state == TEAM_PREVIEW):
        load_species()
        app.TEAM_PREVIEW_index = 0
        app.opponent_team = app.TEAM_SELECT_opponent_team
        app.TEAM_PREVIEW_selected_lead = None
        app.TEAM_PREVIEW_opponent_lead = None
        app.TEAM_PREVIEW_ready_sent = False
        app.TEAM_PREVIEW_opponent_ready = False
        app.TEAM_PREVIEW_column = 0
    if  (new_state == PKMN_VIEW):
        app.PKMN_VIEW_move_index = None
        app.PKMN_VIEW_mode = "STATS"
    if  (new_state == SPECIES_VIEW):
        app.SPECIES_VIEW_mode = "STATS"
    if  (new_state == TEAM_SELECT):
        app.TEAM_SELECT_team_sent = False
        app.TEAM_SELECT_opponent_team = None
        load_species()
        app.TEAM_SELECT_index = 0
        teams_data = load_teams()
        app.teams_data = teams_data["teams"]
        app.available_teams = []
        for team in app.teams_data:
            app.available_teams.append(team["name"])
        app.TEAM_SELECT_selected_team_data = app.teams_data[0]
        app.TEAM_SELECT_preview_team = []
    if  (new_state == OPTIONS):
        app.OPTIONS_scroll = 0
        app.OPTIONS_index = 0
    if  (new_state == KEYBOARD):
        app.KEYBOARD_text = app.player_name
    if  (new_state == OPTIONS_MUSIC):
        if new_state == OPTIONS_MUSIC:
            app.OPTIONS_MUSIC_index = 0
            app.OPTIONS_MUSIC_scroll = 0
            app.music_data = load_music_data()
    if  (new_state == SINGLE_MENU):
        app.SINGLE_MENU_index = 0
    if  (new_state == SINGLE_MENU_TRAINER):
        app.SINGLE_MENU_TRAINER_index = 0
    app.state = new_state