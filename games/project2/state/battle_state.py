from battle.battle_background import (
    load_battle_background
)
import random


class BattleState:

    def __init__(self):

        self.background = (
            load_battle_background(
                random.randint(0, 14)
            )
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