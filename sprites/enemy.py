from typing import Optional

from base_classes.entity import Entity, HealthBar
from settings.settings import *
from base_classes.game_sprite import GameSprite
from pyglet.math import Vec2


class Enemy(Entity):
    def __init__(self, img,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 speed: int, hp: int = 100,
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        super().__init__(img, x, y, batch, speed, hp, mass=mass, elastic=elastic)
        self.hpbar = HealthBar(self, hp, hp)

    def handle(self, dt):
        self.hpbar.hp = self.hp
        self.hpbar.update()
        super().handle(dt)
