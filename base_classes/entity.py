from typing import Optional

import pyglet.sprite

from settings.settings import *

from base_classes.game_sprite import GameSprite


class HealthBar(pyglet.shapes.Rectangle):
    def __init__(self, entity: "Entity", hp: int, max_hp: int):
        x = entity.left
        y = entity.top + 10
        width = entity.width
        height = 10
        super().__init__(x, y, width, height, (255, 100, 100), batch=entity.batch)
        self.max_width = self.width
        self.entity = entity
        self.hp = hp
        self.max_hp = max_hp

    def update_bar(self):
        percent = self.hp / self.max_hp
        self.width = max(0, percent * self.max_width)

    def update(self):
        self.update_bar()
        self.batch = self.entity.batch
        self.x = self.entity.left
        self.y = self.entity.top + 10


class Entity(GameSprite):
    def __init__(self, img,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 speed: int, hp: int = 100,
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        super().__init__(img, x, y, batch=batch, mass=mass, elastic=elastic, *args, **kwargs)
        self.max_hp = hp
        self._hp = hp
        self.speed = speed

    def control(self, dt):
        pass

    def handle(self, dt):
        self.control(dt)
        acceleration = self.calculate_acceleration()
        self.update_velocity(acceleration, dt)
        self.update_position(dt)
        self.spell_channeling()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = min(self.max_hp, max(0, value))
