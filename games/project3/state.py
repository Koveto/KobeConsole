from constants import *
from func import *
from pkmn import *

def change_state(new_state):
    if  (new_state == STATE_LAUNCHER_MENU):
        app.STATE_LAUNCHER_MENU_index = 0
    if  (new_state == STATE_LAN_HOST_JOIN):
        app.STATE_LAN_HOST_JOIN_index = 0
    if  (app.state == STATE_LAN_HOST_JOIN) and \
        (new_state == STATE_LAN_HOST):
        app.STATE_LAN_HOST_last_broadcast_time = 0
        app.STATE_LAN_HOST_ip_address = get_local_ip()
        app.STATE_LAN_HOST_server_socket = create_server(app.STATE_LAN_HOST_ip_address)
        app.STATE_LAN_HOST_client_socket = None
        app.STATE_LAN_HOST_connected = False
    if  (app.state == STATE_LAN_HOST_JOIN) and \
        (new_state == STATE_LAN_JOIN):
        app.STATE_LAN_JOIN_discovery_socket = (listen_for_hosts())
        app.STATE_LAN_JOIN_connected = False
        app.STATE_LAN_JOIN_discovered_host_ip = None
        app.STATE_LAN_JOIN_client_socket = None
    if  (new_state == STATE_LAN_TEAM_PREVIEW):
        load_species()
        app.STATE_LAN_TEAM_PREVIEW_index = 0
        app.STATE_LAN_TEAM_PREVIEW_team = [Pokemon.from_species_number(random.randint(1, len(SPECIES))) for _ in range(6)]
        app.STATE_LAN_TEAM_PREVIEW_opponent_team = []
        app.STATE_LAN_TEAM_PREVIEW_selected_lead = None
        app.STATE_LAN_TEAM_PREVIEW_opponent_lead = None
        app.STATE_LAN_TEAM_PREVIEW_ready_sent = False
        app.STATE_LAN_TEAM_PREVIEW_opponent_ready = False
        app.STATE_LAN_TEAM_PREVIEW_pending_messages = []
        app.STATE_LAN_TEAM_PREVIEW_last_message = ""
        app.STATE_LAN_TEAM_PREVIEW_column = 0
    app.state = new_state