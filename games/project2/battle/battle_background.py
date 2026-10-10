# USED BY MAIN FOR BATTLE STATE!

import pygame
import os

SPRITE_W = 240
SPRITE_H = 112
SCALE = 4

# Path to project root (one level up from battle/)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPRITE_PATH = os.path.join(ROOT, "sprites", "battlebackgrounds.png")


def load_battle_background(index):
    """
    Loads one background (0–15) from sprites/battlebackgrounds.png.
    Returns a scaled 960×448 surface.
    """

    sheet = pygame.image.load(SPRITE_PATH).convert_alpha()

    # Compute row/column in 4×4 grid
    col = index % 4
    row = index // 4

    x = col * SPRITE_W
    y = row * SPRITE_H

    # Extract the subsurface
    rect = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
    bg = sheet.subsurface(rect)

    return bg
