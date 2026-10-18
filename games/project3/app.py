class App:
    def __init__(self):
        self.state = None
        self.screen = None
        self.font0 = None
        self.connection_socket = None
        self.connection_is_host = None

        self.STATE_LAUNCHER_MENU_index = 0
        self.STATE_LAUNCHER_MENU_options = ("Single Player",
                                            "LAN Multiplayer")
        
        self.STATE_LAN_HOST_JOIN_index = None

        self.STATE_LAN_HOST_last_broadcast_time = None
        self.STATE_LAN_HOST_ip_address = None
        self.STATE_LAN_HOST_server_socket = None
        self.STATE_LAN_HOST_client_socket = None
        self.STATE_LAN_HOST_connected = None
        self.STATE_LAN_HOST_is_host = None

        self.STATE_LAN_JOIN_discovery_socket = None
        self.STATE_LAN_JOIN_discovered_host_ip = None
        self.STATE_LAN_JOIN_connected = None
        self.STATE_LAN_JOIN_client_socket = None
        self.STATE_LAN_JOIN_is_host = None

        self.STATE_LAN_TEAM_PREVIEW_index = None
        self.STATE_LAN_TEAM_PREVIEW_team = None
        self.STATE_LAN_TEAM_PREVIEW_opponent_team = None
        self.STATE_LAN_TEAM_PREVIEW_selected_lead = None
        self.STATE_LAN_TEAM_PREVIEW_opponent_lead = None
        self.STATE_LAN_TEAM_PREVIEW_ready_sent = None
        self.STATE_LAN_TEAM_PREVIEW_opponent_ready = None
        self.STATE_LAN_TEAM_PREVIEW_pending_messages = None
        self.STATE_LAN_TEAM_PREVIEW_last_message = None

app = App()