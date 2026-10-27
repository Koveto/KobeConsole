from constants import *
from state import *

def handle_event(event):
    if app.state == LAUNCHER_MENU:
        handle_event_LAUNCHER_MENU(event)
    elif app.state == LAN_HOST_JOIN:
        handle_event_LAN_HOST_JOIN(event)
    elif app.state == LAN_HOST:
        handle_event_LAN_HOST(event)
    elif app.state == LAN_JOIN:
        handle_event_LAN_JOIN(event)
    elif app.state == TEAM_PREVIEW:
        handle_event_TEAM_PREVIEW(event)
    elif app.state == PKMN_VIEW:
        handle_event_PKMN_VIEW(event)
    elif app.state == SPECIES_VIEW:
        handle_event_SPECIES_VIEW(event)
    elif app.state == BATTLE_START:
        handle_event_BATTLE_START(event)
    elif app.state == TEAM_SELECT:
        handle_event_TEAM_SELECT(event)
    elif app.state == OPTIONS:
        handle_event_OPTIONS(event)
    elif app.state == KEYBOARD:
        handle_event_KEYBOARD(event)
    elif app.state == OPTIONS_MUSIC:
        handle_event_OPTIONS_MUSIC(event)
    elif app.state == SINGLE_MENU:
        handle_event_SINGLE_MENU(event)
    elif app.state == SINGLE_MENU_TRAINER:
        handle_event_SINGLE_MENU_TRAINER(event)
    elif app.state == BATTLE_END:
        handle_event_BATTLE_END(event)
    elif app.state == SINGLE_BRACKET:
        handle_event_SINGLE_BRACKET(event)
    elif app.state == SINGLE_DEFEND_GYM:
        handle_event_SINGLE_DEFEND_GYM(event)
    elif app.state == DAMAGE_CALCULATOR:
        handle_event_DAMAGE_CALCULATOR(event)
    elif app.state == PKMN_EDIT:
        handle_event_PKMN_EDIT(event)

def cycle_pkmn_edit_info_mode():

    if (
        app.PKMN_EDIT_info_mode
        == "ACTUAL"
    ):
        app.PKMN_EDIT_info_mode = (
            "BASE"
        )

    elif (
        app.PKMN_EDIT_info_mode
        == "BASE"
    ):
        app.PKMN_EDIT_info_mode = (
            "EVS"
        )

    else:
        app.PKMN_EDIT_info_mode = (
            "ACTUAL"
        )

    app.PKMN_EDIT_error = None

def adjust_pkmn_edit_level(
    direction
):

    pokemon = (
        app.PKMN_EDIT_pokemon
    )

    if pokemon is None:
        return

    new_level = max(
        Pokemon.MIN_LEVEL,
        min(
            Pokemon.MAX_LEVEL,
            pokemon.level + direction
        )
    )

    if new_level == pokemon.level:
        return

    pokemon.set_level(
        new_level
    )

    save_pkmn_edit_pokemon()

def change_pkmn_edit_nature(
    direction
):

    pokemon = (
        app.PKMN_EDIT_pokemon
    )

    if pokemon is None:
        return

    natures = list(
        NATURES.values()
    )

    nature_index = next(
        index
        for index, nature
        in enumerate(
            natures
        )
        if nature.name
        == pokemon.nature.name
    )

    nature_index = (
        nature_index + direction
    ) % len(
        natures
    )

    pokemon.nature = (
        natures[
            nature_index
        ]
    )

    pokemon.set_level(
        pokemon.level
    )

    save_pkmn_edit_pokemon()

def adjust_pkmn_edit_ev(
    direction
):

    pokemon = (
        app.PKMN_EDIT_pokemon
    )

    if pokemon is None:
        return

    evs = get_pkmn_edit_evs(
        pokemon
    )

    ev_index = (
        app.PKMN_EDIT_ev_index
    )

    if direction < 0:

        new_value = max(
            0,
            evs[ev_index] - 4
        )

        if (
            new_value
            == evs[ev_index]
        ):

            app.PKMN_EDIT_error = (
                "STAT EV MIN 0"
            )

            return

        evs[ev_index] = (
            new_value
        )

        app.PKMN_EDIT_error = None

        set_pkmn_edit_evs(
            pokemon,
            evs
        )

        return

    if direction > 0:

        current_total = sum(
            evs
        )

        available_evs = (
            508 - current_total
        )

        increase = min(
            4,
            252 - evs[ev_index],
            available_evs
        )

        if increase <= 0:

            if (
                evs[ev_index]
                >= 252
            ):

                app.PKMN_EDIT_error = (
                    "STAT EV MAX 252"
                )

            else:

                app.PKMN_EDIT_error = (
                    "TOTAL EV MAX 508"
                )

            return

        evs[ev_index] += (
            increase
        )

        app.PKMN_EDIT_error = None

        set_pkmn_edit_evs(
            pokemon,
            evs
        )


def get_pkmn_edit_evs(
    pokemon
):

    return [
        pokemon.hp_ev,
        pokemon.attack_ev,
        pokemon.defense_ev,
        pokemon.special_attack_ev,
        pokemon.special_defense_ev,
        pokemon.speed_ev
    ]


def set_pkmn_edit_evs(
    pokemon,
    evs
):

    pokemon.hp_ev = evs[0]
    pokemon.attack_ev = evs[1]
    pokemon.defense_ev = evs[2]
    pokemon.special_attack_ev = evs[3]
    pokemon.special_defense_ev = evs[4]
    pokemon.speed_ev = evs[5]

    pokemon.set_level(
        pokemon.level
    )

    save_pkmn_edit_pokemon()

def save_pkmn_edit_pokemon():

    pokemon = (
        app.PKMN_EDIT_pokemon
    )

    if pokemon is None:

        return

    if (
        app.PKMN_EDIT_source
        == "TEAMBUILDER"
    ):

        team_index = (
            app.PKMN_EDIT_team_index
        )

        pokemon_index = (
            app.PKMN_EDIT_pokemon_index
        )

        save_data = load_save()

        if (
            team_index is not None
            and
            pokemon_index is not None
            and
            0
            <= team_index
            < len(
                save_data["teams"]
            )
            and
            0
            <= pokemon_index
            < len(
                save_data["teams"][
                    team_index
                ]["pokemon"]
            )
        ):

            save_data["teams"][
                team_index
            ]["pokemon"][
                pokemon_index
            ] = (
                pokemon.to_dict()
            )

            save_save(
                save_data
            )

    elif (
        app.PKMN_EDIT_source
        == "DAMAGE_CALCULATOR_ATTACKER"
    ):

        app.DAMAGE_CALCULATOR_attacker = (
            Pokemon.from_pokemon(
                pokemon
            )
        )

        save_damage_calculator(
            app.DAMAGE_CALCULATOR_attacker,
            app.DAMAGE_CALCULATOR_defender
        )

    elif (
        app.PKMN_EDIT_source
        == "DAMAGE_CALCULATOR_DEFENDER"
    ):

        app.DAMAGE_CALCULATOR_defender = (
            Pokemon.from_pokemon(
                pokemon
            )
        )

        save_damage_calculator(
            app.DAMAGE_CALCULATOR_attacker,
            app.DAMAGE_CALCULATOR_defender
        )

def handle_team_select_pokemon_navigation(
    event
):

    team_size = len(
        app.TEAM_SELECT_preview_team
    )

    if team_size == 0:
        return

    max_index = (
        team_size - 1
    )

    if is_left(event):

        app.TEAM_SELECT_pokemon_index = max(
            0,
            app.TEAM_SELECT_pokemon_index - 1
        )

    elif is_right(event):

        app.TEAM_SELECT_pokemon_index = min(
            max_index,
            app.TEAM_SELECT_pokemon_index + 1
        )

    elif is_up(event):

        app.TEAM_SELECT_pokemon_index = max(
            0,
            app.TEAM_SELECT_pokemon_index - 2
        )

    elif is_down(event):

        new_index = (
            app.TEAM_SELECT_pokemon_index
            + 2
        )

        if new_index <= max_index:

            app.TEAM_SELECT_pokemon_index = (
                new_index
            )

        elif (
            app.TEAM_SELECT_pokemon_index
            % 2
            == 0
            and
            max_index % 2 == 1
        ):

            app.TEAM_SELECT_pokemon_index = (
                max_index
            )

def handle_event_PKMN_EDIT(
    event
):

    pokemon = (
        app.PKMN_EDIT_pokemon
    )

    if pokemon is None:

        if is_cancel(event):

            change_state(
                app.PKMN_EDIT_return_state
            )

        return

    if (
        app.PKMN_EDIT_mode
        == "MOVES"
    ):

        if (
            app.PKMN_EDIT_selecting_move
        ):

            learnset_size = len(
                pokemon.learnset
            )

            if learnset_size == 0:

                app.PKMN_EDIT_selecting_move = (
                    False
                )

                return

            if is_up(event):

                app.PKMN_EDIT_learnset_index = max(
                    0,
                    app.PKMN_EDIT_learnset_index - 1
                )
                app.PKMN_EDIT_error = None

            elif is_down(event):

                app.PKMN_EDIT_learnset_index = min(
                    learnset_size - 1,
                    app.PKMN_EDIT_learnset_index + 1
                )
                app.PKMN_EDIT_error = None

            elif is_confirm(event):

                selected_move = (
                    pokemon.learnset[
                        app.PKMN_EDIT_learnset_index
                    ]
                )

                move_is_duplicate = any(

                    index
                    != app.PKMN_EDIT_move_index

                    and

                    known_move.name
                    == selected_move.name

                    for index, known_move
                    in enumerate(
                        pokemon.moves
                    )

                )

                if move_is_duplicate:

                    app.PKMN_EDIT_error = (
                        "MOVE ALREADY KNOWN"
                    )

                    return

                pokemon.set_move(
                    app.PKMN_EDIT_move_index,
                    selected_move
                )

                save_pkmn_edit_pokemon()

                app.PKMN_EDIT_error = None

                app.PKMN_EDIT_selecting_move = (
                    False
                )

            elif is_cancel(event):

                app.PKMN_EDIT_selecting_move = (
                    False
                )
                app.PKMN_EDIT_error = None

            return

        if is_up(event):

            app.PKMN_EDIT_move_index = max(
                0,
                app.PKMN_EDIT_move_index - 1
            )

        elif is_down(event):

            app.PKMN_EDIT_move_index = min(
                4,
                app.PKMN_EDIT_move_index + 1
            )

        elif is_confirm(event):

            if (
                app.PKMN_EDIT_move_index
                < 4
            ):

                if len(
                    pokemon.learnset
                ) == 0:

                    return

                current_move = (
                    pokemon.moves[
                        app.PKMN_EDIT_move_index
                    ]
                )

                app.PKMN_EDIT_learnset_index = 0

                for index, move in enumerate(
                    pokemon.learnset
                ):

                    if (
                        move.name
                        == current_move.name
                    ):

                        app.PKMN_EDIT_learnset_index = (
                            index
                        )

                        break

                app.PKMN_EDIT_selecting_move = (
                    True
                )

            else:

                app.PKMN_EDIT_mode = (
                    "MAIN"
                )

                app.PKMN_EDIT_index = 3

        elif is_cancel(event):

            app.PKMN_EDIT_mode = (
                "MAIN"
            )

            app.PKMN_EDIT_index = 3

        return

    if (
        app.PKMN_EDIT_mode
        == "STATS"
    ):

        if is_cx(event):

            cycle_pkmn_edit_info_mode()

            return

        if is_up(event):

            app.PKMN_EDIT_stats_index = max(
                0,
                app.PKMN_EDIT_stats_index - 1
            )

            app.PKMN_EDIT_error = None

        elif is_down(event):

            app.PKMN_EDIT_stats_index = min(
                9,
                app.PKMN_EDIT_stats_index + 1
            )

            app.PKMN_EDIT_error = None

        elif is_left(event):

            if (
                app.PKMN_EDIT_stats_index
                == 0
            ):

                cycle_pkmn_edit_info_mode()

            elif (
                app.PKMN_EDIT_stats_index
                == 1
            ):

                change_pkmn_edit_nature(
                    -1
                )

            elif (
                app.PKMN_EDIT_stats_index
                == 2
            ):

                adjust_pkmn_edit_level(
                    -1
                )

            elif (
                3
                <= app.PKMN_EDIT_stats_index
                <= 8
            ):

                app.PKMN_EDIT_ev_index = (
                    app.PKMN_EDIT_stats_index
                    - 3
                )

                adjust_pkmn_edit_ev(
                    -1
                )

        elif is_right(event):

            if (
                app.PKMN_EDIT_stats_index
                == 0
            ):

                cycle_pkmn_edit_info_mode()

            elif (
                app.PKMN_EDIT_stats_index
                == 1
            ):

                change_pkmn_edit_nature(
                    1
                )

            elif (
                app.PKMN_EDIT_stats_index
                == 2
            ):

                adjust_pkmn_edit_level(
                    1
                )

            elif (
                3
                <= app.PKMN_EDIT_stats_index
                <= 8
            ):

                app.PKMN_EDIT_ev_index = (
                    app.PKMN_EDIT_stats_index
                    - 3
                )

                adjust_pkmn_edit_ev(
                    1
                )

        elif is_confirm(event):

            if (
                app.PKMN_EDIT_stats_index
                == 0
            ):

                cycle_pkmn_edit_info_mode()

            elif (
                app.PKMN_EDIT_stats_index
                == 9
            ):

                app.PKMN_EDIT_mode = (
                    "MAIN"
                )

                app.PKMN_EDIT_index = 4
                app.PKMN_EDIT_error = None

        elif is_cancel(event):

            app.PKMN_EDIT_mode = (
                "MAIN"
            )

            app.PKMN_EDIT_index = 4
            app.PKMN_EDIT_error = None

        return

    if is_cx(event):

        cycle_pkmn_edit_info_mode()

        return

    if is_up(event):

        if (
            app.PKMN_EDIT_index
            in (
                3,
                4
            )
        ):

            app.PKMN_EDIT_index = 2

        else:

            app.PKMN_EDIT_index = max(
                0,
                app.PKMN_EDIT_index - 1
            )

    elif is_down(event):

        if (
            app.PKMN_EDIT_index
            < 2
        ):

            app.PKMN_EDIT_index += 1

        elif (
            app.PKMN_EDIT_index
            == 2
        ):

            app.PKMN_EDIT_index = 3

    elif is_left(event):

        if (
            app.PKMN_EDIT_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_edit_pokemon()

        elif (
            app.PKMN_EDIT_index
            == 4
        ):

            app.PKMN_EDIT_index = 3

    elif is_right(event):

        if (
            app.PKMN_EDIT_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_edit_pokemon()

        elif (
            app.PKMN_EDIT_index
            == 3
        ):

            app.PKMN_EDIT_index = 4

    elif is_confirm(event):

        if (
            app.PKMN_EDIT_index
            == 0
        ):

            # SPECIES_EDIT will open here.
            pass

        elif (
            app.PKMN_EDIT_index
            == 1
        ):

            app.KEYBOARD_mode = (
                "POKEMON_NICKNAME"
            )

            app.KEYBOARD_return_state = (
                PKMN_EDIT
            )

            app.KEYBOARD_team_index = None

            app.KEYBOARD_pokemon = (
                pokemon
            )

            change_state(
                KEYBOARD
            )

        elif (
            app.PKMN_EDIT_index
            == 2
        ):

            pokemon.set_shiny(
                not pokemon.is_shiny
            )

            save_pkmn_edit_pokemon()

        elif (
            app.PKMN_EDIT_index
            == 3
        ):

            app.PKMN_EDIT_mode = (
                "MOVES"
            )

            app.PKMN_EDIT_move_index = 0
            app.PKMN_EDIT_learnset_index = 0
            app.PKMN_EDIT_selecting_move = False

        elif (
            app.PKMN_EDIT_index
            == 4
        ):

            app.PKMN_EDIT_mode = (
                "STATS"
            )

            app.PKMN_EDIT_stats_index = 0
            app.PKMN_EDIT_error = None

    elif is_cancel(event):

        save_pkmn_edit_pokemon()

        change_state(
            app.PKMN_EDIT_return_state
        )

def generate_teambuilder_team():

    load_species()

    candidates = []

    for species in SPECIES.values():

        bst = sum(
            species.stats.values()
        )

        if bst > 480:

            candidates.append(
                species.no
            )

    if len(candidates) == 0:

        raise ValueError(
            "No species found with BST over 480"
        )

    return [

        Pokemon.from_species_number(
            random.choice(
                candidates
            )
        )

        for _ in range(6)

    ]

def complete_keyboard_entry():

    text = (
        app.KEYBOARD_text.strip()
    )

    if len(text) == 0:

        return

    if (
        app.KEYBOARD_mode
        == "PLAYER_NAME"
    ):

        app.player_name = text

        save_player()

        change_state(
            OPTIONS
        )

        return

    if (
        app.KEYBOARD_mode
        == "CREATE_TEAM"
    ):

        team = (
            generate_teambuilder_team()
        )

        save_data = load_save()

        save_data["teams"].insert(
            0,
            {
                "name": text,
                "pokemon": [
                    pokemon.to_dict()
                    for pokemon in team
                ]
            }
        )

        save_save(
            save_data
        )

        app.TEAM_SELECT_restore_index = 1
        app.TEAM_SELECT_restore_scroll = 0
        app.TEAM_SELECT_submenu = False

        change_state(
            TEAM_SELECT
        )

        return

    if (
        app.KEYBOARD_mode
        == "RENAME_TEAM"
    ):

        team_index = (
            app.KEYBOARD_team_index
        )

        save_data = load_save()

        if (
            team_index is not None
            and
            0
            <= team_index
            < len(
                save_data["teams"]
            )
        ):

            save_data["teams"][
                team_index
            ]["name"] = text

            save_save(
                save_data
            )

        app.TEAM_SELECT_restore_index = (
            team_index + 1
            if team_index is not None
            else 0
        )

        app.TEAM_SELECT_restore_scroll = (
            app.TEAM_SELECT_scroll
        )

        app.TEAM_SELECT_submenu = False

        change_state(
            TEAM_SELECT
        )

        return

    if (
        app.KEYBOARD_mode
        == "POKEMON_NICKNAME"
    ):

        pokemon = (
            app.KEYBOARD_pokemon
        )

        if pokemon is None:

            return

        pokemon.nickname = text

        app.PKMN_EDIT_pokemon = (
            pokemon
        )

        app.KEYBOARD_pokemon = None

        save_pkmn_edit_pokemon()

        change_state(
            PKMN_EDIT
        )

        return

def handle_event_DAMAGE_CALCULATOR(
    event
):

    if is_left(event):

        app.DAMAGE_CALCULATOR_column = max(
            0,
            app.DAMAGE_CALCULATOR_column - 1
        )

        app.DAMAGE_CALCULATOR_index = 0

    elif is_right(event):

        app.DAMAGE_CALCULATOR_column = min(
            2,
            app.DAMAGE_CALCULATOR_column + 1
        )

        app.DAMAGE_CALCULATOR_index = 0

    elif is_up(event):

        app.DAMAGE_CALCULATOR_index = max(
            0,
            app.DAMAGE_CALCULATOR_index - 1
        )

    elif is_down(event):

        if (
            app.DAMAGE_CALCULATOR_column
            == 1
        ):

            app.DAMAGE_CALCULATOR_index = min(
                3,
                app.DAMAGE_CALCULATOR_index + 1
            )

        else:

            app.DAMAGE_CALCULATOR_index = min(
                1,
                app.DAMAGE_CALCULATOR_index + 1
            )

    elif is_cancel(event):

        change_state(
            LAUNCHER_MENU
        )

    elif is_confirm(event):

        if (
            app.DAMAGE_CALCULATOR_column
            == 0
            and
            app.DAMAGE_CALCULATOR_index
            == 0
        ):

            app.TEAM_SELECT_mode = (
                "IMPORT"
            )

            app.TEAM_SELECT_import_target = (
                "ATTACKER"
            )

            app.TEAM_SELECT_return_state = (
                DAMAGE_CALCULATOR
            )

            change_state(
                TEAM_SELECT
            )

        elif (
            app.DAMAGE_CALCULATOR_column
            == 0
            and
            app.DAMAGE_CALCULATOR_index
            == 1
        ):

            if (
                app.DAMAGE_CALCULATOR_attacker
                is None
            ):

                return

            app.PKMN_EDIT_pokemon = (
                Pokemon.from_pokemon(
                    app.DAMAGE_CALCULATOR_attacker
                )
            )

            app.PKMN_EDIT_source = (
                "DAMAGE_CALCULATOR_ATTACKER"
            )

            app.PKMN_EDIT_team_index = None
            app.PKMN_EDIT_pokemon_index = None

            app.PKMN_EDIT_return_state = (
                DAMAGE_CALCULATOR
            )

            change_state(
                PKMN_EDIT
            )

        elif (
            app.DAMAGE_CALCULATOR_column
            == 2
            and
            app.DAMAGE_CALCULATOR_index
            == 0
        ):

            app.TEAM_SELECT_mode = (
                "IMPORT"
            )

            app.TEAM_SELECT_import_target = (
                "DEFENDER"
            )

            app.TEAM_SELECT_return_state = (
                DAMAGE_CALCULATOR
            )

            change_state(
                TEAM_SELECT
            )

        elif (
            app.DAMAGE_CALCULATOR_column
            == 2
            and
            app.DAMAGE_CALCULATOR_index
            == 1
        ):

            if (
                app.DAMAGE_CALCULATOR_defender
                is None
            ):

                return

            app.PKMN_EDIT_pokemon = (
                Pokemon.from_pokemon(
                    app.DAMAGE_CALCULATOR_defender
                )
            )

            app.PKMN_EDIT_source = (
                "DAMAGE_CALCULATOR_DEFENDER"
            )

            app.PKMN_EDIT_team_index = None
            app.PKMN_EDIT_pokemon_index = None

            app.PKMN_EDIT_return_state = (
                DAMAGE_CALCULATOR
            )

            change_state(
                PKMN_EDIT
            )



def ensure_gym_progress():

    save_data = load_save()

    gym_progress = save_data[
        "gym_progress"
    ]

    gyms_data = load_gyms()

    changed = False

    for gym in gyms_data[
        "gyms"
    ]:

        gym_type = gym["type"]

        if gym_type not in gym_progress:

            gym_progress[
                gym_type
            ] = [
                False,
                False,
                False
            ]

            changed = True

    if changed:

        save_save(
            save_data
        )

    return gym_progress

def generate_type_team(
    type_name
):

    load_species()

    candidates = []

    for species in (
        SPECIES.values()
    ):

        if (
            type_name
            in
            species.types
        ):

            candidates.append(
                species.no
            )

    random.shuffle(
        candidates
    )

    return [

        Pokemon.from_species_number(
            species_no
        )

        for species_no
        in
        candidates[:6]

    ]


def team_matches_type(
    team,
    required_type
):

    for pokemon in team:

        if (
            required_type
            not in
            pokemon.species.types
        ):

            return False

    return True

def get_num_completed_gyms():

    gym_progress = (
        ensure_gym_progress()
    )

    count = 0

    for progress in (
        gym_progress.values()
    ):

        if all(progress):

            count += 1

    return count

def handle_event_SINGLE_DEFEND_GYM(
    event
):

    if is_up(event):

        app.SINGLE_DEFEND_GYM_index = max(
            0,
            app.SINGLE_DEFEND_GYM_index - 1
        )

        if (
            app.SINGLE_DEFEND_GYM_index
            <
            app.SINGLE_DEFEND_GYM_scroll
        ):
            app.SINGLE_DEFEND_GYM_scroll -= 1

    elif is_down(event):

        app.SINGLE_DEFEND_GYM_index = min(
            len(app.gyms_data) - 1,
            app.SINGLE_DEFEND_GYM_index + 1
        )

        if (
            app.SINGLE_DEFEND_GYM_index
            >=
            app.SINGLE_DEFEND_GYM_scroll + 2
        ):
            app.SINGLE_DEFEND_GYM_scroll += 1

    elif is_left(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        current = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        app.SINGLE_DEFEND_GYM_trainer_indices[
            gym["type"]
        ] = max(
            0,
            current - 1
        )

    elif is_right(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        current = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        app.SINGLE_DEFEND_GYM_trainer_indices[
            gym["type"]
        ] = min(
            2,
            current + 1
        )

    elif is_confirm(event):

        gym = (
            app.gyms_data[
                app.SINGLE_DEFEND_GYM_index
            ]
        )

        trainer_index = (
            app.SINGLE_DEFEND_GYM_trainer_indices.get(
                gym["type"],
                0
            )
        )

        trainer_name = (
            gym["challengers"][
                trainer_index
            ]
        )

        trainer = next(
            t
            for t
            in app.trainers_data
            if t["name"] == trainer_name
        )

        app.SINGLE_DEFEND_GYM_selected_gym = gym

        app.SINGLE_DEFEND_GYM_selected_type = (
            gym["type"]
        )

        app.SINGLE_DEFEND_GYM_selected_trainer = (
            trainer_name
        )

        app.selected_SINGLE_DEFEND_GYM_trainer_index = (
            trainer_index
        )

        app.selected_trainer_data = (
            trainer
        )

        app.TEAM_SELECT_return_state = (
            SINGLE_DEFEND_GYM
        )

        app.allow_team_change = True

        app.allow_lead_change = True

        app.game_mode = (
            "DEFEND_GYM"
        )

        change_state(
            TEAM_SELECT
        )

    elif is_cancel(event):

        change_state(
            SINGLE_MENU
        )

def start_tournament():
    app.tournament_semifinals = []
    app.tournament_finals = []
    app.tournament_active = True
    app.tournament_round = 0
    selected_trainers = random.sample(
        app.trainers_data,
        7
    )
    app.tournament_quarterfinals = [
        "PLAYER",
        selected_trainers[0],
        selected_trainers[1],
        selected_trainers[2],
        selected_trainers[3],
        selected_trainers[4],
        selected_trainers[5],
        selected_trainers[6]
    ]
    app.tournament_current_trainer = (
        app.tournament_quarterfinals[1]
    )

def handle_event_SINGLE_BRACKET(
    event
):

    if is_confirm(event):

        if (
            app.tournament_round
            == 0
        ):

            app.TEAM_SELECT_return_state = (
                SINGLE_BRACKET
            )

            app.allow_team_change = True

            app.allow_lead_change = True

            change_state(
                TEAM_SELECT
            )

        else:

            if (
                app.tournament_round
                == 1
            ):

                opponent = (
                    app.tournament_semifinals[
                        1
                    ]
                )

            else:

                opponent = (
                    app.tournament_finals[
                        1
                    ]
                )

            app.tournament_current_trainer = (
                opponent
            )

            app.selected_trainer_data = (
                opponent
            )

            app.opponent_team = [

                Pokemon.from_dict(
                    pokemon_data
                )

                for pokemon_data
                in
                opponent["team"]

            ]

            app.allow_team_change = False

            app.allow_lead_change = True

            change_state(
                TEAM_PREVIEW
            )

def start_next_endless_battle():
    trainer_index = random.randint(
        0,
        len(app.trainers_data) - 1
    )
    app.endless_trainer_index = (
        trainer_index
    )
    trainer = (
        app.trainers_data[
            trainer_index
        ]
    )
    app.selected_trainer_data = (
        trainer
    )
    app.opponent_team = [
        Pokemon.from_dict(
            pokemon_data
        )
        for pokemon_data in
        trainer["team"]
    ]
    for pokemon in app.opponent_team:
        pokemon.set_level(
            app.option_level_npc
        )

def handle_event_BATTLE_END(event):
    pass

def handle_event_SINGLE_MENU_TRAINER(event):
    if is_up(event):
        app.SINGLE_MENU_TRAINER_index = max(0, app.SINGLE_MENU_TRAINER_index - 1)
    elif is_down(event):
        app.SINGLE_MENU_TRAINER_index = min(2, app.SINGLE_MENU_TRAINER_index + 1)
    elif is_cancel(event):
        change_state(SINGLE_MENU)
    elif is_confirm(event):
        if (
            app.SINGLE_MENU_TRAINER_index
            == 0
        ):
            app.single_battle_mode = (
                "RANDOM_TEAM"
            )
        elif (
            app.SINGLE_MENU_TRAINER_index
            == 1
        ):
            app.single_battle_mode = (
                "MY_TEAM"
            )
        else:
            app.single_battle_mode = (
                "TRAINER"
            )
        app.selected_trainer_data = (
            app.trainers_data[
                app.SINGLE_MENU_TRAINER_selected_trainer
            ]
        )
        app.TEAM_SELECT_return_state = (
            SINGLE_MENU_TRAINER
        )

        app.allow_team_change = True
        app.allow_lead_change = True

        if (
            app.single_battle_mode
            == "MY_TEAM"
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is None
        ):
            return

        app.restore_single_menu_trainer = True
        change_state(
            TEAM_SELECT
        )
    elif is_left(event):
        if (
            app.SINGLE_MENU_TRAINER_index == 1
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is not None
        ):
            app.SINGLE_MENU_TRAINER_selected_team = max(
                0,
                app.SINGLE_MENU_TRAINER_selected_team - 1
            )
            selected_team = (
                app.teams_data[
                    app.SINGLE_MENU_TRAINER_selected_team
                ]
            )

            app.SINGLE_MENU_TRAINER_my_team_preview = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                selected_team["pokemon"]
            ]
        elif app.SINGLE_MENU_TRAINER_index == 2:
            app.SINGLE_MENU_TRAINER_selected_trainer = max(
                0,
                app.SINGLE_MENU_TRAINER_selected_trainer - 1
            )
            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )
            app.SINGLE_MENU_TRAINER_preview_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                trainer["team"]
            ]
    elif is_right(event):
        if (
            app.SINGLE_MENU_TRAINER_index == 1
            and
            app.SINGLE_MENU_TRAINER_selected_team
            is not None
        ):
            app.SINGLE_MENU_TRAINER_selected_team = min(
                len(app.teams_data) - 1,
                app.SINGLE_MENU_TRAINER_selected_team + 1
            )
            selected_team = (
                app.teams_data[
                    app.SINGLE_MENU_TRAINER_selected_team
                ]
            )

            app.SINGLE_MENU_TRAINER_my_team_preview = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data
                in
                selected_team["pokemon"]
            ]
        elif app.SINGLE_MENU_TRAINER_index == 2:
            app.SINGLE_MENU_TRAINER_selected_trainer = min(
                len(app.trainers_data) - 1,
                app.SINGLE_MENU_TRAINER_selected_trainer + 1
            )
            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )
            app.SINGLE_MENU_TRAINER_preview_team = [

                Pokemon.from_dict(
                    pokemon_data
                )

                for pokemon_data
                in
                trainer["team"]

            ]
    elif is_cvxy(event):

        if (
            app.option_omniscient
            and
            app.SINGLE_MENU_TRAINER_index == 2
        ):

            trainer = (
                app.trainers_data[
                    app.SINGLE_MENU_TRAINER_selected_trainer
                ]
            )

            save_data = load_save()

            save_data["teams"].insert(
                0,
                {
                    "name": trainer["name"],
                    "pokemon": trainer["team"]
                }
            )

            save_save(
                save_data
            )

def generate_test_teams():

    load_species()

    save_data = load_save()

    teams = []

    species_list = list(
        SPECIES.keys()
    )

    for team_index in range(10):

        team = {
            "name":
                f"Test Team {team_index + 1}",
            "pokemon": []
        }

        for _ in range(6):

            pokemon = (
                Pokemon.from_species_number(
                    random.choice(
                        species_list
                    )
                )
            )

            team["pokemon"].append(
                pokemon.to_dict()
            )

        teams.append(
            team
        )

    save_data[
        "teams"
    ] = teams

    save_save(
        save_data
    )


def handle_event_SINGLE_MENU(event):
    if is_up(event):
        app.SINGLE_MENU_index = max(0, app.SINGLE_MENU_index - 1)
    elif is_down(event):
        app.SINGLE_MENU_index = min(len(app.SINGLE_MENU_options) - 1, app.SINGLE_MENU_index + 1)
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)
    elif is_confirm(event):
        if app.SINGLE_MENU_index == 0:
            change_state(
                SINGLE_MENU_TRAINER
            )
        elif app.SINGLE_MENU_index == 1:
            app.game_mode = (
                "ENDLESS"
            )
            if app.endless_active:
                start_next_endless_battle()
                change_state(
                    TEAM_PREVIEW
                )
            else:
                app.endless_active = (
                    True
                )
                app.endless_wins = 0
                app.TEAM_SELECT_return_state = (
                    SINGLE_MENU
                )
                app.allow_team_change = True
                app.allow_lead_change = True
                change_state(
                    TEAM_SELECT
                )
        elif app.SINGLE_MENU_index == 2:

            gyms_data = load_gyms()

            app.gyms_data = (
                gyms_data["gyms"]
            )

            change_state(
                SINGLE_DEFEND_GYM
            )
        elif app.SINGLE_MENU_index == 3:
            app.game_mode = "TOURNAMENT"
            start_tournament()
            change_state(SINGLE_BRACKET)
    elif is_vy(event):
        reset_save()
        generate_test_teams()
        change_state(
            SINGLE_MENU
        )

def handle_event_OPTIONS_MUSIC(event):
    filenames = sorted(
        app.music_data.keys()
    )
    if is_up(event):
        app.OPTIONS_MUSIC_index = max(
            0,
            app.OPTIONS_MUSIC_index - 1
        )
        if (
            app.OPTIONS_MUSIC_index
            <
            app.OPTIONS_MUSIC_scroll
        ):
            app.OPTIONS_MUSIC_scroll -= 1
    elif is_down(event):
        app.OPTIONS_MUSIC_index = min(
            len(filenames) - 1,
            app.OPTIONS_MUSIC_index + 1
        )
        if (
            app.OPTIONS_MUSIC_index
            >=
            app.OPTIONS_MUSIC_scroll + 8
        ):
            app.OPTIONS_MUSIC_scroll += 1
    elif is_confirm(event):
        filename = filenames[app.OPTIONS_MUSIC_index]
        if app.current_music == filename:
            stop_music()
        else:
            play_music(filename)
    elif is_cancel(event):
        change_state(OPTIONS)
    elif is_cx(event):
        filename = filenames[app.OPTIONS_MUSIC_index]
        app.music_data[
            filename
        ]["menu"] = (
            not
            app.music_data[
                filename
            ]["menu"]
        )
        save_music_data(app.music_data)
    elif is_vy(event):
        filename = filenames[
            app.OPTIONS_MUSIC_index
        ]
        app.music_data[
            filename
        ]["battle"] = (
            not
            app.music_data[
                filename
            ]["battle"]
        )
        save_music_data(app.music_data)

def handle_event_KEYBOARD(event):
    if not using_controller():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
            
                if app.KEYBOARD_mode == "POKEMON_NICKNAME":
                    app.KEYBOARD_pokemon = None
                if (
                    app.KEYBOARD_return_state is not None
                ):
                    change_state(app.KEYBOARD_return_state)
            elif (
                event.unicode.isalnum()
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += (
                    event.unicode.upper()
                )
            elif (
                event.key == pygame.K_SPACE
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += " "
            elif (
                event.key == pygame.K_RETURN
            ):

                complete_keyboard_entry()
            elif (
                event.key == pygame.K_BACKSPACE
            ):
                app.KEYBOARD_text = (
                    app.KEYBOARD_text[:-1]
                )
    else:
        if is_up(event):
            app.KEYBOARD_row = max(
                0,
                app.KEYBOARD_row - 1
            )
        elif is_down(event):
            app.KEYBOARD_row = min(
                len(KEYBOARD_GRID) - 1,
                app.KEYBOARD_row + 1
            )
        elif is_left(event):
            app.KEYBOARD_column = max(
                0,
                app.KEYBOARD_column - 1
            )
        elif is_right(event):
            max_column = (
                len(
                    KEYBOARD_GRID[
                        app.KEYBOARD_row
                    ]
                ) - 1
            )
            app.KEYBOARD_column = min(
                max_column,
                app.KEYBOARD_column + 1
            )
        elif is_confirm(event):
            row = KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
            app.KEYBOARD_column = min(
                app.KEYBOARD_column,
                len(row) - 1
            )
            selected = row[
                app.KEYBOARD_column
            ]
            if (
                selected == "SPACE"
                and
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += " "
            elif (
                selected == "BACK"
            ):
                app.KEYBOARD_text = (
                    app.KEYBOARD_text[:-1]
                )
            elif (
                selected == "DONE"
            ):

                complete_keyboard_entry()
            elif (
                len(app.KEYBOARD_text) < 10
            ):
                app.KEYBOARD_text += (
                    selected
                )
        elif is_cancel(event):

            if (app.KEYBOARD_mode == "POKEMON_NICKNAME"):
                app.KEYBOARD_pokemon = None
            if (app.KEYBOARD_return_state is not None):
                change_state(
                    app.KEYBOARD_return_state
                )
    app.KEYBOARD_column = min(
        app.KEYBOARD_column,
        len(
            KEYBOARD_GRID[
                app.KEYBOARD_row
            ]
        ) - 1
    )

def handle_event_OPTIONS(event):
    if is_up(event):
        app.OPTIONS_index = max(0, app.OPTIONS_index - 1)
        if app.OPTIONS_index < app.OPTIONS_scroll:
            app.OPTIONS_scroll -= 1
    elif is_down(event):
        app.OPTIONS_index = min(8, app.OPTIONS_index + 1)
        if app.OPTIONS_index >= app.OPTIONS_scroll + 6:
            app.OPTIONS_scroll += 1
    elif is_left(event):
        if app.OPTIONS_index == 1:
            app.player_sprite -= 1
            if app.player_sprite < 0:
                app.player_sprite = 161
            save_player()
        elif app.OPTIONS_index == 7:
            app.option_level = max(1, app.option_level - 1)
            save_options()
        elif app.OPTIONS_index == 8:
            app.option_level_npc = max(1, app.option_level_npc - 1)
            save_options()
    elif is_right(event):
        if app.OPTIONS_index == 1:
            app.player_sprite += 1
            if app.player_sprite > 161:
                app.player_sprite = 0
            save_player()
        elif app.OPTIONS_index == 7:
            app.option_level = min(100, app.option_level + 1)
            save_options()
        elif app.OPTIONS_index == 8:
            app.option_level_npc = min(100, app.option_level_npc + 1)
            save_options()
    elif is_confirm(event):
        if app.OPTIONS_index == 0:

            app.KEYBOARD_mode = (
                "PLAYER_NAME"
            )

            app.KEYBOARD_return_state = (
                OPTIONS
            )

            app.KEYBOARD_team_index = None

            change_state(
                KEYBOARD
            )
        elif app.OPTIONS_index == 2:
            change_state(OPTIONS_MUSIC)
        elif app.OPTIONS_index == 3:
            app.option_omniscient = not app.option_omniscient
            save_options()
        elif app.OPTIONS_index == 4:
            app.option_pkmn_animation = not app.option_pkmn_animation
            save_options()
        elif app.OPTIONS_index == 5:
            app.option_fanart = (
                not app.option_fanart
            )
            save_options()
        elif app.OPTIONS_index == 6:
            app.option_music_shuffle = not app.option_music_shuffle
            save_options()
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)

def handle_event_TEAM_SELECT(event):
    if (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        if is_cancel(event):

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            return

        if is_confirm(event):

            team_index = (
                app.TEAM_SELECT_index - 1
            )

            pokemon_index = (
                app.TEAM_SELECT_pokemon_index
            )

            app.PKMN_EDIT_pokemon = (
                Pokemon.from_pokemon(
                    app.TEAM_SELECT_preview_team[
                        pokemon_index
                    ]
                )
            )

            app.PKMN_EDIT_source = (
                "TEAMBUILDER"
            )

            app.PKMN_EDIT_team_index = (
                team_index
            )

            app.PKMN_EDIT_pokemon_index = (
                pokemon_index
            )

            app.PKMN_EDIT_return_state = (
                TEAM_SELECT
            )

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            app.TEAM_SELECT_restore_index = (
                app.TEAM_SELECT_index
            )

            app.TEAM_SELECT_restore_scroll = (
                app.TEAM_SELECT_scroll
            )

            change_state(
                PKMN_EDIT
            )

            return

        handle_team_select_pokemon_navigation(
            event
        )

        return
    if (
        app.TEAM_SELECT_mode
        == "TEAMBUILDER"
        and
        app.TEAM_SELECT_submenu
    ):
        if is_up(event):

            app.TEAM_SELECT_submenu_index = max(
                0,
                app.TEAM_SELECT_submenu_index - 1
            )

        elif is_down(event):

            app.TEAM_SELECT_submenu_index = min(
                3,
                app.TEAM_SELECT_submenu_index + 1
            )

        elif is_cancel(event):

            app.TEAM_SELECT_submenu = False

        elif is_confirm(event):

            action = (
                TEAM_BUILDER_ACTIONS[
                    app.TEAM_SELECT_submenu_index
                ]
            )

            if action == "EDIT":

                if len(
                    app.TEAM_SELECT_preview_team
                ) == 0:

                    app.TEAM_SELECT_error = (
                        "TEAM HAS NO POKEMON"
                    )

                    app.TEAM_SELECT_submenu = False

                    return

                app.TEAM_SELECT_error = None

                app.TEAM_SELECT_submenu = False

                app.TEAM_SELECT_selecting_pokemon = (
                    True
                )

                app.TEAM_SELECT_pokemon_index = 0

            elif action == "RENAME":

                app.KEYBOARD_mode = (
                    "RENAME_TEAM"
                )

                app.KEYBOARD_return_state = (
                    TEAM_SELECT
                )

                app.KEYBOARD_team_index = (
                    app.TEAM_SELECT_index - 1
                )

                change_state(
                    KEYBOARD
                )

            elif action == "DUPLICATE":
                team = copy.deepcopy(
                    app.selected_team_data
                )

                save_data = load_save()

                save_data["teams"].insert(
                    0, team
                )

                save_save(
                    save_data
                )

                app.TEAM_SELECT_restore_index = 1
                app.TEAM_SELECT_restore_scroll = 0
                app.TEAM_SELECT_submenu = False

                change_state(
                    TEAM_SELECT
                )

            elif action == "ERASE":

                old_index = (
                    app.TEAM_SELECT_index
                )

                old_scroll = (
                    app.TEAM_SELECT_scroll
                )

                team_index = (
                    old_index - 1
                )

                save_data = load_save()

                if (
                    0
                    <= team_index
                    < len(
                        save_data["teams"]
                    )
                ):

                    del save_data[
                        "teams"
                    ][
                        team_index
                    ]

                    save_save(
                        save_data
                    )

                remaining_team_count = len(
                    save_data["teams"]
                )

                new_index = min(
                    old_index,
                    remaining_team_count
                )

                available_count = (
                    remaining_team_count
                    + 1
                )

                max_scroll = max(
                    0,
                    available_count - 7
                )

                new_scroll = min(
                    old_scroll,
                    max_scroll
                )

                if (
                    new_index
                    < new_scroll
                ):
                    new_scroll = (
                        new_index
                    )

                elif (
                    new_index
                    >= new_scroll + 7
                ):
                    new_scroll = max(
                        0,
                        new_index - 6
                    )

                app.TEAM_SELECT_restore_index = (
                    new_index
                )

                app.TEAM_SELECT_restore_scroll = (
                    new_scroll
                )

                app.TEAM_SELECT_submenu = False

                change_state(
                    TEAM_SELECT
                )
        
        return

    if (
        app.TEAM_SELECT_mode
        == "IMPORT"
        and
        app.TEAM_SELECT_selecting_pokemon
    ):

        if is_cancel(event):

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            return

        if is_confirm(event):

            pokemon_index = (
                app.TEAM_SELECT_pokemon_index
            )

            selected_pokemon = (
                Pokemon.from_pokemon(
                    app.TEAM_SELECT_preview_team[
                        pokemon_index
                    ]
                )
            )

            if (
                app.TEAM_SELECT_import_target
                == "ATTACKER"
            ):

                app.DAMAGE_CALCULATOR_attacker = (
                    selected_pokemon
                )

            else:

                app.DAMAGE_CALCULATOR_defender = (
                    selected_pokemon
                )

            save_damage_calculator(
                app.DAMAGE_CALCULATOR_attacker,
                app.DAMAGE_CALCULATOR_defender
            )

            app.TEAM_SELECT_selecting_pokemon = (
                False
            )

            app.TEAM_SELECT_mode = (
                "BATTLE"
            )

            change_state(
                app.TEAM_SELECT_return_state
            )

            return

        handle_team_select_pokemon_navigation(
            event
        )

        return
    is_lan_battle = app.connection_socket is not None
    if (
        is_up(event)
        and
        app.player_team is None
    ):
        handle_team_select_navigation(
            -1
        )
    elif (
        is_down(event)
        and
        app.player_team is None
    ):
        handle_team_select_navigation(
            1
        )
    elif is_cancel(event):

        if (
            app.connection_socket
            is None
        ):
            change_state(
                app.TEAM_SELECT_return_state
            )
    elif (
        is_confirm(event)
        and
        app.player_team is None
    ):
        if (
            app.TEAM_SELECT_mode
            == "TEAMBUILDER"
        ):

            if (
                app.TEAM_SELECT_index
                == 0
            ):

                app.KEYBOARD_mode = (
                    "CREATE_TEAM"
                )

                app.KEYBOARD_return_state = (
                    TEAM_SELECT
                )

                app.KEYBOARD_team_index = None

                change_state(
                    KEYBOARD
                )
            else:
                app.TEAM_SELECT_submenu = True
                app.TEAM_SELECT_submenu_index = 0

            return
        if (
            app.TEAM_SELECT_mode
            == "IMPORT"
        ):

            if len(
                app.TEAM_SELECT_preview_team
            ) == 0:

                app.TEAM_SELECT_error = (
                    "TEAM HAS NO POKEMON"
                )

                return

            app.TEAM_SELECT_error = None

            app.TEAM_SELECT_selecting_pokemon = (
                True
            )

            app.TEAM_SELECT_pokemon_index = 0

            return
        load_species()
        if app.TEAM_SELECT_index == 0:

            if (
                app.game_mode
                == "DEFEND_GYM"
            ):

                app.player_team = (
                    generate_type_team(
                        app.SINGLE_DEFEND_GYM_selected_type
                    )
                )

            else:

                app.player_team = [
                    Pokemon.from_species_number(
                        random.choice(
                            list(
                                SPECIES.keys()
                            )
                        )
                    )
                    for _ in range(6)
                ]

        else:

            app.player_team = [
                Pokemon.from_dict(
                    pokemon_data
                )
                for pokemon_data in
                app.selected_team_data[
                    "pokemon"
                ]
            ]
        for pokemon in app.player_team:
            pokemon.set_level(app.option_level)
        if (
            app.game_mode
            == "DEFEND_GYM"
        ):

            if not team_matches_type(
                app.player_team,
                app.SINGLE_DEFEND_GYM_selected_type
            ):

                app.TEAM_SELECT_error = (
                    f"ONLY "
                    f"{app.SINGLE_DEFEND_GYM_selected_type.upper()} TYPES"
                )

                app.player_team = None

                return
        if is_lan_battle:
            app.TEAM_SELECT_team_sent = False
        else:
            if app.game_mode == "ENDLESS":
                start_next_endless_battle()
            elif app.game_mode == "TOURNAMENT":
                trainer = app.tournament_current_trainer
                app.selected_trainer_data = trainer
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in trainer["team"]
                ]
            elif (
                app.game_mode
                == "DEFEND_GYM"
            ):

                trainer = (
                    app.selected_trainer_data
                )

                app.opponent_team = [

                    Pokemon.from_dict(
                        pokemon_data
                    )

                    for pokemon_data
                    in
                    trainer["team"]

                ]

            elif (
                app.single_battle_mode
                == "RANDOM_TEAM"
            ):
                app.opponent_team = [
                    Pokemon.from_species_number(
                        random.choice(
                            list(
                                SPECIES.keys()
                            )
                        )
                    )
                    for _ in range(6)
                ]
            elif (
                app.single_battle_mode
                == "MY_TEAM"
            ):
                selected_team_data = (
                    app.teams_data[
                        app.SINGLE_MENU_TRAINER_selected_team
                    ]
                )
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in
                    selected_team_data[
                        "pokemon"
                    ]
                ]
            elif (
                app.single_battle_mode
                == "TRAINER"
            ):
                app.opponent_team = [
                    Pokemon.from_dict(
                        pokemon_data
                    )
                    for pokemon_data in
                    app.selected_trainer_data[
                        "team"
                    ]
                ]
            for pokemon in app.opponent_team:
                pokemon.set_level(
                    app.option_level_npc
                )
            app.TEAM_PREVIEW_return_state = (
                TEAM_SELECT
            )
            change_state(
                TEAM_PREVIEW
            )


def handle_event_BATTLE_START(event):
    pass

def handle_event_SPECIES_VIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(
            0,
            app.TEAM_PREVIEW_index - 1
        )
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(
            5,
            app.TEAM_PREVIEW_index + 1
        )
    elif is_left(event):
        if app.option_omniscient:
            app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        if app.option_omniscient:
            app.TEAM_PREVIEW_column = 1
    elif is_vy(event):
        if (
            app.SPECIES_VIEW_mode
            == "STATS"
        ):
            app.SPECIES_VIEW_mode = (
                "AFFINITIES"
            )
        else:
            app.SPECIES_VIEW_mode = (
                "STATS"
            )
    elif is_cancel(event):
        change_state(
            app.previous_state
        )
    if app.TEAM_PREVIEW_column == 0:
        app.SPECIES_VIEW_pokemon = (
            app.player_team[
                app.TEAM_PREVIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        app.TEAM_PREVIEW_index
        <
        len(app.opponent_team)
    ):
        app.SPECIES_VIEW_pokemon = (
            app.opponent_team[
                app.TEAM_PREVIEW_index
            ]
        )

def handle_event_PKMN_VIEW(event):
    if is_up(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_index = max(
                0,
                app.PKMN_VIEW_index - 1
            )
        else:
            app.PKMN_VIEW_move_index = max(
                0,
                app.PKMN_VIEW_move_index - 1
            )
    elif is_down(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_index = min(
                5,
                app.PKMN_VIEW_index + 1
            )
        else:
            app.PKMN_VIEW_move_index = min(
                len(
                    app.PKMN_VIEW_pokemon.moves
                ) - 1,
                app.PKMN_VIEW_move_index + 1
            )
    elif is_left(event):

        if (
            app.PKMN_VIEW_move_index
            is None
            and
            app.option_omniscient
        ):
            
            if app.PKMN_VIEW_column == 0:
                app.PKMN_VIEW_column = 1
            else:
                app.PKMN_VIEW_column = 0

    elif is_right(event):

        if (
            app.PKMN_VIEW_move_index
            is None
            and
            app.option_omniscient
        ):
            if app.PKMN_VIEW_column == 0:
                app.PKMN_VIEW_column = 1
            else:
                app.PKMN_VIEW_column = 0
    elif is_cx(event):
        if (
            app.PKMN_VIEW_mode
            == "STATS"
        ):

            app.PKMN_VIEW_mode = (
                "EVS"
            )

        elif (
            app.PKMN_VIEW_mode
            == "EVS"
        ):

            app.PKMN_VIEW_mode = (
                "BASE"
            )

        else:

            app.PKMN_VIEW_mode = (
                "STATS"
            )
    elif is_vy(event):
        if app.PKMN_VIEW_mode == "AFFINITIES":
            app.PKMN_VIEW_mode = "STATS"
        else:
            app.PKMN_VIEW_mode = "AFFINITIES"
    elif is_confirm(event):
        if app.PKMN_VIEW_move_index is None:
            app.PKMN_VIEW_move_index = 0
    elif is_cancel(event):
        if app.PKMN_VIEW_move_index is not None:
            app.PKMN_VIEW_move_index = None
        else:
            change_state(
                app.previous_state
            )
    if app.PKMN_VIEW_column == 0:
        app.PKMN_VIEW_pokemon = (
            app.player_team[
                app.PKMN_VIEW_index
            ]
        )
    elif (
        app.option_omniscient
        and
        app.PKMN_VIEW_index
        <
        len(app.opponent_team)
    ):
        app.PKMN_VIEW_pokemon = (
            app.opponent_team[
                app.PKMN_VIEW_index
            ]
        )


def handle_event_TEAM_PREVIEW(event):
    if is_up(event):
        app.TEAM_PREVIEW_index = max(
            0,
            app.TEAM_PREVIEW_index - 1
        )
    elif is_down(event):
        app.TEAM_PREVIEW_index = min(
            5,
            app.TEAM_PREVIEW_index + 1
        )
    elif is_left(event):
        app.TEAM_PREVIEW_column = 0
    elif is_right(event):
        if app.option_omniscient:
            app.TEAM_PREVIEW_column = 1
    elif is_confirm(event):
        if app.TEAM_PREVIEW_column == 0:
            app.player_lead = (
                app.TEAM_PREVIEW_index
            )
            if (
                app.connection_socket
                is None
            ):
                change_state(
                    BATTLE_START
                )
    elif is_cvxy(event):
        if app.TEAM_PREVIEW_column == 0:
            app.PKMN_VIEW_index = (
                app.TEAM_PREVIEW_index
            )
            app.PKMN_VIEW_column = (
                app.TEAM_PREVIEW_column
            )
            app.PKMN_VIEW_pokemon = (
                app.player_team[
                    app.TEAM_PREVIEW_index
                ]
            )
            change_state(
                PKMN_VIEW
            )
        elif (
            app.option_omniscient
            and
            app.TEAM_PREVIEW_index
            <
            len(app.opponent_team)
        ):
            app.PKMN_VIEW_index = (
                app.TEAM_PREVIEW_index
            )
            app.PKMN_VIEW_column = (
                app.TEAM_PREVIEW_column
            )
            app.PKMN_VIEW_pokemon = (
                app.opponent_team[
                    app.TEAM_PREVIEW_index
                ]
            )
            change_state(
                PKMN_VIEW
            )
    elif is_cancel(event):
        if (
            app.game_mode
            == "ENDLESS"
        ):
            change_state(
                SINGLE_MENU
            )
        elif (
            app.allow_team_change
            and
            app.TEAM_SELECT_return_state
            is not None
        ):
            app.restore_team_select = True
            change_state(
                app.TEAM_PREVIEW_return_state
            )
        
def handle_event_LAN_JOIN(event):
    if is_cancel(event):
        disconnect()
        change_state(LAN_HOST_JOIN)

def handle_event_LAN_HOST(event):
    if is_cancel(event):
        disconnect()
        change_state(LAN_HOST_JOIN)

def handle_event_LAN_HOST_JOIN(event):
    if is_up(event):
        app.LAN_HOST_JOIN_index = max(0, app.LAN_HOST_JOIN_index - 1)
    elif is_down(event):
        app.LAN_HOST_JOIN_index = min(1, app.LAN_HOST_JOIN_index + 1)
    elif is_confirm(event):
        if app.LAN_HOST_JOIN_index == 0:
            change_state(LAN_HOST)
        elif app.LAN_HOST_JOIN_index == 1:
            change_state(LAN_JOIN)
    elif is_cancel(event):
        change_state(LAUNCHER_MENU)

def handle_event_LAUNCHER_MENU(event):
    if is_up(event):
        app.LAUNCHER_MENU_index = max(0, app.LAUNCHER_MENU_index - 1)
    elif is_down(event):
        app.LAUNCHER_MENU_index = min(len(app.LAUNCHER_MENU_options) - 1, app.LAUNCHER_MENU_index + 1)
    elif is_confirm(event):
        if app.LAUNCHER_MENU_index == 0:
            change_state(
                SINGLE_MENU
            )
        elif app.LAUNCHER_MENU_index == 1:
            change_state(
                LAN_HOST_JOIN
            )
        elif app.LAUNCHER_MENU_index == 2:
            load_species()
            calculator_data = (
                load_damage_calculator()
            )
            attacker_data = (
                calculator_data.get(
                    "attacker"
                )
            )
            defender_data = (
                calculator_data.get(
                    "defender"
                )
            )
            if attacker_data is not None:
                app.DAMAGE_CALCULATOR_attacker = (
                    Pokemon.from_dict(
                        attacker_data
                    )
                )
            else:
                app.DAMAGE_CALCULATOR_attacker = (
                    Pokemon.from_species_number(
                        6
                    )
                )
            if defender_data is not None:
                app.DAMAGE_CALCULATOR_defender = (
                    Pokemon.from_dict(
                        defender_data
                    )
                )
            else:
                app.DAMAGE_CALCULATOR_defender = (
                    Pokemon.from_species_number(
                        248
                    )
                )
            app.DAMAGE_CALCULATOR_index = 0
            app.DAMAGE_CALCULATOR_column = 1
            change_state(
                DAMAGE_CALCULATOR
            )
        elif app.LAUNCHER_MENU_index == 3:

            app.TEAM_SELECT_mode = (
                "TEAMBUILDER"
            )

            app.TEAM_SELECT_return_state = (
                LAUNCHER_MENU
            )

            change_state(
                TEAM_SELECT
            )

        elif app.LAUNCHER_MENU_index == 4:

            change_state(
                OPTIONS
            )

def handle_team_select_navigation(
    move_direction
):

    app.TEAM_SELECT_index = max(
        0,
        min(
            len(app.available_teams) - 1,
            app.TEAM_SELECT_index + move_direction
        )
    )

    if (
        app.TEAM_SELECT_index
        < app.TEAM_SELECT_scroll
    ):
        app.TEAM_SELECT_scroll -= 1

    elif (
        app.TEAM_SELECT_index
        >= app.TEAM_SELECT_scroll + 7
    ):
        app.TEAM_SELECT_scroll += 1

    if (
        app.TEAM_SELECT_mode
        != "IMPORT"
        and
        app.TEAM_SELECT_index == 0
    ):

        app.selected_team_data = None

        app.TEAM_SELECT_preview_team = []

        return

    if (
        app.TEAM_SELECT_mode
        == "IMPORT"
    ):
        team_index = (
            app.TEAM_SELECT_index
        )
    else:
        team_index = (
            app.TEAM_SELECT_index - 1
        )

    app.selected_team_data = (
        app.teams_data[
            team_index
        ]
    )

    app.TEAM_SELECT_preview_team = [
        Pokemon.from_dict(
            pokemon_data
        )
        for pokemon_data in
        app.selected_team_data[
            "pokemon"
        ]
    ]