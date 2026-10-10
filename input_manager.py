import pygame


def is_left(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_LEFT

    #
    # Windows Controller
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 13

    #
    # Pi Controller
    #
    if event.type == pygame.JOYHATMOTION:
        return event.value == (-1, 0)

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

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_RETURN

    #
    # Windows Controller
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 0

    #
    # Pi Controller
    #
    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == 2

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