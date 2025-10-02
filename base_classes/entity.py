from typing import Optional

from settings.settings import *

from base_classes.game_sprite import GameSprite
from ui.damage_numbers import DamageNumber
from random import randint


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
