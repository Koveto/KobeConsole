import os
import random
import pygame

from battle.battle_font import BattleFont
from pokemon.pkmn_sprite import *
from pokemon.pkmn_data import *
from pokemon.pkmn_battle import BattlePokemon
from input_manager_pkmn import *

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

        self.player_attack_offset_x = 0
        self.enemy_attack_offset_x = 0

        self.attack_offset_y = 0

        self.flash_alpha = 0
        self.flash_color = None

        self.defender_visible = True

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

    def handle_event(
        self,
        event
    ):
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

        if self.phase_timer > 0:

            self.phase_timer -= 1

            if self.phase_timer == 60:

                self.player_attack_offset_x = 0
                self.enemy_attack_offset_x = 0

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

            enemy_pokemon = (
                self.opponent_team[0]
            )
            print(
                enemy_pokemon
            )

            self.enemy_species = (
                enemy_pokemon
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

            self.player_species_no = (
                lead_pokemon[
                    "species_no"
                ]
            )

            self.player_species = (
                lead_pokemon[
                    "species"
                ]
            )

            self.player_sprite = (
                load_player_sprite(
                    self.player_species_no
                )
            )

            self.enemy = BattlePokemon(
                self.enemy_species,
                level=50
            )

            self.player = BattlePokemon(
                self.player_species,
                level=50
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
        if (
            self.selected_action is not None
            and self.opponent_action is not None
            and not self.turn_started
        ):
            self.turn_started = True

            
            if self.player.speed >= self.enemy.speed:

                first_user = self.player
                first_species = self.player_species
                first_action = self.selected_action

                second_user = self.enemy
                second_species = self.enemy_species
                second_action = self.opponent_action

            else:

                first_user = self.enemy
                first_species = self.enemy_species
                first_action = self.opponent_action

                second_user = self.player
                second_species = self.player_species
                second_action = self.selected_action

            if first_user is self.player:

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
                + first_action["move"].upper()
                + "!"
            )
            self.dialogue_state = "battle"
            self.phase_timer = 120
            if first_user is self.player:

                self.player_attack_offset_x = 8

            else:

                self.enemy_attack_offset_x = -8


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

        surface.blit(
            self.enemy_sprite,
            (
                BattleState.ENEMY_X
                + self.enemy_attack_offset_x,

                BattleState.ENEMY_Y
            )
        )

        surface.blit(
            self.player_sprite,
            (
                BattleState.PLAYER_X
                + self.player_attack_offset_x,

                BattleState.PLAYER_Y
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
            f"{self.player.current_hp}"
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
            self.player.current_hp
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
            self.enemy.current_hp
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