from constants import *
from func import *
from state import *

def update():
    if app.state == LAN_HOST:
        update_LAN_HOST()
    elif app.state == LAN_JOIN:
        update_LAN_JOIN()
    elif app.state == TEAM_PREVIEW:
        update_TEAM_PREVIEW()

def update_TEAM_PREVIEW():
    if not app.TEAM_PREVIEW_team_sent:
        team_data = []
        for pokemon in app.TEAM_PREVIEW_team:
            team_data.append(
                pokemon.to_dict()
            )
        message = json.dumps(
            team_data
        )
        app.connection_socket.send(
            (
                "TEAM:"
                + message
            ).encode()
        )
        app.TEAM_PREVIEW_team_sent = True
    try:
        data = (
            app.connection_socket.recv(
                8192
            )
        )
        if data:
            message = data.decode()
            if message.startswith(
                "TEAM:"
            ):
                json_text = (
                    message.replace(
                        "TEAM:",
                        "",
                        1
                    )
                )
                team_data = json.loads(
                    json_text
                )
                app.TEAM_PREVIEW_opponent_team = []
                for pokemon_data in team_data:
                    app.TEAM_PREVIEW_opponent_team.append(
                        Pokemon.from_dict(
                            pokemon_data
                        )
                    )
    except (
        BlockingIOError,
        OSError
    ):
        pass

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
            change_state(TEAM_PREVIEW)
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
            change_state(TEAM_PREVIEW)
        except (
            BlockingIOError,
            OSError
        ):
            pass