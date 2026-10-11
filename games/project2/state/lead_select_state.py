import random

from battle.battle_font import BattleFont
from pokemon.pkmn_data import get_species
from pokemon.pkmn_sprite import load_enemy_sprite
from input_manager_pkmn import *
from constants import *


class LeadSelectState:

    def __init__(self):

        self.font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6
        )

        self.team = []
        self.team_sprites = []
        self.team_sent = False
        self.opponent_team = []

        for _ in range(6):

            species_no = random.randint(
                1,
                392
            )

            species = get_species(
                species_no
            )

            self.team.append(
                {
                    "species_no": species_no,
                    "species": species
                }
            )

            self.team_sprites.append(
                load_enemy_sprite(
                    species_no
                )
            )

        self.index = 0

        self.selected_lead = None
        self.opponent_ready = False
        self.ready_sent = False

    def handle_event(
        self,
        event
    ):

        if self.selected_lead is not None:
            return

        if is_up(event):

            self.index = max(
                0,
                self.index - 1
            )

        elif is_down(event):

            self.index = min(
                5,
                self.index + 1
            )

        elif is_confirm(event):

            self.selected_lead = (
                self.index
            )

            if not self.ready_sent:

                self.client_socket.send(
                    f"LEAD:{self.index}".encode()
                )

                self.ready_sent = True


    def update(self):

        if not hasattr(
            self,
            "client_socket"
        ):

            self.client_socket = (
                self.state_manager.shared[
                    "client_socket"
                ]
            )

            self.is_host = (
                self.state_manager.shared[
                    "is_host"
                ]
            )
        if not self.team_sent:

            team_ids = []

            for pokemon in self.team:

                team_ids.append(
                    str(
                        pokemon["species_no"]
                    )
                )

            self.client_socket.send(
                (
                    "TEAM:"
                    + ",".join(team_ids)
                ).encode()
            )

            self.team_sent = True

        try:

            message = (
                self.client_socket.recv(
                    1024
                ).decode()
            )

            if message.startswith(
                "TEAM:"
            ):

                team_data = message.replace(
                    "TEAM:",
                    ""
                )

                species_ids = (
                    team_data.split(",")
                )

                self.opponent_team = []

                for species_id in species_ids:

                    self.opponent_team.append(
                        get_species(
                            int(species_id)
                        )
                    )
            elif message.startswith(
                "LEAD:"
            ):

                self.opponent_ready = True

        except (
            BlockingIOError,
            OSError
        ):
            pass

        if (
            self.selected_lead is not None
            and self.opponent_ready
        ):

            self.state_manager.shared[
                "player_team"
            ] = self.team

            self.state_manager.shared[
                "opponent_team"
            ] = self.opponent_team

            self.state_manager.shared[
                "player_lead"
            ] = self.selected_lead

            self.state_manager.change(
                STATE_BATTLE
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
            "CHOOSE LEAD",
            10,
            10
        )

        for i, pokemon in enumerate(
            self.team
        ):

            name = pokemon[
                "species"
            ]["name"]

            if (
                self.selected_lead is None
                and i == self.index
            ):

                name = "> " + name

            elif (
                self.selected_lead == i
            ):

                name = "* " + name

            self.font.draw_text(
                surface,
                name,
                10,
                30 + i * 15
            )

        preview_index = (
            self.selected_lead
            if self.selected_lead is not None
            else self.index
        )

        sprite = self.team_sprites[
            preview_index
        ]

        sprite_x = (
            surface.get_width()
            - sprite.get_width()
        ) // 2

        surface.blit(
            sprite,
            (
                sprite_x,
                35
            )
        )

        if self.selected_lead is None:

            self.font.draw_text(
                surface,
                "SELECT A LEAD",
                10,
                140
            )

        else:

            self.font.draw_text(
                surface,
                "READY",
                10,
                140
            )

        if self.opponent_ready:

            self.font.draw_text(
                surface,
                "OPPONENT READY",
                10,
                155
            )

        for i, pokemon in enumerate(
            self.opponent_team
        ):

            self.font.draw_text(
                surface,
                pokemon["name"],
                170,
                30 + i * 15
            )