class App:
    def __init__(self):
        self.state = None
        self.previous_state = None
        self.screen = None
        self.font0 = None
        self.connection_socket = None
        self.connection_is_host = None
        self.connection_buffer = ""
        self.player_team = None
        self.opponent_team = None
        self.available_teams = []
        self.teams_data = []
        self.player_name = "KOBE"
        self.player_sprite = 0
        self.pkmn_animation_time = 0
        self.music_data = {}
        self.current_music = None
        self.current_music_mode = None
        self.muted = False
        self.player_lead = None
        self.opponent_lead = None
        self.trainers_data = []
        self.single_battle_mode = None
        self.selected_trainer_data = None
        self.preview_index = 0
        self.preview_column = 0
        self.team_select_index = 0
        self.team_select_scroll = 0
        self.team_select_preview_team = []
        self.selected_team_data = None


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

        self.TEAM_PREVIEW_opponent_team = None
        self.TEAM_PREVIEW_ready_sent = None
        self.TEAM_PREVIEW_opponent_ready = None

        self.PKMN_VIEW_pokemon = None
        self.PKMN_VIEW_move_index = None
        self.PKMN_VIEW_mode = None
        self.PKMN_VIEW_index = 0
        self.PKMN_VIEW_column = 0

        self.SPECIES_VIEW_pokemon = None
        self.SPECIES_VIEW_mode = None

        self.TEAM_SELECT_team_sent = False
        self.TEAM_SELECT_opponent_team = None

        self.OPTIONS_index = 0
        self.OPTIONS_editing_name = False
        self.OPTIONS_scroll = 0
        self.option_omniscient = False
        self.option_pkmn_animation = True
        self.option_music_shuffle = False
        self.option_mute = False
        self.option_level = 100
        self.option_level_npc = 100

        self.KEYBOARD_row = 0
        self.KEYBOARD_column = 0
        self.KEYBOARD_text = ""

        self.OPTIONS_MUSIC_index = 0
        self.OPTIONS_MUSIC_scroll = 0

        self.SINGLE_MENU_index = 0
        self.SINGLE_MENU_options = (
            "Trainer Battle",
            "Endless Battle",
            "Defend Gym",
            "Tournament"
        )

        self.SINGLE_MENU_TRAINER_index = 0
        self.SINGLE_MENU_TRAINER_options = (
            "Random Team",
            "My Team",
            "Trainer"
        )
        self.SINGLE_MENU_TRAINER_selected_trainer = 0
        self.SINGLE_MENU_TRAINER_selected_team = 0

app = App()