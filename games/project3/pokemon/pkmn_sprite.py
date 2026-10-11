import os
import random
import pygame


POKEMON_SHEET = None
PLAYER_SPRITE = None

CELL_SIZE = 69
SPRITE_SIZE = 64
BORDER_SIZE = 5
ALPHA_KEY = (165, 235, 255)

def load_enemy_sprite(pokedex_number):

    global POKEMON_SHEET

    if POKEMON_SHEET is None:

        root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        filepath = os.path.join(
            root,
            "sprites",
            "pokemon.png"
        )

        POKEMON_SHEET = (
            pygame.image.load(
                filepath
            ).convert()
        )

        POKEMON_SHEET.set_colorkey(
            ALPHA_KEY
        )

    row = pokedex_number - 1

    column = random.choice(
        [0, 1, 2]
    )

    x = column * CELL_SIZE + BORDER_SIZE
    y = row * CELL_SIZE + BORDER_SIZE

    rect = pygame.Rect(
        x,
        y,
        SPRITE_SIZE,
        SPRITE_SIZE
    )

    return POKEMON_SHEET.subsurface(
        rect
    )

def load_player_sprite(pokedex_number):

    global POKEMON_SHEET

    if POKEMON_SHEET is None:

        root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        filepath = os.path.join(
            root,
            "sprites",
            "pokemon.png"
        )

        POKEMON_SHEET = (
            pygame.image.load(
                filepath
            ).convert()
        )

        POKEMON_SHEET.set_colorkey(
            ALPHA_KEY
        )

    row = pokedex_number - 1

    column = random.choice(
        [3, 4]
    )

    x = column * CELL_SIZE + BORDER_SIZE
    y = row * CELL_SIZE + BORDER_SIZE

    rect = pygame.Rect(
        x,
        y,
        SPRITE_SIZE,
        SPRITE_SIZE
    )

    return POKEMON_SHEET.subsurface(
        rect
    )