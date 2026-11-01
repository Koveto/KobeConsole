from constants import *
from func import *
from state import *
from save import *
from handle_event import *

def update():

    current_time = (
        pygame.time.get_ticks()
    )

    if (
        app.option_pkmn_animation
        and
        current_time
        - app.pkmn_animation_time
        > 500
    ):

        app.pkmn_animation_time = (
            current_time
        )

        for pokemon in get_loaded_pokemon():

            pokemon.animate_sprite()

    if app.state == LAN_HOST:

        update_LAN_HOST()

    elif app.state == LAN_JOIN:

        update_LAN_JOIN()

    elif app.state == ONLINE_HOST:

        update_ONLINE_HOST()

    elif app.state == ONLINE_JOIN:

        update_ONLINE_JOIN()

    elif app.state == TEAM_PREVIEW:

        update_TEAM_PREVIEW()

    elif app.state == BATTLE_START:

        update_BATTLE_START()

    elif app.state == TEAM_SELECT:

        update_TEAM_SELECT()

    elif app.state == BATTLE_END:

        update_BATTLE_END()

    elif app.state == PKMN_INFO:

        update_PKMN_INFO()

    elif app.state == SPECIES_EDIT:

        update_SPECIES_EDIT()

def process_online_packets():

    packets = (
        recv_packets()
    )

    for packet in packets:

        print(
            (
                "ONLINE PACKET: "
                f"{packet}"
            ),
            flush=True
        )

        packet_type = (
            packet.get(
                "type"
            )
        )

        if (
            packet_type
            == "ROOM_CREATED"
        ):

            app.ONLINE_room_code = (
                packet.get(
                    "room_code",
                    ""
                )
            )

            app.ONLINE_status = (
                "WAITING FOR PLAYER"
            )

        elif (
            packet_type
            == "MATCH_FOUND"
        ):

            app.ONLINE_room_code = (
                packet.get(
                    "room_code",
                    app.ONLINE_room_code
                )
            )

            app.ONLINE_is_host = bool(
                packet.get(
                    "is_host",
                    False
                )
            )

            app.connection_is_host = (
                app.ONLINE_is_host
            )

            app.ONLINE_connected = True
            app.ONLINE_matched = True

            app.ONLINE_status = (
                "MATCH FOUND"
            )

            return "MATCH_FOUND"

        elif (
            packet_type
            == "ONLINE_ERROR"
        ):

            message = (
                packet.get(
                    "message",
                    "ONLINE ERROR"
                )
            )

            disconnect_multiplayer()

            app.ONLINE_error = (
                message
            )

            app.ONLINE_status = (
                "FAILED"
            )

            return "ERROR"

        elif (
            packet_type
            == "NETWORK_ERROR"
        ):

            message = (
                packet.get(
                    "message",
                    "NETWORK ERROR"
                )
            )

            disconnect_multiplayer()

            app.ONLINE_error = (
                message
            )

            app.ONLINE_status = (
                "FAILED"
            )

            return "ERROR"

        elif (
            packet_type
            == "DISCONNECT"
        ):

            disconnect_multiplayer()

            app.ONLINE_error = (
                "OTHER PLAYER DISCONNECTED"
            )

            app.ONLINE_status = (
                "DISCONNECTED"
            )

            return "DISCONNECT"

    return None


def update_ONLINE_HOST():

    if (
        app.connection_socket
        is None
    ):

        return

    result = (
        process_online_packets()
    )

    if (
        result
        == "MATCH_FOUND"
    ):

        print(
            "HOST ENTERING TEAM SELECT",
            flush=True
        )

        open_team_select(
            mode="BATTLE",
            return_state=ONLINE_MENU
        )

def update_ONLINE_JOIN():

    if (
        app.connection_socket
        is None
    ):

        return

    result = (
        process_online_packets()
    )

    if (
        result
        == "MATCH_FOUND"
    ):

        print(
            "JOINER ENTERING TEAM SELECT",
            flush=True
        )

        open_team_select(
            mode="BATTLE",
            return_state=ONLINE_MENU
        )

def get_species_edit_hold_direction():

    keys = (
        pygame.key.get_pressed()
    )

    if keys[
        pygame.K_LEFT
    ]:

        return "LEFT"

    if keys[
        pygame.K_RIGHT
    ]:

        return "RIGHT"

    if keys[
        pygame.K_UP
    ]:

        return "UP"

    if keys[
        pygame.K_DOWN
    ]:

        return "DOWN"

    if (
        pygame.joystick.get_count()
        == 0
    ):

        return None

    joystick = (
        pygame.joystick.Joystick(
            0
        )
    )

    if not joystick.get_init():

        joystick.init()

    if (
        joystick.get_numaxes()
        > CONTROLLER_LEFT_STICK_X_AXIS
    ):

        horizontal_axis = (
            joystick.get_axis(
                CONTROLLER_LEFT_STICK_X_AXIS
            )
        )

        if (
            horizontal_axis
            < -STICK_PRESS_THRESHOLD
        ):

            return "LEFT"

        if (
            horizontal_axis
            > STICK_PRESS_THRESHOLD
        ):

            return "RIGHT"

    if (
        joystick.get_numaxes()
        > CONTROLLER_LEFT_STICK_Y_AXIS
    ):

        vertical_axis = (
            joystick.get_axis(
                CONTROLLER_LEFT_STICK_Y_AXIS
            )
        )

        if (
            vertical_axis
            < -STICK_PRESS_THRESHOLD
        ):

            return "UP"

        if (
            vertical_axis
            > STICK_PRESS_THRESHOLD
        ):

            return "DOWN"

    if IS_WINDOWS:

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_LEFT
            and
            joystick.get_button(
                CONTROLLER_DPAD_LEFT
            )
        ):

            return "LEFT"

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_RIGHT
            and
            joystick.get_button(
                CONTROLLER_DPAD_RIGHT
            )
        ):

            return "RIGHT"

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_UP
            and
            joystick.get_button(
                CONTROLLER_DPAD_UP
            )
        ):

            return "UP"

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_DOWN
            and
            joystick.get_button(
                CONTROLLER_DPAD_DOWN
            )
        ):

            return "DOWN"

    elif IS_LINUX:

        if (
            joystick.get_numhats()
            > 0
        ):

            hat_x, hat_y = (
                joystick.get_hat(
                    0
                )
            )

            if hat_x < 0:

                return "LEFT"

            if hat_x > 0:

                return "RIGHT"

            if hat_y > 0:

                return "UP"

            if hat_y < 0:

                return "DOWN"

    return None

def update_SPECIES_EDIT():

    if (
        app.SPECIES_EDIT_dex_mode
    ):

        reset_species_edit_hold()

        return

    direction = (
        get_species_edit_hold_direction()
    )

    if direction is None:

        reset_species_edit_hold()

        return

    current_time = (
        pygame.time.get_ticks()
    )

    if (
        direction
        != app.SPECIES_EDIT_hold_direction
    ):

        app.SPECIES_EDIT_hold_direction = (
            direction
        )

        app.SPECIES_EDIT_hold_start_time = (
            current_time
        )

        app.SPECIES_EDIT_repeat_time = (
            current_time
        )

        return

    initial_delay = 350
    repeat_delay = 80

    held_time = (
        current_time
        - app.SPECIES_EDIT_hold_start_time
    )

    since_last_repeat = (
        current_time
        - app.SPECIES_EDIT_repeat_time
    )

    if (
        held_time
        < initial_delay
        or
        since_last_repeat
        < repeat_delay
    ):

        return

    moved = (
        move_species_edit_selection(
            direction
        )
    )

    app.SPECIES_EDIT_repeat_time = (
        current_time
    )

    if not moved:

        return

def get_pkmn_info_ev_hold_direction():

    keys = pygame.key.get_pressed()

    if keys[
        pygame.K_LEFT
    ]:

        return -1

    if keys[
        pygame.K_RIGHT
    ]:

        return 1

    if (
        pygame.joystick.get_count()
        == 0
    ):

        return 0

    joystick = (
        pygame.joystick.Joystick(
            0
        )
    )

    if not joystick.get_init():

        joystick.init()

    if (
        joystick.get_numaxes()
        > 0
    ):

        horizontal_axis = (
            joystick.get_axis(
                0
            )
        )

        if horizontal_axis < -0.8:

            return -1

        if horizontal_axis > 0.8:

            return 1

    if IS_WINDOWS:

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_LEFT
            and
            joystick.get_button(
                CONTROLLER_DPAD_LEFT
            )
        ):

            return -1

        if (
            joystick.get_numbuttons()
            > CONTROLLER_DPAD_RIGHT
            and
            joystick.get_button(
                CONTROLLER_DPAD_RIGHT
            )
        ):

            return 1

    elif IS_LINUX:

        if (
            joystick.get_numhats()
            > 0
        ):

            hat_x, hat_y = (
                joystick.get_hat(
                    0
                )
            )

            if hat_x < 0:

                return -1

            if hat_x > 0:

                return 1

    return 0


def reset_pkmn_info_ev_hold():

    app.PKMN_INFO_ev_hold_direction = 0
    app.PKMN_INFO_ev_hold_start_time = 0
    app.PKMN_INFO_ev_repeat_time = 0


def update_PKMN_INFO():

    if (
        app.connection_socket
        is not None
    ):

        for packet in recv_packets():

            if (
                packet["type"]
                == "DISCONNECT"
            ):

                disconnect()

                change_state(
                    LAN_HOST_JOIN
                )

                return

    if (
        not app.PKMN_INFO_editable
        or
        app.PKMN_INFO_mode
        != "STATS"
    ):

        reset_pkmn_info_ev_hold()

        return

    is_level_selected = (
        app.PKMN_INFO_stats_index
        == 2
    )

    is_ev_selected = (
        3
        <= app.PKMN_INFO_stats_index
        <= 8
    )

    if (
        not is_level_selected
        and
        not is_ev_selected
    ):

        reset_pkmn_info_ev_hold()

        return

    direction = (
        get_pkmn_info_ev_hold_direction()
    )

    if direction == 0:

        reset_pkmn_info_ev_hold()

        return

    current_time = (
        pygame.time.get_ticks()
    )

    if (
        direction
        != app.PKMN_INFO_ev_hold_direction
    ):

        app.PKMN_INFO_ev_hold_direction = (
            direction
        )

        app.PKMN_INFO_ev_hold_start_time = (
            current_time
        )

        app.PKMN_INFO_ev_repeat_time = (
            current_time
        )

        return

    initial_delay = 350
    repeat_delay = 70

    held_time = (
        current_time
        - app.PKMN_INFO_ev_hold_start_time
    )

    since_last_repeat = (
        current_time
        - app.PKMN_INFO_ev_repeat_time
    )

    if (
        held_time
        < initial_delay
        or
        since_last_repeat
        < repeat_delay
    ):

        return

    if is_level_selected:

        adjust_pkmn_info_level(
            direction
        )

    elif is_ev_selected:

        app.PKMN_INFO_ev_index = (
            app.PKMN_INFO_stats_index
            - 3
        )

        adjust_pkmn_info_ev(
            direction
        )

    app.PKMN_INFO_ev_repeat_time = (
        current_time
    )

def update_BATTLE_END():
    if (
        app.game_mode
        == "ENDLESS"
    ):
        if random.choice(
            [True, False]
        ):

            app.endless_wins += 1

            save_endless_record(
                app.endless_wins
            )

            start_next_endless_battle()

            app.player_lead = None

            change_state(
                TEAM_PREVIEW
            )

        else:

            app.endless_active = False

            app.endless_wins = 0

            change_state(
                SINGLE_MENU
            )

        return

    if (
        app.game_mode
        == "TOURNAMENT"
    ):

        if random.choice(
            [True, False]
        ):

            app.tournament_round += 1
            app.player_lead = None

            if (
                app.tournament_round
                == 1
            ):

                app.tournament_semifinals = [

                    "PLAYER",

                    random.choice(
                        [
                            app.tournament_quarterfinals[2],
                            app.tournament_quarterfinals[3]
                        ]
                    ),

                    random.choice(
                        [
                            app.tournament_quarterfinals[4],
                            app.tournament_quarterfinals[5]
                        ]
                    ),

                    random.choice(
                        [
                            app.tournament_quarterfinals[6],
                            app.tournament_quarterfinals[7]
                        ]
                    )

                ]

            elif (
                app.tournament_round
                == 2
            ):

                app.tournament_finals = [

                    "PLAYER",

                    random.choice(
                        [
                            app.tournament_semifinals[2],
                            app.tournament_semifinals[3]
                        ]
                    )

                ]

            elif (
                app.tournament_round
                >= 3
            ):

                    save_title()

                    app.tournament_active = False

                    change_state(
                        SINGLE_MENU
                    )

                    return

            change_state(
                SINGLE_BRACKET
            )

        else:

            app.tournament_active = False

            change_state(
                SINGLE_MENU
            )

        return

    if (
        app.game_mode
        == "DEFEND_GYM"
    ):

        if random.choice(
            [True, False]
        ):

            gym_progress = (
                ensure_gym_progress()
            )

            gym_progress[
                app.SINGLE_DEFEND_GYM_selected_type
            ][
                app.selected_SINGLE_DEFEND_GYM_trainer_index
            ] = True

            save_gym_progress(
                gym_progress
            )

        app.player_lead = None

        change_state(
            SINGLE_DEFEND_GYM
        )

        return

    if (
        app.single_battle_mode
        == "TRAINER"
        and
        app.selected_trainer_data
        is not None
    ):
        trainer_name = (
            app.selected_trainer_data[
                "name"
            ]
        )
        if (
            trainer_name
            not in
            get_trainer_defeats()
        ):
            save_trainer_defeat(
                trainer_name
            )
    app.restore_single_menu_trainer = True
    change_state(
        SINGLE_MENU_TRAINER
    )

def update_TEAM_SELECT():
    if app.connection_socket is None:
        return
    if (
        app.player_team is not None
        and
        not app.TEAM_SELECT_team_sent
    ):
        team_data = [
            pokemon.to_dict()
            for pokemon in app.player_team
        ]
        send_packet(
            {
                "type": "TEAM",
                "data": team_data
            }
        )
        app.TEAM_SELECT_team_sent = True
    for packet in recv_packets():
        if packet["type"] == "TEAM":
            app.TEAM_SELECT_opponent_team = []
            for pokemon_data in packet["data"]:
                app.TEAM_SELECT_opponent_team.append(
                    Pokemon.from_dict(pokemon_data)
                )
        elif packet["type"] == "DISCONNECT":
            disconnect()
            change_state(LAN_HOST_JOIN)
    if (
        app.connection_socket
        is not None
        and
        app.player_team is not None
        and
        app.TEAM_SELECT_opponent_team
        is not None
    ):
        change_state(
            TEAM_PREVIEW
        )


def update_TEAM_PREVIEW():
    if app.connection_socket is None:
        return
    if (
        app.player_lead
        is not None
        and
        not app.TEAM_PREVIEW_ready_sent
    ):
        send_packet(
            {
                "type": "LEAD",
                "data":
                    app.player_lead
            }
        )
        app.TEAM_PREVIEW_ready_sent = True
    for packet in recv_packets():
        if packet["type"] == "LEAD":
            app.opponent_lead = (
                packet["data"]
            )
            app.TEAM_PREVIEW_opponent_ready = True
        elif (
            packet["type"]
            == "DISCONNECT"
        ):
            disconnect()
            change_state(
                LAN_HOST_JOIN
            )
    if (
        app.player_lead
        is not None
        and
        app.TEAM_PREVIEW_opponent_ready
    ):
        change_state(
            BATTLE_START
        )

def update_LAN_JOIN():

    if (
        app.LAN_JOIN_discovery_socket
        is not None
    ):

        try:

            data, address = (
                app.LAN_JOIN_discovery_socket.recvfrom(
                    1024
                )
            )

            app.LAN_JOIN_discovered_host_ip = (
                address[0]
            )

        except (
            BlockingIOError,
            OSError
        ):

            pass

    if (
        app.LAN_JOIN_discovered_host_ip
        is None
        or
        app.LAN_JOIN_connected
    ):

        return

    try:

        app.LAN_JOIN_client_socket = (
            connect_to_server(
                app.LAN_JOIN_discovered_host_ip
            )
        )

        app.LAN_JOIN_connected = True
        app.LAN_JOIN_is_host = False

        app.connection_socket = (
            app.LAN_JOIN_client_socket
        )

        app.connection_is_host = False
        app.connection_buffer = ""

        app.multiplayer_transport = (
            "LAN"
        )

        open_team_select(
            mode="BATTLE",
            return_state=LAN_HOST_JOIN
        )

    except OSError:

        pass

def update_LAN_HOST():

    current_time = (
        pygame.time.get_ticks()
    )

    if (
        current_time
        - app.LAN_HOST_last_broadcast_time
        > 1000
    ):

        broadcast_host()

        app.LAN_HOST_last_broadcast_time = (
            current_time
        )

    if app.LAN_HOST_connected:
        return

    try:

        (
            app.LAN_HOST_client_socket,
            address
        ) = (
            app.LAN_HOST_server_socket.accept()
        )

        app.LAN_HOST_client_socket.setblocking(
            False
        )

        app.LAN_HOST_connected = True
        app.LAN_HOST_is_host = True

        app.connection_socket = (
            app.LAN_HOST_client_socket
        )

        app.connection_is_host = True
        app.connection_buffer = ""

        app.multiplayer_transport = (
            "LAN"
        )

        open_team_select(
            mode="BATTLE",
            return_state=LAN_HOST_JOIN
        )

    except (
        BlockingIOError,
        OSError
    ):

        pass

def update_BATTLE_START():

    if (
        app.connection_socket
        is None
    ):

        change_state(
            BATTLE_END
        )

        return

    for packet in recv_packets():

        if (
            packet["type"]
            == "DISCONNECT"
        ):
            disconnect()
            change_state(
                LAN_HOST_JOIN
            )