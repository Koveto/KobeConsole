import random

from battle.battle_font import BattleFont
from pokemon.pkmn_data import get_species
from input_manager_pkmn import *


class LanBattleState:

    def __init__(self):

        self.font = BattleFont(
            "font_menu.png",
            glyph_w=6,
            glyph_h=13,
            scale=1,
            spacing=6
        )

        self.team = []

        for _ in range(6):

            species_no = random.randint(
                1,
                392
            )

            self.team.append(
                get_species(
                    species_no
                )
            )

        self.index = 0

        self.selected_lead = None

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
            "CHOOSE LEAD",
            10,
            10
        )

        for i, pokemon in enumerate(
            self.team
        ):

            name = pokemon["name"]

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