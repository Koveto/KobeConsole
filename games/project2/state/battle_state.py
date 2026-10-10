import os
import random
import pygame
from battle.battle_font import BattleFont

class BattleState:

    BACKGROUND_SHEET = None
    FRAME_SPRITE = None

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
            "DIALOGUE FONT",
            10,
            115
        )

        self.menu_font.draw_text(
            surface,
            "MENU FONT",
            10,
            130
        )

        self.info_font.draw_text(
            surface,
            "INFO FONT",
            10,
            145
        )

    def _load_background(self):

        root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        filepath = os.path.join(
            root,
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

            root = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    ".."
                )
            )

            filepath = os.path.join(
                root,
                "sprites",
                "battleframe.png"
            )

            BattleState.FRAME_SPRITE = (
                pygame.image.load(
                    filepath
                ).convert_alpha()
            )

        return BattleState.FRAME_SPRITE