from copy import deepcopy

import pyglet
from pyglet.window import key
from resources import *

WIDTH = 800
HEIGHT = 500
FULLSCREEN = False
FPS = 60
DEFAULT_MASS = 5

KEYBOARD = key.KeyStateHandler()
ALL_OBJECTS = pyglet.graphics.Batch()

# PLAYER SETTINGS
PLAYER_MASS = 10
PLAYER_ELASTIC = 0.8
PLAYER_JUMP_POWER = 5

BACKGROUND_IMAGE = pyglet.image.load('textures/map/background_game.png')
