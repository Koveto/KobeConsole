from constants import *
from func import *
from state import *

def update():
    if app.state == STATE_LAN_HOST:
        update_LAN_HOST()
    elif app.state == STATE_LAN_JOIN:
        update_LAN_JOIN()
    elif app.state == STATE_LAN_TEAM_PREVIEW:
        update_LAN_TEAM_PREVIEW()

def update_LAN_TEAM_PREVIEW():
    try:
        data = app.connection_socket.recv(1024)
        if data:
            app.STATE_LAN_TEAM_PREVIEW_last_message = data.decode()
    except (
        BlockingIOError,
        OSError
    ):
        pass

def update_LAN_JOIN():
    if app.STATE_LAN_JOIN_discovery_socket is None:
        return
    try:
        data, address = (app.STATE_LAN_JOIN_discovery_socket.recvfrom(1024))
        app.STATE_LAN_JOIN_discovered_host_ip = (address[0])
    except (
        BlockingIOError,
        OSError
    ):
        pass
    if ((app.STATE_LAN_JOIN_discovered_host_ip is not None) and \
        not (app.STATE_LAN_JOIN_connected)):
        try:
            app.STATE_LAN_JOIN_client_socket = (connect_to_server(app.STATE_LAN_JOIN_discovered_host_ip))
            app.STATE_LAN_JOIN_connected = True
            app.STATE_LAN_JOIN_is_host = False
            app.connection_socket = app.STATE_LAN_JOIN_client_socket
            app.connection_is_host = False
            change_state(STATE_LAN_TEAM_PREVIEW)
        except OSError:
            pass

def update_LAN_HOST():
    current_time = pygame.time.get_ticks()
    if (
        current_time
        - app.STATE_LAN_HOST_last_broadcast_time
        > 1000
    ):
        broadcast_host()
        app.STATE_LAN_HOST_last_broadcast_time = (current_time)
    if not app.STATE_LAN_HOST_connected:
        try:
            (app.STATE_LAN_HOST_client_socket, address) = app.STATE_LAN_HOST_server_socket.accept()
            app.STATE_LAN_HOST_client_socket.setblocking(False)
            app.STATE_LAN_HOST_connected = True
            app.STATE_LAN_HOST_is_host = True
            app.connection_socket = app.STATE_LAN_HOST_client_socket
            app.connection_is_host = True
            change_state(STATE_LAN_TEAM_PREVIEW)
        except (
            BlockingIOError,
            OSError
        ):
            pass