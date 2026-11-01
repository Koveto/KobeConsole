import json
import random
import socketserver
import string
import threading


RELAY_HOST = ""
RELAY_PORT = 5001

ROOM_CODE_LENGTH = 6

ROOMS = {}
ROOMS_LOCK = threading.Lock()


def encode_packet(
    packet
):

    return (
        json.dumps(
            packet
        )
        + "\n"
    ).encode(
        "utf-8"
    )


def generate_room_code():

    characters = (
        "ABCDEFGHJKLMNPQRSTUVWXYZ"
    )

    while True:

        room_code = "".join(

            random.choice(
                characters
            )

            for _ in range(
                ROOM_CODE_LENGTH
            )

        )

        with ROOMS_LOCK:

            if room_code not in ROOMS:

                return room_code


def send_relay_packet(
    sock,
    packet
):

    if sock is None:

        return False

    try:

        sock.sendall(
            encode_packet(
                packet
            )
        )

    except OSError as error:

        print(
            (
                "Relay send failed: "
                f"{error}"
            ),
            flush=True
        )

        return False

    return True


def receive_first_packet(
    request
):

    buffer = ""

    while "\n" not in buffer:

        data = request.recv(
            4096
        )

        if data == b"":

            return None

        buffer += data.decode(
            "utf-8"
        )

        if len(
            buffer
        ) > 16384:

            return None

    line, remainder = buffer.split(
        "\n",
        1
    )

    if not line:

        return None

    try:

        packet = json.loads(
            line
        )

    except json.JSONDecodeError:

        return None

    return (
        packet,
        remainder
    )


class RelayRoom:

    def __init__(
        self,
        room_code,
        host_socket
    ):

        self.room_code = room_code

        self.host_socket = (
            host_socket
        )

        self.join_socket = None

        self.lock = (
            threading.Lock()
        )

        self.closed = False


class RelayRequestHandler(
    socketserver.BaseRequestHandler
):

    def handle(
        self
    ):

        room = None
        is_host = False
        remainder = ""

        try:

            first_result = (
                receive_first_packet(
                    self.request
                )
            )

            if first_result is None:

                return

            first_packet, remainder = (
                first_result
            )

            packet_type = (
                first_packet.get(
                    "type"
                )
            )

            if packet_type == "CREATE_ROOM":

                room, is_host = (
                    self.create_room()
                )

            elif packet_type == "JOIN_ROOM":

                room_code = str(
                    first_packet.get(
                        "room_code",
                        ""
                    )
                ).strip().upper()

                room, is_host = (
                    self.join_room(
                        room_code
                    )
                )

            else:

                send_relay_packet(
                    self.request,
                    {
                        "type": "ONLINE_ERROR",
                        "message": (
                            "INVALID REQUEST"
                        )
                    }
                )

                return

            if room is None:

                return

            if remainder:

                self.forward_data(
                    room,
                    is_host,
                    remainder.encode(
                        "utf-8"
                    )
                )

            self.forward_loop(
                room,
                is_host
            )

        except (
            ConnectionError,
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError
        ):

            pass

        finally:

            if room is not None:

                self.leave_room(
                    room,
                    is_host
                )


    def create_room(
        self
    ):

        room_code = (
            generate_room_code()
        )

        room = RelayRoom(
            room_code,
            self.request
        )

        with ROOMS_LOCK:

            ROOMS[
                room_code
            ] = room

        sent = (
            send_relay_packet(
                self.request,
                {
                    "type": "ROOM_CREATED",
                    "room_code": room_code
                }
            )
        )

        if not sent:

            with ROOMS_LOCK:

                if (
                    ROOMS.get(
                        room_code
                    )
                    is room
                ):

                    del ROOMS[
                        room_code
                    ]

            return (
                None,
                True
            )

        print(
            (
                "Room created: "
                f"{room_code}"
            ),
            flush=True
        )

        return (
            room,
            True
        )

    def join_room(
        self,
        room_code
    ):

        with ROOMS_LOCK:

            room = ROOMS.get(
                room_code
            )

            if (
                room is None
                or
                room.closed
            ):

                send_relay_packet(
                    self.request,
                    {
                        "type": "ONLINE_ERROR",
                        "message": (
                            "ROOM NOT FOUND"
                        )
                    }
                )

                print(
                    (
                        "Join failed, room "
                        f"not found: {room_code}"
                    ),
                    flush=True
                )

                return (
                    None,
                    False
                )

            if (
                room.join_socket
                is not None
            ):

                send_relay_packet(
                    self.request,
                    {
                        "type": "ONLINE_ERROR",
                        "message": (
                            "ROOM IS FULL"
                        )
                    }
                )

                print(
                    (
                        "Join failed, room "
                        f"full: {room_code}"
                    ),
                    flush=True
                )

                return (
                    None,
                    False
                )

            room.join_socket = (
                self.request
            )

        #
        # Notify the joining client first.
        #
        # The host must not advance unless the joining
        # client was also successfully notified.
        #

        join_notified = (
            send_relay_packet(
                room.join_socket,
                {
                    "type": "MATCH_FOUND",
                    "room_code": room_code,
                    "is_host": False
                }
            )
        )

        if not join_notified:

            with ROOMS_LOCK:

                if (
                    room.join_socket
                    is self.request
                ):

                    room.join_socket = None

            print(
                (
                    "Could not notify joining "
                    f"client for room {room_code}"
                ),
                flush=True
            )

            return (
                None,
                False
            )

        host_notified = (
            send_relay_packet(
                room.host_socket,
                {
                    "type": "MATCH_FOUND",
                    "room_code": room_code,
                    "is_host": True
                }
            )
        )

        if not host_notified:

            send_relay_packet(
                room.join_socket,
                {
                    "type": "ONLINE_ERROR",
                    "message": (
                        "HOST DISCONNECTED"
                    )
                }
            )

            print(
                (
                    "Could not notify host "
                    f"for room {room_code}"
                ),
                flush=True
            )

            return (
                None,
                False
            )

        print(
            (
                "Match found in room: "
                f"{room_code}"
            ),
            flush=True
        )

        return (
            room,
            False
        )
    

    def get_peer_socket(
        self,
        room,
        is_host
    ):

        if is_host:

            return room.join_socket

        return room.host_socket


    def forward_data(
        self,
        room,
        is_host,
        data
    ):

        peer_socket = (
            self.get_peer_socket(
                room,
                is_host
            )
        )

        if peer_socket is None:

            return

        with room.lock:

            peer_socket.sendall(
                data
            )


    def forward_loop(
        self,
        room,
        is_host
    ):

        self.request.settimeout(
            0.5
        )

        while True:

            if room.closed:

                return

            try:

                data = self.request.recv(
                    8192
                )

            except TimeoutError:

                continue

            except OSError as error:

                if (
                    error.__class__.__name__
                    == "TimeoutError"
                ):

                    continue

                raise

            if data == b"":

                return

            self.forward_data(
                room,
                is_host,
                data
            )


    def leave_room(
        self,
        room,
        is_host
    ):

        peer_socket = None

        with ROOMS_LOCK:

            if room.closed:

                return

            room.closed = True

            if is_host:

                peer_socket = (
                    room.join_socket
                )

            else:

                peer_socket = (
                    room.host_socket
                )

            if (
                ROOMS.get(
                    room.room_code
                )
                is room
            ):

                del ROOMS[
                    room.room_code
                ]

        if peer_socket is not None:

            try:

                send_relay_packet(
                    peer_socket,
                    {
                        "type": (
                            "DISCONNECT"
                        )
                    }
                )

            except OSError:

                pass


class ThreadedRelayServer(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer
):

    allow_reuse_address = True
    daemon_threads = True


def main():

    server_address = (
        RELAY_HOST,
        RELAY_PORT
    )

    with ThreadedRelayServer(
        server_address,
        RelayRequestHandler
    ) as server:

        print(
            (
                "Online relay listening "
                f"on port {RELAY_PORT}"
            )
        )

        server.serve_forever()


if __name__ == "__main__":

    main()