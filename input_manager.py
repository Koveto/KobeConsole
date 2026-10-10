import pygame
import platform

pygame.joystick.init()

for i in range(pygame.joystick.get_count()):

    joystick = pygame.joystick.Joystick(i)

    joystick.init()


IS_WINDOWS = (
    platform.system() == "Windows"
)

IS_LINUX = (
    platform.system() == "Linux"
)


#
# Controller Mappings
#

if IS_WINDOWS:

    CONTROLLER_A = 0
    CONTROLLER_B = 1
    CONTROLLER_HOME = 7

    CONTROLLER_DPAD_LEFT = 13
    CONTROLLER_DPAD_RIGHT = 14
    CONTROLLER_DPAD_UP = 11
    CONTROLLER_DPAD_DOWN = 12

elif IS_LINUX:

    CONTROLLER_A = 2
    CONTROLLER_B = 1
    CONTROLLER_HOME = 12

    CONTROLLER_DPAD_LEFT = (-1, 0)
    CONTROLLER_DPAD_RIGHT = (1, 0)
    CONTROLLER_DPAD_UP = (0, 1)
    CONTROLLER_DPAD_DOWN = (0, -1)


def get_controller_name():

    if pygame.joystick.get_count() == 0:
        return None

    joystick = pygame.joystick.Joystick(0)

    return joystick.get_name()


CONTROLLER_NAME = get_controller_name()


#
# Keyboard
#

def is_keyboard_up(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_UP
    )


def is_keyboard_down(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_DOWN
    )


def is_keyboard_left(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_LEFT
    )


def is_keyboard_right(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_RIGHT
    )


def is_keyboard_enter(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_RETURN
    )


def is_keyboard_escape(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
    )


def is_keyboard_q(event):

    return (
        event.type == pygame.KEYDOWN
        and event.key == pygame.K_q
    )


#
# Controller D-Pad
#

def is_controller_dpad_left(event):

    if IS_WINDOWS:

        return (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == CONTROLLER_DPAD_LEFT
        )

    if IS_LINUX:

        return (
            event.type == pygame.JOYHATMOTION
            and event.value == CONTROLLER_DPAD_LEFT
        )

    return False


def is_controller_dpad_right(event):

    if IS_WINDOWS:

        return (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == CONTROLLER_DPAD_RIGHT
        )

    if IS_LINUX:

        return (
            event.type == pygame.JOYHATMOTION
            and event.value == CONTROLLER_DPAD_RIGHT
        )

    return False


def is_controller_dpad_up(event):

    if IS_WINDOWS:

        return (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == CONTROLLER_DPAD_UP
        )

    if IS_LINUX:

        return (
            event.type == pygame.JOYHATMOTION
            and event.value == CONTROLLER_DPAD_UP
        )

    return False


def is_controller_dpad_down(event):

    if IS_WINDOWS:

        return (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == CONTROLLER_DPAD_DOWN
        )

    if IS_LINUX:

        return (
            event.type == pygame.JOYHATMOTION
            and event.value == CONTROLLER_DPAD_DOWN
        )

    return False


#
# Controller Buttons
#

def is_controller_button_a(event):

    return (
        event.type == pygame.JOYBUTTONDOWN
        and event.button == CONTROLLER_A
    )


def is_controller_button_b(event):

    return (
        event.type == pygame.JOYBUTTONDOWN
        and event.button == CONTROLLER_B
    )


def is_controller_button_home(event):

    return (
        event.type == pygame.JOYBUTTONDOWN
        and event.button == CONTROLLER_HOME
    )


#
# Actions
#

def is_up(event):

    return (
        is_keyboard_up(event)
        or is_controller_dpad_up(event)
    )


def is_down(event):

    return (
        is_keyboard_down(event)
        or is_controller_dpad_down(event)
    )


def is_left(event):

    return (
        is_keyboard_left(event)
        or is_controller_dpad_left(event)
    )


def is_right(event):

    return (
        is_keyboard_right(event)
        or is_controller_dpad_right(event)
    )


def is_confirm(event):

    return (
        is_keyboard_enter(event)
        or is_controller_button_a(event)
    )


def is_cancel(event):

    return (
        is_keyboard_escape(event)
        or is_controller_button_b(event)
    )


def is_quit(event):

    return (
        event.type == pygame.QUIT
        or is_keyboard_q(event)
        or is_controller_button_home(event)
    )