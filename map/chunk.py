from base_classes.game_sprite import GameSprite
from settings.settings import *


class Chunk:
    def __init__(self, x):
        self.batch = pyglet.graphics.Batch()
        self.sprites: list[GameSprite] = []
        self.x = x

    def add_sprite(self, sprite: GameSprite):
        sprite.batch = self.batch
        self.sprites.append(sprite)

    def draw(self):
        self.batch.draw()
