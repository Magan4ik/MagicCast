from copy import deepcopy

import pyglet
from pyglet.window import key
from resources import *

WIDTH = 800
HEIGHT = 500
FULLSCREEN = False
FPS = 120
DEFAULT_MASS = 5
FRICTION_MU = 0.5

KEYBOARD = key.KeyStateHandler()
ALL_OBJECTS = pyglet.graphics.Batch()

# PLAYER SETTINGS
PLAYER_MASS = 20
PLAYER_ELASTIC = 1
PLAYER_JUMP_POWER = 250

BACKGROUND_IMAGE = pyglet.image.load('textures/map/background_game.png')
