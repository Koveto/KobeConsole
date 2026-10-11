import math
import random

from pokemon.pkmn_typechart import (
    combined_effectiveness
)

def calculate_damage(
    attacker,
    defender,
    move_data
):

    if move_data["category"] == "Physical":

        attack_stat = attacker.atk
        defense_stat = defender.defense

    else:

        attack_stat = attacker.spatk
        defense_stat = defender.spdef

    stab = 1.0

    if (
        move_data["type"]
        in attacker.species["types"]
    ):
        stab = 1.5

    type_multiplier = (
        combined_effectiveness(
            move_data["type"],
            defender.species["types"]
        )
    )

    rand = random.uniform(
        0.85,
        1.0
    )

    base_damage = (
        2
        + math.floor(
            (
                (
                    attack_stat
                    / defense_stat
                )
                * move_data["power"]
                * (
                    2
                    + math.floor(
                        (
                            2
                            * attacker.level
                        ) / 5
                    )
                )
            ) / 50
        )
    )

    damage = math.floor(
        type_multiplier
        * stab
        * rand
        * base_damage
    )

    return max(
        1,
        damage
    )