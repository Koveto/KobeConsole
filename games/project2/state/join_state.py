import pygame

from battle.battle_font import BattleFont
from network.lan import *
from constants import *

class JoinState:

    def __init__(self):

        self.font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6
        )

        self.discovery_socket = (
            listen_for_hosts()
        )

        self.discovered_host_ip = None
        self.connected = False
        self.client_socket = None

    def handle_event(
        self,
        event
    ):
        pass

    def update(self):

        if self.discovery_socket is None:
            return

        try:

            data, address = (
                self.discovery_socket.recvfrom(
                    1024
                )
            )

            self.discovered_host_ip = (
                address[0]
            )

        except (
            BlockingIOError,
            OSError
        ):
            pass

        if (
            self.discovered_host_ip is not None
            and not self.connected
        ):

            try:

                self.client_socket = (
                    connect_to_server(
                        self.discovered_host_ip
                    )
                )

                self.connected = True
                self.state_manager.change(
                    STATE_LAN_BATTLE
                )

            except OSError:

                pass

    def draw(
        self,
        surface
    ):

        surface.fill(
            (255, 255, 255)
        )

        if self.discovered_host_ip:

            self.font.draw_text(
                surface,
                self.discovered_host_ip,
                40,
                80
            )

        status = (
            "CONNECTED"
            if self.connected
            else "SEARCHING..."
        )

        self.font.draw_text(
            surface,
            status,
            40,
            40
        )