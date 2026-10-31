import os
import math
import random
import pygame
from nature import *
from func import *
from save import *

POKEMON_SHEET = None
CELL_SIZE = 69
SPRITE_SIZE = 64
BORDER_SIZE = 5
ALPHA_KEY = (
    165,
    235,
    255
)
FANART_CACHE = {}
def load_pokemon_sheet():
    global POKEMON_SHEET
    if POKEMON_SHEET is not None:
        return
    filepath = os.path.join(
        os.path.dirname(__file__),
        "sprites",
        "pokemon.png"
    )
    POKEMON_SHEET = pygame.image.load(
        filepath
    ).convert()
    POKEMON_SHEET.set_colorkey(
        ALPHA_KEY
    )
def get_sprite(
    pokedex_number,
    column
):
    load_pokemon_sheet()
    row = pokedex_number - 1
    x = (
        column * CELL_SIZE
        + BORDER_SIZE
    )
    y = (
        row * CELL_SIZE
        + BORDER_SIZE
    )
    rect = pygame.Rect(
        x,
        y,
        SPRITE_SIZE,
        SPRITE_SIZE
    )
    return POKEMON_SHEET.subsurface(
        rect
    )
def load_fanart(
    species_name,
    front=True
):

    direction = (
        "f"
        if front
        else "b"
    )

    cache_key = (
        species_name,
        direction
    )

    if cache_key in FANART_CACHE:

        return FANART_CACHE[
            cache_key
        ]

    sprite_dir = os.path.join(
        os.path.dirname(__file__),
        "sprites"
    )

    candidates = []

    prefix = (
        f"fanart_{species_name.lower()}_{direction}_"
    )

    for filename in os.listdir(
        sprite_dir
    ):

        if (
            filename.startswith(
                prefix
            )
            and
            filename.endswith(
                ".png"
            )
        ):

            candidates.append(
                filename
            )

    if len(candidates) == 0:

        FANART_CACHE[
            cache_key
        ] = None

        return None

    filename = random.choice(
        candidates
    )

    image = pygame.image.load(
        os.path.join(
            sprite_dir,
            filename
        )
    ).convert()

    image.set_colorkey(
        ALPHA_KEY
    )

    FANART_CACHE[
        cache_key
    ] = image

    return image
def load_fanart_frame(
    species_name,
    front,
    frame
):

    sprite_dir = os.path.join(
        os.path.dirname(__file__),
        "sprites"
    )

    direction = (
        "f"
        if front
        else "b"
    )

    filename = (
        f"fanart_"
        f"{species_name.lower()}_"
        f"{direction}_"
        f"{frame}.png"
    )

    filepath = os.path.join(
        sprite_dir,
        filename
    )

    if not os.path.exists(
        filepath
    ):
        return None

    image = pygame.image.load(
        filepath
    ).convert()

    image.set_colorkey(
        ALPHA_KEY
    )

    return image

class Pokemon:
    VALID_GENDERS = [
        "♂",
        "♀"
    ]

    MIN_LEVEL = 1
    MAX_LEVEL = 100

    @staticmethod
    def normalize_integer(
        value,
        minimum,
        maximum,
        default
    ):

        try:

            value = int(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            value = default

        return max(
            minimum,
            min(
                maximum,
                value
            )
        )


    @classmethod
    def normalize_level(
        cls,
        level
    ):

        return cls.normalize_integer(
            level,
            cls.MIN_LEVEL,
            cls.MAX_LEVEL,
            cls.MAX_LEVEL
        )


    @staticmethod
    def normalize_stat_values(
        values,
        value_count,
        minimum,
        maximum,
        default_value=0,
        total_maximum=None
    ):

        if not isinstance(
            values,
            (
                list,
                tuple
            )
        ):

            values = []

        normalized_values = []

        for index in range(
            value_count
        ):

            if index < len(
                values
            ):

                value = values[
                    index
                ]

            else:

                value = default_value

            value = (
                Pokemon.normalize_integer(
                    value,
                    minimum,
                    maximum,
                    default_value
                )
            )

            normalized_values.append(
                value
            )

        if total_maximum is None:

            return normalized_values

        overflow = max(
            0,
            sum(
                normalized_values
            )
            - total_maximum
        )

        for index in range(
            len(
                normalized_values
            ) - 1,
            -1,
            -1
        ):

            if overflow <= 0:
                break

            reduction = min(
                normalized_values[
                    index
                ],
                overflow
            )

            normalized_values[
                index
            ] -= reduction

            overflow -= reduction

        return normalized_values


    @staticmethod
    def get_move_name(
        move
    ):

        if isinstance(
            move,
            str
        ):

            return move

        if move is None:

            return None

        return getattr(
            move,
            "name",
            None
        )


    @staticmethod
    def resolve_move(
        move
    ):

        move_name = (
            Pokemon.get_move_name(
                move
            )
        )

        if not move_name:

            return None

        return get_move(
            move_name
        )


    @staticmethod
    def build_unique_move_list(
        moves
    ):

        unique_moves = []
        known_move_names = set()

        if not isinstance(
            moves,
            (
                list,
                tuple
            )
        ):

            return unique_moves

        for move in moves:

            resolved_move = (
                Pokemon.resolve_move(
                    move
                )
            )

            if resolved_move is None:
                continue

            if (
                resolved_move.name
                in known_move_names
            ):

                continue

            known_move_names.add(
                resolved_move.name
            )

            unique_moves.append(
                resolved_move
            )

        return unique_moves


    @staticmethod
    def normalize_moveset(
        moves,
        learnset
    ):

        legal_moves = (
            Pokemon.build_unique_move_list(
                learnset
            )
        )

        legal_move_names = {
            move.name
            for move in legal_moves
        }

        normalized_moves = []
        known_move_names = set()

        if isinstance(
            moves,
            (
                list,
                tuple
            )
        ):

            for move in moves:

                resolved_move = (
                    Pokemon.resolve_move(
                        move
                    )
                )

                if resolved_move is None:
                    continue

                if (
                    resolved_move.name
                    not in legal_move_names
                ):

                    continue

                if (
                    resolved_move.name
                    in known_move_names
                ):

                    continue

                normalized_moves.append(
                    resolved_move
                )

                known_move_names.add(
                    resolved_move.name
                )

                if len(
                    normalized_moves
                ) == 4:

                    return normalized_moves

        for move in legal_moves:

            if (
                move.name
                in known_move_names
            ):

                continue

            normalized_moves.append(
                move
            )

            known_move_names.add(
                move.name
            )

            if len(
                normalized_moves
            ) == 4:

                break

        return normalized_moves

    def __init__(
        self,
        species,
        level=100,
        nature=None,
        gender=None,
        nickname=None,
        moves=None,
        evs=None,
        ivs=None,
        is_shiny=None,
        front_sprite_number=None,
        back_sprite_number=None,
        status=None
    ):

        if species is None:

            raise ValueError(
                "Pokemon requires a valid species"
            )

        self.species = species

        self.species_no = (
            species.no
        )

        self.species_name = (
            species.name
        )

        if (
            nickname is None
            or
            not isinstance(
                nickname,
                str
            )
            or
            len(
                nickname.strip()
            ) == 0
        ):

            self.nickname = (
                species.name
            )

        else:

            self.nickname = (
                nickname
            )

        self.level = (
            Pokemon.normalize_level(
                level
            )
        )

        if not isinstance(
            nature,
            Nature
        ):

            nature = random.choice(
                list(
                    NATURES.values()
                )
            )

        self.nature = nature

        if (
            gender
            not in Pokemon.VALID_GENDERS
        ):

            gender = random.choice(
                Pokemon.VALID_GENDERS
            )

        self.gender = gender

        self.status = status

        if evs is None:

            stat_indices = [
                0,
                1,
                2,
                3,
                4,
                5
            ]

            random.shuffle(
                stat_indices
            )

            evs = [
                0,
                0,
                0,
                0,
                0,
                0
            ]

            evs[
                stat_indices[0]
            ] = 252

            evs[
                stat_indices[1]
            ] = 252

            evs[
                stat_indices[2]
            ] = 4

        evs = (
            Pokemon.normalize_stat_values(
                values=evs,
                value_count=6,
                minimum=0,
                maximum=252,
                default_value=0,
                total_maximum=508
            )
        )

        if ivs is None:

            ivs = [
                31,
                31,
                31,
                31,
                31,
                31
            ]

        ivs = (
            Pokemon.normalize_stat_values(
                values=ivs,
                value_count=6,
                minimum=0,
                maximum=31,
                default_value=31
            )
        )

        self.hp_ev = evs[0]
        self.attack_ev = evs[1]
        self.defense_ev = evs[2]
        self.special_attack_ev = evs[3]
        self.special_defense_ev = evs[4]
        self.speed_ev = evs[5]

        self.hp_iv = ivs[0]
        self.attack_iv = ivs[1]
        self.defense_iv = ivs[2]
        self.special_attack_iv = ivs[3]
        self.special_defense_iv = ivs[4]
        self.speed_iv = ivs[5]

        self.learnset = (
            Pokemon.build_unique_move_list(
                species.moves
            )
        )

        self.moves = (
            Pokemon.normalize_moveset(
                moves,
                self.learnset
            )
        )

        self.hp_base = (
            species.stats["HP"]
        )

        self.attack_base = (
            species.stats["Atk"]
        )

        self.defense_base = (
            species.stats["Def"]
        )

        self.special_attack_base = (
            species.stats["SpAtk"]
        )

        self.special_defense_base = (
            species.stats["SpDef"]
        )

        self.speed_base = (
            species.stats["Spd"]
        )

        self.attack_modifier = 0
        self.defense_modifier = 0
        self.special_attack_modifier = 0
        self.special_defense_modifier = 0
        self.speed_modifier = 0

        if (
            is_shiny
            not in (
                True,
                False
            )
        ):

            is_shiny = (
                random.randint(
                    1,
                    2
                )
                == 1
            )

        self.is_shiny = (
            is_shiny
        )

        self.front_sprite_number = (
            Pokemon.normalize_integer(
                front_sprite_number,
                0,
                2,
                random.choice(
                    [
                        0,
                        1,
                        2
                    ]
                )
            )
        )

        self.back_sprite_number = (
            Pokemon.normalize_integer(
                back_sprite_number,
                0,
                1,
                random.choice(
                    [
                        0,
                        1
                    ]
                )
            )
        )

        self.front_sprite_anim_state = (
            False
        )

        self.fanart_front_0 = None
        self.fanart_front_1 = None
        self.fanart_back_0 = None

        self.hp_max = (
            self.calculate_hp()
        )

        self.hp_current = (
            self.hp_max
        )

        self.attack = (
            self.calculate_attack()
        )

        self.defense = (
            self.calculate_defense()
        )

        self.special_attack = (
            self.calculate_special_attack()
        )

        self.special_defense = (
            self.calculate_special_defense()
        )

        self.speed = (
            self.calculate_speed()
        )

        self.fanart_front_0 = (
            load_fanart_frame(
                self.species_name,
                True,
                0
            )
        )

        self.fanart_front_1 = (
            load_fanart_frame(
                self.species_name,
                True,
                1
            )
        )

        self.fanart_back_0 = (
            load_fanart_frame(
                self.species_name,
                False,
                0
            )
        )

        self.update_sprites()

    def calculate_hp(self):
        return math.floor(((2 * self.hp_base + self.hp_iv + self.hp_ev / 4) * self.level) / 100) + self.level + 10

    def calculate_other_stat(
        self,
        base_stat,
        iv,
        ev,
        nature_multiplier
    ):
        return math.floor(nature_multiplier* (math.floor(((2 * base_stat+ iv+ ev / 4)* self.level)/ 100)+ 5))
        
    def calculate_attack(self):
        return (self.calculate_other_stat(self.attack_base,self.attack_iv,self.attack_ev,self.nature_multiplier("atk")))

    def calculate_defense(self):
        return (self.calculate_other_stat(self.defense_base,self.defense_iv,self.defense_ev,self.nature_multiplier("def")))

    def calculate_special_attack(self):
        return (self.calculate_other_stat(self.special_attack_base,self.special_attack_iv,self.special_attack_ev,self.nature_multiplier("spatk")))

    def calculate_special_defense(self):
        return (self.calculate_other_stat(self.special_defense_base,self.special_defense_iv,self.special_defense_ev,self.nature_multiplier("spdef")))

    def calculate_speed(self):
        return (self.calculate_other_stat(self.speed_base,self.speed_iv,self.speed_ev,self.nature_multiplier("spe")))

    def update_sprites(self):
        if self.is_shiny:
            front_column = 5 + self.front_sprite_number
            back_column = 8 + self.back_sprite_number
            if self.front_sprite_anim_state:
                anim_column = 6
            else:
                anim_column = 7
        else:
            front_column = self.front_sprite_number
            back_column = 3 + self.back_sprite_number
            if self.front_sprite_anim_state:
                anim_column = 1
            else:
                anim_column = 2
        self.front_sprite = get_sprite(self.species_no,front_column)
        self.front_sprite_anim = get_sprite(self.species_no,anim_column)
        self.back_sprite = get_sprite(self.species_no,back_column)

    def is_fainted(self):
        return self.hp_current <= 0

    def heal(self):
        self.hp_current = self.hp_max

    def take_damage(
        self,
        amount
    ):
        self.hp_current = max(0,self.hp_current - amount)

    def restore_hp(
        self,
        amount
    ):
        self.hp_current = min(self.hp_max,self.hp_current + amount)

    @classmethod
    def from_species_number(
        cls,
        species_number,
        **kwargs
    ):
        return cls(
            get_species(
                species_number
            ),
            **kwargs
        )

    @classmethod
    def from_pokemon(
        cls,
        pokemon
    ):
        return cls(
            species=pokemon.species,
            level=pokemon.level,
            nature=pokemon.nature,
            gender=pokemon.gender,
            nickname=pokemon.nickname,
            moves=[
                move.name
                for move in pokemon.moves
            ],
            evs=[
                pokemon.hp_ev,
                pokemon.attack_ev,
                pokemon.defense_ev,
                pokemon.special_attack_ev,
                pokemon.special_defense_ev,
                pokemon.speed_ev
            ],
            ivs=[
                pokemon.hp_iv,
                pokemon.attack_iv,
                pokemon.defense_iv,
                pokemon.special_attack_iv,
                pokemon.special_defense_iv,
                pokemon.speed_iv
            ],
            is_shiny=pokemon.is_shiny,
            front_sprite_number=(
                pokemon.front_sprite_number
            ),
            back_sprite_number=(
                pokemon.back_sprite_number
            ),
            status=pokemon.status
        )

    def nature_multiplier(
        self,
        stat_name
    ):
        if self.nature is None:
            return 1.0
        if (
            self.nature.boosted_stat
            == stat_name
        ):
            return 1.1
        if (
            self.nature.reduced_stat
            == stat_name
        ):
            return 0.9
        return 1.0

    @staticmethod
    def modifier_multiplier(
        modifier
    ):
        if not (-6 <= modifier <= 6):
            raise ValueError("Modifier must be -6 to 6")
        if modifier >= 0:
            return (2 + modifier) / 2
        return (2 / (2 + abs(modifier)))

    def to_dict(self):
        return {
            "species_no": self.species_no,
            "nickname": self.nickname,
            "level": self.level,
            "nature": self.nature.name,
            "gender": self.gender,
            "is_shiny": self.is_shiny,
            "front_sprite_number": self.front_sprite_number,
            "back_sprite_number": self.back_sprite_number,
            "evs": [
                self.hp_ev,
                self.attack_ev,
                self.defense_ev,
                self.special_attack_ev,
                self.special_defense_ev,
                self.speed_ev
            ],
            "ivs": [
                self.hp_iv,
                self.attack_iv,
                self.defense_iv,
                self.special_attack_iv,
                self.special_defense_iv,
                self.speed_iv
            ],
            "moves": [move.name for move in self.moves],
            "status": self.status
        }

    @classmethod
    def from_dict(
        cls,
        data
    ):

        if not isinstance(
            data,
            dict
        ):

            raise ValueError(
                "Pokemon data must be a dictionary"
            )

        species_number = (
            data.get(
                "species_no"
            )
        )

        species = (
            get_species(
                species_number
            )
        )

        if species is None:

            raise ValueError(
                (
                    "Invalid species number: "
                    f"{species_number}"
                )
            )

        nature_name = (
            data.get(
                "nature"
            )
        )

        nature = (
            NATURES.get(
                nature_name
            )
        )

        return cls(
            species=species,
            nickname=data.get(
                "nickname",
                species.name
            ),
            level=data.get(
                "level",
                cls.MAX_LEVEL
            ),
            nature=nature,
            gender=data.get(
                "gender"
            ),
            evs=data.get(
                "evs"
            ),
            ivs=data.get(
                "ivs"
            ),
            moves=data.get(
                "moves"
            ),
            is_shiny=data.get(
                "is_shiny"
            ),
            front_sprite_number=data.get(
                "front_sprite_number"
            ),
            back_sprite_number=data.get(
                "back_sprite_number"
            ),
            status=data.get(
                "status",
                STATUS_NONE
            )
        )

    def animate_sprite(self):
        self.front_sprite_anim_state = not self.front_sprite_anim_state
        self.update_sprites()

    def set_shiny(
        self,
        is_shiny
    ):
        self.is_shiny = is_shiny
        self.update_sprites()

    def set_front_sprite_number(
        self,
        number
    ):
        if number not in [0, 1, 2]:
            raise ValueError("front sprite 0-2")
        self.front_sprite_number = number
        self.update_sprites()

    def set_back_sprite_number(
        self,
        number
    ):
        if number not in [0,1]:
            raise ValueError("back sprite 0-1")
        self.back_sprite_number = number
        self.update_sprites()

    def nature_symbol(
            self,
            stat_name
    ):
        if (self.nature.boosted_stat == stat_name):
            return "+"
        if (self.nature.reduced_stat == stat_name):
            return "-"
        return ""

    def set_level(
        self,
        level
    ):
        if not (
            Pokemon.MIN_LEVEL
            <= level
            <= Pokemon.MAX_LEVEL
        ):
            raise ValueError(
                f"Invalid level: {level}"
            )
        old_hp_max = self.hp_max
        self.level = level
        self.hp_max = (
            self.calculate_hp()
        )
        self.attack = (
            self.calculate_attack()
        )
        self.defense = (
            self.calculate_defense()
        )
        self.special_attack = (
            self.calculate_special_attack()
        )
        self.special_defense = (
            self.calculate_special_defense()
        )
        self.speed = (
            self.calculate_speed()
        )
        if old_hp_max > 0:
            hp_percent = (
                self.hp_current
                / old_hp_max
            )
            self.hp_current = int(
                self.hp_max
                * hp_percent
            )
        else:
            self.hp_current = (
                self.hp_max
            )
        self.hp_current = min(
            self.hp_current,
            self.hp_max
        )

    def set_move(
        self,
        moveslot,
        move
    ):

        if not (
            0
            <= moveslot
            < 4
        ):

            raise ValueError(
                "moveslot must be 0-3"
            )

        move = (
            Pokemon.resolve_move(
                move
            )
        )

        if move is None:

            raise ValueError(
                "Invalid move"
            )

        legal_move_names = {
            legal_move.name
            for legal_move
            in self.learnset
        }

        if (
            move.name
            not in legal_move_names
        ):

            raise ValueError(
                (
                    f"{self.species_name} "
                    f"cannot learn {move.name}"
                )
            )

        for index, known_move in enumerate(
            self.moves
        ):

            if (
                index != moveslot
                and
                known_move.name
                == move.name
            ):

                raise ValueError(
                    (
                        "Pokemon cannot know "
                        "the same move twice"
                    )
                )

        if (
            moveslot
            < len(
                self.moves
            )
        ):

            self.moves[
                moveslot
            ] = move

            return

        if (
            moveslot
            == len(
                self.moves
            )
        ):

            self.moves.append(
                move
            )

            return

        raise ValueError(
            "Cannot leave empty moveslots"
        )

    def knows_move(
        self,
        move_name
    ):

        return any(
            move.name == move_name
            for move in self.moves
        )

    def set_evs(
        self,
        evs
    ):

        evs = (
            Pokemon.normalize_stat_values(
                values=evs,
                value_count=6,
                minimum=0,
                maximum=252,
                default_value=0,
                total_maximum=508
            )
        )

        self.hp_ev = evs[0]
        self.attack_ev = evs[1]
        self.defense_ev = evs[2]
        self.special_attack_ev = evs[3]
        self.special_defense_ev = evs[4]
        self.speed_ev = evs[5]

        self.set_level(
            self.level
        )

    def set_species(
        self,
        species
    ):

        if species is None:

            raise ValueError(
                "Pokemon requires a valid species"
            )

        old_species_name = (
            self.species_name
        )

        old_nickname = (
            self.nickname
        )

        old_hp_max = (
            self.hp_max
        )

        old_hp_current = (
            self.hp_current
        )

        old_moves = list(
            self.moves
        )

        self.species = species

        self.species_no = (
            species.no
        )

        self.species_name = (
            species.name
        )

        if (
            old_nickname
            == old_species_name
        ):

            self.nickname = (
                species.name
            )

        self.learnset = (
            Pokemon.build_unique_move_list(
                species.moves
            )
        )

        self.moves = (
            Pokemon.normalize_moveset(
                old_moves,
                self.learnset
            )
        )

        self.hp_base = (
            species.stats["HP"]
        )

        self.attack_base = (
            species.stats["Atk"]
        )

        self.defense_base = (
            species.stats["Def"]
        )

        self.special_attack_base = (
            species.stats["SpAtk"]
        )

        self.special_defense_base = (
            species.stats["SpDef"]
        )

        self.speed_base = (
            species.stats["Spd"]
        )

        self.fanart_front_0 = (
            load_fanart_frame(
                self.species_name,
                True,
                0
            )
        )

        self.fanart_front_1 = (
            load_fanart_frame(
                self.species_name,
                True,
                1
            )
        )

        self.fanart_back_0 = (
            load_fanart_frame(
                self.species_name,
                False,
                0
            )
        )

        if old_hp_max > 0:

            hp_percent = (
                old_hp_current
                / old_hp_max
            )

        else:

            hp_percent = 1.0

        self.hp_max = (
            self.calculate_hp()
        )

        self.attack = (
            self.calculate_attack()
        )

        self.defense = (
            self.calculate_defense()
        )

        self.special_attack = (
            self.calculate_special_attack()
        )

        self.special_defense = (
            self.calculate_special_defense()
        )

        self.speed = (
            self.calculate_speed()
        )

        self.hp_current = int(
            self.hp_max
            * hp_percent
        )

        self.hp_current = max(
            0,
            min(
                self.hp_max,
                self.hp_current
            )
        )

        self.update_sprites()