from constants import *
from pkmn_species import *
from pkmn_move import *

def load_trainers():
    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "trainers.json"
    )
    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as infile:
        return json.load(
            infile
        )

def play_music(filename):
    music_path = os.path.join(
        TEXT_ROOT,
        "music",
        filename
    )
    pygame.mixer.music.load(
        music_path
    )
    if app.option_music_shuffle:
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.play(-1)
    app.current_music = filename

def play_random_menu_music():
    songs = []
    for filename, data in (
        app.music_data.items()
    ):
        if data["menu"]:
            songs.append(filename)
    if not songs:
        return
    song = random.choice(songs)
    app.current_music_mode = ("MENU")
    play_music(song)

def play_random_battle_music():
    songs = []
    for filename, data in (
        app.music_data.items()
    ):
        if data["battle"]:
            songs.append(filename)
    if not songs:
        return
    app.current_music_mode = ("BATTLE")
    play_music(random.choice(songs))

def stop_music():
    pygame.mixer.music.stop()
    app.current_music = None

KEYBOARD_GRID = [
    ["A","B","C","D","E","F","G"],
    ["H","I","J","K","L","M","N"],
    ["O","P","Q","R","S","T","U"],
    ["V","W","X","Y","Z"],
    ["0","1","2","3","4","5","6","7","8","9"],
    ["SPACE","BACK","DONE"]
]

TRAINER_SHEET = None
TRAINER_CELL_SIZE = 65
TRAINER_SPRITE_SIZE = 64
TRAINER_BORDER_SIZE = 1
TRAINER_ALPHA_KEY = (112,192,160)
def load_trainer_sheet():
    global TRAINER_SHEET
    if TRAINER_SHEET is not None:
        return
    filepath = os.path.join(
        TEXT_ROOT,
        "sprites",
        "trainers.png"
    )
    TRAINER_SHEET = pygame.image.load(
        filepath
    ).convert()
    TRAINER_SHEET.set_colorkey(
        TRAINER_ALPHA_KEY
    )
def get_trainer_sprite(sprite_number):
    load_trainer_sheet()
    column = sprite_number % 10
    row = sprite_number // 10
    x = (column * TRAINER_CELL_SIZE + TRAINER_BORDER_SIZE)
    y = (row * TRAINER_CELL_SIZE + TRAINER_BORDER_SIZE)
    rect = pygame.Rect(
        x,
        y,
        TRAINER_SPRITE_SIZE,
        TRAINER_SPRITE_SIZE
    )
    return TRAINER_SHEET.subsurface(
        rect
    )

TYPE_CHART = {
    "Normal": {
        "Rock": 0.5, "Ghost": 0.0, "Steel": 0.5
    },
    "Fighting": {
        "Normal": 2.0, "Flying": 0.5, "Poison": 0.5, "Rock": 2.0,
        "Bug": 0.5, "Ghost": 0.0, "Steel": 2.0, "Psychic": 0.5,
        "Ice": 2.0, "Dark": 2.0, "Fairy": 0.5
    },
    "Flying": {
        "Fighting": 2.0, "Rock": 0.5, "Bug": 2.0, "Steel": 2.0,
        "Grass": 2.0, "Electric": 0.5
    },
    "Poison": {
        "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5,
        "Steel": 0.0, "Grass": 2.0, "Fairy": 2.0
    },
    "Ground": {
        "Flying": 0.0, "Poison": 2.0, "Rock": 2.0, "Bug": 0.5,
        "Steel": 2.0, "Fire": 2.0, "Grass": 0.5, "Electric": 2.0
    },
    "Rock": {
        "Fighting": 0.5, "Flying": 2.0, "Ground": 0.5, "Bug": 2.0,
        "Steel": 0.5, "Fire": 2.0, "Ice": 2.0
    },
    "Bug": {
        "Fighting": 0.5, "Flying": 0.5, "Poison": 0.5, "Ghost": 0.5,
        "Steel": 0.5, "Fire": 0.5, "Grass": 2.0, "Psychic": 2.0,
        "Dark": 2.0, "Fairy": 0.5
    },
    "Ghost": {
        "Normal": 0.0, "Ghost": 2.0, "Psychic": 2.0, "Dark": 0.5
    },
    "Steel": {
        "Rock": 2.0, "Steel": 0.5, "Fire": 0.5, "Water": 0.5,
        "Electric": 0.5, "Ice": 2.0, "Fairy": 2.0
    },
    "Fire": {
        "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0,
        "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0
    },
    "Water": {
        "Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0,
        "Rock": 2.0, "Dragon": 0.5
    },
    "Grass": {
        "Flying": 0.5, "Poison": 0.5, "Ground": 2.0, "Rock": 2.0,
        "Bug": 0.5, "Steel": 0.5, "Fire": 0.5, "Water": 2.0,
        "Grass": 0.5, "Dragon": 0.5
    },
    "Electric": {
        "Flying": 2.0, "Ground": 0.0, "Water": 2.0, "Grass": 0.5,
        "Electric": 0.5, "Dragon": 0.5
    },
    "Psychic": {
        "Fighting": 2.0, "Poison": 2.0, "Steel": 0.5, "Psychic": 0.5,
        "Dark": 0.0
    },
    "Ice": {
        "Flying": 2.0, "Ground": 2.0, "Steel": 0.5, "Fire": 0.5,
        "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Dragon": 2.0
    },
    "Dragon": {
        "Steel": 0.5, "Dragon": 2.0, "Fairy": 0.0
    },
    "Dark": {
        "Fighting": 0.5, "Ghost": 2.0, "Psychic": 2.0, "Dark": 0.5,
        "Fairy": 0.5
    },
    "Fairy": {
        "Fighting": 2.0, "Poison": 0.5, "Steel": 0.5, "Fire": 0.5,
        "Dragon": 2.0, "Dark": 2.0
    }
}

def type_effectiveness(attack_type: str, defense_type: str) -> float:
    """Return the damage multiplier for attack_type hitting defense_type."""
    return TYPE_CHART.get(attack_type, {}).get(defense_type, 1.0)

def combined_effectiveness(attack_type: str, defender_types: list[str]) -> float:
    multiplier = 1.0
    for t in defender_types:
        multiplier *= type_effectiveness(attack_type, t)
    return multiplier

def defensive_profile(pokemon):
    """Return lists of weaknesses, resistances, and immunities."""
    weaknesses = []
    resistances = []
    immunities = []

    for attack_type in TYPE_CHART.keys():
        mult = 1.0
        for t in pokemon.types:
            mult *= type_effectiveness(attack_type, t)

        if mult == 0:
            immunities.append(attack_type.lower())
        elif mult > 1:
            weaknesses.append(attack_type.lower())
        elif mult < 1:
            resistances.append(attack_type.lower())

    return weaknesses, resistances, immunities
TYPE_ORDER = [
    "Normal",
    "Fire",
    "Water",
    "Grass",
    "Electric",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy"
]
def get_affinities(pokemon):
    affinities = {}
    for attacking_type in TYPE_ORDER:
        multiplier = 1
        for defending_type in pokemon.species.types:
            multiplier *= (
                type_effectiveness(
                    attacking_type,
                    defending_type
                )
            )
        affinities[
            attacking_type
        ] = multiplier
    return affinities

def disconnect():

    connection_socket = (
        app.connection_socket
    )

    if connection_socket is not None:

        try:

            send_packet(
                {
                    "type": "DISCONNECT"
                }
            )

        except OSError:

            pass

    sockets = [
        app.connection_socket,
        app.ONLINE_connection_socket,
        app.LAN_HOST_server_socket,
        app.LAN_HOST_client_socket,
        app.LAN_JOIN_discovery_socket,
        app.LAN_JOIN_client_socket
    ]

    closed_socket_ids = set()

    for sock in sockets:

        if sock is None:
            continue

        socket_id = id(
            sock
        )

        if socket_id in closed_socket_ids:
            continue

        closed_socket_ids.add(
            socket_id
        )

        try:

            sock.close()

        except OSError:

            pass

    app.connection_socket = None
    app.connection_is_host = False
    app.connection_buffer = ""

    app.multiplayer_transport = None

    app.ONLINE_connection_socket = None
    app.ONLINE_connected = False
    app.ONLINE_matched = False
    app.ONLINE_is_host = False
    app.ONLINE_room_code = ""
    app.ONLINE_status = None

    app.LAN_HOST_server_socket = None
    app.LAN_HOST_client_socket = None
    app.LAN_JOIN_discovery_socket = None
    app.LAN_JOIN_client_socket = None

    app.LAN_HOST_connected = False
    app.LAN_JOIN_connected = False
    app.LAN_HOST_is_host = False
    app.LAN_JOIN_is_host = False

    app.player_team = None
    app.opponent_team = None

    app.player_lead = None
    app.opponent_lead = None

    app.TEAM_PREVIEW_index = 0
    app.TEAM_PREVIEW_column = 0

    app.TEAM_SELECT_index = 0
    app.TEAM_SELECT_scroll = 0
    app.TEAM_SELECT_preview_team = []
    app.TEAM_SELECT_opponent_team = None
    app.TEAM_SELECT_team_sent = False

    app.selected_team_data = None

    app.TEAM_PREVIEW_ready_sent = False
    app.TEAM_PREVIEW_opponent_ready = False

def is_multiplayer_connected():

    return (
        app.connection_socket
        is not None
    )


def is_lan_multiplayer():

    return (
        app.multiplayer_transport
        == "LAN"
    )


def is_online_multiplayer():

    return (
        app.multiplayer_transport
        == "ONLINE"
    )


def send_multiplayer_packet(
    packet
):

    return send_packet(
        packet
    )


def receive_multiplayer_packets():

    return recv_packets()


def disconnect_multiplayer():

    disconnect()
    
def get_loaded_pokemon():

    pokemon = []
    seen = set()

    def add_pokemon(
        loaded_pokemon
    ):

        if loaded_pokemon is None:
            return

        pokemon_id = id(
            loaded_pokemon
        )

        if pokemon_id in seen:
            return

        pokemon.append(
            loaded_pokemon
        )

        seen.add(
            pokemon_id
        )

    def add_team(
        team
    ):

        for loaded_pokemon in (
            team
            or []
        ):

            add_pokemon(
                loaded_pokemon
            )

    add_team(
        app.player_team
    )

    add_team(
        app.opponent_team
    )

    add_team(
        app.TEAM_SELECT_preview_team
    )

    add_team(
        app.SINGLE_MENU_TRAINER_preview_team
    )

    add_team(
        app.SINGLE_MENU_TRAINER_my_team_preview
    )

    add_team(
        app.SPECIES_EDIT_preview_pokemon
    )

    add_pokemon(
        app.DAMAGE_CALCULATOR_attacker
    )

    add_pokemon(
        app.DAMAGE_CALCULATOR_defender
    )

    add_pokemon(
        app.PKMN_INFO_pokemon
    )

    return pokemon

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


def send_packet(
    packet
):

    if (
        app.connection_socket
        is None
    ):

        return False

    packet_data = (
        (
            json.dumps(
                packet
            )
            + "\n"
        ).encode(
            "utf-8"
        )
    )

    try:

        app.connection_socket.sendall(
            packet_data
        )

    except OSError:

        return False

    return True

def recv_packets():

    packets = []

    if (
        app.connection_socket
        is None
    ):

        return packets

    try:

        data = (
            app.connection_socket.recv(
                8192
            )
        )

        if data == b"":

            packets.append(
                {
                    "type": "DISCONNECT"
                }
            )

            return packets

        if data:

            app.connection_buffer += (
                data.decode(
                    "utf-8"
                )
            )

    except BlockingIOError:

        pass

    except (
        OSError,
        UnicodeDecodeError
    ):

        packets.append(
            {
                "type": "DISCONNECT"
            }
        )

        return packets

    while (
        "\n"
        in app.connection_buffer
    ):

        line, app.connection_buffer = (
            app.connection_buffer.split(
                "\n",
                1
            )
        )

        if not line:

            continue

        try:

            packet = (
                json.loads(
                    line
                )
            )

        except json.JSONDecodeError:

            packets.append(
                {
                    "type": (
                        "NETWORK_ERROR"
                    ),
                    "message": (
                        "INVALID PACKET"
                    )
                }
            )

            continue

        if isinstance(
            packet,
            dict
        ):

            packets.append(
                packet
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
        print(f"PKMN_{species.name.upper().replace(' ', '_')} = {species.no}")

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

def connect_to_online_relay():

    relay_socket = (
        socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    )

    relay_socket.settimeout(
        5
    )

    try:

        relay_socket.connect(
            (
                ONLINE_RELAY_HOST,
                ONLINE_RELAY_PORT
            )
        )

    except OSError:

        relay_socket.close()

        return None

    relay_socket.setblocking(
        False
    )

    return relay_socket

def create_online_room():

    disconnect()

    relay_socket = (
        connect_to_online_relay()
    )

    if relay_socket is None:

        app.ONLINE_error = (
            "RELAY UNAVAILABLE"
        )

        return False

    app.connection_socket = (
        relay_socket
    )

    app.connection_is_host = True
    app.connection_buffer = ""

    app.multiplayer_transport = (
        "ONLINE"
    )

    app.ONLINE_connection_socket = (
        relay_socket
    )

    app.ONLINE_connected = True
    app.ONLINE_matched = False
    app.ONLINE_is_host = True

    app.ONLINE_room_code = ""
    app.ONLINE_error = None
    app.ONLINE_status = (
        "CREATING ROOM"
    )

    sent = send_packet(
        {
            "type": "CREATE_ROOM"
        }
    )

    if not sent:

        disconnect()

        app.ONLINE_error = (
            "CONNECTION FAILED"
        )

        return False

    return True


def join_online_room(
    room_code
):

    room_code = str(
        room_code
    ).strip().upper()

    if len(
        room_code
    ) != ONLINE_ROOM_CODE_LENGTH:

        app.ONLINE_error = (
            "INVALID ROOM CODE"
        )

        return False

    disconnect()

    relay_socket = (
        connect_to_online_relay()
    )

    if relay_socket is None:

        app.ONLINE_error = (
            "RELAY UNAVAILABLE"
        )

        return False

    app.connection_socket = (
        relay_socket
    )

    app.connection_is_host = False
    app.connection_buffer = ""

    app.multiplayer_transport = (
        "ONLINE"
    )

    app.ONLINE_connection_socket = (
        relay_socket
    )

    app.ONLINE_connected = True
    app.ONLINE_matched = False
    app.ONLINE_is_host = False

    app.ONLINE_room_code = (
        room_code
    )

    app.ONLINE_error = None
    app.ONLINE_status = (
        "JOINING ROOM"
    )

    sent = send_packet(
        {
            "type": "JOIN_ROOM",
            "room_code": room_code
        }
    )

    if not sent:

        disconnect()

        app.ONLINE_error = (
            "CONNECTION FAILED"
        )

        return False

    return True

def load_gyms():

    filepath = os.path.join(
        TEXT_ROOT,
        "data",
        "gyms.json"
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as infile:

        return json.load(
            infile
        )

def calculate_damage(
    attacker,
    defender,
    move,
    random_multiplier
):

    if move.category == "Physical":

        attack_stat = (
            attacker.attack
        )

        defense_stat = (
            defender.defense
        )

    else:

        attack_stat = (
            attacker.special_attack
        )

        defense_stat = (
            defender.special_defense
        )

    stab = 1.0

    if (
        move.type
        in
        attacker.species.types
    ):

        stab = 1.5

    effectiveness = (
        combined_effectiveness(
            move.type,
            defender.species.types
        )
    )

    base_damage = (

        2

        +

        math.floor(

            (

                (
                    attack_stat
                    /
                    defense_stat
                )

                *

                move.power

                *

                (
                    2
                    +
                    math.floor(
                        (
                            2
                            *
                            attacker.level
                        )
                        /
                        5
                    )
                )

            )

            /
            50

        )

    )

    damage = math.floor(

        base_damage
        *
        stab
        *
        effectiveness
        *
        random_multiplier

    )

    return max(
        0,
        damage
    )

def calculate_damage_percent_range(
    attacker,
    defender,
    move
):

    min_damage = calculate_damage(
        attacker,
        defender,
        move,
        0.85
    )

    max_damage = calculate_damage(
        attacker,
        defender,
        move,
        1.0
    )

    min_percent = (
        min_damage
        /
        defender.hp_max
        * 100
    )

    max_percent = (
        max_damage
        /
        defender.hp_max
        * 100
    )

    return (
        min_percent,
        max_percent
    )