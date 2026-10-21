import os
import math
import random
import pygame
from nature import *
from func import *

POKEMON_SHEET = None
CELL_SIZE = 69
SPRITE_SIZE = 64
BORDER_SIZE = 5
ALPHA_KEY = (
    165,
    235,
    255
)
STATUS_NONE = None
STATUS_POISON = "POISON"
STATUS_BURN = "BURN"
STATUS_PARALYSIS = "PARALYSIS"
STATUS_SLEEP = "SLEEP"
STATUS_FREEZE = "FREEZE"
STATUS_FAINTED = "FAINTED"
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

class Pokemon:
    VALID_GENDERS = [
        "♂",
        "♀"
    ]

    MIN_LEVEL = 1
    MAX_LEVEL = 100

    def __init__(
        self,
        species,
        level=100,
        nature=HARDY,
        gender=None,
        nickname=None,
        moves=None,
        evs=None,
        ivs=None,
        is_shiny=False,
        front_sprite_number=None,
        back_sprite_number=None
    ):
        self.species = species
        self.species_no = species.no
        self.species_name = species.name
        self.nickname = nickname if nickname is not None else species.name
        if not (Pokemon.MIN_LEVEL <= level <= Pokemon.MAX_LEVEL):
            raise ValueError(f"Invalid level: {level}")
        self.level = level
        if not isinstance(nature,Nature):
            raise ValueError("Invalid nature")
        self.nature = nature
        if gender is None:
            gender = random.choice(Pokemon.VALID_GENDERS)
        if (gender not in Pokemon.VALID_GENDERS):
            raise ValueError(f"Invalid gender: {gender}")
        self.gender = gender
        self.status = None
        if evs is None:
            evs = [0,0,0,0,0,0]
        if len(evs) != 6:
            raise ValueError("EV list must contain 6 values")
        if any(ev < 0 or ev > 252 for ev in evs):
            raise ValueError("EVs must be between 0 and 252")
        if sum(evs) > 508:
            raise ValueError("EV total exceeds 508")
        if ivs is None:
            ivs = [31, 31, 31, 31, 31, 31]
        if len(ivs) != 6:
            raise ValueError("IV list must contain 6 values")
        if any(iv < 0 or iv > 31 for iv in ivs):
            raise ValueError("IVs must be between 0 and 31")
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
        if moves is None:
            moves = species.moves
        if len(moves) > 4:
            raise ValueError("Pokemon may only know 4 moves")
        self.moves = []
        for move in moves:
            if isinstance(move,str):
                move = get_move(move)
            if move is None:
                raise ValueError("Invalid move")
            self.moves.append(move)
        self.hp_base = species.stats["HP"]
        self.attack_base = species.stats["Atk"]
        self.defense_base = species.stats["Def"]
        self.special_attack_base = species.stats["SpAtk"]
        self.special_defense_base = species.stats["SpDef"]
        self.speed_base = species.stats["Spd"]
        self.attack_modifier = 0
        self.defense_modifier = 0
        self.special_attack_modifier = 0
        self.special_defense_modifier = 0
        self.speed_modifier = 0
        self.is_shiny = is_shiny
        self.front_sprite_number = front_sprite_number
        self.back_sprite_number = back_sprite_number
        if self.front_sprite_number is None:
            self.front_sprite_number = random.choice([0, 1, 2])
        if self.back_sprite_number is None:
            self.back_sprite_number = random.choice([0, 1])
        self.front_sprite_anim_state = False
        self.hp_max = self.calculate_hp()
        self.hp_current = self.hp_max
        self.attack = self.calculate_attack()
        self.defense = self.calculate_defense()
        self.special_attack = self.calculate_special_attack()
        self.special_defense = self.calculate_special_defense()
        self.speed = self.calculate_speed()
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
                anim_column = 5
            else:
                anim_column = 6
        else:
            front_column = self.front_sprite_number
            back_column = 3 + self.back_sprite_number
            if self.front_sprite_anim_state:
                anim_column = 0
            else:
                anim_column = 1
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
            )
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
            "moves": [move.name for move in self.moves]
        }

    @classmethod
    def from_dict(
        cls,
        data
    ):
        return cls(
            species=get_species(data["species_no"]),
            nickname=data["nickname"],
            level=data["level"],
            nature=NATURES[data["nature"]],
            gender=data["gender"],
            evs=data["evs"],
            ivs=data["ivs"],
            moves=data["moves"],
            is_shiny=data["is_shiny"],
            front_sprite_number=data["front_sprite_number"],
            back_sprite_number=data["back_sprite_number"]
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