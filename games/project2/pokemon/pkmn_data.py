import json
import os


SPECIES_DATA = None

def load_species_data():

    global SPECIES_DATA

    if SPECIES_DATA is None:

        script_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        filepath = os.path.join(
            script_dir,
            "pkmn_stats.json"
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as infile:

            SPECIES_DATA = json.load(
                infile
            )["pokemon"]

    return SPECIES_DATA


def get_species(pokedex_number):

    species_data = load_species_data()

    for species in species_data:

        if species["no"] == pokedex_number:

            return species

    return None