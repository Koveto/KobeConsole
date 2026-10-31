import platform

import pygame


#
# Platform
#

IS_WINDOWS = (
    platform.system()
    == "Windows"
)

IS_LINUX = (
    platform.system()
    == "Linux"
)


#
# Keyboard mappings
#
# Face buttons:
#
# Z = A / Confirm
# X = B / Cancel
# C = X
# V = Y
#
# Shoulder controls:
#
# A = Left front shoulder
# S = Right front shoulder
# D = Left back shoulder / left trigger
# F = Right back shoulder / right trigger
#

KEYBOARD_CONFIRM = pygame.K_z
KEYBOARD_CANCEL = pygame.K_x

KEYBOARD_BUTTON_X = pygame.K_c
KEYBOARD_BUTTON_Y = pygame.K_v

KEYBOARD_LEFT_SHOULDER_FRONT = (
    pygame.K_a
)

KEYBOARD_RIGHT_SHOULDER_FRONT = (
    pygame.K_s
)

KEYBOARD_LEFT_SHOULDER_BACK = (
    pygame.K_d
)

KEYBOARD_RIGHT_SHOULDER_BACK = (
    pygame.K_f
)

KEYBOARD_PLUS = pygame.K_EQUALS
KEYBOARD_MINUS = pygame.K_MINUS

KEYBOARD_LEFT_STICK_BUTTON = (
    pygame.K_1
)

KEYBOARD_RIGHT_STICK_BUTTON = (
    pygame.K_2
)

KEYBOARD_UP = pygame.K_UP
KEYBOARD_DOWN = pygame.K_DOWN
KEYBOARD_LEFT = pygame.K_LEFT
KEYBOARD_RIGHT = pygame.K_RIGHT

KEYBOARD_ENTER = pygame.K_RETURN
KEYBOARD_ESCAPE = pygame.K_ESCAPE
KEYBOARD_QUIT = pygame.K_q



#
# Controller mappings
#

if IS_WINDOWS:

    CONTROLLER_A = 0
    CONTROLLER_B = 1
    CONTROLLER_X = 2
    CONTROLLER_Y = 3

    CONTROLLER_MINUS = 4
    CONTROLLER_HOME = 5
    CONTROLLER_PLUS = 6

    CONTROLLER_LEFT_STICK_BUTTON = 7
    CONTROLLER_RIGHT_STICK_BUTTON = 8

    CONTROLLER_LEFT_SHOULDER_FRONT = 9
    CONTROLLER_RIGHT_SHOULDER_FRONT = 10

    CONTROLLER_DPAD_UP = 11
    CONTROLLER_DPAD_DOWN = 12
    CONTROLLER_DPAD_LEFT = 13
    CONTROLLER_DPAD_RIGHT = 14

    CONTROLLER_SCREENSHOT = 15

    CONTROLLER_LEFT_SHOULDER_BACK_AXIS = 4
    CONTROLLER_RIGHT_SHOULDER_BACK_AXIS = 5

    CONTROLLER_LEFT_SHOULDER_BACK_BUTTON = None
    CONTROLLER_RIGHT_SHOULDER_BACK_BUTTON = None

elif IS_LINUX:

    CONTROLLER_A = 2
    CONTROLLER_B = 1
    CONTROLLER_X = 3
    CONTROLLER_Y = 0

    CONTROLLER_LEFT_SHOULDER_FRONT = 4
    CONTROLLER_RIGHT_SHOULDER_FRONT = 5

    CONTROLLER_LEFT_SHOULDER_BACK_BUTTON = 6
    CONTROLLER_RIGHT_SHOULDER_BACK_BUTTON = 7

    CONTROLLER_MINUS = 8
    CONTROLLER_PLUS = 9

    CONTROLLER_LEFT_STICK_BUTTON = 10
    CONTROLLER_RIGHT_STICK_BUTTON = 11

    CONTROLLER_HOME = 12
    CONTROLLER_SCREENSHOT = 13

    CONTROLLER_DPAD_LEFT = (
        -1,
        0
    )

    CONTROLLER_DPAD_RIGHT = (
        1,
        0
    )

    CONTROLLER_DPAD_UP = (
        0,
        1
    )

    CONTROLLER_DPAD_DOWN = (
        0,
        -1
    )

    CONTROLLER_LEFT_SHOULDER_BACK_AXIS = None
    CONTROLLER_RIGHT_SHOULDER_BACK_AXIS = None

else:

    CONTROLLER_A = 0
    CONTROLLER_B = 1
    CONTROLLER_X = 2
    CONTROLLER_Y = 3

    CONTROLLER_MINUS = 4
    CONTROLLER_HOME = 5
    CONTROLLER_PLUS = 6

    CONTROLLER_LEFT_STICK_BUTTON = 7
    CONTROLLER_RIGHT_STICK_BUTTON = 8

    CONTROLLER_LEFT_SHOULDER_FRONT = 9
    CONTROLLER_RIGHT_SHOULDER_FRONT = 10

    CONTROLLER_DPAD_UP = 11
    CONTROLLER_DPAD_DOWN = 12
    CONTROLLER_DPAD_LEFT = 13
    CONTROLLER_DPAD_RIGHT = 14

    CONTROLLER_SCREENSHOT = 15

    CONTROLLER_LEFT_SHOULDER_BACK_AXIS = 4
    CONTROLLER_RIGHT_SHOULDER_BACK_AXIS = 5

    CONTROLLER_LEFT_SHOULDER_BACK_BUTTON = None
    CONTROLLER_RIGHT_SHOULDER_BACK_BUTTON = None


#
# Controller axes
#

CONTROLLER_LEFT_STICK_X_AXIS = 0
CONTROLLER_LEFT_STICK_Y_AXIS = 1

CONTROLLER_RIGHT_STICK_X_AXIS = 2
CONTROLLER_RIGHT_STICK_Y_AXIS = 3


#
# Axis thresholds
#

STICK_PRESS_THRESHOLD = 0.8
STICK_RELEASE_THRESHOLD = 0.3

TRIGGER_PRESS_THRESHOLD = 0.8
TRIGGER_RELEASE_THRESHOLD = -0.5


#
# Axis activation state
#
# Each direction fires once when pressed.
# It may fire again after returning toward center.
#

AXIS_ACTIVE = {
    "LEFT_STICK_LEFT": False,
    "LEFT_STICK_RIGHT": False,
    "LEFT_STICK_UP": False,
    "LEFT_STICK_DOWN": False,

    "RIGHT_STICK_LEFT": False,
    "RIGHT_STICK_RIGHT": False,
    "RIGHT_STICK_UP": False,
    "RIGHT_STICK_DOWN": False,

    "LEFT_SHOULDER_BACK": False,
    "RIGHT_SHOULDER_BACK": False
}


#
# Joystick initialization
#

pygame.joystick.init()

for joystick_index in range(
    pygame.joystick.get_count()
):

    joystick = pygame.joystick.Joystick(
        joystick_index
    )

    joystick.init()


def get_controller():

    if (
        pygame.joystick.get_count()
        == 0
    ):

        return None

    joystick = pygame.joystick.Joystick(
        0
    )

    if not joystick.get_init():

        joystick.init()

    return joystick


def get_controller_name():

    joystick = get_controller()

    if joystick is None:
        return None

    return joystick.get_name()


def using_controller():

    return (
        get_controller()
        is not None
    )


def get_launcher_text():

    if using_controller():

        return (
            "D-PAD/STICK = Select    "
            "A = Launch    "
            "B = Exit"
        )

    return (
        "LEFT/RIGHT = Select    "
        "Z/ENTER = Launch    "
        "X/ESC = Exit"
    )


#
# Generic keyboard and controller checks
#

def is_keyboard(
    event,
    key
):

    return (
        event.type == pygame.KEYDOWN
        and
        event.key == key
    )


def is_controller_button(
    event,
    button
):

    if button is None:
        return False

    return (
        event.type == pygame.JOYBUTTONDOWN
        and
        event.button == button
    )


def is_controller_hat(
    event,
    value
):

    return (
        event.type == pygame.JOYHATMOTION
        and
        event.value == value
    )


def is_controller_axis_direction(
    event,
    axis,
    direction,
    state_name
):

    if (
        event.type
        != pygame.JOYAXISMOTION
        or
        event.axis != axis
    ):

        return False

    value = (
        event.value
    )

    if direction < 0:

        if (
            value
            < -STICK_PRESS_THRESHOLD
            and
            not AXIS_ACTIVE[
                state_name
            ]
        ):

            AXIS_ACTIVE[
                state_name
            ] = True

            return True

        if (
            value
            > -STICK_RELEASE_THRESHOLD
        ):

            AXIS_ACTIVE[
                state_name
            ] = False

    else:

        if (
            value
            > STICK_PRESS_THRESHOLD
            and
            not AXIS_ACTIVE[
                state_name
            ]
        ):

            AXIS_ACTIVE[
                state_name
            ] = True

            return True

        if (
            value
            < STICK_RELEASE_THRESHOLD
        ):

            AXIS_ACTIVE[
                state_name
            ] = False

    return False


def is_controller_trigger(
    event,
    axis,
    state_name
):

    if axis is None:
        return False

    if (
        event.type
        != pygame.JOYAXISMOTION
        or
        event.axis != axis
    ):

        return False

    if (
        event.value
        > TRIGGER_PRESS_THRESHOLD
        and
        not AXIS_ACTIVE[
            state_name
        ]
    ):

        AXIS_ACTIVE[
            state_name
        ] = True

        return True

    if (
        event.value
        < TRIGGER_RELEASE_THRESHOLD
    ):

        AXIS_ACTIVE[
            state_name
        ] = False

    return False


#
# Left stick
#

def is_controller_left_stick_left(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_LEFT_STICK_X_AXIS,
        -1,
        "LEFT_STICK_LEFT"
    )


def is_controller_left_stick_right(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_LEFT_STICK_X_AXIS,
        1,
        "LEFT_STICK_RIGHT"
    )


def is_controller_left_stick_up(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_LEFT_STICK_Y_AXIS,
        -1,
        "LEFT_STICK_UP"
    )


def is_controller_left_stick_down(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_LEFT_STICK_Y_AXIS,
        1,
        "LEFT_STICK_DOWN"
    )


#
# Right stick
#

def is_controller_right_stick_left(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_RIGHT_STICK_X_AXIS,
        -1,
        "RIGHT_STICK_LEFT"
    )


def is_controller_right_stick_right(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_RIGHT_STICK_X_AXIS,
        1,
        "RIGHT_STICK_RIGHT"
    )


def is_controller_right_stick_up(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_RIGHT_STICK_Y_AXIS,
        -1,
        "RIGHT_STICK_UP"
    )


def is_controller_right_stick_down(
    event
):

    return is_controller_axis_direction(
        event,
        CONTROLLER_RIGHT_STICK_Y_AXIS,
        1,
        "RIGHT_STICK_DOWN"
    )


#
# D-pad
#

def is_controller_dpad_left(
    event
):

    if IS_LINUX:

        return is_controller_hat(
            event,
            CONTROLLER_DPAD_LEFT
        )

    return is_controller_button(
        event,
        CONTROLLER_DPAD_LEFT
    )


def is_controller_dpad_right(
    event
):

    if IS_LINUX:

        return is_controller_hat(
            event,
            CONTROLLER_DPAD_RIGHT
        )

    return is_controller_button(
        event,
        CONTROLLER_DPAD_RIGHT
    )


def is_controller_dpad_up(
    event
):

    if IS_LINUX:

        return is_controller_hat(
            event,
            CONTROLLER_DPAD_UP
        )

    return is_controller_button(
        event,
        CONTROLLER_DPAD_UP
    )


def is_controller_dpad_down(
    event
):

    if IS_LINUX:

        return is_controller_hat(
            event,
            CONTROLLER_DPAD_DOWN
        )

    return is_controller_button(
        event,
        CONTROLLER_DPAD_DOWN
    )


#
# Direction actions
#

def is_up(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_UP
        )
        or
        is_controller_left_stick_up(
            event
        )
        or
        is_controller_dpad_up(
            event
        )
    )


def is_down(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_DOWN
        )
        or
        is_controller_left_stick_down(
            event
        )
        or
        is_controller_dpad_down(
            event
        )
    )


def is_left(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_LEFT
        )
        or
        is_controller_left_stick_left(
            event
        )
        or
        is_controller_dpad_left(
            event
        )
    )


def is_right(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_RIGHT
        )
        or
        is_controller_left_stick_right(
            event
        )
        or
        is_controller_dpad_right(
            event
        )
    )


#
# Face-button actions
#

def is_confirm(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_CONFIRM
        )
        or
        is_keyboard(
            event,
            KEYBOARD_ENTER
        )
        or
        is_controller_button(
            event,
            CONTROLLER_A
        )
    )


def is_cancel(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_CANCEL
        )
        or
        is_keyboard(
            event,
            KEYBOARD_ESCAPE
        )
        or
        is_controller_button(
            event,
            CONTROLLER_B
        )
    )


def is_cx(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_BUTTON_X
        )
        or
        is_controller_button(
            event,
            CONTROLLER_X
        )
    )


def is_vy(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_BUTTON_Y
        )
        or
        is_controller_button(
            event,
            CONTROLLER_Y
        )
    )


def is_cvxy(
    event
):

    return (
        is_cx(
            event
        )
        or
        is_vy(
            event
        )
    )


#
# Front shoulder actions
#

def is_left_shoulder_front(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_LEFT_SHOULDER_FRONT
        )
        or
        is_controller_button(
            event,
            CONTROLLER_LEFT_SHOULDER_FRONT
        )
    )


def is_right_shoulder_front(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_RIGHT_SHOULDER_FRONT
        )
        or
        is_controller_button(
            event,
            CONTROLLER_RIGHT_SHOULDER_FRONT
        )
    )


#
# Back shoulder / trigger actions
#

def is_left_shoulder_back(
    event
):

    keyboard_pressed = is_keyboard(
        event,
        KEYBOARD_LEFT_SHOULDER_BACK
    )

    if IS_LINUX:

        controller_pressed = (
            is_controller_button(
                event,
                CONTROLLER_LEFT_SHOULDER_BACK_BUTTON
            )
        )

    else:

        controller_pressed = (
            is_controller_trigger(
                event,
                CONTROLLER_LEFT_SHOULDER_BACK_AXIS,
                "LEFT_SHOULDER_BACK"
            )
        )

    return (
        keyboard_pressed
        or
        controller_pressed
    )


def is_right_shoulder_back(
    event
):

    keyboard_pressed = is_keyboard(
        event,
        KEYBOARD_RIGHT_SHOULDER_BACK
    )

    if IS_LINUX:

        controller_pressed = (
            is_controller_button(
                event,
                CONTROLLER_RIGHT_SHOULDER_BACK_BUTTON
            )
        )

    else:

        controller_pressed = (
            is_controller_trigger(
                event,
                CONTROLLER_RIGHT_SHOULDER_BACK_AXIS,
                "RIGHT_SHOULDER_BACK"
            )
        )

    return (
        keyboard_pressed
        or
        controller_pressed
    )


#
# Plus, minus, and stick-button actions
#

def is_plus(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_PLUS
        )
        or
        is_controller_button(
            event,
            CONTROLLER_PLUS
        )
    )


def is_minus(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_MINUS
        )
        or
        is_controller_button(
            event,
            CONTROLLER_MINUS
        )
    )


def is_left_stick_button(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_LEFT_STICK_BUTTON
        )
        or
        is_controller_button(
            event,
            CONTROLLER_LEFT_STICK_BUTTON
        )
    )


def is_right_stick_button(
    event
):

    return (
        is_keyboard(
            event,
            KEYBOARD_RIGHT_STICK_BUTTON
        )
        or
        is_controller_button(
            event,
            CONTROLLER_RIGHT_STICK_BUTTON
        )
    )


#
# Right-stick actions
#

def is_right_stick_left(
    event
):

    return is_controller_right_stick_left(
        event
    )


def is_right_stick_right(
    event
):

    return is_controller_right_stick_right(
        event
    )


def is_right_stick_up(
    event
):

    return is_controller_right_stick_up(
        event
    )


def is_right_stick_down(
    event
):

    return is_controller_right_stick_down(
        event
    )


#
# Global actions
#

def is_quit(
    event
):

    return (
        event.type == pygame.QUIT
        or
        is_keyboard(
            event,
            KEYBOARD_QUIT
        )
        or
        is_controller_button(
            event,
            CONTROLLER_HOME
        )
    )


def is_mute_toggle(
    event
):

    return is_right_shoulder_front(
        event
    )


def is_skip_song(
    event
):

    return is_left_shoulder_front(
        event
    )