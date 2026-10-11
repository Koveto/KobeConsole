import math
import random


class BattlePokemon:

    def __init__(
        self,
        species,
        level
    ):

        self.species = species

        self.moves = (
            species["moves"]
        )

        self.level = level

        self.evs = [
            0, 0, 0,
            0, 0, 0
        ]

        self.ivs = [
            0, 0, 0,
            0, 0, 0
        ]

        self.nature = None

        self.gender = random.choice(
            ["♂", "♀"]
        )

        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.max_hp

        self.atk = self.calculate_atk()
        self.defense = self.calculate_def()
        self.spatk = self.calculate_spatk()
        self.spdef = self.calculate_spdef()
        self.speed = self.calculate_spe()

    def nature_modifier(
        self,
        stat_name
    ):

        if self.nature is None:
            return 1.0

        return 1.0

    def calculate_max_hp(self):

        base_hp = self.species["stats"]["HP"]

        return math.floor(
            (
                (
                    2 * base_hp
                    + self.ivs[0]
                    + self.evs[0] / 4
                )
                * self.level
            ) / 100
        ) + self.level + 10

    def calculate_other_stat(
        self,
        base_stat,
        iv,
        ev,
        nature
    ):

        return math.floor(
            nature * (
                math.floor(
                    (
                        (
                            2 * base_stat
                            + iv
                            + ev / 4
                        )
                        * self.level
                    ) / 100
                )
                + 5
            )
        )

    def calculate_atk(self):

        return self.calculate_other_stat(
            self.species["stats"]["Atk"],
            self.ivs[1],
            self.evs[1],
            self.nature_modifier("atk")
        )

    def calculate_def(self):

        return self.calculate_other_stat(
            self.species["stats"]["Def"],
            self.ivs[2],
            self.evs[2],
            self.nature_modifier("def")
        )

    def calculate_spatk(self):

        return self.calculate_other_stat(
            self.species["stats"]["SpAtk"],
            self.ivs[3],
            self.evs[3],
            self.nature_modifier("spatk")
        )

    def calculate_spdef(self):

        return self.calculate_other_stat(
            self.species["stats"]["SpDef"],
            self.ivs[4],
            self.evs[4],
            self.nature_modifier("spdef")
        )

    def calculate_spe(self):

        return self.calculate_other_stat(
            self.species["stats"]["Spd"],
            self.ivs[5],
            self.evs[5],
            self.nature_modifier("speed")
        )