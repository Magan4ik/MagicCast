from copy import deepcopy

import pyglet
from pyglet.window import key
from resources import *

WIDTH = 1500
HEIGHT = 800
FULLSCREEN = False
FPS = 120
KEYBOARD = key.KeyStateHandler()
ALL_OBJECTS = pyglet.graphics.Batch()

#  PHYS SETTINGS
DEFAULT_MASS = 5
DEFAULT_FRICTION_MU = 0.8


#  MAP SETTINGS
MAP_CELL_SIZE = 50
CHUNK_RENDER_RANGE = 10
CHUNK_COLLIDE_RANGE = 1
CHUNK_SIZE = 5
TILE_GROUP = pyglet.graphics.Group()


#  PLAYER SETTINGS
PLAYER_MASS = 20
PLAYER_ELASTIC = 0.8
PLAYER_JUMP_POWER = 250
PLAYER_SPEED = 150
