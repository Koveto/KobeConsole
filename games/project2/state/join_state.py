import pygame

from battle.battle_font import BattleFont
from network.lan import listen_for_hosts


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

    def draw(
        self,
        surface
    ):

        surface.fill(
            (255, 255, 255)
        )

        self.font.draw_text(
            surface,
            "SEARCHING...",
            40,
            40
        )

        if self.discovered_host_ip:

            self.font.draw_text(
                surface,
                self.discovered_host_ip,
                40,
                80
            )