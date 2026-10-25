from constants import *

SAVE_DEFAULT = {
    "player": {
        "player_name": "KOBE",
        "player_sprite": 0
    },
    "options": {
        "omniscient": True,
        "pkmn_animation": True,
        "fanart": False,
        "music_shuffle": True,
        "mute": False,
        "level": 100,
        "level_npc": 100,
    },
    "music": {},
    "teams": [],
    "selected_team": 0,
    "trainer_defeats": [],
    "endless_record": 0,
    "titles": 0,
    "gym_progress": {

        "Normal": [False, False, False],
        "Fire": [False, False, False],
        "Water": [False, False, False],
        "Grass": [False, False, False],
        "Electric": [False, False, False],
        "Ice": [False, False, False],
        "Fighting": [False, False, False],
        "Poison": [False, False, False],
        "Ground": [False, False, False],
        "Flying": [False, False, False],
        "Psychic": [False, False, False],
        "Bug": [False, False, False],
        "Rock": [False, False, False],
        "Ghost": [False, False, False],
        "Dragon": [False, False, False],
        "Dark": [False, False, False],
        "Steel": [False, False, False],
        "Fairy": [False, False, False],

    }
}


def load_save():
    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "save.json"
    )
    try:
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as infile:
            data = json.load(
                infile
            )
        save_data = copy.deepcopy(
            SAVE_DEFAULT
        )
        for key, value in data.items():
            save_data[key] = value
        save_save(
            save_data
        )
        return save_data
    except (
        FileNotFoundError,
        json.JSONDecodeError,
        KeyError
    ):
        save_data = copy.deepcopy(
            SAVE_DEFAULT
        )
        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as outfile:
            json.dump(
                save_data,
                outfile,
                indent=4
            )
        return save_data


def save_save(
    save_data
):
    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "save.json"
    )
    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as outfile:
        json.dump(
            save_data,
            outfile,
            indent=4
        )


def load_player():
    save_data = load_save()
    return save_data[
        "player"
    ]


def save_player():
    save_data = load_save()
    save_data[
        "player"
    ] = {
        "player_name":
            app.player_name,
        "player_sprite":
            app.player_sprite
    }
    save_save(
        save_data
    )

def load_options():
    save_data = load_save()
    return save_data[
        "options"
    ]


def save_options():
    save_data = load_save()
    save_data[
        "options"
    ] = {
        "omniscient":
            app.option_omniscient,
        "pkmn_animation":
            app.option_pkmn_animation,
        "fanart":
            app.option_fanart,
        "music_shuffle":
            app.option_music_shuffle,
        "mute":
            app.option_mute,
        "level":
            app.option_level,
        "level_npc":
            app.option_level_npc
    }
    save_save(
        save_data
    )


def load_teams():
    save_data = load_save()
    return {
        "teams":
            save_data[
                "teams"
            ]
    }


def save_teams(data):
    save_data = load_save()
    save_data[
        "teams"
    ] = data[
        "teams"
    ]
    save_save(
        save_data
    )


def get_selected_team_index():
    save_data = load_save()
    return save_data[
        "selected_team"
    ]

def set_selected_team_index(
    index
):
    save_data = load_save()
    save_data[
        "selected_team"
    ] = index
    save_save(
        save_data
    )


def get_trainer_defeats():
    save_data = load_save()
    return save_data[
        "trainer_defeats"
    ]

def save_trainer_defeat(
    trainer_name
):
    save_data = load_save()
    defeats = save_data[
        "trainer_defeats"
    ]
    if trainer_name not in defeats:
        defeats.append(
            trainer_name
        )
    save_save(
        save_data
    )

def load_music_data():
    save_data = load_save()
    music_data = save_data[
        "music"
    ]
    music_folder = os.path.join(
        TEXT_ROOT,
        "music"
    )
    current_music_files = set()
    for filename in os.listdir(
        music_folder
    ):
        if (
            filename.lower().endswith(
                ".ogg"
            )
        ):
            current_music_files.add(
                filename
            )
            if (
                filename
                not in music_data
            ):
                music_data[
                    filename
                ] = {
                    "menu": False,
                    "battle": False
                }
    for filename in list(
        music_data.keys()
    ):
        if (
            filename
            not in current_music_files
        ):
            del music_data[
                filename
            ]
    save_data[
        "music"
    ] = music_data
    save_save(
        save_data
    )
    return music_data

def save_music_data(
    music_data
):

    save_data = load_save()

    save_data[
        "music"
    ] = music_data

    save_save(
        save_data
    )

def get_num_trainer_defeats():

    return len(
        get_trainer_defeats()
    )

def reset_save():

    save_save(
        copy.deepcopy(
            SAVE_DEFAULT
        )
    )

def get_endless_record():

    save_data = load_save()

    return save_data[
        "endless_record"
    ]

def save_endless_record(
    wins
):

    save_data = load_save()

    save_data[
        "endless_record"
    ] = max(
        wins,
        save_data[
            "endless_record"
        ]
    )

    save_save(
        save_data
    )

def get_num_titles():

    save_data = load_save()

    return save_data[
        "titles"
    ]

def save_title():

    save_data = load_save()
    titles = get_num_titles() + 1

    save_data[
        "titles"
    ] = max(
        titles,
        save_data[
            "titles"
        ]
    )

    save_save(
        save_data
    )

def get_gym_progress():

    save_data = load_save()

    return save_data[
        "gym_progress"
    ]

def save_gym_progress(
    gym_progress
):

    save_data = load_save()

    save_data[
        "gym_progress"
    ] = gym_progress

    save_save(
        save_data
    )

