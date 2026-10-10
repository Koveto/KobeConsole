import pygame
import platform

pygame.joystick.init()

IS_WINDOWS = (
    platform.system() == "Windows"
)

IS_LINUX = (
    platform.system() == "Linux"
)

LEFT_STICK_HORIZONTAL = 0
LEFT_STICK_VERTICAL = 1
CANCEL_BUTTON = 1
if IS_WINDOWS:

    CONFIRM_BUTTON = 0

    LEFT_BUTTON = 13
    RIGHT_BUTTON = 14
    UP_BUTTON = 11
    DOWN_BUTTON = 12

elif IS_LINUX:

    CONFIRM_BUTTON = 2

    LEFT_HAT = (-1, 0)
    RIGHT_HAT = (1, 0)
    UP_HAT = (0, 1)
    DOWN_HAT = (0, -1)

def get_controller_name():

    if pygame.joystick.get_count() == 0:
        return None

    joystick = pygame.joystick.Joystick(0)

    return joystick.get_name()
CONTROLLER_NAME = get_controller_name()
#Controller: PowerA Core (Plus) Wired Controller

def is_left(event):

    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_LEFT

    if IS_WINDOWS:
        return (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == LEFT_BUTTON
        )

    if IS_LINUX:
        return (
            event.type == pygame.JOYHATMOTION
            and event.value == LEFT_HAT
        )

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
    if IS_WINDOWS:
        if event.type == pygame.JOYBUTTONDOWN:
            return event.button == RIGHT_BUTTON

    #
    # Pi D-Pad
    #
    if IS_LINUX:
        if event.type == pygame.JOYHATMOTION:
            return event.value == RIGHT_HAT

    return False

def is_up(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_UP

    #
    # Windows D-Pad
    #
    if IS_WINDOWS:
        if event.type == pygame.JOYBUTTONDOWN:
            return event.button == UP_BUTTON

    #
    # Pi D-Pad
    #
    if IS_LINUX:
        if event.type == pygame.JOYHATMOTION:
            return event.value == UP_HAT

    return False

def is_down(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_DOWN

    #
    # Windows D-Pad
    #
    if IS_WINDOWS:
        if event.type == pygame.JOYBUTTONDOWN:
            return event.button == DOWN_BUTTON

    #
    # Pi D-Pad
    #
    if IS_LINUX:
        if event.type == pygame.JOYHATMOTION:
            return event.value == DOWN_HAT

    return False

def is_confirm(event):

    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_RETURN

    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == CONFIRM_BUTTON

    return False


def is_cancel(event):

    #
    # Keyboard
    #
    if event.type == pygame.KEYDOWN:
        return event.key == pygame.K_q

    if event.type == pygame.JOYBUTTONDOWN:
        return event.button == CANCEL_BUTTON

    return False