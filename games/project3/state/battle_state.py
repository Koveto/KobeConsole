import os
import random
import pygame
from constants import *

from battle.battle_font import BattleFont
from pokemon.pkmn_sprite import *
from pokemon.pkmn_data import *
from pokemon.pkmn_battle import BattlePokemon
from input_manager_pkmn import *
from battle.battle_damage import (
    calculate_damage
)

type_names = {
    "Electric": "ELEC",
    "Psychic": "PSYCH",
    "Fighting": "FIGHT",
    "Poison": "POISN",
    "Ground": "GROND",
    "Flying": "FLYING",
    "Dragon": "DRAGON",
    "Normal": "NORML",
    "Water": "WATER",
    "Grass": "GRASS",
    "Fire": "FIRE",
    "Ice": "ICE",
    "Rock": "ROCK",
    "Ghost": "GHOST",
    "Steel": "STEEL",
    "Fairy": "FAIRY",
    "Dark": "DARK",
    "Bug": "BUG"
}

TYPE_COLORS = {
    "Fire": (255, 80, 0),
    "Water": (0, 120, 255),
    "Grass": (0, 200, 0),
    "Electric": (255, 255, 0),
    "Psychic": (255, 0, 180),
    "Ice": (120, 220, 255),
    "Rock": (160, 140, 80),
    "Ground": (180, 120, 40),
    "Poison": (180, 0, 180),
    "Ghost": (100, 60, 160),
    "Dragon": (80, 80, 255),
    "Dark": (60, 60, 60),
    "Steel": (160, 160, 180),
    "Fairy": (255, 120, 220),
    "Bug": (120, 180, 0),
    "Normal": (200, 200, 200),
    "Flying": (180, 220, 255),
    "Fighting": (200, 60, 60)
}

class BattleState:

    BACKGROUND_SHEET = None
    FRAME_SPRITE = None

    ROOT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    ENEMY_X = 144
    ENEMY_Y = 8

    PLAYER_X = 42
    PLAYER_Y = 48

    HP_BOX_SPRITE_PLAYER = None
    HP_FILL_SPRITE = None
    HP_BOX_SPRITE_ENEMY = None

    def __init__(self):

        self.background = self._load_background()
        self.frame = self._load_frame()
        self.menu_index = 0
        self.menu_state = "command"
        self.move_row = 0
        self.move_col = 0
        self.selected_action = None
        self.opponent_action = None
        self.waiting_for_opponent = False
        self.pending_messages = []
        self.move_sent = False
        self.dialogue_state = "command"
        self.dialogue_line_1 = ""
        self.dialogue_line_2 = ""
        self.turn_started = False
        self.phase_timer = 0
        self.battle_phase = None
        self.animation_duration = 15
        self.current_move_category = None
        self.current_attacker = None    
        self.party_preview_sprite = None
        self.player_attack_offset_x = 0
        self.player_attack_offset_y = 0

        self.enemy_attack_offset_x = 0
        self.enemy_attack_offset_y = 0

        self.flash_alpha = 0
        self.flash_color = None

        self.defender_visible = True
        self.displayed_player_hp = 0
        self.displayed_enemy_hp = 0

        self.damage_target = None
        self.damage_amount = 0

        self.first_user = None
        self.first_action = None

        self.second_user = None
        self.second_action = None

        self.second_move_pending = False
        self.party_cursor = 0
        self.fainted_side = None

        self.dialogue_font = BattleFont(
            "font_dialogue.png",
            glyph_w=7,
            glyph_h=13,
            scale=1,
            spacing=7
        )

        self.menu_font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6,
            row2="0123456789!? -   >/+"
        )

        self.info_font = BattleFont(
            "font_info.png",
            glyph_w=7,
            glyph_h=13,
            scale=1,
            spacing=7
        )

        self.hp_font = BattleFont(
            "font_hp.png",
            glyph_w=5,
            glyph_h=8,
            scale=1,
            spacing=5,
            row2="0123456789♂♀/"
        )

        self.enemy_species_no = random.randint(
            1,
            392
        )

        self.enemy_species = get_species(
            self.enemy_species_no
        )

        self.enemy_sprite = (
            load_enemy_sprite(
                self.enemy_species_no
            )
        )

        self.enemy = BattlePokemon(
            self.enemy_species,
            level=50
        )

        self.player_species_no = random.randint(
            1,
            392
        )

        self.player_species = get_species(
            self.player_species_no
        )

        self.player_sprite = (
            load_player_sprite(
                self.player_species_no
            )
        )

        self.player = BattlePokemon(
            self.player_species,
            level=50
        )

        self.hp_box = self._load_hp_box()
        self.enemy_hp_box = self._load_enemy_hp_box()
        self.hp_fill = self._load_hp_fill()
        self.displayed_player_hp = (
            self.player.current_hp
        )

        self.displayed_enemy_hp = (
            self.enemy.current_hp
        )

    def handle_event(
        self,
        event
    ):

        if self.battle_phase == "battle_over":

            if is_confirm(event):

                try:
                    self.client_socket.close()
                except OSError:
                    pass

                self.state_manager.shared.pop(
                    "client_socket",
                    None
                )

                self.state_manager.change(
                    STATE_MENU
                )

            return


        if self.battle_phase == "forced_switch":

            if is_up(event):

                self.party_cursor = max(
                    0,
                    self.party_cursor - 1
                )

                selected = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                self.party_preview_sprite = (
                    load_enemy_sprite(
                        selected.species["no"]
                    )
                )

            elif is_down(event):

                self.party_cursor = min(
                    len(self.player_team) - 1,
                    self.party_cursor + 1
                )

                selected = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                self.party_preview_sprite = (
                    load_enemy_sprite(
                        selected.species["no"]
                    )
                )

            elif is_confirm(event):

                pokemon = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                if (pokemon.current_hp > 0 and pokemon is not self.player):

                    self.client_socket.send(
                        f"SWITCH:{self.party_cursor}".encode()
                    )

                    self.player = pokemon

                    self.player_species = (
                        pokemon.species
                    )

                    self.player_species_no = (
                        pokemon.species["no"]
                    )

                    self.player_sprite = (
                        load_player_sprite(
                            self.player_species_no
                        )
                    )

                    self.displayed_player_hp = (
                        self.player.current_hp
                    )

                    self.selected_action = None
                    self.opponent_action = None

                    self.first_user = None
                    self.first_action = None

                    self.second_user = None
                    self.second_action = None

                    self.turn_started = False
                    self.second_move_pending = False

                    self.waiting_for_opponent = False

                    self.dialogue_state = "command"
                    self.menu_state = "command"

                    self.battle_phase = None
                    self.fainted_side = None

            return

        if self.battle_phase == "party_select":


            if is_cancel(event):

                self.battle_phase = None

                self.menu_state = "command"

                self.dialogue_state = "command"
                    
            if is_up(event):

                self.party_cursor = max(
                    0,
                    self.party_cursor - 1
                )

                selected = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                self.party_preview_sprite = (
                    load_enemy_sprite(
                        selected.species["no"]
                    )
                )

            elif is_down(event):

                self.party_cursor = min(
                    len(self.player_team) - 1,
                    self.party_cursor + 1
                )

                selected = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                self.party_preview_sprite = (
                    load_enemy_sprite(
                        selected.species["no"]
                    )
                )

            elif is_confirm(event):

                pokemon = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                if (pokemon.current_hp > 0 and pokemon is not self.player):

                    self.selected_action = {
                        "type": "swap",
                        "index": self.party_cursor
                    }

                    self.client_socket.send(
                        f"SWAP:{self.party_cursor}".encode()
                    )

                    self.waiting_for_opponent = True
                    self.dialogue_state = "waiting"

                    self.battle_phase = None

            return
                
        if self.dialogue_state == "battle":
        
            return
                
                
        if is_up(event):

            if self.menu_state == "command":

                self.menu_index = max(
                    0,
                    self.menu_index - 1
                )

            else:

                self.move_row = max(
                    0,
                    self.move_row - 1
                )

        elif is_down(event):

            if self.menu_state == "command":

                self.menu_index = min(
                    1,
                    self.menu_index + 1
                )

            else:

                self.move_row = min(
                    1,
                    self.move_row + 1
                )

        elif is_left(event):

            if self.menu_state == "moves":

                self.move_col = max(
                    0,
                    self.move_col - 1
                )

        elif is_right(event):

            if self.menu_state == "moves":

                self.move_col = min(
                    1,
                    self.move_col + 1
                )

        elif is_confirm(event):

            if self.menu_state == "command":

                if self.menu_index == 0:

                    self.menu_state = "moves"

                    self.move_row = 0
                    self.move_col = 0
                    self.dialogue_state = None

                elif self.menu_index == 1:

                    self.party_cursor = 0

                    selected = (
                        self.player_team[
                            self.party_cursor
                        ]
                    )

                    self.party_preview_sprite = (
                        load_enemy_sprite(
                            selected.species["no"]
                        )
                    )

                    self.battle_phase = "party_select"

            elif self.menu_state == "moves":
                move_index = (
                self.move_row * 2
                + self.move_col
                )
                move_name = (
                    self.player.moves[
                        move_index
                    ]
                )
                self.selected_action = {
                    "type": "move",
                    "move": move_name
                }

                self.client_socket.send(
                    f"MOVE:{move_name}".encode()
                )
                
                self.waiting_for_opponent = True
                self.dialogue_state = "waiting"

        elif is_cancel(event):

            if self.menu_state == "moves":

                self.menu_state = "command"
                self.menu_index = 0
                self.dialogue_state = "command"

    def update(self):

        if self.flash_alpha > 0:

            self.flash_alpha -= 8

            if self.flash_alpha < 0:

                self.flash_alpha = 0

        if self.battle_phase == "text_pause":
            self.update_text_pause()

        elif self.battle_phase == "physical_lunge":
            self.update_physical_lunge()

        elif self.battle_phase == "physical_return":
            self.update_physical_return()

        elif self.battle_phase == "special_flash":
            self.update_special_flash()

        elif self.battle_phase == "damage":
            self.update_damage_animation()

        elif self.battle_phase == "resolve_turn":
            self.resolve_turn_progress()

        elif self.battle_phase == "faint_message":
            self.update_faint_message()

        elif self.battle_phase == "forced_switch":
            pass


        if not hasattr(
            self,
            "battle_initialized"
        ):

            self.battle_initialized = True

            self.player_team = (
                self.state_manager.shared[
                    "player_team"
                ]
            )

            self.player_lead = (
                self.state_manager.shared[
                    "player_lead"
                ]
            )

            self.opponent_team = (
                self.state_manager.shared[
                    "opponent_team"
                ]
            )

            self.opponent_lead = (
                self.state_manager.shared[
                    "opponent_lead"
                ]
            )

            self.enemy = (
                self.opponent_team[
                    self.opponent_lead
                ]
            )

            self.enemy_species = (
                self.enemy.species
            )

            self.enemy_species_no = (
                self.enemy_species["no"]
            )


            self.enemy_sprite = (
                load_enemy_sprite(
                    self.enemy_species_no
                )
            )

            lead_pokemon = (
                self.player_team[
                    self.player_lead
                ]
            )

            self.player = lead_pokemon

            self.player_species = (
                self.player.species
            )

            self.player_species_no = (
                self.player_species["no"]
            )

            self.player_sprite = (
                load_player_sprite(
                    self.player_species_no
                )
            )

            self.displayed_player_hp = (
                self.player.current_hp
            )

            self.displayed_enemy_hp = (
                self.enemy.current_hp
            )

        if not hasattr(
            self,
            "client_socket"
        ):

            self.client_socket = (
                self.state_manager.shared[
                    "client_socket"
                ]
            )

        try:

            data = self.client_socket.recv(
                1024
            )

            if data:

                self.pending_messages.append(
                    data.decode()
                )

        except (
            BlockingIOError,
            OSError
        ):
            pass

        while self.pending_messages:

            message = (
                self.pending_messages.pop(0)
            )

            if message.startswith(
                "MOVE:"
            ):

                move_name = (
                    message.replace(
                        "MOVE:",
                        ""
                    )
                )

                self.opponent_action = {
                    "type": "move",
                    "move": move_name
                }

            elif message.startswith(
                "SWITCH:"
            ):

                switch_index = int(
                    message.replace(
                        "SWITCH:",
                        ""
                    )
                )

                self.enemy = (
                    self.opponent_team[
                        switch_index
                    ]
                )

                self.enemy_species = (
                    self.enemy.species
                )

                self.enemy_species_no = (
                    self.enemy_species["no"]
                )

                self.enemy_sprite = (
                    load_enemy_sprite(
                        self.enemy_species_no
                    )
                )

                self.displayed_enemy_hp = (
                    self.enemy.current_hp
                )

                self.selected_action = None
                self.opponent_action = None

                self.first_user = None
                self.first_action = None

                self.second_user = None
                self.second_action = None

                self.turn_started = False
                self.second_move_pending = False

                self.waiting_for_opponent = False
                self.menu_state = "command"
                self.dialogue_state = "command"

                self.battle_phase = None
                self.fainted_side = None

            elif message.startswith(
                "SWAP:"
            ):
                swap_index = int(
                    message.replace(
                        "SWAP:",
                        ""
                    )
                )

                self.opponent_action = {
                    "type": "swap",
                    "index": swap_index
                }

        if (
            self.selected_action is not None
            and self.opponent_action is not None
            and not self.turn_started
        ):
            self.turn_started = True

            if self.selected_action["type"] == "swap":

                pokemon = self.player_team[
                    self.selected_action["index"]
                ]

                self.player = pokemon

                self.player_species = (
                    pokemon.species
                )

                self.player_species_no = (
                    pokemon.species["no"]
                )

                self.player_sprite = (
                    load_player_sprite(
                        self.player_species_no
                    )
                )

                self.displayed_player_hp = (
                    self.player.current_hp
                )

            if self.opponent_action["type"] == "swap":

                pokemon = self.opponent_team[
                    self.opponent_action["index"]
                ]

                self.enemy = pokemon

                self.enemy_species = (
                    pokemon.species
                )

                self.enemy_species_no = (
                    pokemon.species["no"]
                )

                self.enemy_sprite = (
                    load_enemy_sprite(
                        self.enemy_species_no
                    )
                )

                self.displayed_enemy_hp = (
                    self.enemy.current_hp
                )

            if (
                self.selected_action["type"] == "swap"
                and self.opponent_action["type"] == "swap"
            ):

                self.selected_action = None
                self.opponent_action = None

                self.turn_started = False
                self.waiting_for_opponent = False

                self.dialogue_state = "command"
                self.menu_state = "command"

                return
            
            if self.player.speed >= self.enemy.speed:

                self.first_user = self.player
                first_species = self.player_species
                self.first_action = self.selected_action

                self.second_user = self.enemy
                second_species = self.enemy_species
                self.second_action = self.opponent_action

            else:

                self.first_user = self.enemy
                first_species = self.enemy_species
                self.first_action = self.opponent_action

                self.second_user = self.player
                second_species = self.player_species
                self.second_action = self.selected_action
            self.second_move_pending = True
            if self.first_action["type"] == "swap":

                if self.second_action["type"] == "swap":

                    self.selected_action = None
                    self.opponent_action = None

                    self.turn_started = False
                    self.waiting_for_opponent = False

                    self.dialogue_state = "command"
                    self.menu_state = "command"

                    return

                self.first_user = self.second_user
                self.first_action = self.second_action

                self.second_move_pending = False

                move_data = get_move(
                    self.first_action["move"]
                )

                damage = calculate_damage(
                    self.first_user,
                    self.player
                    if self.first_user is self.enemy
                    else self.enemy,
                    move_data
                )

                target = (
                    self.player
                    if self.first_user is self.enemy
                    else self.enemy
                )

                target.current_hp = max(
                    0,
                    target.current_hp - damage
                )

                self.damage_target = target

                self.current_move_category = (
                    move_data["category"]
                )

                self.current_attacker = self.first_user

                if self.first_user is self.player:

                    pokemon_name = (
                        self.player_species["name"].upper()
                    )

                else:

                    pokemon_name = (
                        "OPPOSING "
                        + self.enemy_species["name"].upper()
                    )

                self.dialogue_line_1 = (
                    pokemon_name
                )

                self.dialogue_line_2 = (
                    "USED "
                    + self.first_action["move"].upper()
                    + "!"
                )

                self.dialogue_state = "battle"

                self.phase_timer = 0
                self.battle_phase = "text_pause"

                return


            move_data = get_move(
                self.first_action["move"]
            )
            damage = calculate_damage(
                self.first_user,
                self.second_user,
                move_data
            )

            self.second_user.current_hp = max(
                0,
                self.second_user.current_hp - damage
            )

            self.damage_target = self.second_user

            self.phase_timer = 0
            self.battle_phase = "damage"

            self.current_move_category = (
                move_data["category"]
            )

            self.current_attacker = self.first_user

            if self.first_user is self.player:

                pokemon_name = (
                    first_species["name"].upper()
                )

            else:

                pokemon_name = (
                    "OPPOSING "
                    + first_species["name"].upper()
                )

            self.dialogue_line_1 = (
                pokemon_name
            )

            self.dialogue_line_2 = (
                "USED "
                + self.first_action["move"].upper()
                + "!"
            )
            self.dialogue_state = "battle"
            self.phase_timer = 0
            self.battle_phase = "text_pause"

            self.flash_color = (
                TYPE_COLORS[
                    move_data["type"]
                ]
            )


    def draw(
        self,
        surface
    ):

        surface.blit(
            self.background,
            (0, 0)
        )

        surface.blit(
            self.frame,
            (0, 112)
        )

        if (
            self.damage_target is not self.enemy
            or self.defender_visible
        ):

            surface.blit(
                self.enemy_sprite,
                (
                    BattleState.ENEMY_X
                    + self.enemy_attack_offset_x,
                    BattleState.ENEMY_Y
                    + self.enemy_attack_offset_y
                )
            )

        if (
            self.damage_target is not self.player
            or self.defender_visible
        ):

            surface.blit(
                self.player_sprite,
                (
                    BattleState.PLAYER_X
                    + self.player_attack_offset_x,
                    BattleState.PLAYER_Y
                    + self.player_attack_offset_y
                )
            )

        surface.blit(
            self.hp_box,
            (127, 74)
        )

        self.hp_font.draw_text(
            surface,
            self.player_species["name"]
            + self.player.gender,
            142,
            79
        )

        hp_text = (
            f"{self.displayed_player_hp}"
            f"/"
            f"{self.player.max_hp}"
        )

        hp_width = len(hp_text) * self.hp_font.spacing

        self.hp_font.draw_text(
            surface,
            hp_text,
            221 - hp_width,
            97
        )

        self.hp_font.draw_text(
            surface,
            str(self.player.level),
            207,
            79
        )

        hp_ratio = (
            self.displayed_player_hp
            / self.player.max_hp
        )

        hp_width = int(
            48 * hp_ratio
        )

        hp_surface = pygame.transform.scale(
            self.hp_fill,
            (
                hp_width,
                2
            )
        )

        surface.blit(
            hp_surface,
            (
                174,
                91
            )
        )

        surface.blit(
            self.enemy_hp_box,
            (13, 16)
        )

        self.hp_font.draw_text(
            surface,
            self.enemy_species["name"]
            + self.enemy.gender,
            20,
            21
        )

        self.hp_font.draw_text(
            surface,
            str(self.enemy.level),
            85,
            21
        )

        enemy_hp_ratio = (
            self.displayed_enemy_hp
            / self.enemy.max_hp
        )

        enemy_hp_width = int(
            48 * enemy_hp_ratio
        )

        enemy_hp_surface = pygame.transform.scale(
            self.hp_fill,
            (
                enemy_hp_width,
                2
            )
        )

        surface.blit(
            enemy_hp_surface,
            (
                52,
                33
            )
        )

        if (self.menu_state == "command"
            and not self.waiting_for_opponent):

            options = [
                "FIGHT",
                "POKEMON"
            ]

            for i, option in enumerate(
                options
            ):

                text = option

                if i == self.menu_index:

                    text = "> " + text

                self.menu_font.draw_text(
                    surface,
                    text,
                    180,
                    124 + i * 15
                )

        elif (self.menu_state == "moves"
              and not self.waiting_for_opponent):

            moves = (
                self.player.moves
            )

            positions = [
                (10, 122),
                (90, 122),
                (10, 138),
                (90, 138)
            ]

            cursor = (
                self.move_row * 2
                + self.move_col
            )

            selected_move_name = (
                moves[cursor]
            )

            selected_move = (
                get_move(
                    selected_move_name
                )
            )

            for i, move in enumerate(
                moves
            ):

                if i == cursor:

                    pygame.draw.rect(
                        surface,
                        (80, 120, 255),
                        (
                            positions[i][0] - 2,
                            positions[i][1] - 1,
                            75,
                            14
                        ),
                        1
                    )

                self.menu_font.draw_text(
                    surface,
                    move,
                    positions[i][0],
                    positions[i][1]
                )  

            move_type = type_names.get(
                selected_move["type"],
                selected_move["type"]
            ) 

            self.menu_font.draw_text(
                surface,
                f"TYPE/{move_type}",
                165,
                122
            )

            self.menu_font.draw_text(
                surface,
                f"POWER/{selected_move['power']}",
                165,
                138
            )

        if (
            self.battle_phase == "forced_switch"
            or self.battle_phase == "party_select"
        ):

            self.draw_party_menu(
                surface
            )

        if self.dialogue_state == "command":

            self.dialogue_font.draw_text(
                surface,
                "WHAT WILL",
                12,
                121
            )

            self.dialogue_font.draw_text(
                surface,
                f"{self.player_species['name'].upper()} DO?",
                12,
                136
            )

        elif self.dialogue_state == "waiting":

            self.dialogue_font.draw_text(
                surface,
                "WAITING FOR",
                12,
                121
            )

            self.dialogue_font.draw_text(
                surface,
                "OPPONENT...",
                12,
                136
            )

        elif self.dialogue_state == "battle":

            self.dialogue_font.draw_text(
                surface,
                self.dialogue_line_1,
                12,
                121
            )

            self.dialogue_font.draw_text(
                surface,
                self.dialogue_line_2,
                12,
                136
            )

        if self.flash_alpha > 0:

            overlay = pygame.Surface(
                (
                    surface.get_width(),
                    surface.get_height()
                )
            )

            overlay.fill(
                self.flash_color
            )

            overlay.set_alpha(
                self.flash_alpha
            )

            surface.blit(
                overlay,
                (0, 0)
            )

    def all_fainted(
        self,
        team
    ):
        return all(
            pokemon.current_hp <= 0
            for pokemon in team
        )
    
    def draw_party_menu(
        self,
        surface
    ):

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (10, 10, 220, 100)
        )

        for i, pokemon in enumerate(
            self.player_team
        ):

            y = 16 + i * 14

            if pokemon.current_hp <= 0:

                prefix = "X "

            else:

                prefix = "  "

            if i == self.party_cursor:

                pygame.draw.rect(
                    surface,
                    (80, 120, 255),
                    (
                        12,
                        y - 1,
                        140,
                        14
                    ),
                    1
                )

            text = (
                f"{prefix}"
                f"{pokemon.species['name']} "
                f"{pokemon.current_hp}/"
                f"{pokemon.max_hp}"
            )

            self.menu_font.draw_text(
                surface,
                text,
                16,
                y
            )
        if self.party_preview_sprite:

            surface.blit(
                self.party_preview_sprite,
                (
                    165,
                    25
                )
            )

    def _load_enemy_hp_box(self):

        if BattleState.HP_BOX_SPRITE_ENEMY is None:

            filepath = os.path.join(
                BattleState.ROOT,
                "sprites",
                "hp_enemy_0.png"
            )

            BattleState.HP_BOX_SPRITE_ENEMY = (
                pygame.image.load(
                    filepath
                ).convert()
            )

            BattleState.HP_BOX_SPRITE_ENEMY.set_colorkey(
                (255, 0, 228)
            )

        return BattleState.HP_BOX_SPRITE_ENEMY
    
    def update_faint_message(self):

        self.phase_timer -= 1

        if self.phase_timer <= 0:

            if self.fainted_side == "player":

                self.party_cursor = 0

                selected = (
                    self.player_team[
                        self.party_cursor
                    ]
                )

                self.party_preview_sprite = (
                    load_enemy_sprite(
                        selected.species["no"]
                    )
                )

                self.battle_phase = (
                    "forced_switch"
                )


            else:

                pass

    def resolve_turn_progress(self):

        if (
            self.player.current_hp <= 0
            and self.enemy.current_hp <= 0
        ):

            self.dialogue_line_1 = (
                "DRAW!"
            )

            self.dialogue_line_2 = (
                "PRESS A"
            )

            self.dialogue_state = "battle"

            self.battle_phase = "battle_over"

            return

        if self.all_fainted(
            self.opponent_team
        ):

            self.dialogue_line_1 = (
                "YOU WIN!"
            )

            self.dialogue_line_2 = ""

            self.dialogue_state = "battle"

            self.battle_phase = "battle_over"

            return


        if self.all_fainted(
            self.player_team
        ):

            self.dialogue_line_1 = (
                "YOU LOSE!"
            )

            self.dialogue_line_2 = ""

            self.dialogue_state = "battle"

            self.battle_phase = "battle_over"

            return

        if self.enemy.current_hp <= 0:

            self.dialogue_line_1 = (
                self.enemy_species["name"].upper()
            )

            self.dialogue_line_2 = "FAINTED!"

            self.dialogue_state = "battle"

            self.phase_timer = 180

            self.fainted_side = "enemy"

            self.battle_phase = "faint_message"

            return

        if self.player.current_hp <= 0:

            self.dialogue_line_1 = (
                self.player_species["name"].upper()
            )

            self.dialogue_line_2 = "FAINTED!"

            self.dialogue_state = "battle"

            self.phase_timer = 180

            self.fainted_side = "player"

            self.battle_phase = "faint_message"

            return

        if self.second_move_pending:
        
            self.second_move_pending = False

            if self.second_action["type"] == "swap":

                self.selected_action = None
                self.opponent_action = None

                self.first_user = None
                self.first_action = None

                self.second_user = None
                self.second_action = None

                self.turn_started = False
                self.second_move_pending = False

                self.waiting_for_opponent = False

                self.menu_state = "command"
                self.dialogue_state = "command"

                self.battle_phase = None

                return

            move_data = get_move(
                self.second_action["move"]
            )

            damage = calculate_damage(
                self.second_user,
                self.first_user,
                move_data
            )

            self.first_user.current_hp = max(
                0,
                self.first_user.current_hp - damage
            )

            self.damage_target = (
                self.first_user
            )

            self.current_attacker = (
                self.second_user
            )

            self.current_move_category = (
                move_data["category"]
            )

            if self.second_user is self.player:

                pokemon_name = (
                    self.player_species["name"].upper()
                )

            else:

                pokemon_name = (
                    "OPPOSING "
                    + self.enemy_species["name"].upper()
                )

            self.dialogue_line_1 = pokemon_name

            self.dialogue_line_2 = (
                "USED "
                + self.second_action["move"].upper()
                + "!"
            )

            self.phase_timer = 0
            self.battle_phase = "text_pause"

            self.flash_color = (
                TYPE_COLORS[
                    move_data["type"]
                ]
            )

            return

        self.selected_action = None
        self.opponent_action = None

        self.first_user = None
        self.first_action = None

        self.second_user = None
        self.second_action = None

        self.turn_started = False
        self.second_move_pending = False

        self.waiting_for_opponent = False

        self.menu_state = "command"
        self.dialogue_state = "command"

        self.battle_phase = None

    def update_special_flash(self):

        self.phase_timer += 1

        progress = self.phase_timer / 30

        self.flash_alpha = int(
            180 * (1 - progress)
        )

        if self.phase_timer >= 30:

            self.flash_alpha = 0
            self.phase_timer = 0

            self.battle_phase = "damage"

    def update_text_pause(self):

        self.phase_timer += 1

        if self.phase_timer >= 60:

            self.phase_timer = 0

            if self.current_move_category == "Physical":

                self.battle_phase = (
                    "physical_lunge"
                )

            else:

                self.flash_alpha = 180

                self.battle_phase = (
                    "special_flash"
                )

    def update_damage_animation(self):

        self.phase_timer += 1

        self.defender_visible = (
            (self.phase_timer // 5) % 2 == 0
        )

        if self.damage_target is self.player:

            if (
                self.displayed_player_hp
                > self.player.current_hp
            ):
                self.displayed_player_hp -= 1

        else:

            if (
                self.displayed_enemy_hp
                > self.enemy.current_hp
            ):
                self.displayed_enemy_hp -= 1

        animation_finished = True

        if self.damage_target is self.player:

            animation_finished = (
                self.displayed_player_hp
                == self.player.current_hp
            )

        else:

            animation_finished = (
                self.displayed_enemy_hp
                == self.enemy.current_hp
            )

        if animation_finished:

            self.defender_visible = True

            self.battle_phase = "resolve_turn"

            self.phase_timer = 0

    def update_physical_lunge(self):

        self.phase_timer += 1

        progress = (
            self.phase_timer
            / self.animation_duration
        )

        if self.current_attacker is self.player:

            self.player_attack_offset_x = int(
                96 * progress
            )

            self.player_attack_offset_y = int(
                -48 * progress
            )

        else:

            self.enemy_attack_offset_x = int(
                -96 * progress
            )

            self.enemy_attack_offset_y = int(
                48 * progress
            )

        if self.phase_timer >= self.animation_duration:

            self.phase_timer = 0

            self.battle_phase = (
                "physical_return"
            )

    def update_physical_return(self):

        self.phase_timer += 1

        progress = (
            self.phase_timer
            / self.animation_duration
        )

        if self.current_attacker is self.player:

            self.player_attack_offset_x = int(
                96 * (1 - progress)
            )

            self.player_attack_offset_y = int(
                -48 * (1 - progress)
            )

        else:

            self.enemy_attack_offset_x = int(
                -96 * (1 - progress)
            )

            self.enemy_attack_offset_y = int(
                48 * (1 - progress)
            )

        if self.phase_timer >= self.animation_duration:

            self.player_attack_offset_x = 0
            self.player_attack_offset_y = 0

            self.enemy_attack_offset_x = 0
            self.enemy_attack_offset_y = 0

            self.phase_timer = 0

            self.battle_phase = "damage"
            

    def _load_hp_fill(self):

        if BattleState.HP_FILL_SPRITE is None:

            filepath = os.path.join(
                BattleState.ROOT,
                "sprites",
                "hpfill.png"
            )

            BattleState.HP_FILL_SPRITE = (
                pygame.image.load(
                    filepath
                ).convert()
            )

        return BattleState.HP_FILL_SPRITE

    def _load_hp_box(self):

        if BattleState.HP_BOX_SPRITE_PLAYER is None:

            filepath = os.path.join(
                BattleState.ROOT,
                "sprites",
                "hp_plyr_0.png"
            )

            BattleState.HP_BOX_SPRITE_PLAYER = (
                pygame.image.load(
                    filepath
                ).convert()
            )

            BattleState.HP_BOX_SPRITE_PLAYER.set_colorkey(
                (255, 0, 228)
            )

        return BattleState.HP_BOX_SPRITE_PLAYER

    def _load_background(self):

        filepath = os.path.join(
            BattleState.ROOT,
            "sprites",
            "battlebackgrounds.png"
        )

        if BattleState.BACKGROUND_SHEET is None:

            BattleState.BACKGROUND_SHEET = (
                pygame.image.load(
                    filepath
                ).convert_alpha()
            )

        sheet = BattleState.BACKGROUND_SHEET

        index = random.randrange(15)

        col = index % 4
        row = index // 4

        rect = pygame.Rect(
            col * 240,
            row * 112,
            240,
            112
        )

        return sheet.subsurface(rect)

    def _load_frame(self):

        if BattleState.FRAME_SPRITE is None:

            filepath = os.path.join(
                BattleState.ROOT,
                "sprites",
                "battleframe.png"
            )

            BattleState.FRAME_SPRITE = (
                pygame.image.load(
                    filepath
                ).convert_alpha()
            )

        return BattleState.FRAME_SPRITE