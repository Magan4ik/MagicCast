from base_classes.entity import Entity
from base_classes.game_sprite import GameSprite
from settings.settings import *


class Chunk:
    def __init__(self, x):
        self.batch = pyglet.graphics.Batch()
        self.sprites: list[GameSprite] = []
        self.entities: list[Entity] = []
        self.x = x

    def add_sprite(self, sprite: GameSprite):
        sprite.batch = self.batch
        self.sprites.append(sprite)

    def add_entity(self, entity: Entity):
        entity.batch = self.batch
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        entity.batch = None
        self.entities.remove(entity)

    def update_entities(self, dt):
        for entity in self.entities:
            entity.handle(dt)

    def draw(self):
        self.batch.draw()
