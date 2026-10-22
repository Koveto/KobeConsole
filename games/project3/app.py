class App:
    def __init__(self):
        self.state = None
        self.previous_state = None
        self.screen = None
        self.font0 = None
        self.connection_socket = None
        self.connection_is_host = None
        self.connection_buffer = ""
        self.option_omniscient = False
        self.selected_team = None
        self.available_teams = []
        self.teams_data = []

        self.LAUNCHER_MENU_index = 0
        self.LAUNCHER_MENU_options = ("Single Player",
                                      "LAN Multiplayer",
                                      "Options")
        
        self.LAN_HOST_JOIN_index = None

        self.LAN_HOST_last_broadcast_time = None
        self.LAN_HOST_ip_address = None
        self.LAN_HOST_server_socket = None
        self.LAN_HOST_client_socket = None
        self.LAN_HOST_connected = None
        self.LAN_HOST_is_host = None

        self.LAN_JOIN_discovery_socket = None
        self.LAN_JOIN_discovered_host_ip = None
        self.LAN_JOIN_connected = None
        self.LAN_JOIN_client_socket = None
        self.LAN_JOIN_is_host = None

        self.TEAM_PREVIEW_index = None
        self.TEAM_PREVIEW_team = None
        self.TEAM_PREVIEW_opponent_team = None
        self.TEAM_PREVIEW_selected_lead = None
        self.TEAM_PREVIEW_opponent_lead = None
        self.TEAM_PREVIEW_ready_sent = None
        self.TEAM_PREVIEW_opponent_ready = None
        self.TEAM_PREVIEW_column = None

        self.PKMN_VIEW_pokemon = None
        self.PKMN_VIEW_move_index = None
        self.PKMN_VIEW_mode = None

        self.SPECIES_VIEW_pokemon = None
        self.SPECIES_VIEW_mode = None

        self.TEAM_SELECT_index = 0
        self.TEAM_SELECT_preview_team = []
        self.TEAM_SELECT_team_sent = False
        self.TEAM_SELECT_opponent_team = None
        self.TEAM_SELECT_selected_team_data = None

        self.OPTIONS_index = 0

app = App()