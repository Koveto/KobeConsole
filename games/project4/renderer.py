# renderer.py

import pygame
import cpu

from defines import *


pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "SMB Python Translation"
)

font = pygame.font.SysFont(
    "consolas",
    20
)


def draw():

    screen.fill((0, 0, 0))

    lines = [
        "=== REGISTERS ===",

        f"A  : {cpu.A:02X}",
        f"X  : {cpu.X:02X}",
        f"Y  : {cpu.Y:02X}",
        f"SP : {cpu.SP:02X}",

        "",

        "=== FLAGS ===",

        f"C : {cpu.C}",
        f"Z : {cpu.Z}",
        f"N : {cpu.N}",
        f"I : {cpu.I}",
        f"D : {cpu.D}",

        "",

        "=== DEBUG ===",

        f"FrameCounter Variable : {cpu.FrameCounter}",

        "",

        "=== NES RAM ===",

        f"FrameCounter ($09) : {cpu.NESRAM[FrameCounter]:02X}",
        f$08) : {cpu.NESRAM[ObjectOffset]:02X}",
        flag : {cpu.NESRAM[DisableScreenFlag]:02X}",
        f: {cpu.NESRAM[WarmBootValidation]:02X}",
    ]

    y = 20

    for line in lines:

        surface = font.render(
          rue,
            (255, 255, 255)
        )

        screen.blit(
            surface,
            (20, y)
        )

        y += 24

    pygame.display.flip()