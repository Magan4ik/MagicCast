from copy import deepcopy

import pyglet
from pyglet.window import key
from resources import *

WIDTH = 1500
HEIGHT = 800
FULLSCREEN = False
FPS = 120
DEFAULT_MASS = 5
FRICTION_MU = 0.8

MAP_CELL_SIZE = 50
CHUNK_RENDER_RANGE = 20
CHUNK_SIZE = 2

KEYBOARD = key.KeyStateHandler()
ALL_OBJECTS = pyglet.graphics.Batch()

# PLAYER SETTINGS
PLAYER_MASS = 20
PLAYER_ELASTIC = 0.8
PLAYER_JUMP_POWER = 250

BACKGROUND_IMAGE_PATH = 'textures/map/background_game.png'
