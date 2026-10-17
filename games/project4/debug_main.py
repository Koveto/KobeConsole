# debug_main.py

import pygame
import cpu

from renderer import draw
from defines import *

running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    cpu.FrameCounter += 1
    cpu.NESRAM[FrameCounter] += 1

    draw()

    clock.tick(60)

pygame.quit()