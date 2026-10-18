import os
import pygame
import socket
from app import app
from input_manager import *

W_SCREEN_LOGICAL = 240

H_SCREEN_LOGICAL = 160

TEXT_WINDOW_TITLE = "Pkmn Battle Simulator V2"
TEXT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATE_LAUNCHER_MENU    = 0
STATE_LAN_HOST_JOIN    = 1
STATE_LAN_HOST         = 2
STATE_LAN_JOIN         = 3
STATE_LAN_TEAM_PREVIEW = 4

COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_ALPHA_0 = (255, 0, 228)

NUM_TARGET_FPS = 30
NUM_DISCOVERY_PORT = 55556
NUM_PORT = 5000