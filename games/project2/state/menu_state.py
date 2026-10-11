import os
import pygame

from battle.battle_font import BattleFont
from input_manager_pkmn import *
from constants import *


class MenuState:

    CURSOR = None

    def __init__(self):

        self.options = [
            "Single Player",
            "LAN Multiplayer"
        ]

        self.index = 0

        self.font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6
        )

        self.cursor = self._load_cursor()

    def handle_event(
        self,
        event
    ):

        if is_up(event):

            self.index = max(
                0,
                self.index - 1
            )

        elif is_down(event):

            self.index = min(
                len(self.options) - 1,
                self.index + 1
            )

        elif is_confirm(event):

            if self.index == 0:

                self.state_manager.change(
                    STATE_BATTLE
                )

            elif self.index == 1:

                self.state_manager.change(
                    STATE_LAN_MENU
                )

    def update(self):
        pass

    def draw(
        self,
        surface
    ):

        surface.fill(
            (255, 255, 255)
        )

        self.font.draw_text(
            surface,
            "Pokemon Battle Simulator",
            70,
            40
        )

        for i, option in enumerate(
            self.options
        ):

            y = 80 + i * 20

            if i == self.index:

                surface.blit(
                    self.cursor,
                    (
                        30,
                        y + 3
                    )
                )

            self.font.draw_text(
                surface,
                option,
                45,
                y
            )

    def _load_cursor(self):

        if MenuState.CURSOR is None:

            root = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    ".."
                )
            )

            filepath = os.path.join(
                root,
                "sprites",
                "cursor.png"
            )

            MenuState.CURSOR = (
                pygame.image.load(
                    filepath
                ).convert()
            )

            MenuState.CURSOR.set_colorkey(
                (255, 0, 228)
            )

        return MenuState.CURSOR