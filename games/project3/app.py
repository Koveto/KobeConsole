from constants import *

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
        self.selected_team_data = None
        self.game_mode = None
        self.allow_team_change = True
        self.allow_lead_change = True
        self.pending_opponent_team = None
        self.pending_opponent_trainer = None
        self.battle_result = None
        self.restore_team_select = False
        self.restore_single_menu_trainer = False
        self.endless_active = False
        self.endless_wins = 0
        self.endless_trainer_index = None
        self.tournament_active = False
        self.tournament_round = 0
        self.tournament_current_trainer = None
        self.tournament_quarterfinals = []
        self.tournament_semifinals = []
        self.tournament_finals = []
        self.tournament_champion = None
        self.gyms_data = []

        self.option_omniscient = False
        self.option_pkmn_animation = True
        self.option_music_shuffle = False
        self.option_mute = False
        self.option_level = 100
        self.option_level_npc = 100
        self.option_fanart = False

        self.LAUNCHER_MENU_index = 0
        self.LAUNCHER_MENU_options = ("Single Player",
                                      "LAN Multiplayer",
                                      "Damage Calculator",
                                      "Team Builder",
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
        self.TEAM_PREVIEW_return_state = None
        self.TEAM_PREVIEW_index = 0
        self.TEAM_PREVIEW_column = 0

        self.PKMN_VIEW_pokemon = None
        self.PKMN_VIEW_move_index = None
        self.PKMN_VIEW_mode = None
        self.PKMN_VIEW_index = 0
        self.PKMN_VIEW_column = 0

        self.SPECIES_VIEW_pokemon = None
        self.SPECIES_VIEW_mode = None

        self.TEAM_SELECT_team_sent = False
        self.TEAM_SELECT_opponent_team = None
        self.TEAM_SELECT_error = None
        self.TEAM_SELECT_return_state = None
        self.TEAM_SELECT_index = 0
        self.TEAM_SELECT_scroll = 0
        self.TEAM_SELECT_preview_team = []
        self.TEAM_SELECT_mode = "BATTLE"
        self.TEAM_SELECT_selecting_pokemon = False
        self.TEAM_SELECT_pokemon_index = 0
        self.TEAM_SELECT_import_target = None
        self.TEAM_SELECT_return_state = None
        self.TEAM_SELECT_submenu = False
        self.TEAM_SELECT_submenu_index = 0
        self.TEAM_SELECT_restore_index = None
        self.TEAM_SELECT_restore_scroll = None

        self.OPTIONS_index = 0
        self.OPTIONS_editing_name = False
        self.OPTIONS_scroll = 0

        self.KEYBOARD_row = 0
        self.KEYBOARD_column = 0
        self.KEYBOARD_text = ""
        self.KEYBOARD_mode = "PLAYER_NAME"
        self.KEYBOARD_return_state = OPTIONS
        self.KEYBOARD_team_index = None

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
        self.SINGLE_MENU_TRAINER_preview_team = []
        self.SINGLE_MENU_TRAINER_my_team_preview = []
        
        self.SINGLE_DEFEND_GYM_index = 0
        self.SINGLE_DEFEND_GYM_scroll = 0
        self.SINGLE_DEFEND_GYM_trainer_index = 0
        self.SINGLE_DEFEND_GYM_selected_gym = None
        self.SINGLE_DEFEND_GYM_selected_type = None
        self.SINGLE_DEFEND_GYM_selected_trainer = None
        self.SINGLE_DEFEND_GYM_trainer_indices = {}

        self.DAMAGE_CALCULATOR_attacker = None
        self.DAMAGE_CALCULATOR_defender = None
        self.DAMAGE_CALCULATOR_index = 0
        self.DAMAGE_CALCULATOR_column = 1

app = App()