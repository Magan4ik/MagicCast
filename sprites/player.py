from settings import *
from base_classes.game_sprite import GameSprite
from pyglet.math import Vec2


class Player(GameSprite):
    def __init__(self, img: list[pyglet.image.AbstractImage],
                 x: float, y: float, width: int, height: int, speed: int,
                 batch: pyglet.graphics.Batch):
        super().__init__(img, x, y, width, height, batch, mass=PLAYER_MASS, elastic=PLAYER_ELASTIC)
        self.speed = speed

    def control(self, dt):
        if KEYBOARD[key.D]:
            self.x += self.speed * dt
            self.scale_x = 1
        if KEYBOARD[key.A]:
            self.x -= self.speed * dt
            self.scale_x = -1
        if KEYBOARD[key.SPACE]:
            self.velocity = Vec2(self.velocity.x, PLAYER_JUMP_POWER)

    def handle(self, dt):
        self.hitbox.center = self.position
        self.control(dt)
        acceleration = self.calculate_acceleration()
        self.update_velocity(acceleration, dt)
        self.update_position()
