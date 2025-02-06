from typing import Optional

from settings.settings import *
from base_classes.game_sprite import GameSprite
from pyglet.math import Vec2


class Player(GameSprite):
    def __init__(self, img: list[pyglet.image.AbstractImage],
                 x: float, y: float, speed: int,
                 batch: Optional[pyglet.graphics.Batch]):
        super().__init__(img, x, y, batch, mass=PLAYER_MASS, elastic=PLAYER_ELASTIC)
        self.speed = speed

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

    def handle(self, dt):
        self.control(dt)
        acceleration = self.calculate_acceleration()
        self.update_velocity(acceleration, dt)
        self.update_position(dt)
        self.spell_channeling()
