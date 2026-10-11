import pygame

from battle.battle_font import BattleFont
from constants import *
from input_manager_pkmn import *
import pygame

from battle.battle_font import BattleFont
from network.lan import *

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
        self.ip_address = get_local_ip()

        self.server_socket = create_server(
            self.ip_address
        )

        self.client_socket = None

        self.connected = False

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
        if not self.connected:

            try:

                (
                    self.client_socket,
                    address
                ) = self.server_socket.accept()

                self.connected = True

            except (
                BlockingIOError,
                OSError
            ):
                pass

    def draw(
        self,
        surface
    ):

        surface.fill(
            (255, 255, 255)
        )
        
        status = (
            "CONNECTED"
            if self.connected
            else "HOSTING..."
        )

        self.font.draw_text(
            surface,
            status,
            60,
            70
        )