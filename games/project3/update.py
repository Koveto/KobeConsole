from constants import *
from func import *
from state import *
from save import *

def update():
    current_time = pygame.time.get_ticks()
    if (app.option_pkmn_animation and current_time - app.pkmn_animation_time > 500):
        app.pkmn_animation_time = current_time
        for pokemon in get_loaded_pokemon():
            pokemon.animate_sprite()
    if app.state == LAN_HOST:
        update_LAN_HOST()
    elif app.state == LAN_JOIN:
        update_LAN_JOIN()
    elif app.state == TEAM_PREVIEW:
        update_TEAM_PREVIEW()
    elif app.state == PKMN_VIEW:
        update_PKMN_VIEW()
    elif app.state == SPECIES_VIEW:
        update_SPECIES_VIEW()
    elif app.state == BATTLE_START:
        update_BATTLE_START()
    elif app.state == TEAM_SELECT:
        update_TEAM_SELECT()
    elif app.state == BATTLE_END:
        update_BATTLE_END()

def update_BATTLE_END():

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


def update_SPECIES_VIEW():
    for packet in recv_packets():
        if packet["type"] == "DISCONNECT":
            disconnect()
            change_state(LAN_HOST_JOIN)


def update_PKMN_VIEW():
    if (
        app.connection_socket
        is None
    ):
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
    if app.LAN_JOIN_discovery_socket is None:
        return
    try:
        data, address = (app.LAN_JOIN_discovery_socket.recvfrom(1024))
        app.LAN_JOIN_discovered_host_ip = (address[0])
    except (
        BlockingIOError,
        OSError
    ):
        pass
    if ((app.LAN_JOIN_discovered_host_ip is not None) and \
        not (app.LAN_JOIN_connected)):
        try:
            app.LAN_JOIN_client_socket = (connect_to_server(app.LAN_JOIN_discovered_host_ip))
            app.LAN_JOIN_connected = True
            app.LAN_JOIN_is_host = False
            app.connection_socket = app.LAN_JOIN_client_socket
            app.connection_is_host = False
            change_state(TEAM_SELECT)
        except OSError:
            pass

def update_LAN_HOST():
    current_time = pygame.time.get_ticks()
    if (
        current_time
        - app.LAN_HOST_last_broadcast_time
        > 1000
    ):
        broadcast_host()
        app.LAN_HOST_last_broadcast_time = (current_time)
    if not app.LAN_HOST_connected:
        try:
            (app.LAN_HOST_client_socket, address) = app.LAN_HOST_server_socket.accept()
            app.LAN_HOST_client_socket.setblocking(False)
            app.LAN_HOST_connected = True
            app.LAN_HOST_is_host = True
            app.connection_socket = app.LAN_HOST_client_socket
            app.connection_is_host = True
            change_state(TEAM_SELECT)
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