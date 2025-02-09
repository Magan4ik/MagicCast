from typing import Optional

from base_classes.entity import Entity
from settings.settings import *
from base_classes.game_sprite import GameSprite
from pyglet.math import Vec2


class Player(Entity):
    def __init__(self, img,
                 x: float, y: float, batch: Optional[pyglet.graphics.Batch],
                 speed: int, hp: int = 100,
                 mass: float = DEFAULT_MASS, elastic: float = 0, *args, **kwargs):
        super().__init__(img, x, y, batch, speed, hp, mass=PLAYER_MASS, elastic=PLAYER_ELASTIC)

    def control(self, dt):
        if KEYBOARD[key.D]:
            if abs(self.velocity.x) < self.speed:
                self.velocity = Vec2(self.speed, self.velocity.y)
            self.scale_x = 1
        elif KEYBOARD[key.A]:
            if abs(self.velocity.x) < self.speed:
                self.velocity = Vec2(-self.speed, self.velocity.y)
            self.update_forces(move=Vec2(-self.speed, 0))
            self.scale_x = -1
        else:
            self.update_forces(move=Vec2(0, 0))

        if KEYBOARD[key.SPACE]:
            self.velocity = Vec2(self.velocity.x, PLAYER_JUMP_POWER)
