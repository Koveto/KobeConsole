import pygame
import platform

IS_PI = (
    platform.system() == "Linux"
)


def is_left(event):

    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_LEFT

    if IS_PI:

        if event.type == pygame.JOYHATMOTION:
            return event.value == (-1, 0)

    else:

        if event.type == pygame.JOYBUTTONDOWN:
            return event.button == 13

    return False

def is_right(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_RIGHT

    #
    # Windows D-Pad
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 14

    #
    # Pi D-Pad
    #
    if event.type == pygame.JOYHATMOTION:
        return event.value == (1, 0)

    return False

def is_confirm(event):

    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_RETURN

    if event.type == pygame.JOYBUTTONDOWN:

        if IS_PI:
            return event.button == 2

        return event.button == 0

    return False


def is_cancel(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_q

    #
    # Windows Controller
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 1

    #
    # Pi Controller
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 1

    return False