from base_classes.game_sprite import GameSprite
from settings import *


class Chunk:
    def __init__(self, x):
        self.batch = pyglet.graphics.Batch()
        self.sprites: list[GameSprite] = []
        self.x = x
        # self.old_len = 0
        # self.pos_cache = (float('inf'), float('inf'))

    def add_sprite(self, sprite: GameSprite):
        sprite.batch = self.batch
        self.sprites.append(sprite)

    # def get_position(self):
    #     if len(self.sprites) != self.old_len:
    #         x = float('inf')
    #         y = float('inf')
    #         for sprite in self.sprites:
    #             if sprite.x < x:
    #                 x = sprite.x
    #             if sprite.y < y:
    #                 y = sprite.y
    #         self.old_len = len(self.sprites)
    #         self.pos_cache = x, y
    #     else:
    #         x, y = self.pos_cache
    #
    #     return x, y

    def draw(self):
        self.batch.draw()
