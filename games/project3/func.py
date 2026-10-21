from constants import *
from pkmn_species import *
from pkmn_move import *

def disconnect():
    if app.connection_socket is not None:
        try:
            send_packet({"type":"DISCONNECT"})
        except OSError:
            pass
        try:
            app.connection_socket.close()
        except OSError:
            pass
    app.connection_socket = None
    app.connection_is_host = False
    app.LAN_HOST_connected = False
    app.LAN_JOIN_connected = False
    app.TEAM_PREVIEW_opponent_team = []
    app.TEAM_PREVIEW_selected_lead = None
    app.TEAM_PREVIEW_opponent_lead = None
    app.TEAM_PREVIEW_opponent_ready = False
    app.TEAM_PREVIEW_ready_sent = False

TYPE_SHEET = None
TYPE_ICON_WIDTH = 32
TYPE_ICON_HEIGHT = 16
TYPE_ALPHA_KEY = (255, 0, 228)
TYPE_POSITIONS = {
    "Normal":   (0, 0),
    "Fighting": (1, 0),
    "Flying":   (2, 0),
    "Poison":   (3, 0),
    "Ground":   (0, 1),
    "Rock":     (1, 1),
    "Bug":      (2, 1),
    "Ghost":    (3, 1),
    "Steel":    (0, 2),
    "Fairy":    (1, 2),
    "Fire":     (2, 2),
    "Water":    (3, 2),
    "Grass":    (0, 3),
    "Electric": (1, 3),
    "Psychic":  (2, 3),
    "Ice":      (3, 3),
    "Dragon":   (0, 4),
    "Dark":     (1, 4)
}
def load_type_sheet():
    global TYPE_SHEET
    if TYPE_SHEET is not None:
        return
    filepath = os.path.join(
        TEXT_ROOT,
        "sprites",
        "types.png"
    )
    TYPE_SHEET = pygame.image.load(
        filepath
    ).convert()
    TYPE_SHEET.set_colorkey(
        TYPE_ALPHA_KEY
    )
def get_type_icon(
    type_name
):
    load_type_sheet()
    column, row = TYPE_POSITIONS[type_name]
    rect = pygame.Rect(
        column * TYPE_ICON_WIDTH,
        row * TYPE_ICON_HEIGHT,
        TYPE_ICON_WIDTH,
        TYPE_ICON_HEIGHT
    )
    return TYPE_SHEET.subsurface(rect)


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
        if data == b"":
            packets.append({"type":"DISCONNECT"})
            return packets
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