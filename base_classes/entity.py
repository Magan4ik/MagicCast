from typing import Optional

import pyglet.sprite

from settings.settings import *

from base_classes.game_sprite import GameSprite
from ui.damage_numbers import DamageNumber
from random import randint


class HealthBar(pyglet.shapes.Rectangle):
    def __init__(self, entity: "Entity", hp: int, max_hp: int):
        x = entity.left
        y = entity.top + 10
        width = entity.width
        height = 10
        self.group_back = pyglet.graphics.Group(order=1)
        self.group_for = pyglet.graphics.Group(order=0)
        super().__init__(x, y, width, height, (255, 100, 100), batch=entity.batch, group=self.group_back)
        self.max_width = self.width

        self.entity = entity
        self.hp = hp
        self.max_hp = max_hp
        self.sep_lines = list()
        self.create_separators()

    def create_separators(self):
        self.sep_lines.clear()
        num_separators = self.max_hp // HPBAR_SEP_VALUE
        sep_width = self.max_width // num_separators
        for i in range(1, num_separators):
            sep_x = self.x + i * sep_width
            line = pyglet.shapes.Line(sep_x, self.y, sep_x, self.y + self.height, thickness=1,
                                      batch=self.entity.batch, color=(150, 50, 50) if i % 5 != 0 else (25, 10, 10),
                                      group=self.group_for)
            self.sep_lines.append(line)

    def update_bar(self):
        num_separators = self.max_hp // HPBAR_SEP_VALUE
        sep_width = self.max_width // num_separators
        percent = self.hp / self.max_hp
        self.width = max(0, percent * self.max_width)
        for i, line in enumerate(self.sep_lines, 1):
            line.x = self.x + i * sep_width
            line.x2 = self.x + i * sep_width
            line.y = self.y
            line.y2 = self.y + self.height
            if line.x > self.x + self.width:
                line.batch = None
            else:
                if line.batch is not self.entity.batch:
                    line.batch = self.entity.batch

    def update(self):
        self.x = self.entity.left
        self.y = self.entity.top + 10
        self.update_bar()
        if self.batch is not self.entity.batch:
            self.batch = self.entity.batch


class Entity(GameSprite):
    def __init__(self, img,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 speed: int, hp: int = 100,
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        super().__init__(img, x, y, batch=batch, mass=mass, elastic=elastic, *args, **kwargs)
        self.max_hp = hp
        self._hp = hp
        self.speed = speed
        self.damage_numbers = []

    def take_damage(self, damage: float):
        self.hp -= damage
        self.damage_numbers.append(
            DamageNumber(randint(int(self.x - self.width // 4), int(self.x + self.width // 4)),
                         randint(int(self.y + self.width // 4), int(self.y + self.width)), damage, batch=ALL_OBJECTS,
                         lifespan=1)
        )

    def control(self, dt):
        pass

    def update_damage_numbers(self, dt):
        for dn in self.damage_numbers:
            dn.update(dt)
            if dn.is_finished:
                self.damage_numbers.remove(dn)

    def handle(self, dt):
        self.control(dt)
        acceleration = self.calculate_acceleration()
        self.update_velocity(acceleration, dt)
        self.update_position(dt)
        self.spell_channeling()
        self.handle_effect()
        self.update_damage_numbers(dt)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = min(self.max_hp, max(0, value))
