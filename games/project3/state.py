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
    if  (new_state == TEAM_PREVIEW):
        load_species()
        app.TEAM_PREVIEW_index = 0
        app.TEAM_PREVIEW_team = [Pokemon.from_species_number(random.randint(1, len(SPECIES))) for _ in range(6)]
        app.TEAM_PREVIEW_opponent_team = []
        app.TEAM_PREVIEW_selected_lead = None
        app.TEAM_PREVIEW_opponent_lead = None
        app.TEAM_PREVIEW_ready_sent = False
        app.TEAM_PREVIEW_opponent_ready = False
        app.TEAM_PREVIEW_column = 0
        app.TEAM_PREVIEW_team_sent = False
    if  (new_state == PKMN_VIEW):
        pass
    app.state = new_state