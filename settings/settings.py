from pyglet.window import key
from settings.resources import *

WIDTH = 1500
HEIGHT = 800
FULLSCREEN = False
FPS = 120
KEYBOARD = key.KeyStateHandler()
ALL_OBJECTS = pyglet.graphics.Batch()

KEY_NUMBERS = {
    key._1: 1,
    key._2: 2,
    key._3: 3,
    key._4: 4,
    key._5: 5,
    key._6: 6,
    key._7: 7,
    key._8: 8,
    key._9: 9,
}
SPELL_KEYS = {
    key.Z: 0,
    key.X: 1,
    key.C: 2,
    key.V: 3,
    key.B: 4
}

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

