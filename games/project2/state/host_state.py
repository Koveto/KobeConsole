import pygame

from battle.battle_font import BattleFont
from constants import *
from input_manager_pkmn import *
import pygame

from battle.battle_font import BattleFont
from network.lan import broadcast_host

class HostState:

    def __init__(self):

        self.font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6
        )
        self.last_broadcast_time = 0

    def handle_event(
        self,
        event
    ):

        if is_cancel(event):

            self.state_manager.change(
                STATE_LAN_MENU
            )

    def update(self):

        current_time = pygame.time.get_ticks()

        if (
            current_time
            - self.last_broadcast_time
            > 1000
        ):

            broadcast_host()

            self.last_broadcast_time = (
                current_time
            )

    def draw(
        self,
        surface
    ):

        surface.fill(
            (255, 255, 255)
        )

        self.font.draw_text(
            surface,
            "HOSTING...",
            60,
            70
        )