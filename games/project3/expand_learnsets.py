import json
import os
import random
import shutil
from datetime import datetime


ROOT = os.path.abspath(
    os.path.dirname(
        __file__
    )
)

STATS_PATH = os.path.join(
    ROOT,
    "data",
    "pkmn_stats.json"
)

MOVES_PATH = os.path.join(
    ROOT,
    "data",
    "pkmn_moves.json"
)

LEARNSET_SIZE = 10
RANDOM_SEED = 20261017


def load_json(
    filepath
):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as infile:

        return json.load(
            infile
        )


def save_json(
    filepath,
    data
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            data,
            outfile,
            indent=4
        )


def make_backup(
    filepath
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = (
        filepath
        + "."
        + timestamp
        + ".bak"
    )

    shutil.copy2(
        filepath,
        backup_path
    )

    return backup_path


def unique_valid_moves(
    move_names,
    valid_move_names
):

    result = []
    seen = set()

    for move_name in move_names:

        if (
            move_name in valid_move_names
            and
            move_name not in seen
        ):

            result.append(
                move_name
            )

            seen.add(
                move_name
            )

    return result


def build_learnset(
    species,
    move_data,
    randomizer
):

    valid_move_names = set(
        move_data.keys()
    )

    current_moves = unique_valid_moves(
        species.get(
            "moves",
            []
        ),
        valid_move_names
    )

    species_types = set(
        species.get(
            "types",
            []
        )
    )

    same_type_moves = []
    other_moves = []

    for move_name, data in (
        move_data.items()
    ):

        if move_name in current_moves:
            continue

        if (
            data.get(
                "type"
            )
            in species_types
        ):

            same_type_moves.append(
                move_name
            )

        else:

            other_moves.append(
                move_name
            )

    randomizer.shuffle(
        same_type_moves
    )

    randomizer.shuffle(
        other_moves
    )

    candidates = (
        same_type_moves
        + other_moves
    )

    learnset = list(
        current_moves
    )

    for move_name in candidates:

        if (
            len(
                learnset
            )
            >= LEARNSET_SIZE
        ):

            break

        learnset.append(
            move_name
        )

    if (
        len(
            learnset
        )
        < LEARNSET_SIZE
    ):

        raise ValueError(
            (
                f"Could only assign "
                f"{len(learnset)} unique moves "
                f"to {species.get('name', 'UNKNOWN')}"
            )
        )

    return learnset[
        :LEARNSET_SIZE
    ]


def main():

    stats_data = load_json(
        STATS_PATH
    )

    moves_json = load_json(
        MOVES_PATH
    )

    move_data = moves_json[
        "moves"
    ]

    if (
        len(
            move_data
        )
        < LEARNSET_SIZE
    ):

        raise ValueError(
            (
                "pkmn_moves.json must contain "
                f"at least {LEARNSET_SIZE} moves"
            )
        )

    pokemon_data = stats_data[
        "pokemon"
    ]

    randomizer = random.Random(
        RANDOM_SEED
    )

    backup_path = make_backup(
        STATS_PATH
    )

    for species in pokemon_data:

        species[
            "moves"
        ] = build_learnset(
            species,
            move_data,
            randomizer
        )

    save_json(
        STATS_PATH,
        stats_data
    )

    print(
        (
            f"Revised {len(pokemon_data)} "
            f"Pokemon learnsets."
        )
    )

    print(
        (
            f"Every learnset now contains "
            f"{LEARNSET_SIZE} unique moves."
        )
    )

    print(
        f"Backup created: {backup_path}"
    )


if __name__ == "__main__":

    main()