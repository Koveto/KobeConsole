import os
import random
import pygame
from battle.battle_font import BattleFont
from pokemon.pkmn_sprite import *
from pokemon.pkmn_data import *

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

    def __init__(self):

        self.background = self._load_background()
        self.frame = self._load_frame()
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
            spacing=6
        )
        self.info_font = BattleFont(
            "font_info.png",
            glyph_w=7,
            glyph_h=13,
            scale=1,
            spacing=7
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
        self.hp_box = self._load_hp_box()

    def handle_event(
        self,
        event
    ):
        pass

    def update(self):
        pass

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

        self.dialogue_font.draw_text(
            surface,
            self.player_species["name"],
            120,
            145
        )

        self.menu_font.draw_text(
            surface,
            "MENU FONT",
            10,
            130
        )

        self.info_font.draw_text(
            surface,
            str(self.enemy_species["types"]),
            10,
            130
        )
        surface.blit(
            self.enemy_sprite,
            (
                BattleState.ENEMY_X,
                BattleState.ENEMY_Y
            )
        )
        surface.blit(
            self.player_sprite,
            (
                BattleState.PLAYER_X,
                BattleState.PLAYER_Y
            )
        )
        surface.blit(
            self.hp_box,
            (127, 74)
        )

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