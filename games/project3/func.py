from constants import *
from pkmn_species import *
from pkmn_move import *

def send_packet(packet):
    app.connection_socket.send(
        (
            json.dumps(packet)
            + "\n"
        ).encode()
    )

def recv_packets():
    packets = []
    try:
        data = app.connection_socket.recv(
            8192
        )
        if data:
            app.connection_buffer += (
                data.decode()
            )
    except (
        BlockingIOError,
        OSError
    ):
        pass
    while "\n" in app.connection_buffer:
        line, app.connection_buffer = (
            app.connection_buffer.split(
                "\n",
                1
            )
        )
        if line:
            packets.append(
                json.loads(
                    line
                )
            )
    return packets

SPECIES = {}
def load_species():
    global SPECIES
    if SPECIES:
        return
    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "pkmn_stats.json"
    )
    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as infile:
        data = json.load(infile)
    for species_data in data["pokemon"]:

        species = PokemonSpecies(
            no=species_data["no"],
            name=species_data["name"],
            types=species_data["types"],
            stats=species_data["stats"],
            moves=species_data["moves"]
        )

        SPECIES[species.no] = species
def get_species(pokedex_number):
    load_species()
    return SPECIES.get(pokedex_number)
def generate_list_names_dex_numbers():
    load_species()
    for species in SPECIES.values():

        print(
            f"PKMN_{species.name.upper().replace(' ', '_')} = {species.no}"
        )

MOVE_DATA = {}
def load_moves():
    global MOVE_DATA
    if MOVE_DATA:
        return
    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "pkmn_moves.json"
    )
    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as infile:
        data = json.load(
            infile
        )["moves"]
    for name, move_data in data.items():
        MOVE_DATA[name] = Move(
            name=name,
            move_type=move_data["type"],
            category=move_data["category"],
            accuracy=move_data["accuracy"],
            power=move_data["power"]
        )
def get_move(name):
    load_moves()
    return MOVE_DATA.get(name)

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