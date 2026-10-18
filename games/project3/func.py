from constants import *





def get_local_ip():

    temp_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    temp_socket.connect(
        ("8.8.8.8", 80)
    )

    ip_address = (
        temp_socket.getsockname()[0]
    )

    temp_socket.close()

    return ip_address

def broadcast_host():

    broadcast_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    broadcast_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BROADCAST,
        1
    )

    broadcast_socket.sendto(
        b"KOBE_TICTACTOE_HOST",
        ("<broadcast>", NUM_DISCOVERY_PORT)
    )

    broadcast_socket.close()

def listen_for_hosts():

    try:

        discovery_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        discovery_socket.bind(
            ("", NUM_DISCOVERY_PORT)
        )

        discovery_socket.setblocking(False)

        return discovery_socket

    except OSError:

        return None

def create_server(
    ip_address
):

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.bind(
        (
            ip_address,
            NUM_PORT
        )
    )

    server_socket.listen(1)

    server_socket.setblocking(
        False
    )

    return server_socket

def connect_to_server(
    host_ip
):

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.settimeout(
        2
    )

    client_socket.connect(
        (
            host_ip,
            NUM_PORT
        )
    )

    client_socket.setblocking(
        False
    )

    return client_socket